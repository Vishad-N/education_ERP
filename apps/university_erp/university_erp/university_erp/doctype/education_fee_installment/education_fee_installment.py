import frappe
from frappe import _
from frappe.model.document import Document


class EducationFeeInstallment(Document):
	def validate(self):
		if self.installment_number < 1:
			frappe.throw(_("Installment Number must be positive."))
		if self.amount <= 0:
			frappe.throw(_("Installment Amount must be positive."))
		if self.percentage <= 0 or self.percentage > 100:
			frappe.throw(_("Installment Percentage must be between 0 and 100."))
