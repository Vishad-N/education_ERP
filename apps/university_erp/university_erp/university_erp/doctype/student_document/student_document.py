import frappe
from frappe import _
from frappe.model.document import Document


class StudentDocument(Document):
	def validate(self):
		if not self.student and not self.student_applicant:
			frappe.throw(_("Either Student or Student Applicant is required."))
		if self.student and self.student_applicant:
			frappe.throw(_("Link either Student or Student Applicant, not both."))
		if self.scan_status == "Scan Failed" and not self.rejection_reason:
			frappe.throw(_("Rejection Reason is required when Scan Status is Scan Failed."))
		if self.verification_status == "Verified" and self.scan_status != "Scan Passed":
			frappe.throw(_("Only scan-passed documents can be verified."))
