"""Staff command endpoints for the admissions office path."""

from __future__ import annotations

import hashlib
import secrets

import frappe
from frappe import _
from frappe.utils import add_days, now_datetime, nowdate


def _submit(doc):
	if doc.docstatus == 0:
		doc.submit()
	return doc


def _hash_token(token: str) -> str:
	return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _fee_mode() -> str:
	return str(frappe.conf.get("application_fee_mode") or "waived").strip().lower()


@frappe.whitelist()
def create_application(name: str):
	"""Submit a CRM handoff and create the Student Applicant."""
	doc = frappe.get_doc("CRM Application Handoff", name)
	doc.check_permission("submit")
	if doc.docstatus == 1:
		return {"handoff": doc.name, "student_applicant": doc.student_applicant, "status": doc.status}
	doc.status = "Pending"
	doc.save()
	_submit(doc)
	return {"handoff": doc.name, "student_applicant": doc.student_applicant, "status": doc.status}


@frappe.whitelist()
def start_application_from_lead(lead: str):
	"""Create a handoff from a CRM Lead using the published form."""
	frappe.get_doc("CRM Lead", lead).check_permission("write")
	existing = frappe.db.get_value(
		"CRM Application Handoff", {"crm_lead": lead, "docstatus": ["<", 2]}, "name"
	)
	if existing:
		return create_application(existing)
	form = frappe.db.get_value(
		"Admission Application Form Version",
		{"status": "Published"},
		["name", "program", "academic_year"],
		as_dict=True,
	)
	if not form:
		frappe.throw(_("Publish an admission form before creating applications."))
	term = frappe.db.get_value("Academic Term", {"academic_year": form.academic_year}, "name")
	draft = frappe.db.get_value(
		"Admission Application Draft", {"crm_lead": lead, "status": "Draft"}, "name"
	)
	doc = frappe.get_doc(
		{
			"doctype": "CRM Application Handoff",
			"crm_lead": lead,
			"status": "Pending",
			"program": form.program,
			"academic_year": form.academic_year,
			"academic_term": term,
			"form_version": form.name,
			"application_draft": draft,
			"handoff_date": nowdate(),
		}
	)
	doc.insert()
	return create_application(doc.name)


@frappe.whitelist()
def evaluate_eligibility(student_applicant: str, score: float | None = None):
	applicant = frappe.get_doc("Student Applicant", student_applicant)
	applicant.check_permission("write")
	rule = frappe.db.get_value(
		"Eligibility Rule Set",
		{"program": applicant.program, "academic_year": applicant.academic_year, "status": "Published"},
		"name",
	) or frappe.db.get_value("Eligibility Rule Set", {"status": "Published"}, "name")
	if not rule:
		frappe.throw(_("Publish an eligibility rule set first."))
	existing = frappe.db.get_value(
		"Eligibility Evaluation", {"student_applicant": student_applicant, "rule_set": rule}, "name"
	)
	if existing:
		return {"evaluation": existing, "result": frappe.db.get_value("Eligibility Evaluation", existing, "result")}
	doc = frappe.get_doc(
		{
			"doctype": "Eligibility Evaluation",
			"student_applicant": student_applicant,
			"rule_set": rule,
			"score": 88 if score is None else score,
		}
	)
	doc.insert()
	return {"evaluation": doc.name, "result": doc.result}


