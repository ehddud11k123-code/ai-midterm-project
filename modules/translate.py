import streamlit as st

PREVIEW_CHARS = 8000
CHUNK_CHARS = 5000


def _get_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        return None, "오류: GROQ_API_KEY가 설정되지 않았습니다."
    from groq import Groq
    return Groq(api_key=api_key), None


def _translate_chunk(client, chunk: str) -> str:
    prompt = f"""아래 영어 텍스트를 자연스러운 한국어로 번역하세요.
원문의 단락 구조와 줄바꿈을 그대로 유지하세요.
번역문만 출력하고, 다른 설명은 하지 마세요.

[영어 원문]
{chunk}"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=4096,
    )
    return response.choices[0].message.content.strip()


def translate_to_korean(text: str) -> str:
    """UI용 미리보기 번역 (최대 8000자)"""
    client, err = _get_client()
    if err:
        return err
    truncated = text[:PREVIEW_CHARS]
    note = f"\n\n*(원문이 길어 앞부분 {PREVIEW_CHARS}자만 번역되었습니다. Word 파일에는 전문이 포함됩니다.)*" if len(text) > PREVIEW_CHARS else ""
    try:
        return _translate_chunk(client, truncated) + note
    except Exception as e:
        return f"번역 오류: {e}"


def translate_full_to_korean(text: str) -> str:
    """docx용 전문 번역 (청크 분할)"""
    client, err = _get_client()
    if err:
        return err

    paragraphs = text.split("\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) + 1 > CHUNK_CHARS and current:
            chunks.append(current.strip())
            current = para + "\n"
        else:
            current += para + "\n"
    if current.strip():
        chunks.append(current.strip())

    results = []
    for chunk in chunks:
        try:
            results.append(_translate_chunk(client, chunk))
        except Exception as e:
            results.append(f"[번역 오류: {e}]")

    return "\n\n".join(results)
