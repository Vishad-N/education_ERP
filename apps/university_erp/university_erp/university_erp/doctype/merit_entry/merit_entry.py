import frappe
from frappe import _
from frappe.model.document import Document


class MeritEntry(Document):
	def validate(self):
		if self.rank < 1:
			frappe.throw(_("Rank must be positive."))
		if self.score < 0:
			frappe.throw(_("Score cannot be negative."))
		run_status = frappe.db.get_value("Merit Run", self.merit_run, "status")
		if run_status not in {"Draft", "Published"}:
			frappe.throw(_("Merit entries require a draft or published merit run."))
		if frappe.db.exists(
			"Merit Entry",
			{"merit_run": self.merit_run, "rank": self.rank, "name": ["!=", self.name]},
		):
			frappe.throw(_("Rank must be unique within a merit run."))
		if frappe.db.exists(
			"Merit Entry",
			{"merit_run": self.merit_run, "student_applicant": self.student_applicant, "name": ["!=", self.name]},
		):
			frappe.throw(_("Student Applicant must be unique within a merit run."))
