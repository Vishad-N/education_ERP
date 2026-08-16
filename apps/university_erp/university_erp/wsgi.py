"""WSGI factory for single-site container runtimes.

Railway and ECS health probes do not send the public site Host header.
Frappe resolves the site from Host and does not honor serve_default_site
on HTTP requests, so the probe must pin SITE_NAME before the app loads.
"""

from __future__ import annotations

import os

import frappe.app as frappe_app


def pin_default_site(site_name: str | None = None) -> str | None:
	resolved = site_name if site_name is not None else os.environ.get("SITE_NAME")
	if resolved:
		frappe_app._site = resolved
	return resolved


def create_application():
	pin_default_site()
	return frappe_app.application_with_statics()
