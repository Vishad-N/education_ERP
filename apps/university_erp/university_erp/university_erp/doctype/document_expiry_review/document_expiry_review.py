import frappe
from frappe import _
from frappe.model.document import Document


class DocumentExpiryReview(Document):
	def validate(self):
		if not self.expiry_date:
			frappe.throw(_("Expiry Date is required."))

	def before_submit(self):
		document = frappe.get_doc("Student Document", self.student_document)
		document.expiry_date = self.expiry_date
		document.verification_status = "Expired"
		document.save(ignore_permissions=True)
		self.status = "Expired"
