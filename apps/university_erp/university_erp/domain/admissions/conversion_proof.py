from __future__ import annotations

import frappe

from university_erp.domain.admissions.merit_seat_proof import run_merit_seat_proof


P43_DOCTYPES = [
	"Admission Confirmation",
	"Admission Student Conversion",
]


def run_conversion_proof() -> dict:
	"""Create and validate a synthetic P4.3 admission confirmation and conversion."""

	merit = run_merit_seat_proof()
	confirmation = _ensure_submitted(
		"Admission Confirmation",
		{"seat_offer": merit["accepted_offer"]},
		{
			"seat_offer": merit["accepted_offer"],
			"status": "Draft",
			"document_gate_passed": 1,
			"fee_gate_passed": 1,
			"confirmed_on": "2026-01-27 10:00:00",
			"notes": "Synthetic P4.3 confirmation proof",
		},
	)
	conversion = _ensure_submitted(
		"Admission Student Conversion",
		{"admission_confirmation": confirmation},
		{
			"admission_confirmation": confirmation,
			"status": "Draft",
			"conversion_date": "2026-01-27",
			"idempotency_key": "P43-CONVERT-PRIMARY",
			"notes": "Synthetic P4.3 conversion proof",
		},
	)
	second_conversion = _ensure_submitted(
		"Admission Student Conversion",
		{"admission_confirmation": confirmation},
		{
			"admission_confirmation": confirmation,
			"status": "Draft",
			"conversion_date": "2026-01-27",
			"idempotency_key": "P43-CONVERT-PRIMARY",
		},
	)
	student = frappe.db.get_value("Admission Student Conversion", conversion, "student")
	student_applicant = frappe.db.get_value(
		"Admission Student Conversion", conversion, "student_applicant"
	)
	program_enrollment = frappe.db.get_value(
		"Admission Student Conversion", conversion, "program_enrollment"
	)
	identity_issuance = frappe.db.get_value(
		"Admission Student Conversion", conversion, "identity_issuance"
	)
	identity_profile = frappe.db.get_value(
		"Student Identity Issuance", identity_issuance, "identity_profile"
	)

	validation_checks = {
		"waitlist_confirmation_rejected": _rejects_waitlist_confirmation(merit["waitlist_offer"]),
		"missing_gate_confirmation_rejected": _rejects_missing_gate_confirmation(
			merit["accepted_offer"]
		),
		"duplicate_conversion_rejected": _rejects_duplicate_conversion(confirmation),
	}
	audit_versions = _ensure_audit_version("Student Identity Profile", identity_profile)

	result = {
		"doctype_count": _count_p43_doctypes(),
		"permission_count": _count_required_permissions(),
		"confirmation": confirmation,
		"confirmation_status": frappe.db.get_value("Admission Confirmation", confirmation, "status"),
		"conversion": conversion,
		"second_conversion": second_conversion,
		"conversion_status": frappe.db.get_value("Admission Student Conversion", conversion, "status"),
		"student_applicant": student_applicant,
		"student": student,
		"student_applicant_status": frappe.db.get_value(
			"Student Applicant", student_applicant, "application_status"
		),
		"student_count": frappe.db.count("Student", {"student_applicant": student_applicant}),
		"program_enrollment": program_enrollment,
		"program_enrollment_count": frappe.db.count(
			"Program Enrollment", {"student": student, "docstatus": 1}
		),
		"identity_issuance": identity_issuance,
		"identity_issuance_status": frappe.db.get_value(
			"Student Identity Issuance", identity_issuance, "status"
		),
		"identity_profile": identity_profile,
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_submitted(doctype: str, filters: dict, values: dict) -> str:
	if existing := frappe.db.exists(doctype, filters):
		doc = frappe.get_doc(doctype, existing)
	else:
		doc = frappe.get_doc({"doctype": doctype, **values})
		doc.insert(ignore_permissions=True)
	if doc.docstatus == 0:
		doc.submit()
	return doc.name


def _rejects_waitlist_confirmation(waitlist_offer: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Admission Confirmation",
				"seat_offer": waitlist_offer,
				"document_gate_passed": 1,
				"fee_gate_passed": 1,
				"confirmed_on": "2026-01-27 10:10:00",
			}
		).insert(ignore_permissions=True)
	except frappe.DuplicateEntryError:
		frappe.clear_messages()
		return True
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_missing_gate_confirmation(accepted_offer: str) -> bool:
	if existing := frappe.db.exists("Admission Confirmation", {"seat_offer": accepted_offer}):
		confirmed = frappe.get_doc("Admission Confirmation", existing)
		if confirmed.docstatus == 1:
			return True
	try:
		doc = frappe.get_doc(
			{
				"doctype": "Admission Confirmation",
				"seat_offer": accepted_offer,
				"document_gate_passed": 1,
				"fee_gate_passed": 0,
				"confirmed_on": "2026-01-27 10:20:00",
			}
		)
		doc.insert(ignore_permissions=True)
		doc.submit()
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_duplicate_conversion(confirmation: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Admission Student Conversion",
				"admission_confirmation": confirmation,
				"conversion_date": "2026-01-27",
				"idempotency_key": "P43-CONVERT-DUPLICATE",
			}
		).insert(ignore_permissions=True)
	except frappe.DuplicateEntryError:
		frappe.clear_messages()
		return True
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P4.3 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p43_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P43_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P43_DOCTYPES],
			"role": ["in", ["System Manager", "Academics User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P43_DOCTYPES):
		frappe.throw("P4.3 proof failed: expected custom confirmation/conversion DocTypes.")
	if result["permission_count"] < len(P43_DOCTYPES) * 2:
		frappe.throw("P4.3 proof failed: expected System Manager and Academics User permissions.")
	if result["confirmation_status"] != "Confirmed":
		frappe.throw("P4.3 proof failed: admission confirmation was not confirmed.")
	if result["conversion_status"] != "Converted":
		frappe.throw("P4.3 proof failed: admission conversion was not converted.")
	if result["conversion"] != result["second_conversion"]:
		frappe.throw("P4.3 proof failed: repeated conversion did not reuse the same record.")
	if not result["student"] or result["student_count"] != 1:
		frappe.throw("P4.3 proof failed: expected exactly one Student for the applicant.")
	if not result["program_enrollment"] or result["program_enrollment_count"] != 1:
		frappe.throw("P4.3 proof failed: expected exactly one submitted Program Enrollment.")
	if result["identity_issuance_status"] != "Issued":
		frappe.throw("P4.3 proof failed: identity issuance was not issued.")
	if result["student_applicant_status"] != "Admitted":
		frappe.throw("P4.3 proof failed: Student Applicant was not marked Admitted.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P4.3 proof failed: expected invalid records to be rejected.")
	if result["audit_versions"] < 1:
		frappe.throw("P4.3 proof failed: expected audit Version evidence.")
