import frappe
from frappe.tests import IntegrationTestCase

from university_erp.api.portal import _hash_token, get_student_portal_snapshot


class TestStudentPortalApi(IntegrationTestCase):
	"""Contract coverage for the access-token boundary of the student portal."""

	def test_access_token_is_hashed(self):
		access_value = "p71-test-token"
		self.assertNotEqual(_hash_token(access_value), access_value)
		self.assertEqual(_hash_token(access_value), _hash_token(access_value))

	def test_invalid_access_token_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			get_student_portal_snapshot("invalid-p71-token")

	def test_snapshot_requires_existing_proof_access(self):
		access = frappe.db.get_value(
			"Student Portal Access",
			{"token_hash": _hash_token("p62-student-portal-proof-token"), "status": "Active"},
			"name",
		)
		if not access:
			self.skipTest("P6.2 synthetic portal proof data is not loaded on this site")

		snapshot = get_student_portal_snapshot("p62-student-portal-proof-token")
		self.assertIn("student", snapshot)
		self.assertIn("dues", snapshot)
		self.assertIn("receipts", snapshot)
		self.assertIn("documents", snapshot)
