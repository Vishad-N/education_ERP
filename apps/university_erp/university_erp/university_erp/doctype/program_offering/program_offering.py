import frappe
from frappe import _
from frappe.model.document import Document


class ProgramOffering(Document):
	def autoname(self):
		self.name = self.offering_code

	def validate(self):
		self.offering_code = (self.offering_code or "").strip().upper()
		if self.program_version:
			version = frappe.get_cached_doc("Program Version", self.program_version)
			if version.status != "Published":
				frappe.throw(_("Program Version must be published before it can be offered."))
			self.program = version.program
		if self.institution_node:
			node = frappe.get_cached_doc("Education Institution Node", self.institution_node)
			if node.status != "Active":
				frappe.throw(_("Program Offering institution node must be Active."))

