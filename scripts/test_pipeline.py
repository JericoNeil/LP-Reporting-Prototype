import os, sys, json, urllib.request
import pdfplumber

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    print("No ANTHROPIC_API_KEY env var set")
    sys.exit(1)

MODEL = "claude-haiku-4-5-20251001"

DRAFT_SYSTEM = """You are a financial analyst supporting the investor relations team at a European growth buyout private equity firm. You will be given the extracted text of one portfolio company's quarterly report.

Do two things:
1. Identify any KPI or development that looks unusual and may warrant investor attention. Use these as guidance, not hard rules: revenue growth (YoY) below 10%, any EBITDA margin decline of more than 2 percentage points, recurring revenue/ARR growth below 15%, or any explicitly mentioned delay, cancellation, cost pressure, or other negative qualitative development.
2. Draft a short paragraph (120-180 words) as a FIRST DRAFT of a limited partner (LP) quarterly update for this single portfolio company. Include the most important KPIs and the key qualitative development. If you identified unusual items in step 1, state them directly and factually - do not hide, soften, or omit them, but do not editorialize or speculate about causes or outcomes beyond what the source text states.

Output format: return ONLY the draft paragraph. No preamble, no headers, no markdown, no the word "Draft"."""

REVIEW_SYSTEM = """You are an editor at a European growth buyout private equity firm, reviewing a draft limited partner (LP) quarterly update paragraph before it is sent to institutional investors. You are given the original source report text and a first draft paragraph. Revise the draft according to these rules:

1. Factual only - every claim must be directly traceable to the source text provided. Remove or rephrase anything that reads as speculation, forecast, or opinion not grounded in the source.
2. No promotional or marketing language (avoid words like "exciting", "thrilled", "game-changing", "best-in-class", "robust success"). Use neutral, institutional language.
3. No speculative language about future outcomes (avoid phrases like "is expected to significantly boost X" unless the source explicitly states that expectation).
4. Keep it concise: exactly one paragraph, 100-160 words.
5. Tone: measured, precise, and understated - appropriate for a sophisticated institutional LP audience at a European growth buyout fund. This is a factual update, not marketing collateral.

Return ONLY the final revised paragraph. No preamble, no headers, no markdown, no notes about what you changed."""


def call_claude(system, user_content, max_tokens=500):
    body = json.dumps({
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user_content}]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    usage = data.get("usage", {})
    return data["content"][0]["text"], usage


pdfs = [
    "pdfs/NexoraCloud_Q2_2026_Report.pdf",
    "pdfs/Solvex_Diagnostics_Q2_2026_Report.pdf",
    "pdfs/Kestrel_Data_Systems_Q2_2026_Report.pdf",
]

total_in, total_out = 0, 0

for pdf_path in pdfs:
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

    print("=" * 80)
    print(pdf_path)
    print("-" * 80)

    draft, u1 = call_claude(DRAFT_SYSTEM, "Source report text:\n\n" + text)
    print("DRAFT:\n", draft)
    total_in += u1.get("input_tokens", 0)
    total_out += u1.get("output_tokens", 0)

    final, u2 = call_claude(
        REVIEW_SYSTEM,
        "Source report text:\n\n" + text + "\n\n---\n\nDraft paragraph to review:\n\n" + draft
    )
    print("\nFINAL:\n", final)
    total_in += u2.get("input_tokens", 0)
    total_out += u2.get("output_tokens", 0)
    print()

print("=" * 80)
print(f"Total tokens: input={total_in} output={total_out}")
# Haiku 4.5 approx pricing: $1/MTok in, $5/MTok out (example order of magnitude)
est_cost = (total_in / 1_000_000) * 1.0 + (total_out / 1_000_000) * 5.0
print(f"Estimated cost for this test run: ${est_cost:.4f}")
