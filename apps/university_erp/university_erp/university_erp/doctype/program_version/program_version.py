import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class ProgramVersion(Document):
	def validate(self):
		if cint(self.minimum_credits) < 0 or cint(self.maximum_credits) < 0:
			frappe.throw(_("Credits cannot be negative."))
		if self.maximum_credits and self.minimum_credits and self.maximum_credits < self.minimum_credits:
			frappe.throw(_("Maximum Credits cannot be less than Minimum Credits."))

	def before_submit(self):
		self.status = "Published"

	def on_cancel(self):
		self.status = "Cancelled"

