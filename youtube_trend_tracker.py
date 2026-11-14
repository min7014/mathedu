import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import json
import re
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
TREND_FILE = ROOT_DIR / "youtube_uploads" / "strategy_v2_trend_history.json"

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
    try:
        import youtube_community_controller as ycc
        from playwright.sync_api import sync_playwright

        channel_id = "UCSlqQfOEtRfJuMPyGMLgFYA"
        with sync_playwright() as p:
            ctx = ycc._launch_studio_context(p, headless=True)
            try:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(f"https://studio.youtube.com/channel/{channel_id}/monetization", wait_until="domcontentloaded", timeout=35000)
                page.wait_for_timeout(4500)
                earn_txt = page.inner_text("body")
                m_wh = re.search(r"유효 공개 시청 시간\s*([\d,\.]+)\s*시간", earn_txt)
                if m_wh:
                    res["studio_watch_hours"] = float(m_wh.group(1).replace(",", ""))
                m_sv = re.search(r"유효 공개 Shorts 조회수\s*([\d,\.]+)\s*(만|천)?\s*회", earn_txt)
                if m_sv:
                    val = float(m_sv.group(1).replace(",", ""))
                    unit = m_sv.group(2) or ""
                    if unit == "만":
                        val *= 10000
                    elif unit == "천":
                        val *= 1000
                    res["studio_valid_shorts_views"] = int(val)

                page.goto(f"https://studio.youtube.com/channel/{channel_id}/analytics/tab-reach_viewers/period-default", wait_until="domcontentloaded", timeout=35000)
                page.wait_for_timeout(5000)
                reach_txt = page.inner_text("body")
                m_stay = re.search(r"계속 시청함\s*([\d\.]+)%", reach_txt)
                if m_stay:
                    stay = float(m_stay.group(1))
                    res["studio_shorts_stay_pct"] = stay
                    res["studio_shorts_swipe_pct"] = round(100.0 - stay, 1)
                m_srch = re.search(r"YouTube 검색\s*([\d\.]+)%", reach_txt)
                if m_srch:
                    res["studio_search_pct"] = float(m_srch.group(1))
                m_brw = re.search(r"탐색 기능\s*([\d\.]+)%", reach_txt)
                if m_brw:
                    res["studio_browse_pct"] = float(m_brw.group(1))
            finally:
                ctx.close()
    except Exception:
        pass
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
        yt, _ = vm.get_available_youtube_upload_service()
        if yt is not None:
            ch = yt.channels().list(part="statistics,contentDetails", mine=True).execute()["items"][0]
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

    if include_studio:
        st_kpis = _scrape_studio_kpis_headless()
        snap.update(st_kpis)

    # 스냅샷 누적 저장 (최소 15분 간격 또는 수치 변동 시 추가, 최근 120개 보존)
    snapshots = hist.setdefault("snapshots", [])
    if len(snapshots) <= 1 or snap["total_views_api"] != prev.get("total_views_api") or snap["subscribers"] != prev.get("subscribers") or include_studio:
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

    return (
        "📈 [@min7014_ai 전략 v2.0 전면 적용 추이 리포트 (기준점: 11/14 10:55 KST)]\n"
        f"• 구독자: {base['subscribers']}명 ➔ {cur['subscribers']}명 ({d_subs:+d}명 | 전환율 {cur['sub_conversion_pct']:.2f}%)\n"
        f"• 총 조회수: {base['total_views_api']:,}회 ➔ {cur['total_views_api']:,}회 ({d_views:+,}회)\n"
        f"• 공개 영상: {base['public_videos']}편 ➔ {cur['public_videos']}편 ({d_vids:+d}편)\n"
        f"• 스튜디오 유효 시청시간: {base['studio_watch_hours']}h ➔ {cur['studio_watch_hours']}h ({d_wh:+.1f}h / 목표 3,000h)\n"
        f"• 쇼츠 계속 시청함(핵심!): {base['studio_shorts_stay_pct']}% ➔ {cur['studio_shorts_stay_pct']}% ({d_stay:+.1f}%p / 목표 55%+)\n"
        f"• 유입 구조: 검색 {cur['studio_search_pct']}% | 탐색(홈 추천) {cur['studio_browse_pct']}%\n"
        f"• v2.0 이후 신규 업로드 코호트: {cur['post_v2_videos_count']}편 (편당 평균 {cur['post_v2_avg_views']}뷰)\n"
        f"• 퍼널 가동 현황: 본편 연결 쇼츠 {cur['related_shorts_linked']}편({d_rel:+d}) | 커뮤니티 퀴즈 {cur['community_quizzes']}건({d_comm:+d}) | 실전함정 하이브리드 준비 {cur.get('exam_hybrid_mp4_ready', 0)}편"
    )


if __name__ == "__main__":
    import sys
    deep = "--studio" in sys.argv
    print(format_trend_report(include_studio=deep))
