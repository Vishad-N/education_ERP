"""Public, low-bandwidth endpoints for the applicant and guardian portal."""

import hashlib
import json
import base64
import mimetypes
import secrets
from html import escape
from datetime import timedelta

import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe.utils import add_to_date, get_datetime
from frappe.utils.pdf import get_pdf
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

from university_erp.integrations.antivirus.fake_clamav import FakeClamAvAdapter
from university_erp.integrations.payments.fake_razorpay import FakeRazorpayAdapter
from university_erp.integrations.payments.ports import PaymentOrderRequest
from university_erp.integrations.storage.fake_r2 import FakeR2Adapter
from university_erp.domain.fees.accounting_proof import _account


def _hash_token(token: str) -> str:
	return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _open_lead_status() -> str:
	"""Pick a CRM lead status that does not require a lost reason."""
	for lead_status in ("New", "New Lead"):
		if name := frappe.db.get_value("CRM Lead Status", {"lead_status": lead_status}, "name"):
			return name
	if name := frappe.db.get_value("CRM Lead Status", {"type": "Open"}, "name"):
		return name
	frappe.throw(_("No open CRM lead status is configured for new applications."))


def _application_fee_config() -> dict:
	"""Application fee is waived until a payment gateway is configured."""
	mode = str(frappe.conf.get("application_fee_mode") or "waived").strip().lower()
	if mode not in {"waived", "offline", "gateway"}:
		mode = "waived"
	required = mode == "gateway"
	return {
		"mode": mode,
		"required": required,
		"amount": 500 if required else 0,
		"currency": "INR",
	}


def _published_form(form_version: str | None = None):
	filters = {"status": "Published"}
	if form_version:
		filters["name"] = form_version
	form = frappe.db.get_value(
		"Admission Application Form Version",
		filters,
		["name", "program", "academic_year", "form_schema"],
		as_dict=True,
	)
	if not form:
		frappe.throw(_("No published admission form is available."))
	return form


@frappe.whitelist(allow_guest=True)
def get_application_context():
	"""Return only published form metadata needed to start an application."""
	forms = frappe.get_all(
		"Admission Application Form Version",
		filters={"status": "Published"},
		fields=["name", "program", "academic_year", "form_schema"],
		order_by="published_on desc, name desc",
	)
	for form in forms:
		try:
			form["form_schema"] = json.loads(form["form_schema"] or "{}")
		except (TypeError, ValueError):
			form["form_schema"] = {}
	offerings = frappe.get_all(
		"Program Offering",
		filters={"status": "Open"},
		fields=["program", "academic_year"],
		order_by="program asc",
	)
	programs = []
	seen = set()
	for row in offerings:
		if row.program and row.program not in seen:
			seen.add(row.program)
			programs.append(row.program)
	if not programs:
		programs = ["Class 6", "Class 7", "Class 8", "Class 9"]
	return {"forms": forms, "application_fee": _application_fee_config(), "programs": programs}


@frappe.whitelist(allow_guest=True)
def save_application_draft(payload: str, resume_token: str | None = None, form_version: str | None = None):
	"""Create or update a guardian draft without exposing the stored token."""
	try:
		data = json.loads(payload) if isinstance(payload, str) else payload
	except (TypeError, ValueError):
		frappe.throw(_("Application data must be valid JSON."))
	if not isinstance(data, dict):
		frappe.throw(_("Application data must be an object."))

	mobile = "".join(character for character in str(data.get("mobile", "")) if character.isdigit())
	guardian_name = str(data.get("guardianName", "")).strip()
	child_name = str(data.get("childName", "")).strip()
	if len(mobile) != 10 or not guardian_name or not child_name:
		frappe.throw(_("Mobile number, guardian name and child name are required."))

	form = _published_form(form_version or data.get("formVersion"))
	if resume_token:
		draft_name = frappe.db.get_value(
			"Admission Application Draft", {"resume_token_hash": _hash_token(resume_token)}, "name"
		)
	else:
		draft_name = None

	if draft_name:
		draft = frappe.get_doc("Admission Application Draft", draft_name)
		if draft.status != "Draft":
			frappe.throw(_("This application has already been submitted."))
		lead_name = draft.crm_lead
	else:
		status = _open_lead_status()
		lead = frappe.get_doc(
			{
				"doctype": "CRM Lead",
				"naming_series": "CRM-LEAD-.YYYY.-",
				"first_name": child_name,
				"last_name": "",
				"lead_name": child_name,
				"email": f"guardian-{mobile}@example.invalid",
				"mobile_no": mobile,
				"status": status,
			}
		)
		lead.insert(ignore_permissions=True)
		lead_name = lead.name
		resume_token = secrets.token_urlsafe(24)
		draft = frappe.get_doc(
			{
				"doctype": "Admission Application Draft",
				"form_version": form.name,
				"crm_lead": lead_name,
				"status": "Draft",
				"resume_token_hash": _hash_token(resume_token),
				"last_saved_on": now_datetime(),
				"draft_payload": "{}",
			}
		)
		draft.insert(ignore_permissions=True)

	draft.form_version = form.name
	draft.draft_payload = json.dumps(data, sort_keys=True)
	draft.last_saved_on = now_datetime()
	draft.save(ignore_permissions=True)
	frappe.db.commit()
	return {
		"draft": draft.name,
		"form_version": form.name,
		"saved_on": str(draft.last_saved_on),
		"resume_token": resume_token,
		"status": draft.status,
	}


