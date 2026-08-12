# P3.1 Initial Master Schema Evidence

Date: 2026-08-12

Site: `p21.localhost`

Superseded by: `docs/evidence/phase-3/p3.1/completion.md`

## Scope Started

This evidence records the first executable slice of `P3.1 - Institution and Academic Masters`.

Implemented in the custom app only:

- `Education Institution Node`
- `Institution Structure Version`
- `Program Version`
- `Program Offering`
- `Class Offering`
- `Academic Section`
- `Program Intake`
- `Category Intake`
- synthetic proof harness at `university_erp.domain.academic.master_proof.run_master_proof`

The DocTypes are located under the generated Frappe module package:

```text
apps/university_erp/university_erp/university_erp/doctype/
```

No upstream files under `apps/frappe`, `apps/erpnext`, `apps/education`, `apps/crm`, or `apps/payments` were modified.

## Local Verification

```powershell
docker compose exec backend bench --site p21.localhost migrate
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && env/bin/python -m compileall -q apps/university_erp/university_erp/domain/academic apps/university_erp/university_erp/university_erp/doctype"
docker compose exec backend bench --site p21.localhost execute university_erp.domain.academic.master_proof.run_master_proof
```

Result:

```json
{
  "doctype_count": 8,
  "institution_nodes": ["P31-UNIV", "P31-CAMPUS", "P31-COLLEGE", "P31-DEPT"],
  "structure_version": "ISV-2026-00001",
  "academic_year": "P31 Academic Year 2026-27",
  "academic_term": "P31 Academic Year 2026-27 (Term 1)",
  "program": "P31 Proof Program",
  "program_version": "PV-P31 Proof Program-2026",
  "program_offering": "P31-OFFER-2026",
  "class_offering": "P31-CLASS-2026",
  "section": "P31-A",
  "student_category": "P31 General",
  "program_intake": "PI-P31-OFFER-2026-00002"
}
```

The proof was run twice and returned the same business records on the second run.

## Validation Covered

- Institution node codes are normalized to uppercase.
- Institution hierarchy order is validated from University to Campus to College to Department.
- Structure versions can be submitted and become `Published`.
- Program versions validate credit bounds and become `Published` on submit.
- Program offerings require a published program version and an active institution node.
- Class offerings require an open or locked program offering.
- Section capacity must be non-negative.
- Program intake category capacity totals must match the total capacity and become `Approved` on submit.

## Former Open P3.1 Work

At the time this slice was recorded, it was not the P3.1 exit gate. The remaining items were:

- academic session policy and calendar lifecycle beyond standard `Academic Year` and `Academic Term`;
- curriculum/course/CBCS/NEP rules;
- subject offerings;
- timetable slot and entry foundations;
- faculty assignment and workload foundations;
- lock workflows and approval workflows;
- permission, audit, failure-path, migration, and report tests;
- traceable acceptance criteria for every affected BRD story.

## Current Status

This file records the first P3.1 slice only. P3.1 later passed its completion gate in `docs/evidence/phase-3/p3.1/completion.md`.
