from groq import Groq

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"


def groq_create(client: Groq, messages: list, temperature: float = 0.3,
                max_tokens: int = 2048) -> str:
    """Try PRIMARY_MODEL; fall back to FALLBACK_MODEL on 429 rate-limit."""
    for model in (PRIMARY_MODEL, FALLBACK_MODEL):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content
        except Exception as e:
            if model == PRIMARY_MODEL and "429" in str(e):
                continue  # retry with fallback
            raise
    return ""
