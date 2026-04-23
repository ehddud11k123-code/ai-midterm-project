from wordcloud import WordCloud
from PIL import Image
import plotly.graph_objects as go
import os
import urllib.request


def _get_korean_font() -> str:
    font_path = "/tmp/NanumGothic.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com/naver/nanumfont/releases/download/VER2.5/NanumFont_TTF_ALL.zip"
        # Fallback: use a direct TTF URL
        ttf_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        urllib.request.urlretrieve(ttf_url, font_path)
    return font_path


def generate_wordcloud(text: str) -> Image.Image:
    from modules.lang_utils import detect_language
    lang = detect_language(text)
    kwargs = dict(
        width=800, height=400,
        background_color="white",
        max_words=100,
        colormap="viridis",
    )
    if lang == "ko":
        from modules.korean_nlp import korean_nouns
        nouns = korean_nouns(text)
        text_for_cloud = " ".join(nouns)
        kwargs["font_path"] = _get_korean_font()
        wc = WordCloud(**kwargs).generate(text_for_cloud if text_for_cloud else text)
    else:
        wc = WordCloud(**kwargs).generate(text)
    return wc.to_image()


def plot_keyword_bar(keywords: list) -> go.Figure:
    words = [w for w, _ in reversed(keywords)]
    freqs = [f for _, f in reversed(keywords)]
    fig = go.Figure(go.Bar(
        x=freqs, y=words, orientation="h", marker_color="steelblue",
    ))
    fig.update_layout(
        title="키워드 빈도",
        xaxis_title="빈도",
        height=max(300, len(keywords) * 25),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def plot_sentiment_gauge(polarity: float, lang: str = "en") -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=polarity,
        title={"text": "감정 극성" if lang == "ko" else "Sentiment Polarity"},
        gauge={
            "axis": {"range": [-1, 1]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [-1, -0.1], "color": "#ff6b6b"},
                {"range": [-0.1, 0.1], "color": "#ffd93d"},
                {"range": [0.1, 1], "color": "#6bcb77"},
            ],
        },
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_sentence_length_hist(sentences: list) -> go.Figure:
    lengths = [len(s.split()) for s in sentences]
    fig = go.Figure(go.Histogram(x=lengths, nbinsx=20, marker_color="steelblue"))
    fig.update_layout(
        title="문장 길이 분포",
        xaxis_title="문장당 단어 수",
        yaxis_title="빈도",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig
