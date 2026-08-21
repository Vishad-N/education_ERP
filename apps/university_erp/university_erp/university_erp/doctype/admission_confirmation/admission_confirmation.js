frappe.ui.form.on("Admission Confirmation", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Confirm Admission"), () => {
				university_erp.run({
					frm,
					method: "university_erp.api.admissions.confirm_admission",
					args: { name: frm.doc.name },
					freeze: __("Confirming admission..."),
					callback() {
						frappe.show_alert({ message: __("Admission confirmed"), indicator: "green" });
						frm.reload_doc();
					},
				});
			}).addClass("btn-primary");
		}
		if (frm.doc.docstatus === 1 && frm.doc.status === "Confirmed") {
			frm.add_custom_button(__("Create Student"), () => {
				university_erp.run({
					method: "university_erp.api.admissions.create_student",
					args: { admission_confirmation: frm.doc.name },
					freeze: __("Creating student..."),
					callback(r) {
						frappe.msgprint({
							title: __("Student created"),
							message: __("Student {0}. Portal: {1}", [r.message.student, r.message.portal_url || ""]),
							indicator: "green",
						});
						frappe.set_route("Form", "Student", r.message.student);
					},
				});
			}).addClass("btn-primary");
		}
	},
});
