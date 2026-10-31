#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
designer.py — mathedu Chief Art & UI/UX Design Director Agent CLI
Collaborates with mathteacher (Math Pedagogy) & gamemaker (3D Game Mechanics)
to elevate visual hierarchy, mathematical typography, theme skins, and cognitive ergonomics.
"""

import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DESIGN_THEMES = [
    ("cosmic", "🌌 코스믹 아틀리에 (Cosmic Atelier)", "딥 스페이스 네이비(#060b19) + 에메랄드/시안 홀로그램 글래스모피즘"),
    ("sanctuary", "🧘 플라톤의 사색 서재 (Plato's Sanctuary)", "웜 인디고·오로라 바이올렛(#0f1026) + 눈이 편안한 사색 골드·민트 아틀리에"),
    ("euclid", "📜 유클리드 왕립 아카데미 (Euclid Royal)", "학술 아카데미 하이콘트라스트 슬레이트(#0b1320) + 로얄 골드 & 애저 잉크 포인트"),
]


def cmd_status():
    quest_js = os.path.join(ROOT_DIR, "mathedu-quest-game.js")
    index_html = os.path.join(ROOT_DIR, "index.html")
    q_size = os.path.getsize(quest_js) if os.path.exists(quest_js) else 0
    i_size = os.path.getsize(index_html) if os.path.exists(index_html) else 0
    print("=" * 74)
    print("🎨 [designer] 수석 아트 & UI/UX 디자인 디렉터 에이전트 상태 보고")
    print("=" * 74)
    print("• 3대 에이전트 협업 체제      : 👩‍🏫 mathteacher × 🎮 gamemaker × 🎨 designer")
    print("• 핵심 디자인 철학            : 📐 황금비(φ=1.618) 여백 · 수식 가독성 최우선 · 사색 몰입 인체공학")
    print(f"• 3D 원정대 UI/UX 스타일 엔진 : mathedu-quest-game.js ({q_size:,} bytes)")
    print(f"• 메인 포털 Stitch 디자인     : index.html ({i_size:,} bytes)")
    print("• 탑재된 핵심 디자인 시스템   :")
    print("  1) 🎨 3대 비주얼 테마 스킨 스위처 (🌌 코스믹 아틀리에 / 🧘 플라톤의 사색 서재 / 📜 유클리드 아카데미)")
    print("  2) 📐 황금비(φ=1.618) 시각적 위계 및 2단 캡슐 도크 HUD (인지 부하 최소화)")
    print("  3) ✒️ 수식(MathJax/LaTeX) & 핵심 조건 하이라이트 퍼스트 타이포그래피")
    print("  4) 🧘 사색 모드(Deep Focus) 연동 앰비언트 오로라 컬러 시프트 & 글래스모피즘")
    print("  5) ✨ 물리 탄성 마이크로 인터랙션(cubic-bezier) & 모바일/태블릿/PC 반응형 인체공학")
    print("=" * 74)


def cmd_themes():
    print("=" * 74)
    print("🎨 [designer] 인게임 3대 비주얼 테마 팔레트 명세")
    print("=" * 74)
    for tid, name, desc in DESIGN_THEMES:
        print(f"• [{tid}] {name}")
        print(f"    └─ {desc}")
    print("=" * 74)


def cmd_verify():
    print("🔍 [designer] UI/UX 스크립트 문법 및 플랫폼 무결성 검증 시작...")
    r1 = subprocess.run(["node", "-c", "mathedu-quest-game.js"], cwd=ROOT_DIR)
    if r1.returncode != 0:
        sys.exit(r1.returncode)
    print("✅ mathedu-quest-game.js 문법 검증 통과!")
    r2 = subprocess.run([sys.executable, "audit_engine.py"], cwd=ROOT_DIR)
    if r2.returncode != 0:
        sys.exit(r2.returncode)
    r3 = subprocess.run([sys.executable, "audit_full_mathedu.py"], cwd=ROOT_DIR)
    sys.exit(r3.returncode)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    if cmd == "themes":
        cmd_themes()
    elif cmd == "verify":
        cmd_verify()
    else:
        cmd_status()
