import json

import frappe
from frappe import _
from frappe.model.document import Document


class EligibilityEvaluation(Document):
	def validate(self):
		if self.score < 0:
			frappe.throw(_("Score cannot be negative."))
		rule_set = frappe.get_doc("Eligibility Rule Set", self.rule_set)
		if rule_set.status != "Published":
			frappe.throw(_("Only published eligibility rule sets can be evaluated."))
		rules = json.loads(rule_set.rules_json)
		minimum_score = float(rules["minimum_score"])
		expected = "Eligible" if float(self.score) >= minimum_score else "Ineligible"
		if self.result != expected:
			frappe.throw(_("Eligibility result does not match the configured rule set."))
		explanation = json.loads(self.explanation_json)
		if not isinstance(explanation, dict) or "minimum_score" not in explanation:
			frappe.throw(_("Explanation JSON must include minimum_score."))
