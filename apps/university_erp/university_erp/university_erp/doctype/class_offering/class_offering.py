import frappe
from frappe import _
from frappe.model.document import Document


class ClassOffering(Document):
	def autoname(self):
		self.name = self.class_code

	def validate(self):
		self.class_code = (self.class_code or "").strip().upper()
		if self.program_offering:
			offering = frappe.get_cached_doc("Program Offering", self.program_offering)
			if offering.status not in ("Open", "Locked"):
				frappe.throw(_("Program Offering must be Open or Locked before classes can be configured."))

