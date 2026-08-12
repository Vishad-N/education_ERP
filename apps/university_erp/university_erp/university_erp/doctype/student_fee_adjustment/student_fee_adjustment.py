import frappe
from frappe import _
from frappe.model.document import Document


class StudentFeeAdjustment(Document):
	def validate(self):
		if self.amount <= 0:
			frappe.throw(_("Adjustment Amount must be positive."))
		if self.status == "Approved" and not self.approved_on:
			frappe.throw(_("Approved On is required for approved adjustments."))
