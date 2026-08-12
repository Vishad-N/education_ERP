from __future__ import annotations

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from frappe.utils import flt, now_datetime, nowdate

from university_erp.domain.fees.accounting_proof import _account
from university_erp.domain.fees.demand_generation_proof import run_demand_generation_proof
from university_erp.integrations.payments.fake_razorpay import FakeRazorpayAdapter
from university_erp.integrations.payments.ports import PaymentOrderRequest


P52_DOCTYPES = ["Payment Provider Event", "Student Fee Payment"]
ONLINE_EVENT_ID = "evt_p52_payment_captured_0001"
ONLINE_PAYMENT_ID = "pay_p52_online_0001"
ONLINE_REFERENCE = f"P5.2-{ONLINE_EVENT_ID}"
OFFLINE_REFERENCE = "P5.2-OFFLINE-RECEIPT-0001"
ONLINE_AMOUNT = 400
OFFLINE_AMOUNT = 450


def run_payment_collection_proof() -> dict:
	"""Create and validate synthetic P5.2 payment collection and receipts."""

	frappe.flags.in_test = True
	frappe.set_user("Administrator")

	demand_result = run_demand_generation_proof()
	demand = demand_result["demand"]
	invoice_name = demand_result["sales_invoice"]

	adapter = FakeRazorpayAdapter()
	order_id = _ensure_provider_order(adapter, demand)
	online_payment = _process_webhook_once(demand, invoice_name, order_id)
	duplicate_webhook_payment = _process_webhook_once(demand, invoice_name, order_id)
	browser_callback_payment = _process_browser_callback_once(demand, invoice_name, order_id)
	offline_payment = _ensure_offline_payment(demand, invoice_name)

	invoice = frappe.get_doc("Sales Invoice", invoice_name)
	validation_checks = {
		"duplicate_provider_payment_rejected": _rejects_duplicate_provider_payment(
			demand, invoice_name, order_id, online_payment["payment_entry"]
		),
		"offline_without_approval_rejected": _rejects_unapproved_offline_payment(
			demand, invoice_name, offline_payment["payment_entry"]
		),
	}
	audit_versions = _ensure_audit_version("Payment Provider Event", online_payment["provider_event"])

	result = {
		"doctype_count": _count_p52_doctypes(),
		"permission_count": _count_required_permissions(),
		"demand": demand,
		"sales_invoice": invoice_name,
		"provider_order_id": order_id,
		"online_fee_payment": online_payment["fee_payment"],
		"online_payment_entry": online_payment["payment_entry"],
		"duplicate_webhook_payment_entry": duplicate_webhook_payment["payment_entry"],
		"browser_callback_payment_entry": browser_callback_payment["payment_entry"],
		"offline_fee_payment": offline_payment["fee_payment"],
		"offline_payment_entry": offline_payment["payment_entry"],
		"online_receipt_no": frappe.db.get_value(
			"Student Fee Payment", online_payment["fee_payment"], "receipt_no"
		),
		"offline_receipt_no": frappe.db.get_value(
			"Student Fee Payment", offline_payment["fee_payment"], "receipt_no"
		),
		"invoice_outstanding": flt(invoice.outstanding_amount, 2),
		"online_payment_entries_for_event": frappe.db.count(
			"Payment Entry", {"reference_no": ONLINE_REFERENCE, "docstatus": 1}
		),
		"offline_payment_entries_for_receipt": frappe.db.count(
			"Payment Entry", {"reference_no": OFFLINE_REFERENCE, "docstatus": 1}
		),
		"validation_checks": validation_checks,
		"audit_versions": audit_versions,
	}
	_assert_result(result)
	frappe.db.commit()
	return result


def _ensure_provider_order(adapter: FakeRazorpayAdapter, demand: str) -> str:
	if existing := frappe.db.exists(
		"Payment Provider Event", {"idempotency_key": "P52-ORDER-DEMAND-PRIMARY"}
	):
		return frappe.db.get_value("Payment Provider Event", existing, "provider_order_id")

	order = adapter.create_order(
		PaymentOrderRequest(
			amount=ONLINE_AMOUNT * 100,
			currency="INR",
			receipt=f"P52-{demand}",
			notes={"student_fee_demand": demand},
		),
		idempotency_key="P52-ORDER-DEMAND-PRIMARY",
	)
	event = frappe.get_doc(
		{
			"doctype": "Payment Provider Event",
			"provider": adapter.provider,
			"event_type": "Order Created",
			"status": "Processed",
			"provider_event_id": "order_created_p52_0001",
			"provider_order_id": order.order_id,
			"student_fee_demand": demand,
			"amount": ONLINE_AMOUNT,
			"currency": "INR",
			"idempotency_key": "P52-ORDER-DEMAND-PRIMARY",
			"payload": f'{{"order_id":"{order.order_id}"}}',
		}
	)
	event.insert(ignore_permissions=True)
	return order.order_id


