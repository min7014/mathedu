#!/usr/bin/env python3
"""
mathedu AI 자동 퀴즈 빌더 (_auto_quiz_builder.py)
웹에서 접수된 문제 출제 요청(_request_new)을 기반으로
초등·중학생도 이해할 수 있는 5~8단계 인터랙티브 수학 퀴즈 HTML을 자동 제작하고
board/index.json 등록 및 GitHub Pages에 실시간 배포합니다.
"""
import os, sys, json, re, time, hashlib, subprocess, urllib.request
from datetime import datetime, timezone, timedelta
import generator

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(REPO_DIR, 'board')
INDEX_FILE = os.path.join(BOARD_DIR, 'index.json')
KST = timezone(timedelta(hours=9))

TELEGRAM_BOT_TOKEN = '8825093659:AAGKWO6FH4WF5PaqHrRadjtvC7fRxyuHg5o'
TELEGRAM_CHAT_ID = '43453234'

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def make_smart_fallback_title(content):
    """
    제목이 비어있을 때 문제 지문과 수식을 분석하여 최적의 단원/주제 제목을 도출합니다.
    """
    clean = re.sub(r'\[문제 생성 요청\]|내용:|정답/힌트:.*|\[이미지:.*\]', '', content or '', flags=re.S).strip()
    
    topic_map = [
        ("수열과 점화식", ["수열", "점화식", "등차수열", "등비수열", "일반항", "시그마", "a_{n+1}", "a_n"]),
        ("조건부확률과 통계", ["조건부확률", "이항분포", "정규분포", "표본평균", "신뢰구간", "확률변수", "독립시행"]),
        ("경우의 수와 순열·조합", ["경우의 수", "순열", "조합", "중복조합", "원순열", "최단 거리", "최단거리", "주사위", "카드"]),
        ("미분과 접선의 방정식", ["도함수", "미분계수", "접선의 방정식", "접선", "극댓값", "극솟값", "변곡점", "미분"]),
        ("정적분과 넓이", ["정적분", "부정적분", "구간", "넓이", "역도함수", "적분"]),
        ("지수함수와 로그함수", ["지수함수", "로그함수", "지수방정식", "로그방정식", "지수부등식", "상용로그", "2^x", "log_"]),
        ("삼각함수와 그래프", ["삼각함수", "사인", "코사인", "탄젠트", "sin", "cos", "tan", "주기"]),
        ("이차함수와 직선의 위치 관계", ["이차함수", "포물선", "판별식", "서로 다른 두 점", "접선", "x^2"]),
        ("이차방정식과 근과 계수", ["이차방정식", "근과 계수의 관계", "실근", "허근", "중근"]),
        ("기하와 벡터", ["벡터", "공간도형", "타원", "쌍곡선", "포물선", "정사영", "내적"]),
    ]
    
    for name, kws in topic_map:
        if any(k in clean for k in kws):
            return name
            
    first_line = clean.splitlines()[0] if clean else ""
    first_line = re.sub(r'[\$\[\]\{\}\(\)\=\+\-\*\/]', ' ', first_line)
    first_line = ' '.join(first_line.split())
    if first_line:
        s = first_line if len(first_line) <= 20 else first_line[:20] + "…"
        return f"수학 퀴즈 · {s}"
    return f"수학 퀴즈 · 단계별 핵심 개념 ({datetime.now(KST).strftime('%H:%M')})"

def parse_request_text(text):
    """
    [문제 생성 요청]
    제목: {title}
    내용: {content}
    정답/힌트: {hint}
    """
    title = ""
    content = ""
    hint = ""
    
    title_m = re.search(r'제목:\s*(.*?)(?=\n내용:|\n정답|\Z)', text, re.S)
    if title_m: title = title_m.group(1).strip()
    
    content_m = re.search(r'내용:\s*(.*?)(?=\n정답/힌트:|\n정답:|\Z)', text, re.S)
    if content_m: content = content_m.group(1).strip()
    
    hint_m = re.search(r'정답(?:/힌트)?:\s*(.*?)$', text, re.S)
    if hint_m: hint = hint_m.group(1).strip()
    
    if not title and not content:
        content = text
        
    return title, content or text, hint

