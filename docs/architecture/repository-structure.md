# Repository and Folder Structure

## Target layout

```text
erp-repository/
|-- AGENTS.md
|-- README.md
|-- apps.json
|-- compose.yaml
|-- .env.example
|-- .editorconfig
|-- .gitignore
|-- .pre-commit-config.yaml
|-- docs/
|   |-- README.md
|   |-- adr/
|   |-- architecture/
|   |-- development/
|   |-- operations/
|   |-- quality/
|   |-- requirements/
|   `-- security/
|-- infrastructure/
|   |-- environments/
|   |   |-- development/
|   |   |-- staging/
|   |   `-- production/
|   |-- modules/
|   |-- monitoring/
|   `-- policies/
|-- docker/
|   |-- Dockerfile
|   |-- entrypoints/
|   `-- config/
|-- scripts/
|   |-- bootstrap/
|   |-- ci/
|   |-- migration/
|   `-- operations/
|-- tests/
|   |-- contract/
|   |-- e2e/
|   |-- performance/
|   `-- security/
`-- apps/
    `-- university_erp/
        |-- pyproject.toml
        |-- package.json
        |-- README.md
        |-- license.txt
        `-- university_erp/
            |-- hooks.py
            |-- modules.txt
            |-- patches.txt
            |-- config/
            |-- fixtures/
            |-- patches/
            |-- public/
            |-- templates/
            |-- website/
            |-- api/
            |   `-- v1/
            |-- domain/
            |   |-- institution/
            |   |-- academic/
            |   |-- student_identity/
            |   |-- admissions/
            |   |-- merit/
            |   |-- fees/
            |   |-- notifications/
            |   |-- compliance/
            |   `-- reporting/
            |-- integrations/
            |   |-- payments/
            |   |-- sms/
            |   |-- email/
            |   |-- storage/
            |   `-- antivirus/
            `-- tests/
```

Bench-managed upstream applications may live beside `university_erp` in a development bench, but their source is not committed or modified as part of this product repository unless the approved repository strategy explicitly vendors them.

## Domain package convention

Each domain may contain:

```text
domain_name/
|-- doctype/          generated DocType packages and controllers
|-- services/         multi-DocType application commands
|-- policies/         pure business rule evaluation
|-- queries/          permission-safe read models
|-- events/           event schemas and handlers
|-- permissions.py    query and document permission rules
|-- constants.py      stable domain constants only
`-- tests/            domain-focused tests
```

Do not create every folder pre-emptively. Add it when the first owned implementation exists.

## Dependency direction

```text
API / UI / jobs
    -> domain services
        -> domain policies and DocType controllers
            -> Frappe / ERPNext / Education APIs

integrations
    implement domain-owned ports

reporting
    reads domain-owned records through permission-safe queries
```

- A domain cannot import another domain's private controller internals.
- Cross-domain writes go through a named service command.
- Provider SDKs remain inside `integrations`.
- API modules validate transport concerns and delegate business behavior.
- Client code never becomes the only owner of a business rule.
- Circular domain imports must be removed through an explicit command/event contract.

## Generated and committed artifacts

Commit custom DocType JSON, reports, workspaces, fixtures, patches, print formats, translations, and migration metadata required to reproduce a site. Do not commit runtime sites, logs, backups, private files, secrets, caches, dependencies, or generated build output unless release tooling specifically requires an artifact manifest.

## Configuration rules

- `.env.example` contains names and safe examples, never real secrets.
- Site-specific configuration is supplied by the deployment environment.
- Feature flags are typed, documented, default-safe, and removable.
- Environment differences are configuration, not divergent source branches.
- Infrastructure modules are versioned and promoted using reviewed plans.

## Naming

- Python packages and modules: `snake_case`.
- DocTypes and user-facing records: singular Title Case.
- API paths: lowercase nouns under `/api/v1/`.
- Events: past-tense domain facts such as `admission.offer_accepted.v1`.
- Commands/services: imperative names such as `accept_seat_offer`.
- Tests: describe behavior and condition, not implementation method.

## Ownership

Add `CODEOWNERS` when teams are assigned. At minimum, require domain owner review for accounting, permissions, identity/PII, schema migrations, external contracts, infrastructure, and production runbooks.

