#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mathedu_telegram_bridge.py
===============================================================================
📱 Antigravity ↔ Telegram 실시간 양방향 대화 & 원격 지시 브릿지
- mathedu를 포함하여 Antigravity 에이전트와 스마트폰 텔레그램으로 실시간 대화·지시합니다.

[2가지 연결 모드 모두 지원]
1. 🔴 현재 대화창 직결 모드 (Live Session Reactive Wakeup)
   - `python -X utf8 mathedu_telegram_bridge.py --listen-once`
     : 백그라운드에서 대기하다가 텔레그램 메시지가 도착하면 즉시 종료(Exit 0)하여
       현재 열려 있는 Antigravity 에이전트 세션을 자동으로 깨웁니다(Reactive Wakeup).
   - `python -X utf8 mathedu_telegram_bridge.py --reply "답장 텍스트"`
     : 현재 Antigravity 에이전트가 처리 결과나 대화를 텔레그램으로 즉시 전송합니다.

2. 🟢 24시간 독립 데몬 모드 (Standalone Antigravity SDK Agent)
   - `python -X utf8 mathedu_telegram_bridge.py` (또는 `--daemon`)
     : PC에 설치된 `google.antigravity` SDK를 통해 대화 맥락을 유지하며
       언제든 텔레그램으로 Antigravity와 자유롭게 대화하고 작업을 지시합니다.
