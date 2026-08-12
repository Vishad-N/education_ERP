import frappe
from frappe import _
from frappe.model.document import Document


class StudentGuardianRelationship(Document):
	def validate(self):
		if not self.student and not self.student_applicant:
			frappe.throw(_("Either Student or Student Applicant is required."))
		if self.student and self.student_applicant:
			frappe.throw(_("Link either Student or Student Applicant, not both."))
		if self.is_primary_guardian and self.status == "Active":
			self._validate_single_primary_guardian()

	def _validate_single_primary_guardian(self):
		filters = {
			"name": ["!=", self.name],
			"is_primary_guardian": 1,
			"status": "Active",
		}
		if self.student:
			filters["student"] = self.student
		else:
			filters["student_applicant"] = self.student_applicant
		if frappe.db.exists("Student Guardian Relationship", filters):
			frappe.throw(_("Only one active primary guardian is allowed."))
