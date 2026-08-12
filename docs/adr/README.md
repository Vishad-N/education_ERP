# Architecture Decision Records

ADRs capture decisions that are expensive to reverse or affect multiple domains. They explain context and tradeoffs; they do not replace requirements or implementation documentation.

## Status values

`Proposed`, `Accepted`, `Superseded`, `Deprecated`, or `Rejected`.

## Process

1. Copy [ADR template](0000-template.md) and assign the next number.
2. Link affected BRD IDs, security controls, contracts, and migration impact.
3. Review with architecture plus affected domain owners.
4. Record the decision date and approvers.
5. Update this index and related specifications in the same change.
6. Supersede an ADR with a new ADR; do not rewrite accepted history.

## Index

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-frappe-v16-platform.md) | Frappe v16 platform baseline | Accepted |
| [0002](0002-custom-app-no-core-forks.md) | Custom app and no routine core forks | Accepted |
| [0003](0003-modular-monolith.md) | Modular monolith first | Accepted |
| [0004](0004-site-per-institution.md) | Site per independent institution | Accepted |
| [0005](0005-erpnext-accounting-source.md) | ERPNext is accounting source of truth | Accepted |
| [0006](0006-immutable-container-releases.md) | Immutable container releases | Accepted |
| [0007](0007-hostinger-vps-platform.md) | Hostinger VPS pilot and pod platform | Accepted |
| [0008](0008-cloudflare-r2-storage.md) | Cloudflare R2 private object storage | Accepted |
| [0009](0009-razorpay-initial-payments.md) | Razorpay initial payment provider | Accepted; ownership resolved by ADR-0012 |
| [0010](0010-initial-messaging-providers.md) | MSG91 SMS and Hostinger SMTP | Accepted; ownership resolved by ADR-0012 |
| [0011](0011-bilingual-low-literacy-pwa.md) | English/Hindi low-literacy PWA | Accepted |
| [0012](0012-institution-owned-provider-accounts.md) | Institution-owned provider accounts for money, SMS, and email identity | Accepted |
| [0013](0013-fee-demand-sales-invoice-accounting-pattern.md) | Sales Invoice pattern for education fee demands | Accepted for Phase 2 proof |
| [0014](0014-fake-provider-contract-foundation.md) | Fake provider adapters for integration contract proofs | Accepted for Phase 2 proof |
