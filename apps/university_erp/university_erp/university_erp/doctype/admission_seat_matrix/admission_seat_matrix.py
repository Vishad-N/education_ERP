import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionSeatMatrix(Document):
	def validate(self):
		if self.capacity < 0 or self.supernumerary_capacity < 0:
			frappe.throw(_("Seat capacity cannot be negative."))
		if self.status == "Locked" and not self.locked_on:
			frappe.throw(_("Locked On is required when seat matrix is locked."))