@frappe.whitelist(allow_guest=True)
def get_application_draft(resume_token: str):
	"""Resume a draft using the one-time token returned during save."""
	if not resume_token:
		frappe.throw(_("A resume token is required."))
	draft_name = frappe.db.get_value(
		"Admission Application Draft", {"resume_token_hash": _hash_token(resume_token)}, "name"
	)
	if not draft_name:
		frappe.throw(_("Application draft not found."))
	draft = frappe.get_doc("Admission Application Draft", draft_name)
	return {
		"draft": draft.name,
		"form_version": draft.form_version,
		"payload": json.loads(draft.draft_payload or "{}"),
		"saved_on": str(draft.last_saved_on),
		"status": draft.status,
	}


def _draft_from_token(resume_token: str):
	if not resume_token:
		frappe.throw(_("A resume token is required."))
	draft_name = frappe.db.get_value(
		"Admission Application Draft", {"resume_token_hash": _hash_token(resume_token)}, "name"
	)
	if not draft_name:
		frappe.throw(_("Application draft not found."))
	draft = frappe.get_doc("Admission Application Draft", draft_name)
	if draft.status != "Draft":
		frappe.throw(_("This application is no longer editable."))
	return draft


@frappe.whitelist(allow_guest=True)
def upload_application_document(
	resume_token: str, document_type: str, file_name: str, content_base64: str, idempotency_key: str
):
	"""Store an applicant document in private quarantine and scan it before passing it."""
	draft = _draft_from_token(resume_token)
	if not idempotency_key or len(idempotency_key) > 140:
		frappe.throw(_("A valid upload retry key is required."))
	if existing := frappe.db.exists("Admission Application Document", {"idempotency_key": idempotency_key}):
		doc = frappe.get_doc("Admission Application Document", existing)
		return {"document": doc.name, "scan_status": doc.scan_status, "idempotent": True}
	try:
		body = base64.b64decode(content_base64, validate=True)
	except (ValueError, TypeError):
		frappe.throw(_("The uploaded file is invalid."))
	if not body or len(body) > 5 * 1024 * 1024:
		frappe.throw(_("Files must be smaller than 5 MB."))
	content_type = mimetypes.guess_type(file_name or "")[0] or "application/octet-stream"
	allowed_types = {"application/pdf", "image/jpeg", "image/png"}
	if content_type not in allowed_types:
		frappe.throw(_("Only PDF, JPG and PNG files are accepted."))
	key = f"applications/{draft.name}/{secrets.token_hex(12)}-{file_name.replace('/', '_')}"
	storage = FakeR2Adapter()
	stored = storage.put_private_object(key=key, body=body, content_type=content_type)
	scan = FakeClamAvAdapter().scan(body=body)
	doc = frappe.get_doc(
		{
			"doctype": "Admission Application Document",
			"application_draft": draft.name,
			"document_type": document_type,
			"file_name": file_name,
			"file_key": stored.key,
			"checksum_sha256": stored.checksum_sha256,
			"file_size": stored.size,
			"content_type": content_type,
			"scan_status": "Scan Passed" if scan.status == "clean" else "Scan Failed",
			"scan_provider": scan.provider,
			"scan_failure_reason": scan.signature if scan.status != "clean" else None,
			"idempotency_key": idempotency_key,
		}
	)
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	return {"document": doc.name, "scan_status": doc.scan_status, "idempotent": False}


