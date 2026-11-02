#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
min7014_ai_server.py
====================
video_studio.html 웹 화면에서 원클릭으로:
1) 선택한 PDF 자료(또는 미업로드 866개 자료 연속 배치)의 8개국어 설명 대본 생성
2) 한국어(_ko.mp4) & 영어(_en.mp4) 1080p Broadcast Master 영상 + 1280x720 썸네일 + SRT 자막 렌더링
3) https://www.youtube.com/@min7014_ai (UCSlqQfOEtRfJuMPyGMLgFYA) 채널로 자동 업로드 및 GitHub 반영
을 수행하는 로컬 자동화 데몬 서버 (http://127.0.0.1:8765) 입니다.
"""

import json
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
PORT = 8765

STATE = {
    "status": "idle",
    "current_slug": "",
    "mode": "",
    "logs": ["[@min7014_ai Auto-Upload Server Ready] http://127.0.0.1:8765"],
    "last_updated": time.time(),
}
STATE_LOCK = threading.Lock()


def append_log(line):
    with STATE_LOCK:
        STATE["logs"].append(line)
        if len(STATE["logs"]) > 120:
            STATE["logs"] = STATE["logs"][-120:]
        STATE["last_updated"] = time.time()


def run_pipeline_worker(cmd_args, slug_label, mode_label):
    with STATE_LOCK:
        STATE["status"] = "running"
        STATE["current_slug"] = slug_label
        STATE["mode"] = mode_label
    append_log(f"🚀 Starting {mode_label}: {' '.join(cmd_args)}")
    try:
        proc = subprocess.Popen(
            cmd_args,
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        for line in proc.stdout:
            clean = line.rstrip()
            if clean:
                append_log(clean)
        proc.wait()
        if proc.returncode == 0:
            append_log(f"✅ Completed {mode_label} ({slug_label}) successfully!")
        else:
            append_log(f"⚠️ Process exited with code {proc.returncode}")
    except Exception as e:
        append_log(f"❌ Error: {e}")
    finally:
        with STATE_LOCK:
            STATE["status"] = "idle"
            STATE["last_updated"] = time.time()


class AutoUploadHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._send_cors_headers(200)

    def do_GET(self):
        if self.path.startswith("/status"):
            self._send_cors_headers(200)
            with STATE_LOCK:
                payload = dict(STATE)
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        else:
            self._send_cors_headers(404)
            self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = self.rfile.read(length).decode("utf-8", "ignore") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
        except Exception:
            body = {}

        if self.path.startswith("/auto-upload"):
            with STATE_LOCK:
                if STATE["status"] == "running":
                    self._send_cors_headers(409)
                    self.wfile.write(json.dumps({"ok": False, "message": "이미 자동 생성·업로드 작업이 진행 중입니다."}).encode("utf-8"))
                    return

            slug = (body.get("slug") or "").strip()
            count = int(body.get("count") or 1)
            git_push = bool(body.get("git_push", True))
            privacy = (body.get("privacy") or "public").strip()

            cmd = [sys.executable, "-X", "utf8", "min7014_video_maker.py", "--auto-pipeline", "--privacy", privacy]
            if slug:
                cmd += ["--slug", slug]
                label = slug
            else:
                cmd += ["--count", str(count)]
                label = f"batch_{count}"
            if git_push:
                cmd.append("--git-push")

            t = threading.Thread(target=run_pipeline_worker, args=(cmd, label, "AI Video Generation & @min7014_ai Upload"), daemon=True)
            t.start()
            self._send_cors_headers(200)
            self.wfile.write(json.dumps({"ok": True, "started": label}).encode("utf-8"))
            return

        if self.path.startswith("/sync-rss"):
            cmd = [sys.executable, "-X", "utf8", "min7014_video_maker.py", "--sync-channel"]
            t = threading.Thread(target=run_pipeline_worker, args=(cmd, "@min7014_ai", "RSS Auto-Sync"), daemon=True)
            t.start()
            self._send_cors_headers(200)
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            return

        self._send_cors_headers(404)
        self.wfile.write(json.dumps({"error": "unknown endpoint"}).encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    print(f"======================================================================")
    print(f"🤖 [@min7014_ai 자동 영상 생성 & 유튜브 업로드 브릿지 서버 가동]")
    print(f"• Target Channel: https://www.youtube.com/@min7014_ai (UCSlqQfOEtRfJuMPyGMLgFYA)")
    print(f"• Local Endpoint: http://127.0.0.1:{PORT}")
    print(f"======================================================================")
    server = HTTPServer(("127.0.0.1", PORT), AutoUploadHandler)
    server.serve_forever()
