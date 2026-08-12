import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class PaymentProviderEvent(Document):
	def validate(self):
		if flt(self.amount) < 0:
			frappe.throw(_("Amount cannot be negative."))
		if self.status == "Processed" and self.event_type == "Payment Captured":
			if not self.provider_payment_id:
				frappe.throw(_("Provider Payment ID is required for captured payment events."))
			if not self.student_fee_payment or not self.payment_entry:
				frappe.throw(_("Processed payment events require a fee payment and payment entry."))
