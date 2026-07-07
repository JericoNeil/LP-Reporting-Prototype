# LP Reporting Assistant

An AI-assisted tool that turns raw quarterly reports from portfolio companies into a single, branded quarterly investor report, automatically drafted, fact-checked, and laid out, with a human always reviewing before anything is sent.

---

## Table of contents

1. [The problem](#1-the-problem)
2. [The solution](#2-the-solution)
3. [What it produces](#3-what-it-produces)
4. [How it works, step by step](#4-how-it-works-step-by-step)
5. [The technology, in plain terms](#5-the-technology-in-plain-terms)
6. [What's in this project](#6-whats-in-this-project)
7. [How to run it](#7-how-to-run-it)
8. [Cost](#8-cost)
9. [Safety: a human is always in the loop](#9-safety-a-human-is-always-in-the-loop)
10. [Limitations of the prototype](#10-limitations-of-the-prototype)
11. [How this could be improved and taken to production](#11-how-this-could-be-improved-and-taken-to-production)
12. [The n8n workflow, node by node](#12-the-n8n-workflow-node-by-node)

---

## 1. The problem

Private equity and growth investors raise money from large institutional investors: pension funds, insurers, endowments, family offices. These backers are called **Limited Partners**, or **LPs**.

Every quarter, the firm owes its LPs an update: how is each company in the portfolio performing? Revenue, profitability, growth, headcount, and a short narrative on anything notable, such as a big new contract, a margin dip, or a delayed product launch.

Today this is largely **manual work**:

- Each portfolio company sends in its own quarterly report. These reports are **inconsistent**: some are 2 pages, some are 10; some have polished tables, some are loose prose; every company formats things differently.
- A member of the investor-relations or performance team has to **read each report end to end**, pull out the numbers that matter, notice anything unusual, and **write a clean, neutral paragraph** summarizing the quarter.
- They then have to **assemble all of these into one consistent, branded document** to send to LPs.

This is slow, repetitive, and easy to get subtly wrong (a missed anomaly, an inconsistent tone, a number transposed). It's also the kind of work that scales badly: more portfolio companies means proportionally more hours, every single quarter.

## 2. The solution

This prototype automates the **first draft** of that entire process.

You give it the raw quarterly reports (PDFs) from your portfolio companies. It:

1. **Reads and understands each report**, regardless of length or layout.
2. **Extracts the key figures**: revenue, margins, growth, segment mix, quarter-over-quarter trends.
3. **Writes a concise, neutral investor-update paragraph** for each company.
4. **Automatically flags anomalies** worth an investor's attention (e.g. growth slowing below a threshold, a margin drop, a delayed launch).
5. **Compiles everything into one branded quarterly document**: a cover page and firm introduction, followed by one clean page per company with tables, charts, and colour-coded status flags.

Crucially, it **does not send anything and does not make decisions**. It produces a polished draft so a human can spend their time *reviewing and approving* instead of *writing from a blank page*.

**In one sentence:** upload each company's raw report, and get back one professional, fact-checked quarterly LP report, ready for human review.

## 3. What it produces

The output is a single **Google Doc** per quarter, built on the firm's own investor-report template:

- **Page 1, Cover.** The firm's "Investor Report" cover with logo and branding.
- **Page 2, Firm introduction.** The firm's mission, investment philosophy, key metrics, value-creation approach, and recent investment activity.
- **One page per portfolio company**, each containing:
  - A short, reviewed narrative summarising the quarter.
  - A **key-metrics table** (this quarter vs. prior quarter vs. change).
  - **Charts**: revenue trend, EBITDA-margin trend, and revenue-by-segment.
  - A **watch-items table** with colour-coded status: green (**On Track**), amber (**Monitor**), red (**Attention**), so anomalies jump off the page.

Every quarter you process gets its own dated folder and document, and running additional companies for the same quarter appends them to the same report.

## 4. How it works, step by step

When a report comes in (either uploaded through the web app or dropped into the workflow), it flows through these stages:

1. **Intake.** The PDF arrives, either via the web page or the automation's built-in trigger.
2. **Text extraction.** The PDF is converted to plain text, a fast, essentially free step that makes everything downstream cheaper and more reliable than sending an image to an AI model.
3. **Metadata parsing.** The tool figures out *which company* this is and *which quarter* it covers, straight from the report's own text.
4. **AI Pass 1, Draft and extract.** An AI model (Claude) reads the full report and returns a structured result: a first-draft update paragraph, the key metrics, the multi-quarter trends, the revenue-by-segment breakdown, and a set of watch items, explicitly flagging anything unusual so it can't get glossed over.
5. **AI Pass 2, Review and refine.** A second AI pass acts as an editor: it removes any speculation or promotional language, checks that every claim traces back to the source report, and tightens the paragraph to a measured, institutional tone.
6. **Assemble the document.** The tool copies the firm's template (cover and intro come through untouched), then writes the company's section: narrative, metrics table, charts (rendered as images), and the colour-coded watch-items table, all in the firm's typeface.
7. **Deliver.** You get a link to the finished Google Doc.

This is deliberately a **two-step AI workflow** (draft, then review), *not* an autonomous agent. It drafts; a person reviews; a person sends.

## 5. The technology, in plain terms

You don't need to be technical to follow what's under the hood. Each piece was chosen to be reliable, low-cost, and easy to run:

| Component | What it is | Why it's used |
|---|---|---|
| **n8n** | A visual "automation builder" where you connect boxes (read a file, call an AI, write to a document) into a flow. | Lets the whole pipeline be built, seen, and edited visually, with no heavy custom software to maintain. Runs free on your own computer. |
| **Claude (Anthropic)** | The AI model that reads reports and writes the drafts. | Strong at reading long, messy documents and writing in a precise, controllable tone. The prototype uses the smallest, cheapest current model on purpose. |
| **Google Docs & Drive** | Where the finished report is created and stored. | Everyone already uses it; the output is instantly editable and shareable, and the firm's real template lives there. |
| **QuickChart** | A charting service that turns numbers into chart images. | Produces clean trend and bar charts that can be dropped straight into the document. |
| **React + Vite** | The technology behind the simple upload web page. | Gives a clean, friendly front door for the demo instead of working inside the automation tool. |
| **Docker** | A way to run the automation tool on any computer with one command. | No complicated install, `docker compose up` and it's running. |
| **Python (ReportLab)** | A small script that generates the sample portfolio-company reports. | Creates realistic, varied test data (2 to 10 page reports) to demonstrate the tool. |

## 6. What's in this project

| Folder / file | In plain terms |
|---|---|
| `frontend/` | The simple web page where you add the PDFs and click "Generate quarterly report." |
| `n8n/` | The automation itself, plus a full setup walkthrough (`n8n/SETUP.md`). |
| `reports/` | Three made-up portfolio-company reports (NexoraCloud, Solvex Diagnostics, Kestrel Data Systems) used to demo the tool. |
| `scripts/generate_reports.py` | Recreates those three sample reports. |
| `scripts/test_pipeline.py` | Lets you test the AI drafting steps directly, without opening the automation tool. |
| `docs/` | A detailed use-case write-up of the project (problem, solution, architecture, production path). |
| `docker-compose.yml` | Runs the automation tool locally with one command. |

## 7. How to run it

**Start the automation tool:**

```bash
docker compose up -d
```

**Open the web app** (from the `frontend/` folder):

```bash
npm install
npm run dev
```

Then open the address it prints (usually `http://localhost:5173`), click **"Load all 3 sample reports"** (or drag in your own PDFs), and click **"Generate quarterly report."** You'll get a link to the finished document.

Full setup, connecting the AI account and Google account, importing the automation, is in **`n8n/SETUP.md`**.

## 8. Cost

The AI steps deliberately use the smallest, cheapest current model. A full run for several companies costs a **small fraction of a cent**; the entire prototype was built and tested for well under a dollar. The automation tool, the web app, and running it locally are all **free and open-source**.

## 9. Safety: a human is always in the loop

This is a drafting assistant, not an autonomous system. By design:

- It **never sends** anything to LPs; it only produces a draft document.
- It **never makes investment or disclosure decisions**.
- The second AI pass is specifically instructed to **stick to the facts in the source report**: no speculation, no forecasts, no marketing language.
- Every anomaly is **surfaced, not hidden**, so a reviewer sees exactly what to double-check.

A person reviews and approves the document before it ever reaches an investor.

## 10. Limitations of the prototype

Being honest about where this is a prototype rather than a finished product:

- **Reports are appended, not deduplicated.** If two reports for the same quarter are submitted within a few seconds of each other, a cloud-storage indexing delay can occasionally create two documents instead of one. Processing them one at a time (as the web app does) avoids this.
- **The logo and template live in one person's Google Drive.** In production these would live in a shared, governed location.
- **Charts depend on an external charting service.** Fine for a prototype; a production version would generate them in-house.
- **No login, audit trail, or access controls yet.** Appropriate for a demo, essential for production.
- **AI output always needs human review.** The tool is designed around that assumption, not despite it.

## 11. How this could be improved and taken to production

This prototype proves the concept. A production version could add:

**Reliability & scale**
- A proper database record of every report processed, with versioning and an audit trail.
- Guaranteed one-document-per-quarter behaviour (removing the indexing-delay edge case).
- Batch processing of an entire portfolio in one go, with automatic retries.

**Trust & governance**
- User accounts, permissions, and a full log of who generated and approved what.
- A side-by-side "source vs. draft" review screen so a reviewer can verify every figure against the original report in one click.
- Automated checks that every number in the draft appears in the source document.

**Capability**
- Deeper anomaly detection tuned to the firm's own thresholds and sectors.
- Trend commentary across multiple quarters, not just the current one.
- Support for more input formats (Excel, scanned documents, data-room exports).
- Direct, governed publishing into the firm's existing LP portal or data room.

**Cost & control**
- Self-hosted charting and document rendering, removing external dependencies.
- Model choice tuned per step: a cheaper model for extraction, a stronger one for the final review.

**In short:** the hard part, reliably turning messy, varied reports into a clean, fact-checked, branded quarterly report, already works. The path to production is mostly about governance, reliability, and integration with the firm's existing systems.

## 12. The n8n workflow, node by node

Section 4 described the pipeline in plain terms. This section walks through the actual automation (`n8n/lp_reporting_assistant_workflow.json`), which is organized into five stages left to right, each marked with an on-canvas note so it can be read like a diagram during a demo.

**Stage 1: Intake.** The workflow has two possible starting points. `Manual Trigger: New Quarterly Report` → `Select Report` → `Read PDF from Disk` is used for local testing: it picks a PDF that's already sitting on disk. `Webhook: Report Uploaded` is the path the frontend actually uses: it listens on `POST /webhook/lp-report-upload` and receives a PDF as `multipart/form-data`. Both paths feed into `Extract from File`, which converts the PDF into plain text. Doing this conversion once, up front, keeps every downstream step working with cheap text instead of an image.

**Stage 2: Metadata and two-step AI drafting.** `Parse Report Metadata` is a small script that reads the company name and the reporting quarter straight out of the extracted text (no manual data entry needed). `Claude 1: Draft + Flag Anomalies` then reads the full report and returns a structured result: a first-draft update paragraph, a key-metrics table, revenue and margin trends, the revenue-by-segment split, and a list of watch items worth an investor's attention. `Parse Draft Response` turns that into a clean object the rest of the workflow can use. `Claude 2: Review + Refine for LPs` then acts purely as an editor on the narrative paragraph: it removes speculation and promotional language, checks every claim against the source report, and tightens the tone. `Parse Final Paragraph` extracts the reviewed text, and `Build Section Content` turns the whole structured result into the QuickChart URLs and text blocks the document itself needs.

**Stage 3: Drive folder structure.** This stage keeps every quarter's output in one predictable place. `Find Keensight Parent Folder` looks for the top-level folder in Drive; `Parent Folder Exists?` branches into `Create Keensight Parent Folder` the first time only. `Normalize Parent Folder Id` reconciles the two branches back into one value, and the same find-or-create pattern repeats one level down for the dated quarter subfolder (`Find Quarter Folder` → `Folder Exists?` → `Create Quarter Folder` → `Normalize Folder Id`).

**Stage 4: Quarterly document lookup.** `Find Quarter Doc` checks whether a Google Doc already exists for this quarter. `Doc Exists?` branches: if not, `Create Quarter Doc from Template` copies the firm's real investor-report template into the quarter folder, preserving the cover page and firm introduction exactly as they are. `Normalize Doc Id` merges the two branches, and `Is New Doc?` decides which write path runs next, since a brand-new document needs its section written differently from one that already has other companies in it.

**Stage 5: Write, style, and output.** `Write Section: First Company (Template)` writes directly into the fresh template copy; `Write Section: Append Company` inserts a page break and writes into a document that already has content. Both converge at `Get Document`. Styling then runs in two passes, which turned out to be necessary because filling text into one table shifts the character indices of every table after it: pass one (`Compute Cell Fills` → `Apply Cell Fills`) writes plain text into every table cell only; the document is then re-fetched (`Get Document 2`) so all indices are known and settled, and pass two (`Compute Styles` → `Apply Styles`) applies fonts, colours, bold, and bullet-style resets against that settled document. `Output: Doc Link + Paragraph` returns the finished document link and the reviewed paragraph, which is also what the webhook sends back to the frontend.

---

*This is a demonstration prototype. All portfolio companies, figures, and events in the sample data are fictional. The tool produces drafts for human review and does not send communications or make decisions on its own.*
