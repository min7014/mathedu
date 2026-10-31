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

ROOT_DIR = Path(__file__).resolve().parent
ENV_FILE = ROOT_DIR / ".env.telegram"
OFFSET_FILE = ROOT_DIR / ".agents" / "telegram_offset.json"
INBOX_FILE = ROOT_DIR / ".agents" / "telegram_inbox.jsonl"
HISTORY_FILE = ROOT_DIR / ".agents" / "telegram_history.json"
PID_FILE = ROOT_DIR / ".agents" / "telegram_daemon.pid"


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
    # 텔레그램 메시지 길이 제한(4096자) 고려 분할 전송
    chunk_size = 3800
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        try:
            tg_api(token, "sendMessage", {"chat_id": chat_id, "text": chunk})
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
    """
    state = load_offset_state()
    offset = int(state.get("offset", 0))
    if not allowed_chat_id and state.get("chat_id"):
        allowed_chat_id = str(state["chat_id"])

    start_ts = time.time()
    while time.time() - start_ts < max_wait_sec:
        try:
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
                hist = load_history()
                hist.append({"role": "user", "text": full_text, "ts": datetime.datetime.now().isoformat()})
                save_history(hist)
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
        except Exception as e:
            time.sleep(3)
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
        proc = subprocess.run(
            ["agy", "-p", prompt, "--dangerously-skip-permissions"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        reply = (proc.stdout or "").strip()
        if not reply:
            reply = "✅ 요청하신 작업을 완료했습니다."
        history.append({"role": "user", "text": user_text, "ts": datetime.datetime.now().isoformat()})
        history.append({"role": "assistant", "text": reply, "ts": datetime.datetime.now().isoformat()})
        save_history(history)
        return reply
    except Exception as e:
        return f"⚠️ 처리 중 오류가 발생했습니다: {e}"


async def run_daemon_with_sdk(token: str, allowed_chat_id: str) -> None:
    """
    독립 백그라운드 프로세스에서 상시 동작하며, 현재 열려 있는 대화창에 일절 로그나 툴 호출을 표시하지 않고
    텔레그램 메시지를 수신·처리·응답합니다.
    """
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    log_file = open(ROOT_DIR / ".agents" / "telegram_daemon.log", "a", encoding="utf-8", buffering=1)
    sys.stdout = log_file
    sys.stderr = log_file

    state = load_offset_state()
    offset = int(state.get("offset", 0))
    if not allowed_chat_id and state.get("chat_id"):
        allowed_chat_id = str(state["chat_id"])

    print(f"🚀 [Antigravity Telegram 독립 데몬 가동 중 | PID={os.getpid()}]", flush=True)
    while True:
        try:
            res = await asyncio.to_thread(
                tg_api, token, "getUpdates", {"offset": offset, "timeout": 25}, 35
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
                print(f"[📩 수신] ({chat_id}): {full_text}", flush=True)

                # 빠른 내장 단축 명령어 처리
                if full_text == "/status":
                    git_st = run_shell(["git", "status", "-s"])
                    git_log = run_shell(["git", "log", "-n", "3", "--oneline"])
                    await asyncio.to_thread(
                        send_msg,
                        token,
                        chat_id,
                        f"📊 [현재 워크스페이스 상태]\n• 최근 커밋:\n{git_log}\n\n• 변경사항:\n{git_st or '없음 (Clean)'}",
                    )
                    continue
                elif full_text == "/audit":
                    await asyncio.to_thread(send_msg, token, chat_id, "🔍 전체 무결성 검사를 실행합니다...")
                    out1 = run_shell([sys.executable, "-X", "utf8", "audit_engine.py"])
                    out2 = run_shell([sys.executable, "-X", "utf8", "audit_full_mathedu.py"])
                    await asyncio.to_thread(send_msg, token, chat_id, f"✅ [검사 결과]\n{out1}\n\n{out2[-1200:]}")
                    continue

                # 독립 백그라운드 Antigravity 에이전트 호출 및 응답
                reply_text = await asyncio.to_thread(run_agy_prompt, full_text)
                await asyncio.to_thread(send_msg, token, chat_id, reply_text)
        except KeyboardInterrupt:
            print("\n👋 텔레그램 에이전트 데몬을 종료합니다.")
            break
        except Exception as e:
            print(f"[재시도 대기] 오류: {e}", flush=True)
            await asyncio.sleep(4)


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
        print(f"✅ 텔레그램({target_chat_id})으로 답장을 전송했습니다.")
        return

    if args.start_detached:
        if PID_FILE.exists():
            try:
                old_pid = int(PID_FILE.read_text(encoding="utf-8").strip())
                subprocess.run(
                    ["taskkill", "/F", "/PID", str(old_pid)],
                    capture_output=True,
                )
            except Exception:
                pass
        py_exe = Path(sys.executable)
        pyw_exe = py_exe.with_name("pythonw.exe")
        runner = str(pyw_exe if pyw_exe.exists() else py_exe)
        script = str(Path(__file__).resolve())
        cmd_line = f'"{runner}" -X utf8 "{script}"'
        ps_cmd = (
            "$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create "
            f"-Arguments @{{CommandLine='{cmd_line}'; CurrentDirectory='{str(ROOT_DIR)}'}}; "
            "Write-Output $r.ProcessId"
        )
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True,
        )
        pid_str = (res.stdout or "").strip().splitlines()[-1].strip()
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(pid_str, encoding="utf-8")
        print(f"✅ 텔레그램 독립 백그라운드 데몬이 시작되었습니다 (PID: {pid_str}).")
        return

    if args.listen_once:
        sys.exit(listen_once_for_live_session(token, allowed_chat_id))

    asyncio.run(run_daemon_with_sdk(token, allowed_chat_id))


if __name__ == "__main__":
    main()
