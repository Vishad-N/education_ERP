"""Validate pilot migration CSVs without writing to Frappe or production."""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


SCHEMAS = {
    "students": {"source_id", "student_id", "full_name", "date_of_birth", "status"},
    "guardians": {"source_id", "student_source_id", "full_name", "mobile"},
    "fee_opening_balances": {"source_id", "student_source_id", "invoice_source_id", "amount", "currency"},
}


def read_rows(path: Path, required: set[str]) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = required - fields
        if missing:
            errors.append(f"{path.name}: missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        source_id = row.get("source_id", "").strip()
        if not source_id:
            errors.append(f"{path.name}:{index}: source_id is required")
        elif source_id in seen:
            errors.append(f"{path.name}:{index}: duplicate source_id {source_id}")
        seen.add(source_id)
    return rows, errors


def validate(folder: Path) -> dict[str, object]:
    errors: list[str] = []
    rows_by_type: dict[str, list[dict[str, str]]] = {}
    for kind, required in SCHEMAS.items():
        path = folder / f"{kind}.csv"
        if not path.exists():
            errors.append(f"missing template: {path.name}")
            continue
        rows, row_errors = read_rows(path, required)
        rows_by_type[kind] = rows
        errors.extend(row_errors)

    student_ids = {row.get("source_id", "").strip() for row in rows_by_type.get("students", [])}
    for index, row in enumerate(rows_by_type.get("guardians", []), start=2):
        if row.get("student_source_id", "").strip() not in student_ids:
            errors.append(f"guardians.csv:{index}: unknown student_source_id")

    total = Decimal("0")
    for index, row in enumerate(rows_by_type.get("fee_opening_balances", []), start=2):
        if row.get("student_source_id", "").strip() not in student_ids:
            errors.append(f"fee_opening_balances.csv:{index}: unknown student_source_id")
        try:
            amount = Decimal(row.get("amount", ""))
            if amount < 0:
                errors.append(f"fee_opening_balances.csv:{index}: amount cannot be negative")
            total += amount
        except InvalidOperation:
            errors.append(f"fee_opening_balances.csv:{index}: amount must be a decimal")

    return {
        "valid": not errors,
        "counts": {kind: len(rows) for kind, rows in rows_by_type.items()},
        "opening_balance_total": str(total),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    result = validate(args.folder)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