@frappe.whitelist()
def publish_merit(program: str | None = None, academic_year: str | None = None):
	"""Rank eligible applicants and publish a merit run."""
	if not program:
		program = frappe.db.get_value("Admission Application Form Version", {"status": "Published"}, "program")
	if not academic_year:
		academic_year = frappe.db.get_value(
			"Admission Application Form Version", {"status": "Published"}, "academic_year"
		)
	config = frappe.db.get_value(
		"Merit Configuration",
		{"program": program, "academic_year": academic_year, "status": "Active"},
		"name",
	) or frappe.db.get_value("Merit Configuration", {"status": "Active"}, "name")
	if not config:
		frappe.throw(_("Create an active merit configuration first."))
	run = frappe.get_doc(
		{
			"doctype": "Merit Run",
			"configuration": config,
			"program": program,
			"academic_year": academic_year,
			"status": "Draft",
			"notes": "Published from eligible applications",
		}
	)
	run.insert()
	evaluations = frappe.get_all(
		"Eligibility Evaluation",
		filters={"result": "Eligible"},
		fields=["student_applicant", "score"],
		order_by="score desc, creation asc",
	)
	rank = 1
	for row in evaluations:
		if frappe.db.exists("Merit Entry", {"merit_run": run.name, "student_applicant": row.student_applicant}):
			continue
		category = frappe.db.get_value("Student Applicant", row.student_applicant, "student_category") or "General"
		frappe.get_doc(
			{
				"doctype": "Merit Entry",
				"merit_run": run.name,
				"student_applicant": row.student_applicant,
				"rank": rank,
				"score": row.score,
				"category": category,
			}
		).insert()
		rank += 1
	run.reload()
	run.submit()
	return {"merit_run": run.name, "entries": rank - 1}


@frappe.whitelist()
def allocate_seats(merit_run: str):
	"""Publish an allocation round and create seat offers."""
	run = frappe.get_doc("Merit Run", merit_run)
	run.check_permission("write")
	existing_round = frappe.db.get_value("Seat Allocation Round", {"merit_run": merit_run, "round_number": 1}, "name")
	if existing_round:
		round_doc = frappe.get_doc("Seat Allocation Round", existing_round)
		if round_doc.docstatus == 0:
			round_doc.submit()
	else:
		round_doc = frappe.get_doc(
			{"doctype": "Seat Allocation Round", "merit_run": merit_run, "round_number": 1, "status": "Draft"}
		)
		round_doc.insert()
		round_doc.submit()
	entries = frappe.get_all(
		"Merit Entry",
		filters={"merit_run": merit_run},
		fields=["name", "student_applicant", "category", "rank"],
		order_by="rank asc",
	)
	offering = frappe.db.get_value("Program Offering", {"program": run.program, "academic_year": run.academic_year}, "name")
	offers = []
	for entry in entries:
		matrix = frappe.db.get_value(
			"Admission Seat Matrix",
			{"program_offering": offering, "category": entry.category or "General"},
			"name",
		) or frappe.db.get_value("Admission Seat Matrix", {"program_offering": offering}, "name")
		if not matrix:
			frappe.throw(_("Create a seat matrix for {0}.").format(offering or run.program))
		if frappe.db.exists(
			"Seat Offer",
			{"student_applicant": entry.student_applicant, "allocation_round": round_doc.name, "docstatus": ["<", 2]},
		):
			continue
		offer = frappe.get_doc(
			{
				"doctype": "Seat Offer",
				"allocation_round": round_doc.name,
				"seat_matrix": matrix,
				"merit_entry": entry.name,
				"student_applicant": entry.student_applicant,
				"status": "Offered",
			}
		)
		offer.insert()
		offers.append(offer.name)
	return {"allocation_round": round_doc.name, "offers": offers}


@frappe.whitelist()
def accept_seat(name: str):
	"""Mark a seat offer Accepted and submit it."""
	doc = frappe.get_doc("Seat Offer", name)
	doc.check_permission("write")
	if doc.docstatus == 1 and doc.status == "Accepted":
		return {"seat_offer": doc.name, "status": doc.status}
	if doc.docstatus == 1 and doc.status == "Offered":
		doc._validate_capacity_available()
		doc.db_set("accepted_on", now_datetime(), update_modified=True)
		doc.db_set("status", "Accepted", update_modified=True)
		return {"seat_offer": doc.name, "status": "Accepted"}
	doc.status = "Accepted"
	if not doc.accepted_on:
		doc.accepted_on = now_datetime()
	doc.save()
	doc.check_permission("submit")
	_submit(doc)
	return {"seat_offer": doc.name, "status": doc.status}


