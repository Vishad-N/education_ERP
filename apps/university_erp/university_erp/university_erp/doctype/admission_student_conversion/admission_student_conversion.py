import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionStudentConversion(Document):
	def validate(self):
		confirmation = frappe.get_doc("Admission Confirmation", self.admission_confirmation)
		if confirmation.status != "Confirmed" or confirmation.docstatus != 1:
			frappe.throw(_("Student conversion requires a submitted confirmed admission."))
		self.student_applicant = confirmation.student_applicant
		if frappe.db.exists(
			"Admission Student Conversion",
			{
				"student_applicant": self.student_applicant,
				"name": ["!=", self.name],
				"docstatus": ["<", 2],
			},
		):
			frappe.throw(_("This Student Applicant already has an active conversion."))

	def before_submit(self):
		confirmation = frappe.get_doc("Admission Confirmation", self.admission_confirmation)
		offer = frappe.get_doc("Seat Offer", confirmation.seat_offer)
		round_doc = frappe.get_doc("Seat Allocation Round", offer.allocation_round)
		merit_run = frappe.get_doc("Merit Run", round_doc.merit_run)
		applicant = frappe.get_doc("Student Applicant", self.student_applicant)

		self.student = self._create_or_get_student(applicant)
		self.program_enrollment = self._create_or_get_program_enrollment(applicant, merit_run)
		identity_profile = self._create_or_get_identity_profile(applicant)
		self.identity_issuance = self._create_or_get_identity_issuance(identity_profile, applicant)
		frappe.db.set_value("Student Applicant", applicant.name, "application_status", "Admitted")
		self.status = "Converted"

	def _create_or_get_student(self, applicant):
		if existing := frappe.db.exists("Student", {"student_applicant": applicant.name}):
			return existing
		if existing := frappe.db.exists("Student", {"student_email_id": applicant.student_email_id}):
			return existing
		student = frappe.get_doc(
			{
				"doctype": "Student",
				"naming_series": "EDU-STU-.YYYY.-",
				"first_name": applicant.first_name,
				"middle_name": applicant.middle_name,
				"last_name": applicant.last_name,
				"student_applicant": applicant.name,
				"student_email_id": applicant.student_email_id,
				"student_mobile_number": applicant.student_mobile_number,
				"date_of_birth": applicant.date_of_birth,
				"joining_date": self.conversion_date,
			}
		)
		student.insert(ignore_permissions=True)
		return student.name

	def _create_or_get_program_enrollment(self, applicant, merit_run):
		filters = {
			"student": self.student,
			"program": merit_run.program,
			"academic_year": merit_run.academic_year,
		}
		if existing := frappe.db.exists("Program Enrollment", filters):
			return existing
		enrollment = frappe.get_doc(
			{
				"doctype": "Program Enrollment",
				"student": self.student,
				"program": merit_run.program,
				"academic_year": merit_run.academic_year,
				"academic_term": applicant.academic_term,
				"student_category": applicant.student_category,
				"enrollment_date": self.conversion_date,
			}
		)
		enrollment.insert(ignore_permissions=True)
		enrollment.submit()
		return enrollment.name

	def _create_or_get_identity_profile(self, applicant):
		if existing := frappe.db.exists("Student Identity Profile", {"student": self.student}):
			return existing
		if existing := frappe.db.exists("Student Identity Profile", {"student_applicant": applicant.name}):
			profile = frappe.get_doc("Student Identity Profile", existing)
			profile.student = self.student
			profile.student_applicant = None
			profile.save(ignore_permissions=True)
			return profile.name
		profile = frappe.get_doc(
			{
				"doctype": "Student Identity Profile",
				"student": self.student,
				"full_name": " ".join(
					filter(None, [applicant.first_name, applicant.middle_name, applicant.last_name])
				),
				"date_of_birth": applicant.date_of_birth,
				"student_category": applicant.student_category,
				"primary_mobile": applicant.student_mobile_number,
				"primary_email": applicant.student_email_id,
				"status": "Active",
				"consent_recorded": 1,
			}
		)
		profile.insert(ignore_permissions=True)
		return profile.name

	def _create_or_get_identity_issuance(self, identity_profile, applicant):
		if existing := frappe.db.exists("Student Identity Issuance", {"student": self.student}):
			return existing
		issuance = frappe.get_doc(
			{
				"doctype": "Student Identity Issuance",
				"identity_profile": identity_profile,
				"student": self.student,
				"student_applicant": applicant.name,
				"student_number": f"P43-STU-{applicant.name}",
				"enrollment_number": f"P43-ENR-{applicant.name}",
				"issued_on": self.conversion_date,
				"status": "Draft",
				"notes": "Synthetic P4.3 conversion identity issuance",
			}
		)
		issuance.insert(ignore_permissions=True)
		issuance.submit()
		return issuance.name
