from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def clean_pdf_text(text):
    """
    Replace characters that may not display correctly
    with ReportLab's built-in fonts.
    """

    if text is None:
        return ""

    replacements = {
        "—": "-",
        "–": "-",
        "•": "-",
        "✅": "[Matched]",
        "❌": "[Missing]",
        "📌": "-",
        "🚀": "",
        "🤖": "",
        "🎤": "",
        "’": "'",
        "“": '"',
        "”": '"',
    }

    cleaned_text = str(text)

    for original, replacement in replacements.items():
        cleaned_text = cleaned_text.replace(
            original,
            replacement
        )

    return cleaned_text.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")


def add_markdown_text(story, text, styles):
    """
    Convert simple Gemini Markdown text into PDF paragraphs.
    """

    cleaned_text = clean_pdf_text(text)

    for line in cleaned_text.splitlines():
        stripped_line = line.strip()

        if not stripped_line:
            story.append(
                Spacer(1, 8)
            )
            continue

        if stripped_line.startswith("### "):
            story.append(
                Paragraph(
                    escape(stripped_line[4:]),
                    styles["Heading3"]
                )
            )

        elif stripped_line.startswith("## "):
            story.append(
                Paragraph(
                    escape(stripped_line[3:]),
                    styles["Heading2"]
                )
            )

        elif stripped_line.startswith("# "):
            story.append(
                Paragraph(
                    escape(stripped_line[2:]),
                    styles["Heading1"]
                )
            )

        elif stripped_line.startswith(("- ", "* ")):
            story.append(
                Paragraph(
                    "- " + escape(stripped_line[2:]),
                    styles["BodyText"]
                )
            )

        else:
            story.append(
                Paragraph(
                    escape(stripped_line),
                    styles["BodyText"]
                )
            )

        story.append(
            Spacer(1, 5)
        )


def generate_pdf_report(
    job_description,
    match_score,
    ats_result,
    required_skills,
    matched_skills,
    missing_skills,
    ai_advice,
    interview_questions
):
    """
    Generate the complete NextRole AI career report
    and return it as PDF bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="NextRole AI Career Report"
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            leading=28,
            spaceAfter=18
        )
    )

    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 15

    story = []

    # Report title
    story.append(
        Paragraph(
            "NextRole AI Career Analysis Report",
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            "AI-powered job matching, ATS analysis and interview preparation",
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 18)
    )

    # Score summary table
    score_data = [
        ["Analysis", "Score"],
        ["Job Match Score", f"{match_score}%"],
        ["Estimated ATS Score", f"{ats_result['ats_score']}%"],
        ["Keyword Coverage", f"{ats_result['keyword_score']}%"],
        ["Resume Sections", f"{ats_result['section_score']}%"],
        ["Contact Information", f"{ats_result['contact_score']}%"],
        ["Achievement Quality", f"{ats_result['achievement_score']}%"],
        ["Resume Length", f"{ats_result['length_score']}%"],
    ]

    score_table = Table(
        score_data,
        colWidths=[
            3.6 * inch,
            1.5 * inch
        ]
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica"
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ]
        )
    )

    story.append(
        score_table
    )

    story.append(
        Spacer(1, 20)
    )

    # Job description
    story.append(
        Paragraph(
            "Job Description",
            styles["Heading1"]
        )
    )

    add_markdown_text(
        story,
        job_description,
        styles
    )

    story.append(
        PageBreak()
    )

    # Required skills
    story.append(
        Paragraph(
            "Skills Required by the Job",
            styles["Heading1"]
        )
    )

    if required_skills:
        for skill in required_skills:
            story.append(
                Paragraph(
                    f"- {escape(clean_pdf_text(skill.title()))}",
                    styles["BodyText"]
                )
            )
    else:
        story.append(
            Paragraph(
                "No required skills were detected.",
                styles["BodyText"]
            )
        )

    story.append(
        Spacer(1, 14)
    )

    # Matched skills
    story.append(
        Paragraph(
            "Matching Skills",
            styles["Heading1"]
        )
    )

    if matched_skills:
        for skill in matched_skills:
            story.append(
                Paragraph(
                    f"- {escape(clean_pdf_text(skill.title()))}",
                    styles["BodyText"]
                )
            )
    else:
        story.append(
            Paragraph(
                "No matching skills were detected.",
                styles["BodyText"]
            )
        )

    story.append(
        Spacer(1, 14)
    )

    # Missing skills
    story.append(
        Paragraph(
            "Skills to Improve",
            styles["Heading1"]
        )
    )

    if missing_skills:
        for skill in missing_skills:
            story.append(
                Paragraph(
                    f"- {escape(clean_pdf_text(skill.title()))}",
                    styles["BodyText"]
                )
            )
    else:
        story.append(
            Paragraph(
                "No missing skills were detected.",
                styles["BodyText"]
            )
        )

    story.append(
        PageBreak()
    )

    # ATS breakdown
    story.append(
        Paragraph(
            "ATS Analysis",
            styles["Heading1"]
        )
    )

    ats_details = [
        [
            "Matched Keywords",
            (
                f"{ats_result['matched_keyword_count']}/"
                f"{ats_result['total_keyword_count']}"
            )
        ],
        [
            "Resume Word Count",
            str(ats_result["word_count"])
        ],
        [
            "Found Sections",
            ", ".join(
                ats_result["found_sections"]
            ) or "None"
        ],
        [
            "Missing Sections",
            ", ".join(
                ats_result["missing_sections"]
            ) or "None"
        ],
        [
            "Found Contact Details",
            ", ".join(
                ats_result["found_contact_items"]
            ) or "None"
        ],
        [
            "Missing Contact Details",
            ", ".join(
                ats_result["missing_contact_items"]
            ) or "None"
        ],
    ]

    ats_table = Table(
        ats_details,
        colWidths=[
            2.1 * inch,
            4.2 * inch
        ]
    )

    ats_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.whitesmoke
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
            ]
        )
    )

    story.append(
        ats_table
    )

    story.append(
        PageBreak()
    )

    # AI advice
    story.append(
        Paragraph(
            "AI Career Advice",
            styles["Heading1"]
        )
    )

    add_markdown_text(
        story,
        ai_advice,
        styles
    )

    story.append(
        PageBreak()
    )

    # Interview questions
    story.append(
        Paragraph(
            "Personalized Interview Questions",
            styles["Heading1"]
        )
    )

    add_markdown_text(
        story,
        interview_questions,
        styles
    )

    document.build(
        story
    )

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes