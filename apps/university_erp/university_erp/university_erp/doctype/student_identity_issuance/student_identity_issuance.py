import frappe
from frappe import _
from frappe.model.document import Document


class StudentIdentityIssuance(Document):
	def validate(self):
		if self.student_number and frappe.db.exists(
			"Student Identity Issuance",
			{"student_number": self.student_number, "name": ["!=", self.name], "docstatus": ["<", 2]},
		):
			frappe.throw(_("Student Number must be unique."))
		if self.enrollment_number and frappe.db.exists(
			"Student Identity Issuance",
			{"enrollment_number": self.enrollment_number, "name": ["!=", self.name], "docstatus": ["<", 2]},
		):
			frappe.throw(_("Enrollment Number must be unique."))
		if not self.student and not self.student_applicant:
			frappe.throw(_("Either Student or Student Applicant is required."))

	def before_submit(self):
		self.status = "Issued"

	def before_cancel(self):
		if self.status == "Issued":
			frappe.throw(_("Issued identities are immutable and cannot be cancelled."))
