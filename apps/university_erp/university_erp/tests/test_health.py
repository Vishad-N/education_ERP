import frappe.app as frappe_app
from frappe.tests import IntegrationTestCase

from university_erp.api.health import live, ready
from university_erp.wsgi import pin_default_site


class TestPlatformHealth(IntegrationTestCase):
	def test_liveness_has_no_sensitive_details(self):
		self.assertEqual(live(), {"status": "ok"})

	def test_readiness_checks_database_and_cache(self):
		self.assertEqual(ready(), {"status": "ready"})

	def test_wsgi_factory_pins_site_for_hostless_probes(self):
		previous = frappe_app._site
		try:
			self.assertEqual(pin_default_site("healthcheck.invalid"), "healthcheck.invalid")
			self.assertEqual(frappe_app._site, "healthcheck.invalid")
		finally:
			frappe_app._site = previous
