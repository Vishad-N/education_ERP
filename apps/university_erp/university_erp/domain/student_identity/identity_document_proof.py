from __future__ import annotations

import frappe

from university_erp.domain.academic.master_proof import run_master_proof


P32_DOCTYPES = [
	"Communication Consent",
	"Document Expiry Review",
	"Document Rejection Reason",
	"Document Replacement Request",
	"Document Scan Result",
	"Document Requirement Matrix",
	"Document Verification",
	"Duplicate Candidate",
	"Student Category History",
	"Student Correction Request",
	"Student Data Access Log",
	"Student Document",
	"Student Document Type",
	"Student Guardian Relationship",
	"Student Identity Profile",
	"Student Identity Issuance",
	"Student Privacy Export Request",
	"Student Status Change",
]


def run_identity_document_proof() -> dict:
	"""Create and validate a synthetic P3.2 student identity/document slice."""

	academic = run_master_proof()
	applicant = _ensure_applicant(academic)
	guardian = _ensure_guardian()
	identity_profile = _ensure_identity_profile(applicant, academic["student_category"])
	candidate_profile = _ensure_candidate_profile(applicant)
	guardian_relationship = _ensure_doc(
		"Student Guardian Relationship",
		{"student_applicant": applicant, "guardian": guardian},
		{
			"student_applicant": applicant,
			"guardian": guardian,
			"relationship": "Father",
			"is_primary_guardian": 1,
			"can_receive_notifications": 1,
			"status": "Active",
		},
	)
	identity_issuance = _ensure_submitted(
		"Student Identity Issuance",
		{"identity_profile": identity_profile, "student_number": "P32-STU-0001"},
		{
			"identity_profile": identity_profile,
			"student_applicant": applicant,
			"student_number": "P32-STU-0001",
			"enrollment_number": "P32-ENR-2026-0001",
			"issued_on": "2026-01-15",
			"status": "Draft",
			"notes": "Synthetic immutable identity proof",
		},
	)
	consent = _ensure_doc(
		"Communication Consent",
		{"identity_profile": identity_profile, "consent_source": "Application"},
		{
			"identity_profile": identity_profile,
			"consent_source": "Application",
			"consent_date": "2026-01-15",
			"sms_allowed": 1,
			"email_allowed": 1,
			"guardian_name": "P32 Proof Guardian",
		},
	)
	status_change = _ensure_doc(
		"Student Status Change",
		{"identity_profile": identity_profile, "to_status": "Active"},
		{
			"identity_profile": identity_profile,
			"from_status": "Draft",
			"to_status": "Active",
			"effective_date": "2026-01-15",
			"reason": "Synthetic P3.2 activation",
		},
	)
	category_history = _ensure_doc(
		"Student Category History",
		{"identity_profile": identity_profile, "to_category": academic["student_category"]},
		{
			"identity_profile": identity_profile,
			"to_category": academic["student_category"],
			"effective_date": "2026-01-15",
			"reason": "Synthetic P3.2 category assignment",
		},
	)
	correction_request = _ensure_submitted(
		"Student Correction Request",
		{"identity_profile": identity_profile, "field_name": "full_name"},
		{
			"identity_profile": identity_profile,
			"field_name": "full_name",
			"current_value": "P32 Proof Applicant",
			"requested_value": "P32 Proof Applicant Updated",
			"reason": "Synthetic correction proof",
			"status": "Draft",
		},
	)
	duplicate_candidate = _ensure_doc(
		"Duplicate Candidate",
		{
			"source_identity_profile": identity_profile,
			"candidate_identity_profile": candidate_profile,
		},
		{
			"source_identity_profile": identity_profile,
			"candidate_identity_profile": candidate_profile,
			"match_score": 92,
			"match_reason": "Name and contact signals match",
			"status": "Open",
		},
	)
	rejection_reason = _ensure_doc(
		"Document Rejection Reason",
		{"reason_code": "P32-BLUR"},
		{
			"reason_code": "P32-BLUR",
			"reason": "Synthetic blurred document reason",
			"status": "Active",
		},
	)
	document_type = _ensure_doc(
		"Student Document Type",
		{"document_type_code": "P32-BIRTH"},
		{
			"document_type_code": "P32-BIRTH",
			"document_type_name": "Synthetic Birth Certificate",
			"status": "Active",
		},
	)
	requirement = _ensure_doc(
		"Document Requirement Matrix",
		{"requirement_code": "P32-BIRTH-GEN"},
		{
			"requirement_code": "P32-BIRTH-GEN",
			"document_type": document_type,
			"student_category": academic["student_category"],
			"program": academic["program"],
			"mandatory": 1,
			"status": "Active",
		},
	)
	student_document = _ensure_doc(
		"Student Document",
		{"student_applicant": applicant, "document_type": document_type},
		{
			"student_applicant": applicant,
			"document_type": document_type,
			"scan_status": "Scan Passed",
			"verification_status": "Pending Verification",
		},
	)
	verification = _ensure_submitted(
		"Document Verification",
		{"student_document": student_document, "result": "Verified"},
		{
			"student_document": student_document,
			"result": "Verified",
			"verified_on": "2026-01-15 10:00:00",
			"verified_by": "Administrator",
			"notes": "Synthetic verification proof",
		},
	)
	replacement_document = _ensure_doc(
		"Student Document",
		{"student_applicant": applicant, "document_type": document_type, "notes": "Synthetic replacement document"},
		{
			"student_applicant": applicant,
			"document_type": document_type,
			"scan_status": "Uploaded",
			"verification_status": "Pending Verification",
			"notes": "Synthetic replacement document",
		},
	)
	scan_result = _ensure_submitted(
		"Document Scan Result",
		{"student_document": replacement_document, "scan_result": "Passed"},
		{
			"student_document": replacement_document,
			"scan_result": "Passed",
			"scanned_on": "2026-01-15 10:15:00",
			"notes": "Synthetic scan pass proof",
		},
	)
	replacement_request = _ensure_submitted(
		"Document Replacement Request",
		{"old_document": student_document, "new_document": replacement_document},
		{
			"old_document": student_document,
			"new_document": replacement_document,
			"requested_on": "2026-01-16",
			"reason": "Synthetic replacement proof",
			"status": "Draft",
		},
	)
	expiry_document = _ensure_doc(
		"Student Document",
		{"student_applicant": applicant, "document_type": document_type, "notes": "Synthetic expiry document"},
		{
			"student_applicant": applicant,
			"document_type": document_type,
			"scan_status": "Scan Passed",
			"verification_status": "Verified",
			"expiry_date": "2026-01-20",
			"notes": "Synthetic expiry document",
		},
	)
	expiry_review = _ensure_submitted(
		"Document Expiry Review",
		{"student_document": expiry_document},
		{
			"student_document": expiry_document,
			"status": "Open",
			"expiry_date": "2026-01-20",
			"reviewed_on": "2026-01-21",
			"notes": "Synthetic expiry proof",
		},
	)
	data_access_log = _ensure_doc(
		"Student Data Access Log",
		{"identity_profile": identity_profile, "access_type": "Export"},
		{
			"identity_profile": identity_profile,
			"access_type": "Export",
			"accessed_by": "Administrator",
			"accessed_on": "2026-01-15 11:00:00",
			"masked_output": 1,
			"purpose": "Synthetic masked export audit proof",
		},
	)
	privacy_export_request = _ensure_submitted(
		"Student Privacy Export Request",
		{"identity_profile": identity_profile, "request_type": "Profile Export"},
		{
			"identity_profile": identity_profile,
			"request_type": "Profile Export",
			"requested_by": "Administrator",
			"requested_on": "2026-01-15 11:05:00",
			"masked_export": 1,
			"reason": "Synthetic privacy export proof",
			"status": "Draft",
		},
	)

	validation_checks = {
		"blank_identity_rejected": _rejects_blank_identity(),
		"empty_consent_rejected": _rejects_empty_consent(identity_profile),
		"self_duplicate_rejected": _rejects_self_duplicate(identity_profile),
		"scan_failed_without_reason_rejected": _rejects_scan_failure_without_reason(applicant, document_type),
		"duplicate_primary_guardian_rejected": _rejects_duplicate_primary_guardian(applicant, guardian),
		"duplicate_identity_number_rejected": _rejects_duplicate_identity_number(
			applicant, identity_profile
		),
		"replacement_same_document_rejected": _rejects_same_document_replacement(student_document),
		"failed_scan_without_reason_rejected": _rejects_failed_scan_without_reason(replacement_document),
		"unmasked_export_rejected": _rejects_unmasked_export(identity_profile),
	}
	audit_versions = _ensure_audit_version("Student Identity Profile", identity_profile)

	result = {
		"doctype_count": _count_p32_doctypes(),
		"permission_count": _count_required_permissions(),
		"applicant": applicant,
		"guardian": guardian,
		"identity_profile": identity_profile,
		"candidate_profile": candidate_profile,
		"guardian_relationship": guardian_relationship,
		"identity_issuance": identity_issuance,
		"consent": consent,
		"status_change": status_change,
		"category_history": category_history,
		"correction_request": correction_request,
		"duplicate_candidate": duplicate_candidate,
		"document_type": document_type,
		"requirement": requirement,
		"rejection_reason": rejection_reason,
		"student_document": student_document,
		"verification": verification,
		"scan_result": scan_result,
		"replacement_document": replacement_document,
		"replacement_request": replacement_request,
		"expiry_document": expiry_document,
		"expiry_review": expiry_review,
		"data_access_log": data_access_log,
		"privacy_export_request": privacy_export_request,
		"issued_identity_status": frappe.db.get_value("Student Identity Issuance", identity_issuance, "status"),
		"old_document_status": frappe.db.get_value("Student Document", student_document, "verification_status"),
		"replacement_document_status": frappe.db.get_value(
			"Student Document", replacement_document, "verification_status"
		),
		"replacement_scan_status": frappe.db.get_value("Student Document", replacement_document, "scan_status"),
		"expiry_document_status": frappe.db.get_value("Student Document", expiry_document, "verification_status"),
		"privacy_export_status": frappe.db.get_value(
			"Student Privacy Export Request", privacy_export_request, "status"
		),
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_applicant(academic: dict) -> str:
	if applicant := frappe.db.exists("Student Applicant", {"student_email_id": "p32.proof@example.invalid"}):
		return applicant
	doc = frappe.get_doc(
		{
			"doctype": "Student Applicant",
			"naming_series": "EDU-APP-.YYYY.-",
			"first_name": "P32",
			"middle_name": "Proof",
			"last_name": "Applicant",
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"academic_term": academic["academic_term"],
			"student_email_id": "p32.proof@example.invalid",
			"student_mobile_number": "9999900320",
			"date_of_birth": "2012-01-15",
			"student_category": academic["student_category"],
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_guardian() -> str:
	return _ensure_doc(
		"Guardian",
		{"email_address": "p32.guardian@example.invalid"},
		{
			"guardian_name": "P32 Proof Guardian",
			"email_address": "p32.guardian@example.invalid",
			"mobile_number": "9999900321",
		},
	)


def _ensure_identity_profile(applicant: str, category: str) -> str:
	return _ensure_doc(
		"Student Identity Profile",
		{"student_applicant": applicant},
		{
			"student_applicant": applicant,
			"full_name": "P32 Proof Applicant",
			"date_of_birth": "2012-01-15",
			"student_category": category,
			"primary_mobile": "9999900320",
			"primary_email": "P32.PROOF@EXAMPLE.INVALID",
			"status": "Active",
			"consent_recorded": 1,
		},
	)


def _ensure_candidate_profile(applicant: str) -> str:
	return _ensure_doc(
		"Student Identity Profile",
		{"primary_email": "p32.candidate@example.invalid"},
		{
			"student_applicant": applicant,
			"full_name": "P32 Proof Applicant",
			"date_of_birth": "2012-01-15",
			"primary_mobile": "9999900320",
			"primary_email": "p32.candidate@example.invalid",
			"status": "Draft",
		},
	)


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


def _rejects_blank_identity() -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Identity Profile",
				"full_name": "Invalid Blank Identity",
				"status": "Draft",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_empty_consent(identity_profile: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Communication Consent",
				"identity_profile": identity_profile,
				"consent_source": "Desk",
				"consent_date": "2026-01-15",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_self_duplicate(identity_profile: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Duplicate Candidate",
				"source_identity_profile": identity_profile,
				"candidate_identity_profile": identity_profile,
				"match_score": 99,
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_scan_failure_without_reason(applicant: str, document_type: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Document",
				"student_applicant": applicant,
				"document_type": document_type,
				"scan_status": "Scan Failed",
				"verification_status": "Rejected",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_duplicate_primary_guardian(applicant: str, guardian: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Guardian Relationship",
				"student_applicant": applicant,
				"guardian": guardian,
				"relationship": "Mother",
				"is_primary_guardian": 1,
				"status": "Active",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_duplicate_identity_number(applicant: str, identity_profile: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Identity Issuance",
				"identity_profile": identity_profile,
				"student_applicant": applicant,
				"student_number": "P32-STU-0001",
				"enrollment_number": "P32-ENR-DUPLICATE",
				"issued_on": "2026-01-15",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_same_document_replacement(student_document: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Document Replacement Request",
				"old_document": student_document,
				"new_document": student_document,
				"requested_on": "2026-01-16",
				"reason": "Invalid replacement proof",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_failed_scan_without_reason(student_document: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Document Scan Result",
				"student_document": student_document,
				"scan_result": "Failed",
				"scanned_on": "2026-01-15 10:30:00",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_unmasked_export(identity_profile: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Privacy Export Request",
				"identity_profile": identity_profile,
				"request_type": "Profile Export",
				"requested_by": "Administrator",
				"requested_on": "2026-01-15 11:10:00",
				"masked_export": 0,
				"reason": "Invalid unmasked export proof",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P3.2 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p32_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P32_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P32_DOCTYPES],
			"role": ["in", ["System Manager", "Academics User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P32_DOCTYPES):
		frappe.throw("P3.2 proof failed: expected custom identity/document DocTypes.")
	if result["permission_count"] < len(P32_DOCTYPES) * 2:
		frappe.throw("P3.2 proof failed: expected System Manager and Academics User permissions.")
	if result["issued_identity_status"] != "Issued":
		frappe.throw("P3.2 proof failed: identity issuance did not submit as Issued.")
	if result["old_document_status"] != "Replaced":
		frappe.throw("P3.2 proof failed: document replacement did not mark old document.")
	if result["replacement_document_status"] != "Pending Verification":
		frappe.throw("P3.2 proof failed: replacement document did not enter verification queue.")
	if result["replacement_scan_status"] != "Scan Passed":
		frappe.throw("P3.2 proof failed: scan result did not update replacement document.")
	if result["expiry_document_status"] != "Expired":
		frappe.throw("P3.2 proof failed: expiry review did not expire document.")
	if result["privacy_export_status"] != "Approved":
		frappe.throw("P3.2 proof failed: privacy export was not approved after masking.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P3.2 proof failed: expected validation checks to reject invalid records.")
	if result["audit_versions"] < 1:
		frappe.throw("P3.2 proof failed: expected audit Version evidence for identity profile.")
