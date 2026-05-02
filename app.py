import nltk
import streamlit as st
from nltk.tokenize import sent_tokenize

for _pkg in ["punkt", "punkt_tab", "stopwords", "averaged_perceptron_tagger",
             "averaged_perceptron_tagger_eng", "maxent_ne_chunker",
             "maxent_ne_chunker_tab", "words"]:
    nltk.download(_pkg, quiet=True)

from modules.stats import get_stats
from modules.keywords import get_keywords
from modules.sentiment import get_sentiment
from modules.readability import get_readability
from modules.visualize import (
    plot_keyword_bar,
    plot_sentiment_gauge,
    plot_sentence_length_hist,
)
from modules.summarize import get_summary
from modules.ngrams import get_ngrams, plot_ngram_bar
from modules.lang_utils import detect_language
from modules.paper_analysis import analyze_paper



def _extract_pdf_text(uploaded_file) -> str:
    import pypdf
    reader = pypdf.PdfReader(uploaded_file)
    sep = chr(10)
    return sep.join(page.extract_text() or "" for page in reader.pages)


SAMPLE_TEXT_EN = """Artificial intelligence is transforming the world at an unprecedented pace.
From healthcare to finance, AI systems are helping professionals make better decisions faster.
Machine learning algorithms can now detect diseases from medical images with accuracy rivaling human experts.
In the financial sector, AI-powered tools analyze market trends and manage risk in real time.
However, the rapid advancement of AI also raises important ethical questions about privacy, bias, and accountability.
Researchers and policymakers are working together to establish guidelines that ensure AI is developed responsibly.
The future of AI depends not only on technical innovation but also on thoughtful governance and public trust.
Education systems must adapt to prepare students for a world where human-AI collaboration is the norm.
Ultimately, artificial intelligence is a tool, and its impact will be shaped by the choices we make today."""

SAMPLE_TEXT_KO = """인공지능은 전례 없는 속도로 세상을 변화시키고 있습니다.
의료부터 금융까지, AI 시스템은 전문가들이 더 빠르고 정확한 의사결정을 내릴 수 있도록 돕고 있습니다.
머신러닝 알고리즘은 이제 의료 영상에서 질병을 인간 전문가 수준의 정확도로 진단할 수 있습니다.
금융 분야에서는 AI 기반 도구가 시장 동향을 분석하고 실시간으로 리스크를 관리합니다.
그러나 AI의 급속한 발전은 개인정보, 편향성, 책임 문제 등 중요한 윤리적 질문도 제기합니다.
연구자와 정책 입안자들은 AI가 책임감 있게 개발되도록 가이드라인을 마련하기 위해 협력하고 있습니다.
AI의 미래는 기술 혁신뿐만 아니라 사려 깊은 거버넌스와 대중의 신뢰에도 달려 있습니다.
교육 시스템은 인간과 AI의 협업이 일상화된 세상에 학생들을 준비시키도록 변화해야 합니다.
궁극적으로 인공지능은 도구이며, 그 영향력은 오늘 우리가 내리는 선택에 의해 결정될 것입니다."""

st.set_page_config(page_title="스마트 문서 분석기", page_icon="📄", layout="wide")
st.title("📄 스마트 문서 분석기")
st.caption("텍스트를 입력하면 키워드·감정·가독성 등을 분석합니다. 한국어와 영어를 자동으로 인식합니다.")

mode = st.radio("모드 선택", ["📄 논문 분석", "문서 분석"], horizontal=True)


