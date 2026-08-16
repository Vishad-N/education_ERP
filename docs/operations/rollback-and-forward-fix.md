# Rollback and Forward-Fix Criteria

Use this file for staging and later production releases. Prefer a forward-fix when the new schema has already accepted writes.

## Decision rule

| Situation | Action |
|---|---|
| New image fails health/ready before traffic | Keep previous running replicas. Do not migrate. |
| New image is healthy, no schema change, defect found | Redeploy the previous known-good image digest. |
| Schema migration ran and new writes occurred | Forward-fix. Do not roll the database back. |
| Schema migration ran, no new writes, migration is reversible | Restore from the pre-migration dump into an isolated database, verify, then cut over only with an explicit data-loss assessment. |
| Seat, payment, or conversion invariant is broken | Freeze the affected command, keep the site up for reads if safe, then forward-fix. |
| Combined scheduler/worker replica is down | Restart that one replica. Do not start a second scheduler. |

## Known-good Railway staging images

| Role | Deployment | Image digest |
|---|---|---|
| `web` | `b757b47a-bd87-4f7a-be60-ec370b3df517` | `sha256:9e67b33f90b77701b1aa6d9d3641f960f39afe0d155ff244d1281db14047eb85` |
| Combined scheduler/worker (`bootstrap` service) | `71c6041d-f258-4317-8a16-6df0f94b4840` | `sha256:43f711b403e4358254994c200147b72d16459c4f57f45c13516039d24ee7c506` |

These two digests were built independently. Before a production cutover, rebuild once and run every role from the same digest.

## Staging rollback commands

```text
railway redeploy --service web --yes
railway redeploy --service bootstrap --yes
```

Redeploy reuses the latest successful build. To return to an older digest, redeploy that deployment from the Railway dashboard or rebuild from the matching Git snapshot.

Do not rerun `bootstrap`/`bench new-site` against a populated database.

## Restore path

1. Take a logical dump with `scripts/operations/backup-mariadb.sh`.
2. Restore into a disposable database with `scripts/operations/restore-mariadb.sh`.
3. Compare table counts.
4. Point a stopped application role at the restored database only after checksum verification.
5. Set `ALLOW_LIVE_RESTORE=1` only when replacing the live schema is an approved incident action.

## Communication

Record the release, digest, decision (rollback vs forward-fix), operator, start time, and verification result in the incident or release note. Do not paste secrets or personal data.
