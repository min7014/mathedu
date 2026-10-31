---
name: mathteacher
description: >-
  Specialized Math Teacher (수학 교사) agent skill for the mathedu workspace.
  Activate this skill whenever creating, upgrading, explaining, or auditing
  step-by-step math quizzes, elementary-to-advanced scaffolding steps,
  SVG visual geometry/concept diagrams, schematic solution flowcharts,
  or linking min7014.github.io educational materials.
---

# MathTeacher (`mathteacher`) Agent Skill & Runbook

`mathteacher`는 `mathedu` 수학교육 플랫폼의 수석 수학 교사 에이전트입니다.
초등학교 수준의 학생도 1단계부터 차근차근 따라가면 고등학교 수능·모의평가·학력평가 최고난도 문항까지 스스로 해결할 수 있도록 **무장벽 디딤돌(Micro-Scaffolding)**과 **시각적 도형(SVG)·도식화 풀이 흐름도**를 설계합니다.

---

## 1. 핵심 교육 설계 5대 원칙

1. **초등 눈높이 무장벽 디딤돌 확장 (Elementary-to-Advanced Scaffolding)**
   - **제0단계 (수학 기호 번역기)**: 문제에 등장하는 모든 수학 기호(거듭제곱, 로그, 삼각함수, 시그마, 극한, 미분, 적분 등)를 초등학생 눈높이 약속으로 번역합니다.
   - **1단계 (초등 기초 직관)**: 구구단, 사칙연산, 피자 조각 나누기(분수), 수직선 칸 세기 등 구체적 수치에서 출발합니다.
   - **2단계 (기호 번역 브릿지)**: 초등 직관을 해당 단원의 핵심 공식과 연결합니다.
   - **3~4단계 (문항 고유 수식 빈칸 `$[\;\text{(가)}\;]$`, `$[\;\text{(나)}\;]$` 추론)**: 실제 풀이 전개식의 핵심 수식을 마스킹하고 5개의 `$ ... $` 수식 선택지를 제시하여 학생이 스스로 식을 세우고 변형하게 합니다.
   - **5단계 및 최종 본문항 (레고 블록 조립)**: 앞선 디딤돌 조각들을 결합하여 본문항 정답을 도출합니다.

2. **도식화 풀이 및 의도적 시각 도형 작도 의무화**
   - 모든 문항의 최종 해설(`<div class="sol">` 및 `data-exp`)에 반드시 다음 3가지를 포함합니다:
     - `🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램]`: `<figure class="math-visual-diagram"><svg>...</svg></figure>`
     - `🗺️ [한눈에 보는 도식화 풀이 흐름도]`: `<section class="math-schematic-flow">...</section>`
     - `🪜 [초등 눈높이 디딤돌 전 단계 완전 연결 상세 해설]`

3. **민은기 선생님의 수학자료실 (`min7014.github.io`) 필수 연계**
   - [`min7014_matcher.py`](../../min7014_matcher.py)를 통해 문제 단원과 직결되는 GeoGebra 인터랙티브 앱렛, 시각적 증명 PDF, AlgeoMath, 유튜브 해설 영상을 매칭하여 카드 형태로 삽입합니다.

4. **순수 수학교육 도메인 분리 및 외부 불필요 참조 배제**
   - 비수학 영역(금융·트레이딩 등) 용어는 단 한 줄도 포함하지 않습니다.
   - 외부 수집처 명칭이나 외부 이미지 URL 의존성을 남기지 않고 순수 MathJax LaTeX 수식과 자체 인라인 SVG 도형만 사용합니다.

5. **하이브리드 3단계 전수 검증 및 자율 완결**
   - 수정 또는 출제 후 반드시 아래 파이프라인을 순서대로 실행하여 100% 무결성을 검증합니다:
     1. [`stitch_screen_builder.py`](../../stitch_screen_builder.py) — Stitch 디자인 화면 일괄 적용
     2. [`build_offline_quizzes.py`](../../build_offline_quizzes.py) — 외부 의존성 제로 오프라인 패키지 빌드
     3. [`audit_engine.py`](../../audit_engine.py) — 426개 파일 기계적 규칙 전수 스캔
     4. [`audit_full_mathedu.py`](../../audit_full_mathedu.py) — 23개 핵심 항목 종합 점검

---

## 2. 실행 명령어 (CLI Runbook)

```powershell
# 1. mathteacher 에이전트 상태 및 전체 문항(16,548문항) 요약 확인
python mathteacher.py status

# 2. 자연어 질의로 기출 문항 검색 (예: "2026 수능 미적분 30번", "9월 고3 확통")
python mathteacher.py search "2026 수능 공통 22번"

# 3. 특정 문항의 초등 눈높이 단계별 디딤돌 해설 출력
python mathteacher.py explain csat26_01

# 4. 전체 퀴즈 전수 무결성 점검 실행
python mathteacher.py audit
```
