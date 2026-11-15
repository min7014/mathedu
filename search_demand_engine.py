#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_demand_engine.py
===============================================================================
🔍 사용자 검색어 분리 저장 · 수요 분석 · 미충족(0건) 수학 수업자료 자동 제작 엔진

[회장님(min7014) 핵심 지침 (2026-11-15)]:
"그리고 검색어를 따로 저장하여 사용자가 무슨 자료를 요구하는지 파악하여
 관련자료가 없을 경우 관련 수업자료 제작을 하도록 하겠다."

주요 기능:
1. 전용 분리 저장소 운영 (오류신고와 철저히 분리):
   - 원시 이벤트 로그: `.agents/user_search_raw_logs.jsonl` (Git 제외)
   - 수요 집계 및 미충족 큐 DB: `assets/user_search_demand_db.json`
2. 실시간 커버리지 교차 검증:
   - `min7014.github.io` 심층 지식 DB (`1,113` 주제 / `3,400+` 자료)
   - `board/index.json` 단독 인터랙티브 디딤돌 수업 (`212+` 문항)
   - `board/archive_catalog.json` 기출 아카이브 (`16,548` 문항)
   - `video_lectures/catalog.json` 설명 영상 (`927+` 편)
3. 순수 수학 검증 게이트 (Rule 2 · Rule 4 · Rule 51) 통과 후 관련 자료가 0건인
   수학 개념·정리·주제에 대해 초등 눈높이 디딤돌(Rule 6) + 시각 SVG 도형·도식화 흐름도(Rule 7) +
   한·영 양방향(Rule 58) 인터랙티브 수업자료(`board/{slug}.html` + `offline/{slug}.html`) 자동 제작·배포!
===============================================================================
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import silent_subprocess  # noqa: F401 — Rule 48 100% 무창 백그라운드 실행 강제
except Exception:
    silent_subprocess = None

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = REPO_DIR / ".agents"
RAW_LOG_FILE = AGENTS_DIR / "user_search_raw_logs.jsonl"
SYNCED_SEARCH_KEYS_FILE = AGENTS_DIR / "synced_search_log_keys.json"
DEMAND_DB_FILE = REPO_DIR / "assets" / "user_search_demand_db.json"
PRIORITY_SLUGS_FILE = AGENTS_DIR / "search_priority_slugs.json"
PRODUCTION_RATE_FILE = AGENTS_DIR / "search_lesson_rate_state.json"
MAX_AUTO_LESSONS_PER_HOUR = 2


# ---------------------------------------------------------------------------
# 순수 수학 도메인 판별 사전 (Rule 2 · Rule 4 · Rule 51 엄수)
# ---------------------------------------------------------------------------
BLOCKED_NON_MATH_OR_TRADEMARK_TOKENS = (
    "트레이딩", "비트코인", "암호화폐", "이더리움", "주식", "코인", "선물옵션", "s-nova",
    "ignore previous", "system prompt", "powershell", "cmd.exe", "<script", "http://", "https://",
    "sat ", "amc ", "aime", "ap calculus", "ib math", "올림피아드", "imo ", "kmo ",
    "날씨", "게임", "유머", "연예", "배고파", "테스트", "test", "asdf",
)

