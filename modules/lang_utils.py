from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    """Returns 'ko' or 'en'."""
    if not text or len(text.strip()) < 10:
        return "en"
    try:
        lang = detect(text)
        return "ko" if lang == "ko" else "en"
    except Exception:
        return "en"
