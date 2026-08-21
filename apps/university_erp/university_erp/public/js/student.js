frappe.ui.form.on("Student", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Issue Portal Link"), () => {
			university_erp.run({
				method: "university_erp.api.admissions.issue_portal_access",
				args: { student: frm.doc.name },
				freeze: __("Issuing portal link..."),
				callback(r) {
					frappe.msgprint({
						title: __("Portal link"),
						message: r.message.portal_url,
						indicator: "green",
					});
				},
			});
		});
	},
});
