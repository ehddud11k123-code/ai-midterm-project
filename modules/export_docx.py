from io import BytesIO
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def _heading(doc: Document, text: str, level: int = 1):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p


def generate_analysis_docx(text: str, stats: dict, sentiment: dict,
                            readability: dict, keywords: list,
                            summary: list, lang: str = "en") -> bytes:
    doc = Document()
    doc.add_heading("문서 분석 결과", 0)

    _heading(doc, "기본 통계", 1)
    table = doc.add_table(rows=1, cols=2)
    table.style = "Light List Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text = "항목"
    hdr[1].text = "값"
    rows = [
        ("단어 수", str(stats.get("word_count", ""))),
        ("문장 수", str(stats.get("sentence_count", ""))),
        ("문단 수", str(stats.get("paragraph_count", ""))),
        ("평균 문장 길이", f"{stats.get('avg_sentence_length', '')} 단어"),
        ("고유 단어 수", str(stats.get("unique_word_count", ""))),
    ]
    for label, value in rows:
        row = table.add_row().cells
        row[0].text = label
        row[1].text = value
    doc.add_paragraph()

    _heading(doc, "핵심 요약", 1)
    if summary:
        for i, sentence in enumerate(summary, 1):
            doc.add_paragraph(f"{i}. {sentence}")
    else:
        doc.add_paragraph("요약을 생성하기에 텍스트가 너무 짧습니다.")
    doc.add_paragraph()

    _heading(doc, "키워드", 1)
    if keywords:
        kw_text = ", ".join(f"{w}({f})" for w, f in keywords[:15])
        doc.add_paragraph(kw_text)
    doc.add_paragraph()

    _heading(doc, "감정 분석", 1)
    doc.add_paragraph(f"판정: {sentiment.get('label', '')}")
    doc.add_paragraph(f"극성(Polarity): {sentiment.get('polarity', '')}")
    if sentiment.get("reason"):
        doc.add_paragraph(f"이유: {sentiment['reason']}")
    doc.add_paragraph()

    _heading(doc, "가독성", 1)
    doc.add_paragraph(f"점수: {readability.get('score', '')}")
    doc.add_paragraph(f"등급: {readability.get('grade', '')}")

    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()


def generate_paper_docx(result: dict) -> bytes:
    doc = Document()
    doc.add_heading("논문 분석 결과", 0)

    sections = [
        ("🎯 연구 주제", "연구주제"),
        ("💡 주요 기여", "주요기여"),
        ("⚙️ 연구 방법", "연구방법"),
        ("📊 핵심 결과", "핵심결과"),
        ("⚠️ 의의 및 한계", "의의및한계"),
    ]
    for title, key in sections:
        if key in result:
            _heading(doc, title, 1)
            doc.add_paragraph(result[key])
            doc.add_paragraph()

    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()
