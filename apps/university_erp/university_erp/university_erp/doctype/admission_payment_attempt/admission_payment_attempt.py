import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionPaymentAttempt(Document):
	def validate(self):
		if self.status == "Paid" and not self.provider_payment_id:
			frappe.throw(_("Provider payment ID is required for a paid attempt."))

