import json

import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionApplicationDraft(Document):
	def validate(self):
		if not self.crm_lead and not self.student_applicant:
			frappe.throw(_("Either CRM Lead or Student Applicant is required."))
		try:
			payload = json.loads(self.draft_payload)
		except Exception:
			frappe.throw(_("Draft Payload must be valid JSON."))
		if not isinstance(payload, dict):
			frappe.throw(_("Draft Payload must be a JSON object."))
		if self.status == "Submitted" and not self.student_applicant:
			frappe.throw(_("Student Applicant is required before draft submission."))
