# Security and Privacy

## Security objectives

Protect student/applicant PII, credentials, documents, admission decisions and financial records; enforce institution/campus/role boundaries; preserve trustworthy audit history; and keep critical operations available during admission and payment peaks.

Project-specific provider controls are mandatory: Razorpay and MSG91 webhooks require signature verification and replay protection; OTP values must never be logged; Hostinger SMTP credentials are isolated by institution/environment; and Cloudflare R2 objects remain private, quarantined until malware checks pass, and accessible only through short-lived signed URLs. See the [provider architecture](../integrations/provider-architecture.md).

## Data classification

| Class | Examples | Controls |
|---|---|---|
| Public | Published program and calendar data | Integrity, publishing approval |
| Internal | Operational configurations, non-sensitive reports | Authenticated access |
| Confidential | Student profile, guardian/contact, applications, fees | Least privilege, encryption, audit, export controls |
| Restricted | Credentials, Aadhaar if lawfully collected, payment secrets, sensitive documents | Strong field/file controls, masking, encryption, access logging, minimal retention |

Do not collect data merely because the system can store it. Record purpose, lawful basis/authority, owner, retention and permitted consumers before adding restricted data.

## Access-control model

Authorization combines site isolation, role, institution/campus scope, record ownership, field permission level, workflow state and explicit approval. UI visibility is not authorization. Query conditions, document permissions, reports, exports, APIs, background jobs and file access must enforce the same policy.

Privileged actions require maker-checker where appropriate: intake/reservation changes, eligibility override, merit republish, manual seat allocation, admission cancellation, identity merge/correction, fee concession, refund/write-off, reconciliation adjustment, role change and audit export.

## Identity and sessions

- MFA for Administrator, System Manager, finance, security and other privileged roles.
- SSO when required, with emergency break-glass accounts separately controlled and monitored.
- Strong password/session policy, login throttling and suspicious-login alerts.
- Separate service identities per integration and environment; no shared human accounts.
- Disable access promptly on role/status change and review privileged access at least quarterly.

## Application controls

- Server-side validation and permission enforcement for every command.
- CSRF protection for browser sessions and strict allowed origins/referrers.
- Parameterized ORM/query-builder access; reviewed SQL only when necessary.
- Output encoding and safe rich-text handling to prevent XSS.
- SSRF-safe outbound allowlists and timeouts.
- Bounded pagination, payload/file limits, rate limits and abuse controls.
- Idempotency and replay protection for payments, webhooks and critical commands.
- Generic external errors with correlated internal diagnostics.

## Sensitive data handling

- Encrypt data in transit and at rest using managed keys.
- Keep site encryption keys and backup keys separate from database backups.
- Mask restricted identifiers by default and exclude them from lists, search indexes, URLs, logs, metrics, notifications and exports.
- Use one-way normalized hashes for duplicate lookup when the clear value is unnecessary.
- Restrict exports, watermark/log them where appropriate, and make generated files private and expiring.
- Mask or synthesize all non-production data.

If Aadhaar is approved for collection, document authority/lawful basis, minimize fields, prefer masked Aadhaar, encrypt it, restrict access, log access and define retention. It must not become the universal student identifier.

## File security

All applicant/student uploads are private. Validate size, extension, MIME and file signature; quarantine and malware-scan; reject active/unapproved content; generate short-lived authorized download URLs; and audit view, verification, replacement and export. Scanner failure leaves files quarantined.

## Secrets and cryptography

- Store production secrets in a managed secret service, never Git, images, logs, tickets or screenshots.
- Rotate credentials and keys on schedule and incident.
- Use platform/provider-supported cryptography; do not invent encryption schemes.
- Verify webhook HMAC/signatures and timestamps using constant-time comparison where applicable.
- Keep separate credentials and keys per environment, site/provider and function.

## Audit requirements

Audit authentication, permission/role change, sensitive record access where required, status transition, approval/override, identity merge, document verification, merit publication, seat allocation, financial posting/reversal, export, configuration and integration credential change. Include actor, delegated actor, time, source, entity, action, reason, approval and correlation ID without sensitive payloads.

Protect audit data from normal user mutation, monitor gaps, retain per approved policy and provide permission-controlled export.

## Privacy lifecycle

Maintain consent/preference history independently from immutable transactional communications. Support correction, access/export, retention, archival, legal hold, anonymization and deletion where approved and lawful. Requirements must account for applicable Indian law, CERT-In directions, institutional policy, financial retention and sector regulations; legal counsel owns legal interpretation.

## Infrastructure security

- Private database/cache networks and minimal inbound exposure.
- WAF, DDoS protection, TLS policy and rate limiting at the edge.
- Hardened minimal images, non-root runtime where supported, read-only filesystem where practical.
- Signed images, SBOM, dependency/container/IaC scanning and patch SLAs.
- Audited administrative path with MFA and least privilege.
- Separate backup account/credentials and immutable backup copies.
- Central security logs and alerting with access controls and retention.

## Vulnerability and incident handling

Define severity, triage owner, remediation SLA, disclosure path and emergency release process. Preserve evidence, rotate affected credentials, assess data/financial impact, notify approved stakeholders, reconcile business state and conduct a blameless corrective-action review.

## Release gate

- Threat model and data-flow review are current.
- Permission matrix and negative tests pass.
- No unaccepted critical/high vulnerabilities.
- Secret, dependency, container and application scans pass policy.
- Penetration findings are resolved or formally accepted.
- Incident contacts/runbooks, backup/restore and monitoring are active.
- Production secrets are newly provisioned or rotated and never reused from lower environments.
