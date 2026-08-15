# P7.3 Synthetic Migration Reconciliation

Date: 2026-08-15
Site class: isolated local development
Dataset class: synthetic, no personal data
Operator: Engineering automation

## Source integrity

| File | SHA-256 | Rows |
|---|---|---:|
| `students.csv` | `856A3625FE731B77F30172E691C2E9AE6E1132912471A601777864081C109AB7` | 1 |
| `guardians.csv` | `5DE97F9AA81566CD4F6FAB7AF7AB91E1AA225407EEB39E44E9458C6D8DB2BC35` | 1 |
| `fee_opening_balances.csv` | `C99FCD59B2839A331CABA304201FC874B2A45C719F2BCD5E43C177F9EB29898A` | 1 |

## Reconciliation result

| Control | Expected | Actual | Result |
|---|---:|---:|---|
| Student rows | 1 | 1 | Pass |
| Guardian rows | 1 | 1 | Pass |
| Opening-balance rows | 1 | 1 | Pass |
| Guardian reference coverage | 100% | 100% | Pass |
| Fee-to-student reference coverage | 100% | 100% | Pass |
| Duplicate source IDs | 0 | 0 | Pass |
| Invalid monetary values | 0 | 0 | Pass |
| Opening balance total | INR 1,000.00 | INR 1,000.00 | Pass |

This is a no-write dry run. It validates source shape, lineage, references and finance totals without posting accounting entries or importing records. A production-sized trial using approved source extracts and finance sign-off remains a pre-production requirement.

Engineering reconciliation decision: accepted for the local P7.3 gate.
