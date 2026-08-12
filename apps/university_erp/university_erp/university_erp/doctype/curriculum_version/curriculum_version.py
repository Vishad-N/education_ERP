import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class CurriculumVersion(Document):
	def validate(self):
		seen = set()
		total = 0
		for row in self.curriculum_courses:
			if row.course in seen:
				frappe.throw(_("Course {0} is duplicated in this curriculum.").format(row.course))
			seen.add(row.course)
			if cint(row.credits) < 0:
				frappe.throw(_("Credits cannot be negative."))
			total += cint(row.credits)
		if cint(self.total_credits) != total:
			self.total_credits = total

	def before_submit(self):
		self.status = "Published"

	def on_cancel(self):
		self.status = "Cancelled"
