import re
import streamlit as st
from groq import Groq

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


def _get_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return None
    if not api_key:
        return None
    return Groq(api_key=api_key)


def analyze_paper(text: str) -> dict:
    client = _get_client()
    if not client:
        return {"error": "API 키가 설정되지 않았습니다."}

    prompt = f"""다음은 학술 논문 텍스트입니다. 아래 항목을 한국어로 분석해주세요.

논문 텍스트:
{text[:6000]}

다음 형식으로 정확히 답해주세요:

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
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024,
        )
        return _parse_response(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def _parse_response(text: str) -> dict:
    result = {}
    parts = re.split(r'\[(\w+)\]', text)
    for i in range(1, len(parts), 2):
        key = parts[i]
        value = parts[i + 1].strip() if i + 1 < len(parts) else ""
        result[key] = value
    return result
