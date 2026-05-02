from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn


def _set_font(run, name: str = '맑은 고딕', size: int = None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if size:
        run.font.size = Pt(size)


def _add_heading(doc: Document, text: str, level: int = 1):
    p = doc.add_heading('', level=level)
    run = p.add_run(text)
    run.font.name = '맑은 고딕'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')


def _add_paragraph(doc: Document, text: str):
    p = doc.add_paragraph()
    run = p.add_run(text)
    _set_font(run)


def generate_paper_docx(result: dict) -> bytes:
    doc = Document()
    _add_heading(doc, '논문 분석 결과', level=0)
    sections = [
        ('1. 논문 개요 및 목적', '개요및목적'),
        ('2. 연구 방법', '연구방법'),
        ('3. 주요 분석 결과', '주요분석결과'),
        ('4. 논문의 의의', '논문의의'),
    ]
    for title, key in sections:
        if key in result:
            _add_heading(doc, title, level=1)
            _add_paragraph(doc, result[key])
            doc.add_paragraph()
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()


def generate_translation_docx(translated: str) -> bytes:
    doc = Document()
    _add_heading(doc, '한국어 번역', level=0)
    for para in translated.split(chr(10)):
        if para.strip():
            _add_paragraph(doc, para.strip())
        else:
            doc.add_paragraph()
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()
