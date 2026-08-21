import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class EligibilityEvaluation(Document):
	def before_insert(self):
		if not self.evaluated_on:
			self.evaluated_on = now_datetime()
		if self.score is None or not self.rule_set:
			return
		rule_set = frappe.get_doc("Eligibility Rule Set", self.rule_set)
		rules = json.loads(rule_set.rules_json or "{}")
		minimum_score = float(rules.get("minimum_score") or 0)
		expected = "Eligible" if float(self.score) >= minimum_score else "Ineligible"
		if not self.result:
			self.result = expected
		if not self.explanation_json:
			self.explanation_json = json.dumps(
				{"minimum_score": minimum_score, "score": float(self.score)},
				sort_keys=True,
			)

	def validate(self):
		if self.score < 0:
			frappe.throw(_("Score cannot be negative."))
		rule_set = frappe.get_doc("Eligibility Rule Set", self.rule_set)
		if rule_set.status != "Published":
			frappe.throw(_("Only published eligibility rule sets can be evaluated."))
		rules = json.loads(rule_set.rules_json)
		minimum_score = float(rules["minimum_score"])
		expected = "Eligible" if float(self.score) >= minimum_score else "Ineligible"
		if not self.result:
			self.result = expected
		if self.result != expected:
			frappe.throw(_("Eligibility result does not match the configured rule set."))
		if not self.explanation_json:
			self.explanation_json = json.dumps(
				{"minimum_score": minimum_score, "score": float(self.score)},
				sort_keys=True,
			)
		explanation = json.loads(self.explanation_json)
		if not isinstance(explanation, dict) or "minimum_score" not in explanation:
			frappe.throw(_("Explanation JSON must include minimum_score."))
