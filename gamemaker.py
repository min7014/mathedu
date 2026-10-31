# -*- coding: utf-8 -*-
"""
gamemaker.py
============
mathedu 수석 게임 디렉터 에이전트 (GameMaker) CLI 및 관리 엔진.
- mathteacher 에이전트와 협력하여 수능 수학 100점 만점 3D 원정대(mathedu-quest-game.js) 및
  게이미피케이션 시스템(mathedu-gamification.js)의 상태 점검, 월드·보스 구성 조회, 무결성 검증을 수행합니다.
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEST_JS = os.path.join(BASE_DIR, "mathedu-quest-game.js")
GAME_JS = os.path.join(BASE_DIR, "mathedu-gamification.js")


def cmd_status():
    q_size = os.path.getsize(QUEST_JS) if os.path.exists(QUEST_JS) else 0
    g_size = os.path.getsize(GAME_JS) if os.path.exists(GAME_JS) else 0
    print("=" * 74)
    print("🎮 [gamemaker] 3D 인터랙티브 수학 게임 디렉터 에이전트 상태 보고")
    print("=" * 74)
    print("• 협업 파트너 에이전트        : 👩‍🏫 mathteacher (수석 수학 교사 에이전트)")
    print("• 최종 게임 목표              : 👑 대학수학능력시험 수학 영역 100점 만점 정복")
    print(f"• 3D 원정대 메인 엔진         : mathedu-quest-game.js ({q_size:,} bytes)")
    print(f"• 게이미피케이션 코어 엔진    : mathedu-gamification.js ({g_size:,} bytes)")
    print("• 탑재된 3D & 게임 기능       :")
    print("  1) 60fps 3D 수학 홀로그램 모뉴먼트 (회전 포물면, 삼각나선, 리만 적층, 단델린의 구, 토러스 매듭, 정이십면체)")
    print("  2) 6대 대륙 3D 행성계 성좌 뷰 (Galaxy Constellation Mode) & 보조선 X-Ray 투시")
    print("  3) 3D 보스 배틀 아레나 (3중 짐벌 결계 파쇄, 3D 파티클 폭발, 육각 허니컴 디딤돌 방어막)")
    print("  4) WebAudio 신디사이저 효과음 (SFX) + 🔥 피버 러시(Fever Rush) + ⚡ 오답 약점 3D 리벤지 레이드")
    print("  5) 16,548문항 실시간 기출 보스 소환 & min7014.github.io 3,400+ 시각 증명 비급서 연동")
    print("=" * 74)


def cmd_worlds():
    print("🗺️ [gamemaker × mathteacher] 6대 탐험 대륙 및 3D 수학 모뉴먼트 목록")
    print("-" * 74)
    worlds = [
        ("World 1 (0➔18점)", "🌱 고1 공통수학 기초 왕국", "3D 회전 포물면 & 원과 직선의 정사영 타워"),
        ("World 2 (18➔45점)", "🔥 수학Ⅰ 지수·로그·삼각·수열 왕국", "3D 단위원 삼각함수 나선(Helix) & 사인·코사인 정사영"),
        ("World 3 (45➔74점)", "⚡ 수학Ⅱ 극한·미분·적분 성채", "3D 구분구적법 리만 원판 적층 & 삼차함수 접선 궤도"),
        ("World 4 (74➔88점)", "🧭 선택과목 3대 신전 (미적·확통·기하)", "3D 단델린의 구(Dandelin Spheres) & 이중 원뿔곡선"),
        ("World 5 (88➔96점)", "🐉 4점 준킬러·킬러 보스 레이드", "3D (2,3)-토러스 매듭 & Frenet-Serret 3축 벡터장"),
        ("World 6 (96➔100점)", "👑 실전 수능 100점 만점 마스터리 전당", "3D 황금비 정이십면체 왕관 & 30문항 피보나치 성좌"),
    ]
    for code, name, mon in worlds:
        print(f"• {code:18s} | {name:30s} | 🌐 {mon}")


def cmd_verify():
    subprocess.run(["node", "-c", QUEST_JS], check=True)
    subprocess.run(["node", "-c", GAME_JS], check=True)
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "audit_engine.py")], check=True)
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "audit_full_mathedu.py")], check=True)


def main():
    arg = sys.argv[1] if len(sys.argv) >= 2 else "status"
    if arg == "worlds":
        cmd_worlds()
    elif arg == "verify":
        cmd_verify()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
