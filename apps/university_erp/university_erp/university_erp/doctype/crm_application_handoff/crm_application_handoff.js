frappe.ui.form.on("CRM Application Handoff", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Create Application"), () => {
				university_erp.run({
					frm,
					method: "university_erp.api.admissions.create_application",
					args: { name: frm.doc.name },
					freeze: __("Creating student applicant..."),
					callback(r) {
						frappe.show_alert({
							message: __("Applicant {0} created", [r.message.student_applicant]),
							indicator: "green",
						});
						frm.reload_doc();
					},
				});
			}).addClass("btn-primary");
		}
	},
});
