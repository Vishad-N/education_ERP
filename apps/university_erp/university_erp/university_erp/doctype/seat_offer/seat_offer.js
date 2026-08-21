frappe.ui.form.on("Seat Offer", {
	refresh(frm) {
		if (frm.doc.status !== "Accepted" && frm.doc.docstatus < 2) {
			frm.add_custom_button(__("Accept Seat"), () => {
				university_erp.run({
					frm,
					method: "university_erp.api.admissions.accept_seat",
					args: { name: frm.doc.name },
					freeze: __("Accepting seat..."),
					callback(r) {
						frappe.show_alert({ message: __("Seat {0}", [r.message.status]), indicator: "green" });
						frm.reload_doc();
					},
				});
			}).addClass("btn-primary");
		}
		if (frm.doc.status === "Accepted" && frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Confirm Admission"), () => {
				university_erp.run({
					method: "university_erp.api.admissions.confirm_admission",
					args: { seat_offer: frm.doc.name },
					freeze: __("Confirming admission..."),
					callback(r) {
						frappe.set_route("Form", "Admission Confirmation", r.message.confirmation);
					},
				});
			}).addClass("btn-primary");
		}
	},
});
