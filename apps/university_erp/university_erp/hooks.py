app_name = "university_erp"
app_title = "University ERP"
app_publisher = "University ERP Engineering"
app_description = "Custom Education ERP application for Frappe v16."
app_email = "engineering@example.invalid"
app_license = "mit"

required_apps = ["frappe", "erpnext", "education", "crm", "payments"]

app_include_js = ["/assets/university_erp/js/actions.js"]

doctype_js = {
	"CRM Lead": "public/js/crm_lead.js",
	"Student Applicant": "public/js/student_applicant.js",
	"Student": "public/js/student.js",
}