def get_text_input(label: str = "") -> str:
    key_text = f"textarea_{label}"

    def _load_sample_ko():
        st.session_state[key_text] = SAMPLE_TEXT_KO

    def _load_sample_en():
        st.session_state[key_text] = SAMPLE_TEXT_EN

    method = st.radio(
        f"입력 방법{' (' + label + ')' if label else ''}",
        ["텍스트 입력", "파일 업로드"],
        horizontal=True,
        key=f"method_{label}",
    )
    text = ""
    if method == "텍스트 입력":
        col_area, col_btn = st.columns([5, 1])
        with col_btn:
            st.write("")
            st.write("")
            st.button("📋 한국어 샘플", key=f"sample_ko_{label}", on_click=_load_sample_ko)
            st.button("📋 영어 샘플", key=f"sample_en_{label}", on_click=_load_sample_en)
        with col_area:
            text = st.text_area(
                f"텍스트 붙여넣기{' (' + label + ')' if label else ''}",
                height=180,
                key=key_text,
                placeholder="한국어 또는 영어 텍스트를 붙여넣으세요...",
            )
    else:
        uploaded = st.file_uploader(
            f"TXT 파일{' (' + label + ')' if label else ''}",
            type=["txt", "pdf"],
            key=f"upload_{label}",
        )
        if uploaded:
            if uploaded.name.endswith(".pdf"):
                text = _extract_pdf_text(uploaded)
            else:
                text = uploaded.read().decode("utf-8", errors="ignore")
            st.success(f"{len(text)} 글자 로드됨")
    return text


def run_analysis(text: str) -> dict:
    lang = detect_language(text)
    if lang == "ko":
        from modules.korean_nlp import korean_sentences
        sentences = korean_sentences(text)
    else:
        sentences = sent_tokenize(text)
    return {
        "lang": lang,
        "stats": get_stats(text),
        "keywords": get_keywords(text, top_n=20),
        "sentiment": get_sentiment(text),
        "readability": get_readability(text),
        "sentences": sentences,
        "summary": get_summary(text, sentence_count=3),
        "bigrams": get_ngrams(text, n=2, top_k=15),
        "trigrams": get_ngrams(text, n=3, top_k=10),
    }


