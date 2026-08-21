import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class CRMApplicationHandoff(Document):
	def validate(self):
		if frappe.db.exists(
			"CRM Application Handoff",
			{"crm_lead": self.crm_lead, "name": ["!=", self.name], "docstatus": ["<", 2]},
		):
			frappe.throw(_("This CRM Lead already has an active application handoff."))
		if (
			self.docstatus == 1
			and self.status == "Application Created"
			and not self.student_applicant
		):
			frappe.throw(_("Student Applicant is required once the handoff creates an application."))

	def before_submit(self):
		if not self.student_applicant:
			self.student_applicant = self._create_or_get_student_applicant()
		self._mark_lead_converted()
		self._submit_application_draft()
		self.status = "Application Created"

	def _mark_lead_converted(self):
		frappe.db.set_value("CRM Lead", self.crm_lead, "converted", 1)

	def _submit_application_draft(self):
		if not self.application_draft:
			return
		draft = frappe.get_doc("Admission Application Draft", self.application_draft)
		draft.student_applicant = self.student_applicant
		draft.status = "Submitted"
		draft.submitted_on = now_datetime()
		draft.save(ignore_permissions=True)

	def _create_or_get_student_applicant(self):
		lead = frappe.get_doc("CRM Lead", self.crm_lead)
		email = lead.email or f"{self.crm_lead.lower()}@example.invalid"
		if existing := frappe.db.exists("Student Applicant", {"student_email_id": email}):
			return existing
		applicant = frappe.get_doc(
			{
				"doctype": "Student Applicant",
				"naming_series": "EDU-APP-.YYYY.-",
				"first_name": lead.first_name,
				"last_name": lead.last_name,
				"student_email_id": email,
				"student_mobile_number": lead.mobile_no,
				"program": self.program,
				"academic_year": self.academic_year,
				"academic_term": self.academic_term,
				"application_date": self.handoff_date,
			}
		)
		applicant.insert(ignore_permissions=True)
		return applicant.name
