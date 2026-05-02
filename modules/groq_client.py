from groq import Groq

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.3-70b"


def _cerebras_create(messages: list, temperature: float, max_tokens: int) -> str:
    import streamlit as st
    from cerebras.cloud.sdk import Cerebras
    try:
        api_key = st.secrets["CEREBRAS_API_KEY"]
    except KeyError:
        raise Exception("CEREBRAS_API_KEY not set in secrets")
    client = Cerebras(api_key=api_key)
    resp = client.chat.completions.create(
        model=FALLBACK_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content


def groq_create(client: Groq, messages: list, temperature: float = 0.3,
                max_tokens: int = 2048) -> str:
    """Try Groq 70b first; fall back to Cerebras on 429/413."""
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
            return _cerebras_create(messages, temperature, max_tokens)
        raise
