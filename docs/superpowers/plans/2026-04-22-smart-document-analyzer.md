# Smart Document Analyzer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 텍스트를 입력하면 키워드·감정·가독성·워드클라우드를 분석해 시각화하는 Streamlit 웹앱을 만든다.

**Architecture:** Streamlit이 UI를 담당하고, modules/ 아래 5개 파일이 각자 하나의 분석 기능을 담당한다. app.py는 각 모듈을 조합해 결과를 렌더링한다.

**Tech Stack:** Python 3.9+, Streamlit, NLTK, TextBlob, Plotly, WordCloud, Pandas, Pillow

---

## File Map

| 파일 | 역할 |
|------|------|
| `requirements.txt` | 패키지 의존성 |
| `modules/__init__.py` | 패키지 초기화 |
| `modules/stats.py` | 단어 수, 문장 수, 문단 수, 평균 문장 길이 계산 |
| `modules/keywords.py` | 상위 N개 키워드 빈도 추출 |
| `modules/sentiment.py` | TextBlob 감정 분석 (polarity, subjectivity, label) |
| `modules/readability.py` | Flesch Reading Ease 점수 및 등급 |
| `modules/visualize.py` | 워드클라우드, 바 차트, 게이지 차트 생성 |
| `app.py` | Streamlit 메인 앱 |
| `tests/test_stats.py` | stats 모듈 테스트 |
| `tests/test_keywords.py` | keywords 모듈 테스트 |
| `tests/test_sentiment.py` | sentiment 모듈 테스트 |
| `tests/test_readability.py` | readability 모듈 테스트 |

---

## Task 1: 프로젝트 초기 설정

**Files:**
- Create: `requirements.txt`
- Create: `modules/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: requirements.txt 생성**

```
streamlit>=1.32.0
nltk>=3.8.0
textblob>=0.17.0
plotly>=5.18.0
wordcloud>=1.9.0
pandas>=2.1.0
Pillow>=10.0.0
pytest>=7.4.0
```

- [ ] **Step 2: 패키지 설치**

```bash
pip install -r requirements.txt
```

Expected: 모든 패키지 설치 완료

- [ ] **Step 3: NLTK 데이터 다운로드**

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

Expected: 다운로드 완료 메시지 출력

- [ ] **Step 4: TextBlob 코퍼스 다운로드**

```bash
python -m textblob.download_corpora
```

Expected: 다운로드 완료

- [ ] **Step 5: 빈 패키지 파일 생성**

`modules/__init__.py` — 빈 파일

`tests/__init__.py` — 빈 파일

- [ ] **Step 6: Commit**

```bash
git add requirements.txt modules/__init__.py tests/__init__.py
git commit -m "chore: project setup and dependencies"
```

---

## Task 2: stats 모듈

**Files:**
- Create: `modules/stats.py`
- Create: `tests/test_stats.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_stats.py`:
```python
from modules.stats import get_stats

SAMPLE = "Hello world. This is a test.\n\nSecond paragraph here."

def test_word_count():
    result = get_stats(SAMPLE)
    assert result["word_count"] > 0

def test_sentence_count():
    result = get_stats(SAMPLE)
    assert result["sentence_count"] == 2

def test_paragraph_count():
    result = get_stats(SAMPLE)
    assert result["paragraph_count"] == 2

def test_avg_sentence_length():
    result = get_stats(SAMPLE)
    assert result["avg_sentence_length"] > 0

def test_unique_word_count():
    result = get_stats(SAMPLE)
    assert result["unique_word_count"] > 0
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
pytest tests/test_stats.py -v
```

Expected: FAILED — ModuleNotFoundError

- [ ] **Step 3: 구현**

`modules/stats.py`:
```python
from nltk.tokenize import word_tokenize, sent_tokenize


def get_stats(text: str) -> dict:
    sentences = sent_tokenize(text)
    words = [w for w in word_tokenize(text) if w.isalpha()]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    word_count = len(words)
    sentence_count = len(sentences)
    paragraph_count = len(paragraphs)
    avg_sentence_length = round(word_count / sentence_count, 1) if sentence_count else 0
    unique_word_count = len(set(w.lower() for w in words))

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_sentence_length": avg_sentence_length,
        "unique_word_count": unique_word_count,
    }
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_stats.py -v
```

Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add modules/stats.py tests/test_stats.py
git commit -m "feat: add stats module"
```

---

## Task 3: keywords 모듈

**Files:**
- Create: `modules/keywords.py`
- Create: `tests/test_keywords.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_keywords.py`:
```python
from modules.keywords import get_keywords

SAMPLE = "The quick brown fox jumps over the lazy dog. The fox is quick and the dog is lazy."

def test_returns_list_of_tuples():
    result = get_keywords(SAMPLE)
    assert isinstance(result, list)
    assert isinstance(result[0], tuple)

def test_top_n_limit():
    result = get_keywords(SAMPLE, top_n=5)
    assert len(result) <= 5

def test_no_stopwords():
    result = get_keywords(SAMPLE)
    words = [w for w, _ in result]
    assert "the" not in words
    assert "is" not in words

def test_frequency_descending():
    result = get_keywords(SAMPLE, top_n=10)
    freqs = [f for _, f in result]
    assert freqs == sorted(freqs, reverse=True)
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
pytest tests/test_keywords.py -v
```

Expected: FAILED — ModuleNotFoundError

