# P3.1 Completion Evidence

Date: 2026-08-12

Site: `p21.localhost`

## Scope Completed

`P3.1 - Institution and Academic Masters` is complete for the local pilot foundation.

Implemented in `university_erp`:

- institution hierarchy and structure versioning;
- academic session policy and calendar;
- program version, offering, class and section;
- curriculum version and curriculum course rows;
- subject offering;
- intake and category capacity rows;
- faculty assignment;
- timetable slot and timetable entry;
- permission metadata for `System Manager` and `Academics User`;
- Frappe `Version` audit evidence on tracked master records.

The implementation is under:

```text
apps/university_erp/university_erp/university_erp/doctype/
apps/university_erp/university_erp/domain/academic/master_proof.py
```

No upstream source under `apps/frappe`, `apps/erpnext`, `apps/education`, `apps/crm`, `apps/payments`, or `apps/frappe_docker` was modified.

## Verification Commands

```powershell
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && env/bin/python -m compileall -q apps/university_erp/university_erp/domain/academic apps/university_erp/university_erp/university_erp/doctype"
docker compose exec backend bench --site p21.localhost migrate
docker compose exec backend bench --site p21.localhost execute university_erp.domain.academic.master_proof.run_master_proof
```

The proof was run twice after migration to confirm repeatable behavior.

## Final Proof Result

```json
{
  "doctype_count": 17,
  "permission_count": 28,
  "institution_nodes": ["P31-UNIV", "P31-CAMPUS", "P31-COLLEGE", "P31-DEPT"],
  "structure_version": "ISV-2026-00001",
  "academic_year": "P31 Academic Year 2026-27",
  "academic_term": "P31 Academic Year 2026-27 (Term 1)",
  "session_policy": "ASP-P31 Academic Year 2026-27-00003",
  "academic_calendar": "P31-CALENDAR-2026",
  "program": "P31 Proof Program",
  "program_version": "PV-P31 Proof Program-2026",
  "course": "P31 English",
  "curriculum_version": "CV-PV-P31 Proof Program-2026-CUR-2026",
  "program_offering": "P31-OFFER-2026",
  "class_offering": "P31-CLASS-2026",
  "section": "P31-A",
  "subject_offering": "P31-ENG-2026",
  "instructor": "P31 Proof Instructor",
  "faculty_assignment": "P31-ENG-FAC-2026",
  "timetable_slot": "P31-MON-0900",
  "timetable_entry": "P31-TT-ENG-001",
  "timetable_conflict_rejected": true,
  "audit_versions": 4,
  "student_category": "P31 General",
  "program_intake": "PI-P31-OFFER-2026-00002"
}
```

## Gate Coverage

- Pilot academic structure can be configured from institution root through campus, college and department.
- Academic year, term, session policy and calendar can be configured.
- Program version, curriculum, course, offering, class, section and subject offering can be configured.
- Intake capacity and category capacity totals are validated.
- Faculty assignment can be configured against a subject offering.
- Timetable slot and entry can be configured.
- Duplicate timetable allocation in the same section/faculty slot is rejected.
- System Manager and Academics User permissions exist on the P3.1 setup DocTypes.
- Tracked DocTypes produce Frappe `Version` audit evidence when changed.

## Remaining Later-Phase Work

P3.1 is complete as a foundation gate, but later phases still need stronger production-grade coverage:

- browser/Desk workflows;
- full CI integration;
- institution-specific approval workflows;
- broader report coverage;
- concurrency tests for admission seats and fee/payment flows in later phases.

## Status

`P3.1` passed its local completion gate. The next executable step is `P3.2 - Student Identity and Documents`.
