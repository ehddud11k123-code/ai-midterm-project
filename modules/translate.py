import streamlit as st

MAX_CHARS = 8000


def translate_to_korean(text: str) -> str:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        return "오류: GROQ_API_KEY가 설정되지 않았습니다."

    from groq import Groq
    client = Groq(api_key=api_key)

    truncated = text[:MAX_CHARS]
    note = f"\n\n*(원문이 길어 앞부분 {MAX_CHARS}자만 번역되었습니다.)*" if len(text) > MAX_CHARS else ""

    prompt = f"""아래 영어 텍스트를 자연스러운 한국어로 번역하세요.
원문의 단락 구조와 줄바꿈을 그대로 유지하세요.
번역문만 출력하고, 다른 설명은 하지 마세요.

[영어 원문]
{truncated}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=4096,
        )
        return response.choices[0].message.content.strip() + note
    except Exception as e:
        return f"번역 오류: {e}"
