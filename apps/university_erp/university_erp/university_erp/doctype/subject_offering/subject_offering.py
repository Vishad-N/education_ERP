import frappe
from frappe import _
from frappe.model.document import Document


class SubjectOffering(Document):
	def autoname(self):
		self.name = self.subject_offering_code

	def validate(self):
		self.subject_offering_code = (self.subject_offering_code or "").strip().upper()
		if self.class_offering:
			class_status = frappe.db.get_value("Class Offering", self.class_offering, "status")
			if class_status not in ("Open", "Locked"):
				frappe.throw(_("Class Offering must be Open or Locked."))
