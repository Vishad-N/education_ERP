import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class DuplicateCandidate(Document):
	def validate(self):
		if self.source_identity_profile == self.candidate_identity_profile:
			frappe.throw(_("Source and Candidate profiles must be different."))
		if flt(self.match_score) < 0 or flt(self.match_score) > 100:
			frappe.throw(_("Match Score must be between 0 and 100."))
