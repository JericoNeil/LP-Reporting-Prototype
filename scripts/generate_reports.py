"""
Generates 3 fictional quarterly portfolio-company reports (PDF) for the
LP Reporting Assistant demo. All companies, figures, and people are fictional.

These are the RAW reports a portfolio company sends in to its sponsor each
quarter -- intentionally varied in length (2-6 pages) and structure between
companies, since real companies don't standardize their own reporting. The
Keensight pipeline's job is to read these messy/varied inputs and produce a
clean, standardized one-page LP update per company (see the n8n workflow).
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)

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


def data_table(header, rows, col_widths):
    data = [header] + rows
    t = Table(data, colWidths=col_widths)
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


def kpi_table(rows):
    return data_table(
        ["KPI", "This Quarter", "Prior Quarter", "YoY"],
        rows, [55 * mm, 32 * mm, 32 * mm, 45 * mm],
    )


def cover_page(company, sector, hq, report_date, kpi_rows, narrative_paras, footer_note):
    story = [
        Paragraph(company, title_style),
        Paragraph(f"{sector} &nbsp;|&nbsp; HQ: {hq} &nbsp;|&nbsp; Quarterly Report to Sponsor &nbsp;|&nbsp; {report_date}", sub_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#111111")),
        Spacer(1, 10),
        Paragraph("Key Performance Indicators", h2_style),
        kpi_table(kpi_rows),
        Spacer(1, 6),
        Paragraph("Business Update", h2_style),
    ]
    for p in narrative_paras:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 6))
    return story


def filler_section(title, paragraphs):
    story = [Paragraph(title, h2_style)]
    for p in paragraphs:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 6))
    return story


def footer_block(footer_note):
    return [
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC")),
        Spacer(1, 6),
        Paragraph(footer_note, label_style),
        Paragraph(
            "This is a fictional document prepared for internal demonstration purposes only. "
            "Company names, figures, and events are illustrative and do not represent real entities.",
            label_style
        ),
    ]


def build(filename, story):
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        topMargin=22 * mm, bottomMargin=20 * mm, leftMargin=20 * mm, rightMargin=20 * mm,
    )
    doc.build(story)
    print(f"Wrote {filename}")


# ---------------------------------------------------------------------------
# 1. NexoraCloud - Tech / Vertical SaaS (healthy quarter, clean narrative)
#    3 pages: cover + KPIs/narrative, then a trend + product appendix.
# ---------------------------------------------------------------------------
story = cover_page(
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
story.append(PageBreak())
story.extend(filler_section("Company Overview", [
    "NexoraCloud was founded in 2016 to serve the digital transformation needs of mid-market "
    "manufacturers across Western and Central Europe. The company's platform provides production "
    "planning, quality management, and supply chain visibility modules delivered as a unified SaaS "
    "suite, with deployment options spanning public cloud, private cloud, and hybrid on-premise "
    "configurations to accommodate customers' data residency requirements.",

    "The company operates from its headquarters in Lyon, France, with satellite offices supporting "
    "regional go-to-market functions. NexoraCloud's leadership team combines enterprise software "
    "veterans with deep domain expertise in discrete and process manufacturing, and the company has "
    "built a reputation for high-touch implementation support that differentiates it from larger, "
    "more horizontally-focused ERP vendors in competitive sales processes.",

    "Since its Series growth investment, the company has expanded its go-to-market motion from a "
    "founder-led sales model to a structured enterprise sales organization, while continuing to invest "
    "meaningfully in product and engineering to extend the platform's capabilities into adjacent "
    "workflows such as supplier risk management and energy consumption tracking.",
]))
story.append(PageBreak())
story.extend(filler_section("Corporate Governance & ESG Update", [
    "The Board of Directors met twice during the quarter, in addition to a dedicated strategy session "
    "held in May 2026 to review the three-year product roadmap. The Audit Committee reviewed quarterly "
    "financial statements and internal control matters in the ordinary course; no material findings "
    "were reported.",

    "On environmental, social, and governance matters, the company continued to track its standard set "
    "of metrics, including employee engagement survey results, gender representation across the "
    "organization, and estimated Scope 2 emissions associated with cloud infrastructure usage. No "
    "material changes to the company's ESG posture occurred during the quarter. The company continued "
    "its participation in a regional apprenticeship program for early-career software engineers, and "
    "renewed its commitment to pro-bono technology support for two local nonprofit organizations in the "
    "Lyon area.",

    "Management notes that these governance and ESG activities are reported for completeness and "
    "transparency and did not have a material impact on financial results during the period.",
]))
story.append(PageBreak())
story.append(Paragraph("Appendix A: Quarterly Trend", h2_style))
story.append(Paragraph(
    "Trailing eight-quarter revenue and EBITDA margin, provided for reference. Figures prior to Q3 2024 "
    "are not tracked on a comparable basis following the FY2024 chart-of-accounts migration.",
    body_style,
))
story.append(Spacer(1, 6))
story.append(data_table(
    ["Quarter", "Revenue (EUR M)", "EBITDA Margin"],
    [
        ["Q3 2024", "30.5", "18.2%"],
        ["Q4 2024", "32.8", "18.9%"],
        ["Q1 2025", "34.0", "19.6%"],
        ["Q2 2025", "35.9", "20.1%"],
        ["Q3 2025", "37.0", "20.4%"],
        ["Q4 2025", "38.5", "20.9%"],
        ["Q1 2026", "39.8", "20.9%"],
        ["Q2 2026", "42.5", "22.1%"],
    ],
    [40 * mm, 45 * mm, 45 * mm],
))
story.append(Spacer(1, 14))
story.append(Paragraph("Appendix B: Revenue by Product Line", h2_style))
story.append(data_table(
    ["Product Line", "Share of Q2 2026 Revenue"],
    [
        ["Core Platform Subscriptions", "68%"],
        ["Add-on Modules", "19%"],
        ["Professional Services", "9%"],
        ["Other", "4%"],
    ],
    [90 * mm, 60 * mm],
))
story.extend(footer_block("Prepared by: NexoraCloud Finance Team | Distribution: Board and Investors | Confidential"))
build("NexoraCloud_Q2_2026_Report.pdf", story)


# ---------------------------------------------------------------------------
# 2. Solvex Diagnostics - Healthcare / IVD devices (flag-worthy quarter)
#    5 pages: cover, regulatory/clinical appendix, financial detail, trend.
# ---------------------------------------------------------------------------
story = cover_page(
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
    ],
    "Prepared by: Solvex Diagnostics Finance Team | Distribution: Board and Investors | Confidential",
)
story.append(PageBreak())
story.extend(filler_section("Company Overview", [
    "Solvex Diagnostics develops and manufactures in-vitro diagnostic instruments and consumables for "
    "hospital and reference laboratories across Europe, with a product portfolio spanning clinical "
    "chemistry, immunoassay, and molecular diagnostics platforms. The company's installed base of "
    "laboratory analyzers generates a recurring stream of consumables revenue that represents the "
    "majority of total revenue in any given period.",

    "Headquartered in Barcelona, Spain, with manufacturing facilities in Spain and Portugal, Solvex "
    "Diagnostics serves customers in over twenty European countries through a combination of direct "
    "sales in core markets and distributor relationships in smaller markets. The company's R&D "
    "organization is focused on expanding the assay menu available on its existing analyzer platforms "
    "and developing next-generation instrument platforms, including the rapid diagnostic panel "
    "discussed elsewhere in this report.",

    "The diagnostics industry operates within a heavily regulated environment, and Solvex Diagnostics "
    "maintains a dedicated regulatory affairs and quality assurance function responsible for managing "
    "relationships with notified bodies and competent authorities across the company's markets.",
]))
story.append(PageBreak())
story.extend(filler_section("ESG & Sustainability Update", [
    "Solvex Diagnostics continued to track its standard ESG metrics during the quarter, including "
    "laboratory safety incident rates, water usage at its manufacturing sites, and packaging waste "
    "associated with consumables shipments. The company's sustainability committee, comprising members "
    "of the operations and quality leadership teams, meets quarterly to review progress against the "
    "company's internal sustainability roadmap.",

    "No material environmental incidents were reported during the quarter. The company continued a "
    "multi-year initiative to reduce single-use plastic packaging across its consumables product lines, "
    "with a pilot program for recyclable reagent cartridges expected to begin in a subset of Spanish "
    "customer sites later in 2026.",
]))
story.append(PageBreak())
story.append(Paragraph("Appendix A: Regulatory & Clinical Update", h2_style))
story.append(Paragraph(
    "The next-generation rapid diagnostic panel, originally targeted for a Q3 2026 launch, has been "
    "delayed by approximately two quarters. The notified body conducting CE-IVD certification requested "
    "an additional clinical validation study following a routine audit of the analytical sensitivity "
    "data package submitted in April 2026. The company does not consider the request to relate to any "
    "safety concern with the existing product line.",
    body_style,
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Management does not expect the delay to affect existing product lines or the current revenue base. "
    "Full-year guidance is unchanged, though the timeline to CE-IVD certification carries some "
    "uncertainty pending the outcome of the validation study, expected to conclude in Q4 2026.",
    body_style,
))
story.append(Spacer(1, 10))
story.append(Paragraph("Regulatory Milestone Tracker", h2_style))
story.append(data_table(
    ["Milestone", "Original Target", "Revised Target", "Status"],
    [
        ["Analytical validation package", "Q1 2026", "Q1 2026", "Complete"],
        ["Notified body review", "Q2 2026", "Q3 2026", "In progress"],
        ["Additional clinical validation study", "n/a", "Q4 2026", "In progress"],
        ["CE-IVD certification", "Q3 2026", "Q1 2027", "Delayed"],
    ],
    [55 * mm, 30 * mm, 30 * mm, 30 * mm],
))
story.append(PageBreak())
story.append(Paragraph("Appendix B: Financial Detail", h2_style))
story.append(Paragraph("Revenue by Segment", h2_style))
story.append(data_table(
    ["Segment", "Share of Q2 2026 Revenue"],
    [
        ["Recurring Consumables", "60.5%"],
        ["Capital Equipment", "29.0%"],
        ["Service & Maintenance", "8.0%"],
        ["Other", "2.5%"],
    ],
    [90 * mm, 60 * mm],
))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "EBITDA margin bridge: the 3.6-point decline versus Q1 2026 is attributable to reagent input cost "
    "inflation (-1.9 pts), higher freight and logistics costs following a carrier contract renewal "
    "(-1.4 pts), and a smaller unfavorable revenue mix shift toward equipment (-0.3 pts).",
    body_style,
))
story.append(PageBreak())
story.append(Paragraph("Appendix C: Quarterly Trend", h2_style))
story.append(data_table(
    ["Quarter", "Revenue (EUR M)", "EBITDA Margin"],
    [
        ["Q3 2024", "64.2", "21.5%"],
        ["Q4 2024", "68.9", "22.0%"],
        ["Q1 2025", "73.5", "22.4%"],
        ["Q2 2025", "79.7", "22.8%"],
        ["Q3 2025", "80.8", "22.7%"],
        ["Q4 2025", "82.1", "22.6%"],
        ["Q1 2026", "82.9", "22.6%"],
        ["Q2 2026", "84.6", "19.0%"],
    ],
    [40 * mm, 45 * mm, 45 * mm],
))
story.extend(footer_block("Prepared by: Solvex Diagnostics Finance Team | Distribution: Board and Investors | Confidential"))
build("Solvex_Diagnostics_Q2_2026_Report.pdf", story)


# ---------------------------------------------------------------------------
# 3. Kestrel Data Systems - Tech / Cybersecurity SaaS (small, high-growth)
#    2 pages: lean report, cover + a brief product/trend appendix.
# ---------------------------------------------------------------------------
story = cover_page(
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
        "quarter of the existing customer base within its first six weeks. Headcount grew 14.1% "
        "quarter-over-quarter, concentrated in engineering and security research roles. The company also "
        "renewed its cyber-insurance partnership and reported no material security incidents during the "
        "quarter.",
    ],
    "Prepared by: Kestrel Data Systems | Distribution: Board and Investors | Confidential",
)
story.append(PageBreak())
story.extend(filler_section("Company Overview", [
    "Kestrel Data Systems provides data loss prevention and data infrastructure security software to "
    "mid-market and enterprise customers, with a particular focus on regulated industries including "
    "financial services and healthcare. The company's platform is delivered as a cloud-native SaaS "
    "product with agent-based endpoint coverage and API-based integrations into customers' existing "
    "identity and data governance tooling.",

    "Founded in Amsterdam in 2019, the company has grown primarily through product-led growth "
    "supplemented by a small enterprise sales team focused on the company's largest accounts. Kestrel "
    "Data Systems has built a reputation in the European cybersecurity community for rapid time-to-value "
    "during customer onboarding relative to legacy data loss prevention vendors.",
]))
story.append(PageBreak())
story.extend(filler_section("Market Context", [
    "The data loss prevention and data security posture management market continues to see elevated "
    "customer interest driven by evolving European data protection regulation and an increasing number "
    "of high-profile data exposure incidents across the region. Management characterizes the "
    "competitive environment as fragmented, with a mix of legacy enterprise security vendors and a "
    "growing set of cloud-native challengers, of which the company considers itself one.",

    "No material changes to the competitive or regulatory landscape were noted during the quarter.",
]))
story.append(PageBreak())
story.append(Paragraph("Product & Growth Detail", h2_style))
story.append(Paragraph(
    "Management highlighted early cross-sell traction for the managed DLP module as a positive signal "
    "for its contribution to ARR in the second half of the year.",
    body_style,
))
story.append(Spacer(1, 8))
story.append(data_table(
    ["Quarter", "Revenue (EUR M)", "EBITDA Margin"],
    [
        ["Q3 2024", "10.8", "2.1%"],
        ["Q4 2024", "12.0", "3.4%"],
        ["Q1 2025", "13.2", "4.8%"],
        ["Q2 2025", "14.3", "5.9%"],
        ["Q3 2025", "15.0", "6.2%"],
        ["Q4 2025", "15.8", "6.6%"],
        ["Q1 2026", "16.7", "6.6%"],
        ["Q2 2026", "18.9", "9.5%"],
    ],
    [40 * mm, 45 * mm, 45 * mm],
))
story.append(Spacer(1, 10))
story.append(data_table(
    ["Revenue Mix", "Share"],
    [
        ["Core Platform Subscriptions", "71%"],
        ["Managed DLP Module", "14%"],
        ["Professional Services", "11%"],
        ["Other", "4%"],
    ],
    [90 * mm, 60 * mm],
))
story.extend(footer_block("Prepared by: Kestrel Data Systems | Distribution: Board and Investors | Confidential"))
build("Kestrel_Data_Systems_Q2_2026_Report.pdf", story)
