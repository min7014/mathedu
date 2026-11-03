# -*- coding: utf-8 -*-
"""
mathedu_foundation_daemon.py
============================
[수학홈페이지(mathedu) 근간 상시 진화 통합 데몬 — Continuous Foundation Evolution Engine]
민은기 선생님의 지시("이 작업은 지속적으로 해야 한다. 수학홈페이지의 근간을 이루는 것이기 때문이다.")에 따라
24시간 무중단으로 다음 3대 근간(Foundation Pillars)을 지속적으로 확장·업그레이드·동기화합니다:

1. [Pillar 1: min7014.github.io 1,113개 심층 수학자료 × mathteacher 4대 수학교육 발전 모듈 상시 확장]
   - 수직 계통성 개념 계보 트리(Vertical Concept Genealogy)
   - 폴리아(Pólya) 조건 ➔ 제1보조선·발상 1초 번역 사전(Heuristic Dictionary)
   - 라카토스 오개념 백신 & 1초 반례 실험실(Misconception Vaccine & Counterexample Lab)
   - 교사용 5분 탐구 수업 시나리오 & 발문 런처(5-Minute Inquiry Lesson Launcher)
   - min7014_deep_knowledge.json의 1,113개 주제에서 아직 수업 시나리오·보조선 사전에 편입되지 않은 주제를 지속적으로 발굴해 assets/mathteacher_pedagogy_engine.json 및 index.html에 자동 반영합니다.

2. [Pillar 2: @min7014_ai v4.0 Viral Cinema 1080p 설명영상 & 9:16 숏폼(#Shorts) 무중단 제작]
   - min7014.github.io의 847개 시각적 증명 플립북 PDF를 순차적으로 스캔하여,
     아직 제작되지 않은 주제의 8개국어 BAZE Vision(claude-sonnet-4-6) 대본,
     v4.0 1080p 본편 영상(3초 클라이맥스 콜드오픈 + 플립북 모션 + -28dB 사색 앰비언트 패드 + 유레카 차임벨 + CTR 14%+ 4단어 임팩트 썸네일)과
     9:16 세로형 숏폼(#Shorts, 58초 미만 보장)을 한국어(KO)·영어(EN)로 지속 제작합니다.

3. [Pillar 3: @min7014_ai 유튜브 채널 자동 업로드 · RSS 실시간 감지 · GitHub Pages 자동 배포]
   - 유튜브 일일 업로드 쿼터가 열리는 즉시 대기 중인 1080p 본편 및 #Shorts를 자동 업로드하고,
   - 커스텀 썸네일·SEO 메타데이터·유레카 퀴즈 고정 댓글·재생목록을 최신화하며,
   - 카탈로그(video_lectures/catalog.json, vault_index.json, assets/mathteacher_pedagogy_engine.json)를 Git Commit & Push 합니다.
"""

import os
import sys
import time
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
PEDAGOGY_JSON = ROOT_DIR / "assets" / "mathteacher_pedagogy_engine.json"
DEEP_JSON = ROOT_DIR / "assets" / "min7014_deep_knowledge.json"
STATUS_JSON = ROOT_DIR / "video_lectures" / "foundation_daemon_status.json"


def ensure_video_maker_hooked():
    p = ROOT_DIR / "min7014_video_maker.py"
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    old = '                    update_video_catalog()\n                    print(f"✅ [Continuous Factory Complete] {next_slug} (1080p KO/EN + #Shorts KO/EN 제작 및 카탈로그 반영 완료!)", flush=True)'
    new = '''                    update_video_catalog()
                    try:
                        import mathteacher
                        import mathedu_foundation_daemon as fdaemon
                        mathteacher.expand_pedagogy_from_min7014_vault(max_add_per_category=2)
                        fdaemon.mine_next_pedagogy_item_from_deep_knowledge()
                        fdaemon.sync_pedagogy_counts_to_index_html()
                        fdaemon.write_daemon_heartbeat(last_completed_slug=next_slug)
                    except Exception as pe_err:
                        print(f"[Pedagogy Sync Notice] {pe_err}", flush=True)
                    subprocess.run(["git", "add", "video_lectures/catalog.json", "video_lectures/vault_index.json", "video_lectures/scripts/", "video_lectures/youtube_packages/", "video_lectures/shorts/", "assets/min7014_deep_knowledge.json", "assets/mathteacher_pedagogy_engine.json", "index.html"], check=False)
                    subprocess.run(["git", "commit", "-m", f"chore(foundation): continuous v4.0 video/shorts & mathteacher pedagogy evolution ({next_slug})"], check=False)
                    subprocess.run(["git", "push", "origin", "main"], check=False)
                    print(f"✅ [Continuous Factory & Pedagogy Evolution Complete] {next_slug} (1080p KO/EN + #Shorts KO/EN + 수학교육 모듈 동기화 완료!)", flush=True)'''
    if old in s and "Continuous Factory & Pedagogy Evolution Complete" not in s:
        s = s.replace(old, new, 1)
        p.write_text(s, encoding="utf-8")


