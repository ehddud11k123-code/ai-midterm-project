from groq import Groq

PRIMARY_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-2.0-flash"
FALLBACK_MAX_CHARS = 8000


def _gemini_create(messages: list, temperature: float, max_tokens: int) -> str:
    import streamlit as st
    import google.generativeai as genai
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        raise Exception("GEMINI_API_KEY not set in secrets")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = messages[-1]["content"]
    resp = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return resp.text


def groq_create(client: Groq, messages: list, temperature: float = 0.3,
                max_tokens: int = 2048) -> str:
    """Try Groq 70b first; fall back to Gemini on 429/413."""
    try:
        resp = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "429" in err or "413" in err:
            return _gemini_create(messages, temperature, max_tokens)
        raise