- [ ] **Step 3: 구현**

`modules/keywords.py`:
```python
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_keywords(text: str, top_n: int = 20) -> list:
    stop_words = set(stopwords.words("english"))
    words = [
        w.lower()
        for w in word_tokenize(text)
        if w.isalpha() and w.lower() not in stop_words
    ]
    counter = Counter(words)
    return counter.most_common(top_n)
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_keywords.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add modules/keywords.py tests/test_keywords.py
git commit -m "feat: add keywords module"
```

---

## Task 4: sentiment 모듈

**Files:**
- Create: `modules/sentiment.py`
- Create: `tests/test_sentiment.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_sentiment.py`:
```python
from modules.sentiment import get_sentiment

def test_positive_text():
    result = get_sentiment("I love this wonderful amazing product!")
    assert result["label"] == "Positive"
    assert result["polarity"] > 0.1

def test_negative_text():
    result = get_sentiment("This is terrible, awful, and disgusting.")
    assert result["label"] == "Negative"
    assert result["polarity"] < -0.1

def test_has_required_keys():
    result = get_sentiment("Hello world.")
    assert "polarity" in result
    assert "subjectivity" in result
    assert "label" in result

def test_polarity_range():
    result = get_sentiment("The sky is blue.")
    assert -1.0 <= result["polarity"] <= 1.0
    assert 0.0 <= result["subjectivity"] <= 1.0
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
pytest tests/test_sentiment.py -v
```

Expected: FAILED — ModuleNotFoundError

- [ ] **Step 3: 구현**

`modules/sentiment.py`:
```python
from textblob import TextBlob


def get_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "label": label,
    }
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_sentiment.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add modules/sentiment.py tests/test_sentiment.py
git commit -m "feat: add sentiment module"
```

---

## Task 5: readability 모듈

**Files:**
- Create: `modules/readability.py`
- Create: `tests/test_readability.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_readability.py`:
```python
from modules.readability import get_readability

EASY_TEXT = "The cat sat on the mat. The dog ran fast."
HARD_TEXT = "The epistemological ramifications of poststructuralist philosophical discourse necessitate comprehensive reexamination."

def test_returns_score_and_grade():
    result = get_readability(EASY_TEXT)
    assert "score" in result
    assert "grade" in result

def test_easy_text_higher_score():
    easy = get_readability(EASY_TEXT)
    hard = get_readability(HARD_TEXT)
    assert easy["score"] > hard["score"]

def test_grade_label_exists():
    result = get_readability(EASY_TEXT)
    assert result["grade"] in ["Very Easy", "Easy", "Moderate", "Difficult", "Very Difficult"]
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
pytest tests/test_readability.py -v
```

Expected: FAILED — ModuleNotFoundError

- [ ] **Step 3: 구현**

`modules/readability.py`:
```python
from nltk.tokenize import sent_tokenize, word_tokenize


def _count_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def get_readability(text: str) -> dict:
    sentences = sent_tokenize(text)
    words = [w for w in word_tokenize(text) if w.isalpha()]

    if not sentences or not words:
        return {"score": 0.0, "grade": "N/A"}

    syllable_count = sum(_count_syllables(w) for w in words)
    score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllable_count / len(words))
    score = round(score, 1)

    if score >= 90:
        grade = "Very Easy"
    elif score >= 70:
        grade = "Easy"
    elif score >= 50:
        grade = "Moderate"
    elif score >= 30:
        grade = "Difficult"
    else:
        grade = "Very Difficult"

    return {"score": score, "grade": grade}
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_readability.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add modules/readability.py tests/test_readability.py
git commit -m "feat: add readability module"
```

---

## Task 6: visualize 모듈

**Files:**
- Create: `modules/visualize.py`

- [ ] **Step 1: 구현**

`modules/visualize.py`:
```python
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
```

- [ ] **Step 2: import 확인**

```bash
python -c "from modules.visualize import generate_wordcloud, plot_keyword_bar, plot_sentiment_gauge, plot_sentence_length_hist; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add modules/visualize.py
git commit -m "feat: add visualize module"
```

---

## Task 7: Streamlit 메인 앱

**Files:**
- Create: `app.py`

- [ ] **Step 1: 구현**

`app.py`:
```python
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
```

- [ ] **Step 2: 로컬 실행 테스트**

```bash
streamlit run app.py
```

Expected: 브라우저에서 http://localhost:8501 열림
확인: 텍스트 입력 후 [분석하기] 클릭 → 통계, 키워드, 감정, 워드클라우드, 가독성 모두 출력

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add streamlit main app"
```

---

## Task 8: 전체 테스트 및 GitHub Push

- [ ] **Step 1: 전체 테스트 실행**

```bash
pytest tests/ -v
```

Expected: 모든 테스트 통과 (16 passed)

- [ ] **Step 2: GitHub push**

```bash
git push origin master
```

---

## Task 9: Streamlit Cloud 배포

- [ ] **Step 1: share.streamlit.io 접속**

브라우저에서 https://share.streamlit.io 접속 후 GitHub 계정으로 로그인

- [ ] **Step 2: New app 생성**

- Repository: `ehddud11k123-code/ai-midterm-project`
- Branch: `master`
- Main file path: `app.py`
- [Deploy] 클릭

- [ ] **Step 3: 배포 URL 확인**

Expected: `https://[앱이름].streamlit.app` 형태의 URL 발급
