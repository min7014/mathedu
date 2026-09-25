#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_jarvis_ai_responder.py — 안티그래비티(Antigravity) 전방위 자동 응답 엔진
@jarvis7014_bot으로 들어오는 M님의 모든 질문(수학, 코딩, 코인/주식 시황, 날씨, 일상, 상식 등)에 대해
실시간 데이터(업비트 시세, 기상청/Open-Meteo 날씨 등)를 연동하고
안티그래비티 고지능 AI 모델(Solar-Pro, Step-3.7, Ling-3.0)을 통해
완벽한 맞춤형 답변을 자동 생성 및 텔레그램으로 전송합니다.
"""
import os, sys, json, argparse, subprocess, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
HERMES_HOME = os.environ.get("HERMES_HOME") or os.path.expanduser(
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes")
)
HERMES_CLI = os.path.join(HERMES_HOME, 'hermes-agent', 'venv', 'Scripts', 'hermes.exe')
HERMES_DELEGATED = 'HERMES_DELEGATED'  # 루프 방지 env var
AGENT_DIR = os.path.join(HERMES_HOME, "hermes-agent")
if os.path.isdir(os.path.join(AGENT_DIR, "hermes_cli")):
    sys.path.insert(0, AGENT_DIR)

from hermes_cli.auth import resolve_nous_access_token

KST = timezone(timedelta(hours=9))
INQUIRIES_LOG = os.path.join(REPO_DIR, '_jarvis_inquiries.json')
TELEGRAM_BOT_TOKEN = "8395764751:AAH5hP8KGIKrrSGaIp_PC2ieEZPDfGleGqM"

WEEKDAY_KR = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

SYSTEM_PROMPT = """You are Antigravity (안티그래비티), an elite AI assistant, mathematician, software engineer, and personal advisor built for M님.
You communicate directly with M님 via Telegram (@jarvis7014_bot).

Core Principles:
1. Universal Capability (모든 질문에 충실히 답변):
   - Answer ANY and ALL questions from M님 across every domain: mathematics, programming, web development, crypto/stock trading, weather, science, philosophy, and daily conversation.
   - Tone: Polite, warm, clear, and respectful Korean (반드시 존댓말 사용, M님 호칭).
   - Concise yet thorough, without unnecessary corporate fluff.

2. Mathematics & Code:
   - 100% mathematically rigorous. No arithmetic hallucinations.
   - For formulas, use clean notation: f(x), x^2, lim_{x->2}, fractions \\frac{a}{b}.
   - For mathedu quizzes: provide laddered, step-by-step intuitive and geometric explanations.

3. Crypto & Trading — M-Parity Framework (M님 시스템의 핵심):
   M님은 10년+ 시스템 트레이딩 경력을 가진 트레이더이며, 아래 프레임워크를 기반으로 운영합니다. 이 철학을 존중하고 이해한 위에서 답변해야 합니다.

   ★ 두 기둥:
   - ①시간은 나의 편(예측이 틀려도 시간이 적으로 작용하지 않게 설계, 생존=수익, 에르고딕성)
   - ②비예측 기반 변동성 수익(박스권 진동을 비예측 구조로 흡수)

   ★ 아래층(비예측 제약) — 절대 위반 불가:
   - 총자산 일정비율 slice (마틴게일 금지)
   - cash floor (현금 바닥 유지, 레버리지=1 고정)
   - max_hold·집중상한·유동성하한·비용예산
   - 붕괴게이트·슬라이스
   - "어떤 단일 예측도 안 죽임"이 목표 (예측 제로가 아님)

   ★ 명칭: M-Parity·현금바닥바벨·시간우호적생존구조
   - 위층(예측): 밴드/회귀/스캐너 — 틀릴 수 있음
   - 아래층(비예측): 자산비율·cash floor·max_hold·집중상한
   - 핵심: 예측 없이, 시간이 우호적인 상태에서 변동성만 먹는다
   - 급등급락은 잡을 수 없음, 시장은 대부분 박스권(횡보)

   ★ 트레이딩 하드게이트:
   - 백테스트(승률/MDD/수익률 기준 통과) 전 신규 전략 실전 적용 금지
   - 안건→백테스트검증→기준통과→적용 순서 엄수

   ★ M님 투자철학 참고 문서: C:\\Users\\min\\investment_philosophy.md

4. Weather & Real-time Info:
   - When real-time context (weather, date, crypto ticker) is provided, incorporate it directly into your answer.

