import frappe
from frappe import _
from frappe.model.document import Document


class SeatAllocationRound(Document):
	def validate(self):
		if self.round_number < 1:
			frappe.throw(_("Round Number must be positive."))
		if self.status == "Published" and not self.published_on:
			frappe.throw(_("Published On is required for published rounds."))

	def before_submit(self):
		self.status = "Published"
