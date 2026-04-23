from textblob import TextBlob
from modules.lang_utils import detect_language


def get_sentiment(text: str) -> dict:
    lang = detect_language(text)
    if lang == "ko":
        from modules.korean_nlp import korean_sentiment
        return korean_sentiment(text)
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return {"label": label, "polarity": polarity, "subjectivity": subjectivity}
