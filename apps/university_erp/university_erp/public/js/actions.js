frappe.provide("university_erp");

university_erp.run = function (opts) {
	const execute = () =>
		frappe.call({
			method: opts.method,
			args: opts.args || {},
			freeze: true,
			freeze_message: opts.freeze || __("Working..."),
			callback(r) {
				if (opts.callback) opts.callback(r);
			},
			error() {
				frappe.msgprint({
					title: __("Action failed"),
					message: __("Check required fields and try again."),
					indicator: "red",
				});
			},
		});
	if (opts.frm && (opts.frm.is_new() || opts.frm.is_dirty())) {
		opts.frm.save().then(execute);
		return;
	}
	execute();
};
