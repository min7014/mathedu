#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
youtube_community_controller.py
===============================
[@min7014_ai 유튜브 단독 최우선 수익화 — 0-쿼터 YouTube Studio 직결 성장 & 쇼츠➔장편 시청시간 퍼널 엔진 v2.0]

1. [YouTube Studio 쇼츠 '관련 동영상(Related Video)' 100% 자동 연결 (API 미지원 독점 기능 · 쿼터 소모 0)]:
   - 채널 조회수의 93.7%를 견인하는 모든 #Shorts 및 Q-#Shorts에 대해
     https://studio.youtube.com/video/{short_id}/edit 에 직접 접속하여
     해당 주제의 1080p 풀버전 본편 또는 25~88분 정주행 마스터클래스를 '관련 동영상'으로 자동 바인딩합니다.
   - 스마트폰 쇼츠 하단에 클릭 가능한 '▶️ 본편 바로가기' 버튼이 생성되어 4,000시간 시청시간과 구독자 전환을 극대화합니다.

2. [비구독자 홈 피드 노출용 소크라테스 5초 수학 퀴즈 커뮤니티 자동 발행 (쿼터 소모 0)]:
   - 정답 스포일러(✅)를 제거하여 호기심 클릭률과 댓글 토론을 유도하는 24종+ 한/영 시각 수학 퀴즈를
     12시간 간격으로 https://www.youtube.com/@min7014_ai/posts 에 자동 발행합니다.

