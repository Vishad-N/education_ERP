frappe.ui.form.on("Student Fee Demand", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Record Counter Payment"), () => {
			university_erp.run({
				frm,
				method: "university_erp.api.admissions.record_counter_payment",
				args: { student_fee_demand: frm.doc.name },
				freeze: __("Recording payment..."),
				callback(r) {
					frappe.msgprint({
						title: __("Receipt"),
						message: r.message.receipt_no || r.message.payment,
						indicator: "green",
					});
					frm.reload_doc();
				},
			});
		}).addClass("btn-primary");
	},
});
