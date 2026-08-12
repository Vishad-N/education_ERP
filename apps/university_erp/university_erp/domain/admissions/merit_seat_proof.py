from __future__ import annotations

import json

import frappe

from university_erp.domain.academic.master_proof import run_master_proof
from university_erp.domain.admissions.application_handoff_proof import run_application_handoff_proof


P42_DOCTYPES = [
	"Admission Seat Matrix",
	"Eligibility Evaluation",
	"Eligibility Rule Set",
	"Merit Configuration",
	"Merit Entry",
	"Merit Run",
	"Seat Allocation Round",
	"Seat Offer",
]


def run_merit_seat_proof() -> dict:
	"""Create and validate a synthetic P4.2 eligibility, merit and seat slice."""

	academic = run_master_proof()
	handoff = run_application_handoff_proof()
	primary_applicant = handoff["student_applicant"]
	waitlist_applicant = _ensure_waitlist_applicant(academic)
	overflow_applicant = _ensure_overflow_applicant(academic)
	rule_set = _ensure_rule_set(academic)
	primary_evaluation = _ensure_evaluation(primary_applicant, rule_set, 88, "Eligible")
	waitlist_evaluation = _ensure_evaluation(waitlist_applicant, rule_set, 82, "Eligible")
	overflow_evaluation = _ensure_evaluation(overflow_applicant, rule_set, 80, "Eligible")
	merit_configuration = _ensure_merit_configuration(academic)
	merit_run = _ensure_submitted(
		"Merit Run",
		{"configuration": merit_configuration},
		{
			"configuration": merit_configuration,
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"status": "Draft",
			"run_on": "2026-01-25 09:00:00",
			"published_on": "2026-01-25 09:30:00",
			"notes": "Synthetic P4.2 merit run",
		},
	)
	primary_merit = _ensure_merit_entry(
		merit_run, primary_applicant, academic["student_category"], 1, 88
	)
	waitlist_merit = _ensure_merit_entry(
		merit_run, waitlist_applicant, academic["student_category"], 2, 82
	)
	overflow_merit = _ensure_merit_entry(
		merit_run, overflow_applicant, academic["student_category"], 3, 80
	)
	seat_matrix = _ensure_doc(
		"Admission Seat Matrix",
		{"program_offering": academic["program_offering"], "category": academic["student_category"]},
		{
			"program_offering": academic["program_offering"],
			"category": academic["student_category"],
			"capacity": 1,
			"supernumerary_capacity": 0,
			"status": "Locked",
			"locked_on": "2026-01-25 09:45:00",
			"notes": "Synthetic one-seat capacity proof",
		},
	)
	allocation_round = _ensure_submitted(
		"Seat Allocation Round",
		{"merit_run": merit_run, "round_number": 1},
		{
			"merit_run": merit_run,
			"round_number": 1,
			"status": "Draft",
			"published_on": "2026-01-25 10:00:00",
			"notes": "Synthetic P4.2 allocation round",
		},
	)
	accepted_offer = _ensure_submitted(
		"Seat Offer",
		{"allocation_round": allocation_round, "student_applicant": primary_applicant},
		{
			"allocation_round": allocation_round,
			"seat_matrix": seat_matrix,
			"merit_entry": primary_merit,
			"student_applicant": primary_applicant,
			"status": "Accepted",
			"offered_on": "2026-01-25 10:15:00",
			"expires_on": "2026-01-30 23:59:59",
			"accepted_on": "2026-01-26 11:00:00",
			"idempotency_key": "P42-SEAT-ACCEPT-PRIMARY",
			"notes": "Synthetic accepted seat proof",
		},
	)
	waitlist_offer = _ensure_doc(
		"Seat Offer",
		{"allocation_round": allocation_round, "student_applicant": waitlist_applicant},
		{
			"allocation_round": allocation_round,
			"seat_matrix": seat_matrix,
			"merit_entry": waitlist_merit,
			"student_applicant": waitlist_applicant,
			"status": "Waitlisted",
			"offered_on": "2026-01-25 10:20:00",
			"expires_on": "2026-01-30 23:59:59",
			"idempotency_key": "P42-SEAT-WAITLIST",
			"notes": "Synthetic waitlist proof",
		},
	)

	validation_checks = {
		"invalid_rule_set_rejected": _rejects_invalid_rule_set(academic),
		"incorrect_eligibility_result_rejected": _rejects_incorrect_eligibility_result(
			primary_applicant, rule_set
		),
		"duplicate_merit_rank_rejected": _rejects_duplicate_merit_rank(
			merit_run, waitlist_applicant, academic["student_category"]
		),
		"second_accepted_offer_rejected": _rejects_second_accepted_offer(
			allocation_round, seat_matrix, overflow_merit, overflow_applicant
		),
	}
	audit_versions = _ensure_audit_version("Seat Offer", waitlist_offer)

	result = {
		"doctype_count": _count_p42_doctypes(),
		"permission_count": _count_required_permissions(),
		"rule_set": rule_set,
		"primary_evaluation": primary_evaluation,
		"waitlist_evaluation": waitlist_evaluation,
		"overflow_evaluation": overflow_evaluation,
		"merit_configuration": merit_configuration,
		"merit_run": merit_run,
		"merit_run_status": frappe.db.get_value("Merit Run", merit_run, "status"),
		"primary_merit": primary_merit,
		"waitlist_merit": waitlist_merit,
		"overflow_merit": overflow_merit,
		"seat_matrix": seat_matrix,
		"seat_capacity": frappe.db.get_value("Admission Seat Matrix", seat_matrix, "capacity"),
		"allocation_round": allocation_round,
		"allocation_round_status": frappe.db.get_value(
			"Seat Allocation Round", allocation_round, "status"
		),
		"accepted_offer": accepted_offer,
		"accepted_offer_status": frappe.db.get_value("Seat Offer", accepted_offer, "status"),
		"waitlist_offer": waitlist_offer,
		"waitlist_offer_status": frappe.db.get_value("Seat Offer", waitlist_offer, "status"),
		"accepted_offer_count": frappe.db.count(
			"Seat Offer", {"seat_matrix": seat_matrix, "status": "Accepted", "docstatus": 1}
		),
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_waitlist_applicant(academic: dict) -> str:
	if applicant := frappe.db.exists("Student Applicant", {"student_email_id": "p42.waitlist@example.invalid"}):
		return applicant
	doc = frappe.get_doc(
		{
			"doctype": "Student Applicant",
			"naming_series": "EDU-APP-.YYYY.-",
			"first_name": "P42",
			"last_name": "Waitlist",
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"academic_term": academic["academic_term"],
			"student_email_id": "p42.waitlist@example.invalid",
			"student_mobile_number": "9999900420",
			"date_of_birth": "2012-02-01",
			"student_category": academic["student_category"],
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_overflow_applicant(academic: dict) -> str:
	if applicant := frappe.db.exists("Student Applicant", {"student_email_id": "p42.overflow@example.invalid"}):
		return applicant
	doc = frappe.get_doc(
		{
			"doctype": "Student Applicant",
			"naming_series": "EDU-APP-.YYYY.-",
			"first_name": "P42",
			"last_name": "Overflow",
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"academic_term": academic["academic_term"],
			"student_email_id": "p42.overflow@example.invalid",
			"student_mobile_number": "9999900421",
			"date_of_birth": "2012-02-02",
			"student_category": academic["student_category"],
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_rule_set(academic: dict) -> str:
	return _ensure_doc(
		"Eligibility Rule Set",
		{"rule_code": "P42-MIN-SCORE", "version": "2026.1"},
		{
			"rule_code": "P42-MIN-SCORE",
			"version": "2026.1",
			"status": "Published",
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"effective_from": "2026-01-25",
			"rules_json": json.dumps({"minimum_score": 75}, sort_keys=True),
		},
	)


def _ensure_evaluation(applicant: str, rule_set: str, score: int, result: str) -> str:
	return _ensure_doc(
		"Eligibility Evaluation",
		{"student_applicant": applicant, "rule_set": rule_set},
		{
			"student_applicant": applicant,
			"rule_set": rule_set,
			"result": result,
			"score": score,
			"evaluated_on": "2026-01-25 08:30:00",
			"explanation_json": json.dumps(
				{"minimum_score": 75, "score": score, "result": result}, sort_keys=True
			),
		},
	)


def _ensure_merit_configuration(academic: dict) -> str:
	return _ensure_doc(
		"Merit Configuration",
		{"configuration_code": "P42-MERIT-2026"},
		{
			"configuration_code": "P42-MERIT-2026",
			"program": academic["program"],
			"academic_year": academic["academic_year"],
			"status": "Active",
			"tie_breaker_json": json.dumps(["score_desc", "date_of_birth_asc"], sort_keys=True),
		},
	)


def _ensure_merit_entry(
	merit_run: str, applicant: str, category: str, rank: int, score: int
) -> str:
	return _ensure_doc(
		"Merit Entry",
		{"merit_run": merit_run, "student_applicant": applicant},
		{
			"merit_run": merit_run,
			"student_applicant": applicant,
			"rank": rank,
			"score": score,
			"category": category,
			"tie_breaker_summary": "score_desc",
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


def _rejects_invalid_rule_set(academic: dict) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Eligibility Rule Set",
				"rule_code": "P42-BAD",
				"version": "2026.1",
				"status": "Published",
				"program": academic["program"],
				"academic_year": academic["academic_year"],
				"effective_from": "2026-01-25",
				"rules_json": "{}",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_incorrect_eligibility_result(applicant: str, rule_set: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Eligibility Evaluation",
				"student_applicant": applicant,
				"rule_set": rule_set,
				"result": "Eligible",
				"score": 50,
				"evaluated_on": "2026-01-25 08:45:00",
				"explanation_json": json.dumps({"minimum_score": 75, "score": 50}),
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_duplicate_merit_rank(merit_run: str, applicant: str, category: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Merit Entry",
				"merit_run": merit_run,
				"student_applicant": applicant,
				"rank": 1,
				"score": 81,
				"category": category,
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_second_accepted_offer(
	allocation_round: str, seat_matrix: str, merit_entry: str, applicant: str
) -> bool:
	if existing := frappe.db.exists("Seat Offer", {"idempotency_key": "P42-SEAT-ACCEPT-OVERFLOW"}):
		existing_doc = frappe.get_doc("Seat Offer", existing)
		if existing_doc.docstatus == 0:
			existing_doc.delete(ignore_permissions=True)
	try:
		doc = frappe.get_doc(
			{
				"doctype": "Seat Offer",
				"allocation_round": allocation_round,
				"seat_matrix": seat_matrix,
				"merit_entry": merit_entry,
				"student_applicant": applicant,
				"status": "Accepted",
				"offered_on": "2026-01-25 10:30:00",
				"expires_on": "2026-01-30 23:59:59",
				"accepted_on": "2026-01-26 11:30:00",
				"idempotency_key": "P42-SEAT-ACCEPT-OVERFLOW",
			}
		)
		doc.insert(ignore_permissions=True)
		doc.submit()
	except frappe.ValidationError:
		if frappe.db.exists("Seat Offer", {"idempotency_key": "P42-SEAT-ACCEPT-OVERFLOW"}):
			frappe.get_doc(
				"Seat Offer",
				frappe.db.exists("Seat Offer", {"idempotency_key": "P42-SEAT-ACCEPT-OVERFLOW"}),
			).delete(ignore_permissions=True)
		frappe.clear_messages()
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P4.2 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p42_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P42_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P42_DOCTYPES],
			"role": ["in", ["System Manager", "Academics User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P42_DOCTYPES):
		frappe.throw("P4.2 proof failed: expected custom eligibility/merit/seat DocTypes.")
	if result["permission_count"] < len(P42_DOCTYPES) * 2:
		frappe.throw("P4.2 proof failed: expected System Manager and Academics User permissions.")
	if result["merit_run_status"] != "Published":
		frappe.throw("P4.2 proof failed: merit run was not published.")
	if result["allocation_round_status"] != "Published":
		frappe.throw("P4.2 proof failed: allocation round was not published.")
	if result["accepted_offer_status"] != "Accepted":
		frappe.throw("P4.2 proof failed: primary offer was not accepted.")
	if result["waitlist_offer_status"] != "Waitlisted":
		frappe.throw("P4.2 proof failed: second applicant was not waitlisted.")
	if result["accepted_offer_count"] > result["seat_capacity"]:
		frappe.throw("P4.2 proof failed: accepted offers exceeded capacity.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P4.2 proof failed: expected invalid records to be rejected.")
	if result["audit_versions"] < 1:
		frappe.throw("P4.2 proof failed: expected audit Version evidence for seat offer.")
