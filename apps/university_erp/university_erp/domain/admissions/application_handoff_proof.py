from __future__ import annotations

import json

import frappe

from university_erp.domain.academic.master_proof import run_master_proof


P41_DOCTYPES = [
	"Admission Application Draft",
	"Admission Application Form Version",
	"CRM Application Handoff",
]


def run_application_handoff_proof() -> dict:
	"""Create and validate a synthetic P4.1 CRM-to-application handoff."""

	academic = run_master_proof()
	status = _ensure_doc("CRM Lead Status", {"lead_status": "New Lead"}, {"lead_status": "New Lead"})
	lead = _ensure_crm_lead(status)
	form_version = _ensure_form_version(academic)
	draft = _ensure_application_draft(lead, form_version)
	_save_draft_again(draft)
	handoff = _ensure_submitted(
		"CRM Application Handoff",
		{"crm_lead": lead},
		{
			"crm_lead": lead,
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"academic_term": academic["academic_term"],
			"form_version": form_version,
			"application_draft": draft,
			"handoff_date": "2026-01-20",
			"idempotency_key": "P41-HANDOFF-LEAD-0001",
			"status": "Pending",
			"notes": "Synthetic P4.1 handoff proof",
		},
	)
	student_applicant = frappe.db.get_value("CRM Application Handoff", handoff, "student_applicant")

	validation_checks = {
		"invalid_form_schema_rejected": _rejects_invalid_form_schema(academic),
		"invalid_draft_payload_rejected": _rejects_invalid_draft_payload(form_version, lead),
		"duplicate_lead_handoff_rejected": _rejects_duplicate_lead_handoff(
			lead, academic, form_version, draft
		),
		"duplicate_idempotency_key_rejected": _rejects_duplicate_idempotency_key(
			academic, form_version
		),
	}
	audit_versions = _ensure_audit_version("Admission Application Draft", draft)

	result = {
		"doctype_count": _count_p41_doctypes(),
		"permission_count": _count_required_permissions(),
		"crm_lead": lead,
		"lead_converted": frappe.db.get_value("CRM Lead", lead, "converted"),
		"form_version": form_version,
		"application_draft": draft,
		"draft_status": frappe.db.get_value("Admission Application Draft", draft, "status"),
		"draft_student_applicant": frappe.db.get_value(
			"Admission Application Draft", draft, "student_applicant"
		),
		"handoff": handoff,
		"handoff_status": frappe.db.get_value("CRM Application Handoff", handoff, "status"),
		"student_applicant": student_applicant,
		"student_applicant_count": frappe.db.count(
			"Student Applicant", {"student_email_id": "p41.proof@example.invalid"}
		),
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_crm_lead(status: str) -> str:
	if lead := frappe.db.exists("CRM Lead", {"email": "p41.proof@example.invalid"}):
		return lead
	doc = frappe.get_doc(
		{
			"doctype": "CRM Lead",
			"naming_series": "CRM-LEAD-.YYYY.-",
			"first_name": "P41",
			"last_name": "Proof",
			"lead_name": "P41 Proof Lead",
			"email": "p41.proof@example.invalid",
			"mobile_no": "9999900410",
			"status": status,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_secondary_crm_lead(status: str) -> str:
	if lead := frappe.db.exists("CRM Lead", {"email": "p41.secondary@example.invalid"}):
		return lead
	doc = frappe.get_doc(
		{
			"doctype": "CRM Lead",
			"naming_series": "CRM-LEAD-.YYYY.-",
			"first_name": "P41",
			"last_name": "Secondary",
			"lead_name": "P41 Secondary Lead",
			"email": "p41.secondary@example.invalid",
			"mobile_no": "9999900411",
			"status": status,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_form_version(academic: dict) -> str:
	return _ensure_doc(
		"Admission Application Form Version",
		{"form_code": "P41-PILOT", "version": "2026.1"},
		{
			"form_code": "P41-PILOT",
			"version": "2026.1",
			"status": "Published",
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"published_on": "2026-01-20",
			"form_schema": json.dumps(
				{
					"fields": [
						{"fieldname": "first_name", "fieldtype": "Data", "required": True},
						{"fieldname": "student_email_id", "fieldtype": "Email", "required": True},
						{"fieldname": "student_mobile_number", "fieldtype": "Phone", "required": True},
					]
				},
				sort_keys=True,
			),
		},
	)


def _ensure_application_draft(lead: str, form_version: str) -> str:
	return _ensure_doc(
		"Admission Application Draft",
		{"crm_lead": lead, "form_version": form_version},
		{
			"crm_lead": lead,
			"form_version": form_version,
			"status": "Draft",
			"resume_token_hash": "p41-resume-token-hash",
			"last_saved_on": "2026-01-20 09:00:00",
			"draft_payload": json.dumps(
				{
					"first_name": "P41",
					"last_name": "Proof",
					"student_email_id": "p41.proof@example.invalid",
				},
				sort_keys=True,
			),
		},
	)


def _save_draft_again(draft: str) -> None:
	doc = frappe.get_doc("Admission Application Draft", draft)
	payload = json.loads(doc.draft_payload)
	payload["student_mobile_number"] = "9999900410"
	doc.draft_payload = json.dumps(payload, sort_keys=True)
	doc.last_saved_on = "2026-01-20 09:15:00"
	doc.save(ignore_permissions=True)


def _ensure_doc(doctype: str, filters: dict, values: dict) -> str:
	if existing := frappe.db.exists(doctype, filters):
		return existing
	doc = frappe.get_doc({"doctype": doctype, **values})
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_submitted(doctype: str, filters: dict, values: dict) -> str:
	if existing := frappe.db.exists(doctype, filters):
		doc = frappe.get_doc(doctype, existing)
	else:
		doc = frappe.get_doc({"doctype": doctype, **values})
		doc.insert(ignore_permissions=True)
	if doc.docstatus == 0:
		doc.submit()
	return doc.name


def _rejects_invalid_form_schema(academic: dict) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Admission Application Form Version",
				"form_code": "P41-BAD",
				"version": "2026.1",
				"status": "Published",
				"program": academic["program"],
				"academic_year": academic["academic_year"],
				"published_on": "2026-01-20",
				"form_schema": "{}",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_invalid_draft_payload(form_version: str, lead: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Admission Application Draft",
				"form_version": form_version,
				"crm_lead": lead,
				"resume_token_hash": "p41-invalid-payload",
				"last_saved_on": "2026-01-20 09:30:00",
				"draft_payload": "[]",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_duplicate_lead_handoff(
	lead: str, academic: dict, form_version: str, draft: str
) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "CRM Application Handoff",
				"crm_lead": lead,
				"program": academic["program"],
				"academic_year": academic["academic_year"],
				"academic_term": academic["academic_term"],
				"form_version": form_version,
				"application_draft": draft,
				"handoff_date": "2026-01-20",
				"idempotency_key": "P41-HANDOFF-DUPLICATE-LEAD",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_duplicate_idempotency_key(academic: dict, form_version: str) -> bool:
	status = _ensure_doc("CRM Lead Status", {"lead_status": "New Lead"}, {"lead_status": "New Lead"})
	try:
		frappe.get_doc(
			{
				"doctype": "CRM Application Handoff",
				"crm_lead": _ensure_secondary_crm_lead(status),
				"program": academic["program"],
				"academic_year": academic["academic_year"],
				"academic_term": academic["academic_term"],
				"form_version": form_version,
				"handoff_date": "2026-01-20",
				"idempotency_key": "P41-HANDOFF-LEAD-0001",
			}
		).insert(ignore_permissions=True)
	except frappe.UniqueValidationError:
		frappe.clear_messages()
		return True
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P4.1 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p41_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P41_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P41_DOCTYPES],
			"role": ["in", ["System Manager", "Academics User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P41_DOCTYPES):
		frappe.throw("P4.1 proof failed: expected custom admissions DocTypes.")
	if result["permission_count"] < len(P41_DOCTYPES) * 2:
		frappe.throw("P4.1 proof failed: expected System Manager and Academics User permissions.")
	if result["handoff_status"] != "Application Created":
		frappe.throw("P4.1 proof failed: handoff did not create application.")
	if not result["student_applicant"] or result["student_applicant_count"] != 1:
		frappe.throw("P4.1 proof failed: handoff was not idempotent for Student Applicant.")
	if result["draft_status"] != "Submitted":
		frappe.throw("P4.1 proof failed: draft was not submitted by handoff.")
	if result["draft_student_applicant"] != result["student_applicant"]:
		frappe.throw("P4.1 proof failed: draft was not linked to created applicant.")
	if not result["lead_converted"]:
		frappe.throw("P4.1 proof failed: CRM Lead was not marked converted.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P4.1 proof failed: expected invalid records to be rejected.")
	if result["audit_versions"] < 1:
		frappe.throw("P4.1 proof failed: expected audit Version evidence for application draft.")
