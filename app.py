import streamlit as st
from nltk.tokenize import sent_tokenize

from modules.stats import get_stats
from modules.keywords import get_keywords
from modules.sentiment import get_sentiment
from modules.readability import get_readability
from modules.visualize import (
    generate_wordcloud,
    plot_keyword_bar,
    plot_sentiment_gauge,
    plot_sentence_length_hist,
)

st.set_page_config(page_title="Smart Document Analyzer", page_icon="📄", layout="wide")
st.title("📄 Smart Document Analyzer")
st.caption("텍스트를 입력하면 키워드·감정·가독성·워드클라우드를 분석합니다.")

input_method = st.radio("입력 방법", ["텍스트 직접 입력", "파일 업로드"], horizontal=True)

text = ""
if input_method == "텍스트 직접 입력":
    text = st.text_area("텍스트를 여기에 붙여넣으세요", height=200, placeholder="Paste your text here...")
else:
    uploaded = st.file_uploader("TXT 파일 업로드", type=["txt"])
    if uploaded:
        text = uploaded.read().decode("utf-8", errors="ignore")
        st.success(f"{len(text)} 글자 로드됨")

analyze_btn = st.button("🔍 분석하기", type="primary", disabled=not text.strip())

if analyze_btn and text.strip():
    with st.spinner("분석 중..."):
        stats = get_stats(text)
        keywords = get_keywords(text, top_n=20)
        sentiment = get_sentiment(text)
        readability = get_readability(text)
        sentences = sent_tokenize(text)

    st.subheader("📊 기본 통계")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("단어 수", stats["word_count"])
    c2.metric("문장 수", stats["sentence_count"])
    c3.metric("문단 수", stats["paragraph_count"])
    c4.metric("평균 문장 길이", f"{stats['avg_sentence_length']} 단어")
    c5.metric("고유 단어 수", stats["unique_word_count"])

    st.divider()

    col_kw, col_sent = st.columns(2)

    with col_kw:
        st.subheader("🔑 키워드 분석")
        if keywords:
            st.plotly_chart(plot_keyword_bar(keywords), use_container_width=True)
        else:
            st.info("키워드를 추출할 수 없습니다.")

    with col_sent:
        st.subheader("😊 감정 분석")
        label_color = {"Positive": "🟢", "Neutral": "🟡", "Negative": "🔴"}
        st.markdown(f"### {label_color.get(sentiment['label'], '')} {sentiment['label']}")
        st.plotly_chart(plot_sentiment_gauge(sentiment["polarity"]), use_container_width=True)
        st.caption(f"Subjectivity: {sentiment['subjectivity']} (0=객관적, 1=주관적)")

    st.divider()

    st.subheader("☁️ 워드클라우드")
    try:
        wc_image = generate_wordcloud(text)
        st.image(wc_image, use_container_width=True)
    except Exception:
        st.warning("워드클라우드 생성 실패. 텍스트가 너무 짧을 수 있습니다.")

    st.divider()

    col_read, col_hist = st.columns(2)

    with col_read:
        st.subheader("📖 가독성 점수")
        st.metric("Flesch Reading Ease", readability["score"])
        st.markdown(f"**등급:** {readability['grade']}")
        grade_desc = {
            "Very Easy": "매우 쉬운 글 — 초등학생도 이해 가능",
            "Easy": "쉬운 글",
            "Moderate": "보통 난이도",
            "Difficult": "어려운 글 — 대학 수준",
            "Very Difficult": "매우 어려운 글 — 전문가 수준",
        }
        st.caption(grade_desc.get(readability["grade"], ""))

    with col_hist:
        st.subheader("📏 문장 길이 분포")
        st.plotly_chart(plot_sentence_length_hist(sentences), use_container_width=True)
