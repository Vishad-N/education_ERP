frappe.ui.form.on("Merit Run", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Publish Merit"), () => {
				university_erp.run({
					frm,
					method: "university_erp.api.admissions.publish_merit",
					args: { program: frm.doc.program, academic_year: frm.doc.academic_year },
					freeze: __("Publishing merit..."),
					callback(r) {
						frappe.set_route("Form", "Merit Run", r.message.merit_run);
					},
				});
			}).addClass("btn-primary");
		}
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Allocate Seats"), () => {
				university_erp.run({
					method: "university_erp.api.admissions.allocate_seats",
					args: { merit_run: frm.doc.name },
					freeze: __("Allocating seats..."),
					callback(r) {
						frappe.show_alert({
							message: __("{0} offers created", [(r.message.offers || []).length]),
							indicator: "green",
						});
					},
				});
			}).addClass("btn-primary");
		}
	},
});
