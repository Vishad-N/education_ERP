import frappe
from frappe import _
from frappe.model.document import Document


class DocumentScanResult(Document):
	def validate(self):
		if self.scan_result == "Failed" and not self.failure_reason:
			frappe.throw(_("Failure Reason is required when scan result is Failed."))

	def before_submit(self):
		document = frappe.get_doc("Student Document", self.student_document)
		document.scan_status = "Scan Passed" if self.scan_result == "Passed" else "Scan Failed"
		if self.scan_result == "Failed":
			document.rejection_reason = self.failure_reason
		document.save(ignore_permissions=True)
