import frappe
from frappe import _
from frappe.model.document import Document


class StudentPrivacyExportRequest(Document):
	def validate(self):
		if not self.reason:
			frappe.throw(_("Reason is required for privacy export requests."))
		if not self.masked_export:
			frappe.throw(_("Privacy exports must be masked for the Phase 3.2 baseline."))

	def before_submit(self):
		self.status = "Approved"
