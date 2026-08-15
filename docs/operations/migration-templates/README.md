# Pilot Migration Templates

These CSV templates are for masked, synthetic trial loads only. They are validated by `scripts/migration/validate-trial-load.py` and are not import commands.

Required files:

- `students.csv`: one row per source student identity.
- `guardians.csv`: guardian rows linked by `student_source_id`.
- `fee_opening_balances.csv`: finance-approved opening receivables linked by student and source invoice IDs.

Rules:

- `source_id` is the immutable source-system key and must be unique per file.
- References must point to a row in `students.csv`.
- Opening balances must be non-negative decimal amounts with an explicit currency.
- Use synthetic or masked data outside an approved migration environment.
- Financial totals require finance sign-off before any target posting.
