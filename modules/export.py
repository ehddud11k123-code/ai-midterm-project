from fpdf import FPDF
import io


def generate_pdf_report(
    text_snippet: str,
    stats: dict,
    sentiment: dict,
    readability: dict,
    keywords: list,
    summary: list,
) -> bytes:
    """Generate a PDF report and return as bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Smart Document Analyzer - Report", ln=True, align="C")
    pdf.ln(4)

    # Text snippet
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Input Text (first 300 chars)", ln=True)
    pdf.set_font("Helvetica", size=10)
    snippet = text_snippet[:300].replace("\n", " ")
    pdf.multi_cell(0, 6, snippet)
    pdf.ln(4)

    # Stats
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Basic Statistics", ln=True)
    pdf.set_font("Helvetica", size=10)
    for key, val in stats.items():
        label = key.replace("_", " ").title()
        pdf.cell(0, 6, f"  {label}: {val}", ln=True)
    pdf.ln(4)

    # Sentiment
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Sentiment Analysis", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, f"  Label: {sentiment['label']}", ln=True)
    pdf.cell(0, 6, f"  Polarity: {sentiment['polarity']}", ln=True)
    pdf.cell(0, 6, f"  Subjectivity: {sentiment['subjectivity']}", ln=True)
    pdf.ln(4)

    # Readability
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Readability", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, f"  Score: {readability['score']}", ln=True)
    pdf.cell(0, 6, f"  Grade: {readability['grade']}", ln=True)
    pdf.ln(4)

    # Keywords
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Top Keywords", ln=True)
    pdf.set_font("Helvetica", size=10)
    for word, freq in keywords[:10]:
        pdf.cell(0, 6, f"  {word}: {freq}", ln=True)
    pdf.ln(4)

    # Summary
    if summary:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Extractive Summary", ln=True)
        pdf.set_font("Helvetica", size=10)
        for i, sentence in enumerate(summary, 1):
            pdf.multi_cell(0, 6, f"  {i}. {sentence}")

    return bytes(pdf.output())
