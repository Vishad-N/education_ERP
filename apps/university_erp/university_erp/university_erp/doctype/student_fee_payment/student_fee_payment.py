import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class StudentFeePayment(Document):
	def validate(self):
		if flt(self.amount) <= 0:
			frappe.throw(_("Amount must be greater than zero."))
		if not self.student_fee_demand:
			frappe.throw(_("Student Fee Demand is required."))

		demand = frappe.get_doc("Student Fee Demand", self.student_fee_demand)
		if demand.docstatus != 1:
			frappe.throw(_("Student Fee Demand must be submitted."))
		if not self.sales_invoice:
			self.sales_invoice = demand.sales_invoice
		if self.sales_invoice != demand.sales_invoice:
			frappe.throw(_("Sales Invoice must match the linked fee demand."))

		invoice = frappe.get_doc("Sales Invoice", self.sales_invoice)
		if invoice.docstatus != 1:
			frappe.throw(_("Sales Invoice must be submitted."))

		if self.provider_payment_id:
			duplicate = frappe.db.exists(
				"Student Fee Payment",
				{
					"provider": self.provider,
					"provider_payment_id": self.provider_payment_id,
					"docstatus": 1,
					"name": ["!=", self.name],
				},
			)
			if duplicate:
				frappe.throw(_("Provider payment has already been posted."))

	def before_submit(self):
		if self.collection_type == "Offline" and not self.approved_on:
			frappe.throw(_("Approved On is required before posting offline payments."))
		if not self.payment_entry:
			frappe.throw(_("Payment Entry is required before posting a fee payment."))

		payment = frappe.get_doc("Payment Entry", self.payment_entry)
		if payment.docstatus != 1:
			frappe.throw(_("Payment Entry must be submitted."))
		if flt(payment.paid_amount, 2) != flt(self.amount, 2):
			frappe.throw(_("Payment Entry amount must match the fee payment amount."))

		self.status = "Posted"
		if not self.receipt_no:
			self.receipt_no = f"FEE-REC-{self.name}"
		self.outstanding_amount = flt(
			frappe.db.get_value("Sales Invoice", self.sales_invoice, "outstanding_amount"), 2
		)