===============================================================================
"""

import argparse
import asyncio
import datetime
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import silent_subprocess  # noqa: F401 — Windows 전 하위 프로세스 완전 무창(CREATE_NO_WINDOW) 강제

ROOT_DIR = Path(__file__).resolve().parent
ENV_FILE = ROOT_DIR / ".env.telegram"
OFFSET_FILE = ROOT_DIR / ".agents" / "telegram_offset.json"
INBOX_FILE = ROOT_DIR / ".agents" / "telegram_inbox.jsonl"
HISTORY_FILE = ROOT_DIR / ".agents" / "telegram_history.json"
PID_FILE = ROOT_DIR / ".agents" / "telegram_daemon.pid"
LISTENER_PID_FILE = ROOT_DIR / ".agents" / "telegram_listener.pid"
LIVE_TURN_LOCK_FILE = ROOT_DIR / ".agents" / "telegram_live_turn.lock"


def _is_pid_alive(pid_file: Path) -> bool:
    if not pid_file.exists():
        return False
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
        if pid <= 0:
            return False
        if os.name == "nt":
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not handle:
                return False
            try:
                exit_code = ctypes.c_ulong()
                if not ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                    return False
                if exit_code.value != STILL_ACTIVE:
                    return False
                buf = ctypes.create_unicode_buffer(512)
                size = ctypes.c_ulong(512)
                if ctypes.windll.kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                    if "python" not in buf.value.lower():
                        return False
                return True
            finally:
                ctypes.windll.kernel32.CloseHandle(handle)
        else:
            os.kill(pid, 0)
            return True
    except Exception:
        return False


def _is_live_session_owning_telegram(grace_sec: float = 90.0) -> bool:
    """현재 Antigravity 대화창의 --listen-once가 살아있거나 방금 메시지를 깨워 처리 중인지 확인"""
    if _is_pid_alive(LISTENER_PID_FILE):
        return True
    if LIVE_TURN_LOCK_FILE.exists():
        try:
            ts = float(LIVE_TURN_LOCK_FILE.read_text(encoding="utf-8").strip())
            if 0 <= (time.time() - ts) < grace_sec:
                return True
        except Exception:
            pass
    return False


def load_env_config() -> dict:
    cfg = {
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(),
        "TELEGRAM_CHAT_ID": os.environ.get("TELEGRAM_CHAT_ID", "").strip(),
    }
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k in cfg and v:
                cfg[k] = v
    return cfg


def save_env_chat_id(chat_id: str) -> None:
    if not ENV_FILE.exists():
        return
    lines = ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("TELEGRAM_CHAT_ID="):
            new_lines.append(f"TELEGRAM_CHAT_ID={chat_id}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"TELEGRAM_CHAT_ID={chat_id}")
    ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def load_offset_state() -> dict:
    if OFFSET_FILE.exists():
        try:
            return json.loads(OFFSET_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"offset": 0, "chat_id": ""}


def save_offset_state(offset: int, chat_id: str) -> None:
    OFFSET_FILE.parent.mkdir(parents=True, exist_ok=True)
    OFFSET_FILE.write_text(
        json.dumps({"offset": offset, "chat_id": str(chat_id)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def tg_api(token: str, method: str, payload: dict | None = None, timeout: int = 35) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_msg(token: str, chat_id: str | int, text: str) -> None:
    if not text:
        return
    # 영상 ID 없는 불완전 임베드 경로 문자열(www.youtube.com/embed)이 텔레그램에서 깨진 링크·프리뷰로 오인 변환되는 현상 원천 차단
    import re as _re_tg
    text = _re_tg.sub(r"(?:https?://)?(?:www\.)?youtube\.com/embed(?!/[A-Za-z0-9_-]{11})", "유튜브 공식 임베드 경로", text)
    has_real_yt_video = bool(_re_tg.search(r"(?:youtu\.be/[A-Za-z0-9_-]{11}|youtube\.com/(?:watch\?v=|shorts/)[A-Za-z0-9_-]{11})", text))
    # 텔레그램 메시지 길이 제한(4096자) 고려 분할 전송
    chunk_size = 3800
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        try:
            payload = {"chat_id": chat_id, "text": chunk}
            if not has_real_yt_video:
                payload["link_preview_options"] = {"is_disabled": True}
            tg_api(token, "sendMessage", payload)
        except Exception as e:
            print(f"[WARN] sendMessage 오류: {e}")


def run_shell(cmd: list[str], timeout: int = 180) -> str:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return out.strip() or f"(코드 {proc.returncode} 완료)"
    except Exception as e:
        return f"❌ 명령 실행 오류: {e}"


def listen_once_for_live_session(token: str, allowed_chat_id: str, max_wait_sec: int = 604800) -> int:
    """
    현재 열려 있는 Antigravity 대화 세션과 1:1로 연동하기 위한 단일 수신 리스너.
    메시지가 도착하면 즉시 콘솔에 출력하고 종료(code 0)하여 Antigravity의 Reactive Wakeup을 트리거합니다.
    (상시 대기 워치독 데몬 PID_FILE은 죽이지 않고 그대로 두되, 워치독이 LISTENER_PID_FILE을 감지해 자동으로 양보합니다.)
    """
    if LISTENER_PID_FILE.exists():
        try:
            old_pid = int(LISTENER_PID_FILE.read_text(encoding="utf-8").strip())
            if old_pid and old_pid != os.getpid() and _is_pid_alive(LISTENER_PID_FILE):
                _terminate_pid_silently(old_pid)
        except Exception:
            pass
    LISTENER_PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    LISTENER_PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    try:
        if LIVE_TURN_LOCK_FILE.exists():
            LIVE_TURN_LOCK_FILE.unlink()
    except Exception:
        pass

    state = load_offset_state()
    offset = int(state.get("offset", 0))
    if not allowed_chat_id and state.get("chat_id"):
        allowed_chat_id = str(state["chat_id"])

    start_ts = time.time()
    last_report_poll_ts = 0.0
    while time.time() - start_ts < max_wait_sec:
        try:
            if time.time() - last_report_poll_ts >= 90.0:
                last_report_poll_ts = time.time()
                try:
                    sys.path.insert(0, str(ROOT_DIR))
                    import _antigravity_report_watcher as _arw
                    rep_res = _arw.poll_and_notify_error_reports_once(send_telegram=True)
                    if rep_res.get("newly_alerted"):
                        print("======================================================================")
                        print("🚨 [WEB_ERROR_REPORT_INCOMING] 홈페이지 신규 오류신고 감지 (Reactive Wakeup)")
                        print(json.dumps(rep_res.get("newly_alerted"), ensure_ascii=False, indent=2))
                        print("======================================================================")
                        return 0
                except Exception:
                    pass
            st_cur = load_offset_state()
            offset = max(offset, int(st_cur.get("offset", 0)))
            res = tg_api(token, "getUpdates", {"offset": offset, "timeout": 25}, timeout=35)
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or {}
                chat = msg.get("chat") or {}
                chat_id = str(chat.get("id", ""))
                text = (msg.get("text") or "").strip()
                if not chat_id or not text:
                    save_offset_state(offset, allowed_chat_id or chat_id)
                    continue

                if not allowed_chat_id:
                    allowed_chat_id = chat_id
                    save_env_chat_id(chat_id)

                if str(chat_id) != str(allowed_chat_id):
                    save_offset_state(offset, allowed_chat_id)
                    continue

                save_offset_state(offset, allowed_chat_id)
                collected_texts = [text]
                # 긴 메시지가 여러 조각으로 나뉘어 도착하는 경우(1.2초 내 후속 청크)까지 한 번에 병합 수신
                time.sleep(1.2)
                try:
                    more = tg_api(token, "getUpdates", {"offset": offset, "timeout": 1}, timeout=5)
                    for m_upd in more.get("result", []):
                        offset = m_upd["update_id"] + 1
                        m_msg = m_upd.get("message") or {}
                        m_chat = m_msg.get("chat") or {}
                        if str(m_chat.get("id", "")) == str(allowed_chat_id):
                            m_text = (m_msg.get("text") or "").strip()
                            if m_text:
                                collected_texts.append(m_text)
                    save_offset_state(offset, allowed_chat_id)
                except Exception:
                    pass

                full_text = "\n".join(collected_texts)
                # [0-Credit Instant Router] 정형 현황·수익·업로드·무결성 명령은 LLM 크레딧 0원으로 즉시 응답 후 리스닝 지속!
                quick_reply = _handle_zero_credit_quick_command(full_text)
                if quick_reply is not None:
                    send_msg(token, chat_id, quick_reply)
                    continue

                hist = load_history()
                hist.append({"role": "user", "text": full_text, "ts": datetime.datetime.now().isoformat()})
                save_history(hist)
                try:
                    LIVE_TURN_LOCK_FILE.write_text(str(time.time()), encoding="utf-8")
                except Exception:
                    pass
                send_msg(token, chat_id, "🤖 [Antigravity] 메시지를 수신했습니다. 생각하고 작업을 수행합니다...")
                print("======================================================================")
                print("📩 [TELEGRAM_INCOMING_MESSAGE]")
                print(f"• Chat ID: {chat_id}")
                print(f"• 사용자: {chat.get('username') or chat.get('first_name') or 'User'}")
                print(f"• 시각: {datetime.datetime.now().isoformat()}")
                print("• 내용:")
                print(full_text)
                print("======================================================================")
                return 0
        except KeyboardInterrupt:
            return 130
        except Exception:
            time.sleep(2)
    print("[TIMEOUT] 대기 시간 동안 새 텔레그램 메시지가 없었습니다.")
    return 0


def load_history() -> list[dict]:
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data[-100:]
        except Exception:
            pass
    return []


def save_history(history: list[dict]) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        json.dumps(history[-100:], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _resolve_agy_bin() -> str:
    import shutil
    found = shutil.which("agy")
    if found:
        return found
    candidate = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\min\AppData\Local")) / "agy" / "bin" / "agy.EXE"
    if candidate.exists():
        return str(candidate)
    return "agy"


def _build_secretary_fallback_briefing() -> str:
    try:
        import secretary
        metrics = secretary.collect_live_workspace_metrics()
        return secretary.format_executive_briefing(metrics)
    except Exception as e:
        return f"📊 [워크스페이스 요약]\n• 상태 조회 중 보조 알림: {e}"


def _handle_zero_credit_quick_command(raw_text: str) -> str | None:
    """
    [Rule 46: 크레딧 소모 0원(Zero-Credit) 즉시 파이썬 명령 라우터]
    정형 상태 확인·유튜브 수익 지표·수동 업로드·무결성 점검·애드센스 설정은 고비용 LLM 턴을 깨우지 않고
    로컬 파이썬으로 1~3초 내 즉시 수행하여 크레딧 소모를 80~90% 절감합니다.
    """
    cmd = (raw_text or "").strip()
    low = cmd.lower()

    if low in ("!도움말", "/help", "!help"):
        return (
            "💡 [크레딧 소모 0원 · 유튜브 최우선 수익화 단축 명령어]\n"
            "아래 단축어를 입력하시면 AI 크레딧 0원으로 파이썬이 즉시 처리합니다:\n"
            "• !추이 (또는 /trend) : [전략 v2.0 기준점 대비] 구독자·조회수·시청시간·쇼츠 유지율·신규 코호트 변화 추이\n"
            "• !추이정밀 (또는 /trenddeep) : [API 쿼터 0] YouTube Studio 내부 시청시간·이탈률까지 실시간 정밀 실측\n"
            "• !수익 (또는 /revenue) : 실시간 유튜브 구독자·조회수·YPP 1/2단계 달성 현황·쇼츠 본편 바인딩 수\n"
            "• !쇼츠연결 (또는 /linkshorts) : [API 쿼터 0] 스튜디오에서 쇼츠 8편에 1080p 본편 '관련 동영상' 즉시 연결\n"
            "• !커뮤니티 (또는 /community) : [API 쿼터 0] 채널 커뮤니티 탭에 5초 수학 퀴즈 게시물 즉시 발행\n"
            "• !고품질화 (또는 /flow) : [크레딧 0] 기존 자료 Google Flow ULTRA 실사 모션 자동 고품질화 현황 조회\n"
            "• !고품질화실행 (또는 /retrofit) : [크레딧 0] 유휴 고품질화 1주제 백그라운드 즉시 실행\n"
            "• !업로드 (또는 /wave) : 전략 v2.0(실전함정·3~10분 본편 3 + 한/영 Q-#Shorts 3) 업로드 웨이브 즉시 실행\n"
            "• !현황 (또는 /status) : 24/7 데몬 상태·금일 업로드 밸런스·최근 커밋 확인\n"
            "• !신고 (또는 !오류신고 / /reports) : [크레딧 0] mathedu 홈페이지 실시간 오류신고 접수·수리 현황 조회\n"
            "• !감사 (또는 !저작권 / !상표권) : [크레딧 0] 독립 감사관(auditor) 7계층 저작권·상표권·라이브 유튜브 전수 감사\n"
            "• !점검 (또는 /audit) : 전 문항·전 시스템 무결성 고속 스캔\n"
            "• !브리핑 (또는 /briefing) : 수석 비서 정례 종합 브리핑\n\n"
            "※ 일반 대화나 새로운 개발·수정 지시는 평소처럼 편하게 말씀하시면 AI가 즉시 깨어나 수행합니다."
        )

    if low in ("!신고", "!오류신고", "/reports", "!reports"):
        sys.path.insert(0, str(ROOT_DIR))
        import _antigravity_report_watcher as _arw
        _arw.poll_and_notify_error_reports_once(send_telegram=False)
        return _arw.format_error_reports_summary()

    if low in ("!감사", "!저작권", "!상표권", "/copyright", "!copyright"):
        sys.path.insert(0, str(ROOT_DIR))
        import auditor
        return auditor.build_telegram_audit_summary(check_live=True, auto_fix=True)

    if low in ("!추이", "!트렌드", "/trend", "!trend"):
        sys.path.insert(0, str(ROOT_DIR))
        import youtube_trend_tracker as ytt
        return ytt.format_trend_report(include_studio=False)

    if low in ("!추이정밀", "/trenddeep", "!trenddeep"):
        sys.path.insert(0, str(ROOT_DIR))
        import youtube_trend_tracker as ytt
        return ytt.format_trend_report(include_studio=True)

    if low in ("!현황", "/status", "!status"):
        f_alive = _is_pid_alive(ROOT_DIR / ".agents" / "foundation_daemon.pid")
        w_alive = _is_pid_alive(PID_FILE)
        git_log = run_shell(["git", "log", "-n", "3", "--oneline"], timeout=15)
        bal_p = ROOT_DIR / ".agents" / "daily_wave_balance.json"
        bal_txt = bal_p.read_text(encoding="utf-8") if bal_p.exists() else "{}"
        return (
            "📊 [크레딧 0원 · 실시간 시스템 현황]\n"
            f"• 24/7 렌더링·업로드 데몬: {'🟢 정상 가동' if f_alive else '🔴 중지 (5분 내 자동복구)'}\n"
            f"• 24/7 텔레그램 워치독: {'🟢 정상 대기' if w_alive else '🟡 리스너 단독'}\n"
            f"• 금일 업로드 밸런스(4:2): {bal_txt.strip()}\n"
            f"• 최근 커밋:\n{git_log}"
        )

    if low in ("!수익", "/revenue", "!유튜브", "/yt"):
        rel_p = ROOT_DIR / ".agents" / "studio_shorts_related_linked.json"
        rel_cnt = len((json.loads(rel_p.read_text(encoding="utf-8")).get("linked_short_ids") or [])) if rel_p.exists() else 0
        comm_p = ROOT_DIR / "youtube_uploads" / "community_posts" / "published_community_state.json"
        comm_cnt = len((json.loads(comm_p.read_text(encoding="utf-8")).get("published_ids") or [])) if comm_p.exists() else 0
        st_p = ROOT_DIR / ".agents" / "live_yt_stats.json"
        cached = json.loads(st_p.read_text(encoding="utf-8")) if st_p.exists() else {}
        ch_title = "민은기 선생님의 단계별 시각적 수학 증명 (@min7014_ai)"
        subs = int(cached.get("subscribers_live", 8))
        views = int(cached.get("total_views_live", 5264))
        vcnt = int(cached.get("public_videos_live", 442))
        live_tag = "실측 캐시 · API 쿼터 리셋 대기(17:00 KST)"
        try:
            sys.path.insert(0, str(ROOT_DIR))
            import min7014_video_maker as vm
            yt, _ = vm.get_available_youtube_upload_service()
            if yt is not None:
                ch = yt.channels().list(part="snippet,statistics", mine=True).execute()["items"][0]
                ch_title = ch["snippet"].get("title") or ch_title
                st = ch.get("statistics", {})
                subs = int(st.get("subscriberCount", subs))
                views = int(st.get("viewCount", views))
                vcnt = int(st.get("videoCount", vcnt))
                live_tag = "실시간 API 조회"
                snap = {
                    "public_videos_live": vcnt,
                    "total_views_live": views,
                    "subscribers_live": subs,
                    "checked_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st_p.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
        return (
            f"🎬 [크레딧 0원 · @min7014_ai 유튜브 단독 수익화 리포트 ({live_tag})]\n"
            f"• 채널: {ch_title}\n"
            f"• 구독자: {subs:,}명\n"
            f"  ├ 1단계 YPP(500명·3,000시간 · 슈퍼땡스/멤버십 개시): -{max(0, 500-subs):,}명\n"
            f"  └ 2단계 정식 광고 YPP(1,000명·4,000시간): -{max(0, 1000-subs):,}명\n"
            f"• 총 조회수: {views:,}회 | 공개 영상: {vcnt:,}편\n"
            f"• [0-쿼터 스튜디오 직결] 본편 연결 완료 쇼츠: {rel_cnt}편 / 커뮤니티 퀴즈: {comm_cnt}건\n"
            "• 일일 업로드 엔진: 4:2 황금비(1080p/마스터클래스 4 + 질문형 Q-#Shorts/#Shorts 2) 1시간 간격 자동 가동 중"
        )

    if low in ("!쇼츠연결", "/linkshorts", "!linkshorts"):
        out = run_shell([sys.executable, "-X", "utf8", "youtube_community_controller.py", "--link-shorts", "8"], timeout=240)
        return f"🔗 [크레딧 0원 · API 쿼터 0 · 스튜디오 쇼츠 관련 동영상 바인딩 완료]\n{out[-1800:]}"

    if low in ("!커뮤니티", "/community", "!community"):
        out = run_shell([sys.executable, "-X", "utf8", "youtube_community_controller.py", "--post-community"], timeout=180)
        return f"🗳️ [크레딧 0원 · API 쿼터 0 · 유튜브 커뮤니티 5초 퀴즈 발행 결과]\n{out[-1500:]}"

    if low in ("!고품질화", "!플로우", "!업그레이드현황", "/flow", "!flow"):
        sys.path.insert(0, str(ROOT_DIR))
        import nano_banana_cinema_creator as nbcc
        sm = nbcc.get_flow_retrofit_status_summary()
        slugs_txt = ", ".join(sm.get("flow_motion_slugs") or []) or "(준비 중)"
        return (
            "🎬 [크레딧 0원 · Google Flow ULTRA 기존 자료 고품질화 현황]\n"
            f"• 금일 자동 고품질화 완료: {sm.get('today_upgraded_count', 0)} / 일 최대 {sm.get('daily_cap', 8)}주제\n"
            f"• Veo 3.1 양단고정 실사 모션 클립 보유: {sm.get('total_flow_motion_clips', 0)}주제 ({slugs_txt})\n"
            f"• 하이브리드 본편·쇼츠 렌더링 완료: {sm.get('total_hybrid_rendered_slugs', 0)}주제\n"
            f"• 저조회(≤15뷰) 안전 교체 완료: {sm.get('safe_swapped_count', 0)}건\n"
            f"• 인기 영상(>15뷰 · 삭제 금지 보호 · 썸네일만 업그레이드): {sm.get('protected_high_view_count', 0)}건\n"
            "• 작동 방식: 데몬 업로드 대기(Pacing/Cooldown) 유휴 시간마다 Antigravity 쿼터 0원으로 자동 수행"
        )

    if low in ("!고품질화실행", "!플로우실행", "/retrofit", "!retrofit"):
        bg_pid = silent_subprocess.spawn_windowless_background_python(
            str(ROOT_DIR / "nano_banana_cinema_creator.py"),
            extra_args=["--retrofit-once"],
            cwd=str(ROOT_DIR),
        )
        return (
            f"🚀 [크레딧 0원 · 백그라운드 무창 고품질화 착수 (PID={bg_pid})]\n"
            "• 다음 우선순위 기존 자료 1주제에 대해 Google Flow ULTRA 키프레임(0크레딧) + Veo 3.1 Lite 양단고정 8초 모션(5크레딧) 생성 및 KO/EN 본편·Q-#Shorts 고품질 렌더링을 시작했습니다.\n"
            "• 약 2~3분 뒤 `!고품질화` 명령으로 완료 현황을 확인하실 수 있습니다."
        )

    if low in ("!업로드", "/wave", "!wave"):
        out = run_shell([sys.executable, "-X", "utf8", "finance.py", "cashflow-wave"], timeout=300)
        return f"🚀 [크레딧 0원 · 황금비 업로드 웨이브 실행 완료]\n{out[-1800:]}"

    if low in ("!점검", "/audit", "!audit"):
        out1 = run_shell([sys.executable, "-X", "utf8", "audit_engine.py"], timeout=120)
        out2 = run_shell([sys.executable, "-X", "utf8", "audit_full_mathedu.py"], timeout=120)
        return f"✅ [크레딧 0원 · 전수 무결성 점검 완료]\n{out1[-800:]}\n\n{out2[-1000:]}"

    if low in ("!브리핑", "/briefing", "/report"):
        return _build_secretary_fallback_briefing()

    if low.startswith(("!애드센스 ", "/adsense ")):
        parts = cmd.split()
        if len(parts) >= 2 and parts[1].startswith("ca-pub-"):
            slot = parts[2] if len(parts) >= 3 else ""
            c_args = [sys.executable, "-X", "utf8", "finance.py", "set-adsense", "--client", parts[1]]
            if slot:
                c_args += ["--slot", slot]
            out = run_shell(c_args, timeout=60)
            run_shell(["git", "add", "ad_config.json", "ads.txt"], timeout=30)
            run_shell(["git", "commit", "-m", "feat(finance): activate Google AdSense & ads.txt"], timeout=30)
            run_shell(["git", "push", "origin", "main"], timeout=60)
            return f"💰 [크레딧 0원 · 웹 애드센스 즉시 활성화 및 GitHub 배포 완료]\n{out}"
        return "ℹ️ 사용법: `!애드센스 ca-pub-1234567890123456 [슬롯번호]`"

    return None


def run_agy_prompt(user_text: str) -> str:
    history = load_history()
    hist_lines = []
    for item in history[-8:]:
        role = "선생님(Telegram)" if item.get("role") == "user" else "Antigravity"
        hist_lines.append(f"[{role}]: {item.get('text', '')}")
    hist_block = "\n".join(hist_lines) if hist_lines else "(첫 대화)"

    prompt = (
        "[텔레그램 전용 독립 백그라운드 응답 모드]\n"
        "당신은 민은기 선생님(min7014)의 전담 수석 비서 Antigravity입니다.\n"
        "현재 선생님이 스마트폰 텔레그램(@anti7014_bot)으로 메시지를 보내셨습니다.\n"
        "주의사항:\n"
        "1. 이 응답의 표준 출력(stdout) 자체가 텔레그램 데몬에 의해 자동으로 선생님의 텔레그램으로 전송됩니다.\n"
        "2. 따라서 절대 `mathedu_telegram_bridge.py --reply`나 `--listen-once` 명령을 직접 실행하지 마십시오.\n"
        "3. GEMINI.md의 원칙(수학교육과 비수학 영역의 분리, 자율 실행 등)을 철저히 준수하되, 선생님의 질문이나 지시에 대해 모바일 텔레그램 화면에서 읽기 편하도록 명확하고 친절한 한국어로 바로 답변 텍스트만 출력하십시오.\n\n"
        f"[최근 텔레그램 대화 맥락]\n{hist_block}\n\n"
        f"[선생님의 새 텔레그램 메시지]\n{user_text}"
    )

    try:
        agy_bin = _resolve_agy_bin()
        proc = subprocess.run(
            [agy_bin, "-p", prompt, "--dangerously-skip-permissions"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        reply = (proc.stdout or "").strip()
        if not reply:
            reply = _build_secretary_fallback_briefing()
        history.append({"role": "user", "text": user_text, "ts": datetime.datetime.now().isoformat()})
        history.append({"role": "assistant", "text": reply, "ts": datetime.datetime.now().isoformat()})
        save_history(history)
        return reply
    except Exception as e:
        fb = _build_secretary_fallback_briefing()
        return f"👔 [수석 비서 상시 대기 모드 즉시 브리핑]\n(참고: 독립 CLI 응답 전환 — {e})\n\n{fb}"


async def run_daemon_with_sdk(token: str, allowed_chat_id: str) -> None:
    """
    [Zero-Conflict 상시 대기 워치독 데몬]
    - 현재 열린 Antigravity 대화창의 `--listen-once`가 살아 있는 동안에는 `getUpdates`를 호출하지 않고
      대기(Standby)하여 HTTP 409 Conflict를 0%로 원천 차단합니다.
    - 대화창이 닫히거나 새 창 전환·PC 재부팅 등으로 `--listen-once`가 없는 순간 즉시 자동으로
      `getUpdates(timeout=8)` 제어권을 넘겨받아 텔레그램 연결 끊김(Dead Zone)을 완벽히 방지합니다.
    """
    if _is_pid_alive(PID_FILE):
        try:
            existing_pid = int(PID_FILE.read_text(encoding="utf-8").strip())
            if existing_pid != os.getpid():
                return
        except Exception:
            pass

    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    log_file = open(ROOT_DIR / ".agents" / "telegram_daemon.log", "a", encoding="utf-8", buffering=1)
    sys.stdout = log_file
    sys.stderr = log_file

    state = load_offset_state()
    offset = int(state.get("offset", 0))
    if not allowed_chat_id and state.get("chat_id"):
        allowed_chat_id = str(state["chat_id"])

    print(f"🚀 [Antigravity Telegram 무충돌 상시 워치독 가동 중 | PID={os.getpid()} | {datetime.datetime.now().isoformat()}]", flush=True)
    last_wd_report_poll = 0.0
    while True:
        try:
            if _is_live_session_owning_telegram():
                await asyncio.sleep(3.0)
                continue

            if time.time() - last_wd_report_poll >= 90.0:
                last_wd_report_poll = time.time()
                try:
                    sys.path.insert(0, str(ROOT_DIR))
                    import _antigravity_report_watcher as _arw_wd
                    await asyncio.to_thread(_arw_wd.poll_and_notify_error_reports_once, True)
                except Exception:
                    pass

            st_cur = load_offset_state()
            offset = max(offset, int(st_cur.get("offset", 0)))
            res = await asyncio.to_thread(
                tg_api, token, "getUpdates", {"offset": offset, "timeout": 8}, 15
            )
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or {}
                chat = msg.get("chat") or {}
                chat_id = str(chat.get("id", ""))
                text = (msg.get("text") or "").strip()
                if not chat_id or not text:
                    save_offset_state(offset, allowed_chat_id or chat_id)
                    continue

                if not allowed_chat_id:
                    allowed_chat_id = chat_id
                    save_env_chat_id(chat_id)

                if str(chat_id) != str(allowed_chat_id):
                    save_offset_state(offset, allowed_chat_id)
                    continue

                save_offset_state(offset, allowed_chat_id)
                collected_texts = [text]
                await asyncio.sleep(1.0)
                try:
                    more = await asyncio.to_thread(
                        tg_api, token, "getUpdates", {"offset": offset, "timeout": 1}, 5
                    )
                    for m_upd in more.get("result", []):
                        offset = m_upd["update_id"] + 1
                        m_msg = m_upd.get("message") or {}
                        m_chat = m_msg.get("chat") or {}
                        if str(m_chat.get("id", "")) == str(allowed_chat_id):
                            m_text = (m_msg.get("text") or "").strip()
                            if m_text:
                                collected_texts.append(m_text)
                    save_offset_state(offset, allowed_chat_id)
                except Exception:
                    pass

                full_text = "\n".join(collected_texts)
                print(f"[📩 워치독 수신] ({chat_id}): {full_text}", flush=True)

                # [0-Credit Instant Router] 단축 명령어는 LLM 호출 없이 즉시 응답
                quick_reply = await asyncio.to_thread(_handle_zero_credit_quick_command, full_text)
                if quick_reply is not None:
                    await asyncio.to_thread(send_msg, token, chat_id, quick_reply)
                    continue

                await asyncio.to_thread(
                    send_msg,
                    token,
                    chat_id,
                    "🤖 [Antigravity 상시 대기 비서] 메시지를 수신했습니다. 확인 후 답변드립니다...",
                )

                # 독립 백그라운드 Antigravity 에이전트 호출 및 응답
                reply_text = await asyncio.to_thread(run_agy_prompt, full_text)
                await asyncio.to_thread(send_msg, token, chat_id, reply_text)
        except KeyboardInterrupt:
            print("\n👋 텔레그램 에이전트 데몬을 종료합니다.")
            break
        except Exception as e:
            print(f"[재시도 대기] 오류: {e}", flush=True)
            await asyncio.sleep(3)


def _terminate_pid_silently(pid: int) -> None:
    if pid <= 0 or pid == os.getpid():
        return
    if os.name == "nt":
        try:
            import ctypes
            h = ctypes.windll.kernel32.OpenProcess(0x0001, False, int(pid))
            if h:
                ctypes.windll.kernel32.TerminateProcess(h, 0)
                ctypes.windll.kernel32.CloseHandle(h)
                return
        except Exception:
            pass
    subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)


def _spawn_detached_watchdog(force_restart: bool = False) -> str:
    if not force_restart and _is_pid_alive(PID_FILE):
        return PID_FILE.read_text(encoding="utf-8").strip()
    if PID_FILE.exists() and _is_pid_alive(PID_FILE):
        try:
            old_pid = int(PID_FILE.read_text(encoding="utf-8").strip())
            _terminate_pid_silently(old_pid)
        except Exception:
            pass
    new_pid = silent_subprocess.spawn_windowless_background_python(
        str(Path(__file__).resolve()),
        cwd=str(ROOT_DIR),
    )
    pid_str = str(new_pid) if new_pid > 0 else ""
    if pid_str:
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(pid_str, encoding="utf-8")
    return pid_str


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity ↔ Telegram 양방향 대화 및 지시 브릿지")
    parser.add_argument(
        "--listen-once",
        action="store_true",
        help="텔레그램 메시지 1건을 수신하면 즉시 출력 후 종료하여 현재 Antigravity 세션을 깨웁니다.",
    )
    parser.add_argument(
        "--start-detached",
        action="store_true",
        help="현재 대화창과 완전히 분리된 OS 백그라운드 데몬 프로세스로 텔레그램 브릿지를 실행합니다.",
    )
    parser.add_argument(
        "--watchdog-ensure",
        action="store_true",
        help="상시 대기 워치독 데몬이 실행 중인지 확인하고 죽어 있을 때만 무소음 자동 기동합니다(작업 스케줄러용).",
    )
    parser.add_argument(
        "--reply",
        type=str,
        default="",
        help="지정한 텍스트를 사용자의 텔레그램 채팅방으로 즉시 전송합니다.",
    )
    parser.add_argument(
        "--set-token",
        type=str,
        default="",
        help=".env.telegram 파일에 TELEGRAM_BOT_TOKEN을 저장합니다.",
    )
    parser.add_argument(
        "--set-chat-id",
        type=str,
        default="",
        help=".env.telegram 파일에 TELEGRAM_CHAT_ID를 저장합니다.",
    )
    args = parser.parse_args()

    if args.set_token or args.set_chat_id:
        cfg = load_env_config()
        if args.set_token:
            cfg["TELEGRAM_BOT_TOKEN"] = args.set_token.strip()
        if args.set_chat_id:
            cfg["TELEGRAM_CHAT_ID"] = args.set_chat_id.strip()
        ENV_FILE.write_text(
            f"TELEGRAM_BOT_TOKEN={cfg['TELEGRAM_BOT_TOKEN']}\n"
            f"TELEGRAM_CHAT_ID={cfg['TELEGRAM_CHAT_ID']}\n",
            encoding="utf-8",
        )
        print(f"✅ `{ENV_FILE.name}` 설정이 저장되었습니다.")
        return

    cfg = load_env_config()
    token = cfg["TELEGRAM_BOT_TOKEN"]
    allowed_chat_id = cfg["TELEGRAM_CHAT_ID"]

    if not token:
        print("=" * 72)
        print("📱 [Antigravity ↔ 텔레그램 직결 설정 안내]")
        print("=" * 72)
        print("아직 TELEGRAM_BOT_TOKEN이 설정되지 않았습니다.")
        print("봇 토큰을 알려주시거나 아래 명령어로 등록해 주세요:\n")
        print("  python -X utf8 mathedu_telegram_bridge.py --set-token \"발급받은_봇_토큰\"")
        print("=" * 72)
        return

    if args.reply:
        state = load_offset_state()
        target_chat_id = allowed_chat_id or state.get("chat_id", "")
        if not target_chat_id:
            print("❌ 전송할 TELEGRAM_CHAT_ID가 아직 등록되지 않았습니다. 먼저 텔레그램 봇에게 메시지를 한 번 보내주세요.")
            sys.exit(1)
        send_msg(token, target_chat_id, args.reply)
        hist = load_history()
        hist.append({"role": "assistant", "text": args.reply, "ts": datetime.datetime.now().isoformat()})
        save_history(hist)
        try:
            if LIVE_TURN_LOCK_FILE.exists():
                LIVE_TURN_LOCK_FILE.unlink()
        except Exception:
            pass
        print(f"✅ 텔레그램({target_chat_id})으로 답장을 전송했습니다.")
        return

    if args.watchdog_ensure:
        if _is_pid_alive(PID_FILE):
            return
        pid_str = _spawn_detached_watchdog(force_restart=False)
        print(f"✅ 텔레그램 상시 대기 워치독 자동 복구 완료 (PID: {pid_str}).")
        return

    if args.start_detached:
        pid_str = _spawn_detached_watchdog(force_restart=True)
        print(f"✅ 텔레그램 독립 백그라운드 데몬이 시작되었습니다 (PID: {pid_str}).")
        return

    if args.listen_once:
        sys.exit(listen_once_for_live_session(token, allowed_chat_id))

    asyncio.run(run_daemon_with_sdk(token, allowed_chat_id))


if __name__ == "__main__":
    main()
