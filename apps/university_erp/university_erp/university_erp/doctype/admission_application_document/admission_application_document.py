import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionApplicationDocument(Document):
	def validate(self):
		if self.scan_status == "Scan Failed" and not self.scan_failure_reason:
			frappe.throw(_("Scan failure reason is required."))

