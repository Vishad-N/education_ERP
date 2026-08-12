from frappe.model.document import Document


class DocumentRejectionReason(Document):
	def autoname(self):
		self.name = self.reason_code

	def validate(self):
		self.reason_code = (self.reason_code or "").strip().upper()
