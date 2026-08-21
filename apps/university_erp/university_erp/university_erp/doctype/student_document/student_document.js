frappe.ui.form.on("Student Document", {
	refresh(frm) {
		if (frm.is_new()) return;
		if (frm.doc.verification_status === "Pending Verification") {
			frm.add_custom_button(__("Verify"), () => {
				university_erp.run({
					method: "university_erp.api.admissions.verify_document",
					args: { student_document: frm.doc.name, result: "Verified" },
					freeze: __("Verifying..."),
					callback() {
						frappe.show_alert({ message: __("Verified"), indicator: "green" });
						frm.reload_doc();
					},
				});
			}).addClass("btn-primary");
		}
	},
});
