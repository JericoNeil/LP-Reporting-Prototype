# LP Reporting Assistant

A working prototype built for the AI Intern / AI Deployment Strategist interview at Keensight Capital.

**What it is:** a two-step AI workflow (drafting + review — not a multi-agent system) in n8n that takes a raw quarterly portfolio company report (PDF) and produces a polished, LP-appropriate update paragraph, written automatically into a branded Google Doc.

## Contents

| Path | What it is |
|---|---|
| `reports/` | 3 fictional quarterly report PDFs (dummy dataset), for fictional Tech/Healthcare companies matching Keensight's investment thesis |
| `n8n/lp_reporting_assistant_workflow.json` | The importable n8n workflow |
| `n8n/SETUP.md` | Step-by-step setup: Docker, credentials, import, run |
| `docker-compose.yml` | Runs n8n self-hosted, locally, for free |
| `scripts/generate_reports.py` | Regenerates the 3 dummy PDFs |
| `scripts/test_pipeline.py` | Standalone script to test the Claude prompts outside of n8n |
| `docs/` | Word document explaining the project for the interview |

The Google Doc output template (Keensight-styled, with a logo placeholder) lives in Google Drive, not in this repo — see `n8n/SETUP.md` for the link.

## Quick start

```bash
docker compose up -d
open http://localhost:5678
```

Then follow `n8n/SETUP.md` to import the workflow, add credentials, and run it.

## Workflow shape

1. **Trigger** — manual "Execute Workflow" button (simulates a new quarterly report arriving)
2. **Data source** — one of the 3 dummy PDFs
3. **Extract from File** — converts PDF to plain text before it reaches Claude, to keep token usage (and cost) low
4. **Claude, step 1 (draft)** — flags unusual KPIs (e.g. revenue growth under 10%, EBITDA margin drop) and drafts a short LP-update paragraph
5. **Claude, step 2 (review)** — refines the draft against a fixed rule set: factual only, no speculative language, no promotional tone, appropriate for an LP audience
6. **Output** — final paragraph written into a Google Doc styled to Keensight's minimalist black-and-white, institutional aesthetic

Both Claude steps currently use `claude-haiku-4-5-20251001` (cheapest current model) — total cost per run is a small fraction of a cent.

This is a lightweight, two-step AI pipeline with a human in the loop before anything reaches an LP — not an autonomous multi-agent system.
