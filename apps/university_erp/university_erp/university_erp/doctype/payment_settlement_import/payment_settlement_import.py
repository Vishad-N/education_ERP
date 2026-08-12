import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class PaymentSettlementImport(Document):
	def validate(self):
		if flt(self.settlement_amount) < 0 or flt(self.expected_amount) < 0:
			frappe.throw(_("Settlement amounts cannot be negative."))
		self.difference_amount = flt(self.settlement_amount) - flt(self.expected_amount)
		if self.status == "Reconciled" and flt(self.difference_amount, 2) != 0:
			frappe.throw(_("Reconciled settlements cannot have a difference."))
		if self.status == "Mismatch" and flt(self.difference_amount, 2) == 0:
			frappe.throw(_("Mismatch settlements must have a non-zero difference."))
