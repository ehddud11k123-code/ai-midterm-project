from modules.lang_utils import detect_language


def get_sentiment(text: str) -> dict:
    groq_result = _groq_sentiment(text)
    if groq_result:
        return groq_result
    return _textblob_sentiment(text)


def _groq_sentiment(text: str) -> dict | None:
    try:
        import streamlit as st
        from groq import Groq
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        prompt = f"""다음 텍스트의 감정을 분석해주세요. 반드시 아래 형식으로만 답하세요.

텍스트:
{text[:3000]}

형식:
LABEL: Positive 또는 Negative 또는 Neutral
POLARITY: -1.0에서 1.0 사이 숫자
REASON: 한 문장으로 이유"""

        from modules.groq_client import groq_create
        _content = groq_create(client, [{"role": "user", "content": prompt}],
                              temperature=0.1, max_tokens=128)
        return _parse_sentiment(_content)
    except Exception:
        return None


def _parse_sentiment(text: str) -> dict | None:
    import re
    label_m = re.search(r'LABEL:\s*(Positive|Negative|Neutral)', text, re.IGNORECASE)
    polarity_m = re.search(r'POLARITY:\s*([-\d.]+)', text)
    reason_m = re.search(r'REASON:\s*(.+)', text)
    if not label_m or not polarity_m:
        return None
    return {
        "label": label_m.group(1).capitalize(),
        "polarity": round(float(polarity_m.group(1)), 3),
        "subjectivity": 0.0,
        "reason": reason_m.group(1).strip() if reason_m else "",
    }


def _textblob_sentiment(text: str) -> dict:
    from textblob import TextBlob
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return {"label": label, "polarity": polarity, "subjectivity": subjectivity, "reason": ""}
