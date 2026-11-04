#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baze_gateway.py — Mindlogic BAZE API Gateway Unified Client for mathedu Agents
==============================================================================
Official BAZE API Gateway integration (https://docs.factchat.kr/agent-setup/prompt.md):
  • Base URL         : https://api.baze.co/v1/gateway
  • Claude Base URL  : https://api.baze.co/v1/gateway/claude
  • Models Endpoint  : https://api.baze.co/v1/gateway/models/
  • Chat Completions : https://api.baze.co/v1/gateway/chat/completions
  • Authentication   : Authorization: Bearer <BAZE_API_KEY> (or x-api-key: <BAZE_API_KEY>)

사용법:
  python -X utf8 baze_gateway.py verify
  python -X utf8 baze_gateway.py models
  python -X utf8 baze_gateway.py test-chat
"""

import argparse
import json
import os
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BAZE_BASE_URL = "https://api.baze.co/v1/gateway"
BAZE_CLAUDE_BASE_URL = "https://api.baze.co/v1/gateway/claude"


def load_baze_api_key() -> str:
    env_key = os.environ.get("BAZE_API_KEY", "").strip()
    if env_key:
        return env_key
    key_file = ROOT_DIR / ".baze_api_key"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip().startswith("BAZE_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def ensure_baze_env_configured() -> dict:
    """
    워크스페이스 내 모든 에이전트(mathteacher, Video_Creator, gamemaker, designer, pr)와
    OpenAI / Anthropic 호환 클라이언트가 BAZE API Gateway를 기본 사용하도록 환경변수 및 .env를 설정합니다.
    """
    key = load_baze_api_key()
    if not key:
        return {}
    env_vars = {
        "BAZE_API_KEY": key,
        "OPENAI_BASE_URL": BAZE_BASE_URL,
        "OPENAI_API_KEY": key,
        "ANTHROPIC_BASE_URL": BAZE_CLAUDE_BASE_URL,
        "ANTHROPIC_AUTH_TOKEN": key,
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    env_path = ROOT_DIR / ".env"
    env_lines = [
        "# BAZE API Gateway Configuration (https://docs.factchat.kr/agent-setup/prompt.md)",
        f"BAZE_API_KEY={key}",
        f"OPENAI_BASE_URL={BAZE_BASE_URL}",
        f"OPENAI_API_KEY={key}",
        f"ANTHROPIC_BASE_URL={BAZE_CLAUDE_BASE_URL}",
        f"ANTHROPIC_AUTH_TOKEN={key}",
    ]
    env_path.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    return env_vars


def list_baze_models() -> list:
    key = load_baze_api_key()
    if not key:
        raise RuntimeError("BAZE_API_KEY not found in environment or .baze_api_key")
    req = urllib.request.Request(
        f"{BAZE_BASE_URL}/models/",
        headers={
            "Authorization": f"Bearer {key}",
            "x-api-key": key,
            "User-Agent": "Mozilla/5.0",
        },
    )
    raw = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
    data = json.loads(raw)
    return data.get("data", [])


def baze_chat_completion(
    messages: list,
    model: str = "claude-sonnet-4-6",
    fallback_models: tuple = ("claude-sonnet-5-5", "gemini-3.8-flash", "gpt-5.4"),
    max_tokens: int = 4096,
    temperature: float = 0.3,
    timeout: int = 55,
) -> str:
    """
    BAZE API Gateway (/v1/gateway/chat/completions)를 호출하며,
    지정 모델 타임아웃 또는 일시적 오류 시 fallback_models로 자동 전환합니다.
    """
    key = load_baze_api_key()
    if not key:
        raise RuntimeError("BAZE_API_KEY not configured.")

    candidates = [model] + [m for m in fallback_models if m != model]
    last_err = None
    for m_id in candidates:
        try:
            payload = {
                "model": m_id,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            req = urllib.request.Request(
                f"{BAZE_BASE_URL}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {key}",
                    "x-api-key": key,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                },
            )
            raw_resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
            resp_obj = json.loads(raw_resp)
            return resp_obj["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"All BAZE models failed: {last_err}")


def main():
    parser = argparse.ArgumentParser(description="Mindlogic BAZE API Gateway Client for mathedu")
    parser.add_argument("cmd", nargs="?", default="verify", choices=["verify", "models", "test-chat"])
    parser.add_argument("--model", default="claude-sonnet-4-6")
    args = parser.parse_args()

    ensure_baze_env_configured()
    models = list_baze_models()
    model_ids = [m.get("id") for m in models]

    if args.cmd == "models":
        for m in models:
            print(f"• {m.get('id')}")
        return

    print("=" * 84)
    print("🔌 [BAZE API Gateway — Agent Setup & Verification]")
    print("=" * 84)
    print(f" • Base URL            : {BAZE_BASE_URL}")
    print(f" • Claude Endpoint     : {BAZE_CLAUDE_BASE_URL}")
    print(f" • Workspace .env      : Configured (OPENAI_BASE_URL / ANTHROPIC_BASE_URL / BAZE_API_KEY)")
    print(f" • Available Models    : {len(model_ids)} models verified")
    print(f"   - Claude Family     : {', '.join(x for x in model_ids if 'claude' in x)[:95]}")
    print(f"   - GPT Family        : {', '.join(x for x in model_ids if x.startswith('gpt-'))[:95]}")
    print(f"   - Gemini Family     : {', '.join(x for x in model_ids if 'gemini' in x)[:95]}")
    print("=" * 84)

    if args.cmd == "test-chat":
        reply = baze_chat_completion(
            messages=[{"role": "user", "content": "피타고라스 정리의 아름다움을 한국어 한 문장으로 답해주세요."}],
            model=args.model,
            max_tokens=200,
        )
        print(f"💬 [Live Chat Completion ({args.model})]: {reply}")


if __name__ == "__main__":
    main()