PURE_MATH_LEXICON = (
    # 대수·수체계·함수
    "방정식", "부등식", "다항식", "인수분해", "항등식", "나머지정리", "조립제법", "복소수", "허수", "켤레",
    "이차함수", "삼차함수", "사차함수", "유리함수", "무리함수", "역함수", "합성함수", "절댓값", "가우스",
    "지수", "로그", "상용로그", "자연로그", "거듭제곱", "제곱근", "루트", "비례", "분수", "소수", "약수", "배수",
    "최대공약수", "최소공배수", "소인수", "기수법", "이진법", "집합", "명제", "필요충분", "대우", "귀류법",
    "수열", "등차", "등비", "귀납법", "점화식", "시그마", "부분분수", "계차", "피보나치", "카탈란",
    "행렬", "연립", "판별식", "근과 계수", "산술기하", "코시", "슈바르츠", "젠센", "산술평균", "기하평균",
    # 미적분·해석학
    "극한", "연속", "미분", "도함수", "접선", "극대", "극소", "변곡점", "오목", "볼록", "평균값", "롤의 정리",
    "사잇값", "중간값", "로피탈", "테일러", "매클로린", "적분", "부정적분", "정적분", "구분구적", "치환적분",
    "부분적분", "급수", "무한급수", "무한등비", "수렴", "발산", "미분방정식", "매개변수", "음함수", "속도", "가속도",
    "회전체", "단면적", "부피", "넓이", "곡선의 길이", "리만", "입실론", "델타",
    # 기하·삼각·벡터·이차곡선
    "삼각형", "사각형", "다각형", "오각형", "육각형", "정칠각형", "원주각", "중심각", "접선", "할선", "현",
    "내심", "외심", "무게중심", "수심", "방심", "오심", "구점원", "오일러 직선", "닮음", "합동", "평행", "수직",
    "피타고라스", "체바", "메넬라우스", "톨레미", "파푸스", "중선정리", "스튜어트", "헤론", "브라마굽타",
    "아폴로니우스", "데자르그", "파스칼", "브リアン숑", "심슨선", "나폴레옹", "몰리", "페르마 점", "토리첼리",
    "포물선", "타원", "쌍곡선", "이차곡선", "원뿔곡선", "단델린", "초점", "준선", "점근선", "이심률",
    "삼각비", "삼각함수", "사인", "코사인", "탄젠트", "사인법칙", "코사인법칙", "덧셈정리", "배각", "반각", "합성",
    "호도법", "라디안", "부채꼴", "벡터", "내적", "외적", "위치벡터", "법선벡터", "방향벡터",
    "공간도형", "삼수선", "이면각", "정사영", "구면", "정다면체", "다면체", "오일러 지표", "작도", "종이접기", "매듭",
    "좌표", "직선의 방정식", "원의 방정식", "평행이동", "대칭이동", "자취", "사이클로이드", "추적선", "포락선",
    # 확률·통계·이산·정수론
    "경우의 수", "순열", "조합", "중복순열", "중복조합", "원순열", "같은 것이 있는", "교란순열", "완전순열",
    "이항정리", "파스칼의 삼각형", "포함배제", "비둘기집", "확률", "조건부확률", "독립시행", "베이즈", "여사건",
    "기댓값", "평균", "분산", "표준편차", "이항분포", "정규분포", "표준정규분포", "표본평균", "신뢰구간", "모비율",
    "합동식", "모듈러", "페르마의 소정리", "오일러 정리", "중국인의 나머지", "유클리드 호제법", "디오판토스",
    "그래프 이론", "한붓그리기", "색칠", "점화", "생성함수", "정리", "공식", "증명", "기하", "대수", "미적", "함수",
    # English pure math terms
    "theorem", "proof", "lemma", "formula", "equation", "inequality", "polynomial", "quadratic", "cubic",
    "quartic", "function", "inverse", "logarithm", "exponential", "sequence", "series", "induction",
    "matrix", "determinant", "eigenvalue", "eigenvector", "cauchy", "schwarz", "am-gm", "jensen",
    "limit", "continuity", "derivative", "differentiation", "tangent", "inflection", "integral", "integration",
    "riemann", "taylor", "maclaurin", "differential", "convergence", "divergence",
    "triangle", "polygon", "circle", "inscribed", "circumcenter", "incenter", "centroid", "orthocenter",
    "pythagoras", "pythagorean", "ceva", "menelaus", "ptolemy", "stewart", "heron", "apollonius",
    "desargues", "pascal", "simson", "euler", "nine-point", "fermat", "napoleon", "morley",
    "parabola", "ellipse", "hyperbola", "conic", "dandelin", "focus", "directrix", "asymptote", "eccentricity",
    "sine", "cosine", "trigonometry", "trigonometric", "radian", "vector", "dot product", "cross product",
    "projection", "dihedral", "polyhedron", "cycloid", "envelope", "locus",
    "permutation", "combination", "derangement", "binomial", "pigeonhole", "inclusion-exclusion",
    "probability", "conditional", "bayes", "expectation", "variance", "normal distribution", "confidence",
    "modular", "congruence", "diophantine", "euclidean", "fibonacci", "catalan", "barycentric", "inversion",
)

