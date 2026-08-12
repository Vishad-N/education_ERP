import frappe
from frappe import _
from frappe.model.document import Document


class EducationFeeCode(Document):
	def validate(self):
		if self.default_amount < 0:
			frappe.throw(_("Default Amount cannot be negative."))
		if self.status == "Active" and not self.fee_category:
			frappe.throw(_("Fee Category is required for active fee codes."))
