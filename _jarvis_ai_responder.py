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
        # 가장 최근 max_entries개를 시간 순서(과거 -> 최신)로 배치
        recent = records[:max_entries]
        if not recent:
            return ""
        lines = []
        for r in reversed(recent):
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

# ── 동적 모델 발견 (근본 해결: 하드코딩 모델명 제거) ──
# 라이브 /v1/models 목록에서 :free 모델을 실시간 조회 → 프로브 → 살아있는 것만 폴백 체인에 등록.
# 모델이 무료기간 종료/404로 죽어도 다음 실행 때 자동으로 우회하므로 "명목상 모델 문제"가 시스템을 멈추지 않음.
_MODEL_CACHE = {"ts": 0, "chain": []}
_MODEL_CACHE_TTL = 1800  # 30분

def discover_free_models(token, timeout=20):
    """Nous inference-api에서 사용 가능한 :free 모델 ID 목록을 라이브 조회."""
    try:
        req = urllib.request.Request(
            'https://inference-api.nousresearch.com/v1/models',
            headers={'Authorization': f'Bearer {token}'}
        )
        d = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8'))
        ids = [x.get('id', '') for x in d.get('data', [])]
        return [i for i in ids if i and ':free' in i]
    except Exception:
        return []

def probe_model(token, model, timeout=45):
    """모델에 '2'를 반환하는 초경량 프로브를 보내 생존 여부 판정."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "1+1=? 숫자만 답해"}],
        "max_tokens": 50
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://inference-api.nousresearch.com/v1/chat/completions',
        data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        res = json.loads(resp.read().decode('utf-8'))
        msg = res['choices'][0]['message']
        return bool((msg.get('content') or msg.get('reasoning') or '').strip())
    except Exception:
        return False

def resolve_model_chain(token):
    """살아있는 free 모델 체인을 캐시 기반으로 반환. 캐시 만료/빈 체인이면 재발견."""
    import time as _time
    now = _time.time()
    if _MODEL_CACHE["chain"] and (now - _MODEL_CACHE["ts"]) < _MODEL_CACHE_TTL:
        return _MODEL_CACHE["chain"]

    discovered = discover_free_models(token)
    # 우선순위: step-5 → laguna-s → solar-mini4 → longcat → 나머지
    def _rank(mid):
        prefs = ["stepfun/step-5-preview", "poolside/laguna-s-2.1", "upstage/solar-mini4", "meituan/longcat-2.5"]
        for idx, p in enumerate(prefs):
            if p in mid:
                return idx
        return 99
    discovered.sort(key=_rank)

    chain = []
    for mid in discovered:
        if probe_model(token, mid):
            chain.append(mid)
        if len(chain) >= 3:  # 상위 3개만 확보하면 충분 (프로브 비용 절감)
            break

    if chain:
        _MODEL_CACHE["chain"] = chain
        _MODEL_CACHE["ts"] = now
    return chain

# ══════════════════════════════════════════════════════════════════════
# [B방식] 안티그래비티 단일 인터페이스 아키텍처 보강
# 원칙: 아래층(비예측 제약)은 LLM 불개입 · 위층(예측/대화)만 LLM 경유
# ══════════════════════════════════════════════════════════════════════
import hashlib

# ── 1계층: 라우터 분리 ──
# 메시지를 아래층(lower)/위층(upper)으로 결정론적 분류. 이 분류 자체가 LLM을 쓰지 않음.
_LOWER_INTENT_RULES = [
    ('asset_ratio',   ['자산비율', '슬라이스', '자산 배분', '자산배분']),
    ('cash_floor',    ['현금 비율', '현금비율', 'cash floor', '캐시 플로어', '현금 바닥', '현금바닥', '현금 보유', '현금보유']),
    ('collapse_gate', ['붕괴게이트', '붕괴 게이트', '붕괴게 이트', '생존 게이트', '서킷브레이커']),
    ('bot_state',     ['봇 상태', '봇상태', '트레이딩 상태', '트레이딩상태', '포지션', '보유 종목', '보유종목', '잔고']),
]

def classify_message(query):
    """결정론적 메시지 분류기 — 아래층(lower) 명령은 LLM 없이 처리 대상."""
    if not query:
        return ('upper', None)
    q = query.lower()
    for intent, keywords in _LOWER_INTENT_RULES:
        for kw in keywords:
            if kw in q:
                return ('lower', intent)
    return ('upper', None)


# ── 2계층: 도구 화이트리스트 ──
# 아래층 도구 = 검증된 결정론적 API 전용. 위층(LLM) 도구와 물리적 분리.
LOWER_TOOL_WHITELIST = frozenset({
    'bot_state_api',      # /api/state (결정론적 HTTP 조회)
    'assets_history',     # assets_history.json (결정론적 파일 조회)
    'deterministic_rule', # 규칙 엔진 (순수 함수, LLM 불개입)
})

def _lower_tool_bot_state():
    """결정론적 봇 상태 조회 (HTTP). 봇 미가동 시 결정론적 '미가동' 반환."""
    try:
        req = urllib.request.Request('http://127.0.0.1:5000/api/state',
                                     headers={'User-Agent': 'Antigravity-LowerTier/1.0'})
        raw = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        return json.loads(raw), True
    except Exception:
        return None, False

def _lower_tool_assets_history():
    """결정론적 자산 이력 조회 (파일)."""
    path = r'C:\Users\min\Desktop\Hermes\assets_history.json'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            return data[-1], True
    except Exception:
        pass
    return None, False

# 아래층 규칙 엔진 — 순수 결정론 파라미터 (LLM 불개입 보장)
_LOWER_RULES = {
    'cash_floor_pct': 50.0,      # M-Parity 현금 바닥
    'asset_ratio_pct': 50.0,     # 투자 자산비율
    'collapse_gate_pct': -30.0,  # 붕괴 게이트 발동 임계 (총자산 -30%)
    'base_assets': 10000.0,      # 기준 자산
}

def _rule_engine_cash_floor(state):
    """현금 비율 규칙 판정 — 순수 결정론."""
    if not state:
        return None
    cash = float(state.get('cash', 0) or 0)
    total = float(state.get('total_assets', 0) or state.get('total', 0) or 0)
    if total <= 0:
        return None
    ratio = cash / total * 100.0
    floor = _LOWER_RULES['cash_floor_pct']
    if ratio >= floor:
        verdict = '정상'
    elif ratio >= floor * 0.6:
        verdict = '주의 (바닥 미달)'
    else:
        verdict = '위험 (바닥 심각 미달)'
    return {'cash_pct': round(ratio, 2), 'threshold': floor, 'verdict': verdict}

def _rule_engine_asset_ratio(state):
    """자산비율(슬라이스) 규칙 판정 — 순수 결정론."""
    if not state:
        return None
    total = float(state.get('total_assets', 0) or 0)
    if total <= 0:
        return None
    invest = total * (_LOWER_RULES['asset_ratio_pct'] / 100.0)
    return {'total': round(total, 0), 'invest_target': round(invest, 0),
            'ratio_pct': _LOWER_RULES['asset_ratio_pct']}

def _rule_engine_collapse_gate(state):
    """붕괴게이트 규칙 판정 — 순수 결정론."""
    if not state:
        return None
    total = float(state.get('total_assets', 0) or 0)
    base = float(state.get('initial_assets', 0) or _LOWER_RULES['base_assets'])
    if base <= 0:
        base = _LOWER_RULES['base_assets']
    pnl_pct = (total - base) / base * 100.0
    gate = pnl_pct <= _LOWER_RULES['collapse_gate_pct']
    return {'pnl_pct': round(pnl_pct, 2), 'gate_threshold': _LOWER_RULES['collapse_gate_pct'],
            'gate_triggered': gate}

def route_lower_tier(intent, query):
    """아래층 명령 라우팅 — LLM 불개입, 결정론적 도구+규칙엔진만 사용."""
    state, bot_alive = _lower_tool_bot_state()
    if not state:
        last, _ = _lower_tool_assets_history()
        state = {'total_assets': (last.get('total_assets', 0) if last else 0), 'cash': 0}

    src = '봇 가동 중' if bot_alive else '봇 미가동 — 마지막 기록 기준'

    if intent == 'cash_floor':
        r = _rule_engine_cash_floor(state)
        if not r:
            return None
        return (f"[아래층·결정론] 현금 비율: {r['cash_pct']}% (바닥 {r['threshold']}%) → {r['verdict']}\n"
                f"({src})")
    if intent == 'asset_ratio':
        r = _rule_engine_asset_ratio(state)
        if not r:
            return None
        return (f"[아래층·결정론] 자산비율: 총 {r['total']:,.0f}원 × {r['ratio_pct']}% = 투자 {r['invest_target']:,.0f}원\n"
                f"({src})")
    if intent == 'collapse_gate':
        r = _rule_engine_collapse_gate(state)
        if not r:
            return None
        gate = '🚨 발동' if r['gate_triggered'] else '✅ 정상'
        return (f"[아래층·결정론] 붕괴게이트: 손익 {r['pnl_pct']}% (임계 {r['gate_threshold']}%) → {gate}\n"
                f"({src})")
    if intent == 'bot_state':
        if not bot_alive:
            return ("[아래층·결정론] 봇 상태: 미가동\n"
                    "(single_trader.py 대시보드 127.0.0.1:5000 응답 없음)")
        pos = state.get('positions') or state.get('position') or '정보 없음'
        return (f"[아래층·결정론] 봇 상태: 가동 중\n"
                f"총자산: {float(state.get('total_assets', 0)):,.0f}원 / 현금: {float(state.get('cash', 0)):,.0f}원\n"
                f"포지션: {pos}")
    return None


# ── 3계층: 감사 로그 분리 ──
# 아래층 실행 로그는 LLM 응답 경로(INQUIRIES_LOG)와 별도 저장소에 기록.
LOWER_AUDIT_LOG = os.path.join(REPO_DIR, '_ag_audit_lower.jsonl')

def audit_lower_execution(intent, query, result):
    """아래층 실행 감사 기록 — LLM 응답 경로와 물리적으로 분리된 저장소."""
    try:
        entry = {
            'ts': datetime.now(KST).isoformat(),
            'tier': 'lower',
            'intent': intent,
            'query': (query or '')[:200],
            'result_sha': hashlib.sha256((result or '').encode('utf-8')).hexdigest()[:16],
            'llm_involved': False,
            'tools': sorted(LOWER_TOOL_WHITELIST & {'bot_state_api', 'deterministic_rule'}),
        }
        with open(LOWER_AUDIT_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except Exception:
        pass  # 감사 로그 실패가 아래층 응답을 막지 않음


def generate_ai_response(query, user_name="M님", image_path=None):
    # ── [B방식] 1계층 라우터: 아래층 명령은 LLM 불개입으로 결정론적 처리 ──
    if not image_path:
        tier, intent = classify_message(query)
        if tier == 'lower':
            result = route_lower_tier(intent, query)
            if result:
                audit_lower_execution(intent, query, result)
                return result
            # 결과 없으면 위층(LLM)으로 자연스럽게 fall through

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
                "model": resolve_model_chain(token)[0] if resolve_model_chain(token) else "stepfun/step-5-preview:free",
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

    # 동적 모델 체인 (죽은 모델 자동 우회). 실패 시 하드코딩 백업도 유지.
    candidate_models = resolve_model_chain(token)
    if not candidate_models:
        candidate_models = ["stepfun/step-5-preview:free", "upstage/solar-mini4:free", "poolside/laguna-s-2.1:free"]

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
            resp = urllib.request.urlopen(req, timeout=60)
            res = json.loads(resp.read().decode('utf-8'))
            msg = res['choices'][0]['message']
            answer = (msg.get('content') or msg.get('reasoning') or "").strip()
            if answer:
                return answer
            last_err = RuntimeError(f"{model}: 빈 응답")
            continue
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
