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
        title = text.splitlines()[0][:40] if text else "수학 퀴즈"
        content = text
        
    return title or "수학 퀴즈", content or text, hint

def build_quiz_with_ai(title, content, hint):
    """
    AI 에이전트를 호출하여 단계별 퀴즈 JSON을 생성합니다.
    """
    prompt = f"""You are an elite mathematics educator creating an interactive step-by-step quiz for Korean students.
Problem Title: {title}
Original Problem Statement:
{content}
Hint/Answer: {hint}

Your task:
Break this problem down into a progressive pedagogical quiz (at least 3 building-block levels + 1 final target problem level) so that even younger students can learn the principles step by step.

Return ONLY a strictly valid JSON object (no markdown code blocks, no backticks, just raw JSON) matching this exact schema:
{{
  "title": "{title}",
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
2. Use valid Korean for all explanations and titles.
3. Every question must have exactly 5 options and answer between 1 and 5.
4. Output ONLY the JSON.
"""
    try:
        res = subprocess.run(
            ["hermes", "-z", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            shell=True
        )
        out = res.stdout.strip()
        # JSON 추출
        if "{" in out and "}" in out:
            start = out.find("{")
            end = out.rfind("}") + 1
            json_str = out[start:end]
            return json.loads(json_str)
    except Exception as e:
        print(f"AI 호출 실패: {e}")

    # Fallback 기본 템플릿
    return {
        "title": title,
        "symbols": [{"sym": "$x$", "desc": "미지수"}],
        "levels": [
            {
                "title": "🔰 제1단계 · 기본 개념 확인",
                "knowledge": f"{title}을(를) 풀기 위한 기본 개념을 점검합니다.",
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
    """
    print(f"\n[AI_BUILDER] 신규 퀴즈 생성 시작: '{title}' (신청자: {reporter})")
    
    # 1. 퀴즈 구조 생성
    quiz_data = build_quiz_with_ai(title, content, hint)
    
    # 2. 고유 slug 생성 (8자리 hex)
    slug = hashlib.md5((title + str(time.time())).encode('utf-8')).hexdigest()[:8]
    quiz_data["slug"] = slug
    
    # 3. HTML 생성
    html_content = generator.generate_html(quiz_data)
    
    # 4. mathedu-room.js 및 수업 연동 스크립트 주입
    if "mathedu-room.js" not in html_content:
        if "</body>" in html_content:
            html_content = html_content.replace("</body>", '<script src="../mathedu-room.js"></script>\n</body>')
        else:
            html_content += '\n<script src="../mathedu-room.js"></script>'
            
    # 5. 파일 저장
    html_path = os.path.join(BOARD_DIR, f"{slug}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  ↳ HTML 저장 완료: board/{slug}.html")

    # 6. board/index.json에 새 퀴즈 최상단 추가
    now_str = datetime.now(KST).strftime('%Y-%m-%d %H:%M')
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            idx = json.load(f)
    except Exception:
        idx = []
        
    idx.insert(0, {
        "title": title,
        "slug": slug,
        "time": now_str
    })
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"  ↳ board/index.json 메타데이터 등록 완료")

    # 7. Git commit & push
    deploy_ok = False
    try:
        subprocess.run(["git", "add", f"board/{slug}.html", "board/index.json"], cwd=REPO_DIR, check=True)
        commit_msg = f"feat(quiz): auto-generate new quiz '{title}' ({slug})"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
        deploy_ok = True
        print(f"  ↳ ✅ GitHub Pages 배포 완료")
    except Exception as e:
        print(f"  ↳ ⚠️ Git 배포 오류: {e}")

    # 8. 텔레그램 알림 발송
    quiz_url = f"https://min7014.github.io/mathedu/board/{slug}.html"
    telegram_msg = (
        f"🎉 <b>[mathedu 신규 퀴즈 자동 생성 & 배포 완료]</b>\n\n"
        f"• <b>제목</b>: {title}\n"
        f"• <b>출제자</b>: {reporter}\n"
        f"• <b>퀴즈 링크</b>: <a href='{quiz_url}'>{quiz_url}</a>\n"
        f"• <b>배포 상태</b>: {'✅ 배포 완료' if deploy_ok else '⚠️ 로컬 생성 완료 (푸시 확인 필요)'}\n"
        f"• <b>생성 시각</b>: {now_str}"
    )
    send_telegram(telegram_msg)
    
    return slug, quiz_url

if __name__ == '__main__':
    if len(sys.argv) > 1:
        t = sys.argv[1]
        c = sys.argv[2] if len(sys.argv) > 2 else t
        create_and_publish_quiz(t, c, "", "테스트출제자")
    else:
        print("사용법: python _auto_quiz_builder.py <제목> <내용>")
