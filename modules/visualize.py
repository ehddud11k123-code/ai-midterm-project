from wordcloud import WordCloud
from PIL import Image
import plotly.graph_objects as go


def generate_wordcloud(text: str) -> Image.Image:
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=100,
        colormap="viridis",
    ).generate(text)
    return wc.to_image()


def plot_keyword_bar(keywords: list) -> go.Figure:
    words = [w for w, _ in reversed(keywords)]
    freqs = [f for _, f in reversed(keywords)]
    fig = go.Figure(go.Bar(
        x=freqs,
        y=words,
        orientation="h",
        marker_color="steelblue",
    ))
    fig.update_layout(
        title="Top Keywords",
        xaxis_title="Frequency",
        height=max(300, len(keywords) * 25),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def plot_sentiment_gauge(polarity: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=polarity,
        title={"text": "Sentiment Polarity"},
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
        title="Sentence Length Distribution",
        xaxis_title="Words per Sentence",
        yaxis_title="Count",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig
