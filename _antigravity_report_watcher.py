#!/usr/bin/env python3
"""
mathedu 안티그래비티 전용 실시간 오류 신고 감시 및 텔레그램 연동 모듈 (Antigravity Realtime Error Report Watcher)
Google Sheets 백엔드(?action=reports)를 상시 점검하여:
1. 신규 홈페이지 오류 신고 감지 시:
   - .agents/pending_error_reports.json 큐에 저장 및 중복 알림 방지(.agents/processed_error_reports.json)
   - 회장님 전용 텔레그램(@anti7014_bot, Chat ID: 43453234)으로 실시간 접수 알림 발송
   - 활성 대화 세션(--listen-once) 가동 중일 경우 Reactive Wakeup 트리거로 자율 전수 수리(Rule 4 & Rule 5) 연계
2. 수리 완료 시:
   - post_fix_report(...)를 통해 Google Sheets(fix_timestamp / fix_result)에 수리 내역 기록 및 신고자 이메일 안내
"""
import datetime
import json
import os
import subprocess
import sys
import time
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

import re
import shutil

REPO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = REPO_DIR / ".agents"
PROCESSED_FILE = AGENTS_DIR / "processed_error_reports.json"
PENDING_FILE = AGENTS_DIR / "pending_error_reports.json"
AUTOFIX_RATE_FILE = AGENTS_DIR / "autofix_rate_state.json"
LEGACY_PROCESSED_FILE = REPO_DIR / "_processed_reports.json"
API_URL_FILE = REPO_DIR / "progress-api-url.txt"
MAX_AUTOFIX_RUNS_PER_HOUR = 3
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
            and p.get("status") in ("fixed", "resolved")
            for p in processed_items
        )
        if not already:
            unfixed.append(r)
    return unfixed


def _send_telegram_error_alert(newly_detected: list[dict], total_unfixed: int) -> None:
    if not newly_detected:
        return
    try:
        import mathedu_telegram_bridge as tg_bridge

        cfg = tg_bridge.load_env_config()
        token = cfg.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = cfg.get("TELEGRAM_CHAT_ID", "") or tg_bridge.load_offset_state().get("chat_id", "")
        if not token or not chat_id:
            return

        lines = [
            f"🚨 [mathedu 홈페이지 신규 오류신고 실시간 감지 ({len(newly_detected)}건 / 미처리 총 {total_unfixed}건)]"
        ]
        for idx, r in enumerate(newly_detected[:5], 1):
            ts = str(r.get("timestamp") or "")[:19].replace("T", " ")
            qs = str(r.get("quiz_slug") or "mathedu")
            qn = str(r.get("question_num") or "-")
            rep = str(r.get("reporter") or "익명")
            raw_txt = str(r.get("text") or "").strip()
            short_txt = " / ".join(ln.strip() for ln in raw_txt.splitlines()[:4] if ln.strip())
            if len(short_txt) > 220:
                short_txt = short_txt[:217] + "..."
            lines.append(
                f"{idx}) [{qs} | 단계:{qn}] ({rep}, {ts})\n"
                f"   • {short_txt}"
            )
        if len(newly_detected) > 5:
            lines.append(f"   ... 외 {len(newly_detected) - 5}건")
        lines.append(
            "\n💡 수학교육 문항·화면 오류(Rule 4 & Rule 5)는 안티그래비티가 전수 점검·수리 후 시트 완료 처리까지 수행합니다. "
            "(실시간 목록 확인: `!신고`)"
        )
        tg_bridge.send_msg(token, chat_id, "\n".join(lines))
    except Exception as e:
        print(f"[ErrorReport Telegram Alert Notice] {e}", flush=True)