@frappe.whitelist(allow_guest=True)
def create_application_payment(resume_token: str, idempotency_key: str, amount: float = 500):
	"""Create or retry an application-fee order without charging twice."""
	draft = _draft_from_token(resume_token)
	if not idempotency_key or len(idempotency_key) > 140:
		frappe.throw(_("A valid payment retry key is required."))
	if existing := frappe.db.exists("Admission Payment Attempt", {"idempotency_key": idempotency_key}):
		attempt = frappe.get_doc("Admission Payment Attempt", existing)
		return {
			"attempt": attempt.name,
			"provider_order_id": attempt.provider_order_id,
			"status": attempt.status,
			"idempotent": True,
		}
	fee = _application_fee_config()
	if fee["mode"] != "gateway":
		attempt = frappe.get_doc(
			{
				"doctype": "Admission Payment Attempt",
				"application_draft": draft.name,
				"amount": 0,
				"currency": "INR",
				"status": "Paid",
				"provider": "none",
				"provider_order_id": f"waived-{draft.name}",
				"provider_payment_id": "waived",
				"idempotency_key": idempotency_key,
				"notes": "Application fee waived; no payment gateway.",
			}
		)
		attempt.insert(ignore_permissions=True)
		frappe.db.commit()
		return {
			"attempt": attempt.name,
			"provider_order_id": attempt.provider_order_id,
			"status": attempt.status,
			"idempotent": False,
		}
	if float(amount) != 500:
		frappe.throw(_("The application fee amount is fixed by the published pilot policy."))
	adapter = FakeRazorpayAdapter()
	order = adapter.create_order(
		PaymentOrderRequest(amount=50000, currency="INR", receipt=draft.name, notes={"draft": draft.name}),
		idempotency_key=idempotency_key,
	)
	attempt = frappe.get_doc(
		{
			"doctype": "Admission Payment Attempt",
			"application_draft": draft.name,
			"amount": 500,
			"currency": "INR",
			"status": "Pending",
			"provider": adapter.provider,
			"provider_order_id": order.order_id,
			"idempotency_key": idempotency_key,
		}
	)
	attempt.insert(ignore_permissions=True)
	frappe.db.commit()
	return {
		"attempt": attempt.name,
		"provider_order_id": attempt.provider_order_id,
		"status": attempt.status,
		"idempotent": False,
	}


@frappe.whitelist(allow_guest=True)
def check_application_payment(resume_token: str, idempotency_key: str):
	"""Return the current payment state without creating another provider order."""
	draft = _draft_from_token(resume_token)
	attempt_name = frappe.db.get_value(
		"Admission Payment Attempt",
		{"application_draft": draft.name, "idempotency_key": idempotency_key},
		"name",
	)
	if not attempt_name:
		frappe.throw(_("Payment attempt not found."))
	attempt = frappe.get_doc("Admission Payment Attempt", attempt_name)
	if attempt.status == "Pending" and attempt.provider in {"fake_razorpay", "none"}:
		attempt.status = "Paid"
		attempt.provider_payment_id = attempt.provider_payment_id or f"pay_{attempt.provider_order_id}"
		attempt.save(ignore_permissions=True)
		frappe.db.commit()
	return {
		"attempt": attempt.name,
		"provider_order_id": attempt.provider_order_id,
		"provider_payment_id": attempt.provider_payment_id,
		"status": attempt.status,
	}


@frappe.whitelist(allow_guest=True)
def confirm_application_payment(
	resume_token: str, idempotency_key: str, provider_order_id: str, provider_payment_id: str | None = None
):
	"""Apply one captured fake-provider callback; duplicate callbacks are no-ops."""
	draft = _draft_from_token(resume_token)
	attempt_name = frappe.db.get_value(
		"Admission Payment Attempt",
		{"application_draft": draft.name, "idempotency_key": idempotency_key},
		"name",
	)
	if not attempt_name:
		frappe.throw(_("Payment attempt not found."))
	attempt = frappe.get_doc("Admission Payment Attempt", attempt_name)
	if attempt.status == "Paid":
		return {"attempt": attempt.name, "status": attempt.status, "provider_payment_id": attempt.provider_payment_id, "idempotent": True}
	if provider_order_id != attempt.provider_order_id:
		frappe.throw(_("Provider order does not match this application."))
	adapter = FakeRazorpayAdapter()
	order = adapter.create_order(
		PaymentOrderRequest(amount=50000, currency="INR", receipt=draft.name, notes={"draft": draft.name}),
		idempotency_key=idempotency_key,
	)
	if order.order_id != provider_order_id:
		frappe.throw(_("Provider order could not be verified."))
	payment = adapter.capture_payment(order.order_id)
	attempt.status = "Paid"
	attempt.provider_payment_id = provider_payment_id or payment.payment_id
	attempt.save(ignore_permissions=True)
	frappe.db.commit()
	return {
		"attempt": attempt.name,
		"status": attempt.status,
		"provider_payment_id": attempt.provider_payment_id,
		"idempotent": False,
	}


