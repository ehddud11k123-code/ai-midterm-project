from fpdf import FPDF


def _safe_text(text: str) -> str:
    """Remove characters that fpdf cannot render with Helvetica."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_pdf_report(
    text_snippet: str,
    stats: dict,
    sentiment: dict,
    readability: dict,
    keywords: list,
    summary: list,
) -> bytes:
    """Generate a PDF report and return as bytes."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    page_w = pdf.w - pdf.l_margin - pdf.r_margin  # usable width

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(page_w, 10, "Smart Document Analyzer - Report", ln=True, align="C")
    pdf.ln(4)

    # Text snippet
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(page_w, 8, "Input Text (first 300 chars)", ln=True)
    pdf.set_font("Helvetica", size=10)
    snippet = _safe_text(text_snippet[:300].replace("\n", " "))
    pdf.multi_cell(page_w, 6, snippet)
    pdf.ln(4)

    # Stats
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(page_w, 8, "Basic Statistics", ln=True)
    pdf.set_font("Helvetica", size=10)
    for key, val in stats.items():
        label = key.replace("_", " ").title()
        pdf.cell(page_w, 6, f"  {label}: {val}", ln=True)
    pdf.ln(4)

    # Sentiment
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(page_w, 8, "Sentiment Analysis", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(page_w, 6, f"  Label: {sentiment['label']}", ln=True)
    pdf.cell(page_w, 6, f"  Polarity: {sentiment['polarity']}", ln=True)
    pdf.cell(page_w, 6, f"  Subjectivity: {sentiment['subjectivity']}", ln=True)
    pdf.ln(4)

    # Readability
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(page_w, 8, "Readability", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(page_w, 6, f"  Score: {readability['score']}", ln=True)
    pdf.cell(page_w, 6, f"  Grade: {readability['grade']}", ln=True)
    pdf.ln(4)

    # Keywords
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(page_w, 8, "Top Keywords", ln=True)
    pdf.set_font("Helvetica", size=10)
    for word, freq in keywords[:10]:
        pdf.cell(page_w, 6, f"  {word}: {freq}", ln=True)
    pdf.ln(4)

    # Summary
    if summary:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(page_w, 8, "Extractive Summary", ln=True)
        pdf.set_font("Helvetica", size=10)
        for i, sentence in enumerate(summary, 1):
            safe = _safe_text(f"  {i}. {sentence}")
            pdf.multi_cell(page_w, 6, safe)
            pdf.ln(1)

    return bytes(pdf.output())
