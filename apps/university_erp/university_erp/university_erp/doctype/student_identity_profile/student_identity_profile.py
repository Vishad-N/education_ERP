import frappe
from frappe import _
from frappe.model.document import Document


class StudentIdentityProfile(Document):
	def validate(self):
		if not self.student and not self.student_applicant:
			frappe.throw(_("Either Student or Student Applicant is required."))
		if self.student and self.student_applicant:
			frappe.throw(_("Link either Student or Student Applicant, not both."))
		self.normalized_full_name = " ".join((self.full_name or "").upper().split())
		self.primary_mobile = (self.primary_mobile or "").strip()
		self.primary_email = (self.primary_email or "").strip().lower()
