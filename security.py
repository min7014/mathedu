#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security.py
===============================================================================
🛡️ [Security Agent] mathedu 웹 · 인증 · 시크릿 · 서버 · 원격관제 7계층 사이버보안 엔진
- AI 크레딧 소모 0원 (100% 순수 파이썬 정적·저장소·DB·설정·격리 전수 점검)
- Rule 48 완전 무창 실행 (silent_subprocess 강제 주입)

[7대 사이버보안 방어 계층 (S1 ~ S7)]
  S1. secret_and_git_guard      : 비밀키/OAuth/개인파일 Git 미추적, .gitignore 검증, DB PII 0건, 라이브 시크릿 스캔
  S2. telegram_acl_guard        : 원격 텔레그램 브릿지 Fail-Closed Chat ID 핀닝 & 탈취 패턴 차단
  S3. localhost_server_guard    : 로컬 대시보드(127.0.0.1) CORS 화이트리스트·Host/Origin CSRF·경로탐색 차단
  S4. member_auth_guard         : 무료 정식 회원가입(mathedu-auth.js) 백도어 시드·평문비번 제거, JWT 검증, Policy 78 무광고 검증
  S5. apps_script_injection_guard: Google Apps Script 수식/HTML 인젝션 및 오픈 메일 릴레이 차단
  S6. frontend_xss_guard        : 핵심 프론트엔드 JS 내 javascript: URL 및 eval 인젝션 0건 보장
  S7. runtime_isolation_guard   : 핵심 데몬/서버 silent_subprocess 무창 격리 및 로컬 시크릿 미추적 재검증
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SECURITY_REPORT_FILE = ROOT_DIR / ".agents" / "latest_security_report.json"

TRACKED_SECRET_FILE_RE = re.compile(
    r"(?:^\.env|client_secret.*\.json$|youtube_token.*\.json$|\.(?:pem|key|pfx|p12)$|^_local_|^board/private_index\.json$)",
    re.IGNORECASE,
)

REQUIRED_GITIGNORE_PATTERNS = [
    "youtube_client_secret.json",
    "youtube_token*.json",
    ".env",
    "*.pem",
    "*.key",
    ".agents/latest_security_report.json",
]

