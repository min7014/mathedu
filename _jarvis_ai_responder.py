#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_jarvis_ai_responder.py — 안티그래비티(Antigravity) 텔레그램 자동 응답 엔진
@jarvis7014_bot으로 들어온 M님의 질문/문의에 대해
수학적 무결성, LaTeX 표기, mathedu 플랫폼 맥락을 탑재한
고지능 안티그래비티 답변을 자동 생성하여 반환합니다.
"""
import os, sys, json, argparse, urllib.request
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
HERMES_HOME = os.environ.get("HERMES_HOME") or os.path.expanduser(
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes")
)
AGENT_DIR = os.path.join(HERMES_HOME, "hermes-agent")
if os.path.isdir(os.path.join(AGENT_DIR, "hermes_cli")):
    sys.path.insert(0, AGENT_DIR)

from hermes_cli.auth import resolve_nous_access_token

KST = timezone(timedelta(hours=9))
INQUIRIES_LOG = os.path.join(REPO_DIR, '_jarvis_inquiries.json')

SYSTEM_PROMPT = """You are Antigravity (안티그래비티), an elite AI pair-programming and mathematics education expert built for M님's 'mathedu' platform.
You are responding directly to M님 via Telegram (@jarvis7014_bot).

Core Rules:
1. Tone & Persona:
   - Polite, clear, direct, and helpful Korean (존댓말).
   - Address M님 respectfully.
   - Concise yet thorough, without unnecessary fluff or sycophancy.
2. Mathematics & Code:
   - 100% mathematically rigorous. No arithmetic hallucinations.
   - For formulas, use standard mathematical notation or clean formatting. Note: Telegram Markdown/HTML parses standard text or `code`. Avoid unescaped special characters. Use readable notation like f(x), x^2, lim_{x->2}.
   - If asked about a quiz or problem in mathedu (e.g. 29afb597, continuous function, quadratic, etc.), provide exact, step-by-step verified explanations.
3. System Awareness:
   - Platform: mathedu (https://min7014.github.io/mathedu/)
   - Quizzes are laddered 5-choice interactive web quizzes starting from elementary concepts up to advanced calculus/algebra.
   - Provide direct answers and actionable insights.
"""

def generate_ai_response(query, user_name="M"):
    try:
        token = resolve_nous_access_token(timeout_seconds=15.0)
    except Exception as e:
        return f"⚠️ [안티그래비티 인증 오류] 토큰 갱신 실패: {e}"

    url = 'https://inference-api.nousresearch.com/v1/chat/completions'
    
    # mathedu 최근 퀴즈 현황 요약 주입
    recent_info = ""
    try:
        idx_p = os.path.join(REPO_DIR, 'board', 'index.json')
        if os.path.exists(idx_p):
            with open(idx_p, 'r', encoding='utf-8') as f:
                idx = json.load(f)[:5]
                recent_info = "최근 생성된 퀴즈 목록:\n" + "\n".join(f"- {it.get('title')} (slug: {it.get('slug')})" for it in idx)
    except Exception:
        pass

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\n\n[현재 mathedu 상태]\n{recent_info}"},
        {"role": "user", "content": query}
    ]

    candidate_models = [
        "upstage/solar-pro4:free",
        "stepfun/step-3.7-flash:free",
        "inclusionai/ling-3.0-flash-fin:free",
        "inclusionai/ling-3.0-flash-sante:free"
    ]

    last_err = None
    for model in candidate_models:
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1500
        }).encode('utf-8')

        req = urllib.request.Request(
            url, data=payload,
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        try:
            resp = urllib.request.urlopen(req, timeout=25)
            res = json.loads(resp.read().decode('utf-8'))
            answer = res['choices'][0]['message']['content'].strip()
            return answer
        except Exception as e:
            last_err = e
            continue

    return f"⚠️ 안티그래비티 답변 생성 중 일시적 지연이 발생했습니다: {last_err}"

def record_inquiry(query, answer, user="M", chat_id=""):
    now_str = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S KST')
    records = []
    if os.path.exists(INQUIRIES_LOG):
        try:
            with open(INQUIRIES_LOG, 'r', encoding='utf-8') as f:
                records = json.load(f)
        except Exception:
            records = []
    records.insert(0, {
        "time": now_str,
        "user": user,
        "chat_id": str(chat_id),
        "query": query,
        "answer": answer
    })
    # 최대 100건 보관
    records = records[:100]
    with open(INQUIRIES_LOG, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", required=True, help="질문 내용")
    parser.add_argument("--user", "-u", default="M님", help="질문자 이름")
    parser.add_argument("--chat_id", "-c", default="43453234", help="텔레그램 chat_id")
    args = parser.parse_args()

    answer = generate_ai_response(args.query, args.user)
    record_inquiry(args.query, answer, args.user, args.chat_id)

    # stdout으로 출력 (Hermes가 M님께 그대로 전송함)
    print(answer)

if __name__ == '__main__':
    main()
