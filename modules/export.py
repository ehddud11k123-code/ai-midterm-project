from fpdf import FPDF
import os
import urllib.request


def _get_korean_font() -> str:
    font_path = "/tmp/NanumGothic.ttf"
    if not os.path.exists(font_path):
        ttf_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        urllib.request.urlretrieve(ttf_url, font_path)
    return font_path


def generate_pdf_report(
    text_snippet: str,
    stats: dict,
    sentiment: dict,
    readability: dict,
    keywords: list,
    summary: list,
    lang: str = "en",
) -> bytes:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if lang == "ko":
        font_path = _get_korean_font()
        pdf.add_font("Nanum", fname=font_path)
        pdf.set_font("Nanum", size=16)
    else:
        pdf.set_font("Helvetica", "B", 16)

    page_w = pdf.w - pdf.l_margin - pdf.r_margin

    # Title
    title = "스마트 문서 분석 리포트" if lang == "ko" else "Smart Document Analyzer - Report"
    pdf.cell(page_w, 10, title, ln=True, align="C")
    pdf.ln(4)

    def heading(txt):
        if lang == "ko":
            pdf.set_font("Nanum", size=12)
        else:
            pdf.set_font("Helvetica", "B", 12)
        pdf.cell(page_w, 8, txt, ln=True)

    def body(txt):
        if lang == "ko":
            pdf.set_font("Nanum", size=10)
        else:
            pdf.set_font("Helvetica", size=10)
        safe = txt if lang == "ko" else txt.encode("latin-1", errors="replace").decode("latin-1")
        pdf.multi_cell(page_w, 6, safe)

    # Text snippet
    heading("입력 텍스트 (앞 300자)" if lang == "ko" else "Input Text (first 300 chars)")
    snippet = text_snippet[:300].replace("\n", " ")
    body(f"  {snippet}")
    pdf.ln(4)

    # Stats
    heading("기본 통계" if lang == "ko" else "Basic Statistics")
    for key, val in stats.items():
        label = key.replace("_", " ")
        body(f"  {label}: {val}")
    pdf.ln(4)

    # Sentiment
    heading("감정 분석" if lang == "ko" else "Sentiment Analysis")
    body(f"  {'결과' if lang == 'ko' else 'Label'}: {sentiment['label']}")
    body(f"  {'극성' if lang == 'ko' else 'Polarity'}: {sentiment['polarity']}")
    pdf.ln(4)

    # Readability
    heading("가독성" if lang == "ko" else "Readability")
    body(f"  {'점수' if lang == 'ko' else 'Score'}: {readability['score']}")
    body(f"  {'등급' if lang == 'ko' else 'Grade'}: {readability['grade']}")
    pdf.ln(4)

    # Keywords
    heading("핵심 키워드" if lang == "ko" else "Top Keywords")
    for word, freq in keywords[:10]:
        body(f"  {word}: {freq}")
    pdf.ln(4)

    # Summary
    if summary:
        heading("요약" if lang == "ko" else "Extractive Summary")
        for i, sentence in enumerate(summary, 1):
            body(f"  {i}. {sentence}")
            pdf.ln(1)

    return bytes(pdf.output())
