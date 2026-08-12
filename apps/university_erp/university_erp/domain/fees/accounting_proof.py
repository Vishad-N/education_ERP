from __future__ import annotations

import frappe
from education.education.doctype.fee_schedule.fee_schedule import create_sales_invoice
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from erpnext.setup.utils import enable_all_roles_and_domains
from frappe.utils import flt, now_datetime, nowdate


PROOF_COMPANY = "P2.2 Accounting Proof School"
PROOF_ABBR = "P22"
PROOF_PROGRAM = "P2.2 Accounting Proof Program"
PROOF_ACADEMIC_YEAR = "P2.2 AY 2026"
PROOF_ACADEMIC_TERM = "P2.2 Term 1"
PROOF_FEE_CATEGORY = "P2.2 Tuition Fee"
PROOF_STUDENT_GROUP = "P2.2 Accounting Proof Group"
PROOF_AMOUNT = 1000.0
FIRST_PAYMENT_AMOUNT = 400.0
SECOND_PAYMENT_AMOUNT = 600.0


def run_accounting_proof() -> dict:
	"""Run the local P2.2 fee-to-GL accounting proof on the current site."""

	frappe.flags.in_test = True
	frappe.set_user("Administrator")

	company = _ensure_accounting_setup()
	student = _ensure_education_setup(company)
	fee_schedule = _create_fee_schedule()
	invoice = _create_submitted_sales_invoice(fee_schedule, student)

	first_event_id = f"P2.2-PAY-1-{invoice.name}"
	second_event_id = f"P2.2-PAY-2-{invoice.name}"
	refund_event_id = f"P2.2-REFUND-1-{invoice.name}"

	first_payment = _post_payment_once(
		external_event_id=first_event_id,
		invoice_name=invoice.name,
		amount=FIRST_PAYMENT_AMOUNT,
		bank_account=_account("Cash"),
	)
	duplicate_payment = _post_payment_once(
		external_event_id=first_event_id,
		invoice_name=invoice.name,
		amount=FIRST_PAYMENT_AMOUNT,
		bank_account=_account("Cash"),
	)

	second_payment = _post_payment_once(
		external_event_id=second_event_id,
		invoice_name=invoice.name,
		amount=SECOND_PAYMENT_AMOUNT,
		bank_account=_account("Cash"),
	)

	credit_note = _create_credit_note(invoice.name)
	refund_payment = _post_payment_once(
		external_event_id=refund_event_id,
		invoice_name=credit_note.name,
		amount=None,
		bank_account=_account("Cash"),
	)
	duplicate_refund = _post_payment_once(
		external_event_id=refund_event_id,
		invoice_name=credit_note.name,
		amount=None,
		bank_account=_account("Cash"),
	)

	invoice.reload()
	credit_note.reload()

	result = {
		"site": frappe.local.site,
		"company": company,
		"student": student,
		"fee_schedule": fee_schedule,
		"sales_invoice": invoice.name,
		"sales_invoice_grand_total": flt(invoice.grand_total, 2),
		"sales_invoice_outstanding_after_payments": flt(invoice.outstanding_amount, 2),
		"first_payment_entry": first_payment.name,
		"duplicate_payment_entry": duplicate_payment.name,
		"duplicate_payment_reused_existing": first_payment.name == duplicate_payment.name,
		"second_payment_entry": second_payment.name,
		"credit_note": credit_note.name,
		"credit_note_grand_total": flt(credit_note.grand_total, 2),
		"refund_payment_entry": refund_payment.name,
		"duplicate_refund_entry": duplicate_refund.name,
		"duplicate_refund_reused_existing": refund_payment.name == duplicate_refund.name,
		"payment_entries_for_first_event": frappe.db.count(
			"Payment Entry",
			{"reference_no": first_event_id, "docstatus": 1},
		),
		"payment_entries_for_refund_event": frappe.db.count(
			"Payment Entry",
			{"reference_no": refund_event_id, "docstatus": 1},
		),
		"gl_balance_by_account": _gl_balance_by_account(
			[invoice.name, credit_note.name, first_payment.name, second_payment.name, refund_payment.name]
		),
	}

	_assert_proof_result(result)
	frappe.db.commit()
	return result


