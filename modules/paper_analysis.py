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

[연구주제]
- 이 논문이 풀려는 문제가 무엇인가? 왜 이 문제가 중요한가?
- 기존 연구의 어떤 한계를 극복하려 하는가?
- 3-4문장. 방법론/결과 언급 금지.

[주요기여]
- 이 논문이 기존 연구와 다른 점은 무엇인가? (novelty)
- 새롭게 제안된 아이디어, 프레임워크, 개념만 작성.
- bullet 5개. 실험 수치/결과 언급 금지.

[연구방법]
- 구체적인 기술 구현: 아키텍처, 알고리즘, 수식, 레이어 구조 등
- 사용한 데이터셋 이름, 크기, 전처리 방법
- 학습 설정(optimizer, lr, batch size 등) 포함
- 4-5문장. 결과 수치 언급 금지.

[핵심결과]
- 실험에서 달성한 구체적인 수치(정확도, F1, BLEU 등)만 나열
- 베이스라인 대비 몇 % 향상되었는지 명시
- bullet 5개. 방법 설명 금지, 숫자 위주로.

[의의및한계]
- 이 연구 결과가 실제로 어떤 분야/문제에 적용 가능한가?
- 실험 설계, 데이터, 일반화 측면에서 아직 해결되지 않은 약점
- 향후 연구 방향 제안
- 3-4문장. 앞 섹션 내용 반복 금지.
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
    parts = re.split(r'\[(\w+)\]', text)
    for i in range(1, len(parts), 2):
        key = parts[i]
        value = parts[i + 1].strip() if i + 1 < len(parts) else ""
        result[key] = value
    return result
