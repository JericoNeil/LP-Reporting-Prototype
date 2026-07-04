"""
Generates 3 fictional quarterly portfolio-company reports (PDF) for the
LP Reporting Assistant demo. All companies, figures, and people are fictional.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=18, leading=22, textColor=colors.HexColor("#111111"), spaceAfter=2,
)
sub_style = ParagraphStyle(
    "SubCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, textColor=colors.HexColor("#555555"), spaceAfter=14,
)
h2_style = ParagraphStyle(
    "H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, textColor=colors.HexColor("#111111"), spaceBefore=14, spaceAfter=6,
)
body_style = ParagraphStyle(
    "BodyCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=15, textColor=colors.HexColor("#222222"),
)
label_style = ParagraphStyle(
    "LabelCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9, textColor=colors.HexColor("#777777"),
)


def kpi_table(rows):
    data = [["KPI", "Q2 2026", "Q1 2026", "YoY (Q2'25 -> Q2'26)"]] + rows
    t = Table(data, colWidths=[55 * mm, 32 * mm, 32 * mm, 45 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111111")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F4F4")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def build_report(filename, company, sector, hq, report_date, kpi_rows, narrative_paras, footer_note):
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        topMargin=22 * mm, bottomMargin=20 * mm, leftMargin=20 * mm, rightMargin=20 * mm,
    )
    story = []
    story.append(Paragraph(company, title_style))
    story.append(Paragraph(f"{sector} &nbsp;|&nbsp; HQ: {hq} &nbsp;|&nbsp; Quarterly Portfolio Report &nbsp;|&nbsp; {report_date}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#111111")))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Performance Indicators", h2_style))
    story.append(kpi_table(kpi_rows))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Business Update", h2_style))
    for p in narrative_paras:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(footer_note, label_style))
    story.append(Paragraph(
        "This is a fictional document prepared for internal demonstration purposes only. "
        "Company names, figures, and events are illustrative and do not represent real entities.",
        label_style
    ))

    doc.build(story)
    print(f"Wrote {filename}")


# ---------------------------------------------------------------------------
# 1. NexoraCloud — Tech / Vertical SaaS (healthy quarter, clean narrative)
# ---------------------------------------------------------------------------
build_report(
    "NexoraCloud_Q2_2026_Report.pdf",
    "NexoraCloud",
    "Sector: Enterprise Software (Vertical SaaS for Mid-Market Manufacturers)",
    "Lyon, France",
    "Quarter ended 30 June 2026",
    [
        ["Revenue", "EUR 42.5M", "EUR 39.8M", "+18.4%"],
        ["ARR", "EUR 168.2M", "EUR 158.6M", "+21.3%"],
        ["EBITDA", "EUR 9.4M", "EUR 8.3M", "+24.1%"],
        ["EBITDA Margin", "22.1%", "20.9%", "+1.6 pts"],
        ["Headcount (FTE)", "312", "298", "+9.5%"],
        ["Net Revenue Retention", "118%", "116%", "+3 pts"],
    ],
    [
        "NexoraCloud delivered a strong second quarter, with revenue growth accelerating on the back of "
        "continued momentum in the mid-market manufacturing vertical. ARR growth of 21.3% year-over-year "
        "was driven by both new logo acquisition and expansion within the existing customer base, reflected "
        "in a net revenue retention rate of 118%.",

        "The quarter's standout event was the signing of a multi-year enterprise agreement with a major "
        "European retail supply chain group, representing the company's largest single contract to date. "
        "Implementation is expected to begin in Q3 2026, with initial revenue recognition starting in Q4.",

        "The company also opened a small sales and customer success presence in Warsaw to support growing "
        "demand in Central and Eastern Europe, adding 14 net new hires across product and go-to-market "
        "functions during the quarter. Management reaffirmed full-year guidance and noted no material "
        "changes to the competitive landscape.",
    ],
    "Prepared by: NexoraCloud Finance Team | Distribution: Board and Investors | Confidential",
)


# ---------------------------------------------------------------------------
# 2. Solvex Diagnostics — Healthcare / IVD devices (flag-worthy quarter)
# ---------------------------------------------------------------------------
build_report(
    "Solvex_Diagnostics_Q2_2026_Report.pdf",
    "Solvex Diagnostics",
    "Sector: Healthcare (In-Vitro Diagnostics & Lab Equipment)",
    "Barcelona, Spain",
    "Quarter ended 30 June 2026",
    [
        ["Revenue", "EUR 84.6M", "EUR 82.9M", "+6.1%"],
        ["Recurring Consumables Revenue", "EUR 51.2M", "EUR 50.1M", "+7.4%"],
        ["EBITDA", "EUR 16.1M", "EUR 18.7M", "-9.2%"],
        ["EBITDA Margin", "19.0%", "22.6%", "-3.6 pts"],
        ["Headcount (FTE)", "540", "536", "+1.9%"],
        ["Backlog (Equipment Orders)", "EUR 12.3M", "EUR 15.8M", "-14.0%"],
    ],
    [
        "Solvex Diagnostics recorded revenue growth of 6.1% year-over-year in Q2 2026, a deceleration "
        "from the 14-16% growth rates achieved over the prior four quarters. Growth in the recurring "
        "consumables business remained comparatively resilient at 7.4%, while capital equipment orders "
        "softened amid longer procurement cycles among European hospital networks.",

        "EBITDA margin declined by 3.6 points to 19.0%, reflecting higher input costs for reagent "
        "components and increased freight expenses that were not yet offset by the pricing adjustments "
        "implemented in May 2026. Management expects the full benefit of these price increases to be "
        "reflected from Q4 2026 onward.",

        "The company confirmed that its next-generation rapid diagnostic panel, originally targeted for "
        "a Q3 2026 launch, has been delayed by approximately two quarters pending completion of an "
        "additional clinical validation study requested by the notified body. Management does not expect "
        "the delay to affect existing product lines or the current revenue base, and has not changed "
        "full-year guidance at this time, though it noted the timeline carries some uncertainty pending "
        "the outcome of the validation study.",
    ],
    "Prepared by: Solvex Diagnostics Finance Team | Distribution: Board and Investors | Confidential",
)


# ---------------------------------------------------------------------------
# 3. Kestrel Data Systems — Tech / Cybersecurity SaaS (small, high-growth)
# ---------------------------------------------------------------------------
build_report(
    "Kestrel_Data_Systems_Q2_2026_Report.pdf",
    "Kestrel Data Systems",
    "Sector: Cybersecurity & Data Infrastructure Software",
    "Amsterdam, Netherlands",
    "Quarter ended 30 June 2026",
    [
        ["Revenue", "EUR 18.9M", "EUR 16.7M", "+31.7%"],
        ["ARR", "EUR 71.4M", "EUR 63.8M", "+34.5%"],
        ["EBITDA", "EUR 1.8M", "EUR 1.1M", "+63.6%"],
        ["EBITDA Margin", "9.5%", "6.6%", "+2.9 pts"],
        ["Headcount (FTE)", "146", "128", "+14.1%"],
        ["Net Revenue Retention", "129%", "124%", "+5 pts"],
    ],
    [
        "Kestrel Data Systems posted another quarter of high growth, with ARR increasing 34.5% year-over-year "
        "and EBITDA margin turning further positive as the business continues to scale efficiently. Net "
        "revenue retention of 129% reflects strong upsell into existing accounts as customers expand their "
        "data protection footprint.",

        "The quarter's key development was the general availability launch of the company's managed data "
        "loss prevention module, which shipped on schedule and has already been adopted by roughly a "
        "quarter of the existing customer base within its first six weeks. Management highlighted early "
        "cross-sell traction as a positive signal for the module's contribution to ARR in the second half "
        "of the year.",

        "Headcount grew 14.1% quarter-over-quarter, concentrated in engineering and security research roles "
        "to support the expanded product roadmap. The company also renewed its cyber-insurance partnership "
        "and reported no material security incidents during the quarter.",
    ],
    "Prepared by: Kestrel Data Systems Finance Team | Distribution: Board and Investors | Confidential",
)