EN_KO_BRIDGE = [
    ("pythagoras", "피타고라스"), ("pythagorean", "피타고라스"),
    ("ellipse", "타원"), ("parabola", "포물선"), ("hyperbola", "쌍곡선"), ("conic", "이차곡선"),
    ("dandelin", "단델린"), ("ceva", "체바"), ("menelaus", "메넬라우스"), ("ptolemy", "톨레미"),
    ("stewart", "스튜어트"), ("heron", "헤론"), ("pappus", "파푸스"), ("apollonius", "아폴로니우스"),
    ("euler", "오일러"), ("fermat", "페르마"), ("cauchy", "코시"), ("schwarz", "슈바르츠"),
    ("jensen", "젠센"), ("bayes", "베이즈"), ("taylor", "테일러"), ("riemann", "리만"),
    ("derangement", "교란순열"), ("pigeonhole", "비둘기집"), ("catalan", "카탈란"), ("fibonacci", "피보나치"),
    ("cycloid", "사이클로이드"), ("inversion", "반전기하"), ("barycentric", "무게중심"),
    ("calculus", "미적분"), ("derivative", "미분"), ("integral", "적분"), ("vector", "벡터"),
    ("normal distribution", "정규분포"), ("binomial", "이항"), ("sequence", "수열"),
    ("inscribed angle", "원주각"), ("projection", "정사영"), ("logarithm", "로그"),
]


def load_demand_db() -> dict:
    if DEMAND_DB_FILE.exists():
        try:
            data = json.loads(DEMAND_DB_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("total_search_events", 0)
                data.setdefault("queries", {})
                data.setdefault("unmet_lesson_queue", [])
                data.setdefault("produced_lessons", [])
                return data
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "updated_at": datetime.datetime.now().isoformat(),
        "total_search_events": 0,
        "queries": {},
        "unmet_lesson_queue": [],
        "produced_lessons": [],
    }


def save_demand_db(db: dict) -> None:
    DEMAND_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    db["updated_at"] = datetime.datetime.now().isoformat()
    DEMAND_DB_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_synced_keys() -> set[str]:
    if SYNCED_SEARCH_KEYS_FILE.exists():
        try:
            arr = json.loads(SYNCED_SEARCH_KEYS_FILE.read_text(encoding="utf-8"))
            if isinstance(arr, list):
                return set(str(x) for x in arr)
        except Exception:
            pass
    return set()


