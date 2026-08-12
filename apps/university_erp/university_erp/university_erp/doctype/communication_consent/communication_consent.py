import frappe
from frappe import _
from frappe.model.document import Document


class CommunicationConsent(Document):
	def validate(self):
		if not self.sms_allowed and not self.email_allowed and not self.whatsapp_allowed:
			frappe.throw(_("At least one communication channel must be allowed or the consent should not be recorded."))
