import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class EducationFeePolicyVersion(Document):
	def validate(self):
		if self.status == "Published" and not self.effective_from:
			frappe.throw(_("Effective From is required for published fee policies."))
		expected = flt(self.base_amount) - flt(self.concession_amount) - flt(self.scholarship_amount)
		expected += flt(self.fine_amount) - flt(self.waiver_amount)
		if expected < 0:
			frappe.throw(_("Net Amount cannot be negative."))
		if flt(self.net_amount, 2) != flt(expected, 2):
			frappe.throw(_("Net Amount must equal base minus concessions/scholarships/waivers plus fines."))