def _save_synced_keys(keys: set[str]) -> None:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    SYNCED_SEARCH_KEYS_FILE.write_text(
        json.dumps(sorted(keys)[-5000:], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def normalize_query_key(q: str) -> str:
    return re.sub(r"\s+", " ", (q or "").strip()).lower()


def is_verified_pure_math_topic(raw_query: str) -> tuple[bool, str]:
    """
    [3계층 순수 수학 검증 게이트]
    비수학·상표권·욕설·오입력·단순 자모를 배제하고 순수 수학교육 개념/정리/단원인지 판별합니다.
    """
    q = re.sub(r"\s+", " ", (raw_query or "").strip())
    if len(q) < 2 or len(q) > 70:
        return (False, "길이 부적합")
    if re.search(r"[ㄱ-ㅎㅏ-ㅣ]", q):
        return (False, "미완성 한글 자모 포함")

    low = q.lower()
    if any(b in low for b in BLOCKED_NON_MATH_OR_TRADEMARK_TOKENS):
        return (False, "보안·비수학·외부상표 필터 차단(Rule 2·4·51)")

    if any(term in low for term in PURE_MATH_LEXICON):
        return (True, "순수 수학 개념·용어 사전 일치")

    # 학년도/모평/번 문항 형태
    if re.search(r"(\d+\s*번|고[123]|모평|학평|수능)", q):
        return (True, "수학 문항 조건 검색")

    return (False, "수학 개념 사전 미일치 (단순 일반어 또는 오입력 추정)")


def evaluate_topic_coverage(raw_query: str) -> dict:
    """
    기존 자산(1,113개 심층 증명 DB, 212+ 단독 퀴즈, 16,548 기출 아카이브, 927+ 영상)에서
    해당 검색어 관련 자료가 존재하는지 정밀 교차 조사합니다.
    """
    q = normalize_query_key(raw_query)
    variants = [q]
    for en_w, ko_w in EN_KO_BRIDGE:
        if en_w in q and ko_w not in variants:
            variants.append(ko_w)
        if ko_w in q and en_w not in variants:
            variants.append(en_w)

    proof_hits = 0
    matched_proof_slugs: list[str] = []
    dk_path = REPO_DIR / "assets" / "min7014_deep_knowledge.json"
    if dk_path.exists():
        try:
            dk = json.loads(dk_path.read_text(encoding="utf-8"))
            for item in dk:
                hay = " ".join(
                    str(item.get(k) or "")
                    for k in ("title", "sub_domain_ko", "category", "breadcrumb", "core_concept")
                ).lower() + " " + " ".join(item.get("tags") or []).lower()
                if any(v in hay for v in variants):
                    proof_hits += 1
                    sl = str(item.get("slug") or item.get("id") or "")
                    if sl and len(matched_proof_slugs) < 5:
                        matched_proof_slugs.append(sl)
        except Exception:
            pass

    standalone_quiz_hits = 0
    b_idx_path = REPO_DIR / "board" / "index.json"
    if b_idx_path.exists():
        try:
            b_items = json.loads(b_idx_path.read_text(encoding="utf-8"))
            for qz in b_items:
                hay = (
                    f"{qz.get('title', '')} {qz.get('title_en', '')} "
                    f"{qz.get('subject', '')} {' '.join(qz.get('tags') or [])}"
                ).lower()
                if any(v in hay for v in variants):
                    standalone_quiz_hits += 1
        except Exception:
            pass

    archive_hits = 0
    arc_path = REPO_DIR / "board" / "archive_catalog.json"
    if arc_path.exists():
        try:
            arc = json.loads(arc_path.read_text(encoding="utf-8"))
            for c in arc:
                hay = f"{c.get('t', '')} {c.get('sub', '')} {' '.join(c.get('tg') or [])}".lower()
                if any(v in hay for v in variants):
                    archive_hits += 1
        except Exception:
            pass

    video_hits = 0
    v_cat_path = REPO_DIR / "video_lectures" / "catalog.json"
    if v_cat_path.exists():
        try:
            vcat = json.loads(v_cat_path.read_text(encoding="utf-8"))
            vitems = vcat.get("items", vcat) if isinstance(vcat, dict) else vcat
            if isinstance(vitems, list):
                for v in vitems:
                    hay = f"{v.get('title', '')} {v.get('title_en', '')} {v.get('category', '')}".lower()
                    if any(v_kw in hay for v_kw in variants):
                        video_hits += 1
        except Exception:
            pass

    total_hits = proof_hits + standalone_quiz_hits + archive_hits + video_hits
    return {
        "proof_hits": proof_hits,
        "standalone_quiz_hits": standalone_quiz_hits,
        "archive_hits": archive_hits,
        "video_hits": video_hits,
        "total_hits": total_hits,
        "matched_proof_slugs": matched_proof_slugs,
        "is_zero_material": total_hits == 0,
        "needs_standalone_lesson": (proof_hits == 0 and standalone_quiz_hits == 0),
    }


def _parse_search_sheet_row(r: dict) -> dict | None:
    slug = str(r.get("quiz_slug") or "").strip()
    if slug not in ("_search_log", "_search_gap"):
        return None
    raw_txt = str(r.get("text") or "").strip()
    m_q = re.search(r"\[검색어\]\s*(.*?)(?=\n\[|\Z)", raw_txt, flags=re.S)
    query = (m_q.group(1).strip() if m_q else raw_txt.splitlines()[0].strip()) if raw_txt else ""
    if not query:
        return None

    m_lang = re.search(r"\[언어\]\s*([A-Za-z]+)", raw_txt)
    m_src = re.search(r"\[출처\]\s*([A-Za-z0-9_-]+)", raw_txt)
    m_prio = re.search(r"\[우선요청\]\s*([YN])", raw_txt)
    web_hits_raw = str(r.get("question_num") or "0").strip()
    web_hits = int(web_hits_raw) if web_hits_raw.isdigit() else 0

    return {
        "timestamp": str(r.get("timestamp") or datetime.datetime.now().isoformat()),
        "sheet_slug": slug,
        "query": query,
        "lang": (m_lang.group(1).upper() if m_lang else "KO"),
        "source": (m_src.group(1) if m_src else "web"),
        "priority": bool(m_prio and m_prio.group(1) == "Y"),
        "web_reported_hits": web_hits,
        "raw_row": r,
    }


def record_search_event_locally(
    query: str,
    lang: str = "KO",
    source: str = "direct",
    priority: bool = False,
    timestamp: str | None = None,
) -> dict:
    """
    단일 검색어 이벤트를 원시 JSONL 로그와 수요 집계 DB(`user_search_demand_db.json`)에 기록하고,
    관련 자료가 없는 순수 수학 주제이면 `unmet_lesson_queue`에 자동 편입합니다.
    """
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = timestamp or datetime.datetime.now().isoformat()
    q_clean = re.sub(r"\s+", " ", query.strip())
    q_key = normalize_query_key(q_clean)

    cov = evaluate_topic_coverage(q_clean)
    is_math, math_reason = is_verified_pure_math_topic(q_clean)

    raw_event = {
        "timestamp": ts,
        "query": q_clean,
        "lang": lang,
        "source": source,
        "priority": priority,
        "is_math": is_math,
        "coverage": cov,
    }
    with open(RAW_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(raw_event, ensure_ascii=False) + "\n")

    db = load_demand_db()
    db["total_search_events"] = int(db.get("total_search_events", 0)) + 1
    queries_map = db.setdefault("queries", {})
    q_rec = queries_map.get(q_key) or {
        "display_query": q_clean,
        "count": 0,
        "first_searched_at": ts,
        "last_searched_at": ts,
        "langs": [],
        "sources": [],
        "is_pure_math": is_math,
        "coverage": cov,
    }
    q_rec["count"] = int(q_rec.get("count", 0)) + 1
    q_rec["last_searched_at"] = ts
    q_rec["is_pure_math"] = is_math
    q_rec["coverage"] = cov
    if lang not in q_rec["langs"]:
        q_rec["langs"].append(lang)
    if source not in q_rec["sources"]:
        q_rec["sources"].append(source)
    queries_map[q_key] = q_rec

    # 인기 증명 주제는 영상 렌더링 우선순위 큐에도 반영
    if cov["matched_proof_slugs"]:
        try:
            prio_list = []
            if PRIORITY_SLUGS_FILE.exists():
                prio_list = json.loads(PRIORITY_SLUGS_FILE.read_text(encoding="utf-8"))
            for sl in cov["matched_proof_slugs"]:
                if sl not in prio_list:
                    prio_list.insert(0, sl)
            PRIORITY_SLUGS_FILE.write_text(
                json.dumps(prio_list[:100], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    # 관련 자료가 없는(또는 단독 디딤돌·증명 자료가 전혀 없는) 순수 수학 주제 -> 미충족 제작 큐 등록!
    queued_new_gap = False
    already_produced = any(
        normalize_query_key(p.get("query", "")) == q_key for p in db.get("produced_lessons", [])
    )
    if is_math and not already_produced and (cov["is_zero_material"] or (priority and cov["needs_standalone_lesson"])):
        queue = db.setdefault("unmet_lesson_queue", [])
        existing_gap = next((g for g in queue if normalize_query_key(g.get("query", "")) == q_key), None)
        if existing_gap:
            existing_gap["request_count"] = int(existing_gap.get("request_count", 1)) + 1
            existing_gap["last_requested_at"] = ts
            if priority:
                existing_gap["priority"] = True
        else:
            queue.append(
                {
                    "query": q_clean,
                    "lang": lang,
                    "priority": priority,
                    "request_count": 1,
                    "first_requested_at": ts,
                    "last_requested_at": ts,
                    "status": "pending",
                    "coverage_snapshot": cov,
                    "math_check": math_reason,
                }
            )
            queued_new_gap = True

    save_demand_db(db)
    return {
        "query": q_clean,
        "is_math": is_math,
        "coverage": cov,
        "queued_new_gap": queued_new_gap,
    }


def sync_search_logs_from_sheets(preloaded_rows: list[dict] | None = None) -> dict:
    """
    Google Sheets(reports 탭)에 적재된 `_search_log` 및 `_search_gap` 행을 전용 검색수요 DB로 분리 이관하고
    시트에서는 완료 마킹하여 오류신고 목록과 섞이지 않게 유지합니다.
    """
    import _antigravity_report_watcher as arw

    if preloaded_rows is not None:
        all_rows = preloaded_rows
    else:
        try:
            all_rows = arw.fetch_all_reports(timeout=12)
        except Exception as e:
            return {"ok": False, "error": str(e), "synced": 0, "new_gaps": []}

    synced_keys = _load_synced_keys()
    keys_dirty = False
    synced_count = 0
    new_gaps: list[str] = []

    for r in all_rows:
        slug = str(r.get("quiz_slug") or "").strip()
        if slug not in ("_search_log", "_search_gap"):
            continue
        ts = str(r.get("timestamp") or "").strip()
        qn = str(r.get("question_num") or "").strip()
        row_key = f"{ts}|{slug}|{qn}|{str(r.get('text') or '')[:40]}"
        if row_key in synced_keys:
            if not r.get("fix_timestamp"):
                arw.post_fix_report(ts, slug, qn, "📊 [검색수요 전용 DB 분리 저장 완료]")
            continue

        parsed = _parse_search_sheet_row(r)
        if parsed:
            rec_res = record_search_event_locally(
                query=parsed["query"],
                lang=parsed["lang"],
                source=parsed["source"],
                priority=parsed["priority"],
                timestamp=parsed["timestamp"],
            )
            synced_count += 1
            if rec_res.get("queued_new_gap"):
                new_gaps.append(parsed["query"])

        synced_keys.add(row_key)
        keys_dirty = True
        if not r.get("fix_timestamp"):
            arw.post_fix_report(ts, slug, qn, "📊 [검색수요 전용 DB 분리 저장 완료]")

    if keys_dirty:
        _save_synced_keys(synced_keys)

    return {"ok": True, "synced": synced_count, "new_gaps": new_gaps}


# ---------------------------------------------------------------------------
# 미충족(0건) 수학 주제 수업자료 자동 제작·배포 파이프라인
# ---------------------------------------------------------------------------
def _can_consume_lesson_slot() -> bool:
    now = time.time()
    runs: list[float] = []
    if PRODUCTION_RATE_FILE.exists():
        try:
            data = json.loads(PRODUCTION_RATE_FILE.read_text(encoding="utf-8"))
            runs = [float(x) for x in (data.get("runs") or []) if now - float(x) < 3600.0]
        except Exception:
            runs = []
    if len(runs) >= MAX_AUTO_LESSONS_PER_HOUR:
        return False
    runs.append(now)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    PRODUCTION_RATE_FILE.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")
    return True


def _resolve_agy_cli() -> str:
    found = shutil.which("agy")
    if found:
        return found
    cand = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\min\AppData\Local")) / "agy" / "bin" / "agy.EXE"
    if cand.exists():
        return str(cand)
    return "agy"


def produce_lesson_material_for_topic(
    topic_query: str,
    force: bool = False,
    notify_telegram: bool = True,
) -> dict:
    """
    관련 자료가 없는 수학 검색어(topic_query)에 대해 `mathteacher` 표준 규격의
    초등 눈높이 6단계 디딤돌 + 인라인 SVG 도형 + 도식화 흐름도 + 한·영 완벽 번역 수업자료를
    자동 생성(`board/{slug}.html` + `board/index.json` + `offline/{slug}.html`)하고 GitHub Pages에 배포합니다.
    """
    q_clean = re.sub(r"\s+", " ", topic_query.strip())
    is_math, reason = is_verified_pure_math_topic(q_clean)
    if not is_math and not force:
        return {"ok": False, "status": "rejected_not_pure_math", "reason": reason}

    if not force and not _can_consume_lesson_slot():
        return {"ok": False, "status": "rate_limited_hourly_cap"}

    slug_hash = hashlib.sha1(f"lesson|{q_clean.lower()}".encode("utf-8")).hexdigest()[:8]
    new_slug = f"s{slug_hash}"

    prompt = (
        "[mathedu 미충족 검색어 맞춤형 수학 수업자료 자율 제작·배포 모드]\n"
        f"사용자가 홈페이지에서 **\"{q_clean}\"** 주제를 검색했으나 현재 직접 대응하는 수업자료가 없어 신규 제작합니다.\n"
        f"반드시 아래 규격(GEMINI.md Rule 1, 2, 3, 6, 7, 11, 13.2, 51, 58)을 100% 준수하여 `board/{new_slug}.html` 단독 인터랙티브 수업자료를 생성하고 배포하십시오:\n"
        f"1. 기존 최신 문항 파일(예: `board/ac8dc374.html` 또는 `board/c2610p30.html`)의 HTML/CSS/스크립트(`mathedu-i18n.js?v=20261115_en`, `mathedu-room.js?v=20261115_en`, `mathedu-report.js`) 구조를 그대로 참조하여 `board/{new_slug}.html`을 작성하십시오.\n"
        "2. [Rule 6 초등 눈높이 무장벽 디딤돌]: 초등학생도 직관적인 작은 숫자·도형 관찰에서 출발하여 1단계부터 6단계까지 스스로 풀며 최종 심화 개념·정리·활용 문제까지 정복하도록 6단계 디딤돌(`.q`)을 정교하게 구성하고 수학적 오류(정답·수식·보기 중복)가 단 1건도 없도록 검산하십시오.\n"
        "3. [Rule 7 시각적 도형 및 도식화 풀이 필수]: 본문 및 최종 해설(`.sol`)에 반드시 정교한 인라인 `<figure class=\"math-visual-diagram\"><svg ...>...</svg></figure>` 도형 다이어그램과 `<section class=\"math-schematic-flow\">` 한눈에 보는 도식화 풀이 흐름도를 포함하십시오.\n"
        "4. [Rule 3 & Rule 58]: `min7014.github.io`의 가장 밀접한 관련 수학자료실 링크를 안내에 연결하고, 한국어(`title`)와 깔끔한 영문 제목(`title_en`, 한글 0자)을 모두 갖추어 `board/index.json` 최상단에 등록하십시오 (외부 시험 상표권 단어 절대 사용 금지, `MIN EUN GI` 대문자 원칙 준수).\n"
        "5. `python -X utf8 build_offline_quizzes.py`를 실행하여 `offline/` 패키지를 동기화하고, `python -X utf8 auditor.py check`가 `PASS_ZERO_VIOLATIONS`임을 확인한 뒤, 안전한 웹/데이터 파일만 `git add` -> `git commit` -> `git push origin main`으로 배포하십시오.\n"
        f"6. 완료 후 생성된 수업 제목과 라이브 URL(`https://min7014.github.io/mathedu/board/{new_slug}.html`)을 한국어 5줄 이내로 출력하십시오 (`--reply`나 `--listen-once` 직접 호출 금지)."
    )

    try:
        agy_bin = _resolve_agy_cli()
        proc = subprocess.run(
            [agy_bin, "-p", prompt, "--dangerously-skip-permissions"],
            cwd=str(REPO_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=900,
        )
        summary = (proc.stdout or "").strip()
        created_path = REPO_DIR / "board" / f"{new_slug}.html"
        ok = proc.returncode == 0 and created_path.exists()

        if ok:
            live_url = f"https://min7014.github.io/mathedu/board/{new_slug}.html"
            db = load_demand_db()
            q_key = normalize_query_key(q_clean)
            for g in db.get("unmet_lesson_queue", []):
                if normalize_query_key(g.get("query", "")) == q_key:
                    g["status"] = "produced"
                    g["produced_slug"] = new_slug
                    g["lesson_url"] = live_url
                    g["produced_at"] = datetime.datetime.now().isoformat()
            db.setdefault("produced_lessons", []).append(
                {
                    "query": q_clean,
                    "slug": new_slug,
                    "lesson_url": live_url,
                    "produced_at": datetime.datetime.now().isoformat(),
                }
            )
            save_demand_db(db)

            if notify_telegram:
                try:
                    import mathedu_telegram_bridge as tg_bridge

                    cfg = tg_bridge.load_env_config()
                    tk, cid = cfg.get("TELEGRAM_BOT_TOKEN", ""), cfg.get("TELEGRAM_CHAT_ID", "")
                    if tk and cid:
                        tg_bridge.send_msg(
                            tk,
                            cid,
                            (
                                f"🎓 [사용자 미충족 검색어 맞춤형 수업자료 자동 제작·배포 완료!]\n"
                                f"• 요구 검색어: \"{q_clean}\"\n"
                                f"• 생성 슬러그: {new_slug} (6단계 초등 디딤돌 + SVG 시각 도형 + 한/영 지원)\n"
                                f"• 라이브 수업 링크: {live_url}\n\n"
                                f"{summary[-1200:]}"
                            ),
                        )
                except Exception:
                    pass
            return {"ok": True, "slug": new_slug, "lesson_url": live_url, "summary": summary[-1000:]}
        return {"ok": False, "status": "generation_incomplete", "summary": summary[-800:]}
    except Exception as e:
        return {"ok": False, "status": f"error: {e}"}


def run_search_demand_cycle(auto_produce: bool = True, notify_telegram: bool = True) -> dict:
    """
    1) Google Sheets에서 신규 검색 로그를 전용 DB로 분리 동기화하고,
    2) 대기 중인 미충족(0건) 순수 수학 검색어가 있으면 자동으로 수업자료 1건을 제작·배포합니다.
    """
    sync_res = sync_search_logs_from_sheets()
    db = load_demand_db()
    pending = [g for g in db.get("unmet_lesson_queue", []) if g.get("status") == "pending"]
    # 우선요청(priority=True) 및 요청 횟수(request_count) 순 정렬
    pending.sort(key=lambda g: (1 if g.get("priority") else 0, int(g.get("request_count", 1))), reverse=True)

    produced_res = None
    if auto_produce and pending:
        top_gap = pending[0]
        produced_res = produce_lesson_material_for_topic(
            top_gap["query"],
            force=False,
            notify_telegram=notify_telegram,
        )

    return {
        "ok": True,
        "synced_events": sync_res.get("synced", 0),
        "pending_unmet_count": len([g for g in load_demand_db().get("unmet_lesson_queue", []) if g.get("status") == "pending"]),
        "produced_result": produced_res,
    }


def format_search_demand_summary() -> str:
    sync_search_logs_from_sheets()
    db = load_demand_db()
    total_ev = int(db.get("total_search_events", 0))
    queries_map = db.get("queries") or {}
    top_q = sorted(queries_map.values(), key=lambda x: int(x.get("count", 0)), reverse=True)[:10]
    pending_gaps = [g for g in (db.get("unmet_lesson_queue") or []) if g.get("status") == "pending"]
    produced_list = db.get("produced_lessons") or []

    lines = [
        "🔍 [크레딧 0원 · mathedu 사용자 검색어 수요 분석 & 미충족 수업자료 자동 제작 현황]",
        f"• 누적 기록된 검색 이벤트: {total_ev:,}건 (고유 검색어 {len(queries_map):,}종 | 오류신고와 100% 분리 저장)",
        f"• 관련자료 0건 미충족 수학 주제: 제작 대기 {len(pending_gaps)}건 / ✅ 자동 제작·배포 완료 {len(produced_list)}건",
    ]
    if top_q:
        lines.append("\n📈 [인기 사용자 검색어 TOP 10]:")
        for idx, item in enumerate(top_q, 1):
            cov = item.get("coverage") or {}
            tot_h = cov.get("total_hits", 0)
            tag = "🚨 자료없음(제작대상)" if tot_h == 0 and item.get("is_pure_math") else f"자료 {tot_h}건"
            lines.append(f"  {idx}) \"{item.get('display_query')}\" — {item.get('count')}회 검색 ({tag})")
    else:
        lines.append("\n• 아직 집계된 사용자 검색어가 없으며, 지금부터 입력되는 모든 검색어가 실시간 기록됩니다.")

    if pending_gaps:
        lines.append("\n🛠️ [관련자료 부재 -> 자동 수업자료 제작 대기 큐]:")
        for g in pending_gaps[:5]:
            prio_b = "⭐우선요청 " if g.get("priority") else ""
            lines.append(f"  - {prio_b}\"{g.get('query')}\" ({g.get('request_count', 1)}회 요구)")

    if produced_list:
        lines.append("\n🎓 [검색 수요 기반 자동 제작 완료 수업자료]:")
        for p in produced_list[-5:]:
            lines.append(f"  - \"{p.get('query')}\" ➔ {p.get('lesson_url')}")

    lines.append("\n💡 특정 주제를 즉시 수업자료로 만들려면: `!자료제작 <수학 주제명>`")
    return "\n".join(lines)


def main() -> None:
    if "--summary" in sys.argv:
        print(format_search_demand_summary())
        return
    if "--sync" in sys.argv:
        print(json.dumps(sync_search_logs_from_sheets(), ensure_ascii=False, indent=2))
        return
    if "--cycle" in sys.argv:
        print(json.dumps(run_search_demand_cycle(auto_produce=True, notify_telegram=True), ensure_ascii=False, indent=2))
        return
    if "--produce" in sys.argv:
        idx = sys.argv.index("--produce")
        topic = " ".join(sys.argv[idx + 1 :]).strip()
        if not topic:
            db = load_demand_db()
            pending = [g for g in db.get("unmet_lesson_queue", []) if g.get("status") == "pending"]
            if not pending:
                print("ℹ️ 현재 대기 중인 미충족 수학 검색어가 없습니다.")
                return
            topic = pending[0]["query"]
        res = produce_lesson_material_for_topic(topic, force=True, notify_telegram=True)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(format_search_demand_summary())


if __name__ == "__main__":
    main()