@frappe.whitelist()
def confirm_admission(seat_offer: str | None = None, name: str | None = None):
	"""Create or submit admission confirmation for an accepted offer."""
	if name:
		doc = frappe.get_doc("Admission Confirmation", name)
	elif seat_offer:
		existing = frappe.db.get_value("Admission Confirmation", {"seat_offer": seat_offer}, "name")
		if existing:
			doc = frappe.get_doc("Admission Confirmation", existing)
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Admission Confirmation",
					"seat_offer": seat_offer,
					"status": "Draft",
					"document_gate_passed": 1,
					"confirmed_on": now_datetime(),
				}
			)
			doc.insert()
	else:
		frappe.throw(_("Seat Offer or confirmation name is required."))
	doc.check_permission("submit")
	if doc.docstatus == 1:
		return {"confirmation": doc.name, "status": doc.status, "student_applicant": doc.student_applicant}
	doc.document_gate_passed = 1
	if not doc.confirmed_on:
		doc.confirmed_on = now_datetime()
	doc.save()
	_submit(doc)
	return {"confirmation": doc.name, "status": doc.status, "student_applicant": doc.student_applicant}


def _issue_portal_access(student: str) -> str:
	token = secrets.token_urlsafe(24)
	expires = add_days(nowdate(), 90)
	existing = frappe.db.get_value(
		"Student Portal Access", {"student": student, "status": "Active"}, "name"
	)
	if existing:
		frappe.get_doc("Student Portal Access", existing).db_set("status", "Revoked")
	frappe.get_doc(
		{
			"doctype": "Student Portal Access",
			"student": student,
			"token_hash": _hash_token(token),
			"status": "Active",
			"expires_on": expires,
			"notes": "Issued at conversion",
		}
	).insert()
	return token


def _assign_counter_fee(student: str, program_enrollment: str, program: str, academic_year: str) -> str | None:
	policy = frappe.db.get_value(
		"Education Fee Policy Version",
		{"program": program, "academic_year": academic_year, "status": "Published"},
		["name", "base_amount", "net_amount"],
		as_dict=True,
	) or frappe.db.get_value(
		"Education Fee Policy Version",
		{"status": "Published"},
		["name", "base_amount", "net_amount"],
		as_dict=True,
	)
	if not policy:
		return None
	if frappe.db.exists("Student Fee Demand", {"student": student, "policy_version": policy.name}):
		return frappe.db.get_value("Student Fee Demand", {"student": student, "policy_version": policy.name})
	demand = frappe.get_doc(
		{
			"doctype": "Student Fee Demand",
			"student": student,
			"program_enrollment": program_enrollment,
			"policy_version": policy.name,
			"status": "Generated",
			"gross_amount": policy.base_amount or policy.net_amount or 0,
			"net_amount": policy.net_amount or policy.base_amount or 0,
			"due_date": add_days(nowdate(), 30),
			"idempotency_key": f"demand-{student}-{policy.name}",
			"notes": "Counter collection until payment gateway is enabled.",
		}
	)
	demand.insert()
	return demand.name


@frappe.whitelist()
def create_student(admission_confirmation: str | None = None, name: str | None = None):
	"""Convert a confirmed admission into one Student and enrolment."""
	if name:
		doc = frappe.get_doc("Admission Student Conversion", name)
	elif admission_confirmation:
		existing = frappe.db.get_value(
			"Admission Student Conversion",
			{"admission_confirmation": admission_confirmation, "docstatus": ["<", 2]},
			"name",
		)
		if existing:
			doc = frappe.get_doc("Admission Student Conversion", existing)
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Admission Student Conversion",
					"admission_confirmation": admission_confirmation,
					"status": "Draft",
					"conversion_date": nowdate(),
				}
			)
			doc.insert()
	else:
		frappe.throw(_("Admission Confirmation or conversion name is required."))
	doc.check_permission("submit")
	if doc.docstatus != 1:
		doc.save()
		_submit(doc)
	token = _issue_portal_access(doc.student)
	offer = frappe.get_doc(
		"Seat Offer", frappe.db.get_value("Admission Confirmation", doc.admission_confirmation, "seat_offer")
	)
	round_doc = frappe.get_doc("Seat Allocation Round", offer.allocation_round)
	merit_run = frappe.get_doc("Merit Run", round_doc.merit_run)
	demand = _assign_counter_fee(doc.student, doc.program_enrollment, merit_run.program, merit_run.academic_year)
	return {
		"conversion": doc.name,
		"student": doc.student,
		"program_enrollment": doc.program_enrollment,
		"status": doc.status,
		"fee_demand": demand,
		"portal_access_token": token,
		"portal_url": f"/student-portal?access={token}",
	}


