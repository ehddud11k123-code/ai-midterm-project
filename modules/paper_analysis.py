import json
import re
import streamlit as st
from groq import Groq


def analyze_paper(text: str) -> dict:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        return {"error": "GROQ_API_KEY가 설정되지 않았습니다."}
    client = Groq(api_key=api_key)

    prompt = (
        "You are an academic paper analyst. Analyze the paper below and return ONLY a JSON object. "
        "No explanation, no markdown, no code block. Just the raw JSON.\n\n"
        "Required JSON format:\n"
        "{\"개요및목적\": \"...\", \"연구방법\": \"...\", \"주요분석결과\": \"...\", \"논문의의\": \"...\"}\n\n"
        "Instructions for each field (write in Korean, be thorough and detailed):\n"
        "- 개요및목적: Summarize the paper's background, the problem it addresses, its research goals, and why this topic matters. 4-5 sentences.\n"
        "- 연구방법: Describe in detail the methodology: model architecture, algorithms, datasets used (names and sizes), experimental setup, training configurations. 5-6 sentences.\n"
        "- 주요분석결과: Present the key findings with specific numbers (accuracy, F1, BLEU, etc.), comparisons to baselines, and notable observations. Use bullet points.\n"
        "- 논문의의: Explain the academic and practical significance of this work, its contributions to the field, and potential future research directions. 4-5 sentences.\n\n"
        f"Paper text:\n{text[:10000]}"
    )

    try:
        from modules.groq_client import groq_create
        raw = groq_create(client, [{"role": "user", "content": prompt}],
                          temperature=0.2, max_tokens=4096)
        return _parse_json(raw)
    except Exception as e:
        return {"error": str(e)}


def _parse_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return {"error": "파싱 실패 — AI 원문: " + text[:400]}
