import re
import streamlit as st
import google.generativeai as genai

SECTION_PATTERNS = [
    "abstract", "introduction", "related work", "background",
    "methodology", "methods", "proposed method", "approach",
    "experiment", "experiments", "results", "evaluation",
    "discussion", "conclusion", "conclusions", "future work",
    "references",
]

_HEADER_RE = re.compile(
    r'(?:^|\n)(?:\d+\.?\s+)?(' +
    '|'.join(re.escape(s) for s in SECTION_PATTERNS) +
    r')s?\s*\n',
    re.IGNORECASE,
)


def _get_model():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def detect_sections(text: str) -> dict[str, str]:
    matches = list(_HEADER_RE.finditer(text))
    if not matches:
        return {"전체 텍스트": text}
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1).strip().title()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            key = name if name not in sections else f"{name} ({i+1})"
            sections[key] = body
    return sections if sections else {"전체 텍스트": text}


def analyze_paper_with_gemini(text: str) -> dict:
    model = _get_model()
    if not model:
        return None

    prompt = f"""다음은 학술 논문 텍스트입니다. 아래 항목을 한국어로 분석해주세요.

논문 텍스트:
{text[:8000]}

다음 형식으로 정확히 답해주세요 (각 항목은 줄바꿈으로 구분):

[연구주제]
이 논문이 다루는 핵심 주제나 문제를 1-2문장으로.

[주요기여]
이 논문의 핵심 기여나 제안을 bullet point 3개로.

[연구방법]
사용된 방법론/기법을 2-3문장으로.

[핵심결과]
주요 실험 결과나 발견을 bullet point 3개로.

[한계점]
논문의 한계나 향후 연구 방향을 1-2문장으로."""

    try:
        response = model.generate_content(prompt)
        return _parse_gemini_response(response.text)
    except Exception as e:
        return {"error": str(e)}


def _parse_gemini_response(text: str) -> dict:
    result = {}
    sections = re.split(r'\[(\w+)\]', text)
    for i in range(1, len(sections), 2):
        key = sections[i]
        value = sections[i + 1].strip() if i + 1 < len(sections) else ""
        result[key] = value
    return result


def analyze_paper(text: str) -> dict:
    gemini_result = analyze_paper_with_gemini(text)
    sections = detect_sections(text)
    return {
        "gemini": gemini_result,
        "sections": sections,
    }