def _ensure_accounting_setup() -> str:
	if not frappe.db.exists("Company", PROOF_COMPANY):
		from frappe.desk.page.setup_wizard.setup_wizard import setup_complete

		year = now_datetime().year
		setup_complete(
			{
				"currency": "INR",
				"full_name": "P2.2 Proof User",
				"company_name": PROOF_COMPANY,
				"timezone": "Asia/Kolkata",
				"company_abbr": PROOF_ABBR,
				"industry": "Education",
				"country": "India",
				"fy_start_date": f"{year}-01-01",
				"fy_end_date": f"{year}-12-31",
				"language": "english",
				"company_tagline": "Synthetic accounting proof",
				"email": "p22-proof@example.invalid",
				"password": "admin",
				"chart_of_accounts": "Standard",
			}
		)

	enable_all_roles_and_domains()
	frappe.defaults.set_user_default("Company", PROOF_COMPANY)
	frappe.db.set_single_value("Global Defaults", "default_company", PROOF_COMPANY)
	frappe.db.set_single_value("Education Settings", "create_so", 0)
	frappe.db.set_single_value("Education Settings", "auto_submit_sales_invoice", 1)
	frappe.db.set_single_value("Stock Settings", "auto_insert_price_list_rate_if_missing", 0)
	return PROOF_COMPANY


def _ensure_education_setup(company: str) -> str:
	_ensure_doc(
		"Academic Year",
		{"academic_year_name": PROOF_ACADEMIC_YEAR},
		{
			"academic_year_name": PROOF_ACADEMIC_YEAR,
			"year_start_date": "2026-04-01",
			"year_end_date": "2027-03-31",
		},
	)
	academic_term = _ensure_doc(
		"Academic Term",
		{"term_name": PROOF_ACADEMIC_TERM},
		{
			"term_name": PROOF_ACADEMIC_TERM,
			"academic_year": PROOF_ACADEMIC_YEAR,
			"term_start_date": "2026-04-01",
			"term_end_date": "2026-09-30",
		},
	)
	_ensure_doc(
		"Program",
		{"program_name": PROOF_PROGRAM},
		{"program_name": PROOF_PROGRAM},
	)
	_ensure_fee_category(company)

	student = _ensure_doc(
		"Student",
		{"student_email_id": "p22.accounting.proof@example.invalid"},
		{
			"first_name": "P22",
			"last_name": "Accounting Proof",
			"student_email_id": "p22.accounting.proof@example.invalid",
			"enabled": 1,
		},
	)

	if not frappe.db.exists(
		"Program Enrollment",
		{
			"student": student,
			"program": PROOF_PROGRAM,
			"academic_year": PROOF_ACADEMIC_YEAR,
			"academic_term": academic_term,
			"docstatus": 1,
		},
	):
		enrollment = frappe.new_doc("Program Enrollment")
		enrollment.student = student
		enrollment.program = PROOF_PROGRAM
		enrollment.academic_year = PROOF_ACADEMIC_YEAR
		enrollment.academic_term = academic_term
		enrollment.enrollment_date = nowdate()
		enrollment.insert()
		enrollment.submit()

	if not frappe.db.exists("Student Group", {"student_group_name": PROOF_STUDENT_GROUP}):
		group = frappe.new_doc("Student Group")
		group.student_group_name = PROOF_STUDENT_GROUP
		group.academic_year = PROOF_ACADEMIC_YEAR
		group.academic_term = academic_term
		group.group_based_on = "Batch"
		group.program = PROOF_PROGRAM
		group.append("students", {"student": student, "active": 1})
		group.insert()

	return student


def _ensure_fee_category(company: str) -> str:
	if frappe.db.exists("Fee Category", {"category_name": PROOF_FEE_CATEGORY}):
		return frappe.db.get_value("Fee Category", {"category_name": PROOF_FEE_CATEGORY})

	category = frappe.new_doc("Fee Category")
	category.category_name = PROOF_FEE_CATEGORY
	category.description = "Synthetic P2.2 proof tuition fee"
	category.append(
		"item_defaults",
		{
			"company": company,
			"selling_cost_center": _cost_center(),
			"income_account": _account("Sales"),
		},
	)
	category.insert()
	return category.name


def _create_fee_schedule() -> str:
	academic_term = frappe.db.get_value("Academic Term", {"term_name": PROOF_ACADEMIC_TERM}, "name")
	structure = frappe.new_doc("Fee Structure")
	structure.academic_year = PROOF_ACADEMIC_YEAR
	structure.academic_term = academic_term
	structure.program = PROOF_PROGRAM
	structure.append(
		"components",
		{
			"fees_category": PROOF_FEE_CATEGORY,
			"amount": PROOF_AMOUNT,
			"discount": 0,
			"total": PROOF_AMOUNT,
		},
	)
	structure.insert()
	structure.submit()

	schedule = frappe.new_doc("Fee Schedule")
	schedule.fee_structure = structure.name
	schedule.academic_year = PROOF_ACADEMIC_YEAR
	schedule.academic_term = academic_term
	schedule.company = PROOF_COMPANY
	schedule.posting_date = nowdate()
	schedule.due_date = nowdate()
	schedule.append(
		"components",
		{
			"fees_category": PROOF_FEE_CATEGORY,
			"amount": PROOF_AMOUNT,
			"discount": 0,
			"total": PROOF_AMOUNT,
			"item": frappe.db.get_value("Fee Category", PROOF_FEE_CATEGORY, "item"),
		},
	)
	schedule.append("student_groups", {"student_group": PROOF_STUDENT_GROUP})
	schedule.insert()
	schedule.submit()
	return schedule.name


