import frappe
from frappe import _
from frappe.model.document import Document


class InstitutionStructureVersion(Document):
	def validate(self):
		if self.root_institution_node:
			root = frappe.get_cached_doc("Education Institution Node", self.root_institution_node)
			if root.parent_education_institution_node:
				frappe.throw(_("Root Institution Node must not have a parent."))

	def before_submit(self):
		self.status = "Published"

	def on_cancel(self):
		self.status = "Cancelled"
