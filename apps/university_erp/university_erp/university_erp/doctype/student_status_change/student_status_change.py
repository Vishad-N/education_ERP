import frappe
from frappe import _
from frappe.model.document import Document


class StudentStatusChange(Document):
	def validate(self):
		if self.from_status == self.to_status:
			frappe.throw(_("From Status and To Status must be different."))