@frappe.whitelist(allow_guest=True)
def get_student_portal_snapshot(access_token: str):
	"""Return the minimum student/guardian view bound to one expiring access token."""
	if not access_token:
		frappe.throw(_("A portal access token is required."))
	access = frappe.db.get_value(
		"Student Portal Access",
		{"token_hash": _hash_token(access_token), "status": "Active"},
		["name", "student", "guardian", "expires_on"],
		as_dict=True,
	)
	if not access or str(access.expires_on) < str(frappe.utils.today()):
		frappe.throw(_("This portal access link has expired."))
	student = frappe.db.get_value(
		"Student", access.student, ["name", "student_name", "student_email_id"], as_dict=True
	)
	if not student:
		frappe.throw(_("Student record was not found."))
	access_doc = frappe.get_doc("Student Portal Access", access.name)
	access_doc.last_used_on = now_datetime()
	access_doc.save(ignore_permissions=True)
	dues = frappe.get_all(
		"Student Fee Demand",
		filters={"student": access.student, "status": "Generated"},
		fields=["name", "net_amount", "due_date", "sales_invoice", "status"],
		order_by="due_date asc",
	)
	receipts = frappe.get_all(
		"Student Fee Payment",
		filters={"student_fee_demand": ["in", [row.name for row in dues]]} if dues else {"name": ""},
		fields=["name", "amount", "receipt_no", "approved_on", "status"],
		order_by="approved_on desc",
	)
	documents = frappe.get_all(
		"Student Document",
		filters={"student": access.student},
		fields=["name", "document_type", "scan_status", "verification_status", "expiry_date"],
		order_by="creation desc",
	)
	notices = frappe.get_all(
		"Student Portal Notice",
		filters={"status": "Published", "audience": ["in", ["All Students", "Guardians"]]},
		fields=["name", "title", "message", "published_on", "expires_on"],
		order_by="published_on desc",
	)
	frappe.db.commit()
	return {
		"student": student,
		"expires_on": access.expires_on,
		"dues": dues,
		"receipts": receipts,
		"documents": documents,
		"notices": notices,
		"application_fee": _application_fee_config(),
	}


@frappe.whitelist(allow_guest=True)
def download_student_receipt(access_token: str, receipt: str):
	"""Render a receipt only after proving it belongs to the scoped student."""
	if not access_token or not receipt:
		frappe.throw(_("A portal access token and receipt are required."))
	access = frappe.db.get_value(
		"Student Portal Access", {"token_hash": _hash_token(access_token), "status": "Active"}, ["student", "expires_on"], as_dict=True
	)
	if not access or str(access.expires_on) < str(frappe.utils.today()):
		frappe.throw(_("This portal access link has expired."))
	payment = frappe.db.get_value(
		"Student Fee Payment", receipt, ["student_fee_demand", "receipt_no", "amount", "approved_on", "currency"], as_dict=True
	)
	if not payment:
		frappe.throw(_("Receipt not found."))
	if frappe.db.get_value("Student Fee Demand", payment.student_fee_demand, "student") != access.student:
		frappe.throw(_("This receipt is not available for this student."))
	demand = frappe.db.get_value(
		"Student Fee Demand", payment.student_fee_demand, ["student", "due_date", "sales_invoice"], as_dict=True
	)
	student_name = frappe.db.get_value("Student", access.student, "student_name")
	html = f"""
		<h1>Fee Receipt</h1>
		<p><strong>Student:</strong> {escape(student_name or access.student)}</p>
		<p><strong>Receipt:</strong> {escape(payment.receipt_no or receipt)}</p>
		<p><strong>Demand:</strong> {escape(payment.student_fee_demand)}</p>
		<p><strong>Amount:</strong> {escape(str(payment.amount))} {escape(payment.currency or 'INR')}</p>
		<p><strong>Approved on:</strong> {escape(str(payment.approved_on or ''))}</p>
		<p><strong>Invoice:</strong> {escape(str(demand.sales_invoice or ''))}</p>
	"""
	pdf = get_pdf(html)
	frappe.local.response.filename = f"{payment.receipt_no or receipt}.pdf"
	frappe.local.response.filecontent = pdf
	frappe.local.response.type = "download"


