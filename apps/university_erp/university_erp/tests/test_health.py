from frappe.tests import IntegrationTestCase

from university_erp.api.health import live, ready


class TestPlatformHealth(IntegrationTestCase):
	def test_liveness_has_no_sensitive_details(self):
		self.assertEqual(live(), {"status": "ok"})

	def test_readiness_checks_database_and_cache(self):
		self.assertEqual(ready(), {"status": "ready"})