def write_daemon_heartbeat(last_completed_slug=""):
    try:
        ped = json.loads(PEDAGOGY_JSON.read_text(encoding="utf-8")) if PEDAGOGY_JSON.exists() else {}
        cat_p = ROOT_DIR / "video_lectures" / "catalog.json"
        cat = json.loads(cat_p.read_text(encoding="utf-8")) if cat_p.exists() else []
        STATUS_JSON.parent.mkdir(parents=True, exist_ok=True)
        STATUS_JSON.write_text(json.dumps({
            "daemon": "mathedu_foundation_daemon (24/7 Continuous Evolution)",
            "updated_at": datetime.now().isoformat(),
            "last_completed_slug": last_completed_slug,
            "total_rendered_video_topics": len(cat),
            "pedagogy_counts": {
                "verticalGenealogy": len(ped.get("verticalGenealogy", [])),
                "polyaHeuristics": len(ped.get("polyaHeuristics", [])),
                "misconceptionLab": len(ped.get("misconceptionLab", [])),
                "teacherLessonScenarios": len(ped.get("teacherLessonScenarios", [])),
                "creativeConstructiveLab": len(ped.get("creativeConstructiveLab", [])),
            }
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def mine_next_pedagogy_item_from_deep_knowledge():
    """
    min7014_deep_knowledge.json(1,113개 주제)에서 아직 교사용 5분 탐구 시나리오나 폴리아 보조선 사전에
    등록되지 않은 우수 시각적 증명 주제를 1건씩 발굴하여 mathteacher_pedagogy_engine.json에 자동 추가합니다.
    """
    if not PEDAGOGY_JSON.exists() or not DEEP_JSON.exists():
        return False

    ped = json.loads(PEDAGOGY_JSON.read_text(encoding="utf-8"))
    deep_items = json.loads(DEEP_JSON.read_text(encoding="utf-8"))

    scenarios = ped.setdefault("teacherLessonScenarios", [])
    polya_list = ped.setdefault("polyaHeuristics", [])
    existing_scen_ids = {s.get("id") for s in scenarios}
    existing_polya_ids = {p.get("id") for p in polya_list}

    changed = False
    for it in deep_items:
        item_id = (it.get("id") or "").strip()
        title = re.sub(r"\$[^\$]*\$", "", (it.get("title") or "")).strip()
        tips = it.get("solving_tips") or []
        steps = it.get("scaffolding_steps") or []
        sub_ko = (it.get("sub_domain_ko") or "기하·대수 탐구").split("(")[0].strip()

        if not item_id or not title or len(title) < 4:
            continue

        polya_id = f"polya-min-{item_id}"
        if polya_id not in existing_polya_ids and tips and len(polya_list) < 80:
            tip_text = tips[0].strip()
            if len(tip_text) > 15:
                polya_list.append({
                    "id": polya_id,
                    "domain": sub_ko,
                    "condition": f"[{title}] 관련 도형·수식 구조가 문제에 등장할 때",
                    "firstAction": tip_text,
                    "visualIntuition": (it.get("core_concept") or tip_text)[:140],
                    "formulaBridge": (steps[-1] if steps else tip_text)[:120],
                    "min7014Query": sub_ko,
                    "searchKeyword": sub_ko.replace("·", " ").split()[0]
                })
                existing_polya_ids.add(polya_id)
                changed = True
                print(f"🧭 [Foundation Daemon: Pólya Heuristic Mined] {polya_id} ({title})", flush=True)
                break

    # 탈-5지선다 창의 구성 & What-If-Not 실험실 자동 확장
    creative_list = ped.setdefault("creativeConstructiveLab", [])
    existing_creative_ids = {c.get("id") for c in creative_list}
    for it in deep_items:
        item_id = (it.get("id") or "").strip()
        title = re.sub(r"\$[^\$]*\$", "", (it.get("title") or "")).strip()
        tips = it.get("solving_tips") or []
        steps = it.get("scaffolding_steps") or []
        sub_ko = (it.get("sub_domain_ko") or "기하·대수 탐구").split("(")[0].strip()
        if not item_id or not title or len(title) < 4:
            continue
        cid = f"creative-min-{item_id}"
        if cid not in existing_creative_ids and len(steps) >= 3 and len(creative_list) < 60:
            creative_list.append({
                "id": cid,
                "domain": sub_ko,
                "title": f"[{title}] 보기를 가리고 스스로 보조선과 증명 경로 재발명하기",
                "originalProblem": (it.get("core_concept") or title)[:160],
                "constructivePrompt": f"5지선다 보기에 의존하지 않고, '{title}'의 핵심 보조선을 직접 그어 첫 번째 관계식을 구성해 보세요.",
                "multiPathApproaches": [s[:130] for s in steps[:3]],
                "whatIfNotMutation": f"만약 [{title}]에서 주어진 도형의 대칭 조건이나 각도·차수를 일반화한다면(What-If-Not) 어떤 새로운 정리가 탄생할까?",
                "min7014Query": sub_ko,
                "searchKeyword": sub_ko.replace("·", " ").split()[0]
            })
            existing_creative_ids.add(cid)
            changed = True
            print(f"✍️ [Foundation Daemon: Creative What-If-Not Mined] {cid} ({title})", flush=True)
            break

    if changed:
        PEDAGOGY_JSON.write_text(json.dumps(ped, ensure_ascii=False, indent=2), encoding="utf-8")
    return changed


def sync_pedagogy_counts_to_index_html():
    """assets/mathteacher_pedagogy_engine.json의 최신 데이터를 index.html 인라인 폴백 및 배지 카운트에 동기화합니다."""
    index_p = ROOT_DIR / "index.html"
    if not index_p.exists() or not PEDAGOGY_JSON.exists():
        return
    try:
        ped = json.loads(PEDAGOGY_JSON.read_text(encoding="utf-8"))
        html = index_p.read_text(encoding="utf-8")
        g_cnt = len(ped.get("verticalGenealogy", []))
        p_cnt = len(ped.get("polyaHeuristics", []))
        v_cnt = len(ped.get("misconceptionLab", []))
        l_cnt = len(ped.get("teacherLessonScenarios", []))
        c_cnt = len(ped.get("creativeConstructiveLab", []))

        html = re.sub(r"🌳 1\. 초·중·고 수직 계통성 트리 \(\d+\)", f"🌳 1. 초·중·고 수직 계통성 트리 ({g_cnt})", html)
        html = re.sub(r"🧭 2\. 폴리아 조건➔보조선 사전 \(\d+\)", f"🧭 2. 폴리아 조건➔보조선 사전 ({p_cnt})", html)
        html = re.sub(r"🔬 3\. 오개념 백신 &amp; 반례 실험실 \(\d+\)", f"🔬 3. 오개념 백신 &amp; 반례 실험실 ({v_cnt})", html)
        html = re.sub(r"👩‍🏫 4\. 교사용 5분 탐구 수업 런처 \(\d+\)", f"👩‍🏫 4. 교사용 5분 탐구 수업 런처 ({l_cnt})", html)
        html = re.sub(r"✍️ 5\. 탈-5지선다 창의 구성 &amp; 문제 발명 \(\d+\)", f"✍️ 5. 탈-5지선다 창의 구성 &amp; 문제 발명 ({c_cnt})", html)
        html = re.sub(r">\d+대 계보<", f">{g_cnt}대 계보<", html)
        html = re.sub(r">\d+대 법칙<", f">{p_cnt}대 법칙<", html)
        html = re.sub(r">\d+대 반례<", f">{v_cnt}대 반례<", html)

        ped_js = json.dumps(ped, ensure_ascii=False, indent=2)
        pattern = r"window\.MATHEDU_PEDAGOGY_ENGINE_DATA\s*=\s*\{.*?\};\s*\nwindow\._currentMtHubTab"
        replacement = f"window.MATHEDU_PEDAGOGY_ENGINE_DATA = {ped_js};\nwindow._currentMtHubTab"
        new_html, n_subs = re.subn(pattern, lambda _: replacement, html, count=1, flags=re.S)
        if n_subs > 0 and new_html != html:
            index_p.write_text(new_html, encoding="utf-8")
    except Exception as e:
        print(f"[Index Pedagogy Sync Notice] {e}", flush=True)


def run_continuous_foundation_loop(single_cycle=False):
    ensure_video_maker_hooked()
    import mathteacher
    import pr
    import min7014_video_maker as vmaker

    print("=" * 78, flush=True)
    print("🏛️ [mathedu Foundation Daemon] 수학홈페이지 근간(수학교육 발전 + v4.0 영상/숏폼) 상시 진화 가동!", flush=True)
    print("=" * 78, flush=True)

    mathteacher.expand_pedagogy_from_min7014_vault(max_add_per_category=5)
    mine_next_pedagogy_item_from_deep_knowledge()
    sync_pedagogy_counts_to_index_html()
    try:
        pr.run_autonomous_pr_cycle()
    except Exception as pr_err:
        print(f'[PR Agent Notice] {pr_err}', flush=True)
    write_daemon_heartbeat()

    if single_cycle:
        return

    vmaker.run_shorts_and_video_upload_daemon(open_studio_now=False)


if __name__ == "__main__":
    is_once = "--once" in sys.argv
    run_continuous_foundation_loop(single_cycle=is_once)
