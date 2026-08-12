import frappe
from frappe import _
from frappe.model.document import Document


class AcademicCalendar(Document):
	def autoname(self):
		self.name = self.calendar_code

	def validate(self):
		self.calendar_code = (self.calendar_code or "").strip().upper()
		seen = set()
		for row in self.calendar_days:
			if row.calendar_date in seen:
				frappe.throw(_("Calendar Date {0} is duplicated.").format(row.calendar_date))
			seen.add(row.calendar_date)
		if self.status == "Locked" and not self.calendar_days:
			frappe.throw(_("A locked academic calendar must contain at least one day."))
