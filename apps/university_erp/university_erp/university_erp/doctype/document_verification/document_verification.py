import frappe
from frappe import _
from frappe.model.document import Document


class DocumentVerification(Document):
	def validate(self):
		if self.result == "Rejected" and not self.rejection_reason:
			frappe.throw(_("Rejection Reason is required when result is Rejected."))

	def before_submit(self):
		document = frappe.get_doc("Student Document", self.student_document)
		document.verification_status = self.result
		if self.result == "Rejected":
			document.rejection_reason = self.rejection_reason
		document.save(ignore_permissions=True)
