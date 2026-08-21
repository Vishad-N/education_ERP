frappe.ui.form.on("Seat Allocation Round", {
	refresh(frm) {
		if (frm.doc.merit_run) {
			frm.add_custom_button(__("Allocate Seats"), () => {
				university_erp.run({
					frm,
					method: "university_erp.api.admissions.allocate_seats",
					args: { merit_run: frm.doc.merit_run },
					freeze: __("Allocating seats..."),
					callback(r) {
						frappe.show_alert({
							message: __("{0} offers created", [(r.message.offers || []).length]),
							indicator: "green",
						});
						frm.reload_doc();
					},
				});
			}).addClass("btn-primary");
		}
	},
});