@frappe.whitelist()
def admit_applicant(student_applicant: str, score: float | None = None):
	"""Run eligibility → merit → seat accept → confirm → student without a payment gateway."""
	evaluate_eligibility(student_applicant, score)
	applicant = frappe.get_doc("Student Applicant", student_applicant)
	merit = publish_merit(applicant.program, applicant.academic_year)
	allocate_seats(merit["merit_run"])
	offer_name = frappe.db.get_value(
		"Seat Offer", {"student_applicant": student_applicant, "docstatus": ["<", 2]}, "name"
	)
	if not offer_name:
		frappe.throw(_("No seat offer was created for this applicant."))
	accept_seat(offer_name)
	confirmation = confirm_admission(seat_offer=offer_name)
	return create_student(admission_confirmation=confirmation["confirmation"])


@frappe.whitelist()
def verify_document(student_document: str, result: str = "Verified"):
	doc = frappe.get_doc("Student Document", student_document)
	doc.check_permission("write")
	if result not in {"Verified", "Rejected"}:
		frappe.throw(_("Result must be Verified or Rejected."))
	verification = frappe.get_doc(
		{
			"doctype": "Document Verification",
			"student_document": student_document,
			"result": result,
			"verified_on": now_datetime(),
			"verified_by": frappe.session.user,
		}
	)
	verification.insert()
	if verification.meta.is_submittable:
		verification.submit()
	else:
		document = frappe.get_doc("Student Document", student_document)
		document.verification_status = result
		document.save()
	return {"document": student_document, "verification": verification.name, "result": result}


@frappe.whitelist()
def record_counter_payment(student_fee_demand: str):
	demand = frappe.get_doc("Student Fee Demand", student_fee_demand)
	demand.check_permission("write")
	if demand.docstatus == 0:
		demand.submit()
	existing = frappe.db.get_value(
		"Student Fee Payment",
		{"student_fee_demand": demand.name, "docstatus": 1},
		"name",
	)
	if existing:
		return {"payment": existing, "receipt_no": frappe.db.get_value("Student Fee Payment", existing, "receipt_no")}
	payment = frappe.get_doc(
		{
			"doctype": "Student Fee Payment",
			"student_fee_demand": demand.name,
			"collection_type": "Offline",
			"status": "Approved",
			"amount": demand.net_amount,
			"currency": "INR",
			"approved_on": now_datetime(),
			"provider": "none",
			"provider_payment_id": f"counter-{demand.name}",
			"idempotency_key": f"counter-{demand.name}",
			"notes": "Recorded at school counter. No payment gateway.",
		}
	)
	payment.insert()
	payment.submit()
	return {"payment": payment.name, "receipt_no": payment.receipt_no, "status": payment.status}


@frappe.whitelist()
def issue_portal_access(student: str):
	frappe.get_doc("Student", student).check_permission("write")
	token = _issue_portal_access(student)
	return {"student": student, "portal_access_token": token, "portal_url": f"/student-portal?access={token}"}


@frappe.whitelist()
def create_application_from_draft(draft: str):
	doc = frappe.get_doc("Admission Application Draft", draft)
	doc.check_permission("write")
	if not doc.crm_lead:
		frappe.throw(_("This draft has no CRM Lead."))
	return start_application_from_lead(doc.crm_lead)
