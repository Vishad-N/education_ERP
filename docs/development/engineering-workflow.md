# Engineering Workflow

## Work item readiness

A work item is Ready only when it has BRD IDs, acceptance criteria, domain owner, data changes, state transitions, permissions, audit behavior, API/event impact, migration impact, failure behavior, and a test plan. Financial changes also require accounting mapping and reconciliation criteria.

## Branch and change scope

- Use short-lived branches and focused pull requests.
- Do not combine unrelated refactors with feature behavior.
- Preserve generated Frappe metadata required to reproduce the change.
- Update requirements, ADRs, API contracts and runbooks with the code they govern.
- Never modify upstream applications for convenience.

## Implementation sequence

1. Confirm fit-gap against standard Frappe/Education/ERPNext/CRM behavior.
2. Define the state transition or command and authorization rules.
3. Define data constraints, idempotency and transaction boundary.
4. Implement pure policy/calculation logic where possible.
5. Implement DocType controllers and domain services.
6. Add API/UI adapters without duplicating business rules.
7. Add migrations, indexes and fixtures.
8. Add unit, integration, permission and failure-path tests.
9. Validate observability, deployment and rollback/forward-fix impact.

## Frappe rules

- Use hooks and `extend_doctype_class` where supported before full overrides.
- Business rules run server-side; client code improves ergonomics only.
- Use Frappe ORM/query builder unless measured evidence requires reviewed SQL.
- Never use `ignore_permissions=True` as a general fix. Any privileged service documents its actor, scope, reason and tests.
- Direct status field edits are prohibited; expose controlled commands/workflows.
- Queue work after commit and use idempotent jobs.
- Store provider secrets only in approved encrypted configuration/secrets management.

## Schema and data changes

- Every schema change includes forward migration and compatibility analysis.
- Use expand-and-contract for destructive or incompatible changes.
- Large backfills are checkpointed and resumable.
- Index changes include query-plan evidence and production creation strategy.
- Cancellation/reversal replaces destructive edits to financial/published records.
- Migration tests cover fresh install and oldest supported upgrade path.

## Review requirements

| Change | Required review |
|---|---|
| Financial posting, tax, refund, reconciliation | Finance/accounting owner |
| Identity, consent, PII, documents, retention | Security/privacy owner |
| Permissions or privileged services | Security plus domain owner |
| Schema migration or high-volume query | Database/architecture owner |
| Public API, webhook, event | Integration owner |
| Infrastructure, secrets, backup, deployment | Platform/operations owner |
| User workflow or acceptance behavior | Product/domain owner |

## Pull request description

```text
Problem and BRD IDs
Acceptance criteria
Scope and exclusions
Business rules and state transitions
DocTypes/schema/index changes
Permissions and audit impact
API/event/integration impact
Accounting and reconciliation impact
Privacy/security impact
Tests and evidence
Deployment and migration impact
Rollback or forward-fix plan
Open risks and decisions
```

## Definition of Done

- Acceptance criteria and requirement traceability are updated.
- Automated tests cover success, authorization, validation, concurrency/retry where relevant, and failure recovery.
- Fresh install and upgrade migrations pass.
- Logs/metrics contain correlation but no secrets or unnecessary PII.
- Documentation and runbooks match implementation.
- Required specialist reviews and UAT evidence are complete.
- No unresolved Severity 1/2 defects or unapproved high risks remain.

## Release versioning

Version `university_erp` using SemVer. Record app SHAs, schema/patch state, image digest and release notes. Breaking public contracts require a versioned compatibility and migration plan.

