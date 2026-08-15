"""Unauthenticated platform health probes with no sensitive payloads."""

import frappe


@frappe.whitelist(allow_guest=True)
def live():
	return {"status": "ok"}


@frappe.whitelist(allow_guest=True)
def ready():
	frappe.db.sql("select 1")
	frappe.cache.set_value("university_erp_readiness", "ok", expires_in_sec=30)
	if frappe.cache.get_value("university_erp_readiness") not in ("ok", b"ok"):
		frappe.throw("Cache readiness check failed")
	return {"status": "ready"}
