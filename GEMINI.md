# Project context (Gemini CLI)

> SkillGod manages the memory block below. Your notes above it are safe.

<!-- SKILLGOD:START v1.1 -->
# SkillGod Project Memory (auto-generated — do not edit; updated 2026-08-16 23:25)

# SkillGod Active

Before any **non-trivial coding** task (implement, fix, refactor, debug, wire integrations):
1. Prefer shell: `sg inject "<task>"` (stdout only; exit 0 = success)
2. Or MCP `sg_inject_context` with the user task — if it stalls >5s, cancel and use CLI/digests
3. Digests in this block are the insurance policy when tools are skipped

After completing **meaningful** work (decisions, architecture, non-obvious fixes):
1. Shell: `sg capture --task "..." --output "..."`  **or**
2. MCP `sg_capture_turn` with task + short summary
3. Or `sg remember "decision: ..."`

**Also:** `sg find "<task>"` · `sg timeline` · `sg events --last 20` · `sg doctor`

## SkillGod health
- version: 1.0.1+794a995
- project_id: `visha-90fc8883`
- last inject: 2026-08-16T23:24:07 (runtime)
- last capture: never (-)
- markers: SKILLGOD:START v1.1

## Project memory

## Decisions
- Decision: Railway web role does not run bench new-site, so start-service.sh must mkdir sites/$SITE_NAME/{logs,locks,private,public} before Gunicorn. Missing logs/ caused FileNotFou
- Decision: Railway Metal healthchecks fail with 'service unavailable' when Gunicorn binds IPv4-only 0.0.0.0; bind [::]:$PORT when RAILWAY_ENVIRONMENT is set. Also pin SITE_NAME in u
- Identified that Railway deployment was failing to sync the database because no Prisma migration file was created for the recent `schema.prisma` changes (e.g. `ClientProfile.legalNa
- Fixed 404 and unhandled 401 promise rejections on the client app's `checkout` and `profile` pages. Changed the frontend's profile API call to correctly issue a `PUT` request to `/p
- Fixed a critical bug across 5 dashboard pages (dashboard, meetings, tasks, projects, subscription) that were directly calling `fetch('/api/profile')` instead of using `mockApi.prof
- Updated landing page websiteDesign and ecommerce packages to link to the checkout page instead of the contact form. Also added the packages to the client app checkout page packageD
- Created `/api/orders` route in `apps/client` to fetch client's orders from the backend. Updated `dashboard/page.tsx` to use this endpoint instead of `mockApi.orders`. Also fixed a 

## Notes

_Authoritative project history captured by SkillGod. Treat the decisions above as established context for this project._
<!-- SKILLGOD:END -->
