import frappe
from frappe import _
from frappe.model.document import Document


class DocumentReplacementRequest(Document):
	def validate(self):
		if self.old_document == self.new_document:
			frappe.throw(_("Old Document and New Document must be different."))

	def before_submit(self):
		old_document = frappe.get_doc("Student Document", self.old_document)
		new_document = frappe.get_doc("Student Document", self.new_document)
		old_document.verification_status = "Replaced"
		new_document.verification_status = "Pending Verification"
		old_document.save(ignore_permissions=True)
		new_document.save(ignore_permissions=True)
		self.status = "Approved"
