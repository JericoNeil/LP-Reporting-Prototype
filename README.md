# LP Reporting Assistant

## What this is

Private equity and venture funds send their investors ("Limited Partners," or LPs) a written update every quarter on how each company in their portfolio is doing — revenue, profit, headcount, and a short note on anything notable that happened. Right now, someone has to read the raw report from each company and manually write that update paragraph, for every company, every quarter.

This project automates the first draft of that process. You give it a company's quarterly report (a PDF), and it produces a short, polished update paragraph — ready for a person to review and send. It does not send anything on its own, and it does not decide anything on its own. It just does the tedious first pass so a human can focus on checking and approving instead of writing from scratch.

**In one sentence:** a two-step AI assistant that turns a raw quarterly report into a draft investor update, with a person always reviewing the result before it goes out.

## How it works, step by step

1. **You start it** by clicking a button (this stands in for "a new quarterly report just came in").
2. **It reads the PDF** — a real quarterly report from one company.
3. **It converts the PDF to plain text**, which is a quick, low-cost step that makes the next part cheaper and faster.
4. **An AI model reads that text and writes a first draft** of the update paragraph, and flags anything that looks unusual (like slower growth than usual, or a delayed product launch) so it doesn't get glossed over.
5. **A second AI pass reviews that draft** and tightens it up: no exaggeration, no guessing about the future, just the facts, written in a plain and professional tone appropriate for sending to investors.
6. **The finished paragraph is placed into a nicely formatted document**, with a blank space left at the top for a company logo to be added by hand.

This is a two-step AI workflow, not an autonomous system — it drafts, a person reviews, a person sends. Nothing here makes decisions or takes action on its own.

## What's in this folder

| Folder / file | In plain terms |
|---|---|
| `reports/` | 3 made-up sample quarterly reports (PDFs), used to test the assistant |
| `n8n/` | The actual automation, built in a tool called n8n, plus setup instructions |
| `docker-compose.yml` | One command to run the automation tool on your own computer, for free |
| `scripts/generate_reports.py` | Recreates the 3 sample PDFs if needed |
| `scripts/test_pipeline.py` | Lets you test the AI writing steps directly, without opening the automation tool |
| `docs/` | A longer write-up explaining the project and how it could be used |

The finished output document lives in Google Docs (not in this folder) — see `n8n/SETUP.md` for the link and for full setup steps.

## How to run it

```bash
docker compose up -d
open http://localhost:5678
```

Then follow the instructions in `n8n/SETUP.md` to load the automation, connect it to an AI account and a Google account, and run it.

## Cost

The AI steps use the smallest, cheapest current model available. Each run costs a small fraction of a cent — testing this repeatedly costs well under a dollar in total.
