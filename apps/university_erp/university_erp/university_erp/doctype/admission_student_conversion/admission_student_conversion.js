frappe.ui.form.on("Admission Student Conversion", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Create Student"), () => {
				university_erp.run({
					frm,
					method: "university_erp.api.admissions.create_student",
					args: { name: frm.doc.name },
					freeze: __("Creating student..."),
					callback(r) {
						frappe.msgprint({
							title: __("Student created"),
							message: __("Student {0}. Portal: {1}", [r.message.student, r.message.portal_url || ""]),
							indicator: "green",
						});
						frm.reload_doc();
					},
				});
			}).addClass("btn-primary");
		}
	},
});