5. User Context:
   - M님은 한국 창원에 거주 중. 10년+ 시스템 트레이딩 경력.
   - M님은 표면적 임시방편이 아닌 '근본적 해결'을 강하게 선호함.
   - M님은 영어 + 한국어 이중 언어로 답변받기를 원함.
"""

def fetch_live_crypto_summary():
    """업비트 주요 가상자산 실시간 시세 요약"""
    try:
        url = 'https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH,KRW-SOL,KRW-XRP,KRW-DOGE'
        req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity/1.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        tickers = json.loads(resp.read().decode('utf-8'))
        lines = []
        name_map = {
            'KRW-BTC': '비트코인(BTC)',
            'KRW-ETH': '이더리움(ETH)',
            'KRW-SOL': '솔라나(SOL)',
            'KRW-XRP': '리플(XRP)',
            'KRW-DOGE': '도지코인(DOGE)'
        }
        for t in tickers:
            m = t.get('market')
            name = name_map.get(m, m)
            price = t.get('trade_price', 0)
            rate = t.get('signed_change_rate', 0) * 100
            lines.append(f"- {name}: {price:,.0f}원 ({rate:+.2f}%)")
        return "실시간 업비트 주요 시세:\n" + "\n".join(lines)
    except Exception as e:
        return f"(업비트 시세 조회 지연: {e})"

def fetch_live_weather_summary(city="창원"):
    """창원 지역 실시간 기상 정보 요약 (Open-Meteo)"""
    try:
        # 창원시청 좌표: 위도 35.228, 경도 128.681
        url = "https://api.open-meteo.com/v1/forecast?latitude=35.228&longitude=128.681&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FSeoul"
        req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity/1.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode('utf-8'))
        cw = data.get('current_weather', {})
        daily = data.get('daily', {})
        
        temp = cw.get('temperature')
        wind = cw.get('windspeed')
        max_t = daily.get('temperature_2m_max', [None])[0]
        min_t = daily.get('temperature_2m_min', [None])[0]
        rain_prob = daily.get('precipitation_probability_max', [None])[0]
        
        w_code = cw.get('weathercode', 0)
        # WMO Weather interpretation codes
        if w_code == 0:
            condition = "맑음"
        elif w_code in [1, 2, 3]:
            condition = "대체로 맑거나 구름 다소 있음"
        elif w_code in [45, 48]:
            condition = "안개"
        elif w_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            condition = "비 또는 소나기"
        elif w_code in [71, 73, 75, 85, 86]:
            condition = "눈"
        elif w_code >= 95:
            condition = "뇌우"
        else:
            condition = "흐림"
            
        return f"창원 실시간 날씨: 현재 기온 {temp}℃, 상태: {condition}, 오늘 최고 {max_t}℃ / 최저 {min_t}℃, 강수확률 {rain_prob}%, 풍속 {wind}km/h"
    except Exception as e:
        return f"(날씨 정보 조회 지연: {e})"

def build_context_injection(query):
    """질문 키워드에 따라 최신 실시간 정보를 동적으로 조합"""
    now = datetime.now(KST)
    weekday_str = WEEKDAY_KR[now.weekday()]
    now_str = now.strftime(f'%Y년 %m월 %d일 ({weekday_str}) %H:%M KST')
    
    injections = [f"[현재 시각: {now_str}]"]
    
    q_lower = query.lower()
    
    # 1. 코인 / 트레이딩 관련 질문
    if any(k in q_lower for k in ['코인', '비트코인', 'btc', 'eth', '이더', '시황', '업비트', '가상자산', '트레이딩', '시세', '브리핑']):
        injections.append(f"[실시간 가상자산 시황]\n{fetch_live_crypto_summary()}")
        
    # 2. 날씨 관련 질문
    if any(k in q_lower for k in ['날씨', '기온', '비오', '우산', '온도', '비 오', '미세먼지', '흐림', '맑음']):
        injections.append(f"[실시간 기상 정보]\n{fetch_live_weather_summary()}")
        
    # 3. mathedu / 퀴즈 관련 질문
    if any(k in q_lower for k in ['퀴즈', 'mathedu', '수학', '문제', 'slug', '게시판']):
        try:
            idx_p = os.path.join(REPO_DIR, 'board', 'index.json')
            if os.path.exists(idx_p):
                with open(idx_p, 'r', encoding='utf-8') as f:
                    idx = json.load(f)[:5]
                    recent_info = "최근 생성된 mathedu 퀴즈 목록:\n" + "\n".join(f"- {it.get('title')} (slug: {it.get('slug')})" for it in idx)
                    injections.append(f"[mathedu 현황]\n{recent_info}")
        except Exception:
            pass

    return "\n\n".join(injections)

def load_conversation_history(max_entries=10):
    """이전 대화 이력을 불러와 컨텍스트로 반환"""
    try:
        if not os.path.exists(INQUIRIES_LOG):
            return ""
        with open(INQUIRIES_LOG, 'r', encoding='utf-8') as f:
            records = json.load(f)
        # 가장 최근 max_entries개만 사용
        recent = records[:max_entries]
        if not recent:
            return ""
        lines = []
        for r in recent:
            q = r.get('query', '')
            a = r.get('answer', '')[:500]  # 답변은 길이 제한
            if q and a:
                lines.append(f"[{r.get('time', '')}] M님: {q}")
                lines.append(f"안티그래비티: {a}")
        return "\n\n".join(lines)
    except Exception:
        return ""

def handle_pc_action(query):
    """M님의 PC 직접 제어 액션 (음악 재생, 유튜브, 웹사이트 열기 등)"""
    import subprocess
    q_lower = query.lower()
    
    # 1. 음악 / 유튜브 / 영상 재생 명령
    if any(k in q_lower for k in ['틀어줘', '재생해줘', '들려줘', '플레이해줘', '켜줘', '틀어']):
        # 아이브 (IVE) - I AM
        if any(k in q_lower for k in ['아이브', '아이엠', 'i am', 'ive']):
            url = 'https://www.youtube.com/watch?v=6ZUIwj3FgUY'
            try:
                subprocess.Popen(['powershell', '-Command', f'Start-Process "{url}"'], shell=True)
                return (
                    "🎶 M님! 컴퓨터에서 **아이브(IVE)의 'I AM'** 공식 뮤직비디오를 바로 재생해 드렸습니다!\n\n"
                    f"▶️ [IVE - 'I AM' 공식 MV 감상하기]({url})\n\n"
                    "신나게 감상하시면서 기분 좋은 시간 보내세요! ✨"
                )
            except Exception as e:
                return f"⚠️ 재생 실행 중 오류가 발생했습니다: {e}"

        # 기타 노래 / 음악 검색 재생
        clean_target = query
        for rw in ['틀어줘', '재생해줘', '들려줘', '플레이해줘', '켜줘', '틀어', '유튜브에서', '유튜브', '노래', '음악', '좀']:
            clean_target = clean_target.replace(rw, '')
        clean_target = clean_target.strip()
        if clean_target:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(clean_target)}"
            try:
                subprocess.Popen(['powershell', '-Command', f'Start-Process "{search_url}"'], shell=True)
                return (
                    f"🎵 M님! 컴퓨터에서 **'{clean_target}'**을(를) 바로 재생/검색해 드렸습니다!\n\n"
                    f"▶️ [YouTube 바로가기]({search_url})"
                )
            except Exception as e:
                return f"⚠️ 재생 실행 중 오류가 발생했습니다: {e}"

    # 2. mathedu 사이트 / 대시보드 열기
    if any(k in q_lower for k in ['대시보드 열어줘', 'mathedu 열어줘', '홈페이지 열어줘']):
        url = 'https://min7014.github.io/mathedu/'
        if '대시보드' in q_lower:
            url += 'dashboard-static.html'
        try:
            subprocess.Popen(['powershell', '-Command', f'Start-Process "{url}"'], shell=True)
            return f"🖥️ M님! 컴퓨터에서 mathedu 페이지를 열었습니다:\n{url}"
        except Exception as e:
            return f"⚠️ 페이지 열기 오류: {e}"

    return None

def delegate_to_hermes(text):
    """Hermes에게 위임하여 도구/스킬 접근 (루프 방지 가드 포함)"""
    if os.environ.get(HERMES_DELEGATED) == '1':
        return ''  # 이미 위임 중이면 루프 방지
    if not os.path.isdir(os.path.join(HERMES_HOME, 'hermes-agent')):
        return ''
    try:
        env = {**os.environ, HERMES_DELEGATED: '1', 'HERMES_HOME': HERMES_HOME, 'HOME': 'C:/Users/min'}
        r = subprocess.run(
            [HERMES_CLI, '-z', text],
            cwd='C:/Users/min', env=env,
            capture_output=True, timeout=90
        )
        if r.returncode == 0 and r.stdout.strip():
            raw_text = r.stdout.decode('utf8')
            filtered = [l for l in raw_text.split(chr(10)) if l.strip() and not l.startswith('Query:') and not l.startswith('Initializing')]
            return chr(10).join(filtered).strip()
        return ''
    except Exception:
        return ''

def generate_ai_response(query, user_name="M님", image_path=None):
    # 0. PC 직접 제어 액션 감지 (음악 재생 등)
    if not image_path:
        action_resp = handle_pc_action(query)
        if action_resp:
            return action_resp

    try:
        token = resolve_nous_access_token(timeout_seconds=15.0)
    except Exception as e:
        return f"⚠️ [안티그래비티 인증 오류] 토큰 갱신 실패: {e}"

    url = 'https://inference-api.nousresearch.com/v1/chat/completions'
    context_str = build_context_injection(query)
    conv_history = load_conversation_history(max_entries=6)

    system_content = SYSTEM_PROMPT
    if conv_history:
        system_content += f"\n\n[이전 대화 맥락 — 참고]\n{conv_history}"
    if context_str:
        system_content += f"\n\n[실시간 시스템 컨텍스트]\n{context_str}"

    # 이미지 입력이 있는 경우 멀티모달(Vision) 처리
    if image_path and os.path.exists(image_path):
        import base64
        ext = os.path.splitext(image_path)[1].lower().lstrip('.')
        mime = 'image/png' if ext == 'png' else 'image/jpeg'
        try:
            with open(image_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('ascii')
            data_url = f"data:{mime};base64,{b64}"
            
            vision_query = query.strip() if query and query.strip() else "이 이미지(사진)를 자세히 분석하고, 문제나 내용을 친절하고 명확하게 설명/풀이해 주세요."
            user_content = [
                {"type": "text", "text": vision_query},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]
            payload = json.dumps({
                "model": "stepfun/step-3.7-flash:free",
                "messages": [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ],
                "temperature": 0.2,
                "max_tokens": 2000
            }).encode('utf-8')
            
            req = urllib.request.Request(
                url, data=payload,
                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
            )
            resp = urllib.request.urlopen(req, timeout=35)
            res = json.loads(resp.read().decode('utf-8'))
            msg = res['choices'][0]['message']
            answer = (msg.get('content') or msg.get('reasoning') or "").strip()
            if answer:
                return answer
        except Exception as e:
            return f"⚠️ 이미지 분석 중 오류가 발생했습니다: {e}"

    # 일반 텍스트 질문 처리
    messages = [
        {"role": "system", "content": system_content},
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

    # ── 폴백: Hermes에게 위임 (도구/스킬 필요 시) ──
    hermes_resp = delegate_to_hermes(query)
    if hermes_resp:
        return hermes_resp

    return f"⚠️ 안티그래비티 답변 생성 중 일시적 지연이 발생했습니다: {last_err}"

def record_inquiry(query, answer, user="M님", chat_id="43453234"):
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
    records = records[:100]
    with open(INQUIRIES_LOG, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def send_telegram(chat_id, text):
    """텔레그램 메시지 직접 전송"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        # 4000자 초과 시 분할 전송
        chunks = [text[i:i+3900] for i in range(0, len(text), 3900)]
        for chunk in chunks:
            data = urllib.parse.urlencode({'chat_id': chat_id, 'text': chunk}).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"⚠️ 텔레그램 전송 실패: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", default="이 이미지를 분석해 주세요.", help="질문 내용")
    parser.add_argument("--image", "-i", default=None, help="이미지 파일 경로")
    parser.add_argument("--user", "-u", default="M님", help="질문자 이름")
    parser.add_argument("--chat_id", "-c", default="43453234", help="텔레그램 chat_id")
    parser.add_argument("--send", "-s", action="store_true", help="텔레그램으로 바로 발송")
    args = parser.parse_args()

    answer = generate_ai_response(args.query, args.user, args.image)
    log_query = f"[사진/이미지] {args.query}" if args.image else args.query
    record_inquiry(log_query, answer, args.user, args.chat_id)

    if args.send:
        send_telegram(args.chat_id, answer)

    print(answer)

if __name__ == '__main__':
    main()
