#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finance.py — mathedu Chief Ad Monetization & Sustainable Free-EdTech Director Agent CLI
Keeps mathedu 100% free for all students and teachers while monetizing traffic
through non-intrusive Google AdSense, Kakao AdFit, and In-Game Rewarded Sponsor Chests.
"""

import os
import re
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ADS_JS_PATH = os.path.join(ROOT_DIR, "mathedu-ads.js")
ADS_TXT_PATH = os.path.join(ROOT_DIR, "ads.txt")


def cmd_status():
    ads_js_size = os.path.getsize(ADS_JS_PATH) if os.path.exists(ADS_JS_PATH) else 0
    ads_txt_size = os.path.getsize(ADS_TXT_PATH) if os.path.exists(ADS_TXT_PATH) else 0
    print("=" * 76)
    print("💼 [finance] 무료 교육 지속가능성 & 클린 광고 수익화 디렉터 상태 보고")
    print("=" * 76)
    print("• 5대 에이전트 협업 생태계    : 👩‍🏫 mathteacher × 🎮 gamemaker × 🎨 designer × 📣 pr × 💼 finance")
    print("• 수익화 핵심 원칙            : 학생·교사 100% 영구 무료 학습 + 비침습적 클린 광고 수익 창출")
    print(f"• 클린 광고 & 보상형 엔진     : mathedu-ads.js ({ads_js_size:,} bytes)")
    print(f"• IAB 공식 광고 인증 파일     : ads.txt ({ads_txt_size:,} bytes)")
    print("• 탑재된 4대 광고 수익화 시스템 :")
    print("  1) 🎁 인게임 보상형 광고 — 『아르키메데스의 후원 상자 (Rewarded Ad Chest)』")
    print("     └─ 학생이 자발적으로 5초 스폰서 광고 시청 시 [+50 XP + 기하 필살기 100% 완충 + 통찰 +40%] 지급")
    print("  2) 🖼️ 네이티브 글래스모피즘 배너 슬롯 (Google AdSense & Kakao AdFit 완벽 호환)")
    print("     └─ 문제 풀이와 수식 가독성을 절대 방해하지 않는 하단 네이티브 스폰서 카드 배치")
    print("  3) 📊 인게임 『💼 광고 수익화 & 애드센스 관제 센터 모달 (openFinanceModal)』")
    print("     └─ 노출수(Impressions), 보상형 상자 클릭수, 예상 광고 수익 시뮬레이터 & 원클릭 ID 설정")
    print("  4) 📄 표준 ads.txt 및 원클릭 퍼블리셔 ID 교체 CLI 지원")
    print("=" * 76)


def cmd_set_adsense():
    client_id = "ca-pub-0000000000000000"
    slot_id = "1234567890"
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a in ("--client", "-c") and i + 1 < len(args):
            client_id = args[i + 1].strip()
        elif a in ("--slot", "-s") and i + 1 < len(args):
            slot_id = args[i + 1].strip()
        elif a.startswith("ca-pub-"):
            client_id = a.strip()

    pub_num = client_id.replace("ca-", "")
    if os.path.exists(ADS_TXT_PATH):
        with open(ADS_TXT_PATH, "r", encoding="utf-8") as f:
            txt = f.read()
        txt = re.sub(r"pub-\d+", pub_num, txt)
        with open(ADS_TXT_PATH, "w", encoding="utf-8") as f:
            f.write(txt)

    if os.path.exists(ADS_JS_PATH):
        with open(ADS_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read()
        js = re.sub(r"adsenseClient:\s*'[^']*'", f"adsenseClient: '{client_id}'", js)
        js = re.sub(r"adsenseSlotMain:\s*'[^']*'", f"adsenseSlotMain: '{slot_id}'", js)
        with open(ADS_JS_PATH, "w", encoding="utf-8") as f:
            f.write(js)

    print(f"✅ Google AdSense 설정 완료: client={client_id}, slot={slot_id}")


def cmd_verify():
    print("🔍 [finance] 광고 엔진 문법, ads.txt 및 전체 플랫폼 무결성 검증 시작...")
    if not os.path.exists(ADS_TXT_PATH):
        print("❌ ads.txt 파일이 없습니다.")
        sys.exit(1)
    print("✅ ads.txt 확인 완료!")
    for script in ["mathedu-ads.js", "mathedu-quest-game.js"]:
        r = subprocess.run(["node", "-c", script], cwd=ROOT_DIR)
        if r.returncode != 0:
            sys.exit(r.returncode)
        print(f"✅ {script} 문법 검증 통과!")
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
    if cmd == "set-adsense":
        cmd_set_adsense()
    elif cmd == "verify":
        cmd_verify()
    else:
        cmd_status()
