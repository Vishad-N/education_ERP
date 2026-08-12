import json

import frappe
from frappe import _
from frappe.model.document import Document


class EligibilityRuleSet(Document):
	def validate(self):
		try:
			rules = json.loads(self.rules_json)
		except Exception:
			frappe.throw(_("Rules JSON must be valid JSON."))
		if not isinstance(rules, dict) or "minimum_score" not in rules:
			frappe.throw(_("Rules JSON must contain minimum_score."))
		if float(rules["minimum_score"]) < 0:
			frappe.throw(_("Minimum score cannot be negative."))
		if self.status == "Published" and not self.effective_from:
			frappe.throw(_("Effective From is required for published rule sets."))