def render_analysis(result: dict, text: str, key_prefix: str = ""):
    lang = result.get("lang", "en")
    stats = result["stats"]
    keywords = result["keywords"]
    sentiment = result["sentiment"]
    readability = result["readability"]
    sentences = result["sentences"]
    summary = result["summary"]
    bigrams = result["bigrams"]
    trigrams = result["trigrams"]

    tab_labels = ["📊 통계 & 요약", "🔑 키워드 & N-gram", "😊 감정 & 가독성"]
    if lang == "en":
        tab_labels.append("🌐 한국어 번역")
    tab_objects = st.tabs(tab_labels)
    tab1, tab2, tab3 = tab_objects[0], tab_objects[1], tab_objects[2]

    with tab1:
        st.subheader("기본 통계")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("단어 수", stats["word_count"])
        c2.metric("문장 수", stats["sentence_count"])
        c3.metric("문단 수", stats["paragraph_count"])
        c4.metric("평균 문장 길이", f"{stats['avg_sentence_length']} 단어")
        c5.metric("고유 단어 수", stats["unique_word_count"])

        st.divider()
        st.subheader("✏️ 핵심 요약 (Extractive Summary)")
        if summary:
            for i, sentence in enumerate(summary, 1):
                st.markdown(f"**{i}.** {sentence}")
        else:
            st.info("요약을 생성하기에 텍스트가 너무 짧습니다.")


    with tab2:
        col_kw, col_ng = st.columns(2)
        with col_kw:
            st.subheader("🔑 키워드 빈도")
            if keywords:
                st.plotly_chart(plot_keyword_bar(keywords), use_container_width=True, key=f"kw_{key_prefix}")
            else:
                st.info("키워드를 추출할 수 없습니다.")
        with col_ng:
            st.subheader("🔗 N-gram 분석")
            ng_tab1, ng_tab2 = st.tabs(["Bigram (2단어)", "Trigram (3단어)"])
            with ng_tab1:
                if bigrams:
                    st.plotly_chart(plot_ngram_bar(bigrams, "Top Bigrams"), use_container_width=True, key=f"bi_{key_prefix}")
                else:
                    st.info("Bigram 없음")
            with ng_tab2:
                if trigrams:
                    st.plotly_chart(plot_ngram_bar(trigrams, "Top Trigrams"), use_container_width=True, key=f"tri_{key_prefix}")
                else:
                    st.info("Trigram 없음")

    with tab3:
        col_sent, col_read = st.columns(2)
        with col_sent:
            st.subheader("😊 감정 분석")
            label_color = {"Positive": "🟢", "Neutral": "🟡", "Negative": "🔴"}
            st.markdown(f"### {label_color.get(sentiment['label'], '')} {sentiment['label']}")
            st.plotly_chart(plot_sentiment_gauge(sentiment["polarity"]), use_container_width=True, key=f"gauge_{key_prefix}")
            if sentiment.get("reason"):
                st.caption(f"이유: {sentiment['reason']}")
        with col_read:
            st.subheader("📖 가독성 점수")
            st.metric("가독성 점수", readability["score"])
            st.markdown(f"**등급:** {readability['grade']}")
            grade_desc = {
                "Very Easy": "매우 쉬운 글 — 초등학생도 이해 가능",
                "Easy": "쉬운 글",
                "Moderate": "보통 난이도",
                "Difficult": "어려운 글 — 대학 수준",
                "Very Difficult": "매우 어려운 글 — 전문가 수준",
            }
            st.caption(grade_desc.get(readability["grade"], ""))
            st.divider()
            st.subheader("📏 문장 길이 분포")
            st.plotly_chart(plot_sentence_length_hist(sentences), use_container_width=True, key=f"hist_{key_prefix}")



    if lang == "en":
        with tab_objects[3]:
            st.subheader("🌐 한국어 번역")
            translate_key = f"translated_{key_prefix}"
            if st.button("번역 시작", key=f"translate_{key_prefix}", type="primary"):
                with st.spinner("번역 중..."):
                    from modules.translate import translate_to_korean
                    st.session_state[translate_key] = translate_to_korean(text)
            if translate_key in st.session_state:
                st.markdown(st.session_state[translate_key])
                st.divider()
                from modules.export_docx import generate_translation_docx
                full_translation = st.session_state.get("doc_full_translation", st.session_state[translate_key])
                docx_bytes = generate_translation_docx(full_translation)
                st.download_button(
                    label="📄 Word 파일로 다운로드 (전문)",
                    data=docx_bytes,
                    file_name="translation.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"docx_trans_{key_prefix}",
                )


# --- Main Logic ---
if mode == "📄 논문 분석":

    paper_text = get_text_input()
    if st.button("🔍 논문 분석하기", type="primary", disabled=not paper_text.strip()):
        with st.spinner("AI가 논문을 분석 중..."):
            st.session_state["paper_result"] = analyze_paper(paper_text)

    result = st.session_state.get("paper_result")
    if result is not None:
        if "error" in result:
            st.error(result["error"])
        else:
            from modules.export_docx import generate_paper_docx
            docx_bytes = generate_paper_docx(result.get("content", ""))
            st.success("분석 완료!")
            st.download_button(
                label="📄 Word 파일로 다운로드",
                data=docx_bytes,
                file_name="paper_analysis.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="paper_docx",
            )

elif mode == "문서 분석":

    text = get_text_input()
    if st.button("🔍 분석하기", type="primary", disabled=not text.strip()):
        with st.spinner("분석 중..."):
            result = run_analysis(text)
            st.session_state["doc_result"] = result
            st.session_state["doc_text"] = text
            st.session_state.pop("translated_single", None)
            st.session_state.pop("doc_full_translation", None)
        if result["lang"] == "en":
            with st.spinner("Word 파일용 전문 번역 중..."):
                from modules.translate import translate_full_to_korean
                st.session_state["doc_full_translation"] = translate_full_to_korean(text)

    if "doc_result" in st.session_state and "doc_text" in st.session_state:
        render_analysis(st.session_state["doc_result"], st.session_state["doc_text"], key_prefix="single")