HERMES_BIN = r'C:\Users\min\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe'
if not os.path.exists(HERMES_BIN):
    HERMES_BIN = 'hermes'

def build_quiz_with_ai(title, content, hint):
    """
    AI 에이전트를 호출하여 단계별 퀴즈 JSON을 생성합니다.
    제목이 비어있거나 'TEST', '수학 퀴즈' 등 임의 입력인 경우
    지문과 수식을 정밀 분석하여 전문적인 고품질 한글 수학 제목을 자동 생성합니다.
    """
    generic_titles = ["수학 퀴즈", "TEST", "test", "수학 문제", "자동 생성", "새 퀴즈", "제목 없음", ""]
    is_title_empty = not title or title.strip() in generic_titles

    title_instruction = (
        "Analyze the mathematical concepts, formulas, and question requirements in the Problem Statement deeply. DEDUCE and GENERATE a concise, professional Korean pedagogical title (e.g. '이차함수와 직선의 위치 관계 및 판별식', '지수함수와 로그함수의 역함수 대칭', '수열의 귀납적 정의와 일반항', '조건부확률과 독립시행'). Put this deduced title into the 'title' field of the JSON."
        if is_title_empty else
        f"Use '{title}' as the problem title (or polish it slightly for clarity in Korean)."
    )

    prompt = f"""You are an elite mathematics educator creating an interactive step-by-step quiz for Korean students.
Problem Statement:
{content}
Provided Hint/Answer: {hint}
Input Title: {title if not is_title_empty else '(None provided - please analyze the problem and generate a professional pedagogical title)'}

Your tasks:
1. Title Analysis: {title_instruction}
2. Progressive Breakdown: Break this problem down into a progressive pedagogical quiz (at least 3 building-block levels + 1 final target problem level) so that even younger students can learn the principles step by step.

Return ONLY a strictly valid JSON object (no markdown code blocks, no backticks, just raw JSON) matching this exact schema:
{{
  "title": "분석된 핵심 수학 단원/주제 제목 (한글 25자 이내, 예: 지수함수와 로그함수의 교점)",
  "symbols": [
    {{"sym": "수학 기호 1", "desc": "기호의 의미"}}
  ],
  "levels": [
    {{
      "title": "🔰 제0단계 · 핵심 개념 익히기",
      "knowledge": "이 단계에서 알아야 할 기초 수학 원리 설명 (LaTeX 수식 포함)",
      "questions": [
        {{
          "stem": "기초 확인 문제 지문",
          "options": ["보기 1", "보기 2", "보기 3", "보기 4", "보기 5"],
          "answer": 2,
          "exp": "정답 해설 (LaTeX 수식 포함)"
        }}
      ]
    }},
    {{
      "title": "🔰 제1단계 · 조건 분석하기",
      "knowledge": "심화 공식 또는 유도 과정 설명",
      "questions": [
        {{
          "stem": "중간 유도 문제 지문",
          "options": ["보기 1", "보기 2", "보기 3", "보기 4", "보기 5"],
          "answer": 1,
          "exp": "정답 해설"
        }}
      ]
    }}
  ],
  "final": {{
    "stem": "{content}",
    "options": ["보기 1", "보기 2", "보기 3", "보기 4", "보기 5"],
    "answer": 3,
    "exp": "최종 문제 정답 상세 해설",
    "solution": "전체 문제의 풀이과정 종합 요약"
  }}
}}
Rules:
1. All mathematical formulas must use valid LaTeX like $x^2$ or $\\frac{{a}}{{b}}$.
2. Use standard pedagogical Korean for all explanations and titles. NEVER use Chinese characters or artifacts like '的一般형'.
3. Every question must have exactly 5 options, and the 'answer' field (1-based index 1~5) MUST STRICTLY match the correct option at options[answer - 1].
4. Mathematical Soundness: Ensure all definitions, concavity/convexity (a > 0 is 아래로 볼록/convex down, a < 0 is 위로 볼록/convex up), intervals, bounds, and step-by-step arithmetic are 100% rigorous and verified with NO hallucinations or unsolvable conditions.
5. Output ONLY the valid JSON object.
"""
    try:
        res = subprocess.run(
            [HERMES_BIN, "-z", prompt],
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            timeout=120
        )
        out = (res.stdout or '').strip()
        # JSON 추출
        quiz_data = None
        ai_extracted_title = ""
        if "{" in out and "}" in out:
            start = out.find("{")
            end = out.rfind("}") + 1
            json_str = out[start:end]
            try:
                quiz_data = json.loads(json_str, strict=False)
            except Exception:
                try:
                    fixed = re.sub(r'\\(?![\\"])', r'\\\\', json_str)
                    quiz_data = json.loads(fixed, strict=False)
                except Exception as inner_e:
                    print(f"JSON 파싱 상세 오류: {inner_e}")

            # 혹시 JSON 파싱이 실패했더라도 정규식으로 AI가 작성한 title 필드 직접 추출
            if quiz_data and quiz_data.get("title"):
                ai_extracted_title = quiz_data.get("title").strip()
            else:
                tm = re.search(r'"title"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', json_str)
                if tm:
                    ai_extracted_title = tm.group(1).strip()

        if quiz_data:
            if ai_extracted_title:
                quiz_data["title"] = ai_extracted_title
            # 자동 교정: 중국어 잔재 및 볼록성 반대 표기 정제
            try:
                raw_s = json.dumps(quiz_data, ensure_ascii=False)
                raw_s = raw_s.replace("的一般형", "의 일반형")
                raw_s = re.sub(r'a\s*(&gt;|>)\s*0\s*—\s*위로\s*볼록', r'a \1 0 — 아래로 볼록', raw_s)
                raw_s = re.sub(r'a\s*(&lt;|<)\s*0\s*—\s*아래로\s*볼록', r'a \1 0 — 위로 볼록', raw_s)
                quiz_data = json.loads(raw_s)
            except Exception:
                pass
            return quiz_data
    except Exception as e:
        print(f"AI 호출 실패: {e}")

    # Fallback 기본 템플릿
    fallback_title = ai_extracted_title or (title if not is_title_empty else make_smart_fallback_title(content))
    return {
        "title": fallback_title,
        "symbols": [{"sym": "$x$", "desc": "미지수"}],
        "levels": [
            {
                "title": "🔰 제1단계 · 기본 개념 확인",
                "knowledge": f"{fallback_title}을(를) 풀기 위한 기본 개념을 점검합니다.",
                "questions": [
                    {
                        "stem": "다음 중 문제의 조건을 만족하는 기본 성질은 무엇인가요?",
                        "options": ["조건 A 성립", "조건 B 성립", "조건 C 성립", "조건 D 성립", "조건 E 성립"],
                        "answer": 1,
                        "exp": "문제의 기본 성질에 의해 1번이 타당합니다."
                    }
                ]
            }
        ],
        "final": {
            "stem": content,
            "options": ["1", "2", "3", "4", "5"],
            "answer": 3,
            "exp": f"풀이 해설: {hint or '단계별 풀이를 통해 정답을 도출합니다.'}",
            "solution": f"문제 원본: {content}\n해설: {hint}"
        }
    }

