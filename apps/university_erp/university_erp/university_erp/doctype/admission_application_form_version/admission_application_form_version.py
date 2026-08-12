import json

import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionApplicationFormVersion(Document):
	def validate(self):
		if self.status == "Published" and not self.published_on:
			frappe.throw(_("Published On is required for published forms."))
		try:
			schema = json.loads(self.form_schema)
		except Exception:
			frappe.throw(_("Form Schema must be valid JSON."))
		if not isinstance(schema, dict) or not schema.get("fields"):
			frappe.throw(_("Form Schema must contain a fields list."))
		if frappe.db.exists(
			"Admission Application Form Version",
			{
				"form_code": self.form_code,
				"version": self.version,
				"name": ["!=", self.name],
				"docstatus": ["<", 2],
			},
		):
			frappe.throw(_("Form Code and Version must be unique."))