def classify_error_report_safety(report: dict) -> tuple[str, str]:
    """
    [0-크레딧 1차 기계적 트리아지 게이트 (Rule 2 · Rule 4 · 쿼터 보호)]
    - 'noise': 의미 없는 자음/모음 연타, '사유 없음', 빈 텍스트 등 -> LLM 호출 없이 0크레딧 자동 종결
    - 'hold' : 프롬프트 인젝션, 셸 명령 유도, 비수학(트레이딩/코인 등) 요청 -> 코드 수정 없이 보류 및 텔레그램 보고(Rule 4)
    - 'valid': 정식 수학교육 문항·수식·레이아웃·기능 오류 신고 또는 신규 문제 출제 요청
    """
    raw_text = str(report.get("text") or "").strip()
    if not raw_text:
        return ("noise", "신고 본문이 비어 있어 자동 종결 처리되었습니다.")

    detail = raw_text
    m_det = re.search(r"\[상세내용\]\s*(.*?)(?=\n\[|\Z)", raw_text, flags=re.S)
    if m_det:
        detail = m_det.group(1).strip()

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
    # 한글 자모 단독 연타(ㅋㅋㅋ, ㅎㅎㅎ, ㅏㅓㅗ 등) 또는 알파벳 무작위 자판 연타(asdf, fsdf 등) 필터
    if re.fullmatch(r"[ㄱ-ㅎㅏ-ㅣ]+", cleaned):
        return ("noise", "구체적 문장 없는 자모 연타 입력으로 확인되어 자동 종결 처리되었습니다.")
    if re.fullmatch(r"[asdfghjklqwertyuiopzxcvbnm]{4,20}", cleaned.lower()) and not re.search(
        r"(math|error|font|text|line|step|quiz|button|link|page|image|svg|pdf|video|wrong|typo)",
        cleaned.lower(),
    ):
        return ("noise", "무작위 영문 자판 테스트 입력으로 확인되어 자동 종결 처리되었습니다.")

    return ("valid", "")


