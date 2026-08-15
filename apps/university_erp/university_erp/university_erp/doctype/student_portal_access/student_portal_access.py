import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class StudentPortalAccess(Document):
	def validate(self):
		if self.status == "Active" and self.expires_on and getdate(self.expires_on) < getdate(frappe.utils.today()):
			frappe.throw(_("Expired portal access cannot be active."))
