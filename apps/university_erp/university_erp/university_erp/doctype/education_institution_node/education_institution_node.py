import frappe
from frappe import _
from frappe.utils import getdate
from frappe.utils.nestedset import NestedSet


NODE_ORDER = {
	"University": 1,
	"Campus": 2,
	"College": 3,
	"Department": 4,
}


class EducationInstitutionNode(NestedSet):
	nsm_parent_field = "parent_education_institution_node"

	def autoname(self):
		self.name = self.institution_code

	def validate(self):
		self.institution_code = (self.institution_code or "").strip().upper()
		self.validate_dates()
		self.validate_parent_node()

	def validate_dates(self):
		if self.inactive_from and self.active_from and getdate(self.inactive_from) < getdate(self.active_from):
			frappe.throw(_("Inactive From cannot be before Active From."))

	def validate_parent_node(self):
		if not self.parent_education_institution_node:
			if self.node_type != "University":
				frappe.throw(_("Only University nodes may be created without a parent."))
			return

		parent = frappe.get_cached_doc("Education Institution Node", self.parent_education_institution_node)
		if not parent.is_group:
			frappe.throw(_("Parent institution node must be a group node."))
		if NODE_ORDER[self.node_type] <= NODE_ORDER[parent.node_type]:
			frappe.throw(_("Child institution node type must be below its parent type."))

