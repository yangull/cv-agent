# nodes/export_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from state import AgentState

def export_pdf(state: AgentState) -> AgentState:
    bullets = state["rewritten_bullets"]
    score = state["match_score"]
    explanation = state["match_explanation"]

    # Define the output path — saved in the project root
    output_path = "cv_tailored.pdf"

    # Create the PDF document with A4 size and margins
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Get default styles and define our own for each element type
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=12
    )

    score_style = ParagraphStyle(
        "score",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.HexColor("#16213e"),
        spaceAfter=6
    )

    explanation_style = ParagraphStyle(
        "explanation",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#444444"),
        spaceAfter=20
    )

    bullet_style = ParagraphStyle(
        "bullet",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=8,
        leftIndent=12
    )

    section_style = ParagraphStyle(
        "section",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=10
    )

    # Build the list of elements that go into the PDF top to bottom
    elements = []

    # Title
    elements.append(Paragraph("Tailored CV — AI Agent Output", title_style))
    elements.append(Spacer(1, 0.3*cm))

    # Match score
    elements.append(Paragraph(f"Match Score: {score}/100", score_style))
    elements.append(Spacer(1, 0.2*cm))

    # Gap explanation from Claude
    elements.append(Paragraph(f"Analysis: {explanation}", explanation_style))
    elements.append(Spacer(1, 0.3*cm))

    # Section header for bullets
    elements.append(Paragraph("Rewritten Experience Bullets", section_style))
    elements.append(Spacer(1, 0.2*cm))

    # Each rewritten bullet on its own line with a bullet point prefix
    for bullet in bullets:
        elements.append(Paragraph(f"• {bullet}", bullet_style))

    # Build the PDF — this writes the file to disk
    doc.build(elements)

    print(f"✅ export_pdf: saved to {output_path}")

    # Write the output path into state so main.py can report it
    return {"output_pdf_path": output_path}