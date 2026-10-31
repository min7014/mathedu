#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pr.py — mathedu Chief Public Relations (PR), Viral Growth & SEO/GEO Director Agent CLI
Collaborates with mathteacher, gamemaker, and designer to drive external traffic,
viral friend-challenge deep links (?challenge=...), multi-channel outreach kits, and AI/Search discoverability.
"""

import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PR_CHANNELS = [
    (
        "kakao",
        "💬 카카오톡 / 단톡방 1:1 3D 기출 보스 결투장",
        "🔥 [수능 수학 100점 만점 3D 원정대 도전장!]\n"
        "내가 방금 3D 기출 보스를 『🧠 DEEP EUREKA!!』로 격파했어!\n"
        "막혀도 초등 눈높이 3단계 디딤돌과 인게임 모눈종이 연습장으로 끝까지 내 힘으로 풀 수 있어.\n"
        "너도 이 문제 첫 시도에 깰 수 있는지 지금 바로 도전해봐! 👇\n"
        "👉 https://min7014.github.io/mathedu/?challenge=csat-2026-22",
    ),
    (
        "insta",
        "📸 인스타그램 스토리 / 스레드 / X(트위터) #공스타그램 인증",
        "👑 [오늘의 수능 수학 100점 만점 3D 원정대 기록]\n"
        "🟩🟩🟩 🧠 DEEP EUREKA!! (무오답 귀납 추론 클리어)\n"
        "⏳ 아르키메데스의 사색 통찰 100% · 🃏 수학자의 성물 덱 완성!\n"
        "16,548개 수능·모의고사 기출과 민은기 선생님의 3,400+ 시각적 기하 증명을 무료 3D 게임으로 정복 중 ✨\n"
        "🔗 https://min7014.github.io/mathedu/\n"
        "#수능수학 #수학100점 #공스타그램 #mathedu #수학게임 #기출문제 #지오지브라",
    ),
    (
        "community",
        "🔥 수험생 커뮤니티 (수만휘 · 오르비 · 포만한 · 스터디 카페) 공유글",
        "📌 [무료 사이트 추천] 수능·평가원·교육청 수학 기출 16,548문항을 3D 게임 + 단계별 디딤돌로 푸는 곳 (mathedu)\n\n"
        "4점 준킬러·킬러 문제 풀다가 막히면 바로 해설지 보면서 자책하곤 했는데,\n"
        "여기(https://min7014.github.io/mathedu/)는 문제를 바로 못 풀어도:\n"
        "1) 제0단계 기호 번역기 ➔ 1단계 초등 직관 ➔ 2단계 (가)·(나) 수식 빈칸 추론으로 힌트를 밟아가며 내 손으로 풀게 해주고,\n"
        "2) 화면 안에 '데카르트 모눈종이 연습장'이랑 '사색 모드(타이머 정지 + 폴리아 3단계 생각 정리)'가 있어서 진짜 생각하는 힘을 길러줍니다.\n"
        "3) '9월 고3 확통 문제들', '수1 삼각함수'처럼 자연어로 검색하면 해당 기출만 싹 모아주고 100% 무료(광고·로그인 강제 없음)입니다!",
    ),
    (
        "teacher",
        "🏫 전국 수학교사 커뮤니티 (인디스쿨 · 수학교사 모임 · 교육 블로그) 안내문",
        "📐 [수업 나눔] 3,400+ 동적 기하(GeoGebra) 시각 증명 & 16,548문항 무장벽 디딤돌 퀴즈 플랫폼 'mathedu'\n\n"
        "민은기 선생님의 수학자료실(https://min7014.github.io/)과 연계된 개방형 수학교육 플랫폼(https://min7014.github.io/mathedu/)을 소개합니다.\n"
        "• 수학 기초가 부족한 학생도 포물선·타원(단델린의 구), 삼각함수, 미적분, 확통 기출을 1단계 초등 직관부터 차근차근 따라가며 스스로 해결할 수 있습니다.\n"
        "• 교실 전자칠판/태블릿에서 60fps 3D 수학 도형 홀로그램을 360도 돌려보고, QR 코드로 실시간 수업 방을 열어 학생들과 함께 활용할 수 있는 100% 영구 무료 OER 자료실입니다.",
    ),
    (
        "global",
        "🌐 Global EdTech / Reddit (r/learnmath, r/math) 영문 소개문",
        "🚀 [Open Educational Resource] mathedu: 3,400+ Visual Geometry Proofs & 16,548 Micro-Scaffolded Math Problems in a 60fps 3D Web RPG!\n"
        "Explore interactive 3D mathematical monuments (Dandelin Spheres, Euler Spirals, Riemann Sums), use the built-in Descartes Scratchpad & Polya's 3-Step Deep Contemplation mode, and master calculus, geometry, and probability step by step — 100% free & open.\n"
        "👉 https://min7014.github.io/mathedu/",
    ),
]


def cmd_status():
    quest_js = os.path.join(ROOT_DIR, "mathedu-quest-game.js")
    llms_txt = os.path.join(ROOT_DIR, "llms.txt")
    sitemap_xml = os.path.join(ROOT_DIR, "sitemap.xml")
    q_size = os.path.getsize(quest_js) if os.path.exists(quest_js) else 0
    l_size = os.path.getsize(llms_txt) if os.path.exists(llms_txt) else 0
    s_size = os.path.getsize(sitemap_xml) if os.path.exists(sitemap_xml) else 0
    print("=" * 74)
    print("📣 [pr] 수석 대외홍보(PR) · 바이럴 그로스 & SEO/GEO 에이전트 상태 보고")
    print("=" * 74)
    print("• 4대 에이전트 협업 체제      : 👩‍🏫 mathteacher × 🎮 gamemaker × 🎨 designer × 📣 pr")
    print("• 핵심 미션                  : 외부 홍보 극대화 · 바이럴 친구 도전장 · 검색/AI 엔진 유입 활성화")
    print(f"• 인게임 바이럴 공유 엔진     : mathedu-quest-game.js ({q_size:,} bytes)")
    print(f"• AI 검색엔진 매니페스트      : llms.txt ({l_size:,} bytes)")
    print(f"• 검색엔진 사이트맵           : sitemap.xml ({s_size:,} bytes)")
    print("• 탑재된 외부 홍보 & 바이럴 시스템 :")
    print("  1) ⚔️ 원클릭 친구 도전장 딥링크 (?challenge=문항ID 접속 시 3D 보스전 즉시 자동 소환)")
    print("  2) 🟩 Wordle 스타일 이모지 전적 인증 카드 (DEEP EUREKA · 수능 만점 게이지 · 성물 배지)")
    print("  3) 📋 5대 채널 맞춤 홍보 키트 (카카오톡 / 인스타·X / 수만휘·오르비 / 교사 모임 / Global)")
    print("  4) 🤖 AI 검색엔진 최적화 (llms.txt + Schema.org VideoGame/LearningResource 구조화 데이터)")
    print("  5) 📱 모바일 Web Share API 네이티브 공유 & QR 코드 스터디 초대 연동")
    print("=" * 74)


def cmd_kit():
    print("=" * 74)
    print("📣 [pr] 5대 외부 채널별 즉시 활용 가능한 홍보 문구 (Outreach Copy Kit)")
    print("=" * 74)
    for cid, title, copy_text in PR_CHANNELS:
        print(f"\n[{cid.upper()}] {title}")
        print("-" * 74)
        print(copy_text)
    print("\n" + "=" * 74)


def cmd_verify():
    print("🔍 [pr] 바이럴 딥링크·SEO/GEO 매니페스트 및 플랫폼 무결성 검증 시작...")
    llms_path = os.path.join(ROOT_DIR, "llms.txt")
    if not os.path.exists(llms_path) or os.path.getsize(llms_path) < 100:
        print("❌ llms.txt 누락 또는 크기 부족")
        sys.exit(1)
    print("✅ llms.txt AI 검색엔진 매니페스트 확인 완료!")
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
    if cmd == "kit":
        cmd_kit()
    elif cmd == "verify":
        cmd_verify()
    else:
        cmd_status()
