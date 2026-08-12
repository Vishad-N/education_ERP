import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class FeeGeneralLedgerReconciliation(Document):
	def validate(self):
		self.net_collected_amount = flt(self.collected_amount) - flt(self.refund_amount)
		if flt(self.total_fee_amount) < 0 or flt(self.collected_amount) < 0 or flt(self.refund_amount) < 0:
			frappe.throw(_("Reconciliation amounts cannot be negative."))
		if self.status == "Reconciled" and flt(self.gl_balance, 2) != 0:
			frappe.throw(_("Reconciled records must have balanced GL entries."))
		expected_net = flt(self.total_fee_amount) - flt(self.refund_amount)
		if flt(self.net_collected_amount, 2) != flt(expected_net, 2):
			frappe.throw(_("Net collected amount must reconcile to fee and refund totals."))
