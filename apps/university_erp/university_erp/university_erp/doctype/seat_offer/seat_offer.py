import frappe
from frappe import _
from frappe.model.document import Document


class SeatOffer(Document):
	def validate(self):
		if self.status == "Accepted" and not self.accepted_on:
			frappe.throw(_("Accepted On is required for accepted offers."))
		if frappe.db.exists(
			"Seat Offer",
			{
				"student_applicant": self.student_applicant,
				"allocation_round": self.allocation_round,
				"name": ["!=", self.name],
				"docstatus": ["<", 2],
			},
		):
			frappe.throw(_("Student Applicant already has an offer in this allocation round."))
		round_status = frappe.db.get_value("Seat Allocation Round", self.allocation_round, "status")
		if round_status != "Published":
			frappe.throw(_("Seat offers require a published allocation round."))

	def before_submit(self):
		if self.status == "Accepted":
			self._validate_capacity_available()

	def _validate_capacity_available(self):
		frappe.db.sql(
			"select name from `tabAdmission Seat Matrix` where name = %s for update",
			self.seat_matrix,
		)
		capacity = frappe.db.get_value("Admission Seat Matrix", self.seat_matrix, "capacity")
		accepted_count = frappe.db.count(
			"Seat Offer",
			{
				"seat_matrix": self.seat_matrix,
				"status": "Accepted",
				"docstatus": 1,
				"name": ["!=", self.name],
			},
		)
		if accepted_count >= capacity:
			frappe.throw(_("Seat capacity is already full for this matrix."))