3. [YouTube Data API v3 댓글 자동 소통 연동]:
   - 시청자 댓글 및 퀴즈 답글에 수학적 해설과 1-클릭 구독 링크 자동 답글을 게시합니다.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import silent_subprocess  # noqa: F401 — Playwright node.exe 및 하위 프로세스 완전 무창 강제

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
ROBOT_PROFILE_DIR = ROOT_DIR / ".yt_chrome_robot_profile"
ROBOT_LOCK_FILE = ROOT_DIR / ".agents" / "yt_robot_browser.lock"
RELATED_LINKED_STATE_FILE = ROOT_DIR / ".agents" / "studio_shorts_related_linked.json"
COMMUNITY_PACK_JSON = ROOT_DIR / "youtube_uploads" / "community_posts" / "community_posts_pack.json"
COMMUNITY_STATE_JSON = ROOT_DIR / "youtube_uploads" / "community_posts" / "published_community_state.json"
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
CHANNEL_ID = "UCSlqQfOEtRfJuMPyGMLgFYA"
CHANNEL_POSTS_URL = "https://www.youtube.com/@min7014_ai/posts"
STUDIO_COMMENTS_URL = "https://studio.youtube.com/channel/UCSlqQfOEtRfJuMPyGMLgFYA/comments/inbox"
CHROME_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def _is_pid_running(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            import ctypes
            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
            if not handle:
                return False
            try:
                exit_code = ctypes.c_ulong(0)
                if ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                    return exit_code.value == 259
                return True
            finally:
                ctypes.windll.kernel32.CloseHandle(handle)
        except Exception:
            return False
    return False


def _acquire_robot_lock(max_age_sec: int = 420) -> bool:
    ROBOT_LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    if ROBOT_LOCK_FILE.exists():
        try:
            d = json.loads(ROBOT_LOCK_FILE.read_text(encoding="utf-8"))
            owner_pid = int(d.get("pid") or 0)
            if owner_pid != os.getpid() and _is_pid_running(owner_pid) and (now - float(d.get("ts", 0))) < max_age_sec:
                return False
        except Exception:
            pass
    ROBOT_LOCK_FILE.write_text(json.dumps({"pid": os.getpid(), "ts": now}), encoding="utf-8")
    return True


def _release_robot_lock() -> None:
    try:
        if ROBOT_LOCK_FILE.exists():
            ROBOT_LOCK_FILE.unlink()
    except Exception:
        pass


def _launch_robot_context(p, headless: bool = True):
    ROBOT_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    extra_args = ["--disable-blink-features=AutomationControlled"]
    if not headless:
        extra_args.append("--start-maximized")
    for ch_name in ("chrome", "msedge"):
        try:
            return p.chromium.launch_persistent_context(
                user_data_dir=str(ROBOT_PROFILE_DIR),
                channel=ch_name,
                headless=headless,
                user_agent=CHROME_UA,
                viewport={"width": 1440, "height": 960},
                ignore_default_args=["--enable-automation"],
                args=extra_args,
            )
        except Exception:
            continue
    return p.chromium.launch_persistent_context(
        user_data_dir=str(ROBOT_PROFILE_DIR),
        headless=headless,
        user_agent=CHROME_UA,
        viewport={"width": 1440, "height": 960},
        ignore_default_args=["--enable-automation"],
        args=extra_args,
    )


def ensure_socratic_community_quiz_packs() -> list[dict]:
    """
    https://min7014.github.io/ 오리지널 시각 증명에 기반한 고참여 5초 수학 퀴즈 팩을 생성·보강합니다.
    (정답 ✅ 표시를 보기에서 숨겨 투표 참여율·댓글 토론·마스터클래스 본편 클릭률을 극대화합니다.)
    """
    COMMUNITY_PACK_JSON.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if COMMUNITY_PACK_JSON.exists():
        try:
            existing = json.loads(COMMUNITY_PACK_JSON.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    existing_ids = {x.get("post_id") for x in existing if isinstance(x, dict)}

    sub_url = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"
    curated_quizzes = [
        (
            "comm_quiz_04_ko",
            "[오늘의 5초 기하 보조선 퀴즈 #4 — 이등변삼각형 판정]",
            "❓ 삼각형 ABC에서 두 밑각 ∠B = ∠C 인 것만 알려져 있을 때, 두 변 AB = AC 임을 가장 직관적으로 증명하는 '단 1줄의 보조선'은 무엇일까요?\n\n"
            "먼저 보기를 골라 머릿속으로 합동인 두 삼각형을 그려본 뒤, 댓글로 번호를 남기고 아래 시각 증명 영상에서 정답을 확인해 보세요! 👇\n"
            "🎬 [1080p 질문하는 수학 수업 풀버전 바로 보기]:\n👉 https://www.youtube.com/watch?v=Xv9ELyzFqt0&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [매일 1분 공식 암기 없는 시각 증명 구독하기]:\n👉 {sub_url}",
            ["① 밑변 BC의 중점 M과 꼭짓점 A를 잇는 중선", "② 꼭짓점 A에서 밑변 BC에 내린 수선(또는 ∠A의 이등분선)", "③ 점 B를 지나고 변 AC에 평행한 반직선", "④ 보조선 없이 SAS 합동으로 바로 증명된다"],
        ),
        (
            "comm_quiz_05_ko",
            "[오늘의 5초 시각 증명 퀴즈 #5 — 피타고라스 나무와 넓이 보존]",
            "❓ 직각삼각형의 세 변 위에 정사각형을 계속 뻗어 나가는 '피타고라스 나무(Pythagoras Tree)'에서, 5단계에 생기는 작은 정사각형 32개의 넓이를 모두 더하면 맨 아래 기둥 정사각형 넓이(S)의 몇 배일까요?\n\n"
            "계산기 없이 눈으로 바로 깨치는 11단계 시각 증명 본편에서 정답을 확인하세요! 👇\n"
            "🎬 [피타고라스 나무 넓이 보존 1080p 시각 증명]:\n👉 https://www.youtube.com/watch?v=DSgUHigl82o&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [@min7014_ai 1초 무료 구독]:\n👉 {sub_url}",
            ["① 1/2 배 (절반으로 줄어든다)", "② 정확히 1배 (몇 단계를 올라가도 합은 항상 S로 일정하다)", "③ 2배", "④ 5배 (단계 수에 비례해 커진다)"],
        ),
        (
            "comm_quiz_06_en",
            "[5-Second Visual Geometry Challenge #6 — Menelaus' Theorem]",
            "❓ To prove Menelaus' Theorem on triangle ABC cut by a transversal line — WITHOUT memorizing messy ratio formulas — how many parallel auxiliary lines do you actually need to draw?\n\n"
            "Drop your guess in the comments, then watch the 20-step original visual proof! 👇\n"
            "🎬 [Full 1080p Menelaus Visual Proof & Marathon]:\n👉 https://www.youtube.com/watch?v=d0yl3hSHDgE&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [Subscribe for Daily Visual Math Proofs]:\n👉 {sub_url}",
            ["A) Just 1 parallel auxiliary line!", "B) 3 altitudes from the vertices", "C) The circumcircle of triangle ABC", "D) Coordinate axes & slope equations"],
        ),
        (
            "comm_quiz_07_ko",
            "[오늘의 5초 기하 직관 퀴즈 #7 — 원 밖의 점과 최대 거리]",
            "❓ 평면 위의 원 O와 원 밖의 한 점 P가 있습니다. 점 P에서 원 위의 점 Q까지 거리가 '최대'가 될 때, 선분 PQ는 반드시 어디를 지나야 할까요?\n\n"
            "삼각부등식 단 한 줄로 끝나는 시각 증명을 아래 정주행 강의에서 확인하세요! 👇\n"
            "🎬 [원의 성질 & 기하 정주행 마스터클래스 (1080p)]:\n👉 https://www.youtube.com/watch?v=_5LE_BfLA5w&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [@min7014_ai 구독하고 도형 감각 키우기]:\n👉 {sub_url}",
            ["① 원의 접점 T", "② 현의 수직이등분선 끝점", "③ 원의 중심 O를 지나는 직선과 원의 먼 쪽 교점", "④ 반지름의 길이에 따라 매번 달라진다"],
        ),
        (
            "comm_quiz_08_ko",
            "[오늘의 5초 대수·넓이 직관 퀴즈 #8 — 홀수의 합]",
            "❓ 1 + 3 + 5 + 7 + ··· + 19 (처음 10개의 연속된 홀수의 합)을 공식 암기 없이 '정사각형 타일 붙이기(ㄱ자 모양 Gnomon)'로 생각하면 1초 만에 얼마가 될까요?\n\n"
            "수식을 도형으로 번역하는 시각적 수학 증명 시리즈를 지금 만나보세요! 👇\n"
            "🎬 [전체 시각 증명 정주행 플레이리스트]:\n👉 https://www.youtube.com/watch?v=7RcvUpfGM6s&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [@min7014_ai 무료 구독]:\n👉 {sub_url}",
            ["① 81", "② 90", "③ 100 (= 10²)", "④ 110"],
        ),
        (
            "comm_quiz_09_en",
            "[5-Second Visual Proof Challenge #9 — Ceva's Theorem]",
            "❓ When proving Ceva's Theorem visually, converting each base segment ratio (BD / DC) into the ratio of which geometric quantity makes all three ratios telescope cleanly to 1?\n\n"
            "See the colorful 17-step area proof in 1080p! 👇\n"
            "🎬 [Ceva's Theorem 1080p Visual Proof]:\n👉 https://www.youtube.com/watch?v=aKmG-iKoieQ&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [Subscribe in 1 Click]:\n👉 {sub_url}",
            ["A) Inscribed angles", "B) Areas of triangles sharing the common Cevian point", "C) Perimeters of sub-triangles", "D) Tangents of vertex angles"],
        ),
        (
            "comm_quiz_10_ko",
            "[오늘의 5초 이차곡선 직관 퀴즈 #10 — 타원의 정의와 작도]",
            "❓ 두 초점 F, F'으로부터 거리의 합이 일정한 점들의 자취인 '타원' 위의 한 점 P를 컴퍼스와 자로 작도할 때, 가장 핵심이 되는 대칭·합동 도형은 무엇일까요?\n\n"
            "눈으로 따라가며 깨치는 기하 작도 & 이차곡선 마스터클래스에서 확인하세요! 👇\n"
            "🎬 [기하·벡터 심층 마스터클래스 바로 보기]:\n👉 https://www.youtube.com/watch?v=qZ53vyx90ig&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [@min7014_ai 구독하기]:\n👉 {sub_url}",
            ["① 수직이등분선 위에 생기는 이등변삼각형 (선분 길이 옮기기)", "② 정삼각형의 무게중심", "③ 직각이등변삼각형의 닮음", "④ 평행사변형의 넓이 이등분"],
        ),
        (
            "comm_quiz_11_ko",
            "[오늘의 5초 미적분·극한 오개념 퀴즈 #11 — 조각함수의 극한]",
            "❓ 함수 f(x)가 x ≠ a 일 때는 (x - a) + 3 이고, 딱 한 점 x = a 에서만 함숫값이 f(a) = 100 으로 정의되어 있다면, lim(x→a) f(x) 의 극한값은 얼마일까요?\n\n"
            "90%의 학생이 헷갈리는 '함숫값 f(a)'과 '극한값 lim f(x)'의 차이를 시각 그래프로 확인하세요! 👇\n"
            "🎬 [방정식·함수·극한 오리지널 PDF 마스터클래스]:\n👉 https://www.youtube.com/watch?v=IXQnXURMQ7g&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [@min7014_ai 1초 구독]:\n👉 {sub_url}",
            ["① 3 (x가 a에 한없이 가까워질 뿐 a는 아니므로)", "② 100 (x = a에서의 함숫값)", "③ 103", "④ 극한값이 존재하지 않는다"],
        ),
        (
            "comm_quiz_12_ko",
            "[오늘의 5초 원의 성질 퀴즈 #12 — 두 현의 교점과 할선의 곱]",
            "❓ 원 내부에서 두 현 AB와 CD가 점 P에서 만날 때, PA × PB = PC × PD 가 항상 성립하는 이유를 증명하는 가장 빠른 열쇠는 무엇일까요?\n\n"
            "보조선 2줄로 드러나는 숨은 닮음 삼각형을 직접 눈으로 확인해 보세요! 👇\n"
            "🎬 [원의 성질 & 시각 증명 정주행 (1080p)]:\n👉 https://www.youtube.com/watch?v=_5LE_BfLA5w&list=UUSlqQfOEtRfJuMPyGMLgFYA\n"
            f"🔔 [@min7014_ai 무료 구독하기]:\n👉 {sub_url}",
            ["① 같은 호에 대한 원주각의 크기가 같음 (AA 닮음)", "② 피타고라스 정리 4번 연립", "③ 삼각형의 중선 정리(파푸스 정리)", "④ 원의 넓이 공식 πr²"],
        ),
    ]

    changed = False
    for pid, title, text, opts in curated_quizzes:
        if pid not in existing_ids:
            existing.append({
                "post_id": pid,
                "type": "QUIZ_POLL_EN" if pid.endswith("_en") else "QUIZ_POLL_KO",
                "title": title,
                "post_text": text,
                "poll_options": opts,
            })
            changed = True

    if changed:
        COMMUNITY_PACK_JSON.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return existing


def check_robot_session_logged_in() -> bool:
    """전용 로봇 프로필(.yt_chrome_robot_profile)이 @min7014_ai 구글 계정에 로그인되어 있는지 확인합니다."""
    from playwright.sync_api import sync_playwright

    if not _acquire_robot_lock():
        return True
    try:
        with sync_playwright() as p:
            ctx = _launch_robot_context(p, headless=True)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto(CHANNEL_POSTS_URL, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3000)
            has_box = page.locator("#placeholder-area, ytd-backstage-post-dialog-renderer").count() > 0
            ctx.close()
            return has_box
    except Exception:
        return False
    finally:
        _release_robot_lock()


def _load_related_linked_state() -> dict:
    st = {"linked_short_ids": ["9L_15T8bzS8"], "last_run_ts": 0.0}
    if RELATED_LINKED_STATE_FILE.exists():
        try:
            d = json.loads(RELATED_LINKED_STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(d.get("linked_short_ids"), list):
                merged = list(dict.fromkeys(["9L_15T8bzS8"] + d["linked_short_ids"]))
                d["linked_short_ids"] = merged
                return d
        except Exception:
            pass
    return st


def _save_related_linked_state(st: dict) -> None:
    RELATED_LINKED_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    RELATED_LINKED_STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def _collect_unlinked_live_shorts_candidates(already_linked: set[str]) -> list[dict]:
    import min7014_video_maker as vm

    hot_keywords = (
        "이등변", "피타고라스", "원주각", "접선", "메넬라우스", "체바", "닮음", "외심", "내심", "무게중심",
        "포물선", "타원", "쌍곡선", "삼수선", "극한", "미분", "정적분", "수열", "부등식", "벡터",
    )
    cands = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        try:
            d = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        raw_t = str(d.get("title") or "")
        ko_t, en_t = vm.split_bilingual_title(raw_t)
        clean_ko = vm.latex_to_unicode_title(ko_t or raw_t).strip()
        clean_en = vm.latex_to_unicode_title(str(d.get("title_en") or en_t or ko_t)).strip()
        is_hot = 1 if any(hk in clean_ko for hk in hot_keywords) else 0

        yu = d.get("youtube_urls") or {}
        qyu = d.get("question_youtube_urls") or {}

        for field_name, is_q_short in (("question_shorts_urls", 1), ("shorts_urls", 0)):
            su = d.get(field_name) or {}
            for lc in ("ko", "en"):
                s_url = str(su.get(lc) or "").strip()
                if not s_url:
                    continue
                m = re.search(r"(?:shorts/|youtu\.be/|v=)([A-Za-z0-9_-]{11})", s_url)
                if not m:
                    continue
                short_id = m.group(1)
                if short_id in already_linked:
                    continue
                has_exact_long = 1 if (str(yu.get(lc) or "").strip() or str(qyu.get(lc) or "").strip()) else 0
                search_q = (clean_ko[:18] if lc == "ko" else clean_en[:24]).strip()
                fallback_q = "마스터클래스" if lc == "ko" else "Masterclass"
                cands.append({
                    "priority": (is_q_short, is_hot, has_exact_long, 1 if lc == "ko" else 0),
                    "slug": sp.stem,
                    "lang": lc,
                    "short_id": short_id,
                    "search_query": search_q,
                    "fallback_query": fallback_q,
                    "clean_title": clean_ko if lc == "ko" else clean_en,
                })

    cands.sort(key=lambda x: (-x["priority"][0], -x["priority"][1], -x["priority"][2], -x["priority"][3], x["slug"]))
    return cands


def link_shorts_related_videos_in_studio(max_links: int = 8, headless: bool = True) -> dict:
    """
    [0-Quota YouTube Studio 직결]
    라이브 #Shorts 및 Q-#Shorts에 스튜디오 전용 '관련 동영상(Related Video)'을 자동 연결하여
    모바일 쇼츠 시청자를 1080p 본편 및 25분+ 마스터클래스(4,000시간 트랙)로 즉시 유입시킵니다.
    """
    from playwright.sync_api import sync_playwright

    st = _load_related_linked_state()
    linked_set = set(st.get("linked_short_ids") or [])
    cands = _collect_unlinked_live_shorts_candidates(linked_set)
    if not cands:
        return {"ok": True, "linked_now": 0, "total_linked": len(linked_set), "remaining": 0}

    if not _acquire_robot_lock():
        return {"ok": False, "reason": "robot_browser_busy", "linked_now": 0, "total_linked": len(linked_set)}

    linked_now = 0
    already_had = 0
    details = []
    try:
        with sync_playwright() as p:
            ctx = _launch_robot_context(p, headless=headless)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            for item in cands[: max(1, int(max_links))]:
                sid = item["short_id"]
                try:
                    page.goto(f"https://studio.youtube.com/video/{sid}/edit", wait_until="domcontentloaded", timeout=35000)
                    page.wait_for_timeout(4800)

                    trig = page.locator("ytcp-dropdown-trigger").filter(has_text=re.compile(r"관련 동영상|Related video", re.I)).first
                    if trig.count() == 0:
                        continue
                    cur_txt = trig.inner_text()
                    if ("없음" not in cur_txt) and ("None" not in cur_txt):
                        linked_set.add(sid)
                        already_had += 1
                        continue

                    trig.scroll_into_view_if_needed()
                    trig.click()
                    page.wait_for_timeout(2200)

                    s_in = page.locator("ytcp-video-pick-dialog input#search-yours").first
                    if s_in.count() == 0:
                        page.keyboard.press("Escape")
                        continue

                    picked_ok = False
                    for q_str in (item["search_query"], item["fallback_query"]):
                        if not q_str:
                            continue
                        s_in.click()
                        s_in.fill(q_str)
                        page.wait_for_timeout(2600)
                        long_cards = page.locator("ytcp-video-pick-dialog ytcp-entity-card").filter(has_not_text="#Shorts")
                        if long_cards.count() > 0:
                            chosen_title = long_cards.first.inner_text().splitlines()[0][:70]
                            long_cards.first.click()
                            page.wait_for_timeout(2000)
                            picked_ok = True
                            break

                    if picked_ok:
                        save_btn = page.locator("#save").first
                        if save_btn.count() > 0 and save_btn.get_attribute("aria-disabled") != "true":
                            save_btn.click()
                            page.wait_for_timeout(3800)
                        linked_set.add(sid)
                        linked_now += 1
                        details.append({"short_id": sid, "slug": item["slug"], "linked_to": chosen_title})
                    else:
                        page.keyboard.press("Escape")
                        page.wait_for_timeout(800)
                except Exception:
                    continue

            ctx.close()
    except Exception as e:
        return {"ok": False, "reason": str(e), "linked_now": linked_now, "total_linked": len(linked_set)}
    finally:
        st["linked_short_ids"] = sorted(linked_set)
        st["last_run_ts"] = time.time()
        _save_related_linked_state(st)
        _release_robot_lock()

    rem = max(0, len(cands) - (linked_now + already_had))
    return {
        "ok": True,
        "linked_now": linked_now,
        "already_linked_verified": already_had,
        "total_linked": len(linked_set),
        "remaining_unlinked": rem,
        "details": details,
    }


def publish_next_community_post_directly(headless: bool = True, min_interval_sec: int = 0) -> dict:
    """
    .yt_chrome_robot_profile 세션을 통해 https://www.youtube.com/@min7014_ai/posts 에 접속하여
    오리지널 수학자료실(https://min7014.github.io/) 5초 직관 퀴즈 및 정주행 마스터클래스 직결 게시물을 자동 발행합니다.
    """
    from playwright.sync_api import sync_playwright

    packs = ensure_socratic_community_quiz_packs()
    state = {"published_ids": ["comm_quiz_01_ko", "comm_quiz_02_en", "comm_quiz_03_ko"], "last_published_ts": 0.0}
    if COMMUNITY_STATE_JSON.exists():
        try:
            state.update(json.loads(COMMUNITY_STATE_JSON.read_text(encoding="utf-8")))
        except Exception:
            pass

    now_ts = time.time()
    if min_interval_sec > 0 and (now_ts - float(state.get("last_published_ts") or 0.0)) < min_interval_sec:
        return {"ok": True, "status": "interval_wait", "published_count": len(state.get("published_ids") or [])}

    pub_set = set(state.get("published_ids") or [])
    target_post = None
    for pk in packs:
        if pk.get("post_id") not in pub_set:
            target_post = pk
            break
    if target_post is None:
        return {"ok": True, "status": "all_current_packs_published", "published_count": len(pub_set)}

    if not _acquire_robot_lock():
        return {"ok": False, "reason": "robot_browser_busy"}

    try:
        with sync_playwright() as p:
            ctx = _launch_robot_context(p, headless=headless)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto(CHANNEL_POSTS_URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(4200)

            if page.locator("#placeholder-area").count() == 0:
                ctx.close()
                return {"ok": False, "reason": "placeholder_area_not_found"}

            page.locator("#placeholder-area").first.click()
            page.wait_for_timeout(1500)
            ce = page.locator("#contenteditable-root").first
            ce.click()
            clean_opts = [re.sub(r"\s*✅\s*", "", o).strip() for o in target_post.get("poll_options", [])]
            full_text = target_post["post_text"] + "\n\n[보기 중 정답 번호를 댓글로 먼저 남겨보세요! 👇]\n" + "\n".join(clean_opts)
            page.keyboard.insert_text(full_text)
            page.wait_for_timeout(1800)

            page.locator("#submit-button button").first.click()
            page.wait_for_timeout(5000)

            shot_p = ROOT_DIR / "youtube_uploads" / "community_posts" / f"published_{target_post['post_id']}.png"
            page.screenshot(path=str(shot_p))
            total_posts_on_page = page.locator("ytd-backstage-post-thread-renderer").count()

            pub_set.add(target_post["post_id"])
            state["published_ids"] = sorted(pub_set)
            state["last_published_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            state["last_published_ts"] = time.time()
            COMMUNITY_STATE_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            ctx.close()
            return {
                "ok": True,
                "post_id": target_post["post_id"],
                "title": target_post.get("title"),
                "total_posts_on_channel": total_posts_on_page,
            }
    except Exception as e:
        return {"ok": False, "reason": str(e)}
    finally:
        _release_robot_lock()


def run_zero_quota_studio_growth_cycle(max_related_links: int = 6, allow_community_post: bool = True) -> dict:
    """
    24/7 데몬 및 Finance 엔진이 YouTube API 쿼터 소모 0으로 실행하는 스튜디오 성장 사이클:
      1) 최소 90분 간격으로 미연결 쇼츠 최대 max_related_links편에 '관련 동영상(1080p/마스터클래스)' 자동 바인딩
      2) 최소 12시간(43,200초) 간격으로 커뮤니티 탭에 신규 소크라테스 5초 수학 퀴즈 1건 발행
    """
    st = _load_related_linked_state()
    now_ts = time.time()
    rel_res = {"skipped": "cooldown"}
    if (now_ts - float(st.get("last_run_ts") or 0.0)) >= 5400:
        rel_res = link_shorts_related_videos_in_studio(max_links=max_related_links, headless=True)

    comm_res = {"skipped": "disabled"}
    if allow_community_post:
        comm_res = publish_next_community_post_directly(headless=True, min_interval_sec=43200)

    return {"related_links": rel_res, "community_post": comm_res}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--post-community", action="store_true")
    parser.add_argument("--link-shorts", type=int, default=0, help="Link up to N Shorts to 1080p/Masterclasses in Studio")
    args = parser.parse_args()

    if args.link_shorts > 0:
        res_l = link_shorts_related_videos_in_studio(max_links=args.link_shorts, headless=True)
        print(json.dumps(res_l, ensure_ascii=False, indent=2))
    if args.post_community:
        res_c = publish_next_community_post_directly(headless=True, min_interval_sec=0)
        print(json.dumps(res_c, ensure_ascii=False, indent=2))
    if not args.link_shorts and not args.post_community:
        st_l = _load_related_linked_state()
        ensure_socratic_community_quiz_packs()
        print(json.dumps({
            "robot_logged_in": check_robot_session_logged_in(),
            "linked_shorts_count": len(st_l.get("linked_short_ids") or []),
            "unlinked_shorts_remaining": len(_collect_unlinked_live_shorts_candidates(set(st_l.get("linked_short_ids") or []))),
        }, ensure_ascii=False, indent=2))
