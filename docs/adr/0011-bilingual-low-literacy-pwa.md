# ADR-0011: Build a bilingual low-literacy guardian PWA

- Status: Accepted
- Date: 2026-08-02
- Related requirements: Applicant and student portal experience

## Context

The pilot school serves a township where many guardians may have limited English, formal education, device capability and network quality. Frappe Desk is not an appropriate public applicant experience.

## Decision

Use a mobile-first Vue 3, TypeScript, Frappe UI and Vite PWA for applicants, guardians and students. Support English and Hindi from the first pilot. Use task-based flows, visible language switching, autosave/resume, simple language, large controls and assisted-entry support. Frappe Desk remains the internal staff interface.

## Consequences

- Real-user usability testing is a production gate.
- Hindi translations require local human review.
- All business rules and authorization remain server-side.
- Native apps and additional languages are deferred until justified.

