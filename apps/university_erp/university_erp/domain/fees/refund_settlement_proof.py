from __future__ import annotations

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from frappe.utils import flt, now_datetime, nowdate

from university_erp.domain.fees.accounting_proof import _account, _cost_center
from university_erp.domain.fees.payment_collection_proof import (
	ONLINE_AMOUNT,
	ONLINE_PAYMENT_ID,
	run_payment_collection_proof,
)
from university_erp.integrations.payments.fake_razorpay import FakeRazorpayAdapter
from university_erp.integrations.payments.ports import PaymentOrderRequest


P53_DOCTYPES = [
	"Student Fee Refund",
	"Payment Settlement Import",
	"Fee General Ledger Reconciliation",
]
REFUND_AMOUNT = 200
REFUND_REFERENCE = "P5.3-REFUND-0001"
REFUND_EVENT_ID = "evt_p53_refund_processed_0001"
SETTLEMENT_ID = "setl_p53_0001"


def run_refund_settlement_proof() -> dict:
	"""Create and validate synthetic P5.3 refund, settlement and GL reconciliation."""

	frappe.flags.in_test = True
	frappe.set_user("Administrator")

	payment_result = run_payment_collection_proof()
	demand = payment_result["demand"]
	invoice_name = payment_result["sales_invoice"]
	online_fee_payment = payment_result["online_fee_payment"]

	refund = _ensure_refund(online_fee_payment, invoice_name)
	settlement = _ensure_settlement(payment_result["online_payment_entry"])
	reconciliation = _ensure_reconciliation(
		demand,
		invoice_name,
		[
			invoice_name,
			payment_result["online_payment_entry"],
			payment_result["offline_payment_entry"],
			refund["credit_note"],
			refund["refund_payment_entry"],
		],
	)
	validation_checks = {
		"duplicate_provider_refund_rejected": _rejects_duplicate_provider_refund(
			online_fee_payment,
			refund["credit_note"],
			refund["refund_payment_entry"],
			refund["provider_refund_id"],
		),
		"unapproved_refund_rejected": _rejects_unapproved_refund(
			online_fee_payment,
			refund["credit_note"],
			refund["refund_payment_entry"],
		),
		"settlement_mismatch_rejected": _rejects_settlement_mismatch(),
		"gl_mismatch_rejected": _rejects_gl_mismatch(demand, invoice_name),
	}
	audit_versions = _ensure_audit_version("Payment Settlement Import", settlement)

	result = {
		"doctype_count": _count_p53_doctypes(),
		"permission_count": _count_required_permissions(),
		"demand": demand,
		"sales_invoice": invoice_name,
		"student_fee_refund": refund["student_fee_refund"],
		"credit_note": refund["credit_note"],
		"credit_note_total": flt(
			abs(frappe.db.get_value("Sales Invoice", refund["credit_note"], "grand_total")), 2
		),
		"refund_payment_entry": refund["refund_payment_entry"],
		"duplicate_refund_payment_entry": _post_refund_once(refund["credit_note"]),
		"provider_refund_event": refund["provider_refund_event"],
		"provider_refund_id": refund["provider_refund_id"],
		"settlement": settlement,
		"settlement_status": frappe.db.get_value("Payment Settlement Import", settlement, "status"),
		"settlement_difference": flt(
			frappe.db.get_value("Payment Settlement Import", settlement, "difference_amount"), 2
		),
		"reconciliation": reconciliation,
		"reconciliation_status": frappe.db.get_value(
			"Fee General Ledger Reconciliation", reconciliation, "status"
		),
		"reconciliation_gl_balance": flt(
			frappe.db.get_value("Fee General Ledger Reconciliation", reconciliation, "gl_balance"),
			2,
		),
		"refund_payment_entries_for_event": frappe.db.count(
			"Payment Entry", {"reference_no": REFUND_REFERENCE, "docstatus": 1}
		),
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_refund(student_fee_payment: str, invoice_name: str) -> dict:
	if existing := frappe.db.exists("Student Fee Refund", {"idempotency_key": "P53-REFUND-PRIMARY"}):
		refund = frappe.get_doc("Student Fee Refund", existing)
		event = frappe.db.get_value(
			"Payment Provider Event", {"provider_event_id": REFUND_EVENT_ID}, "name"
		)
		return {
			"student_fee_refund": refund.name,
			"credit_note": refund.credit_note,
			"refund_payment_entry": refund.refund_payment_entry,
			"provider_refund_event": event,
			"provider_refund_id": refund.provider_refund_id,
		}

	provider_refund_id = _create_provider_refund_id()
	credit_note = _ensure_credit_note(invoice_name)
	refund_payment_entry = _post_refund_once(credit_note)
	refund = frappe.get_doc(
		{
			"doctype": "Student Fee Refund",
			"student_fee_payment": student_fee_payment,
			"status": "Approved",
			"amount": REFUND_AMOUNT,
			"credit_note": credit_note,
			"refund_payment_entry": refund_payment_entry,
			"approved_on": now_datetime(),
			"provider_refund_id": provider_refund_id,
			"idempotency_key": "P53-REFUND-PRIMARY",
			"reason": "Synthetic P5.3 refund proof",
		}
	)
	refund.insert(ignore_permissions=True)
	refund.submit()
	event = _ensure_refund_event(refund.name, provider_refund_id)
	return {
		"student_fee_refund": refund.name,
		"credit_note": credit_note,
		"refund_payment_entry": refund_payment_entry,
		"provider_refund_event": event,
		"provider_refund_id": provider_refund_id,
	}


def _create_provider_refund_id() -> str:
	adapter = FakeRazorpayAdapter()
	order = adapter.create_order(
		PaymentOrderRequest(amount=ONLINE_AMOUNT * 100, currency="INR", receipt="P53-REFUND"),
		idempotency_key="P53-REFUND-ORDER",
	)
	payment = adapter.capture_payment(order.order_id)
	refund = adapter.refund(payment.payment_id, REFUND_AMOUNT * 100, idempotency_key="P53-REFUND")
	return refund.refund_id


def _ensure_credit_note(invoice_name: str) -> str:
	if existing := frappe.db.exists(
		"Sales Invoice",
		{
			"is_return": 1,
			"return_against": invoice_name,
			"remarks": "P5.3 synthetic partial refund credit note",
			"docstatus": 1,
		},
	):
		return existing

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
	credit_note.return_against = invoice.name
	credit_note.remarks = "P5.3 synthetic partial refund credit note"
	item = invoice.items[0]
	credit_note.append(
		"items",
		{
			"item_code": item.item_code,
			"qty": -1,
			"rate": REFUND_AMOUNT,
			"income_account": item.income_account,
			"cost_center": item.cost_center or _cost_center(),
		},
	)
	credit_note.insert(ignore_permissions=True)
	credit_note.submit()
	return credit_note.name


def _post_refund_once(credit_note: str) -> str:
	if existing := frappe.db.exists("Payment Entry", {"reference_no": REFUND_REFERENCE, "docstatus": 1}):
		return existing
	payment = get_payment_entry(
		"Sales Invoice",
		credit_note,
		bank_account=_account("Cash"),
		reference_date=nowdate(),
	)
	payment.reference_no = REFUND_REFERENCE
	payment.reference_date = nowdate()
	payment.insert(ignore_permissions=True)
	payment.submit()
	return payment.name


def _ensure_refund_event(student_fee_refund: str, provider_refund_id: str) -> str:
	if existing := frappe.db.exists("Payment Provider Event", {"provider_event_id": REFUND_EVENT_ID}):
		return existing
	event = frappe.get_doc(
		{
			"doctype": "Payment Provider Event",
			"provider": "fake_razorpay",
			"event_type": "Refund Processed",
			"status": "Processed",
			"provider_event_id": REFUND_EVENT_ID,
			"provider_payment_id": ONLINE_PAYMENT_ID,
			"student_fee_payment": frappe.db.get_value(
				"Student Fee Refund", student_fee_refund, "student_fee_payment"
			),
			"payment_entry": frappe.db.get_value(
				"Student Fee Refund", student_fee_refund, "refund_payment_entry"
			),
			"amount": REFUND_AMOUNT,
			"currency": "INR",
			"idempotency_key": "P53-REFUND-EVENT",
			"payload": f'{{"refund_id":"{provider_refund_id}"}}',
			"notes": "Synthetic P5.3 refund provider event",
		}
	)
	event.insert(ignore_permissions=True)
	return event.name


def _ensure_settlement(online_payment_entry: str) -> str:
	if existing := frappe.db.exists("Payment Settlement Import", {"idempotency_key": "P53-SETTLEMENT"}):
		return existing
	settlement = frappe.get_doc(
		{
			"doctype": "Payment Settlement Import",
			"provider": "fake_razorpay",
			"settlement_id": SETTLEMENT_ID,
			"status": "Reconciled",
			"settlement_date": nowdate(),
			"payment_count": 1,
			"settlement_amount": ONLINE_AMOUNT,
			"expected_amount": _payment_entry_amount(online_payment_entry),
			"idempotency_key": "P53-SETTLEMENT",
			"notes": "Synthetic P5.3 settlement proof",
		}
	)
	settlement.insert(ignore_permissions=True)
	return settlement.name


def _ensure_reconciliation(demand: str, invoice_name: str, vouchers: list[str]) -> str:
	if existing := frappe.db.exists(
		"Fee General Ledger Reconciliation", {"idempotency_key": "P53-GL-RECON"}
	):
		return existing
	gl_balance = _gl_balance(vouchers)
	reconciliation = frappe.get_doc(
		{
			"doctype": "Fee General Ledger Reconciliation",
			"student_fee_demand": demand,
			"sales_invoice": invoice_name,
			"status": "Reconciled",
			"checked_on": now_datetime(),
			"total_fee_amount": flt(frappe.db.get_value("Sales Invoice", invoice_name, "grand_total"), 2),
			"collected_amount": 850,
			"refund_amount": REFUND_AMOUNT,
			"gl_balance": gl_balance,
			"idempotency_key": "P53-GL-RECON",
			"notes": "Synthetic P5.3 GL reconciliation proof",
		}
	)
	reconciliation.insert(ignore_permissions=True)
	return reconciliation.name


def _payment_entry_amount(payment_entry: str) -> float:
	return flt(frappe.db.get_value("Payment Entry", payment_entry, "paid_amount"), 2)


def _gl_balance(vouchers: list[str]) -> float:
	rows = frappe.db.sql(
		"""
		select round(sum(debit - credit), 2) as net
		from `tabGL Entry`
		where voucher_no in %(vouchers)s
		""",
		{"vouchers": tuple(vouchers)},
		as_dict=True,
	)
	return flt(rows[0].net if rows else 0, 2)


def _rejects_duplicate_provider_refund(
	student_fee_payment: str, credit_note: str, refund_payment_entry: str, provider_refund_id: str
) -> bool:
	if existing := frappe.db.exists(
		"Student Fee Refund", {"idempotency_key": "P53-DUPLICATE-REFUND", "docstatus": 0}
	):
		frappe.delete_doc("Student Fee Refund", existing, ignore_permissions=True)
	try:
		frappe.get_doc(
			{
				"doctype": "Student Fee Refund",
				"student_fee_payment": student_fee_payment,
				"status": "Approved",
				"amount": REFUND_AMOUNT,
				"credit_note": credit_note,
				"refund_payment_entry": refund_payment_entry,
				"approved_on": now_datetime(),
				"provider_refund_id": provider_refund_id,
				"idempotency_key": "P53-DUPLICATE-REFUND",
				"reason": "Duplicate refund proof",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_unapproved_refund(
	student_fee_payment: str, credit_note: str, refund_payment_entry: str
) -> bool:
	if existing := frappe.db.exists(
		"Student Fee Refund", {"idempotency_key": "P53-UNAPPROVED-REFUND", "docstatus": 0}
	):
		frappe.delete_doc("Student Fee Refund", existing, ignore_permissions=True)
	try:
		doc = frappe.get_doc(
			{
				"doctype": "Student Fee Refund",
				"student_fee_payment": student_fee_payment,
				"status": "Draft",
				"amount": REFUND_AMOUNT,
				"credit_note": credit_note,
				"refund_payment_entry": refund_payment_entry,
				"idempotency_key": "P53-UNAPPROVED-REFUND",
				"reason": "Unapproved refund proof",
			}
		)
		doc.insert(ignore_permissions=True)
		doc.submit()
	except frappe.ValidationError:
		frappe.clear_messages()
		if doc.name and frappe.db.exists("Student Fee Refund", doc.name):
			frappe.delete_doc("Student Fee Refund", doc.name, ignore_permissions=True)
		return True
	return False


def _rejects_settlement_mismatch() -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Payment Settlement Import",
				"provider": "fake_razorpay",
				"settlement_id": "setl_p53_bad_0001",
				"status": "Reconciled",
				"settlement_date": nowdate(),
				"payment_count": 1,
				"settlement_amount": ONLINE_AMOUNT - 1,
				"expected_amount": ONLINE_AMOUNT,
				"idempotency_key": "P53-BAD-SETTLEMENT",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_gl_mismatch(demand: str, invoice_name: str) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Fee General Ledger Reconciliation",
				"student_fee_demand": demand,
				"sales_invoice": invoice_name,
				"status": "Reconciled",
				"checked_on": now_datetime(),
				"total_fee_amount": 850,
				"collected_amount": 850,
				"refund_amount": REFUND_AMOUNT,
				"gl_balance": 1,
				"idempotency_key": "P53-BAD-GL-RECON",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P5.3 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p53_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P53_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P53_DOCTYPES],
			"role": ["in", ["System Manager", "Accounts User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P53_DOCTYPES):
		frappe.throw("P5.3 proof failed: expected refund, settlement and reconciliation DocTypes.")
	if result["permission_count"] < len(P53_DOCTYPES) * 2:
		frappe.throw("P5.3 proof failed: expected System Manager and Accounts User permissions.")
	if result["credit_note_total"] != REFUND_AMOUNT:
		frappe.throw("P5.3 proof failed: credit note total does not match refund amount.")
	if result["refund_payment_entry"] != result["duplicate_refund_payment_entry"]:
		frappe.throw("P5.3 proof failed: duplicate refund event posted another Payment Entry.")
	if result["refund_payment_entries_for_event"] != 1:
		frappe.throw("P5.3 proof failed: refund event has more than one Payment Entry.")
	if result["settlement_status"] != "Reconciled" or result["settlement_difference"] != 0:
		frappe.throw("P5.3 proof failed: settlement did not reconcile.")
	if result["reconciliation_status"] != "Reconciled" or result["reconciliation_gl_balance"] != 0:
		frappe.throw("P5.3 proof failed: GL reconciliation did not balance.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P5.3 proof failed: expected invalid refund/reconciliation records to be rejected.")
	if result["audit_versions"] < 1:
		frappe.throw("P5.3 proof failed: expected audit Version evidence.")
