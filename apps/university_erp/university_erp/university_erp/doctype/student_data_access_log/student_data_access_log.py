import frappe
from frappe import _
from frappe.model.document import Document


class StudentDataAccessLog(Document):
	def validate(self):
		if not self.purpose:
			frappe.throw(_("Purpose is required for student data access."))
		if self.access_type == "Export" and not self.masked_output:
			frappe.throw(_("Student exports must be masked unless a separate approved exception exists."))
