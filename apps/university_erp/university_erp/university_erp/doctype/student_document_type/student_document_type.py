from frappe.model.document import Document


class StudentDocumentType(Document):
	def autoname(self):
		self.name = self.document_type_code

	def validate(self):
		self.document_type_code = (self.document_type_code or "").strip().upper()
