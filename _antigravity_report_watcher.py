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

REPO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = REPO_DIR / ".agents"
PROCESSED_FILE = AGENTS_DIR / "processed_error_reports.json"
PENDING_FILE = AGENTS_DIR / "pending_error_reports.json"
LEGACY_PROCESSED_FILE = REPO_DIR / "_processed_reports.json"
API_URL_FILE = REPO_DIR / "progress-api-url.txt"
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


def poll_and_notify_error_reports_once(send_telegram: bool = True) -> dict:
    """
    Google Sheets의 오류 신고 목록을 1회 조회하여:
    - 미해결 신고를 .agents/pending_error_reports.json에 동기화하고
    - 아직 알림을 보내지 않은 신규 신고가 있으면 즉시 텔레그램 알림을 발송합니다.
    """
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        all_reports = fetch_all_reports(timeout=12)
    except Exception as e:
        return {"ok": False, "error": str(e), "total": 0, "unfixed": 0, "newly_alerted": []}

    proc = load_processed()
    processed_items = proc.setdefault("processed", [])
    alerted_keys = set(proc.setdefault("alerted_keys", []))

    unfixed_list: list[dict] = []
    newly_detected: list[dict] = []

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
            and p.get("status") in ("fixed", "resolved")
            for p in processed_items
        )
        if already_fixed:
            continue
        unfixed_list.append(r)
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
    }


def format_error_reports_summary() -> str:
    try:
        all_reports = fetch_all_reports(timeout=12)
    except Exception as e:
        return f"⚠️ [오류신고 시트 조회 실패]: {e}"

    unfixed = [r for r in all_reports if not r.get("fix_timestamp")]
    fixed_cnt = len(all_reports) - len(unfixed)
    lines = [
        "🚨 [크레딧 0원 · mathedu 홈페이지 오류신고 실시간 관제 현황]",
        f"• 누적 접수 총계: {len(all_reports)}건 (✅ 수리 완료 {fixed_cnt}건 / ⏳ 미처리 {len(unfixed)}건)",
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
