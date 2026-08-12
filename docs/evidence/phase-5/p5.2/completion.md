# P5.2 Completion Evidence - Payment Collection and Receipts

Date: 2026-08-13

Site: `p21.localhost`

Status: Complete

## Scope Verified

- Added custom payment DocTypes for provider events and student fee payments/receipts.
- Created a local fake Razorpay order event without live credentials or network calls.
- Posted one online partial payment to ERPNext `Payment Entry`.
- Replayed the same provider webhook and browser callback and verified they reused the same posted `Payment Entry`.
- Posted one offline maker-checker style approved payment to ERPNext `Payment Entry`.
- Generated receipt numbers for online and offline collections.
- Settled the linked Sales Invoice outstanding amount to zero.
- Rejected duplicate provider payment posting and unapproved offline payment submission.
- Verified System Manager and Accounts User permissions and audit Version evidence.

## Verification Commands

```powershell
docker compose exec backend bench --site p21.localhost execute university_erp.domain.fees.payment_collection_proof.run_payment_collection_proof
docker compose exec backend bench --site p21.localhost execute university_erp.domain.fees.payment_collection_proof.run_payment_collection_proof
```

Both runs passed.

## Final Proof Result

```json
{
  "doctype_count": 2,
  "permission_count": 4,
  "demand": "SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109",
  "sales_invoice": "ACC-SINV-2026-00003",
  "provider_order_id": "order_000001",
  "online_fee_payment": "SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00127",
  "online_payment_entry": "ACC-PAY-2026-00004",
  "duplicate_webhook_payment_entry": "ACC-PAY-2026-00004",
  "browser_callback_payment_entry": "ACC-PAY-2026-00004",
  "offline_fee_payment": "SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00128",
  "offline_payment_entry": "ACC-PAY-2026-00005",
  "online_receipt_no": "FEE-REC-SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00127",
  "offline_receipt_no": "FEE-REC-SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00128",
  "invoice_outstanding": 0.0,
  "online_payment_entries_for_event": 1,
  "offline_payment_entries_for_receipt": 1,
  "validation_checks": {
    "duplicate_provider_payment_rejected": true,
    "offline_without_approval_rejected": true
  },
  "audit_versions": 4
}
```

## Exit Gate

Passed. One provider transaction creates at most one posted accounting result, and browser callback replay reuses the same posted accounting result.

## Next Step

Proceed to `P5.3` refunds, settlement and GL reconciliation.
