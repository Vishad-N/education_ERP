import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionConfirmation(Document):
	def validate(self):
		offer = frappe.get_doc("Seat Offer", self.seat_offer)
		if offer.status != "Accepted" or offer.docstatus != 1:
			frappe.throw(_("Admission confirmation requires a submitted accepted seat offer."))
		self.student_applicant = offer.student_applicant
		if self.status == "Confirmed":
			if not self.document_gate_passed:
				frappe.throw(_("Document gate must pass before admission confirmation."))
			if not self.fee_gate_passed:
				frappe.throw(_("Fee gate must pass before admission confirmation."))
			if not self.confirmed_on:
				frappe.throw(_("Confirmed On is required."))

	def before_submit(self):
		if not self.document_gate_passed:
			frappe.throw(_("Document gate must pass before admission confirmation."))
		if not self.fee_gate_passed:
			frappe.throw(_("Fee gate must pass before admission confirmation."))
		if not self.confirmed_on:
			frappe.throw(_("Confirmed On is required."))
		self.status = "Confirmed"
