# P4.2 Eligibility, Merit, Seats and Offers Completion Evidence

Date: 2026-08-13

Site: `p21.localhost`

## Scope Completed

- Added published eligibility rule sets and explainable eligibility evaluations.
- Added merit configuration, immutable published merit runs and ranked merit entries.
- Added admission seat matrix, allocation round and seat offer records.
- Added server-side accepted-offer capacity protection using a locked seat matrix row before submit.
- Kept all product behavior in `university_erp`; no upstream Frappe, ERPNext, Education, CRM or Payments source was edited.

## Verification

Commands run:

```powershell
docker compose exec backend bench --site p21.localhost migrate
docker compose exec backend bench --site p21.localhost execute university_erp.domain.admissions.merit_seat_proof.run_merit_seat_proof
docker compose exec backend bench --site p21.localhost execute university_erp.domain.admissions.merit_seat_proof.run_merit_seat_proof
```

Result:

- Migration passed.
- Repeatable proof passed twice after the overflow negative-test cleanup.
- Proof counted 8 P4.2 custom DocTypes and 16 role permissions.
- Eligibility rule set: `ERS-P42-MIN-SCORE-2026.1`.
- Merit configuration: `P42-MERIT-2026`.
- Merit run: `MR-P42-MERIT-2026-00066`, status `Published`.
- Seat matrix: `ASM-P31-OFFER-2026-P31 General`, capacity `1`.
- Allocation round: `SAR-MR-P42-MERIT-2026-00066-1`, status `Published`.
- Accepted offer: `SO-SAR-MR-P42-MERIT-2026-00066-1-EDU-APP-2026-00002`.
- Waitlist offer: `SO-SAR-MR-P42-MERIT-2026-00066-1-EDU-APP-2026-00003`.
- Accepted offer count remained `1`, matching the seat matrix capacity.
- Validation checks rejected invalid eligibility rules, incorrect eligibility results, duplicate merit rank and a second accepted offer after capacity was full.
- Seat offer audit Version evidence existed and increased on repeat proof.

## Remaining Later-Phase Work

- Browser/portal workflow tests, public API methods, localization and CI integration remain later-phase work.
- Admission confirmation, required gates and applicant-to-student conversion start in `P4.3`.
