import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class ProgramIntake(Document):
	def validate(self):
		if cint(self.total_capacity) < 0:
			frappe.throw(_("Total Capacity cannot be negative."))
		total = 0
		for row in self.category_intakes:
			if cint(row.capacity) < 0 or cint(row.supernumerary_capacity) < 0:
				frappe.throw(_("Category capacities cannot be negative."))
			total += cint(row.capacity)
		if self.category_intakes and total != cint(self.total_capacity):
			frappe.throw(_("Category capacity total must equal Total Capacity."))

	def before_submit(self):
		self.status = "Approved"

	def on_cancel(self):
		self.status = "Cancelled"

