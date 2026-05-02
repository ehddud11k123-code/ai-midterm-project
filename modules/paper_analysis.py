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
        "{\"연구주제\": \"...\", \"주요기여\": \"...\", \"연구방법\": \"...\", \"핵심결과\": \"...\", \"의의및한계\": \"...\"}\n\n"
        "Instructions for each field (write in Korean):\n"
        "- 연구주제: What problem does this paper solve? Why is it important? Limitations of prior work? (3-4 sentences, NO methods or results)\n"
        "- 주요기여: What is novel vs prior work? 5 bullet points of new ideas/frameworks. NO numbers.\n"
        "- 연구방법: Architecture, dataset names/sizes, training settings (optimizer/lr/batch). 4-5 sentences. NO result numbers.\n"
        "- 핵심결과: Specific numbers (accuracy/F1/BLEU), improvement over baselines. 5 bullet points. Numbers only.\n"
        "- 의의및한계: Applications, weaknesses, future directions. 3-4 sentences.\n\n"
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