def create_and_publish_quiz(title, content, hint, reporter):
    """
    퀴즈를 생성하고 board/{slug}.html 저장, index.json 등록 및 Git 푸시까지 완료합니다.
    제목이 없을 경우 문제 내용을 분석해 고품질 수학 제목을 자동 생성합니다.
    """
    print(f"\n[AI_BUILDER] 신규 퀴즈 생성 시작 (신청자: {reporter}, 입력 제목: '{title or '(없음 - 자동생성)'}')")
    
    # 1. 퀴즈 구조 생성 (AI가 지문/수식을 분석하여 문제 제목 자동 도출)
    quiz_data = build_quiz_with_ai(title, content, hint)
    
    # 2. 최종 제목 확정 (AI 분석 제목 우선 채택)
    ai_title = (quiz_data.get("title") or "").strip()
    generic_titles = ["수학 퀴즈", "TEST", "test", "수학 문제", "자동 생성", "새 퀴즈", "제목 없음", ""]
    
    if ai_title and ai_title not in generic_titles:
        final_title = ai_title
    elif title and title.strip() not in generic_titles:
        final_title = title.strip()
    else:
        final_title = make_smart_fallback_title(content)
        
    quiz_data["title"] = final_title
    print(f"  ↳ 확정된 퀴즈 제목: '{final_title}'")
    
    # 3. 고유 slug 생성 (8자리 hex)
    slug = hashlib.md5((final_title + str(time.time())).encode('utf-8')).hexdigest()[:8]
    quiz_data["slug"] = slug
    quiz_data["original_content"] = content
    
    # 4. HTML 생성
    html_content = generator.generate_html(quiz_data)
    
    # 5. mathedu-room.js 및 수업 연동 스크립트 주입
    if "mathedu-room.js" not in html_content:
        if "</body>" in html_content:
            html_content = html_content.replace("</body>", '<script src="../mathedu-room.js"></script>\n</body>')
        else:
            html_content += '\n<script src="../mathedu-room.js"></script>'
            
    # 6. 파일 저장
    html_path = os.path.join(BOARD_DIR, f"{slug}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  ↳ HTML 저장 완료: board/{slug}.html")

    # 7. board/index.json에 새 퀴즈 최상단 추가
    now_str = datetime.now(KST).strftime('%Y-%m-%d %H:%M')
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            idx = json.load(f)
    except Exception:
        idx = []
        
    idx.insert(0, {
        "title": final_title,
        "slug": slug,
        "time": now_str
    })
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"  ↳ board/index.json 메타데이터 등록 완료: '{final_title}'")

    # 8. Git commit & push
    deploy_ok = False
    try:
        subprocess.run(["git", "add", f"board/{slug}.html", "board/index.json"], cwd=REPO_DIR, check=True)
        commit_msg = f"feat(quiz): auto-generate new quiz '{final_title}' ({slug})"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
        deploy_ok = True
        print(f"  ↳ ✅ GitHub Pages 배포 완료")
    except Exception as e:
        print(f"  ↳ ⚠️ Git 배포 오류: {e}")

    # 9. 텔레그램 알림 발송
    quiz_url = f"https://min7014.github.io/mathedu/board/{slug}.html"
    telegram_msg = (
        f"🎉 <b>[mathedu 신규 퀴즈 자동 생성 & 배포 완료]</b>\n\n"
        f"• <b>제목</b>: {final_title}\n"
        f"• <b>출제자</b>: {reporter}\n"
        f"• <b>퀴즈 링크</b>: <a href='{quiz_url}'>{quiz_url}</a>\n"
        f"• <b>배포 상태</b>: {'✅ 배포 완료' if deploy_ok else '⚠️ 로컬 생성 완료 (푸시 확인 필요)'}\n"
        f"• <b>생성 시각</b>: {now_str}"
    )
    send_telegram(telegram_msg)
    
    return slug, quiz_url, final_title

if __name__ == '__main__':
    if len(sys.argv) > 1:
        t = sys.argv[1]
        c = sys.argv[2] if len(sys.argv) > 2 else t
        create_and_publish_quiz(t, c, "", "테스트출제자")
    else:
        print("사용법: python _auto_quiz_builder.py <제목> <내용>")
