import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class StudentFeeRefund(Document):
	def validate(self):
		if flt(self.amount) <= 0:
			frappe.throw(_("Amount must be greater than zero."))
		if self.status in {"Approved", "Posted"} and not self.approved_on:
			frappe.throw(_("Approved On is required for approved refunds."))
		if self.student_fee_payment:
			payment = frappe.get_doc("Student Fee Payment", self.student_fee_payment)
			if payment.docstatus != 1:
				frappe.throw(_("Student Fee Payment must be submitted."))
			if self.student_fee_demand and self.student_fee_demand != payment.student_fee_demand:
				frappe.throw(_("Refund demand must match the linked fee payment."))
			self.student_fee_demand = payment.student_fee_demand
			self.sales_invoice = payment.sales_invoice
			self.provider = payment.provider
			self.provider_payment_id = payment.provider_payment_id

		if self.provider_refund_id:
			duplicate = frappe.db.exists(
				"Student Fee Refund",
				{
					"provider": self.provider,
					"provider_refund_id": self.provider_refund_id,
					"docstatus": 1,
					"name": ["!=", self.name],
				},
			)
			if duplicate:
				frappe.throw(_("Provider refund has already been posted."))

	def before_submit(self):
		if self.status != "Approved":
			frappe.throw(_("Only approved refunds can be posted."))
		if not self.credit_note or not self.refund_payment_entry:
			frappe.throw(_("Credit Note and Refund Payment Entry are required before posting."))

		credit_note = frappe.get_doc("Sales Invoice", self.credit_note)
		if credit_note.docstatus != 1 or not credit_note.is_return:
			frappe.throw(_("Credit Note must be a submitted return Sales Invoice."))
		if flt(abs(credit_note.grand_total), 2) != flt(self.amount, 2):
			frappe.throw(_("Credit Note total must match the refund amount."))

		refund_payment = frappe.get_doc("Payment Entry", self.refund_payment_entry)
		if refund_payment.docstatus != 1:
			frappe.throw(_("Refund Payment Entry must be submitted."))
		if flt(refund_payment.paid_amount, 2) != flt(self.amount, 2):
			frappe.throw(_("Refund Payment Entry amount must match the refund amount."))

		self.status = "Posted"
