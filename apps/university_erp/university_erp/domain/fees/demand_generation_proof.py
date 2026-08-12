from __future__ import annotations

import frappe
from education.education.doctype.fee_schedule.fee_schedule import create_sales_invoice
from frappe.utils import flt, nowdate

from university_erp.domain.admissions.conversion_proof import run_conversion_proof
from university_erp.domain.fees.accounting_proof import (
	PROOF_COMPANY,
	_account,
	_cost_center,
	_ensure_accounting_setup,
)


P51_DOCTYPES = [
	"Education Fee Code",
	"Education Fee Installment",
	"Education Fee Policy Version",
	"Student Fee Adjustment",
	"Student Fee Demand",
]


def run_demand_generation_proof() -> dict:
	"""Create and validate a synthetic P5.1 fee policy and demand."""

	_ensure_accounting_setup()
	conversion = run_conversion_proof()
	student = conversion["student"]
	program_enrollment = conversion["program_enrollment"]
	program = frappe.db.get_value("Program Enrollment", program_enrollment, "program")
	academic_year = frappe.db.get_value("Program Enrollment", program_enrollment, "academic_year")
	academic_term = frappe.db.get_value("Program Enrollment", program_enrollment, "academic_term")
	fee_category = _ensure_fee_category()
	fee_code = _ensure_fee_code(fee_category)
	policy = _ensure_policy(fee_code, program, academic_year)
	installment = _ensure_installment(policy)
	concession = _ensure_adjustment(student, policy, "Concession", 100)
	scholarship = _ensure_adjustment(student, policy, "Scholarship", 50)
	fine = _ensure_adjustment(student, policy, "Fine", 25)
	waiver = _ensure_adjustment(student, policy, "Waiver", 25)
	fee_schedule = _ensure_fee_schedule(student, program, academic_year, academic_term, fee_category)
	invoice = _ensure_sales_invoice(fee_schedule, student)
	demand = _ensure_submitted(
		"Student Fee Demand",
		{"idempotency_key": "P51-DEMAND-PRIMARY"},
		{
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
			"due_date": "2026-02-15",
			"fee_schedule": fee_schedule,
			"sales_invoice": invoice,
			"idempotency_key": "P51-DEMAND-PRIMARY",
			"notes": "Synthetic P5.1 demand proof",
		},
	)
	repeated_demand = _ensure_submitted(
		"Student Fee Demand",
		{"idempotency_key": "P51-DEMAND-PRIMARY"},
		{
			"student": student,
			"program_enrollment": program_enrollment,
			"policy_version": policy,
			"gross_amount": 1000,
			"net_amount": 850,
			"due_date": "2026-02-15",
			"sales_invoice": invoice,
			"idempotency_key": "P51-DEMAND-PRIMARY",
		},
	)

	validation_checks = {
		"incorrect_policy_total_rejected": _rejects_incorrect_policy_total(
			fee_code, program, academic_year
		),
		"negative_adjustment_rejected": _rejects_negative_adjustment(student, policy),
		"incorrect_demand_total_rejected": _rejects_incorrect_demand_total(
			student, program_enrollment, policy, invoice
		),
		"invoice_mismatch_rejected": _rejects_invoice_mismatch(
			student, program_enrollment, policy, invoice
		),
	}
	audit_versions = _ensure_audit_version("Education Fee Policy Version", policy)

	result = {
		"doctype_count": _count_p51_doctypes(),
		"permission_count": _count_required_permissions(),
		"student": student,
		"program_enrollment": program_enrollment,
		"fee_category": fee_category,
		"fee_code": fee_code,
		"policy": policy,
		"installment": installment,
		"concession": concession,
		"scholarship": scholarship,
		"fine": fine,
		"waiver": waiver,
		"fee_schedule": fee_schedule,
		"sales_invoice": invoice,
		"sales_invoice_total": flt(frappe.db.get_value("Sales Invoice", invoice, "grand_total"), 2),
		"sales_invoice_docstatus": frappe.db.get_value("Sales Invoice", invoice, "docstatus"),
		"demand": demand,
		"repeated_demand": repeated_demand,
		"demand_status": frappe.db.get_value("Student Fee Demand", demand, "status"),
		"demand_net_amount": flt(frappe.db.get_value("Student Fee Demand", demand, "net_amount"), 2),
		"policy_net_amount": flt(
			frappe.db.get_value("Education Fee Policy Version", policy, "net_amount"), 2
		),
		"installment_total": flt(
			frappe.db.get_value("Education Fee Installment", installment, "amount"), 2
		),
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_fee_category() -> str:
	if frappe.db.exists("Fee Category", {"category_name": "P5.1 Tuition Fee"}):
		return frappe.db.get_value("Fee Category", {"category_name": "P5.1 Tuition Fee"})
	category = frappe.new_doc("Fee Category")
	category.category_name = "P5.1 Tuition Fee"
	category.description = "Synthetic P5.1 tuition fee"
	category.append(
		"item_defaults",
		{
			"company": PROOF_COMPANY,
			"selling_cost_center": _cost_center(),
			"income_account": _account("Sales"),
		},
	)
	category.insert()
	return category.name


def _ensure_fee_code(fee_category: str) -> str:
	return _ensure_doc(
		"Education Fee Code",
		{"fee_code": "P51-TUITION"},
		{
			"fee_code": "P51-TUITION",
			"fee_name": "P5.1 Tuition",
			"fee_category": fee_category,
			"status": "Active",
			"default_amount": 1000,
		},
	)


def _ensure_policy(fee_code: str, program: str, academic_year: str) -> str:
	return _ensure_doc(
		"Education Fee Policy Version",
		{"policy_code": "P51-POLICY", "version": "2026.1"},
		{
			"policy_code": "P51-POLICY",
			"version": "2026.1",
			"status": "Published",
			"fee_code": fee_code,
			"program": program,
			"academic_year": academic_year,
			"effective_from": "2026-02-01",
			"base_amount": 1000,
			"concession_amount": 100,
			"scholarship_amount": 50,
			"fine_amount": 25,
			"waiver_amount": 25,
			"net_amount": 850,
		},
	)


def _ensure_installment(policy: str) -> str:
	return _ensure_doc(
		"Education Fee Installment",
		{"policy_version": policy, "installment_number": 1},
		{
			"policy_version": policy,
			"installment_number": 1,
			"due_date": "2026-02-15",
			"percentage": 100,
			"amount": 850,
		},
	)


def _ensure_adjustment(student: str, policy: str, adjustment_type: str, amount: int) -> str:
	return _ensure_doc(
		"Student Fee Adjustment",
		{"student": student, "policy_version": policy, "adjustment_type": adjustment_type},
		{
			"student": student,
			"policy_version": policy,
			"adjustment_type": adjustment_type,
			"status": "Approved",
			"amount": amount,
			"approved_on": "2026-02-01 10:00:00",
			"reason": f"Synthetic {adjustment_type.lower()} proof",
		},
	)


def _ensure_fee_schedule(
	student: str, program: str, academic_year: str, academic_term: str, fee_category: str
) -> str:
	if existing := frappe.db.exists("Fee Schedule", {"posting_date": "2026-02-01", "due_date": "2026-02-15"}):
		return existing
	structure = frappe.new_doc("Fee Structure")
	structure.academic_year = academic_year
	structure.academic_term = academic_term
	structure.program = program
	structure.company = PROOF_COMPANY
	structure.append(
		"components",
		{"fees_category": fee_category, "amount": 850, "discount": 0, "total": 850},
	)
	structure.insert()
	structure.submit()

	group = _ensure_student_group(student, program, academic_year, academic_term)
	schedule = frappe.new_doc("Fee Schedule")
	schedule.fee_structure = structure.name
	schedule.academic_year = academic_year
	schedule.academic_term = academic_term
	schedule.company = PROOF_COMPANY
	schedule.posting_date = "2026-02-01"
	schedule.due_date = "2026-02-15"
	schedule.append(
		"components",
		{
			"fees_category": fee_category,
			"amount": 850,
			"discount": 0,
			"total": 850,
			"item": frappe.db.get_value("Fee Category", fee_category, "item"),
		},
	)
	schedule.append("student_groups", {"student_group": group})
	schedule.insert()
	schedule.submit()
	return schedule.name


def _ensure_student_group(student: str, program: str, academic_year: str, academic_term: str) -> str:
	if existing := frappe.db.exists("Student Group", {"student_group_name": "P5.1 Demand Group"}):
		return existing
	group = frappe.new_doc("Student Group")
	group.student_group_name = "P5.1 Demand Group"
	group.academic_year = academic_year
	group.academic_term = academic_term
	group.group_based_on = "Batch"
	group.program = program
	group.append("students", {"student": student, "active": 1})
	group.insert()
	return group.name


def _ensure_sales_invoice(fee_schedule: str, student: str) -> str:
	if existing := frappe.db.exists(
		"Sales Invoice", {"fee_schedule": fee_schedule, "student": student, "docstatus": 1}
	):
		return existing
	invoice_name = create_sales_invoice(fee_schedule, student)
	invoice = frappe.get_doc("Sales Invoice", invoice_name)
	if invoice.docstatus == 0:
		invoice.submit()
	return invoice.name


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


def _rejects_incorrect_policy_total(fee_code: str, program: str, academic_year: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Education Fee Policy Version",
				"policy_code": "P51-BAD",
				"version": "2026.1",
				"status": "Published",
				"fee_code": fee_code,
				"program": program,
				"academic_year": academic_year,
				"effective_from": "2026-02-01",
				"base_amount": 1000,
				"concession_amount": 100,
				"net_amount": 1000,
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_negative_adjustment(student: str, policy: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Fee Adjustment",
				"student": student,
				"policy_version": policy,
				"adjustment_type": "Fine",
				"status": "Approved",
				"amount": -1,
				"approved_on": "2026-02-01 11:00:00",
				"reason": "Invalid negative adjustment proof",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_incorrect_demand_total(
	student: str, program_enrollment: str, policy: str, invoice: str
) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Student Fee Demand",
				"student": student,
				"program_enrollment": program_enrollment,
				"policy_version": policy,
				"gross_amount": 1000,
				"concession_amount": 100,
				"net_amount": 1000,
				"due_date": "2026-02-15",
				"sales_invoice": invoice,
				"idempotency_key": "P51-BAD-DEMAND-TOTAL",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_invoice_mismatch(student: str, program_enrollment: str, policy: str, invoice: str) -> bool:
	if existing := frappe.db.exists(
		"Student Fee Demand", {"idempotency_key": "P51-BAD-INVOICE-MISMATCH", "docstatus": 0}
	):
		frappe.delete_doc("Student Fee Demand", existing, ignore_permissions=True)
	try:
		doc = frappe.get_doc(
			{
				"doctype": "Student Fee Demand",
				"student": student,
				"program_enrollment": program_enrollment,
				"policy_version": policy,
				"gross_amount": 1000,
				"net_amount": 1000,
				"due_date": "2026-02-15",
				"sales_invoice": invoice,
				"idempotency_key": "P51-BAD-INVOICE-MISMATCH",
			}
		)
		doc.insert(ignore_permissions=True)
		doc.submit()
	except frappe.ValidationError:
		frappe.clear_messages()
		if doc.name and frappe.db.exists("Student Fee Demand", doc.name):
			frappe.delete_doc("Student Fee Demand", doc.name, ignore_permissions=True)
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P5.1 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p51_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P51_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P51_DOCTYPES],
			"role": ["in", ["System Manager", "Accounts User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P51_DOCTYPES):
		frappe.throw("P5.1 proof failed: expected custom fee policy/demand DocTypes.")
	if result["permission_count"] < len(P51_DOCTYPES) * 2:
		frappe.throw("P5.1 proof failed: expected System Manager and Accounts User permissions.")
	if result["policy_net_amount"] != 850 or result["installment_total"] != 850:
		frappe.throw("P5.1 proof failed: policy and installment totals do not match.")
	if result["sales_invoice_docstatus"] != 1 or result["sales_invoice_total"] != 850:
		frappe.throw("P5.1 proof failed: submitted Sales Invoice does not match demand.")
	if result["demand"] != result["repeated_demand"]:
		frappe.throw("P5.1 proof failed: repeated demand generation did not reuse demand.")
	if result["demand_status"] != "Generated" or result["demand_net_amount"] != 850:
		frappe.throw("P5.1 proof failed: generated demand did not reconcile.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P5.1 proof failed: expected invalid fee records to be rejected.")
	if result["audit_versions"] < 1:
		frappe.throw("P5.1 proof failed: expected audit Version evidence.")
