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


def analyze_paper(text: str) -> dict:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        return {"error": "secrets에 GROQ_API_KEY 키가 없습니다."}
    except Exception as e:
        return {"error": f"secrets 읽기 오류: {e}"}
    if not api_key:
        return {"error": "GROQ_API_KEY 값이 비어 있습니다."}
    client = Groq(api_key=api_key)

    prompt = f"""다음은 학술 논문 텍스트입니다. 아래 항목을 한국어로 상세하게 분석해주세요.

논문 텍스트:
{text[:12000]}

다음 형식으로 정확히 답해주세요. 각 항목은 충분히 자세하게 작성해주세요:

[연구주제]
이 논문이 다루는 핵심 주제, 연구 배경, 해결하려는 문제를 3-4문장으로 상세히.

[주요기여]
이 논문의 핵심 기여와 novelty를 bullet point 5개로. 각 항목은 2문장 이상으로.

[연구방법]
사용된 방법론, 모델 구조, 실험 설계, 데이터셋 등을 4-5문장으로 상세히.

[핵심결과]
주요 실험 결과, 수치, 비교 성능 등을 bullet point 5개로. 구체적인 수치 포함.

[의의및한계]
이 연구의 학문적/실용적 의의와 한계점, 향후 연구 방향을 3-4문장으로.
"""

    try:
        from modules.groq_client import groq_create
        content = groq_create(client, [{"role": "user", "content": prompt}],
                              temperature=0.3, max_tokens=2048)
        return _parse_response(content)
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
