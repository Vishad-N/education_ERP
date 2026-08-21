# Project conventions

> SkillGod manages the memory block below.

<!-- SKILLGOD:START v1.1 -->
# SkillGod Project Memory (auto-generated — do not edit; updated 2026-08-22 00:39)

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
- last inject: never (-)
- last capture: never (-)
- markers: SKILLGOD:START v1.1

## Project memory

## Decisions
- {"stdout": "warning: in the working copy of 'apps/admin/src/services/api.ts', LF will be replaced by CRLF the next time Git touches it\ndiff --git a/apps/admin/src/services/api.ts 
- {"filePath": "c:\\Users\\visha\\simbolonew\\apps\\admin\\src\\services\\api.ts", "oldString": " if (!res.ok) {\n throw new Error(`API error (${res.status}): ${res.statusText}`);\n 
- {"mode": "content", "numFiles": 0, "filenames": [], "content": "230: * `<DataTable data={...} />`, instead of an ad-hoc `(response.data || response)`", "numLines": 1, "totalLines":
- {"filePath": "c:\\Users\\visha\\simbolonew\\apps\\admin\\src\\services\\api.ts", "oldString": "const emptyPage = <T,>(pageSize: number): Paginated<T> => ({ items: [], total: 0, pag
- {"questions": [{"question": "How do you want to fix the remaining unsafe pages?", "header": "Fix approach", "options": [{"label": "Harden DataTable + fix each page (Recommended)", 
- {"mode": "content", "numFiles": 0, "filenames": [], "content": "96:export interface Paginated<T> {\n97- items: T[];\n98- total: number;\n99- page: number;\n100- pageSize: number;\n
- {"bytes": 0, "code": 401, "codeText": "Unauthorized", "result": "The server returned HTTP 401 Unauthorized.\n\nThe response body was not retrieved. If this URL requires authenticat

## Notes

_Authoritative project history captured by SkillGod. Treat the decisions above as established context for this project._
<!-- SKILLGOD:END -->
