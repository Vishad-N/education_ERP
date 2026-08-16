# Staging Monitoring Templates

These files define the first operator-facing probes and alerts. They do not provision Grafana Cloud, Uptime Kuma, or a paid metrics vendor.

## Minimum staging probes

| Probe | Target | Pass |
|---|---|---|
| Liveness | `GET /api/method/university_erp.api.health.live` | HTTP 200 |
| Readiness | `GET /api/method/university_erp.api.health.ready` | HTTP 200 |
| Login page | `GET /login` | HTTP 200 |
| Guardian portal | `GET /guardian-admission` | HTTP 200 and JS/CSS assets resolve |

Current Railway origin: `https://web-production-7580e.up.railway.app`

## Files

| File | Purpose |
|---|---|
| `uptime-probes.example.yaml` | Uptime Kuma or any HTTP checker |
| `alert-rules.example.yaml` | Page-worthy staging alerts mapped to runbooks |

## Railway-native fallback

Until an external monitor is approved, use:

- Railway HTTP metrics on `web`
- Railway restart and crash notifications
- Daily logical backup checksum from the backup service
- Manual `scripts/ci/verify-deployment.ps1` after artifact changes
