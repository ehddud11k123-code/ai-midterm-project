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

    prompt = f"""아래 학술 논문을 분석하여 정확히 5개 섹션을 작성하라. 각 섹션은 서로 다른 관점을 다루며 내용이 절대 중복되어서는 안 된다.

논문 텍스트:
{text[:12000]}

===연구주제===
이 논문이 풀려는 문제, 배경, 기존 연구의 한계를 3-4문장. 방법/결과 언급 금지.

===주요기여===
기존 연구와 다른 novelty만. 새로운 아이디어/프레임워크/개념. bullet 5개. 수치 금지.

===연구방법===
아키텍처, 알고리즘, 데이터셋명/크기, 학습설정(optimizer/lr/batch) 등 기술 세부사항. 4-5문장. 결과수치 금지.

===핵심결과===
실험 수치(정확도/F1/BLEU 등), 베이스라인 대비 향상폭만. bullet 5개. 방법설명 금지.

===의의및한계===
적용 가능 분야, 실험/데이터 측면 약점, 향후 연구 방향. 3-4문장. 앞내용 반복 금지.
"""

    try:
        from modules.groq_client import groq_create
        content = groq_create(client, [{"role": "user", "content": prompt}],
                              temperature=0.3, max_tokens=4096)
        parsed = _parse_response(content)
        if not parsed:
            return {"error": "AI 응답 파싱 실패. 원문: " + content[:300]}
        return parsed
    except Exception as e:
        return {"error": str(e)}


def _parse_response(text: str) -> dict:
    result = {}
    parts = re.split(r'===([^=]+)===', text)
    for i in range(1, len(parts), 2):
        key = parts[i].strip()
        value = parts[i + 1].strip() if i + 1 < len(parts) else ""
        result[key] = value
    return result