def _process_webhook_once(demand: str, invoice_name: str, order_id: str) -> dict:
	if existing_event := frappe.db.exists(
		"Payment Provider Event", {"provider_event_id": ONLINE_EVENT_ID}
	):
		event = frappe.get_doc("Payment Provider Event", existing_event)
		return {"provider_event": event.name, "fee_payment": event.student_fee_payment, "payment_entry": event.payment_entry}

	payment_entry = _post_payment_once(ONLINE_REFERENCE, invoice_name, ONLINE_AMOUNT)
	fee_payment = _ensure_submitted_fee_payment(
		{
			"student_fee_demand": demand,
			"collection_type": "Online",
			"status": "Approved",
			"amount": ONLINE_AMOUNT,
			"currency": "INR",
			"sales_invoice": invoice_name,
			"payment_entry": payment_entry,
			"mode_of_payment": "Razorpay",
			"approved_on": now_datetime(),
			"provider": "fake_razorpay",
			"provider_order_id": order_id,
			"provider_payment_id": ONLINE_PAYMENT_ID,
			"provider_event_id": ONLINE_EVENT_ID,
			"idempotency_key": "P52-ONLINE-RECEIPT-PRIMARY",
			"notes": "Synthetic P5.2 online receipt proof",
		}
	)
	event = frappe.get_doc(
		{
			"doctype": "Payment Provider Event",
			"provider": "fake_razorpay",
			"event_type": "Payment Captured",
			"status": "Processed",
			"provider_event_id": ONLINE_EVENT_ID,
			"provider_order_id": order_id,
			"provider_payment_id": ONLINE_PAYMENT_ID,
			"student_fee_demand": demand,
			"student_fee_payment": fee_payment,
			"payment_entry": payment_entry,
			"amount": ONLINE_AMOUNT,
			"currency": "INR",
			"idempotency_key": "P52-WEBHOOK-PRIMARY",
			"payload": f'{{"payment_id":"{ONLINE_PAYMENT_ID}"}}',
		}
	)
	event.insert(ignore_permissions=True)
	return {"provider_event": event.name, "fee_payment": fee_payment, "payment_entry": payment_entry}


def _process_browser_callback_once(demand: str, invoice_name: str, order_id: str) -> dict:
	if existing := frappe.db.exists(
		"Student Fee Payment",
		{"provider": "fake_razorpay", "provider_payment_id": ONLINE_PAYMENT_ID, "docstatus": 1},
	):
		doc = frappe.get_doc("Student Fee Payment", existing)
		return {"fee_payment": doc.name, "payment_entry": doc.payment_entry}

	return _process_webhook_once(demand, invoice_name, order_id)


def _ensure_offline_payment(demand: str, invoice_name: str) -> dict:
	if existing := frappe.db.exists("Student Fee Payment", {"idempotency_key": "P52-OFFLINE-RECEIPT"}):
		doc = frappe.get_doc("Student Fee Payment", existing)
		return {"fee_payment": doc.name, "payment_entry": doc.payment_entry}

	payment_entry = _post_payment_once(OFFLINE_REFERENCE, invoice_name, OFFLINE_AMOUNT)
	fee_payment = _ensure_submitted_fee_payment(
		{
			"student_fee_demand": demand,
			"collection_type": "Offline",
			"status": "Approved",
			"amount": OFFLINE_AMOUNT,
			"currency": "INR",
			"sales_invoice": invoice_name,
			"payment_entry": payment_entry,
			"mode_of_payment": "Cash",
			"approved_on": now_datetime(),
			"idempotency_key": "P52-OFFLINE-RECEIPT",
			"notes": "Synthetic P5.2 offline receipt proof",
		}
	)
	return {"fee_payment": fee_payment, "payment_entry": payment_entry}


def _post_payment_once(reference_no: str, invoice_name: str, amount: int) -> str:
	if existing := frappe.db.exists("Payment Entry", {"reference_no": reference_no, "docstatus": 1}):
		return existing

	payment = get_payment_entry(
		"Sales Invoice",
		invoice_name,
		party_amount=amount,
		bank_account=_account("Cash"),
		reference_date=nowdate(),
	)
	payment.reference_no = reference_no
	payment.reference_date = nowdate()
	payment.insert(ignore_permissions=True)
	payment.submit()
	return payment.name


