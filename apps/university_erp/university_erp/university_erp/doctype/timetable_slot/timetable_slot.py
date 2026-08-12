import frappe
from frappe import _
from frappe.model.document import Document


class TimetableSlot(Document):
	def autoname(self):
		self.name = self.slot_code

	def validate(self):
		self.slot_code = (self.slot_code or "").strip().upper()
		if self.start_time and self.end_time and self.start_time >= self.end_time:
			frappe.throw(_("End Time must be after Start Time."))