@frappe.whitelist(allow_guest=True)
def create_student_payment(access_token: str, student_fee_demand: str, idempotency_key: str):
	"""Create one retry-safe provider order for a scoped student fee demand."""
	if not access_token or not student_fee_demand or not idempotency_key:
		frappe.throw(_("Access, fee demand and retry key are required."))
	access = frappe.db.get_value(
		"Student Portal Access", {"token_hash": _hash_token(access_token), "status": "Active"}, ["student", "expires_on"], as_dict=True
	)
	if not access or str(access.expires_on) < str(frappe.utils.today()):
		frappe.throw(_("This portal access link has expired."))
	demand = frappe.db.get_value(
		"Student Fee Demand", {"name": student_fee_demand, "student": access.student, "status": "Generated"}, ["name", "net_amount", "sales_invoice"], as_dict=True
	)
	if not demand:
		frappe.throw(_("This fee demand is not available for the student."))
	if _application_fee_config()["mode"] != "gateway":
		return {
			"attempt": None,
			"provider_order_id": None,
			"status": "Counter",
			"message": "Pay this fee at the school counter. Online payment is not enabled.",
			"idempotent": True,
		}
	if existing := frappe.db.exists("Student Portal Payment Attempt", {"idempotency_key": idempotency_key}):
		attempt = frappe.get_doc("Student Portal Payment Attempt", existing)
		return {"attempt": attempt.name, "provider_order_id": attempt.provider_order_id, "status": attempt.status, "idempotent": True}
	adapter = FakeRazorpayAdapter()
	order = adapter.create_order(
		PaymentOrderRequest(amount=int(float(demand.net_amount) * 100), currency="INR", receipt=demand.name, notes={"student": access.student}),
		idempotency_key=idempotency_key,
	)
	attempt = frappe.get_doc(
		{
			"doctype": "Student Portal Payment Attempt",
			"student_fee_demand": demand.name,
			"student": access.student,
			"amount": demand.net_amount,
			"currency": "INR",
			"status": "Pending",
			"provider": adapter.provider,
			"provider_order_id": order.order_id,
			"idempotency_key": idempotency_key,
		}
	)
	attempt.insert(ignore_permissions=True)
	frappe.db.commit()
	return {"attempt": attempt.name, "provider_order_id": attempt.provider_order_id, "status": attempt.status, "idempotent": False}


@frappe.whitelist(allow_guest=True)
def confirm_student_payment(access_token: str, attempt: str, provider_order_id: str):
	"""Capture one student payment and post its ERPNext accounting result exactly once."""
	if not access_token or not attempt or not provider_order_id:
		frappe.throw(_("Access, attempt and provider order are required."))
	access = frappe.db.get_value(
		"Student Portal Access", {"token_hash": _hash_token(access_token), "status": "Active"}, ["student", "expires_on"], as_dict=True
	)
	if not access or str(access.expires_on) < str(frappe.utils.today()):
		frappe.throw(_("This portal access link has expired."))
	payment_attempt = frappe.get_doc("Student Portal Payment Attempt", attempt)
	if payment_attempt.student != access.student or payment_attempt.provider_order_id != provider_order_id:
		frappe.throw(_("This payment attempt is not available for the student."))
	if payment_attempt.status == "Paid":
		return {"attempt": attempt, "status": "Paid", "payment": payment_attempt.provider_payment_id, "idempotent": True}
	demand = frappe.get_doc("Student Fee Demand", payment_attempt.student_fee_demand)
	if demand.student != access.student or not demand.sales_invoice:
		frappe.throw(_("This fee demand cannot be paid from the portal."))
	invoice_outstanding = frappe.db.get_value("Sales Invoice", demand.sales_invoice, "outstanding_amount")
	if float(invoice_outstanding or 0) < float(payment_attempt.amount):
		frappe.throw(_("This fee demand has no payable outstanding balance."))
	adapter = FakeRazorpayAdapter()
	order = adapter.create_order(
		PaymentOrderRequest(amount=int(float(payment_attempt.amount) * 100), currency="INR", receipt=demand.name, notes={"student": access.student}),
		idempotency_key=payment_attempt.idempotency_key,
	)
	if order.order_id != provider_order_id:
		frappe.throw(_("Provider order could not be verified."))
	provider_payment = adapter.capture_payment(order.order_id)
	payment_entry = get_payment_entry(
		"Sales Invoice", demand.sales_invoice, party_amount=payment_attempt.amount, bank_account=_account("Cash"), reference_date=frappe.utils.nowdate()
	)
	payment_entry.reference_no = f"PORTAL-{provider_payment.payment_id}"
	payment_entry.reference_date = frappe.utils.nowdate()
	payment_entry.insert(ignore_permissions=True)
	payment_entry.submit()
	fee_payment = frappe.get_doc(
		{
			"doctype": "Student Fee Payment",
			"student_fee_demand": demand.name,
			"collection_type": "Online",
			"status": "Approved",
			"amount": payment_attempt.amount,
			"currency": "INR",
			"sales_invoice": demand.sales_invoice,
			"payment_entry": payment_entry.name,
			"mode_of_payment": "Razorpay",
			"approved_on": now_datetime(),
			"provider": adapter.provider,
			"provider_order_id": provider_order_id,
			"provider_payment_id": provider_payment.payment_id,
			"provider_event_id": f"portal_{provider_payment.payment_id}",
			"idempotency_key": f"portal-payment-{payment_attempt.name}",
		}
	)
	fee_payment.insert(ignore_permissions=True)
	fee_payment.submit()
	payment_attempt.status = "Paid"
	payment_attempt.provider_payment_id = provider_payment.payment_id
	payment_attempt.save(ignore_permissions=True)
	frappe.db.commit()
	return {"attempt": attempt, "status": "Paid", "payment": fee_payment.name, "payment_entry": payment_entry.name, "idempotent": False}


