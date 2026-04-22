# Technical Requirements Document (TRD)
## 스마트 문서 분석 웹앱

**프로젝트명:** AI Midterm Project — Smart Document Analyzer  
**버전:** 1.0  
**작성일:** 2026-04-22  
**작성자:** ehddud11k123-code  

---

## 1. 기술 스택 (Tech Stack)

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| 언어 | Python | 3.9+ | 전체 백엔드 및 앱 로직 |
| 웹 프레임워크 | Streamlit | 1.32+ | 웹 UI 렌더링 |
| NLP | NLTK | 3.8+ | 토큰화, 불용어 처리, 품사 태깅 |
| 감정 분석 | TextBlob | 0.17+ | Polarity/Subjectivity 분석 |
| 시각화 | Plotly | 5.18+ | 인터랙티브 차트 |
| 워드클라우드 | WordCloud | 1.9+ | 워드클라우드 이미지 생성 |
| 데이터 처리 | Pandas | 2.1+ | 데이터 테이블 처리 |
| 배포 | Streamlit Cloud | - | 무료 웹 배포 |

---

## 2. 시스템 아키텍처 (Architecture)

```
[사용자 브라우저]
      |
[Streamlit 웹 서버]
      |
[app.py - 메인 앱]
      |
+----------------------------------+
|        분석 모듈 (modules/)       |
+----------------+-----------------+
| stats.py       | 기본 통계 계산   |
| keywords.py    | 키워드 추출      |
| sentiment.py   | 감정 분석        |
| readability.py | 가독성 점수 계산 |
| visualize.py   | 시각화 생성      |
+----------------+-----------------+
      |
[결과 렌더링 -> 브라우저]
```

---

## 3. 프로젝트 구조 (Directory Structure)

```
ai-midterm-project/
├── app.py                  # Streamlit 메인 앱
├── requirements.txt        # 패키지 의존성
├── modules/
│   ├── __init__.py
│   ├── stats.py            # 기본 통계 (단어 수, 문장 수 등)
│   ├── keywords.py         # 키워드 추출 (TF 기반)
│   ├── sentiment.py        # 감정 분석 (TextBlob)
│   ├── readability.py      # 가독성 점수 계산
│   └── visualize.py        # 워드클라우드, 차트 생성
├── docs/
│   ├── PRD.md
│   └── TRD.md
└── README.md
```

---

## 4. 모듈별 상세 명세

### 4.1 stats.py - 기본 통계

**입력:** text: str  
**출력:** dict

| 항목 | 계산 방법 |
|------|----------|
| 단어 수 | nltk.word_tokenize() 후 알파벳 토큰만 카운트 |
| 문장 수 | nltk.sent_tokenize() |
| 문단 수 | 빈 줄(\n\n) 기준 분리 |
| 평균 문장 길이 | 단어 수 / 문장 수 |
| 고유 단어 수 | set() 적용 후 카운트 |

### 4.2 keywords.py - 키워드 추출

**입력:** text: str, top_n: int = 20  
**출력:** List[Tuple[str, int]] (단어, 빈도)

- NLTK 불용어(stopwords) 제거
- 소문자 변환 후 알파벳 단어만 추출
- Counter로 빈도 계산 후 상위 N개 반환

### 4.3 sentiment.py - 감정 분석

**입력:** text: str  
**출력:** dict

| 항목 | 설명 |
|------|------|
| polarity | -1.0 (부정) ~ 1.0 (긍정) |
| subjectivity | 0.0 (객관) ~ 1.0 (주관) |
| label | "Positive" / "Neutral" / "Negative" |

- TextBlob .sentiment 속성 활용
- polarity > 0.1 -> Positive, < -0.1 -> Negative, 나머지 -> Neutral

### 4.4 readability.py - 가독성 점수

**입력:** text: str  
**출력:** dict

| 항목 | 계산 방법 |
|------|----------|
| Flesch Reading Ease | 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words) |
| 등급 | 90+ Very Easy / 70+ Easy / 50+ Moderate / 30+ Difficult / 30미만 Very Difficult |

### 4.5 visualize.py - 시각화

| 함수 | 출력 |
|------|------|
| generate_wordcloud(text) | WordCloud PIL 이미지 |
| plot_keyword_bar(keywords) | Plotly 가로 바 차트 |
| plot_sentiment_gauge(polarity) | Plotly 게이지 차트 |
| plot_sentence_length_hist(sentences) | Plotly 히스토그램 |

---

## 5. UI 구성 (Streamlit Layout)

```
+------------------------------------------+
|  Smart Document Analyzer                  |
+------------------------------------------+
|  [텍스트 입력창 또는 파일 업로드]            |
|  [분석하기 버튼]                            |
+------------------------------------------+
|  기본 통계                                  |
|  [단어수] [문장수] [문단수] [평균문장길이]    |
+------------------------------------------+
|  키워드 분석          감정 분석             |
|  [바 차트]            [게이지 차트]          |
+------------------------------------------+
|  워드클라우드                               |
|  [이미지]                                   |
+------------------------------------------+
|  가독성 점수                                |
|  [점수 + 등급 + 설명]                        |
+------------------------------------------+
```

---

## 6. 의존성 (requirements.txt)

```
streamlit>=1.32.0
nltk>=3.8.0
textblob>=0.17.0
plotly>=5.18.0
wordcloud>=1.9.0
pandas>=2.1.0
Pillow>=10.0.0
```

---

## 7. 배포 방법 (Deployment)

### 로컬 실행
```bash
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
streamlit run app.py
```

### Streamlit Cloud 배포
1. GitHub 레포에 코드 push
2. share.streamlit.io 에서 레포 연결
3. app.py 지정 후 Deploy

---

## 8. 제약사항 및 한계

| 항목 | 내용 |
|------|------|
| 언어 | 기본 영어 텍스트 최적화 (한국어는 가독성 점수 미지원) |
| 파일 형식 | .txt 파일만 지원 (PDF, docx 미지원) |
| 텍스트 길이 | 10만 자 이하 권장 |
| 오프라인 | 최초 실행 시 NLTK 데이터 다운로드 필요 |
