#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mathedu_telegram_bridge.py
===============================================================================
📱 mathedu 수학교육 플랫폼 전용 텔레그램 원격 지시 브릿지 (Telegram Remote Bridge)
- 외부에서 스마트폰 텔레그램으로 mathedu 홈페이지 점검·빌드·배포 및 AI 에이전트 지시를 수행합니다.
- 외부 패키지 의존성 없이 Python 표준 라이브러리(urllib)만으로 즉시 동작하며,
  `google-antigravity` Python SDK가 설치된 경우 자유로운 자연어 코딩/수학교육 지시까지 실시간 실행합니다.

[사용 방법]
1. 텔레그램 @BotFather 에서 봇 생성 후 토큰(TELEGRAM_BOT_TOKEN) 발급
2. 프로젝트 루트에 `.env.telegram` 파일 생성 (Git에는 자동 제외됨):
   TELEGRAM_BOT_TOKEN=123456789:ABCDEF...
   TELEGRAM_CHAT_ID=본인의_채팅_ID (비워두고 봇에게 첫 메시지를 보내면 콘솔에 Chat ID가 표시됨)
3. 실행:
   python -X utf8 mathedu_telegram_bridge.py
===============================================================================
"""

import asyncio
import datetime
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
ENV_FILE = ROOT_DIR / ".env.telegram"
INBOX_FILE = ROOT_DIR / ".agents" / "telegram_inbox.jsonl"


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
    if len(text) > 3900:
        text = text[:3900] + "\n...(중략)..."
    try:
        tg_api(token, "sendMessage", {"chat_id": chat_id, "text": text})
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


async def run_antigravity_agent_prompt(prompt: str) -> str:
    """
    google-antigravity Python SDK가 설치되어 있으면 에이전트를 직접 스폰하여 지시를 수행하고,
    설치되어 있지 않으면 .agents/telegram_inbox.jsonl 큐에 적재합니다.
    """
    try:
        from google.antigravity import Agent, CapabilitiesConfig, LocalAgentConfig  # type: ignore

        config = LocalAgentConfig(
            system_instructions=(
                "당신은 mathedu 수학교육 플랫폼 전담 자율 에이전트입니다. "
                "GEMINI.md 규칙을 엄수하여 사용자의 텔레그램 지시를 끝까지 수행하고 핵심 결과를 한국어로 간결하게 보고하십시오."
            ),
            capabilities=CapabilitiesConfig(),
        )
        chunks: list[str] = []
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            async for token in response:
                chunks.append(token)
        result = "".join(chunks).strip()
        return result or "✅ 에이전트 작업이 완료되었습니다."
    except ImportError:
        INBOX_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "prompt": prompt,
            "status": "queued",
        }
        with open(INBOX_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return (
            "📥 지시사항이 `.agents/telegram_inbox.jsonl` 작업 큐에 기록되었습니다!\n"
            f"• 내용: {prompt}\n\n"
            "💡 실시간 자율 에이전트 직접 실행을 원하시면 터미널에서 `pip install google-antigravity`를 설치하거나, "
            "현재 열려 있는 Antigravity 채팅창에서 바로 확인하실 수 있습니다."
        )
    except Exception as e:
        return f"⚠️ 에이전트 실행 중 예외 발생: {e}"


def handle_command(token: str, chat_id: str | int, text: str) -> None:
    cmd = text.strip()
    if cmd in ("/start", "/help"):
        help_text = (
            "🎓 [mathedu 수학교육 플랫폼 텔레그램 원격 제어 센터]\n\n"
            "사용 가능한 명령어:\n"
            "• /status : 현재 Git 상태 및 문항 현황 확인\n"
            "• /audit : 기계적 전수 검사(426개) + 종합 무결성 점검(23개 항목) 즉시 실행\n"
            "• /build : 오프라인 단독 퀴즈 패키지(212개) 재빌드\n"
            "• /deploy [메시지] : 변경사항 Git 커밋 및 main 브랜치 즉시 배포\n"
            "• 그 외 자유 메시지 입력 : Antigravity 에이전트에게 수학교육/홈페이지 개선 지시 전달"
        )
        send_msg(token, chat_id, help_text)
        return

    if cmd == "/status":
        git_st = run_shell(["git", "status", "-s"])
        git_log = run_shell(["git", "log", "-n", "3", "--oneline"])
        msg = (
            "📊 [mathedu 플랫폼 상태 보고]\n\n"
            f"• 최신 커밋:\n{git_log}\n\n"
            f"• 작업 트리 변경사항:\n{git_st if git_st else '깨끗함 (Clean)'}"
        )
        send_msg(token, chat_id, msg)
        return

    if cmd == "/audit":
        send_msg(token, chat_id, "🔍 mathedu 전체 무결성 전수 검사를 시작합니다...")
        out1 = run_shell([sys.executable, "-X", "utf8", "audit_engine.py"])
        out2 = run_shell([sys.executable, "-X", "utf8", "audit_full_mathedu.py"])
        send_msg(token, chat_id, f"✅ [전수 검사 완료]\n\n{out1}\n\n{out2[-1200:]}")
        return

    if cmd == "/build":
        send_msg(token, chat_id, "🛠️ 오프라인 단독 퀴즈 패키지 재빌드를 시작합니다...")
        out = run_shell([sys.executable, "-X", "utf8", "build_offline_quizzes.py"], timeout=300)
        send_msg(token, chat_id, f"✅ [오프라인 재빌드 완료]\n\n{out[-1500:]}")
        return

    if cmd.startswith("/deploy"):
        commit_msg = cmd[len("/deploy"):].strip() or "chore(telegram): remote update via mathedu telegram bridge"
        send_msg(token, chat_id, f"🚀 Git 커밋 및 배포를 진행합니다: {commit_msg}")
        add_out = run_shell(["git", "add", "-A"])
        commit_out = run_shell(["git", "commit", "-m", commit_msg])
        push_out = run_shell(["git", "push", "origin", "main"])
        send_msg(token, chat_id, f"✅ [배포 결과]\n{add_out}\n{commit_out}\n{push_out}")
        return

    # 자유 자연어 지시 처리
    send_msg(token, chat_id, f"🤖 지시를 접수했습니다:\n\"{cmd}\"\n처리를 시작합니다...")
    reply = asyncio.run(run_antigravity_agent_prompt(cmd))
    send_msg(token, chat_id, reply)


def main() -> None:
    cfg = load_env_config()
    token = cfg["TELEGRAM_BOT_TOKEN"]
    allowed_chat_id = cfg["TELEGRAM_CHAT_ID"]

    if not token:
        print("=" * 72)
        print("📱 [mathedu 텔레그램 원격 브릿지 설정 안내]")
        print("=" * 72)
        print("아직 TELEGRAM_BOT_TOKEN이 설정되지 않았습니다.")
        print(f"프로젝트 폴더의 `{ENV_FILE.name}` 파일에 아래 형식으로 저장해 주세요:\n")
        print("TELEGRAM_BOT_TOKEN=123456789:ABCDEF_발급받은_봇_토큰")
        print("TELEGRAM_CHAT_ID=본인의_텔레그램_Chat_ID\n")
        print("※ TELEGRAM_CHAT_ID를 모르면 비워두고 실행한 뒤 봇에게 아무 메시지나 보내면 화면에 출력됩니다.")
        print("=" * 72)
        return

    print("=" * 72)
    print("🚀 mathedu 텔레그램 원격 지시 브릿지가 시작되었습니다! (Ctrl+C로 종료)")
    if allowed_chat_id:
        print(f"🔒 허용된 관리자 Chat ID: {allowed_chat_id}")
    else:
        print("⚠️ TELEGRAM_CHAT_ID가 비어 있습니다. 봇에게 첫 메시지를 보내면 Chat ID를 안내합니다.")
    print("=" * 72)

    offset = 0
    while True:
        try:
            res = tg_api(token, "getUpdates", {"offset": offset, "timeout": 25}, timeout=35)
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or {}
                chat = msg.get("chat") or {}
                chat_id = str(chat.get("id", ""))
                text = (msg.get("text") or "").strip()
                if not chat_id or not text:
                    continue

                if not allowed_chat_id:
                    print(f"💡 감지된 첫 메시지 Chat ID: {chat_id} (사용자: {chat.get('username') or chat.get('first_name')})")
                    send_msg(
                        token,
                        chat_id,
                        f"👋 안녕하세요! 회원님의 Chat ID는 `{chat_id}` 입니다.\n"
                        f"보안을 위해 `.env.telegram` 파일에 `TELEGRAM_CHAT_ID={chat_id}`를 추가하신 뒤 사용하세요.",
                    )
                    allowed_chat_id = chat_id

                if str(chat_id) != str(allowed_chat_id):
                    print(f"⛔ 승인되지 않은 Chat ID 접근 차단: {chat_id}")
                    continue

                print(f"[📩 수신] ({chat_id}): {text}")
                handle_command(token, chat_id, text)
        except KeyboardInterrupt:
            print("\n👋 텔레그램 브릿지를 종료합니다.")
            break
        except Exception as e:
            print(f"[재시도 대기] 폴링 오류: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
