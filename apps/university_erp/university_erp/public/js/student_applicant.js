frappe.ui.form.on("Student Applicant", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Evaluate Eligibility"), () => {
			university_erp.run({
				method: "university_erp.api.admissions.evaluate_eligibility",
				args: { student_applicant: frm.doc.name },
				freeze: __("Evaluating..."),
				callback(r) {
					frappe.show_alert({ message: __("Result: {0}", [r.message.result]), indicator: "green" });
				},
			});
		});
		frm.add_custom_button(__("Admit Student"), () => {
			university_erp.run({
				method: "university_erp.api.admissions.admit_applicant",
				args: { student_applicant: frm.doc.name },
				freeze: __("Running admission to student..."),
				callback(r) {
					const data = r.message || {};
					frappe.msgprint({
						title: __("Student created"),
						message: __("Student {0}. Portal: {1}", [data.student, data.portal_url || ""]),
						indicator: "green",
					});
					if (data.student) frappe.set_route("Form", "Student", data.student);
				},
			});
		}).addClass("btn-primary");
	},
});
