# -*- coding: utf-8 -*-
"""
mathteacher.py
==============
mathedu 수석 수학 교사 에이전트 (MathTeacher) CLI 및 코어 엔진.
- 16,548개 전 연도·전 학년 수학 기출 및 디딤돌 퀴즈 조회·검색·해설·검증 수행
- 초등학생 눈높이 무장벽 디딤돌(0단계 기호 번역 + 1~5단계 수식 유도) 및 시각적 SVG 도식화 해설 생성
"""

import os
import sys
import re
import json
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(BASE_DIR, "board")
SHARDS_DIR = os.path.join(BOARD_DIR, "archive_shards")
INDEX_JSON = os.path.join(BOARD_DIR, "index.json")
CATALOG_JSON = os.path.join(BOARD_DIR, "archive_catalog.json")


def load_all_catalog():
    items = []
    if os.path.exists(INDEX_JSON):
        with open(INDEX_JSON, "r", encoding="utf-8") as f:
            items.extend(json.load(f))
    if os.path.exists(CATALOG_JSON):
        with open(CATALOG_JSON, "r", encoding="utf-8") as f:
            cat = json.load(f)
            existing = {it.get("slug") for it in items}
            for c in cat:
                if c.get("s") in existing:
                    continue
                items.append({
                    "slug": c["s"],
                    "title": c["t"],
                    "examYear": c["y"],
                    "examYearAlt": c.get("ya", ""),
                    "month": c["m"],
                    "grade": c["g"],
                    "subject": c["sub"],
                    "qNum": c["q"],
                    "source": c["src"],
                    "tags": c.get("tg", []),
                    "url": f"board/archive.html?id={c['s']}",
                })
    return items


def cmd_status():
    items = load_all_catalog()
    standalone_cnt = len(json.load(open(INDEX_JSON, "r", encoding="utf-8"))) if os.path.exists(INDEX_JSON) else 0
    shard_files = sorted(os.listdir(SHARDS_DIR)) if os.path.exists(SHARDS_DIR) else []
    print("=" * 72)
    print("👩‍🏫 [mathteacher] 수학 교사 에이전트 상태 보고")
    print("=" * 72)
    print(f"• 전체 등록된 단계별 수학 문항 수 : {len(items):,}문항")
    print(f"• 단독 HTML 퀴즈 페이지 (board/)  : {standalone_cnt:,}개")
    print(f"• 연도별 기출 샤드 DB (2006~2026) : {len(shard_files)}개 연도 샤드")
    print("• 교육 설계 기준                  : 제0단계 기호 번역 + 1~5단계 초등 눈높이 디딤돌 + SVG 도형 + 도식화 흐름도 + min7014.github.io 연계")
    print("=" * 72)


def cmd_search(query: str):
    items = load_all_catalog()
    tokens = [t.strip() for t in query.split() if t.strip()]
    results = []
    for it in items:
        hay = f"{it.get('title','')} {it.get('examYear','')}학년도 {it.get('month','')} {it.get('grade','')} {it.get('subject','')} {it.get('qNum','')}번 {it.get('source','')} {' '.join(it.get('tags',[]))}".lower()
        if all(tok.lower() in hay for tok in tokens):
            results.append(it)
    print(f"🔍 [mathteacher 검색 결과] '{query}' ➔ 총 {len(results):,}문항 매칭 (상위 15건 표시)")
    print("-" * 72)
    for idx, r in enumerate(results[:15], 1):
        url = r.get("url") or f"board/{r['slug']}.html"
        print(f"{idx:2d}. [{r.get('slug')}] {r.get('title')}  ➔  {url}")


def cmd_explain(slug: str):
    m = re.match(r"^e(\d{2})_", slug)
    if m:
        yr = "20" + m.group(1)
        shard_path = os.path.join(SHARDS_DIR, f"exam_{yr}.json")
        if os.path.exists(shard_path):
            d = json.load(open(shard_path, "r", encoding="utf-8"))
            prob = d.get("problems", {}).get(slug)
            if prob:
                print("=" * 72)
                print(f"👩‍🏫 [mathteacher 단계별 해설] {prob['title']}")
                print("=" * 72)
                print(f"• 출처: {prob['source']} ({prob['grade']} {prob['subject']} {prob['qNum']}번, {prob.get('point','3')}점)")
                print(f"• 단원: {' > '.join(prob.get('unit_parts', []))}")
                print(f"• 발문: {re.sub(r'<[^>]+>', '', prob['stem'])}")
                print("-" * 72)
                if prob.get("s3_q"):
                    print(f"🌱 [3단계 출발 조건 식 세우기] 정답 {prob['s3_q']['answer']}번 ➔ {prob['s3_q']['options'][prob['s3_q']['answer']-1]}")
                if prob.get("s4_q"):
                    print(f"🌳 [4단계 중간 관계식 유도]   정답 {prob['s4_q']['answer']}번 ➔ {prob['s4_q']['options'][prob['s4_q']['answer']-1]}")
                ans_i = int(prob.get("answer", 1))
                opts = prob.get("options", [])
                ans_str = opts[ans_i - 1] if 1 <= ans_i <= len(opts) else str(ans_i)
                print(f"💎 [최종 정답] {ans_i}번 ({ans_str})")
                print("=" * 72)
                return
    print(f"문항 슬러그 '{slug}'는 board/{slug}.html 단독 페이지 또는 board/archive.html?id={slug}에서 열람할 수 있습니다.")


def cmd_audit():
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "audit_engine.py")], check=True)
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "audit_full_mathedu.py")], check=True)


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "status":
        cmd_status()
    elif sys.argv[1] == "search":
        q = " ".join(sys.argv[2:])
        cmd_search(q)
    elif sys.argv[1] == "explain" and len(sys.argv) >= 3:
        cmd_explain(sys.argv[2])
    elif sys.argv[1] == "audit":
        cmd_audit()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
