import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class FacultyAssignment(Document):
	def autoname(self):
		self.name = self.assignment_code

	def validate(self):
		self.assignment_code = (self.assignment_code or "").strip().upper()
		if self.effective_from and self.effective_to:
			if getdate(self.effective_from) > getdate(self.effective_to):
				frappe.throw(_("Effective To cannot be before Effective From."))
		if self.subject_offering:
			status = frappe.db.get_value("Subject Offering", self.subject_offering, "status")
			if status not in ("Open", "Locked"):
				frappe.throw(_("Subject Offering must be Open or Locked."))
