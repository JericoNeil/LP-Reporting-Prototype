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

## 5. Run it — two ways

The workflow has two entry points that both run the same draft → review → Google Doc pipeline.

**A. Manual button, inside n8n** (quick sanity check / fallback if the frontend has issues)
1. Open the workflow in n8n.
2. In the **Select Report** node, confirm/edit `filePath` to point at one of:
   - `/data/reports/NexoraCloud_Q2_2026_Report.pdf`
   - `/data/reports/Solvex_Diagnostics_Q2_2026_Report.pdf`
   - `/data/reports/Kestrel_Data_Systems_Q2_2026_Report.pdf`
3. Click **Execute Workflow**.
4. Open the new Google Doc created by the final node (its URL is in the last node's output, `googleDocUrl`).

**B. Upload from the web frontend** (the demo-ready version — see `frontend/README` below)
1. In n8n, make sure the workflow is switched **Active** (top-right toggle) — the webhook only listens while the workflow is active, not just open.
2. Start the frontend (see "Running the frontend" below) and upload any of the sample PDFs (or a real one).

Company name, reporting quarter, and report date are read automatically from the PDF's own text (first line, and the "Quarter ended ..." line) — you don't need to type anything in for either path.

## 6. Running the frontend

A small React app (in `frontend/`) lets you upload a PDF in a browser instead of clicking around inside n8n — much better for a live demo.

```bash
cd frontend
npm install
npm run dev
```

Open the URL it prints (typically http://localhost:5173). The dev server proxies requests to `http://localhost:5678` for you, so there's no CORS setup needed — just make sure n8n is running and the workflow is **Active** first.

**How it's wired:** the frontend POSTs the PDF as `multipart/form-data` under a field named `data` to `/webhook/lp-report-upload`, which n8n's Webhook node receives and feeds into the same pipeline as the manual trigger. The response is the same JSON the last node in the workflow outputs: `{ companyName, quarterLabel, finalParagraph, googleDocUrl }`.

If the upload fails with a binary-data error: open the **Webhook: Report Uploaded** node in n8n and check that "Binary Data" is enabled with property name `data` — this option's exact location has shifted slightly across n8n versions, so it's worth a quick look if it doesn't work out of the box.

## 7. Cost

Both Claude steps use `claude-haiku-4-5-20251001` — the cheapest current model. A full run (draft + review on one ~1-page report) costs a small fraction of a cent; testing all three sample reports repeatedly should stay well under $1.

## Optional: test the prompts standalone (no n8n needed)

```bash
pip install pdfplumber
export ANTHROPIC_API_KEY=sk-ant-...
python3 scripts/test_pipeline.py
```

This runs the exact same draft → review prompts against all three sample PDFs and prints the output, useful for sanity-checking wording before demoing inside n8n.
