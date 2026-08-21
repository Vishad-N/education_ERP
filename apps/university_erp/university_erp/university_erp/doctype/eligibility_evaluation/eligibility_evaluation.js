frappe.ui.form.on("Eligibility Evaluation", {
	refresh(frm) {
		if (!frm.doc.student_applicant) return;
		frm.add_custom_button(__("Evaluate"), () => {
			university_erp.run({
				frm,
				method: "university_erp.api.admissions.evaluate_eligibility",
				args: { student_applicant: frm.doc.student_applicant, score: frm.doc.score },
				freeze: __("Evaluating..."),
				callback(r) {
					frappe.show_alert({ message: __("Result: {0}", [r.message.result]), indicator: "green" });
					frm.reload_doc();
				},
			});
		}).addClass("btn-primary");
	},
});
