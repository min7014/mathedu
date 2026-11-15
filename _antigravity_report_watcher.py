#!/usr/bin/env python3
"""
mathedu 안티그래비티 전용 실시간 오류 신고 3트랙 시각 관제 · 텔레그램 연동 모듈
(Antigravity 3-Track Visual Error Report Triage & Auto-Fix Watcher)

[회장님(min7014) 핵심 지침 (2026-11-15)]:
1. Track 1 — 수학적 오류 (math_error):
   수식·계산·부호·정답·기하 조건·논리 등 수학적으로 틀린 내용이 있으면 묻지 않고 즉시 검증·수정·배포!
2. Track 2 — 기승인 유사 오류 유형 (approved_similar):
   회장님이 이미 수정을 승인하셨거나 `assets/approved_error_patterns.json`에 등록된 비슷한 오류 종류는 묻지 않고 즉시 전수 수리·배포!
3. Track 3 — 신규 종류의 화면·기능·디자인·제안 신고 (ask_with_screenshot):
   임의로 먼저 고치지 않고, 해당 신고 화면(URL·문항 단계·선택 영역 하이라이트)을 스크린샷 그림(`sendPhoto`)으로
   텔레그램(`@anti7014_bot`, Chat ID: 43453234)에 먼저 보여드리고 고칠지 여부를 질문!
   -> 회장님이 [✅ 고쳐] 승인 시 즉시 전수 수리 + 해당 오류 종류를 `approved_error_patterns.json`에 자동 등록!
   -> 회장님이 [❌ 고치지 마] 선택 시 코드 수정 없이 즉시 보류·종결!
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
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import silent_subprocess  # Rule 48: 100% 무창(Windowless) 백그라운드 실행 강제
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
SCREENSHOT_DIR = REPO_DIR / ".temp" / "error_report_screenshots"
PROCESSED_FILE = AGENTS_DIR / "processed_error_reports.json"
PENDING_FILE = AGENTS_DIR / "pending_error_reports.json"
AWAITING_APPROVAL_FILE = AGENTS_DIR / "awaiting_approval_reports.json"
APPROVED_PATTERNS_FILE = REPO_DIR / "assets" / "approved_error_patterns.json"
AUTOFIX_RATE_FILE = AGENTS_DIR / "autofix_rate_state.json"
LEGACY_PROCESSED_FILE = REPO_DIR / "_processed_reports.json"
API_URL_FILE = REPO_DIR / "progress-api-url.txt"
MAX_AUTOFIX_RUNS_PER_HOUR = 5
DEFAULT_SHEETS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec"
)


def get_sheets_url() -> str:
    if API_URL_FILE.exists():
        try:
            url = API_URL_FILE.read_text(encoding="utf-8").strip()
            if url.startswith("http"):
                return url
        except Exception:
            pass
    return DEFAULT_SHEETS_URL


def _make_report_key(r: dict) -> str:
    ts = str(r.get("timestamp") or "").strip()
    qs = str(r.get("quiz_slug") or "").strip()
    qn = str(r.get("question_num") or "").strip()
    return f"{ts}|{qs}|{qn}"


def _make_short_id(r: dict, sheet_seq: int | None = None) -> str:
    if sheet_seq and sheet_seq > 0:
        return f"R{sheet_seq}"
    h = hashlib.sha1(_make_report_key(r).encode("utf-8")).hexdigest()[:6].upper()
    return f"R{h}"


def load_processed() -> dict:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    for target in (PROCESSED_FILE, LEGACY_PROCESSED_FILE):
        if target.exists():
            try:
                data = json.loads(target.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    data.setdefault("processed", [])
                    data.setdefault("alerted_keys", [])
                    return data
            except Exception:
                pass
    return {"processed": [], "alerted_keys": []}


def save_processed(data: dict) -> None:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_approved_patterns() -> dict:
    if APPROVED_PATTERNS_FILE.exists():
        try:
            data = json.loads(APPROVED_PATTERNS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("patterns"), list):
                return data
        except Exception:
            pass
    return {"version": "1.0.0", "updated_at": datetime.datetime.now().isoformat(), "patterns": []}


def save_approved_patterns(data: dict) -> None:
    APPROVED_PATTERNS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.datetime.now().isoformat()
    APPROVED_PATTERNS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_awaiting_approvals() -> dict:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    if AWAITING_APPROVAL_FILE.exists():
        try:
            data = json.loads(AWAITING_APPROVAL_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("items"), list):
                return data
        except Exception:
            pass
    return {"items": []}


def save_awaiting_approvals(data: dict) -> None:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    AWAITING_APPROVAL_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_pending_approval_items() -> list[dict]:
    data = load_awaiting_approvals()
    return [it for it in data.get("items", []) if it.get("status") == "awaiting"]


def parse_report_fields(report: dict) -> dict:
    raw_text = str(report.get("text") or "").strip()

    def _extract(tag: str) -> str:
        m = re.search(rf"\[{re.escape(tag)}\]\s*(.*?)(?=\n\[|\Z)", raw_text, flags=re.S)
        return m.group(1).strip() if m else ""

    cat_raw = _extract("오류유형")
    detail = _extract("상세내용") or raw_text
    target_loc = _extract("선택위치")
    excerpt = _extract("발췌문구")
    page_url = _extract("페이지URL")
    viewport = _extract("화면해상도")

    vw, vh = 1440, 920
    m_vp = re.match(r"^\s*(\d{3,4})\s*[xX×]\s*(\d{3,4})\s*$", viewport)
    if m_vp:
        vw = max(390, min(1920, int(m_vp.group(1))))
        vh = max(680, min(1200, int(m_vp.group(2))))

    is_en_ui = bool(
        re.search(r"lang=en\b", page_url, flags=re.I)
        or any(tok in cat_raw for tok in ("Math /", "Typo /", "Answer /", "Image /", "Layout /", "Other "))
    )

    step_num = 0
    raw_qn = str(report.get("question_num") or "").strip()
    if raw_qn.isdigit():
        step_num = int(raw_qn)
    else:
        m_step = re.search(r"제\s*(\d+)\s*단계", target_loc)
        if m_step:
            step_num = int(m_step.group(1))

    return {
        "raw_text": raw_text,
        "category_raw": cat_raw,
        "detail": detail,
        "target_loc": target_loc,
        "excerpt": excerpt,
        "page_url": page_url,
        "viewport": viewport,
        "vw": vw,
        "vh": vh,
        "is_en_ui": is_en_ui,
        "step_num": step_num,
        "quiz_slug": str(report.get("quiz_slug") or "mathedu").strip() or "mathedu",
        "question_num": raw_qn,
        "reporter": str(report.get("reporter") or "익명").strip(),
        "timestamp": str(report.get("timestamp") or "").strip(),
    }


def post_fix_report(
    timestamp: str,
    quiz_slug: str,
    question_num: str | int,
    result: str,
    email: str | None = None,
    quiz_url: str | None = None,
    title: str | None = None,
) -> bool:
    sheets_url = get_sheets_url()
    try:
        payload: dict = {
            "action": "fix_report",
            "timestamp": timestamp,
            "quiz_slug": quiz_slug,
            "question_num": str(question_num if question_num is not None else ""),
            "result": result,
        }
        if email:
            payload["email"] = email
        if quiz_url:
            payload["quiz_url"] = quiz_url
        if title:
            payload["title"] = title

        fix_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            sheets_url,
            data=fix_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp.read()

        proc = load_processed()
        proc.setdefault("processed", []).append(
            {
                "timestamp": timestamp,
                "quiz_slug": quiz_slug,
                "question_num": str(question_num if question_num is not None else ""),
                "status": "fixed",
                "fix": result,
                "fixed_at": datetime.datetime.now().isoformat(),
            }
        )
        r_key = f"{timestamp}|{quiz_slug}|{question_num if question_num is not None else ''}"
        if r_key not in proc.setdefault("alerted_keys", []):
            proc["alerted_keys"].append(r_key)
        save_processed(proc)

        # 대기 큐에 있었다면 함께 완료 상태로 동기화
        aw = load_awaiting_approvals()
        changed_aw = False
        for it in aw.get("items", []):
            if it.get("report_key") == r_key and it.get("status") in ("awaiting", "approved"):
                it["status"] = "fixed"
                it["fixed_at"] = datetime.datetime.now().isoformat()
                changed_aw = True
        if changed_aw:
            save_awaiting_approvals(aw)

        return True
    except Exception:
        return False


def fetch_all_reports(timeout: int = 12) -> list[dict]:
    sheets_url = get_sheets_url()
    req = urllib.request.Request(f"{sheets_url}?action=reports")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    reports = data.get("reports", [])
    return reports if isinstance(reports, list) else []


def check_reports() -> list[dict]:
    try:
        reports = fetch_all_reports(timeout=12)
    except Exception:
        return []

    processed = load_processed()
    processed_items = processed.get("processed", [])

    unfixed: list[dict] = []
    for r in reports:
        if r.get("fix_timestamp"):
            continue
        ts = str(r.get("timestamp") or "")
        qs = str(r.get("quiz_slug") or "")
        qn = str(r.get("question_num") or "")
        already = any(
            str(p.get("timestamp") or "") == ts
            and str(p.get("quiz_slug") or "") == qs
            and str(p.get("question_num") or "") == qn
            and p.get("status") in ("fixed", "resolved", "declined", "held")
            for p in processed_items
        )
        if not already:
            unfixed.append(r)
    return unfixed


def classify_error_report_safety(report: dict) -> tuple[str, str]:
    """
    [0-크레딧 1차 기계적 트리아지 게이트 (Rule 2 · Rule 4 · 쿼터 보호)]
    - 'noise': 의미 없는 자음/모음 연타, '사유 없음', 빈 텍스트 등 -> LLM 호출 없이 0크레딧 자동 종결
    - 'hold' : 프롬프트 인젝션, 셸 명령 유도, 비수학(트레이딩/코인 등) 요청 -> 코드 수정 없이 보류 및 텔레그램 보고(Rule 4)
    - 'valid': 유효한 수학교육 문항·수식·레이아웃·기능 신고
    """
    parsed = parse_report_fields(report)
    raw_text = parsed["raw_text"]
    detail = parsed["detail"]
    if not raw_text or not detail:
        return ("noise", "신고 본문이 비어 있어 자동 종결 처리되었습니다.")

    low_all = raw_text.lower()
    injection_or_nonmath = (
        "ignore previous", "system prompt", "rm -rf", "del /f", "powershell",
        "cmd.exe", "client_secret", ".env", "bot_token", "트레이딩", "암호화폐",
        "비트코인", "주식", "선물옵션", "s-nova",
    )
    if any(tok in low_all for tok in injection_or_nonmath):
        return ("hold", "보안/비수학 도메인 필터(Rule 2·4)에 의해 자동 수정이 보류되었습니다(회장님 확인 필요).")

    cleaned = re.sub(r"[\s\.,!\?~_\-\d]+", "", detail)
    if detail in ("사유 없음", "사유없음", "없음", "test", "TEST", "테스트"):
        return ("noise", "구체적인 오류 설명 없는 단순 테스트/빈 사유 입력으로 확인되어 자동 종결 처리되었습니다.")
    if len(cleaned) < 2:
        return ("noise", "오류 설명이 너무 짧아(2자 미만) 단순 오입력으로 자동 종결 처리되었습니다.")
    if re.fullmatch(r"[ㄱ-ㅎㅏ-ㅣ]+", cleaned):
        return ("noise", "구체적 문장 없는 자모 연타 입력으로 확인되어 자동 종결 처리되었습니다.")
    if re.fullmatch(r"[asdfghjklqwertyuiopzxcvbnm]{4,20}", cleaned.lower()) and not re.search(
        r"(math|error|font|text|line|step|quiz|button|link|page|image|svg|pdf|video|wrong|typo)",
        cleaned.lower(),
    ):
        return ("noise", "무작위 영문 자판 테스트 입력으로 확인되어 자동 종결 처리되었습니다.")

    return ("valid", "")


# ---------------------------------------------------------------------------
# 3-Track 정밀 분류 엔진 (수학적 오류 vs 기승인 유사 오류 vs 스크린샷 승인 대기)
# ---------------------------------------------------------------------------
PREDEFINED_CATEGORY_CATALOG = [
    (
        "floating_ui_overlap",
        "플로팅 버튼·배지·모달 화면 요소 가림/겹침",
        ["가립", "가려", "겹쳐", "겹침", "위로 올라", "짤려", "잘려", "overlap", "clipped", "covers"],
    ),
    (
        "svg_diagram_geometry_visual",
        "SVG 기하 도형·보조선·점 라벨 표시 이상",
        ["도형", "그림이 이상", "그래프가 이상", "보조선", "라벨이 겹", "점 위치", "다이어그램", "svg"],
    ),
    (
        "broken_link_or_resource",
        "PDF·GeoGebra·유튜브 영상 링크 연결 오류",
        ["링크가 안", "페이지가 안 열", "404", "영상이 안 나", "pdf가 안", "지오지브라 안", "broken link"],
    ),
    (
        "creative_input_grading_equiv",
        "주관식·창의 수식 입력 동치 채점/인식 개선",
        ["맞았는데 틀렸", "동치", "입력했는데 오답", "분수 입력", "루트 입력", "인식이 안"],
    ),
    (
        "mobile_responsive_layout",
        "모바일·작은 화면 반응형 레이아웃/스크롤 불편",
        ["모바일", "스크롤이 안", "화면 밖으로", "가로 스크롤", "글자가 너무 작", "버튼이 안 눌"],
    ),
    (
        "audio_narration_subtitle",
        "영상 음성 발음·자막·싱크 오류",
        ["발음이 이상", "음성이 이상", "자막이 틀", "소리가 안", "싱크가 안"],
    ),
]

UI_OR_FEATURE_REQUEST_HINTS = (
    "영어 버전", "영문 버전", "다크모드", "라이트모드", "테마", "색상", "색깔", "폰트 크기",
    "글자 크기", "디자인", "배치", "레이아웃", "메뉴", "버튼 위치", "기능을 넣어", "기능 추가",
    "만들어 주", "만들어주", "있으면 좋겠", "추가해 주", "추가해주", "바꿔 주", "바꿔주",
)

EXPLICIT_MATH_ERROR_KEYWORDS = (
    "정답이 틀", "정답 오류", "답이 틀", "답 오류", "답이 잘못", "정답은 ", "답은 ",
    "계산이 틀", "계산 오류", "계산 실수", "계산이 잘못",
    "부호가 틀", "부호가 반", "부호 오류", "부등호 방향", "부등호가 반",
    "수식이 틀", "수식 오류", "공식이 틀", "공식 오류", "식이 틀", "식이 잘못",
    "조건이 빠", "조건 누락", "진수 조건", "분모가 0", "정의역 오류",
    "논리 오류", "논리가 틀", "모순", "반례", "증명이 틀", "증명 오류", "해설이 틀", "해설 오류",
    "숫자가 틀", "숫자 오타", "계수가 틀", "지수가 틀", "값이 틀", "값이 잘못",
    "채점이 잘못", "채점 오류", "복수정답", "모두 정답",
    "wrong answer", "incorrect answer", "calculation error", "math error",
    "wrong sign", "formula is wrong", "incorrect formula", "proof error",
)


def is_explicit_mathematical_error(parsed: dict) -> bool:
    """
    신고 본문([상세내용])이 실제로 '수학적 내용 오류(수식·계산·부호·정답·논리·조건 오류)'를
    지적하는지 정밀 판별합니다. (기본 선택된 드롭다운 라벨만 보고 오판하지 않음)
    """
    detail = parsed["detail"]
    low = detail.lower()
    cat = parsed["category_raw"]

    # 순수 UI/디자인/신규기능 제안 문구가 주된 내용이고 수학적 수치/식 오류 언급이 없으면 제외
    has_ui_feature_req = any(tok in low for tok in UI_OR_FEATURE_REQUEST_HINTS)
    has_math_err_kw = any(tok in low for tok in EXPLICIT_MATH_ERROR_KEYWORDS)

    if has_math_err_kw:
        return True

    # 사용자가 직접 '🎯 정답 / 채점 이상' 탭을 명시적으로 선택했고 기능 추가 요청이 아닌 경우
    if ("정답 / 채점" in cat or "Answer / Grading" in cat) and not has_ui_feature_req:
        return True

    # "A가 아니라 B입니다 / A -> B로 고쳐야" 형태의 수식·수치 정정 제보 감지
    if not has_ui_feature_req and re.search(
        r"([0-9+\-*/=^√π]|\\[a-zA-Z]+).*?(아니라|아닌가요|잘못|틀렸|오타|고쳐야)",
        detail,
    ):
        return True

    return False


def match_approved_similar_pattern(parsed: dict) -> dict | None:
    detail_low = (parsed["detail"] + " " + parsed["target_loc"]).lower()
    reg = load_approved_patterns()
    for pat in reg.get("patterns", []):
        kws = pat.get("keywords_any") or []
        for kw in kws:
            if kw and kw.lower() in detail_low:
                return pat
    return None


def infer_report_pattern_signature(parsed: dict) -> dict:
    """
    Track 3 신규 신고에 대해 향후 '비슷한 오류종류 자동수리' 등록에 사용할 카테고리 시그니처를 추론합니다.
    """
    detail = parsed["detail"]
    low = (detail + " " + parsed["target_loc"]).lower()
    for cid, label, kws in PREDEFINED_CATEGORY_CATALOG:
        if any(k.lower() in low for k in kws):
            return {
                "category_id": cid,
                "label": label,
                "keywords_any": kws,
                "sample_report_text": detail[:160],
            }

    # 사전 카탈로그 외 신규 유형: 핵심 명사/어구 토큰 추출
    tokens = [
        t for t in re.findall(r"[가-힣A-Za-z]{2,12}", detail)
        if t not in ("오류", "이상", "부분", "화면", "문제", "페이지", "바란다", "해주세요", "같아요", "있습니다", "있어요")
    ]
    key_phrases = []
    if len(tokens) >= 2:
        key_phrases.append(f"{tokens[0]} {tokens[1]}")
    for t in tokens[:3]:
        if len(t) >= 3 and t not in key_phrases:
            key_phrases.append(t)
    if not key_phrases:
        key_phrases = [detail[:20].strip()]

    slug_hash = hashlib.sha1("|".join(key_phrases).encode("utf-8")).hexdigest()[:6]
    short_label = detail[:28] + ("..." if len(detail) > 28 else "")
    return {
        "category_id": f"custom_pattern_{slug_hash}",
        "label": f"유사 화면/기능 이슈 ({short_label})",
        "keywords_any": key_phrases,
        "sample_report_text": detail[:160],
    }


def register_approved_pattern(sig: dict, approved_by: str = "min7014") -> dict:
    reg = load_approved_patterns()
    patterns = reg.setdefault("patterns", [])
    cid = sig.get("category_id") or "custom_pattern"
    for existing in patterns:
        if existing.get("category_id") == cid:
            existing_kws = set(existing.get("keywords_any") or [])
            for k in sig.get("keywords_any") or []:
                if k not in existing_kws:
                    existing.setdefault("keywords_any", []).append(k)
            save_approved_patterns(reg)
            return existing

    new_entry = {
        "category_id": cid,
        "label": sig.get("label") or cid,
        "approved_at": datetime.datetime.now().isoformat(),
        "approved_by": approved_by,
        "keywords_any": sig.get("keywords_any") or [],
        "sample_report_text": sig.get("sample_report_text") or "",
    }
    patterns.append(new_entry)
    save_approved_patterns(reg)
    return new_entry


def triage_error_report(report: dict) -> dict:
    """
    신고 1건을 5단계(noise / hold / math_error / approved_similar / ask_with_screenshot)로 정밀 분류합니다.
    """
    safety, reason = classify_error_report_safety(report)
    parsed = parse_report_fields(report)
    if safety in ("noise", "hold"):
        return {"track": safety, "reason": reason, "parsed": parsed}

    if is_explicit_mathematical_error(parsed):
        return {
            "track": "math_error",
            "reason": "수학적 내용(수식·계산·부호·정답·논리) 오류 제보 -> 묻지 않고 즉시 수학 검증 및 수리",
            "pattern_id": "math_content_error",
            "pattern_label": "수학적 내용/수식/정답 오류",
            "parsed": parsed,
        }

    matched_pat = match_approved_similar_pattern(parsed)
    if matched_pat is not None:
        return {
            "track": "approved_similar",
            "reason": f"기승인 유사 오류 유형('{matched_pat.get('label')}') 일치 -> 묻지 않고 즉시 전수 수리",
            "pattern_id": matched_pat.get("category_id"),
            "pattern_label": matched_pat.get("label"),
            "parsed": parsed,
        }

    sig = infer_report_pattern_signature(parsed)
    return {
        "track": "ask_with_screenshot",
        "reason": "신규 유형의 화면·기능·디자인 신고 -> 텔레그램에 화면 스크린샷 전송 후 수정 여부 질문",
        "pattern_id": sig["category_id"],
        "pattern_label": sig["label"],
        "inferred_signature": sig,
        "parsed": parsed,
    }


# ---------------------------------------------------------------------------
# 신고 화면 정밀 재현 & 하이라이트 스크린샷 캡처 엔진 (Playwright Headless)
# ---------------------------------------------------------------------------
def _resolve_target_url_for_screenshot(parsed: dict) -> str:
    page_url = parsed["page_url"]
    slug = parsed["quiz_slug"]

    # 1. https://min7014.github.io/mathedu/... -> 로컬 파일 매핑 (고속·최신 상태 재현)
    if page_url:
        m = re.match(r"^https?://min7014\.github\.io/mathedu/(.*)$", page_url.strip(), flags=re.I)
        if m:
            rel_and_query = m.group(1)
            parsed_u = urllib.parse.urlsplit(rel_and_query)
            rel_path = parsed_u.path.lstrip("/") or "index.html"
            if rel_path.endswith("/"):
                rel_path += "index.html"
            local_cand = REPO_DIR / rel_path
            if local_cand.exists():
                base_uri = local_cand.resolve().as_uri()
                if parsed_u.query:
                    base_uri += "?" + parsed_u.query
                if parsed_u.fragment:
                    base_uri += "#" + parsed_u.fragment
                return base_uri
        if page_url.startswith(("http://", "https://", "file:///")):
            return page_url

    # 2. quiz_slug 기반 로컬 파일 탐색
    if slug in ("", "mathedu", "index"):
        target = REPO_DIR / "index.html"
    elif (REPO_DIR / f"{slug}.html").exists():
        target = REPO_DIR / f"{slug}.html"
    elif (REPO_DIR / "board" / f"{slug}.html").exists():
        target = REPO_DIR / "board" / f"{slug}.html"
    elif (REPO_DIR / "board" / "private" / f"{slug}.html").exists():
        target = REPO_DIR / "board" / "private" / f"{slug}.html"
    else:
        target = REPO_DIR / "index.html"

    uri = target.resolve().as_uri()
    if parsed["is_en_ui"] and "lang=" not in uri:
        uri += "?lang=en"
    return uri


def capture_error_report_screenshot(report: dict, seq_id: str = "R_PREVIEW") -> Path | None:
    """
    신고된 페이지·해상도·언어·문항 단계(question_num)·선택 영역([선택위치]/[발췌문구])을
    무창 Headless Chromium으로 정확히 재현하고 붉은 하이라이트 배지를 씌워 PNG로 저장합니다.
    """
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", seq_id)
    out_path = SCREENSHOT_DIR / f"report_{safe_name}_{int(time.time())}.png"
    parsed = parse_report_fields(report)
    target_url = _resolve_target_url_for_screenshot(parsed)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": parsed["vw"], "height": parsed["vh"]},
                device_scale_factor=1.5,
            )
            page = context.new_page()
            if parsed["is_en_ui"]:
                page.add_init_script("try { localStorage.setItem('mathedu_lang', 'en'); } catch(e) {}")

            page.goto(target_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(900)

            # 단계 잠금 해제 · 보기/해설/풀이 영역 가시화 · 신고 지점 하이라이트 주입
            page.evaluate(
                """(meta) => {
                    const stepNum = meta.stepNum || 0;
                    const targetLoc = String(meta.targetLoc || '');
                    const excerpt = String(meta.excerpt || '').trim();
                    const detail = String(meta.detail || '').trim();
                    const seqId = String(meta.seqId || '');

                    // 1) 다단계 퀴즈(.q)인 경우 해당 단계까지 잠금 해제하여 실제 문항 표시
                    const allQ = Array.from(document.querySelectorAll('.q'));
                    let stepEl = null;
                    if (stepNum > 0 && allQ.length > 0) {
                        const limit = Math.min(stepNum, allQ.length);
                        for (let i = 0; i < limit; i++) {
                            allQ[i].style.display = 'block';
                            allQ[i].style.opacity = '1';
                            allQ[i].classList.remove('locked', 'hidden', 'disabled');
                        }
                        stepEl = allQ[limit - 1];
                    }

                    // 2) 보기(.opt) / 해설(.exp) / 최종풀이(.sol) 신고 시 숨겨진 영역 표시
                    if (targetLoc.includes('보기')) {
                        const scope = stepEl || document;
                        scope.querySelectorAll('.opts, .opt').forEach(el => {
                            if (getComputedStyle(el).display === 'none') el.style.display = '';
                            el.classList.remove('hidden');
                        });
                    }
                    if (targetLoc.includes('해설') && stepEl) {
                        const expEl = stepEl.querySelector('.exp');
                        if (expEl) {
                            if (!expEl.innerHTML.trim() && stepEl.dataset && stepEl.dataset.exp) {
                                expEl.innerHTML = stepEl.dataset.exp;
                            }
                            expEl.style.display = 'block';
                        }
                    }
                    if (targetLoc.includes('상세 풀이') || targetLoc.includes('.sol')) {
                        document.querySelectorAll('.sol').forEach(el => { el.style.display = 'block'; });
                    }

                    // 3) 신고 타겟 요소 탐색 (선택위치 -> 단계 내부 클래스 -> 발췌문구 일치 순)
                    let found = null;
                    if (stepEl) {
                        if (targetLoc.includes('보기')) found = stepEl.querySelector('.opts') || stepEl.querySelector('.opt');
                        else if (targetLoc.includes('지문')) found = stepEl.querySelector('.stem');
                        else if (targetLoc.includes('해설')) found = stepEl.querySelector('.exp');
                        else found = stepEl;
                    }
                    if (!found && targetLoc && !targetLoc.includes('화면 전체') && !targetLoc.includes('단계')) {
                        try {
                            found = document.querySelector(targetLoc);
                        } catch (e) {
                            const tagCls = targetLoc.split('.')[0];
                            if (tagCls) {
                                try { found = document.querySelector(tagCls); } catch (_) {}
                            }
                        }
                    }
                    if (!found && excerpt && excerpt.length >= 4 && !excerpt.startsWith('file://') && !excerpt.startsWith('http')) {
                        const probe = excerpt.slice(0, 32).replace(/\\s+/g, ' ').trim();
                        if (probe.length >= 3) {
                            const cands = Array.from(document.querySelectorAll('.opt, .stem, .exp, .sol, .q, a, button, p, div, section'));
                            for (const c of cands) {
                                const txt = (c.innerText || '').replace(/\\s+/g, ' ');
                                if (txt.includes(probe) && c.offsetWidth > 20 && c.offsetHeight > 12) {
                                    found = c;
                                    if (c.matches('.opt, .stem, .exp, a, button, p')) break;
                                }
                            }
                        }
                    }

                    // 4) 스크롤 정렬 및 시각적 하이라이트 프레임 + 상단 요약 배너 렌더링
                    if (found && found !== document.body && found !== document.documentElement) {
                        try { found.scrollIntoView({ behavior: 'instant', block: 'center' }); } catch (e) {}
                    }

                    window.__matheduHighlightTarget = found;
                    window.__matheduReportMeta = { seqId, targetLoc: targetLoc || '화면 전체', detail };
                }""",
                {
                    "stepNum": parsed["step_num"],
                    "targetLoc": parsed["target_loc"],
                    "excerpt": parsed["excerpt"],
                    "detail": parsed["detail"],
                    "seqId": seq_id,
                },
            )

            # MathJax 수식 재렌더링 대기 후 정확한 좌표에 하이라이트 박스 부착
            page.evaluate(
                """async () => {
                    try {
                        if (window.MathJax && window.MathJax.typesetPromise) {
                            await window.MathJax.typesetPromise();
                        }
                    } catch (e) {}
                    const found = window.__matheduHighlightTarget;
                    const meta = window.__matheduReportMeta || {};
                    if (found && found.getBoundingClientRect) {
                        try { found.scrollIntoView({ behavior: 'instant', block: 'center' }); } catch (e) {}
                        const r = found.getBoundingClientRect();
                        if (r.width > 4 && r.height > 4) {
                            const hl = document.createElement('div');
                            hl.style.cssText = [
                                'position:fixed',
                                `top:${Math.max(4, r.top - 6)}px`,
                                `left:${Math.max(4, r.left - 6)}px`,
                                `width:${Math.min(window.innerWidth - 8, r.width + 12)}px`,
                                `height:${Math.min(window.innerHeight - 8, r.height + 12)}px`,
                                'border:3.5px solid #ff3b30',
                                'border-radius:10px',
                                'background:rgba(255,59,48,0.08)',
                                'box-shadow:0 0 0 4px rgba(255,59,48,0.22), 0 8px 28px rgba(0,0,0,0.45)',
                                'pointer-events:none',
                                'z-index:2147483646'
                            ].join(';');

                            const badge = document.createElement('div');
                            badge.textContent = `🚨 신고 지점 (${meta.seqId || ''}) · ${meta.targetLoc || ''}`;
                            badge.style.cssText = [
                                'position:absolute',
                                r.top > 38 ? 'top:-32px' : 'bottom:-32px',
                                'left:0',
                                'background:#ff3b30',
                                'color:#ffffff',
                                'font-weight:800',
                                'font-size:13px',
                                'padding:4px 12px',
                                'border-radius:7px',
                                'white-space:nowrap',
                                'box-shadow:0 4px 12px rgba(0,0,0,0.4)',
                                'font-family:Pretendard,"Segoe UI Emoji","Apple Color Emoji",-apple-system,sans-serif'
                            ].join(';');
                            hl.appendChild(badge);
                            document.body.appendChild(hl);
                        }
                    }
                }"""
            )
            page.wait_for_timeout(350)
            page.screenshot(path=str(out_path), full_page=False)
            browser.close()

        if out_path.exists() and out_path.stat().st_size > 1000:
            return out_path
    except Exception as e:
        print(f"[Screenshot Capture Notice] {e}", flush=True)
    return None


# ---------------------------------------------------------------------------
# 텔레그램 알림 & 스크린샷 승인 질문 전송
# ---------------------------------------------------------------------------
def _send_telegram_track3_approval_request(
    report: dict,
    triage_info: dict,
    seq_id: str,
    screenshot_path: Path | None,
) -> int | None:
    """
    Track 3(신규 유형 오류)에 대해 스크린샷 그림 + 인라인 승인 버튼을 텔레그램으로 전송하고 message_id를 반환합니다.
    """
    try:
        import mathedu_telegram_bridge as tg_bridge

        cfg = tg_bridge.load_env_config()
        token = cfg.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = cfg.get("TELEGRAM_CHAT_ID", "") or tg_bridge.load_offset_state().get("chat_id", "")
        if not token or not chat_id:
            return None

        parsed = triage_info["parsed"]
        detail_short = parsed["detail"][:260] + ("..." if len(parsed["detail"]) > 260 else "")
        excerpt_short = parsed["excerpt"][:140] + ("..." if len(parsed["excerpt"]) > 140 else "")

        caption_lines = [
            f"📸 [신규 오류신고 #{seq_id.lstrip('R')} 화면 확인 및 수정 승인 요청]",
            f"• 위치: {parsed['quiz_slug']} (단계: {parsed['question_num'] or '전체'} | {parsed['target_loc'] or '화면 전체'})",
            f"• 추정유형: {triage_info.get('pattern_label', '신규 화면/기능 이슈')}",
            f"• 신고자: {parsed['reporter']}",
            f"• 신고내용: {detail_short}",
        ]
        if excerpt_short and not excerpt_short.startswith(("http", "file://")):
            caption_lines.append(f"• 선택문구: {excerpt_short}")
        caption_lines.append("")
        caption_lines.append("❓ 이 오류신고를 수정할까요?")
        caption_lines.append("(승인 시 비슷한 오류 종류도 앞으로 묻지 않고 자동 수정합니다. 버튼 클릭 또는 '고쳐' / '고치지마' 답장)")
        caption = "\n".join(caption_lines)[:1020]

        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "✅ 고쳐 (비슷한 오류도 앞으로 자동수리)",
                        "callback_data": f"err_approve_auto:{seq_id}",
                    }
                ],
                [
                    {
                        "text": "🔧 이번 건만 수정",
                        "callback_data": f"err_approve_once:{seq_id}",
                    },
                    {
                        "text": "❌ 고치지 마 (기각)",
                        "callback_data": f"err_reject:{seq_id}",
                    },
                ],
            ]
        }

        if screenshot_path and screenshot_path.exists():
            resp = tg_bridge.send_photo(
                token,
                chat_id,
                screenshot_path,
                caption=caption,
                reply_markup=reply_markup,
            )
            if isinstance(resp, dict) and resp.get("ok"):
                return (resp.get("result") or {}).get("message_id")

        # 스크린샷 실패 시 텍스트 + 인라인 버튼 폴백
        resp = tg_bridge.tg_api(
            token,
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": caption,
                "reply_markup": reply_markup,
                "link_preview_options": {"is_disabled": True},
            },
        )
        if isinstance(resp, dict) and resp.get("ok"):
            return (resp.get("result") or {}).get("message_id")
    except Exception as e:
        print(f"[Track3 Telegram Approval Notice] {e}", flush=True)
    return None


def _send_telegram_immediate_autofix_notice(
    report: dict,
    triage_info: dict,
    seq_id: str,
    screenshot_path: Path | None,
) -> None:
    """
    Track 1(수학적 오류) 및 Track 2(기승인 유사 유형)에 대해 묻지 않고 즉시 수리에 착수함을 알립니다.
    """
    try:
        import mathedu_telegram_bridge as tg_bridge

        cfg = tg_bridge.load_env_config()
        token = cfg.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = cfg.get("TELEGRAM_CHAT_ID", "") or tg_bridge.load_offset_state().get("chat_id", "")
        if not token or not chat_id:
            return

        parsed = triage_info["parsed"]
        track = triage_info["track"]
        header = (
            f"⚡ [수학적 오류 신고 #{seq_id.lstrip('R')} 감지 ➔ 묻지 않고 즉시 검증·수정 착수]"
            if track == "math_error"
            else f"⚡ [기승인 유사 오류 #{seq_id.lstrip('R')} 감지 ➔ 묻지 않고 즉시 전수 수리 착수]"
        )
        caption = (
            f"{header}\n"
            f"• 위치: {parsed['quiz_slug']} (단계: {parsed['question_num'] or '전체'})\n"
            f"• 분류: {triage_info.get('pattern_label', '')}\n"
            f"• 신고내용: {parsed['detail'][:240]}\n\n"
            "🛠️ 회장님 지침에 따라 질문 대기 없이 바로 검증·수정 후 완료 결과를 보고드립니다."
        )[:1020]

        if screenshot_path and screenshot_path.exists():
            tg_bridge.send_photo(token, chat_id, screenshot_path, caption=caption)
        else:
            tg_bridge.send_msg(token, chat_id, caption)
    except Exception as e:
        print(f"[Immediate Autofix Telegram Notice] {e}", flush=True)


# ---------------------------------------------------------------------------
# 회장님 승인 / 기각 처리 API (텔레그램 인라인 버튼 & 텍스트 답장 공용)
# ---------------------------------------------------------------------------
def approve_awaiting_report(target_id: str = "", register_similar: bool = True) -> dict:
    """
    대기 중인 Track 3 오류신고를 승인 처리하고, register_similar=True이면 유사 패턴 레지스트리에 자동 등록합니다.
    target_id가 비어 있으면 가장 최근 awaiting 항목을 승인하며, 'ALL'이면 대기 중인 전 항목을 승인합니다.
    """
    aw = load_awaiting_approvals()
    items = aw.get("items", [])
    awaiting = [it for it in items if it.get("status") == "awaiting"]
    if not awaiting:
        return {"ok": False, "reason": "no_awaiting_reports", "approved_reports": []}

    norm_id = target_id.strip().upper()
    if norm_id and not norm_id.startswith("R") and norm_id != "ALL":
        norm_id = f"R{norm_id}"

    selected: list[dict] = []
    if norm_id == "ALL":
        selected = awaiting
    elif norm_id:
        selected = [it for it in awaiting if str(it.get("seq_id", "")).upper() == norm_id]
        if not selected:
            selected = [awaiting[-1]]
    else:
        selected = [awaiting[-1]]

    registered_labels: list[str] = []
    approved_reports: list[dict] = []
    for it in selected:
        it["status"] = "approved"
        it["approved_at"] = datetime.datetime.now().isoformat()
        it["register_similar"] = bool(register_similar)
        approved_reports.append(it["report"])
        if register_similar and it.get("inferred_signature"):
            entry = register_approved_pattern(it["inferred_signature"], approved_by="min7014")
            registered_labels.append(entry.get("label", ""))

    save_awaiting_approvals(aw)
    return {
        "ok": True,
        "approved_items": selected,
        "approved_reports": approved_reports,
        "registered_similar_labels": registered_labels,
    }


def reject_awaiting_report(target_id: str = "") -> dict:
    """
    대기 중인 Track 3 오류신고를 '수정 안 함(기각/보류)'으로 0-크레딧 즉시 종결합니다.
    """
    aw = load_awaiting_approvals()
    items = aw.get("items", [])
    awaiting = [it for it in items if it.get("status") == "awaiting"]
    if not awaiting:
        return {"ok": False, "reason": "no_awaiting_reports", "rejected_ids": []}

    norm_id = target_id.strip().upper()
    if norm_id and not norm_id.startswith("R") and norm_id != "ALL":
        norm_id = f"R{norm_id}"

    if norm_id == "ALL":
        selected = awaiting
    elif norm_id:
        selected = [it for it in awaiting if str(it.get("seq_id", "")).upper() == norm_id]
        if not selected:
            selected = [awaiting[-1]]
    else:
        selected = [awaiting[-1]]

    rejected_ids: list[str] = []
    for it in selected:
        it["status"] = "rejected"
        it["rejected_at"] = datetime.datetime.now().isoformat()
        rejected_ids.append(str(it.get("seq_id", "")))
        rep = it.get("report") or {}
        post_fix_report(
            str(rep.get("timestamp") or ""),
            str(rep.get("quiz_slug") or ""),
            str(rep.get("question_num") or ""),
            "ℹ️ [회장님 화면 확인 완료 · 현행 유지 결정 (코드 미수정 종결)]",
        )

    save_awaiting_approvals(aw)
    return {"ok": True, "rejected_ids": rejected_ids}


# ---------------------------------------------------------------------------
# 메인 폴링 & 3-Track 라우터
# ---------------------------------------------------------------------------
def poll_and_notify_error_reports_once(send_telegram: bool = True) -> dict:
    """
    Google Sheets 오류 신고 목록을 조회하여:
    - Track 0 (noise / hold): 0-크레딧 자동 정리 또는 보안 보류
    - Track 1 (math_error) & Track 2 (approved_similar): 스크린샷 알림 후 `valid_autofix_targets`로 즉시 수리 전달!
    - Track 3 (ask_with_screenshot): 스크린샷 그림 + 인라인 버튼을 텔레그램에 전송하고 회장님 승인 전까지 대기!
    """
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        all_reports = fetch_all_reports(timeout=12)
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "total": 0,
            "unfixed": 0,
            "newly_alerted": [],
            "valid_autofix_targets": [],
            "awaiting_approval_targets": [],
        }

    proc = load_processed()
    processed_items = proc.setdefault("processed", [])
    alerted_keys = set(proc.setdefault("alerted_keys", []))

    aw = load_awaiting_approvals()
    aw_items = aw.setdefault("items", [])
    aw_by_key = {it.get("report_key"): it for it in aw_items if it.get("report_key")}

    unfixed_list: list[dict] = []
    newly_immediate_alerted: list[dict] = []
    newly_asked_approval: list[dict] = []
    immediate_autofix_targets: list[dict] = []
    awaiting_approval_targets: list[dict] = []
    held_reports: list[tuple[dict, str]] = []

    for idx_zero, r in enumerate(all_reports):
        sheet_seq = idx_zero + 1
        if r.get("fix_timestamp"):
            continue
        ts = str(r.get("timestamp") or "")
        qs = str(r.get("quiz_slug") or "")
        qn = str(r.get("question_num") or "")
        r_key = _make_report_key(r)

        already_done = any(
            str(p.get("timestamp") or "") == ts
            and str(p.get("quiz_slug") or "") == qs
            and str(p.get("question_num") or "") == qn
            and p.get("status") in ("fixed", "resolved", "held", "declined")
            for p in processed_items
        )
        if already_done:
            continue

        # 이미 회장님이 승인(approved)해 둔 대기 항목이면 즉시 수리 타겟에 포함
        existing_aw = aw_by_key.get(r_key)
        if existing_aw:
            if existing_aw.get("status") == "rejected":
                continue
            if existing_aw.get("status") == "approved":
                unfixed_list.append(r)
                immediate_autofix_targets.append(r)
                continue
            if existing_aw.get("status") == "awaiting":
                unfixed_list.append(r)
                awaiting_approval_targets.append(r)
                continue

        triage = triage_error_report(r)
        track = triage["track"]

        if track == "noise":
            post_fix_report(ts, qs, qn, f"ℹ️ [0-크레딧 자동 정리] {triage['reason']}")
            continue

        if track == "hold":
            processed_items.append(
                {
                    "timestamp": ts,
                    "quiz_slug": qs,
                    "question_num": qn,
                    "status": "held",
                    "fix": triage["reason"],
                    "fixed_at": datetime.datetime.now().isoformat(),
                }
            )
            if r_key not in alerted_keys:
                alerted_keys.add(r_key)
                held_reports.append((r, triage["reason"]))
            save_processed(proc)
            continue

        seq_id = _make_short_id(r, sheet_seq=sheet_seq)
        unfixed_list.append(r)

        if track in ("math_error", "approved_similar"):
            immediate_autofix_targets.append(r)
            if r_key not in alerted_keys:
                alerted_keys.add(r_key)
                shot = capture_error_report_screenshot(r, seq_id=seq_id) if send_telegram else None
                if send_telegram:
                    _send_telegram_immediate_autofix_notice(r, triage, seq_id, shot)
                r_with_meta = dict(r)
                r_with_meta["_triage_track"] = track
                r_with_meta["_triage_label"] = triage.get("pattern_label", "")
                r_with_meta["_screenshot_path"] = str(shot) if shot else ""
                newly_immediate_alerted.append(r_with_meta)
        else:
            # Track 3: ask_with_screenshot (화면 그림을 보여주고 고칠지 먼저 질문!)
            awaiting_approval_targets.append(r)
            if r_key not in alerted_keys:
                alerted_keys.add(r_key)
                shot = capture_error_report_screenshot(r, seq_id=seq_id)
                msg_id = (
                    _send_telegram_track3_approval_request(r, triage, seq_id, shot)
                    if send_telegram
                    else None
                )
                aw_entry = {
                    "seq_id": seq_id,
                    "report_key": r_key,
                    "status": "awaiting",
                    "asked_at": datetime.datetime.now().isoformat(),
                    "tg_message_id": msg_id,
                    "screenshot_path": str(shot) if shot else "",
                    "inferred_signature": triage.get("inferred_signature"),
                    "report": r,
                }
                aw_items.append(aw_entry)
                save_awaiting_approvals(aw)
                newly_asked_approval.append(aw_entry)

    PENDING_FILE.write_text(
        json.dumps(
            {
                "checked_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_reports": len(all_reports),
                "unfixed_count": len(unfixed_list),
                "immediate_autofix_count": len(immediate_autofix_targets),
                "awaiting_chairman_approval_count": len(awaiting_approval_targets),
                "unfixed_reports": unfixed_list,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if held_reports and send_telegram:
        try:
            import mathedu_telegram_bridge as tg_bridge
            cfg = tg_bridge.load_env_config()
            tk, cid = cfg.get("TELEGRAM_BOT_TOKEN", ""), cfg.get("TELEGRAM_CHAT_ID", "")
            if tk and cid:
                h_lines = ["🛡️ [Rule 4 보안·도메인 필터 보류 보고 (코드 미수정)]"]
                for hr, hreason in held_reports[:3]:
                    h_lines.append(f"• [{hr.get('quiz_slug')}] {hreason}")
                tg_bridge.send_msg(tk, cid, "\n".join(h_lines))
        except Exception:
            pass

    if newly_immediate_alerted or newly_asked_approval:
        proc["alerted_keys"] = sorted(alerted_keys)
        save_processed(proc)

    return {
        "ok": True,
        "total": len(all_reports),
        "unfixed": len(unfixed_list),
        # `newly_alerted` & `valid_autofix_targets` contain ONLY immediate auto-fix targets
        # (Track 1 math_error + Track 2 approved_similar + explicitly approved Track 3 items)
        "newly_alerted": newly_immediate_alerted,
        "newly_asked_approval": newly_asked_approval,
        "valid_autofix_targets": immediate_autofix_targets,
        "awaiting_approval_targets": awaiting_approval_targets,
    }


def _resolve_agy_cli() -> str:
    found = shutil.which("agy")
    if found:
        return found
    cand = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\min\AppData\Local")) / "agy" / "bin" / "agy.EXE"
    if cand.exists():
        return str(cand)
    return "agy"


def _can_consume_autofix_slot() -> bool:
    now = time.time()
    runs: list[float] = []
    if AUTOFIX_RATE_FILE.exists():
        try:
            data = json.loads(AUTOFIX_RATE_FILE.read_text(encoding="utf-8"))
            runs = [float(x) for x in (data.get("runs") or []) if now - float(x) < 3600.0]
        except Exception:
            runs = []
    if len(runs) >= MAX_AUTOFIX_RUNS_PER_HOUR:
        return False
    runs.append(now)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    AUTOFIX_RATE_FILE.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")
    return True


def run_autonomous_agy_autofix(reports: list[dict] | None = None, notify_telegram: bool = True) -> dict:
    """
    [IDE 창이 닫혀 있을 때도 작동하는 24/7 백그라운드 자율 수리·배포 엔진]
    오직 즉시 수리 대상(Track 1 수학적 오류, Track 2 기승인 유사 오류, 또는 회장님이 승인한 Track 3 항목)만 실행합니다.
    """
    if reports is None:
        polled = poll_and_notify_error_reports_once(send_telegram=False)
        reports = polled.get("valid_autofix_targets") or []
    if not reports:
        return {"ok": True, "status": "no_unfixed_reports", "fixed": 0}

    if not _can_consume_autofix_slot():
        return {"ok": False, "status": "rate_limited_hourly_cap", "pending": len(reports)}

    batch = reports[:5]
    batch_json = json.dumps(batch, ensure_ascii=False, indent=2)
    prompt = (
        "[mathedu 홈페이지 오류신고 3트랙 검증·전수 수리·배포 모드]\n"
        "아래는 즉시 수리 대상(① 수학적 내용 오류 제보, ② 기승인 유사 오류 유형, 또는 ③ 회장님 화면 확인 후 수정 승인 건)입니다.\n"
        "반드시 GEMINI.md의 Rule 1, Rule 2, Rule 4, Rule 5, Rule 13.2, Rule 48을 엄수하여 즉시 자율 완결하십시오:\n"
        "1. 수학적 오류 제보인 경우 먼저 수학적 진위를 엄밀히 검산하여 실제로 틀린 수식·계산·정답·해설이 맞으면 즉시 정확하게 수정하고, 만약 원문 수학이 100% 옳다면 코드를 훼손하지 말고 정확한 검산 설명으로 시트를 종결하십시오.\n"
        "2. UI·수식 렌더링·번역·스크립트 오류인 경우 국소 땜질을 금지하고 전체 파일(index.html, video_board.html, mathlab.html, mathedu-room.js, mathedu-i18n.js, board/*.html 등)에서 동일 패턴을 전수 점검·수정하십시오.\n"
        "3. board/*.html, mathedu-room.js, mathedu-i18n.js를 수정한 경우 반드시 `python -X utf8 build_offline_quizzes.py`를 실행하여 offline/*.html을 동기화하십시오.\n"
        "4. 수정된 웹/소스 파일만 안전하게 git add(.mp4/.png/.agents/.temp/비밀키 절대 제외) -> git commit -> `git push origin main`으로 라이브 홈페이지를 즉시 업데이트하십시오.\n"
        "5. 각 처리 완료 항목마다 `python -X utf8 -c \"import _antigravity_report_watcher as w; w.post_fix_report(ts, slug, qnum, summary)\"`를 호출하여 Google Sheets F·G열에 완료 내역을 기록하십시오.\n"
        "6. 마지막에는 수행한 수리 요약 텍스트(한국어 5~8줄)만 표준 출력(stdout)으로 간결히 출력하십시오(`--reply`나 `--listen-once`는 직접 호출 금지).\n\n"
        f"[처리 대상 오류 신고 JSON]\n{batch_json}"
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
        if notify_telegram and summary:
            try:
                import mathedu_telegram_bridge as tg_bridge
                cfg = tg_bridge.load_env_config()
                tk, cid = cfg.get("TELEGRAM_BOT_TOKEN", ""), cfg.get("TELEGRAM_CHAT_ID", "")
                if tk and cid:
                    tg_bridge.send_msg(
                        tk,
                        cid,
                        f"✅ [mathedu 오류신고 자율 수리 & GitHub Pages 배포 완료]\n\n{summary[-2500:]}",
                    )
            except Exception:
                pass
        return {"ok": proc.returncode == 0, "status": "completed", "summary": summary[-1000:]}
    except Exception as e:
        return {"ok": False, "status": f"error: {e}"}


def format_approved_patterns_summary() -> str:
    reg = load_approved_patterns()
    pats = reg.get("patterns") or []
    lines = [
        "📋 [mathedu 오류신고 3트랙 정책 및 자동수리 등록 유형 현황]",
        "• Track 1 (즉시 수리): 수학적으로 틀린 내용(수식·계산·부호·정답·논리 오류) ➔ 묻지 않고 즉시 검산·수정",
        f"• Track 2 (즉시 수리): 기승인 유사 오류 유형 ({len(pats)}종 등록) ➔ 묻지 않고 즉시 전수 수리",
        "• Track 3 (화면 보고 후 질문): 신규 유형 화면·기능·제안 ➔ 텔레그램에 스크린샷 전송 후 수정 여부 질문",
        "",
        "🔖 [현재 등록된 기승인 유사 오류 유형 목록]:",
    ]
    for i, p in enumerate(pats, 1):
        lines.append(f"  {i}) {p.get('label')} (`{p.get('category_id')}`)")
    awaiting = get_pending_approval_items()
    lines.append(f"\n⏳ 현재 회장님 수정 승인 대기 중인 신고: {len(awaiting)}건")
    for it in awaiting[:5]:
        rep = it.get("report") or {}
        parsed = parse_report_fields(rep)
        lines.append(f"  - [{it.get('seq_id')}] {parsed['quiz_slug']}: {parsed['detail'][:70]}")
    return "\n".join(lines)


def format_error_reports_summary() -> str:
    try:
        all_reports = fetch_all_reports(timeout=12)
    except Exception as e:
        return f"⚠️ [오류신고 시트 조회 실패]: {e}"

    unfixed = [r for r in all_reports if not r.get("fix_timestamp")]
    fixed_cnt = len(all_reports) - len(unfixed)
    awaiting = get_pending_approval_items()
    lines = [
        "🚨 [크레딧 0원 · mathedu 홈페이지 오류신고 & 3트랙 시각 관제 현황]",
        f"• 연동 시트(reports 탭): 누적 {len(all_reports)}건 (✅ 처리 완료 {fixed_cnt}건 / ⏳ 미처리 {len(unfixed)}건 / 📸 회장님 승인대기 {len(awaiting)}건)",
        "• 운영 원칙: ① 수학 오류 즉시 수정 | ② 기승인 유사 오류 즉시 수정 | ③ 신규 유형은 화면 스크린샷 보고 후 질문",
    ]
    if not unfixed:
        lines.append("• 현재 미처리된 오류 신고가 **0건**입니다! (최근 신고까지 전량 처리 완료)")
        recent = all_reports[-3:]
        if recent:
            lines.append("• 최근 처리 완료 내역:")
            for r in reversed(recent):
                qs = r.get("quiz_slug") or "mathedu"
                res = str(r.get("fix_result") or "수리 완료")[:90]
                lines.append(f"  - [{qs}] {res}")
    else:
        lines.append("• 미처리 오류 신고 목록:")
        for idx, r in enumerate(unfixed[:8], 1):
            ts = str(r.get("timestamp") or "")[:16].replace("T", " ")
            qs = r.get("quiz_slug") or "mathedu"
            qn = r.get("question_num") or "-"
            snippet = " ".join(str(r.get("text") or "").splitlines()[:2])[:100]
            lines.append(f"  {idx}) [{qs} | 단계:{qn}] ({ts}) {snippet}")
    return "\n".join(lines)


def main() -> None:
    if "--check-once" in sys.argv:
        res = poll_and_notify_error_reports_once(send_telegram=("--no-tg" not in sys.argv))
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if "--summary" in sys.argv:
        print(format_error_reports_summary())
        return
    if "--patterns" in sys.argv:
        print(format_approved_patterns_summary())
        return
    print("[ANTIGRAVITY_WATCHER_ONLINE] mathedu 3트랙 실시간 오류 신고 감시 데몬 가동 중 (60초 주기)", flush=True)
    while True:
        try:
            poll_and_notify_error_reports_once(send_telegram=True)
        except Exception:
            pass
        time.sleep(60)


if __name__ == "__main__":
    main()
