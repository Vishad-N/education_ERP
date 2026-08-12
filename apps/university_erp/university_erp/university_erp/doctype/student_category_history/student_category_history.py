import frappe
from frappe import _
from frappe.model.document import Document


class StudentCategoryHistory(Document):
	def validate(self):
		if self.from_category and self.from_category == self.to_category:
			frappe.throw(_("From Category and To Category must be different."))
