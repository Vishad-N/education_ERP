import json

import frappe
from frappe import _
from frappe.model.document import Document


class MeritConfiguration(Document):
	def validate(self):
		try:
			tie_breakers = json.loads(self.tie_breaker_json)
		except Exception:
			frappe.throw(_("Tie Breaker JSON must be valid JSON."))
		if not isinstance(tie_breakers, list) or not tie_breakers:
			frappe.throw(_("Tie Breaker JSON must contain at least one rule."))