def _create_submitted_sales_invoice(fee_schedule: str, student: str):
	invoice_name = create_sales_invoice(fee_schedule, student)
	invoice = frappe.get_doc("Sales Invoice", invoice_name)
	if invoice.docstatus == 0:
		invoice.submit()
	return invoice


def _post_payment_once(external_event_id: str, invoice_name: str, amount: float | None, bank_account: str):
	existing_name = frappe.db.exists(
		"Payment Entry", {"reference_no": external_event_id, "docstatus": 1}
	)
	if existing_name:
		return frappe.get_doc("Payment Entry", existing_name)

	payment = get_payment_entry(
		"Sales Invoice",
		invoice_name,
		party_amount=amount,
		bank_account=bank_account,
		reference_date=nowdate(),
	)
	payment.reference_no = external_event_id
	payment.reference_date = nowdate()
	payment.insert()
	payment.submit()
	return payment


def _create_credit_note(invoice_name: str):
	invoice = frappe.get_doc("Sales Invoice", invoice_name)
	credit_note = frappe.new_doc("Sales Invoice")
	credit_note.company = invoice.company
	credit_note.customer = invoice.customer
	credit_note.student = invoice.student
	credit_note.fee_schedule = invoice.fee_schedule
	credit_note.posting_date = nowdate()
	credit_note.due_date = nowdate()
	credit_note.debit_to = invoice.debit_to
	credit_note.is_return = 1
	credit_note.remarks = f"P2.2 standalone refund credit note for {invoice.name}"
	for item in invoice.items:
		credit_note.append(
			"items",
			{
				"item_code": item.item_code,
				"qty": -abs(item.qty),
				"rate": item.rate,
				"income_account": item.income_account,
				"cost_center": item.cost_center or _cost_center(),
			},
		)
	credit_note.insert()
	credit_note.submit()
	return credit_note


def _gl_balance_by_account(vouchers: list[str]) -> list[dict]:
	rows = frappe.db.sql(
		"""
		select account, round(sum(debit), 2) as debit, round(sum(credit), 2) as credit,
		       round(sum(debit - credit), 2) as net
		from `tabGL Entry`
		where voucher_no in %(vouchers)s
		group by account
		order by account
		""",
		{"vouchers": tuple(vouchers)},
		as_dict=True,
	)
	return [dict(row) for row in rows]


def _assert_proof_result(result: dict) -> None:
	if result["sales_invoice_grand_total"] != 1000:
		frappe.throw("P2.2 proof failed: expected Sales Invoice total of 1000.")
	if result["sales_invoice_outstanding_after_payments"] != 0:
		frappe.throw("P2.2 proof failed: Sales Invoice was not fully settled.")
	if not result["duplicate_payment_reused_existing"]:
		frappe.throw("P2.2 proof failed: duplicate payment event created a new Payment Entry.")
	if not result["duplicate_refund_reused_existing"]:
		frappe.throw("P2.2 proof failed: duplicate refund event created a new Payment Entry.")
	if result["payment_entries_for_first_event"] != 1:
		frappe.throw("P2.2 proof failed: duplicate payment event count is not one.")
	if result["payment_entries_for_refund_event"] != 1:
		frappe.throw("P2.2 proof failed: duplicate refund event count is not one.")
	if round(sum(row["net"] for row in result["gl_balance_by_account"]), 2) != 0:
		frappe.throw("P2.2 proof failed: GL entries do not balance.")


def _ensure_doc(doctype: str, filters: dict, values: dict) -> str:
	existing = frappe.db.exists(doctype, filters)
	if existing:
		return existing

	doc = frappe.new_doc(doctype)
	doc.update(values)
	doc.insert()
	return doc.name


def _account(account_name: str) -> str:
	account = frappe.db.get_value(
		"Account",
		{"account_name": account_name, "company": PROOF_COMPANY, "is_group": 0},
		"name",
	)
	if not account:
		frappe.throw(f"Missing account {account_name} for {PROOF_COMPANY}.")
	return account


def _cost_center() -> str:
	cost_center = frappe.db.get_value(
		"Cost Center",
		{"company": PROOF_COMPANY, "is_group": 0},
		"name",
	)
	if not cost_center:
		frappe.throw(f"Missing cost center for {PROOF_COMPANY}.")
	return cost_center
