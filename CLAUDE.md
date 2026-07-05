# LP Reporting Assistant — project context for Claude Code

This file is auto-loaded by Claude Code when started in this folder. Read it first, then
`README.md` and `n8n/SETUP.md` for the full user-facing docs.

## What this project is

A prototype built for an AI Intern / AI Deployment Strategist interview at a PE firm. It's a
two-step AI workflow (not a multi-agent system): upload a portfolio company's quarterly report
PDF, Claude drafts an LP update paragraph and flags KPI anomalies, a second Claude pass reviews
it for factual accuracy and tone, and the final paragraph is written into a branded Google Doc.

The interview is imminent — prioritize getting the live demo working end-to-end over further
polish.

## Repo layout

- `reports/` — 3 fictional quarterly report PDFs (dummy dataset): NexoraCloud, Solvex Diagnostics
  (has an intentional anomaly: slowed growth, margin drop, delayed launch), Kestrel Data Systems
- `n8n/lp_reporting_assistant_workflow.json` — the importable n8n workflow, 13 nodes
- `n8n/SETUP.md` — full setup walkthrough (Docker, credentials, running it both ways)
- `docker-compose.yml` — runs n8n self-hosted locally (`docker compose up -d`, http://localhost:5678)
- `frontend/` — React + Vite app for uploading a PDF and viewing the result. `npm install && npm run dev`.
  Vite proxies `/webhook/*` to `http://localhost:5678` (see `frontend/vite.config.js`) so there's no CORS issue.
- `scripts/generate_reports.py` — regenerates the 3 sample PDFs
- `scripts/test_pipeline.py` — standalone script to test the Claude draft/review prompts without n8n
- `docs/Keensight_LP_Reporting_Assistant_Overview.docx` — interview explainer document

## n8n workflow structure

Two entry points feeding the same pipeline:
- **Manual Trigger: New Quarterly Report** → Select Report (sets `filePath`) → Read PDF from Disk → ...
- **Webhook: Report Uploaded** (POST `/webhook/lp-report-upload`, expects `multipart/form-data`
  with the PDF under field name `data`) → ...

Both converge at **Extract from File** → **Parse Report Metadata** (derives companyName/quarterLabel/
reportDate straight from the PDF text — first line, and the "Quarter ended ..." line) →
**Claude 1: Draft + Flag Anomalies** → Parse Draft Response → **Claude 2: Review + Refine for LPs**
→ Parse Final Paragraph → **Copy LP Update Template** (Google Drive, copies a live template doc) →
**Write Paragraph into Google Doc** (HTTP Request calling Google Docs API `batchUpdate` directly,
using `predefinedCredentialType: googleDocsOAuth2Api`) → Output: Doc Link + Paragraph (this is also
the webhook's HTTP response body when triggered via webhook, using `responseMode: lastNode`).

Both Claude nodes are plain HTTP Request nodes calling `https://api.anthropic.com/v1/messages`
directly (not a dedicated Anthropic node), authenticated via a generic "HTTP Header Auth" credential
with header `x-api-key`. Model used for both: `claude-haiku-4-5-20251001`.

The Google Doc template lives in the user's Google Drive (not in this repo):
`LP Update Template — Keensight Capital`, doc ID `1fe38Z4sHGlkAZLp7L4f547oLve-tqOHjjjGJWH0Zybw`.
It has placeholders `{{COMPANY_NAME}}`, `{{QUARTER_LABEL}}`, `{{REPORT_DATE}}`, `{{LP_PARAGRAPH}}`
and a dashed-border box left blank for a logo.

## Current status / where we left off

Built and working so far:
- All 3 dummy PDFs generated and verified (text extracts cleanly)
- n8n running via Docker on the user's Mac, workflow imported
- Anthropic credential connected (no warnings on either Claude node)
- Google Drive + Google Docs OAuth2 credentials connected (had to: add user as a test user on the
  OAuth consent screen since the app is in "Testing" publish status; reset the Client Secret at
  one point since Google only shows it once — both n8n credentials were updated with the new secret)
- Frontend scaffolded, builds cleanly, styled minimalist black/white

**Active bug, unresolved:** uploading a PDF via the frontend and clicking "Generate LP Update"
fails with `Could not reach the workflow. Make sure n8n is running and the workflow is active.`
This is the frontend's generic catch-all error for any failed/non-OK fetch response — the real
cause hasn't been isolated yet. Things tried so far: fixed an empty "File Path" field on the
"Read PDF from Disk" node (unrelated to this bug, but was blocking Publish), fixed the Google Docs
OAuth2 credential. The user was about to check the browser Network tab and try Publishing again
when this handoff happened.

**Suggested next debugging steps:**
1. `docker ps` and `docker logs lp-reporting-assistant-n8n` — confirm the container is healthy.
2. Confirm the workflow shows as actually Active/Published in the n8n UI (not just saved).
3. `curl -X POST http://localhost:5678/webhook/lp-report-upload -F "data=@reports/Solvex_Diagnostics_Q2_2026_Report.pdf"`
   directly from the terminal — this isolates whether the problem is n8n/the workflow itself, or
   the frontend/Vite proxy. If this curl works and returns JSON, the bug is frontend-side (proxy
   config, or the dev server needs restarting since `vite.config.js` was edited after a previous
   `npm run dev` may have already been running).
4. If curl also fails, check the n8n Executions tab for a failed run and read the error on
   whichever node it stopped at.
5. Watch for n8n's test-vs-production webhook URL distinction — the production path (`/webhook/...`)
   only listens while the workflow is Active; the test path (`/webhook-test/...`) only listens
   while you're actively watching the canvas after clicking "Execute workflow".

## Git / GitHub

Local repo has a clean commit history; remote is `https://github.com/JericoNeil/LP-Reporting-Prototype.git`
on branch `main`. The user pushes manually (`git push`) — don't assume push credentials are available.

## Constraints to keep in mind

- Framing: this is a "two-step AI workflow" or "lightweight agentic pipeline" — never describe it
  as a multi-agent or autonomous system, in code comments, docs, or anything user-facing.
- Cost: both Claude calls use the cheapest current model (`claude-haiku-4-5-20251001`) deliberately —
  don't silently upgrade the model without the user asking.
- The user has an interview coming up soon and wants this working and rehearsed, not just "correct
  in theory" — prioritize getting a real, verified end-to-end run over further architecture changes.
