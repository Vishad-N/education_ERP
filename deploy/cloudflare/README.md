# Cloudflare Edge and R2 Templates

These files are configuration templates only. They do not create DNS records, WAF rules, or buckets. Production Cloudflare changes still require explicit approval.

## Intended use

- Staging and later production sit behind Cloudflare DNS, TLS, WAF, and rate limits.
- Private applicant and student files use Cloudflare R2 through short-lived signed URLs.
- Railway staging currently uses the Railway-provided hostname. Point a custom hostname here only after the user approves the zone and records.

## Files

| File | Purpose |
|---|---|
| `dns-records.example.yaml` | Apex/www/api/portal records and TLS mode |
| `waf-rate-limits.example.yaml` | Login, upload, OTP, payment, and public search limits |
| `r2-bucket.example.json` | Private bucket, versioning, quarantine prefix, and lifecycle |

## Staging mapping

When a custom hostname is approved:

1. Create a proxied CNAME from the staging hostname to the Railway web domain.
2. Set SSL/TLS to Full (strict) after the origin certificate is valid.
3. Keep `/api/method/university_erp.api.health.ready` as the origin health path.
4. Do not proxy WebSocket until a same-origin `/socket.io` route exists.
5. Create the R2 bucket from `r2-bucket.example.json` and inject only managed credentials into the application services.

Do not commit account IDs, API tokens, or bucket access keys.
