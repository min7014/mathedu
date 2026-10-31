#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
google_play_publish.py
===============================================================================
🎮 수학의 성전 3D (mathedu) — Google Play Store 등록 & 패키징 관제 도구
- Google Play Console 업로드에 필요한 모든 파일(manifest.json, sw.js, game.html,
  privacy.html, .well-known/assetlinks.json, 스토어 그래픽 에셋 5종) 상태를 점검하고,
- 앱 서명 인증서(SHA-256) 지문을 .well-known/assetlinks.json에 원클릭 등록합니다.
===============================================================================
"""

import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETLINKS = ROOT / ".well-known" / "assetlinks.json"


def check_status():
    print("=" * 78)
    print("🎮 [Google Play Store 등록 준비 상태 점검 — 수학의 성전 3D (mathedu)]")
    print("=" * 78)
    print("• 패키지 ID (Application ID) : io.github.min7014.mathedu")
    print("• 게임 전용 런처 URL         : https://min7014.github.io/mathedu/game.html")
    print("• 웹 매니페스트 URL          : https://min7014.github.io/mathedu/manifest.json")
    print("• 개인정보처리방침 URL       : https://min7014.github.io/mathedu/privacy.html")
    print("• Digital Asset Links URL    : https://min7014.github.io/mathedu/.well-known/assetlinks.json")
    print("-" * 78)

    required_files = [
        "game.html",
        "manifest.json",
        "sw.js",
        "privacy.html",
        "twa-manifest.json",
        ".nojekyll",
        ".well-known/assetlinks.json",
    ]
    for rf in required_files:
        p = ROOT / rf
        print(f"  [{'✅' if p.exists() else '❌'}] {rf:<30} ({p.stat().st_size if p.exists() else 0:,} bytes)")

    print("-" * 78)
    print("🖼️ [Google Play Console 스토어 등록용 그래픽 에셋 (assets/play_store/)]")
    assets_check = [
        ("앱 아이콘 (512x512)", ROOT / "assets/play_store/app_icon_512x512.png", (512, 512)),
        ("그래픽 이미지 (1024x500)", ROOT / "assets/play_store/feature_graphic_1024x500.png", (1024, 500)),
        ("휴대전화 스크린샷 1 (1080x1920)", ROOT / "assets/play_store/phone_screenshot_1_1080x1920.png", (1080, 1920)),
        ("휴대전화 스크린샷 2 (1080x1920)", ROOT / "assets/play_store/phone_screenshot_2_1080x1920.png", (1080, 1920)),
        ("태블릿 스크린샷 1 (1920x1080)", ROOT / "assets/play_store/tablet_screenshot_1_1920x1080.png", (1920, 1080)),
    ]
    for label, path, expected_size in assets_check:
        if path.exists():
            im = Image.open(path)
            ok = im.size == expected_size
            print(f"  [{'✅' if ok else '⚠️'}] {label:<30} : {path.relative_to(ROOT)} ({im.size[0]}x{im.size[1]})")
        else:
            print(f"  [❌] {label:<30} : 누락")
    print("=" * 78)


def set_sha256(fp: str, pkg: str = "io.github.min7014.mathedu"):
    fp = fp.strip().upper()
    data = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": pkg,
                "sha256_cert_fingerprints": [fp],
            },
        }
    ]
    ASSETLINKS.parent.mkdir(parents=True, exist_ok=True)
    ASSETLINKS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ .well-known/assetlinks.json 업데이트 완료: package={pkg}, sha256={fp}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) > 2 and sys.argv[1] == "set-sha256":
        pkg_arg = sys.argv[3] if len(sys.argv) > 3 else "io.github.min7014.mathedu"
        set_sha256(sys.argv[2], pkg_arg)
    else:
        check_status()
