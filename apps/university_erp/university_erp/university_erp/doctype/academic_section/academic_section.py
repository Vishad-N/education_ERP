import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class AcademicSection(Document):
	def autoname(self):
		self.name = self.section_code

	def validate(self):
		self.section_code = (self.section_code or "").strip().upper()
		if cint(self.capacity) < 0:
			frappe.throw(_("Capacity cannot be negative."))

