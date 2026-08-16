"""Isolated restore proof sized for a 500 MB Railway MariaDB volume."""

from __future__ import annotations

import os
import time

import pymysql

REQUIRED = (
	"tabUser",
	"tabDocType",
	"tabRole",
	"tabDefaultValue",
	"tabSeries",
	"tabHas Role",
	"tabSingles",
	"tabModule Def",
)


def ident(name: str) -> str:
	return "`" + name.replace("`", "``") + "`"


def main() -> None:
	host = os.environ["RESTORE_HOST"]
	port = int(os.environ["RESTORE_PORT"])
	password = os.environ["RESTORE_PASSWORD"]
	source = os.environ["RESTORE_SOURCE"]
	target = os.environ.get("RESTORE_TARGET", "education_erp_restore_proof")
	limit = int(os.environ.get("RESTORE_TABLE_LIMIT", "25"))
	started = time.time()

	conn = pymysql.connect(
		host=host,
		port=port,
		user="root",
		password=password,
		connect_timeout=20,
		read_timeout=120,
		write_timeout=120,
		charset="utf8mb4",
	)
	conn.autocommit(True)
	cur = conn.cursor()
	cur.execute(f"DROP DATABASE IF EXISTS {ident(target)}")
	cur.execute(
		"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_type=%s",
		(source, "BASE TABLE"),
	)
	source_tables = cur.fetchone()[0]
	print(f"SOURCE_TABLES={source_tables}", flush=True)

	chosen: list[str] = []
	for name in REQUIRED:
		cur.execute(
			"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
			(source, name),
		)
		if cur.fetchone()[0]:
			chosen.append(name)
	cur.execute(
		"""
		SELECT table_name FROM information_schema.tables
		WHERE table_schema=%s AND table_type='BASE TABLE'
		ORDER BY COALESCE(data_length, 0), table_name
		LIMIT %s
		""",
		(source, limit),
	)
	for (name,) in cur.fetchall():
		if name not in chosen:
			chosen.append(name)

	cur.execute(
		f"CREATE DATABASE {ident(target)} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
	)
	src = ident(source)
	dst = ident(target)
	for name in chosen:
		table = ident(name)
		cur.execute(f"CREATE TABLE {dst}.{table} LIKE {src}.{table}")
		cur.execute(f"INSERT INTO {dst}.{table} SELECT * FROM {src}.{table}")
		cur.execute(f"SELECT COUNT(*) FROM {src}.{table}")
		source_rows = cur.fetchone()[0]
		cur.execute(f"SELECT COUNT(*) FROM {dst}.{table}")
		target_rows = cur.fetchone()[0]
		print(f"RESTORED {name} source={source_rows} restored={target_rows}", flush=True)
		if source_rows != target_rows:
			cur.execute(f"DROP DATABASE {ident(target)}")
			raise SystemExit(f"row-count mismatch for {name}")

	cur.execute(
		"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_type=%s",
		(target, "BASE TABLE"),
	)
	restored_tables = cur.fetchone()[0]
	print(f"RESTORED_TABLES={restored_tables}", flush=True)
	cur.execute(f"DROP DATABASE {ident(target)}")
	cur.close()
	conn.close()
	if restored_tables != len(chosen):
		raise SystemExit("restored table count mismatch")
	print(f"RESTORE_PROOF_OK source_tables={source_tables} restored_tables={restored_tables} seconds={time.time() - started:.1f}", flush=True)


if __name__ == "__main__":
	main()
