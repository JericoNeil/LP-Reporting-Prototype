# LP Reporting Assistant — Setup Guide

A two-step AI workflow (not a multi-agent system) that turns a raw quarterly portfolio company PDF into a polished LP update paragraph, written directly into a branded Google Doc.

## 1. Run n8n locally via Docker

```bash
docker compose up -d
```

Then open http://localhost:5678 and complete the first-run owner setup.

The `reports/` folder (three dummy quarterly PDFs) is mounted read-only into the container at `/data/reports`, which is what the workflow's file paths point to.

## 2. Import the workflow

In n8n: **Workflows > Import from File** → select `lp_reporting_assistant_workflow.json`.

## 3. Set up credentials

**Anthropic API key**
- Credential type: *HTTP Header Auth*
- Name: `Anthropic API Key (x-api-key)`
- Header name: `x-api-key`
- Header value: your Anthropic API key (starts `sk-ant-...`)

**Google Drive OAuth2** and **Google Docs OAuth2**
- Create a Google Cloud OAuth 2.0 Client (same client works for both credential types in n8n)
- Enable the Google Drive API and Google Docs API on that project
- Add both `https://www.googleapis.com/auth/drive` and `https://www.googleapis.com/auth/documents` scopes
- In n8n, create a *Google Drive OAuth2 API* credential and a *Google Docs OAuth2 API* credential using the same Client ID/Secret, and connect both to your Google account

Attach these three credentials to the corresponding nodes (they're already named/labelled in the workflow — n8n will prompt you to select a credential for each on first open).

## 4. Point the workflow at the template Google Doc

The workflow's **Copy LP Update Template** node already references a live template document:
`LP Update Template — Keensight Capital`
https://docs.google.com/document/d/1fe38Z4sHGlkAZLp7L4f547oLve-tqOHjjjGJWH0Zybw/edit

If you'd rather use your own copy, duplicate that doc (or build your own from the same placeholders below), then update the `fileId` in the **Copy LP Update Template** node to your doc's ID.

Template placeholders the workflow fills in automatically:
- `{{COMPANY_NAME}}`
- `{{QUARTER_LABEL}}`
- `{{REPORT_DATE}}`
- `{{LP_PARAGRAPH}}`

A dashed-border box at the top of the template is left blank for the Keensight Capital logo — insert that manually.

## 5. Run it

1. Open the workflow in n8n.
2. In the **Select Report** node, confirm/edit `filePath` to point at one of:
   - `/data/reports/NexoraCloud_Q2_2026_Report.pdf`
   - `/data/reports/Solvex_Diagnostics_Q2_2026_Report.pdf`
   - `/data/reports/Kestrel_Data_Systems_Q2_2026_Report.pdf`
3. Click **Execute Workflow**.
4. Open the new Google Doc created by the final node (its URL is in the last node's output, `googleDocUrl`).

## 6. Cost

Both Claude steps use `claude-haiku-4-5-20251001` — the cheapest current model. A full run (draft + review on one ~1-page report) costs a small fraction of a cent; testing all three sample reports repeatedly should stay well under $1.

## Optional: test the prompts standalone (no n8n needed)

```bash
pip install pdfplumber
export ANTHROPIC_API_KEY=sk-ant-...
python3 scripts/test_pipeline.py
```

This runs the exact same draft → review prompts against all three sample PDFs and prints the output, useful for sanity-checking wording before demoing inside n8n.
