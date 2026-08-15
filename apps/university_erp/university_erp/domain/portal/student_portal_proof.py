import hashlib

import frappe
from education.education.doctype.fee_schedule.fee_schedule import create_sales_invoice

from university_erp.api.portal import get_student_portal_snapshot
from university_erp.api.portal import create_student_payment, confirm_student_payment
from university_erp.domain.fees.demand_generation_proof import run_demand_generation_proof


def run_student_portal_access_proof():
	student = frappe.db.exists("Student", "EDU-STU-2026-00002")
	if not student:
		frappe.throw("P6.2 proof requires the existing synthetic P4.3 student.")
	proof_value = "p62-student-portal-proof-token"
	token_hash = hashlib.sha256(proof_value.encode("utf-8")).hexdigest()
	existing = frappe.db.exists("Student Portal Access", {"token_hash": token_hash})
	if existing:
		access = frappe.get_doc("Student Portal Access", existing)
	else:
		access = frappe.get_doc(
			{
				"doctype": "Student Portal Access",
				"student": student,
				"token_hash": token_hash,
				"status": "Active",
				"expires_on": "2027-01-01",
				"notes": "Synthetic P6.2 portal access proof",
			}
		)
		access.insert(ignore_permissions=True)
	frappe.db.commit()
	notice = frappe.db.exists("Student Portal Notice", {"title": "P6.2 Proof Notice"})
	if not notice:
		notice_doc = frappe.get_doc(
			{
				"doctype": "Student Portal Notice",
				"title": "P6.2 Proof Notice",
				"message": "Synthetic notice for student portal verification.",
				"published_on": "2026-08-13",
				"status": "Published",
				"audience": "All Students",
			}
		)
		notice_doc.insert(ignore_permissions=True)
		notice = notice_doc.name
	frappe.db.commit()
	return {"access": access.name, "student": student, "access_token": proof_value, "notice": notice}


def run_student_portal_snapshot_proof():
	return get_student_portal_snapshot("p62-student-portal-proof-token")


def run_student_portal_payment_proof():
	base = run_demand_generation_proof()
	student = base["student"]
	schedule = base["fee_schedule"]
	program_enrollment = base["program_enrollment"]
	policy = base["policy"]
	invoice = create_sales_invoice(schedule, student)
	invoice_doc = frappe.get_doc("Sales Invoice", invoice)
	if invoice_doc.docstatus == 0:
		invoice_doc.submit()
	demand_name = frappe.db.exists("Student Fee Demand", {"idempotency_key": "P62-PORTAL-DEMAND"})
	if not demand_name:
		demand_doc = frappe.get_doc(
			{
				"doctype": "Student Fee Demand",
				"student": student,
				"program_enrollment": program_enrollment,
				"policy_version": policy,
				"status": "Draft",
				"gross_amount": 1000,
				"concession_amount": 100,
				"scholarship_amount": 50,
				"fine_amount": 25,
				"waiver_amount": 25,
				"net_amount": 850,
				"due_date": "2026-08-30",
				"fee_schedule": schedule,
				"sales_invoice": invoice_doc.name,
				"idempotency_key": "P62-PORTAL-DEMAND",
			}
		)
		demand_doc.insert(ignore_permissions=True)
		demand_doc.submit()
		demand_name = demand_doc.name
	attempt = create_student_payment("p62-student-portal-proof-token", demand_name, "student-payment-p62-capture-001")
	confirmed = confirm_student_payment(
		"p62-student-portal-proof-token", attempt["attempt"], attempt["provider_order_id"]
	)
	repeated = confirm_student_payment(
		"p62-student-portal-proof-token", attempt["attempt"], attempt["provider_order_id"]
	)
	return {"demand": demand_name, "attempt": attempt, "confirmed": confirmed, "repeated": repeated}
