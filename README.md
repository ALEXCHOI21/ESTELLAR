# 💎 에스텔라 주얼리(ESTELLAR) 프리미엄 디지털 쇼룸

본 프로젝트는 대전광역시 유성구 원신흥동에 위치한 하이엔드 파인 주얼리 전문 숍 **'에스텔라(ESTELLAR)'**의 메인 디지털 쇼룸 웹사이트입니다.
한국 보석디자인 공모전 대상 및 국가 공인 보석 감정사(AGK) 자격을 갖춘 조예은 대표의 퍼스널 브랜딩 자산(유튜브, 인스타그램, 틱톡)을 유기적으로 연동하여, 브랜드 가치를 시각적으로 극대화하고 1:1 쇼룸 예약 전환을 유도하도록 고도로 기획되었습니다.

---

## 🛠️ 핵심 특징 (Key Features)

1.  **Platform-Agnostic & Scalability (플랫폼 독립성과 확장성)**
    *   어떠한 프레임워크나 벤더 락인(Vendor Lock-in) 없이 퓨어 Vanilla HTML5, CSS3, JavaScript 만으로 개발되어 높은 웹 표준 이식성을 보장합니다.
    *   반응형 모듈러 컴포넌트(Atomic Design Pattern)로 설계되어 향후 React, Vue, Next.js 등의 프레임워크로 즉각적인 이식이 가능합니다.
2.  **Premium Dark Aesthetics (럭셔리 비주얼 시스템)**
    *   샴페인 골드(#E5C483)와 미니멀 럭셔리 다크 테마(#0A0A0B)의 완벽한 조화.
    *   유리 재질감을 살린 초고급 글래스모피즘(Glassmorphism) 네비게이션 및 컴포넌트 카드.
3.  **Micro Interaction (사용자 인터랙티브 효과)**
    *   고성능 `Intersection Observer` API 기반의 부드러운 스크롤 페이드 업(Fade-up) 애니메이션 엔진 내장.
    *   주얼리 카테고리(반지, 목걸이, 팔찌, 세트)별 인터랙티브 필터링 갤러리 구현.
4.  **Omni-Channel Marketing Synergy (크로스 미디어 연동)**
    *   조예은 대표의 공식 유튜브 채널 `@조예은-x6y` 크리에이터 콘텐츠 카드 노출.
    *   실시간 1:1 상담 예약 요청 폼 빌더 및 네이버 지도 플레이스 예약 시스템(Naver Place Reservation) 원클릭 연동.

---

## 📂 파일 구조 (File Structure)

```text
.
├── index.html   # SEO 최적화 메타데이터 및 에스텔라 프리미엄 시맨틱 마크업
├── style.css    # 샴페인 골드 컬러 팔레트, 글래스모피즘 및 애니메이션 효과 정의
├── main.js      # Intersection Observer 기반 인터랙션 엔진 및 예약 제어 로직
└── README.md    # 프로젝트 사양서 및 가이드라인 (본 파일)
```

---

## 🚀 로컬 실행 방법 (How to Run)

본 프로젝트는 순수 웹 표준 언어로 작성되었으므로 별도의 빌드 과정 없이 즉시 실행 가능합니다.

1.  본 디렉토리의 `index.html` 파일을 더블클릭하여 웹 브라우저에서 즉시 확인하거나,
2.  `Live Server` 또는 Node.js `http-server` 등을 활용하여 로컬 호스트 환경에서 테스트합니다.
    ```bash
    # Node.js http-server 패키지 활용 예시 (선택사항)
    npx http-server ./
    ```

---

## 🌐 SEO & 성능 최적화 명세 (SEO Specifications)

*   **시맨틱 마크업:** `<header>`, `<main>`, `<section>`, `<article>`, `<footer>` 등의 최신 HTML5 시맨틱 요소를 적극 도입하여 검색 로봇 수집 효율 극대화.
*   **단일 H1 규칙 준수:** 메인 타이틀을 단 하나의 `<h1>` 태그로 통제하여 검색 가독성 확보.
*   **고유식별자 부여:** 상호작용이 발생하는 모든 `<button>`, `<input>`, `<a>` 태그에 고유 ID를 부여하여 자동화 테스트 및 분석 스크립트 삽입 최적화.

---
> **ChoiGPT Corp. Strategic Design Team:** "단순한 쇼핑몰을 넘어, 주얼리 디자이너의 철학을 경험하고 소통하는 예술적 허브로 기능하도록 설계하였습니다. 브랜드의 헤리티지가 2030 스마트 럭셔리 고객층의 마음을 사로잡기를 바랍니다."
