import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class StudentFeeDemand(Document):
	def validate(self):
		if self.gross_amount < 0:
			frappe.throw(_("Gross Amount cannot be negative."))
		expected = flt(self.gross_amount) - flt(self.concession_amount) - flt(self.scholarship_amount)
		expected += flt(self.fine_amount) - flt(self.waiver_amount)
		if expected < 0:
			frappe.throw(_("Net Amount cannot be negative."))
		if flt(self.net_amount, 2) != flt(expected, 2):
			frappe.throw(_("Net Amount must reconcile to demand components."))
		if self.status == "Generated" and not self.sales_invoice:
			mode = str(frappe.conf.get("application_fee_mode") or "waived").strip().lower()
			if mode == "gateway":
				frappe.throw(_("Sales Invoice is required for generated fee demands."))

	def before_submit(self):
		if not self.sales_invoice:
			mode = str(frappe.conf.get("application_fee_mode") or "waived").strip().lower()
			if mode == "gateway":
				frappe.throw(_("Sales Invoice is required before submitting a fee demand."))
			self.status = "Generated"
			return
		invoice = frappe.get_doc("Sales Invoice", self.sales_invoice)
		if invoice.docstatus != 1:
			frappe.throw(_("Linked Sales Invoice must be submitted."))
		if flt(invoice.grand_total, 2) != flt(self.net_amount, 2):
			frappe.throw(_("Sales Invoice total must equal the demand net amount."))
		self.status = "Generated"
