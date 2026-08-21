frappe.ui.form.on("Admission Application Draft", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Submitted") return;
		frm.add_custom_button(__("Create Application"), () => {
			university_erp.run({
				method: "university_erp.api.admissions.create_application_from_draft",
				args: { draft: frm.doc.name },
				freeze: __("Creating application..."),
				callback(r) {
					frappe.set_route("Form", "Student Applicant", r.message.student_applicant);
				},
			});
		}).addClass("btn-primary");
	},
});
