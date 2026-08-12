import frappe
from frappe import _
from frappe.model.document import Document


class StudentCorrectionRequest(Document):
	def validate(self):
		if self.current_value == self.requested_value:
			frappe.throw(_("Requested Value must be different from Current Value."))

	def before_submit(self):
		self.status = "Approved"

	def on_cancel(self):
		self.status = "Cancelled"
