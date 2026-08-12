import frappe
from frappe import _
from frappe.model.document import Document


class DocumentRequirementMatrix(Document):
	def autoname(self):
		self.name = self.requirement_code

	def validate(self):
		self.requirement_code = (self.requirement_code or "").strip().upper()
		if not self.student_category and not self.program:
			frappe.throw(_("At least Student Category or Program is required for a document requirement."))
