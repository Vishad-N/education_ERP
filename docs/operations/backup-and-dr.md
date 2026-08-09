# Backup and Disaster Recovery

For this project, Cloudflare R2 object versioning and backup copies supplement but do not replace database PITR, encryption-key escrow, or tested site restore. Hostinger snapshots may accelerate machine recovery but are not the authoritative application backup and must use a separately protected recovery path.

## Objectives

- Recovery Point Objective: 15 minutes.
- Recovery Time Objective: 2 hours.
- Targets are accepted only after measured restore and DR exercises at production scale.

## Backup scope

For every site, protect:

- MariaDB database plus binary logs/PITR chain;
- private/public files and object versions;
- `site_config.json` and site encryption key through a separate secure mechanism;
- application SHA manifest, image digest and schema/patch version;
- infrastructure and monitoring configuration;
- integration configuration references, not plaintext secrets in general backups;
- fleet inventory and restore ordering information.

A database without its matching site encryption key is an incomplete recovery set.

## Policy baseline

- Automated daily full logical/site backup.
- Continuous or frequent binary-log shipping sufficient for the RPO.
- Object storage versioning and cross-account/region replication.
- Encrypted off-host copies with separate credentials.
- Immutable/write-protected recovery copy.
- Example retention: daily 30 days, weekly 12 weeks, monthly 12 months, pending approved legal/finance policy.
- Backup success and age monitored per site.

## Restore validation

Monthly, restore a rotating set of sites into an isolated environment and prove:

- database and files restore with correct keys;
- application/image and schema compatibility;
- login, permissions and private-file access;
- representative admission, student and fee records;
- ERPNext GL and operational fee reconciliation;
- queues/scheduler are intentionally controlled before activation;
- measured RPO and RTO plus evidence.

Do not count a backup job's success message as restore evidence.

## Disaster scenarios

| Scenario | Recovery approach |
|---|---|
| Accidental record change | Domain reversal/version restore; avoid whole-site restore unless necessary |
| Site/database corruption | Isolate, restore latest clean full plus PITR, reconcile |
| Primary database loss | Promote validated replica or restore managed HA, verify consistency |
| Object deletion/corruption | Restore object version/replica and validate database links |
| Region/account outage | Provision DR stack, restore replicated data/keys, switch DNS/provider callbacks |
| Credential/key compromise | Contain, rotate, restore trust, assess data access, reconcile |
| Bad deployment/migration | Stop rollout, forward-fix or restore under incident/data-loss decision |

## DR exercise

At least twice yearly and before the first production pilot:

1. Declare scenario, scope and success criteria.
2. Activate incident command and communication path.
3. Provision or activate isolated recovery infrastructure.
4. Restore secrets/keys through approved access.
5. Restore database to target point and object files.
6. Deploy the matching immutable image and migrate only if planned.
7. Validate technical health, permissions, critical workflows and reconciliation.
8. Measure detection, decision, RPO and RTO.
9. Record gaps, owners and remediation dates.

## Security

Backup operators cannot silently alter production. Backup credentials are separate, least-privileged and MFA-protected. Encrypt in transit/at rest, audit access/restores, scan restored environments, and prevent restored production data from becoming an unmasked development environment.
