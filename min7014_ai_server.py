#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
min7014_ai_server.py
====================
http://localhost:8765 에서 동작하는 @min7014_ai 전용 로컬 웹 대시보드 & 자동 동기화 데몬
"""

import json
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import min7014_video_maker as maker

ROOT_DIR = Path(__file__).resolve().parent
PORT = 8765

STATE = {
    "status": "idle",
    "current_slug": "",
    "mode": "",
    "logs": ["[@min7014_ai 영상저장고 로컬 서버 가동 완료] http://localhost:8765"],
    "last_updated": time.time(),
}
STATE_LOCK = threading.Lock()


def append_log(line):
    with STATE_LOCK:
        STATE["logs"].append(line)
        if len(STATE["logs"]) > 120:
            STATE["logs"] = STATE["logs"][-120:]
        STATE["last_updated"] = time.time()


def background_rss_watcher():
    """5초마다 @min7014_ai 채널 RSS 피드를 자동 감시하여 업로드된 영상을 즉시 사이트에 등록하고 Git 푸시합니다."""
    last_matched = 0
    while True:
        try:
            matched = maker.sync_youtube_channel_rss()
            if matched > last_matched:
                last_matched = matched
                append_log(f"✅ @min7014_ai 채널에서 {matched}개 주제 업로드 감지! 사이트 자동 연동 및 Git 배포 실행...")
                subprocess.run(["git", "add", "video_lectures/", "assets/"], cwd=str(ROOT_DIR), check=False)
                subprocess.run(["git", "commit", "-m", "chore(youtube-vault): auto-sync @min7014_ai uploaded URLs"], cwd=str(ROOT_DIR), check=False)
                subprocess.run(["git", "push", "origin", "main"], cwd=str(ROOT_DIR), check=False)
        except Exception:
            pass
        time.sleep(6.0)


def build_dashboard_html():
    ready_dir = maker.prepare_ready_batch_folder(open_explorer=False)
    cards_html = []
    idx = 0
    for slug in ["math20250130001", "2014111902", "2017090101", "2014111901"]:
        meta_p = maker.YT_PKG_DIR / f"{slug}_youtube_meta.json"
        if not meta_p.exists():
            continue
        mdata = json.loads(meta_p.read_text(encoding="utf-8"))
        for lc in ["ko", "en"]:
            if lc not in mdata:
                continue
            idx += 1
            info = mdata[lc]
            lang_badge = "🇰🇷 한국어" if lc == "ko" else "🇺🇸 영어 (EN)"
            title_esc = info["title"].replace('"', "&quot;")
            desc_json = json.dumps(info["description"], ensure_ascii=False)
            title_json = json.dumps(info["title"], ensure_ascii=False)
            cards_html.append(f"""
            <div style="background:#fff;border:1px solid #cbd5e1;border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:8px;box-shadow:0 2px 6px rgba(0,0,0,0.04)">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-weight:800;color:#006398;font-size:0.9rem">#{idx}. {lang_badge} · {slug}</span>
                <a href="/download-mp4?slug={slug}&lang={lc}" style="background:#e11d48;color:#fff;text-decoration:none;padding:6px 12px;border-radius:8px;font-weight:800;font-size:0.82rem">⬇️ MP4 영상 파일 받기</a>
              </div>
              <div style="font-size:0.85rem;font-weight:700;color:#1e293b">{title_esc}</div>
              <div style="display:flex;gap:6px;flex-wrap:wrap">
                <button onclick='navigator.clipboard.writeText({title_json});this.textContent="✅ 제목 복사됨"' style="padding:5px 10px;border-radius:6px;border:1px solid #94a3b8;background:#f8fafc;cursor:pointer;font-weight:700;font-size:0.78rem">📋 제목 복사</button>
                <button onclick='navigator.clipboard.writeText({desc_json});this.textContent="✅ 설명·타임스탬프 복사됨"' style="padding:5px 10px;border-radius:6px;border:1px solid #94a3b8;background:#f8fafc;cursor:pointer;font-weight:700;font-size:0.78rem">📋 설명·타임스탬프 복사</button>
                <a href="/download-thumb?slug={slug}&lang={lc}" style="padding:5px 10px;border-radius:6px;border:1px solid #94a3b8;background:#f8fafc;text-decoration:none;color:#1e293b;font-weight:700;font-size:0.78rem">🖼️ 썸네일 받기</a>
                <a href="/download-srt?slug={slug}&lang={lc}" style="padding:5px 10px;border-radius:6px;border:1px solid #94a3b8;background:#f8fafc;text-decoration:none;color:#1e293b;font-weight:700;font-size:0.78rem">📥 자막(.srt) 받기</a>
              </div>
            </div>
            """)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>@min7014_ai 유튜브 영상저장고 업로드 센터</title>
<style>
  body {{ font-family: 'Malgun Gothic', sans-serif; background: #f1f5f9; margin: 0; padding: 24px; color: #0f172a; }}
  .wrap {{ max-width: 1080px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; }}
  .hero {{ background: linear-gradient(135deg, #0f172a, #1e3a8a); color: #fff; padding: 20px 24px; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
  .btn-big {{ background: #e11d48; color: #fff; padding: 12px 20px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 0.95rem; border: none; cursor: pointer; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap: 12px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div>
      <h1 style="margin:0;font-size:1.35rem">🤖 @min7014_ai 유튜브 영상저장고 업로드 센터</h1>
      <p style="margin:6px 0 0;font-size:0.88rem;color:#cbd5e1">
        아래 <b>[⬇️ MP4 영상 파일 받기]</b>를 누르면 현재 크롬 다운로드 목록에 제목이 자동으로 적힌 영상이 받아집니다.<br>
        우측의 <b>[📤 @min7014_ai 업로드 창 열기]</b>를 눌러 크롬 다운로드 바에서 영상을 끌어다 놓으시면, <b>6초마다 자동으로 감지하여 사이트에 등록</b>합니다!
      </p>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn-big" style="background:#0284c7" onclick="downloadAllMp4s()">📥 8개 영상 한 번에 모두 받기</button>
      <a class="btn-big" href="https://studio.youtube.com/channel/UCSlqQfOEtRfJuMPyGMLgFYA/videos/upload?d=ud" target="_blank">📤 @min7014_ai 업로드 창 열기</a>
    </div>
  </div>
  <div class="grid">
    {''.join(cards_html)}
  </div>
</div>
<script>
function downloadAllMp4s() {{
  const links = Array.from(document.querySelectorAll('a[href^="/download-mp4"]'));
  links.forEach((a, i) => setTimeout(() => a.click(), i * 600));
}}
</script>
</body>
</html>"""


class AutoUploadHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self, code=200, content_type="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._send_cors_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        if parsed.path in ("/", "/index.html"):
            html = build_dashboard_html().encode("utf-8")
            self._send_cors_headers(200, "text/html; charset=utf-8")
            self.wfile.write(html)
            return

        if parsed.path == "/download-mp4":
            slug = qs.get("slug", ["math20250130001"])[0]
            lang = qs.get("lang", ["ko"])[0]
            mp4_p = maker.YT_UPLOADS_DIR / slug / f"{slug}_{lang}.mp4"
            meta_p = maker.YT_PKG_DIR / f"{slug}_youtube_meta.json"
            if mp4_p.exists():
                mdata = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {}
                raw_title = mdata.get(lang, {}).get("title", f"{slug}_{lang}")
                import re
                safe_title = re.sub(r'[\\/:*?"<>|]', " ", raw_title).strip()
                dl_name = f"{safe_title[:78]} [{slug}_{lang.upper()}].mp4"
                encoded_name = urllib.parse.quote(dl_name)
                data = mp4_p.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")
                self.end_headers()
                self.wfile.write(data)
                return

        if parsed.path == "/download-thumb":
            slug = qs.get("slug", ["math20250130001"])[0]
            lang = qs.get("lang", ["ko"])[0]
            p = maker.YT_PKG_DIR / f"{slug}_{lang}_thumb.png"
            if p.exists():
                data = p.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Disposition", f'attachment; filename="{slug}_{lang}_thumb.png"')
                self.end_headers()
                self.wfile.write(data)
                return

        if parsed.path == "/download-srt":
            slug = qs.get("slug", ["math20250130001"])[0]
            lang = qs.get("lang", ["ko"])[0]
            p = maker.YT_PKG_DIR / f"{slug}_{lang}.srt"
            if p.exists():
                data = p.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Disposition", f'attachment; filename="{slug}_{lang}.srt"')
                self.end_headers()
                self.wfile.write(data)
                return

        if parsed.path.startswith("/status"):
            self._send_cors_headers(200)
            with STATE_LOCK:
                payload = dict(STATE)
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        else:
            self._send_cors_headers(404)
            self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0) or 0)
        raw_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            body_json = json.loads(raw_body) if raw_body.strip() else {}
        except Exception:
            body_json = {}

        if self.path.startswith("/sync-rss"):
            matched = maker.sync_youtube_channel_rss()
            self._send_cors_headers(200)
            self.wfile.write(json.dumps({"ok": True, "matched": matched}).encode("utf-8"))
            return

        if self.path.startswith("/api/register_youtube_link"):
            slug = str(body_json.get("slug") or "").strip()
            yt_ko = body_json.get("youtube_ko")
            yt_en = body_json.get("youtube_en")
            if not slug:
                self._send_cors_headers(400)
                self.wfile.write(json.dumps({"ok": False, "error": "slug is required"}).encode("utf-8"))
                return
            maker.set_youtube_urls_for_slug(slug, yt_ko=yt_ko, yt_en=yt_en)
            append_log(f"✅ 게시판 링크 수동/직접 등록 완료: {slug} -> KO={yt_ko}, EN={yt_en}")
            self._send_cors_headers(200)
            self.wfile.write(json.dumps({"ok": True, "slug": slug, "youtube_ko": yt_ko, "youtube_en": yt_en}).encode("utf-8"))
            return

        if self.path.startswith("/api/produce_and_upload"):
            slug = str(body_json.get("slug") or "").strip() or None
            count = int(body_json.get("count") or 1)
            with STATE_LOCK:
                if STATE["status"] == "running":
                    self._send_cors_headers(200)
                    self.wfile.write(json.dumps({"ok": False, "busy": True, "message": f"현재 {STATE['current_slug']} 작업이 진행 중입니다."}).encode("utf-8"))
                    return
                STATE["status"] = "running"
                STATE["current_slug"] = slug or f"batch({count})"
                STATE["mode"] = "auto_pipeline"

            def _worker():
                try:
                    append_log(f"🚀 AI 설명영상 제작 & @min7014_ai 자동 업로드 시작: {slug or f'다음 {count}개 자료'}")
                    res = maker.auto_pipeline_batch(count=count, specific_slug=slug, privacy="public", upload_enable=True, git_push=True)
                    append_log(f"✅ AI 설명영상 제작 & @min7014_ai 업로드 완료: {json.dumps(res, ensure_ascii=False)}")
                except Exception as e:
                    append_log(f"⚠️ 작업 중 알림: {e}")
                finally:
                    with STATE_LOCK:
                        STATE["status"] = "idle"
                        STATE["current_slug"] = ""

            threading.Thread(target=_worker, daemon=True).start()
            self._send_cors_headers(200)
            self.wfile.write(json.dumps({"ok": True, "started": True, "slug": slug, "count": count}).encode("utf-8"))
            return

        self._send_cors_headers(200)
        self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    t_rss = threading.Thread(target=background_rss_watcher, daemon=True)
    t_rss.start()
    print(f"======================================================================")
    print(f"🤖 [@min7014_ai 영상저장고 대시보드 가동 완료] http://localhost:{PORT}")
    print(f"======================================================================")
    server = HTTPServer(("127.0.0.1", PORT), AutoUploadHandler)
    server.serve_forever()
