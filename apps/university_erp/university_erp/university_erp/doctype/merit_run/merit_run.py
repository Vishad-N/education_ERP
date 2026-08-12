import frappe
from frappe import _
from frappe.model.document import Document


class MeritRun(Document):
	def validate(self):
		if self.status == "Published" and not self.published_on:
			frappe.throw(_("Published On is required for published merit runs."))

	def before_submit(self):
		self.status = "Published"

	def before_cancel(self):
		frappe.throw(_("Published merit runs are immutable and cannot be cancelled."))