def poll_and_notify_error_reports_once(send_telegram: bool = True) -> dict:
    """
    Google Sheets의 오류 신고 목록을 1회 조회하여:
    - 0-크레딧 노이즈는 즉시 시트 자동 종결하고, 보류 건은 코드 수정 없이 알림만 발송하며,
    - 유효 미해결 신고를 .agents/pending_error_reports.json에 동기화하고 텔레그램 알림을 발송합니다.
    """
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        all_reports = fetch_all_reports(timeout=12)
    except Exception as e:
        return {"ok": False, "error": str(e), "total": 0, "unfixed": 0, "newly_alerted": [], "valid_autofix_targets": []}

    proc = load_processed()
    processed_items = proc.setdefault("processed", [])
    alerted_keys = set(proc.setdefault("alerted_keys", []))

    unfixed_list: list[dict] = []
    newly_detected: list[dict] = []
    valid_autofix_targets: list[dict] = []
    held_reports: list[tuple[dict, str]] = []

    for r in all_reports:
        if r.get("fix_timestamp"):
            continue
        ts = str(r.get("timestamp") or "")
        qs = str(r.get("quiz_slug") or "")
        qn = str(r.get("question_num") or "")
        already_fixed = any(
            str(p.get("timestamp") or "") == ts
            and str(p.get("quiz_slug") or "") == qs
            and str(p.get("question_num") or "") == qn
            and p.get("status") in ("fixed", "resolved", "held")
            for p in processed_items
        )
        if already_fixed:
            continue

        verdict, reason = classify_error_report_safety(r)
        if verdict == "noise":
            post_fix_report(ts, qs, qn, f"ℹ️ [0-크레딧 자동 정리] {reason}")
            continue
        if verdict == "hold":
            processed_items.append(
                {
                    "timestamp": ts,
                    "quiz_slug": qs,
                    "question_num": qn,
                    "status": "held",
                    "fix": reason,
                    "fixed_at": datetime.datetime.now().isoformat(),
                }
            )
            r_key = _make_report_key(r)
            if r_key not in alerted_keys:
                alerted_keys.add(r_key)
                held_reports.append((r, reason))
            save_processed(proc)
            continue

        unfixed_list.append(r)
        valid_autofix_targets.append(r)
        r_key = _make_report_key(r)
        if r_key not in alerted_keys:
            newly_detected.append(r)
            alerted_keys.add(r_key)

    PENDING_FILE.write_text(
        json.dumps(
            {
                "checked_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_reports": len(all_reports),
                "unfixed_count": len(unfixed_list),
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

    if newly_detected:
        proc["alerted_keys"] = sorted(alerted_keys)
        save_processed(proc)
        if send_telegram:
            _send_telegram_error_alert(newly_detected, len(unfixed_list))

    return {
        "ok": True,
        "total": len(all_reports),
        "unfixed": len(unfixed_list),
        "newly_alerted": newly_detected,
        "valid_autofix_targets": valid_autofix_targets,
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
    유효한 수학교육·홈페이지 오류 신고(reports 탭 gid=838754808)가 감지되면:
    1) 시간당 최대 3회 쿼터 보호 캡 내에서 Antigravity CLI(`agy -p`)를 무창 호출하여
    2) Rule 4 & Rule 5 전수 수리 -> 오프라인 재빌드(필요 시) -> Git commit & push origin main ->
    3) Google Sheets F·G열(`post_fix_report`) 수리 완료 기록 및 텔레그램 완료 보고까지 한 번에 수행합니다.
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
        "[mathedu 홈페이지 오류신고 24/7 자율 전수 수리·배포 모드]\n"
        "아래는 Google Sheets(reports 탭, gid=838754808)에 접수된 미처리 수학교육 홈페이지 오류 신고입니다.\n"
        "반드시 GEMINI.md의 Rule 1, Rule 2, Rule 4, Rule 5, Rule 13.2, Rule 48을 엄수하여 즉시 자율 완결하십시오:\n"
        "1. 수학교육/홈페이지 UI·수식·문항·스크립트 오류인 경우 국소 땜질을 금지하고 전체 파일(index.html, video_board.html, mathlab.html, mathedu-room.js, board/*.html 등)에서 동일 패턴을 전수 점검·수정하십시오.\n"
        "2. board/*.html 또는 mathedu-room.js를 수정한 경우 반드시 `python -X utf8 build_offline_quizzes.py`를 실행하여 offline/*.html을 동기화하십시오.\n"
        "3. 수정된 웹/소스 파일만 안전하게 git add(.mp4/.png/.agents/비밀키 절대 제외) -> git commit -> `git push origin main`으로 라이브 홈페이지를 즉시 업데이트하십시오.\n"
        "4. 각 처리 완료 항목마다 `python -X utf8 -c \"import _antigravity_report_watcher as w; w.post_fix_report(ts, slug, qnum, summary)\"`를 호출하여 Google Sheets F·G열에 완료 내역을 기록하십시오.\n"
        "5. 마지막에는 수행한 수리 요약 텍스트(한국어 5~8줄)만 표준 출력(stdout)으로 간결히 출력하십시오(`--reply`나 `--listen-once`는 직접 호출 금지).\n\n"
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


def format_error_reports_summary() -> str:
    try:
        all_reports = fetch_all_reports(timeout=12)
    except Exception as e:
        return f"⚠️ [오류신고 시트 조회 실패]: {e}"

    unfixed = [r for r in all_reports if not r.get("fix_timestamp")]
    fixed_cnt = len(all_reports) - len(unfixed)
    lines = [
        "🚨 [크레딧 0원 · mathedu 홈페이지 오류신고 & 시트(gid=838754808) 실시간 관제 현황]",
        f"• 연동 시트(reports 탭): 누적 {len(all_reports)}건 (✅ 수리·홈페이지 반영 완료 {fixed_cnt}건 / ⏳ 미처리 {len(unfixed)}건)",
        "• 적용 페이지: index.html · video_board.html · mathlab.html · video_studio.html · dashboard.html · create.html · game.html · board/*.html(212개) 전 페이지",
    ]
    if not unfixed:
        lines.append("• 현재 미처리된 오류 신고가 **0건**입니다! (최근 신고까지 전량 수리·반영 완료)")
        recent = all_reports[-3:]
        if recent:
            lines.append("• 최근 수리 완료 내역:")
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
    print("[ANTIGRAVITY_WATCHER_ONLINE] mathedu 실시간 오류 신고 감시 데몬 가동 중 (60초 주기)", flush=True)
    while True:
        try:
            poll_and_notify_error_reports_once(send_telegram=True)
        except Exception:
            pass
        time.sleep(60)


if __name__ == "__main__":
    main()