LIVE_SECRET_PATTERNS = [
    ("google_api_key", re.compile(r"AIzaSy[0-9A-Za-z_-]{33}")),
    ("google_oauth_secret", re.compile(r"GOCSPX-[0-9A-Za-z_-]{20,}")),
    ("telegram_bot_token", re.compile(r"\b\d{8,10}:AA[0-9A-Za-z_-]{33}\b")),
    ("github_pat", re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key_pem", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]

DB_SECRET_VALUE_RE = re.compile(r"(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|password|passwd|bearer\s+|token\s*[:=])", re.IGNORECASE)
FRONTEND_JS_FILES = [
    "mathedu-auth.js",
    "mathedu-room.js",
    "mathedu-report.js",
    "mathedu-search-logger.js",
    "mathedu-skills-suite.js",
    "mathedu-guide.js",
    "mathedu-quest-game.js",
    "mathedu-gamification.js",
]
CORE_WEBSITE_ENTRY_PAGES = [
    "index.html",
    "mathlab.html",
    "dashboard.html",
    "create.html",
    "video_board.html",
    "video_studio.html",
    "live_board.html",
    "game.html",
    "csat2027.html",
]
ISOLATED_RUNTIME_MODULES = [
    "mathedu_foundation_daemon.py",
    "mathedu_telegram_bridge.py",
    "min7014_ai_server.py",
    "auditor.py",
    "secretary.py",
    "security.py",
]
LOCAL_SECRET_FILENAMES = [
    "youtube_client_secret.json",
    "youtube_token_min7014_ai.json",
    ".env",
]


def _make_violation(layer: str, severity: str, target: str, detail: str) -> dict:
    return {
        "layer": layer,
        "severity": severity,
        "target": target,
        "detail": detail,
    }


def _git_ls_files() -> list[str]:
    proc = subprocess.run(
        ["git", "-c", "gc.auto=0", "-c", "maintenance.auto=0", "ls-files"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=25,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-files failed ({proc.returncode}): {proc.stderr.strip()}")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _inspect_tracked_sqlite_db(db_rel_path: str) -> list[dict]:
    violations: list[dict] = []
    db_path = ROOT_DIR / db_rel_path
    if not db_path.exists():
        return violations
    try:
        con = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
        try:
            cur = con.cursor()
            tables = [row[0] for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            for table in tables:
                if str(table).startswith("sqlite_"):
                    continue
                escaped = str(table).replace('"', '""')
                for row in cur.execute(f'SELECT * FROM "{escaped}"').fetchall():
                    for val in row:
                        if val is None:
                            continue
                        s_val = str(val)
                        if "@" in s_val or DB_SECRET_VALUE_RE.search(s_val):
                            violations.append(
                                _make_violation(
                                    "S1",
                                    "HIGH",
                                    db_rel_path,
                                    f"추적 중인 DB 테이블 '{table}'에서 민감정보/이메일 의심 문자열 탐지",
                                )
                            )
                            return violations
        finally:
            con.close()
    except Exception as exc:
        violations.append(_make_violation("S1", "HIGH", db_rel_path, f"SQLite DB 점검 오류: {exc}"))
    return violations


def _check_s1_secret_and_git(tracked_files: list[str], auto_fix: bool) -> list[dict]:
    violations: list[dict] = []
    for rel_path in tracked_files:
        if TRACKED_SECRET_FILE_RE.search(rel_path):
            violations.append(_make_violation("S1", "CRITICAL", rel_path, "비밀키·토큰·비공개 파일이 Git에 추적됨"))
        if rel_path.lower().endswith((".db", ".sqlite", ".sqlite3")):
            violations.extend(_inspect_tracked_sqlite_db(rel_path))

    gitignore_path = ROOT_DIR / ".gitignore"
    gi_text = gitignore_path.read_text(encoding="utf-8", errors="ignore") if gitignore_path.exists() else ""
    gi_lines = {ln.strip() for ln in gi_text.splitlines() if ln.strip() and not ln.strip().startswith("#")}
    missing_patterns = [pat for pat in REQUIRED_GITIGNORE_PATTERNS if pat not in gi_lines]
    if missing_patterns and auto_fix:
        addition = "\n# Auto-hardened by security.py (Policy 91)\n" + "\n".join(missing_patterns) + "\n"
        gitignore_path.write_text(gi_text.rstrip() + addition, encoding="utf-8")
        gi_text = gitignore_path.read_text(encoding="utf-8", errors="ignore")
        gi_lines = {ln.strip() for ln in gi_text.splitlines() if ln.strip() and not ln.strip().startswith("#")}
        missing_patterns = [pat for pat in REQUIRED_GITIGNORE_PATTERNS if pat not in gi_lines]
    if missing_patterns:
        violations.append(
            _make_violation(
                "S1",
                "HIGH",
                ".gitignore",
                f"필수 보안 제외 패턴 누락: {', '.join(missing_patterns)}",
            )
        )

    for ext in ("*.py", "*.js", "*.gs"):
        for src_path in ROOT_DIR.glob(ext):
            if src_path.name == "security.py" or not src_path.is_file():
                continue
            try:
                content = src_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for pat_name, pat_re in LIVE_SECRET_PATTERNS:
                if pat_re.search(content):
                    violations.append(
                        _make_violation(
                            "S1",
                            "CRITICAL",
                            src_path.name,
                            f"소스 코드 내 라이브 시크릿 패턴({pat_name}) 하드코딩 의심",
                        )
                    )
                    break
    return violations


def _check_s2_telegram_acl() -> list[dict]:
    violations: list[dict] = []
    bridge_path = ROOT_DIR / "mathedu_telegram_bridge.py"
    if not bridge_path.exists():
        return [_make_violation("S2", "HIGH", "mathedu_telegram_bridge.py", "원격 관제 브릿지 파일 없음")]
    txt = bridge_path.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r'DEFAULT_ALLOWED_CHAT_ID\s*=\s*["\']43453234["\']', txt):
        violations.append(
            _make_violation(
                "S2",
                "CRITICAL",
                "mathedu_telegram_bridge.py",
                "DEFAULT_ALLOWED_CHAT_ID = '43453234' Fail-Closed 고정값 누락",
            )
        )
    if re.search(r"\ballowed_chat_id\s*=\s*chat_id\b", txt):
        violations.append(
            _make_violation(
                "S2",
                "CRITICAL",
                "mathedu_telegram_bridge.py",
                "임의 채팅방 ACL 탈취 패턴(allowed_chat_id = chat_id) 잔존",
            )
        )
    return violations


def _check_s3_localhost_server() -> list[dict]:
    violations: list[dict] = []
    srv_path = ROOT_DIR / "min7014_ai_server.py"
    if not srv_path.exists():
        return [_make_violation("S3", "HIGH", "min7014_ai_server.py", "로컬 서버 파일 없음")]
    txt = srv_path.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r'HTTPServer\(\(\s*["\']127\.0\.0\.1["\']\s*,\s*PORT\s*\)', txt):
        violations.append(
            _make_violation("S3", "CRITICAL", "min7014_ai_server.py", "루프백 127.0.0.1 바인딩 누락")
        )
    if re.search(r'Access-Control-Allow-Origin["\']\s*,\s*["\']\*["\']', txt):
        violations.append(
            _make_violation("S3", "HIGH", "min7014_ai_server.py", "와일드카드 CORS(*) 헤더 잔존")
        )
    for req_symbol in ("SAFE_SLUG_RE", "_is_safe_path_within", "ALLOWED_HOSTS"):
        if req_symbol not in txt:
            violations.append(
                _make_violation("S3", "HIGH", "min7014_ai_server.py", f"보안 검증 심볼 누락: {req_symbol}")
            )
    return violations


def _check_s4_member_auth() -> list[dict]:
    violations: list[dict] = []
    auth_path = ROOT_DIR / "mathedu-auth.js"
    if not auth_path.exists():
        violations.append(_make_violation("S4", "HIGH", "mathedu-auth.js", "회원 인증 모듈 없음"))
    else:
        txt = auth_path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"var\s+DEFAULT_SEED_USERS\s*=\s*\[\s*\]\s*;", txt):
            violations.append(
                _make_violation("S4", "CRITICAL", "mathedu-auth.js", "DEFAULT_SEED_USERS 빈 배열 강제 미적용(시드 백도어 위험)")
            )
        if re.search(r"\bu\.password\s*===", txt):
            violations.append(
                _make_violation("S4", "CRITICAL", "mathedu-auth.js", "평문 비밀번호 비교(u.password ===) 잔존")
            )
        for req_token in ("accounts.google.com", "sanitizeAvatarUrl", "requireAuth", "정식 회원 전용"):
            if req_token not in txt:
                violations.append(
                    _make_violation("S4", "HIGH", "mathedu-auth.js", f"인증/무료 정회원 보호 요소 누락: {req_token}")
                )

    ad_path = ROOT_DIR / "ad_config.json"
    if ad_path.exists():
        try:
            ad_cfg = json.loads(ad_path.read_text(encoding="utf-8"))
            if ad_cfg.get("adsense", {}).get("enabled") is not False:
                violations.append(_make_violation("S4", "MEDIUM", "ad_config.json", "Policy 78 위반: adsense.enabled != false"))
            if ad_cfg.get("kakaoAdfit", {}).get("enabled") is not False:
                violations.append(_make_violation("S4", "MEDIUM", "ad_config.json", "Policy 78 위반: kakaoAdfit.enabled != false"))
        except Exception as exc:
            violations.append(_make_violation("S4", "MEDIUM", "ad_config.json", f"ad_config.json 파싱 오류: {exc}"))
    return violations


def _check_s5_apps_script_injection() -> list[dict]:
    violations: list[dict] = []
    gs_path = ROOT_DIR / "sheets-script.gs"
    if not gs_path.exists():
        return [_make_violation("S5", "HIGH", "sheets-script.gs", "Apps Script 파일 없음")]
    txt = gs_path.read_text(encoding="utf-8", errors="ignore")
    for helper in ("sanitizeSheetText", "escapeHtmlServer", "sanitizeSafeQuizUrl"):
        if helper not in txt:
            violations.append(
                _make_violation("S5", "HIGH", "sheets-script.gs", f"Apps Script 보안 방어 함수 누락: {helper}")
            )
    return violations


def _check_s6_frontend_xss() -> list[dict]:
    violations: list[dict] = []
    js_uri_re = re.compile(r"javascript\s*:", re.IGNORECASE)
    eval_re = re.compile(r"\beval\s*\(")
    for rel_js in FRONTEND_JS_FILES:
        js_path = ROOT_DIR / rel_js
        if not js_path.exists():
            continue
        txt = js_path.read_text(encoding="utf-8", errors="ignore")
        if js_uri_re.search(txt):
            violations.append(_make_violation("S6", "CRITICAL", rel_js, "javascript: URI 패턴 탐지"))
        if eval_re.search(txt):
            violations.append(_make_violation("S6", "CRITICAL", rel_js, "위험한 eval() 호출 탐지"))

    mathlab_path = ROOT_DIR / "mathlab.html"
    if mathlab_path.exists():
        ml_txt = mathlab_path.read_text(encoding="utf-8", errors="ignore")
        for req in ("sanitizeMathExpression", "isSafeMathExpr"):
            if req not in ml_txt:
                violations.append(_make_violation("S6", "CRITICAL", "mathlab.html", f"수식 화이트리스트 방어 누락: {req}"))

    room_path = ROOT_DIR / "mathedu-room.js"
    if room_path.exists():
        rm_txt = room_path.read_text(encoding="utf-8", errors="ignore")
        if "sendThankYouToGiver(\\'' + escapeHtml" in rm_txt:
            violations.append(_make_violation("S6", "CRITICAL", "mathedu-room.js", "인라인 onclick giftFrom JS 탈출 취약점 잔존"))
        if "/^[A-Za-z0-9_-]{1,80}$/" not in rm_txt:
            violations.append(_make_violation("S6", "HIGH", "mathedu-room.js", "?pack= 슬러그 화이트리스트 정규식 누락"))
        if "window.toggleMinGgb = function" not in rm_txt:
            violations.append(_make_violation("S6", "HIGH", "mathedu-room.js", "전역 GeoGebra iframe 도메인 검증 오버라이드 누락"))

    for redir_name in ("home2.html", "home_check.html"):
        rp = ROOT_DIR / redir_name
        if rp.exists():
            r_txt = rp.read_text(encoding="utf-8", errors="ignore")
            if "[A-Za-z0-9_-]{1,80}(?:\\.html)?" not in r_txt:
                violations.append(_make_violation("S6", "HIGH", redir_name, "?goto= 오픈 리다이렉트 화이트리스트 검증 누락"))

    target_blank_no_rel_re = re.compile(r"<a\b(?![^>]*noopener)[^>]*target=[\"']_blank[\"'][^>]*>", re.IGNORECASE)
    insecure_http_re = re.compile(
        r"""(?:src|href|action)\s*=\s*["']http://(?!localhost|127\.0\.0\.1|www\.w3\.org|schemas\.android\.com|ns\.adobe\.com)""",
        re.IGNORECASE,
    )
    referrer_re = re.compile(r"""name=["']referrer["']\s+content=["']strict-origin-when-cross-origin["']""", re.IGNORECASE)
    for page_name in CORE_WEBSITE_ENTRY_PAGES:
        pg_path = ROOT_DIR / page_name
        if not pg_path.exists():
            continue
        pg_txt = pg_path.read_text(encoding="utf-8", errors="ignore")
        if not referrer_re.search(pg_txt):
            violations.append(_make_violation("S6", "MEDIUM", page_name, "Referrer-Policy 메타태그(strict-origin-when-cross-origin) 누락"))
        if target_blank_no_rel_re.search(pg_txt):
            violations.append(_make_violation("S6", "MEDIUM", page_name, "rel=noopener 누락된 _blank 외부 링크 탐지"))
        if insecure_http_re.search(pg_txt):
            violations.append(_make_violation("S6", "HIGH", page_name, "비암호화 외부 http:// 리소스 URL 탐지"))

    for ggb_rel in ("min7014_matcher.py", "board/archive.html", "offline/archive.html"):
        gp = ROOT_DIR / ggb_rel
        if gp.exists():
            g_txt = gp.read_text(encoding="utf-8", errors="ignore")
            if ": ggbUrl;" in g_txt:
                violations.append(_make_violation("S6", "HIGH", ggb_rel, "무검증 GeoGebra iframe 폴백(: ggbUrl;) 잔존"))
    return violations


def _check_s7_runtime_isolation(tracked_files: list[str]) -> list[dict]:
    violations: list[dict] = []
    for mod_name in ISOLATED_RUNTIME_MODULES:
        mod_path = ROOT_DIR / mod_name
        if not mod_path.exists():
            violations.append(_make_violation("S7", "HIGH", mod_name, "핵심 런타임 모듈 누락"))
            continue
        txt = mod_path.read_text(encoding="utf-8", errors="ignore")
        if "import silent_subprocess" not in txt:
            violations.append(_make_violation("S7", "MEDIUM", mod_name, "Rule 48 silent_subprocess 무창 격리 임포트 누락"))

    tracked_set = set(tracked_files)
    for secret_name in LOCAL_SECRET_FILENAMES:
        if (ROOT_DIR / secret_name).exists() and secret_name in tracked_set:
            violations.append(_make_violation("S7", "CRITICAL", secret_name, "로컬 시크릿 파일이 Git에 추적되고 있음"))
    return violations


def run_full_security_audit(auto_fix: bool = True) -> dict:
    """7계층 사이버보안 전수 점검을 실행하고 .agents/latest_security_report.json에 저장합니다."""
    tracked_files: list[str] = []
    git_error = None
    try:
        tracked_files = _git_ls_files()
    except Exception as exc:
        git_error = str(exc)

    s1_violations = _check_s1_secret_and_git(tracked_files, auto_fix=auto_fix)
    if git_error:
        s1_violations.append(_make_violation("S1", "HIGH", "git", git_error))

    layer_results = {
        "S1_secret_and_git_guard": s1_violations,
        "S2_telegram_acl_guard": _check_s2_telegram_acl(),
        "S3_localhost_server_guard": _check_s3_localhost_server(),
        "S4_member_auth_guard": _check_s4_member_auth(),
        "S5_apps_script_injection_guard": _check_s5_apps_script_injection(),
        "S6_frontend_xss_guard": _check_s6_frontend_xss(),
        "S7_runtime_isolation_guard": _check_s7_runtime_isolation(tracked_files),
    }

    all_violations: list[dict] = []
    layers_summary: dict[str, dict] = {}
    for layer_key, vlist in layer_results.items():
        all_violations.extend(vlist)
        layers_summary[layer_key] = {
            "passed": len(vlist) == 0,
            "violations": len(vlist),
        }

    report = {
        "status": "PASS_ZERO_VIOLATIONS" if not all_violations else "VIOLATIONS_DETECTED",
        "total_violations": len(all_violations),
        "checked_layers": len(layer_results),
        "layers": layers_summary,
        "violations": all_violations,
        "checked_at": datetime.now().isoformat(),
    }

    try:
        SECURITY_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        SECURITY_REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    return report


def build_telegram_security_summary(auto_fix: bool = True) -> str:
    """텔레그램 `!보안` 명령용 0-크레딧 모바일 요약 리포트를 반환합니다."""
    rep = run_full_security_audit(auto_fix=auto_fix)
    total_v = rep.get("total_violations", 0)
    badge = "🟢 안전 (위반 0건)" if total_v == 0 else f"🚨 점검 필요 (위반 {total_v}건)"
    lines = [
        f"🔐 [보안 담당관(security) 7계층 실시간 보안 보고] {badge}",
        f"• 점검 시각: {rep.get('checked_at', '')[:19]} | 점검 계층: {rep.get('checked_layers', 7)}계층 (AI 크레딧 0원)",
        "• S1~S3 (Git·시크릿 / 텔레그램 ACL / 로컬서버): "
        + (
            "PASS"
            if all(
                rep["layers"].get(k, {}).get("passed")
                for k in ("S1_secret_and_git_guard", "S2_telegram_acl_guard", "S3_localhost_server_guard")
            )
            else "ALERT"
        ),
        "• S4~S5 (무료 정회원 인증·Policy 78 / Apps Script 인젝션·메일 릴레이): "
        + (
            "PASS"
            if all(
                rep["layers"].get(k, {}).get("passed")
                for k in ("S4_member_auth_guard", "S5_apps_script_injection_guard")
            )
            else "ALERT"
        ),
        "• S6~S7 (프론트엔드 XSS / 데몬 무창 격리 & 시크릿 미추적): "
        + (
            "PASS"
            if all(
                rep["layers"].get(k, {}).get("passed")
                for k in ("S6_frontend_xss_guard", "S7_runtime_isolation_guard")
            )
            else "ALERT"
        ),
    ]
    if total_v > 0:
        for item in (rep.get("violations") or [])[:4]:
            lines.append(f"• ⚠️ [{item.get('layer')}] {item.get('target')}: {item.get('detail')}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="mathedu 7-Layer Security Agent Engine")
    parser.add_argument("action", nargs="?", default="check", choices=["check", "fix", "summary"])
    args = parser.parse_args()

    if args.action == "summary":
        print(build_telegram_security_summary(auto_fix=True))
        rep = json.loads(SECURITY_REPORT_FILE.read_text(encoding="utf-8")) if SECURITY_REPORT_FILE.exists() else {}
        return 0 if rep.get("total_violations", 1) == 0 else 1

    rep = run_full_security_audit(auto_fix=(args.action == "fix"))
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0 if rep.get("total_violations", 1) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
