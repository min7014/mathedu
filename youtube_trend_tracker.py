import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import json
import re
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
TREND_FILE = ROOT_DIR / "youtube_uploads" / "strategy_v2_trend_history.json"
STUDIO_SCRAPE_STATE = ROOT_DIR / ".agents" / "studio_kpi_scrape_state.json"
STUDIO_SCRAPE_INTERVAL_SEC = 21600  # 6시간 간격 0-쿼터 Studio KPI 자동 갱신

BASELINE_V2 = {
    "label": "Strategy v2.0 Launch Baseline (2026-11-14 10:55 KST)",
    "timestamp": "2026-11-14T10:55:00+09:00",
    "public_videos": 455,
    "total_views_api": 6638,
    "subscribers": 8,
    "sub_conversion_pct": 0.12,
    "studio_watch_hours": 1.0,
    "studio_valid_shorts_views": 540,
    "studio_shorts_stay_pct": 14.6,
    "studio_shorts_swipe_pct": 85.4,
    "studio_search_pct": 23.0,
    "studio_browse_pct": 0.2,
    "related_shorts_linked": 73,
    "community_quizzes": 5,
    "post_v2_videos_count": 0,
    "post_v2_avg_views": 0.0,
}


def load_trend_history() -> dict:
    if TREND_FILE.exists():
        try:
            data = json.loads(TREND_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "baseline" in data:
                return data
        except Exception:
            pass
    init_doc = {
        "baseline": BASELINE_V2,
        "snapshots": [dict(BASELINE_V2)],
    }
    TREND_FILE.parent.mkdir(parents=True, exist_ok=True)
    TREND_FILE.write_text(json.dumps(init_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return init_doc


def _scrape_studio_kpis_headless() -> dict:
    """API 쿼터 0으로 YouTube Studio [수익 창출] 및 [채널 분석] 실측 지표를 수집합니다."""
    res = {}
    ycc = None
    acquired = False
    try:
        import youtube_community_controller as ycc
        from playwright.sync_api import sync_playwright

        acquired = bool(ycc._acquire_robot_lock())
        if not acquired:
            return res

        channel_id = "UCSlqQfOEtRfJuMPyGMLgFYA"
        with sync_playwright() as p:
            ctx = ycc._launch_robot_context(p, headless=True)
            try:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(f"https://studio.youtube.com/channel/{channel_id}/monetization", wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(3500)
                earn_txt = page.inner_text("body")
                m_wh = re.search(
                    r"(?:유효 공개 시청 시간\s*([\d,\.]+)\s*시간|([\d,\.]+)\s*valid public watch hours)",
                    earn_txt,
                    re.IGNORECASE,
                )
                if m_wh:
                    raw_wh = (m_wh.group(1) or m_wh.group(2) or "0").replace(",", "")
                    res["studio_watch_hours"] = float(raw_wh)

                m_sv = re.search(
                    r"(?:유효 공개 Shorts 조회수\s*([\d,\.]+)\s*(만|천)?\s*회|([\d,\.]+)\s*([KM])?\s*valid public Shorts views)",
                    earn_txt,
                    re.IGNORECASE,
                )
                if m_sv:
                    raw_sv = (m_sv.group(1) or m_sv.group(3) or "0").replace(",", "")
                    unit = (m_sv.group(2) or m_sv.group(4) or "").upper()
                    val = float(raw_sv)
                    if unit == "만":
                        val *= 10000
                    elif unit in ("천", "K"):
                        val *= 1000
                    elif unit == "M":
                        val *= 1000000
                    res["studio_valid_shorts_views"] = int(val)

                page.goto(f"https://studio.youtube.com/channel/{channel_id}/analytics/tab-reach_viewers/period-default", wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(3500)
                reach_txt = page.inner_text("body")
                m_stay = re.search(r"(?:계속 시청함|Viewed|Stayed to watch)\s*([\d\.]+)%", reach_txt, re.IGNORECASE)
                if m_stay:
                    stay = float(m_stay.group(1))
                    res["studio_shorts_stay_pct"] = stay
                    res["studio_shorts_swipe_pct"] = round(100.0 - stay, 1)
                m_srch = re.search(r"(?:YouTube 검색|YouTube search)\s*([\d\.]+)%", reach_txt, re.IGNORECASE)
                if m_srch:
                    res["studio_search_pct"] = float(m_srch.group(1))
                m_brw = re.search(r"(?:탐색 기능|Browse features)\s*([\d\.]+)%", reach_txt, re.IGNORECASE)
                if m_brw:
                    res["studio_browse_pct"] = float(m_brw.group(1))
            finally:
                ctx.close()
    except Exception:
        pass
    finally:
        if acquired and ycc is not None:
            ycc._release_robot_lock()
    return res


def capture_trend_snapshot(include_studio: bool = False) -> dict:
    hist = load_trend_history()
    prev = hist["snapshots"][-1] if hist.get("snapshots") else BASELINE_V2

    rel_p = ROOT_DIR / ".agents" / "studio_shorts_related_linked.json"
    rel_cnt = len((json.loads(rel_p.read_text(encoding="utf-8")).get("linked_short_ids") or [])) if rel_p.exists() else prev.get("related_shorts_linked", 73)
    comm_p = ROOT_DIR / "youtube_uploads" / "community_posts" / "published_community_state.json"
    comm_cnt = len((json.loads(comm_p.read_text(encoding="utf-8")).get("published_ids") or [])) if comm_p.exists() else prev.get("community_quizzes", 5)
    exam_hyb_cnt = len(list((ROOT_DIR / "youtube_uploads" / "exam_hybrid").glob("*_exam_*.mp4")))

    pub_v = int(prev.get("public_videos", 455))
    views = int(prev.get("total_views_api", 6638))
    subs = int(prev.get("subscribers", 8))
    post_v2_cnt = int(prev.get("post_v2_videos_count", 0))
    post_v2_avg = float(prev.get("post_v2_avg_views", 0.0))

    try:
        import min7014_video_maker as vm
        yt, _ = vm.get_youtube_readonly_service()
        if yt is None:
            yt, _ = vm.get_available_youtube_upload_service()
        if yt is not None:
            ch_resp = yt.channels().list(part="id,statistics,contentDetails", id="UCSlqQfOEtRfJuMPyGMLgFYA").execute()
            if ch_resp.get("items"):
                ch = ch_resp["items"][0]
                st = ch.get("statistics", {})
                pub_v = int(st.get("videoCount", pub_v))
                views = int(st.get("viewCount", views))
                subs = int(st.get("subscriberCount", subs))
                uploads_pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
                pl_items = yt.playlistItems().list(part="snippet,contentDetails", playlistId=uploads_pl, maxResults=35).execute().get("items", [])
                v2_ids = [
                    it["contentDetails"]["videoId"]
                    for it in pl_items
                    if str(it["snippet"].get("publishedAt") or "") >= "2026-11-14T01:55:00Z"
                ]
                if v2_ids:
                    v_resp = yt.videos().list(part="statistics", id=",".join(v2_ids)).execute().get("items", [])
                    v_views = [int((x.get("statistics") or {}).get("viewCount", 0)) for x in v_resp]
                    post_v2_cnt = len(v_views)
                    post_v2_avg = round(sum(v_views) / max(1, len(v_views)), 1)
    except Exception:
        pass

    snap = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "public_videos": pub_v,
        "total_views_api": views,
        "subscribers": subs,
        "sub_conversion_pct": round((subs / max(1, views)) * 100.0, 3),
        "studio_watch_hours": prev.get("studio_watch_hours", 1.0),
        "studio_valid_shorts_views": prev.get("studio_valid_shorts_views", 540),
        "studio_shorts_stay_pct": prev.get("studio_shorts_stay_pct", 14.6),
        "studio_shorts_swipe_pct": prev.get("studio_shorts_swipe_pct", 85.4),
        "studio_search_pct": prev.get("studio_search_pct", 23.0),
        "studio_browse_pct": prev.get("studio_browse_pct", 0.2),
        "related_shorts_linked": rel_cnt,
        "community_quizzes": comm_cnt,
        "exam_hybrid_mp4_ready": exam_hyb_cnt,
        "post_v2_videos_count": post_v2_cnt,
        "post_v2_avg_views": post_v2_avg,
    }

    now_ts = datetime.now().timestamp()
    scrape_state = {}
    if STUDIO_SCRAPE_STATE.exists():
        try:
            scrape_state = json.loads(STUDIO_SCRAPE_STATE.read_text(encoding="utf-8"))
        except Exception:
            scrape_state = {}
    last_scrape_ts = float(scrape_state.get("last_attempt_ts") or 0.0)
    due_for_6h_scrape = (now_ts - last_scrape_ts) >= STUDIO_SCRAPE_INTERVAL_SEC

    st_kpis = {}
    if include_studio or due_for_6h_scrape:
        scrape_state["last_attempt_ts"] = now_ts
        STUDIO_SCRAPE_STATE.parent.mkdir(parents=True, exist_ok=True)
        STUDIO_SCRAPE_STATE.write_text(json.dumps(scrape_state, ensure_ascii=False, indent=2), encoding="utf-8")
        st_kpis = _scrape_studio_kpis_headless()
        if st_kpis:
            snap.update(st_kpis)
            scrape_state["last_success_ts"] = now_ts
            scrape_state["last_kpis"] = st_kpis
            STUDIO_SCRAPE_STATE.write_text(json.dumps(scrape_state, ensure_ascii=False, indent=2), encoding="utf-8")

    # 스냅샷 누적 저장 (최소 15분 간격 또는 수치 변동 시 추가, 최근 120개 보존)
    snapshots = hist.setdefault("snapshots", [])
    if len(snapshots) <= 1 or snap["total_views_api"] != prev.get("total_views_api") or snap["subscribers"] != prev.get("subscribers") or bool(st_kpis):
        snapshots.append(snap)
        hist["snapshots"] = snapshots[-120:]
    else:
        snapshots[-1] = snap
    TREND_FILE.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")
    return snap


def format_trend_report(include_studio: bool = False) -> str:
    hist = load_trend_history()
    base = hist["baseline"]
    cur = capture_trend_snapshot(include_studio=include_studio)

    d_views = cur["total_views_api"] - base["total_views_api"]
    d_subs = cur["subscribers"] - base["subscribers"]
    d_vids = cur["public_videos"] - base["public_videos"]
    d_wh = round(cur["studio_watch_hours"] - base["studio_watch_hours"], 1)
    d_stay = round(cur["studio_shorts_stay_pct"] - base["studio_shorts_stay_pct"], 1)
    d_rel = cur["related_shorts_linked"] - base["related_shorts_linked"]
    d_comm = cur["community_quizzes"] - base["community_quizzes"]

    extra_evo = ""
    roi_line = ""
    try:
        import youtube_self_evolving_engine as ysee
        roi = ysee.evaluate_ai_subscription_roi_gate(
            subscribers=int(cur["subscribers"]),
            watch_hours=float(cur["studio_watch_hours"]),
            valid_shorts_views=int(cur["studio_valid_shorts_views"]),
        )
        roi_line = f"\n{roi['verdict_badge']}"
        cw_p = ROOT_DIR / "youtube_uploads" / "self_evolving_cluster_weights.json"
        pl_p = ROOT_DIR / ".agents" / "playlist_synced_state.json"
        loc_p = ROOT_DIR / ".agents" / "localized_videos_state.json"
        top_c = ", ".join((json.loads(cw_p.read_text(encoding="utf-8")).get("top_3_clusters") or [])[:3]) if cw_p.exists() else "-"
        pl_cnt = len((json.loads(pl_p.read_text(encoding="utf-8")).get("added_pairs") or [])) if pl_p.exists() else 0
        loc_cnt = len((json.loads(loc_p.read_text(encoding="utf-8")).get("localized_ids") or [])) if loc_p.exists() else 0
        extra_evo = f"\n• v3.0 자율진화: 인기 단원 1~3위[{top_c}] | 정주행 재생목록 편입 {pl_cnt}편 | 6개국어 글로벌 현지화 {loc_cnt}편"
    except Exception:
        pass

    return (
        "📈 [@min7014_ai 전략 v2.0➔v3.0 전면 가동 추이 리포트 (기준점: 11/14 10:55 KST)]\n"
        f"• 구독자: {base['subscribers']}명 ➔ {cur['subscribers']}명 ({d_subs:+d}명 | 전환율 {cur['sub_conversion_pct']:.2f}%)\n"
        f"• 총 조회수: {base['total_views_api']:,}회 ➔ {cur['total_views_api']:,}회 ({d_views:+,}회)\n"
        f"• 공개 영상: {base['public_videos']}편 ➔ {cur['public_videos']}편 ({d_vids:+d}편)\n"
        f"• 스튜디오 유효 시청시간: {base['studio_watch_hours']}h ➔ {cur['studio_watch_hours']}h ({d_wh:+.1f}h / 목표 3,000h)\n"
        f"• 쇼츠 계속 시청함(핵심!): {base['studio_shorts_stay_pct']}% ➔ {cur['studio_shorts_stay_pct']}% ({d_stay:+.1f}%p / 목표 55%+)\n"
        f"• 유입 구조: 검색 {cur['studio_search_pct']}% | 탐색(홈 추천) {cur['studio_browse_pct']}%\n"
        f"• v2.0 이후 신규 업로드 코호트: {cur['post_v2_videos_count']}편 (편당 평균 {cur['post_v2_avg_views']}뷰)\n"
        f"• 퍼널 가동 현황: 본편 연결 쇼츠 {cur['related_shorts_linked']}편({d_rel:+d}) | 커뮤니티 퀴즈 {cur['community_quizzes']}건({d_comm:+d}) | 실전함정 하이브리드 준비 {cur.get('exam_hybrid_mp4_ready', 0)}편"
        f"{extra_evo}{roi_line}"
    )


if __name__ == "__main__":
    import sys
    deep = "--studio" in sys.argv
    print(format_trend_report(include_studio=deep))
