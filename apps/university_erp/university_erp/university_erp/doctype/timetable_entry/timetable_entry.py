import frappe
from frappe import _
from frappe.model.document import Document


class TimetableEntry(Document):
	def autoname(self):
		self.name = self.entry_code

	def validate(self):
		self.entry_code = (self.entry_code or "").strip().upper()
		if self.subject_offering:
			status = frappe.db.get_value("Subject Offering", self.subject_offering, "status")
			if status not in ("Open", "Locked"):
				frappe.throw(_("Subject Offering must be Open or Locked."))
		self._validate_no_conflicts()

	def _validate_no_conflicts(self):
		if not self.timetable_slot:
			return
		filters = {"timetable_slot": self.timetable_slot, "name": ["!=", self.name], "status": ["!=", "Cancelled"]}
		if self.academic_section:
			self._throw_if_conflict({**filters, "academic_section": self.academic_section}, "section")
		if self.instructor:
			self._throw_if_conflict({**filters, "instructor": self.instructor}, "faculty")
		if self.room and frappe.db.exists("Timetable Entry", {**filters, "room": self.room}):
			frappe.throw(_("Timetable room conflict for {0}.").format(self.room))

	def _throw_if_conflict(self, filters, label):
		if frappe.db.exists("Timetable Entry", filters):
			frappe.throw(_("Timetable {0} conflict for slot {1}.").format(label, self.timetable_slot))
