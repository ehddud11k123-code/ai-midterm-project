import streamlit as st
from groq import Groq


def analyze_paper(text: str) -> dict:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        return {"error": "GROQ_API_KEY가 설정되지 않았습니다."}
    client = Groq(api_key=api_key)

    prompt = (
        "You are an academic paper analyst. Read the paper below and write a thorough analysis in Korean.\n"
        "Structure your response with these four headings (use ## for headings):\n\n"
        "## 1. 논문 개요 및 목적\n"
        "## 2. 연구 방법\n"
        "## 3. 주요 분석 결과\n"
        "## 4. 논문의 의의\n\n"
        "Write 4-6 sentences per section. Be specific and detailed.\n\n"
        f"Paper:\n{text[:10000]}"
    )

    try:
        from modules.groq_client import groq_create
        raw = groq_create(client, [{"role": "user", "content": prompt}],
                          temperature=0.3, max_tokens=4096)
        if not raw or not raw.strip():
            return {"error": "AI 응답이 비어 있습니다."}
        return {"content": raw.strip()}
    except Exception as e:
        return {"error": str(e)}
