frappe.ui.form.on("CRM Lead", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Create Application"), () => {
			university_erp.run({
				frm,
				method: "university_erp.api.admissions.start_application_from_lead",
				args: { lead: frm.doc.name },
				freeze: __("Creating application..."),
				callback(r) {
					frappe.set_route("Form", "Student Applicant", r.message.student_applicant);
				},
			});
		}).addClass("btn-primary");
	},
});