def _ensure_submitted_fee_payment(values: dict) -> str:
	if existing := frappe.db.exists("Student Fee Payment", {"idempotency_key": values["idempotency_key"]}):
		doc = frappe.get_doc("Student Fee Payment", existing)
	else:
		doc = frappe.get_doc({"doctype": "Student Fee Payment", **values})
		doc.insert(ignore_permissions=True)
	if doc.docstatus == 0:
		doc.submit()
	return doc.name


def _rejects_duplicate_provider_payment(
	demand: str, invoice_name: str, order_id: str, payment_entry: str
) -> bool:
	if existing := frappe.db.exists(
		"Student Fee Payment", {"idempotency_key": "P52-DUPLICATE-PROVIDER-PAYMENT", "docstatus": 0}
	):
		frappe.delete_doc("Student Fee Payment", existing, ignore_permissions=True)
	try:
		frappe.get_doc(
			{
				"doctype": "Student Fee Payment",
				"student_fee_demand": demand,
				"collection_type": "Online",
				"status": "Approved",
				"amount": ONLINE_AMOUNT,
				"currency": "INR",
				"sales_invoice": invoice_name,
				"payment_entry": payment_entry,
				"mode_of_payment": "Razorpay",
				"approved_on": now_datetime(),
				"provider": "fake_razorpay",
				"provider_order_id": order_id,
				"provider_payment_id": ONLINE_PAYMENT_ID,
				"provider_event_id": "evt_p52_duplicate_provider_payment",
				"idempotency_key": "P52-DUPLICATE-PROVIDER-PAYMENT",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _rejects_unapproved_offline_payment(demand: str, invoice_name: str, payment_entry: str) -> bool:
	if existing := frappe.db.exists(
		"Student Fee Payment", {"idempotency_key": "P52-UNAPPROVED-OFFLINE", "docstatus": 0}
	):
		frappe.delete_doc("Student Fee Payment", existing, ignore_permissions=True)
	try:
		doc = frappe.get_doc(
			{
				"doctype": "Student Fee Payment",
				"student_fee_demand": demand,
				"collection_type": "Offline",
				"status": "Approved",
				"amount": OFFLINE_AMOUNT,
				"currency": "INR",
				"sales_invoice": invoice_name,
				"payment_entry": payment_entry,
				"mode_of_payment": "Cash",
				"idempotency_key": "P52-UNAPPROVED-OFFLINE",
			}
		)
		doc.insert(ignore_permissions=True)
		doc.submit()
	except frappe.ValidationError:
		frappe.clear_messages()
		if doc.name and frappe.db.exists("Student Fee Payment", doc.name):
			frappe.delete_doc("Student Fee Payment", doc.name, ignore_permissions=True)
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original = doc.notes
	doc.notes = "P5.2 audit proof"
	doc.save(ignore_permissions=True)
	doc.notes = original
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p52_doctypes() -> int:
	return frappe.db.count("DocType", {"module": "University ERP", "name": ["in", P52_DOCTYPES]})


def _count_required_permissions() -> int:
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", P52_DOCTYPES],
			"role": ["in", ["System Manager", "Accounts User"]],
			"read": 1,
		},
	)


def _assert_result(result: dict) -> None:
	if result["doctype_count"] != len(P52_DOCTYPES):
		frappe.throw("P5.2 proof failed: expected payment DocTypes.")
	if result["permission_count"] < len(P52_DOCTYPES) * 2:
		frappe.throw("P5.2 proof failed: expected System Manager and Accounts User permissions.")
	if result["online_payment_entry"] != result["duplicate_webhook_payment_entry"]:
		frappe.throw("P5.2 proof failed: duplicate webhook posted another Payment Entry.")
	if result["online_payment_entry"] != result["browser_callback_payment_entry"]:
		frappe.throw("P5.2 proof failed: browser callback posted another Payment Entry.")
	if result["online_payment_entries_for_event"] != 1:
		frappe.throw("P5.2 proof failed: provider event has more than one Payment Entry.")
	if result["offline_payment_entries_for_receipt"] != 1:
		frappe.throw("P5.2 proof failed: offline receipt has more than one Payment Entry.")
	if result["invoice_outstanding"] != 0:
		frappe.throw("P5.2 proof failed: invoice was not settled by online and offline payments.")
	if not result["online_receipt_no"] or not result["offline_receipt_no"]:
		frappe.throw("P5.2 proof failed: expected generated receipt numbers.")
	if not all(result["validation_checks"].values()):
		frappe.throw("P5.2 proof failed: expected invalid payment records to be rejected.")
	if result["audit_versions"] < 1:
		frappe.throw("P5.2 proof failed: expected audit Version evidence.")