@frappe.whitelist(allow_guest=True)
def check_student_payment(access_token: str, attempt: str):
	access = frappe.db.get_value("Student Portal Access", {"token_hash": _hash_token(access_token), "status": "Active"}, ["student", "expires_on"], as_dict=True)
	if not access:
		frappe.throw(_("This portal access link is invalid."))
	doc = frappe.get_doc("Student Portal Payment Attempt", attempt)
	if doc.student != access.student:
		frappe.throw(_("This payment attempt is not available for the student."))
	return {"attempt": doc.name, "status": doc.status, "provider_order_id": doc.provider_order_id, "provider_payment_id": doc.provider_payment_id}


@frappe.whitelist(allow_guest=True)
def request_student_otp(access_token: str, mobile: str):
	"""Create a local fake OTP challenge; real SMS delivery is a later provider integration."""
	if not access_token or not mobile:
		frappe.throw(_("Access token and mobile are required."))
	access = frappe.db.get_value("Student Portal Access", {"token_hash": _hash_token(access_token), "status": "Active"}, ["student", "expires_on"], as_dict=True)
	if not access or str(access.expires_on) < str(frappe.utils.today()):
		frappe.throw(_("This portal access link has expired."))
	code = "246810"
	challenge = frappe.get_doc(
		{
			"doctype": "Student Portal Otp Challenge",
			"student": access.student,
			"mobile": mobile,
			"code_hash": _hash_token(code),
			"status": "Pending",
			"expires_on": add_to_date(now_datetime(), minutes=10),
			"notes": "Local fake OTP only; never use in production.",
		}
	)
	challenge.insert(ignore_permissions=True)
	frappe.db.commit()
	return {"challenge": challenge.name, "expires_on": challenge.expires_on, "delivery": "fake_local", "test_code": code}


@frappe.whitelist(allow_guest=True)
def verify_student_otp(access_token: str, challenge: str, code: str):
	access = frappe.db.get_value("Student Portal Access", {"token_hash": _hash_token(access_token), "status": "Active"}, ["student", "expires_on"], as_dict=True)
	if not access:
		frappe.throw(_("This portal access link is invalid."))
	doc = frappe.get_doc("Student Portal Otp Challenge", challenge)
	if doc.student != access.student or doc.status != "Pending" or get_datetime(doc.expires_on) < get_datetime(now_datetime()):
		frappe.throw(_("This OTP challenge is no longer valid."))
	doc.attempt_count = (doc.attempt_count or 0) + 1
	if doc.attempt_count > 5:
		doc.status = "Locked"
		doc.save(ignore_permissions=True)
		frappe.throw(_("Too many OTP attempts."))
	if _hash_token(code) != doc.code_hash:
		doc.save(ignore_permissions=True)
		frappe.throw(_("The OTP is incorrect."))
	doc.status = "Verified"
	doc.verified_on = now_datetime()
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	return {"challenge": doc.name, "status": doc.status, "student": doc.student}
