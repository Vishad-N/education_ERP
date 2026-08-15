import unittest
from datetime import datetime, timedelta

from university_erp.integrations.exceptions import ProviderReplayError, ProviderValidationError
from university_erp.integrations.idempotency import InMemoryIdempotencyStore
from university_erp.integrations.security import (
	assert_export_allowed,
	audit_event,
	mask_identifier,
	retention_expired,
)
from university_erp.integrations.storage.fake_r2 import FakeR2Adapter
from university_erp.integrations.webhooks import HmacWebhookVerifier


class TestSecurityPrimitives(unittest.TestCase):
	def test_identifier_masking_never_returns_full_value(self):
		self.assertEqual(mask_identifier("123456789012"), "********9012")
		self.assertEqual(mask_identifier("123"), "***")
		self.assertIsNone(mask_identifier(None))

	def test_webhook_rejects_bad_signature_and_replay(self):
		verifier = HmacWebhookVerifier(
			**{
				"secret": "local-test-secret",
				"replay_store": InMemoryIdempotencyStore(),
				"now": 1_800_000_000,
			}
		)
		body = b'{"event":"payment.captured"}'
		signature = verifier.sign(timestamp=1_800_000_000, body=body)
		result = verifier.verify(
			event_id="evt-p72-1",
			timestamp=1_800_000_000,
			body=body,
			signature=signature,
			correlation_id="corr-p72-1",
		)
		self.assertEqual(result.correlation_id, "corr-p72-1")
		with self.assertRaises(ProviderReplayError):
			verifier.verify(
				event_id="evt-p72-1",
				timestamp=1_800_000_000,
				body=body,
				signature=signature,
			)
		with self.assertRaises(ProviderValidationError):
			verifier.verify(
				event_id="evt-p72-2",
				timestamp=1_800_000_000,
				body=body,
				signature="invalid",
			)

	def test_private_object_url_ttl_is_bounded(self):
		storage = FakeR2Adapter()
		storage.put_private_object(key="student/p72/document.pdf", body=b"pdf", content_type="application/pdf")
		self.assertIn("expires=900", storage.signed_download_url(key="student/p72/document.pdf", expires_in_seconds=900))
		with self.assertRaises(ProviderValidationError):
			storage.signed_download_url(key="student/p72/document.pdf", expires_in_seconds=901)

	def test_export_requires_approval_and_privilege_for_unmasked_data(self):
		with self.assertRaises(ValueError):
			assert_export_allowed(status="Draft", masked=True, is_privileged=False)
		with self.assertRaises(PermissionError):
			assert_export_allowed(status="Approved", masked=False, is_privileged=False)
		assert_export_allowed(status="Approved", masked=False, is_privileged=True)

	def test_retention_and_audit_contracts(self):
		now = datetime(2026, 8, 14)
		self.assertTrue(retention_expired(now - timedelta(days=31), retention_days=30, now=now))
		self.assertFalse(retention_expired(now - timedelta(days=29), retention_days=30, now=now))
		event = audit_event(action="privacy_export", entity="SPER-1", actor="Administrator", correlation_id="corr-p72")
		self.assertEqual(event["correlation_id"], "corr-p72")
