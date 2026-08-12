import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class AcademicSessionPolicy(Document):
	def validate(self):
		if self.admission_open_date and self.admission_close_date:
			if getdate(self.admission_open_date) > getdate(self.admission_close_date):
				frappe.throw(_("Admission Close Date cannot be before Admission Open Date."))
		if self.status == "Locked" and not self.published_on:
			frappe.throw(_("Only a published session policy can be locked."))

	def before_submit(self):
		self.status = "Published"
		self.published_on = self.published_on or frappe.utils.nowdate()

	def on_cancel(self):
		self.status = "Cancelled"
