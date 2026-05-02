import re
import streamlit as st
from groq import Groq

KEYS = ["개요및목적", "연구방법", "주요분석결과", "논문의의"]


def analyze_paper(text: str) -> dict:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        return {"error": "GROQ_API_KEY가 설정되지 않았습니다."}
    client = Groq(api_key=api_key)

    prompt = (
        "Analyze the academic paper below. Write in Korean. "
        "Use EXACTLY the tags below — nothing before <개요및목적>, nothing after </논문의의>.\n\n"
        "<개요및목적>\n"
        "4-5 sentences: background, problem being solved, why it matters, limitations of prior work. No methods or results.\n"
        "</개요및목적>\n"
        "<연구방법>\n"
        "5-6 sentences: model architecture, algorithms, dataset names/sizes, training settings (optimizer/lr/batch size).\n"
        "</연구방법>\n"
        "<주요분석결과>\n"
        "Bullet points with specific numbers (accuracy/F1/BLEU etc), comparison to baselines.\n"
        "</주요분석결과>\n"
        "<논문의의>\n"
        "4-5 sentences: academic/practical significance, contributions to the field, future research directions.\n"
        "</논문의의>\n\n"
        f"Paper:\n{text[:10000]}"
    )

    try:
        from modules.groq_client import groq_create
        raw = groq_create(client, [{"role": "user", "content": prompt}],
                          temperature=0.2, max_tokens=4096)
        result = _parse(raw)
        if not result:
            return {"error": "파싱 실패 — AI 원문:\n" + raw[:600]}
        return result
    except Exception as e:
        return {"error": str(e)}


def _parse(text: str) -> dict:
    result = {}
    for key in KEYS:
        m = re.search(rf"<{key}>(.*?)</{key}>", text, re.DOTALL)
        if m:
            result[key] = m.group(1).strip()
    return result
