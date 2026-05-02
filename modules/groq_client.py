from groq import Groq

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"
FALLBACK_MAX_CHARS = 3000


def _truncate_messages(messages: list, max_chars: int) -> list:
    result = []
    for msg in messages:
        if msg["role"] == "user" and len(msg["content"]) > max_chars:
            msg = dict(msg, content=msg["content"][:max_chars])
        result.append(msg)
    return result


def groq_create(client: Groq, messages: list, temperature: float = 0.3,
                max_tokens: int = 2048) -> str:
    """Try PRIMARY_MODEL; fall back to FALLBACK_MODEL on 429/413."""
    for model in (PRIMARY_MODEL, FALLBACK_MODEL):
        try:
            msgs = _truncate_messages(messages, FALLBACK_MAX_CHARS) if model == FALLBACK_MODEL else messages
            resp = client.chat.completions.create(
                model=model,
                messages=msgs,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content
        except Exception as e:
            err = str(e)
            if model == PRIMARY_MODEL and ("429" in err or "413" in err):
                continue
            raise
    return ""
