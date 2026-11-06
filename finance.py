#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finance.py — mathedu & @min7014_ai 수석 광고 수익화 디렉터 에이전트 (Chief EdTech Ad Revenue Director v2.0)
===========================================================================================================
목표: 민은기 선생님의 수학자료실(min7014.github.io) 1,113개 시각적 증명 자산과 @min7014_ai 유튜브 채널,
      그리고 mathedu 수학홈페이지(16,548문항)를 결합하여 **월 1,000만 원(연 1.2억 원) 이상의 순수 교육 광고 수익**을
      창출하는 전담 에이전트입니다. (학생과 교사에게는 100% 무료 학습 환경 보장)

[4대 에이전트 수익화 연합 체계]
  1. 💼 finance (총괄 지휘): 월 1,000만 원 수익 로드맵, 고단가(High-RPM) 한/영 키워드 최적화, 8분+ 미드롤(Mid-Roll) 마스터클래스 기획, 웹 애드센스/애드핏 통합 관제
  2. 🎬 Video_Creator (생산 엔진): 1,113개 주제 × 4대 에디션(일반 본편 · 질문수업 본편 · 일반 #Shorts · 질문 #Shorts) × KO/EN 초고화질 영상 무중단 제작·업로드
  3. 📣 pr (트래픽 증폭 엔진): 유튜브 고정댓글 5단 퍼널, 7대 채널 커뮤니티 확산, Google/Naver SEO 및 AI 검색엔진(llms.txt) 유입 극대화
  4. 👩‍🏫 mathteacher (품질 보증 엔진): 100% 수학적 무결성 검수 및 질문하는 수업 발문 설계로 시청 지속 시간(AVD)과 구독 전환율 극대화

CLI 실행:
  python -X utf8 finance.py status
  python -X utf8 finance.py optimize
  python -X utf8 finance.py verify
  python -X utf8 finance.py set-adsense --client ca-pub-XXXXXXXXXXXXXXXX --slot 1234567890
  python -X utf8 finance.py set-adfit --unit DAN-XXXXXXXXXXXXXXXX
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
CATALOG_JSON = ROOT_DIR / "video_lectures" / "catalog.json"
VAULT_JSON = ROOT_DIR / "video_lectures" / "vault_index.json"
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
YT_PKG_DIR = ROOT_DIR / "video_lectures" / "youtube_packages"
YT_UPLOADS_DIR = ROOT_DIR / "youtube_uploads"
QUESTION_DIR = ROOT_DIR / "video_lectures" / "question_classroom"
SHORTS_DIR = ROOT_DIR / "video_lectures" / "shorts"
AD_CONFIG_JSON = ROOT_DIR / "ad_config.json"
ADS_TXT = ROOT_DIR / "ads.txt"
FINANCE_ENGINE_JSON = ROOT_DIR / "assets" / "finance_revenue_engine.json"

MONTHLY_REVENUE_TARGET_KRW = 10_000_000

# 교육 카테고리 고단가(High-CPM/RPM) 타겟 키워드 (한국 수능/학부모 + 북미/영국/호주 Tier-1 EdTech)
HIGH_RPM_KEYWORDS_KO = [
    "수능수학", "수학개념원리", "기하학증명", "수학공부법", "고등수학",
    "중등수학", "시각적증명", "수학강의", "창의사고력수학", "수능킬러문항",
]
HIGH_RPM_KEYWORDS_EN = [
    "SAT Math Prep", "AP Calculus", "AMC Math", "Euclidean Geometry Proof",
    "Visual Math Proof", "STEM Education", "Interactive Geometry", "3Blue1Brown Style",
    "Math Olympiad", "High School Geometry",
]


def _purge_non_math_tutorial_topics() -> list:
    """
    '민은기 선생님' 개인 호칭이 제목에 들어있거나 순수 수학 개념이 아닌 소프트웨어 사용법(체크박스자동화 등)
    스크립트/패키지를 카탈로그에서 즉시 정리하여 채널의 순수 수학 전문성과 알고리즘 타겟팅을 보호합니다.
    """
    removed = []
    bad_slugs = {
        "math20190921002", "math20191102002", "math20191001002",
        "math20190918001", "math20190914001", "math20190914002", "math20190912002",
        "math20190810021",
    }
    for sp in list(SCRIPTS_DIR.glob("*.json")):
        slug = sp.stem
        try:
            txt = sp.read_text(encoding="utf-8")
            sdoc = json.loads(txt)
        except Exception:
            continue
        t_ko = str(sdoc.get("title") or "")
        if slug in bad_slugs or any(k in t_ko for k in ("체크박스", "원노트", "학습자료 링크", "이벤트 만들기", "텍스트 만들기", "민은기")):
            try:
                sp.unlink(missing_ok=True)
                removed.append(slug)
            except Exception:
                pass
            for pkg_f in YT_PKG_DIR.glob(f"{slug}*"):
                try:
                    pkg_f.unlink(missing_ok=True)
                except Exception:
                    pass
    return removed


def analyze_revenue_pipeline() -> dict:
    """
    @min7014_ai 유튜브 채널 + mathedu 수학홈페이지의 4대 에디션 자산 현황과
    월 1,000만 원 수익 달성 3-Track 파이프라인 지표를 정밀 분석합니다.
    """
    _purge_non_math_tutorial_topics()

    scripts = sorted(SCRIPTS_DIR.glob("*.json"))
    total_topics = len(scripts)
    v1_std_ko = 0
    v1_std_en = 0
    v2_q_ko = 0
    v2_q_en = 0
    v3_sh_ko = 0
    v3_sh_en = 0
    v4_qsh_ko = 0
    v4_qsh_en = 0
    yt_live_count = 0
    midroll_eligible_topics = []
    domain_buckets = {}

    for sp in scripts:
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = sdoc.get("slug", sp.stem)
        sub_dom = sdoc.get("sub_domain_ko") or "기하·대수 시각 증명"
        yt_u = sdoc.get("youtube_urls") or {}
        q_yt_u = sdoc.get("question_youtube_urls") or {}
        sh_u = sdoc.get("shorts_urls") or {}
        qsh_u = sdoc.get("question_shorts_urls") or {}

        for d_u in (yt_u, q_yt_u, sh_u, qsh_u):
            for lc in ("ko", "en"):
                if (d_u.get(lc) or "").strip():
                    yt_live_count += 1

        if (YT_UPLOADS_DIR / slug / f"{slug}_ko.mp4").exists() or yt_u.get("ko"):
            v1_std_ko += 1
        if (YT_UPLOADS_DIR / slug / f"{slug}_en.mp4").exists() or yt_u.get("en"):
            v1_std_en += 1
        if (QUESTION_DIR / f"{slug}_q_ko.mp4").exists() or q_yt_u.get("ko"):
            v2_q_ko += 1
        if (QUESTION_DIR / f"{slug}_q_en.mp4").exists() or q_yt_u.get("en"):
            v2_q_en += 1
        if (SHORTS_DIR / f"{slug}_short_ko.mp4").exists() or (YT_UPLOADS_DIR / "shorts" / f"{slug}_short_ko.mp4").exists() or sh_u.get("ko"):
            v3_sh_ko += 1
        if (SHORTS_DIR / f"{slug}_short_en.mp4").exists() or (YT_UPLOADS_DIR / "shorts" / f"{slug}_short_en.mp4").exists() or sh_u.get("en"):
            v3_sh_en += 1
        if (SHORTS_DIR / f"{slug}_short_q_ko.mp4").exists() or qsh_u.get("ko"):
            v4_qsh_ko += 1
        if (SHORTS_DIR / f"{slug}_short_q_en.mp4").exists() or qsh_u.get("en"):
            v4_qsh_en += 1

        ko_dur = float(((sdoc.get("youtube_packages") or {}).get("ko") or {}).get("total_duration_sec") or 0)
        q_dur = float(((sdoc.get("question_classroom_packages") or {}).get("ko") or {}).get("duration_sec") or 0)
        best_dur = max(ko_dur, q_dur)
        if best_dur >= 480.0:
            midroll_eligible_topics.append({
                "slug": slug,
                "title": sdoc.get("title", slug),
                "duration_sec": round(best_dur, 1),
            })
        domain_buckets.setdefault(sub_dom, []).append({
            "slug": slug,
            "title": sdoc.get("title", slug),
            "duration_sec": round(best_dur if best_dur > 0 else 210.0, 1),
        })

    total_rendered_assets = v1_std_ko + v1_std_en + v2_q_ko + v2_q_en + v3_sh_ko + v3_sh_en + v4_qsh_ko + v4_qsh_en

    # 단원별 8분+(480초 이상) 미드롤(Mid-Roll Ad) 마스터클래스 편성표 생성
    midroll_compilations = []
    for dom_name, items in sorted(domain_buckets.items()):
        total_dom_sec = sum(x["duration_sec"] for x in items)
        if total_dom_sec >= 480.0 and len(items) >= 3:
            midroll_compilations.append({
                "domain": dom_name,
                "topic_count": len(items),
                "total_duration_min": round(total_dom_sec / 60.0, 1),
                "estimated_midroll_slots": max(2, int(total_dom_sec // 240)),
                "rpm_multiplier": "2.2x (Mid-Roll Enabled >= 8:00)",
                "sample_slugs": [x["slug"] for x in items[:6]],
            })

    token_files = sorted(ROOT_DIR.glob("youtube_token_min7014_ai*.json"))
    daily_api_quota_units = len(token_files) * 10_000
    daily_api_uploads_capacity = max(1, daily_api_quota_units // 1_650)

    report = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lead_agent": "finance (Chief EdTech Ad Revenue Director)",
        "collaborating_agents": [
            "Video_Creator (4-Edition 1080p & #Shorts Production Engine)",
            "pr (7-Channel Viral Growth & SEO/GEO Funnel Director)",
            "mathteacher (Pedagogical Quality & Retention Auditor)",
            "designer (High-CTR Thumbnail & Native Ad UI Director)",
            "gamemaker (In-Game Rewarded Ad Chest & Engagement Loop)",
        ],
        "monthly_target_krw": MONTHLY_REVENUE_TARGET_KRW,
        "revenue_streams_blueprint": {
            "stream_1_youtube_longform": {
                "target_krw": 6_500_000,
                "share_pct": 65,
                "strategy": "1080p 한국어(KR RPM ~4,500원) + 북미·영국·호주 영어권(EN RPM ~12,500원) 시각적 증명 본편 & 8분+ 질문수업 미드롤(Mid-Roll) 광고",
                "target_monthly_views": 950_000,
            },
            "stream_2_youtube_shorts_funnel": {
                "target_krw": 1_500_000,
                "share_pct": 15,
                "strategy": "일반형 #Shorts + 질문형 Q-#Shorts(36~46초 무한루프 APV 105%+) 피드 광고 수익 및 1080p 본편 고정댓글 퍼널 유입",
                "target_monthly_views": 7_500_000,
            },
            "stream_3_mathedu_web_adsense": {
                "target_krw": 2_000_000,
                "share_pct": 20,
                "strategy": "유튜브 설명란 5단 딥링크 유입 ➔ video_board.html / 16,548문항 퀴즈 / 3D 게임 보상형 스폰서 상자(Rewarded Ad Chest) 웹 애드센스·애드핏 수익",
                "target_monthly_pageviews": 600_000,
            },
        },
        "asset_inventory": {
            "scripted_topics": total_topics,
            "total_target_topics": 1113,
            "total_rendered_mp4_files": total_rendered_assets,
            "edition_1_standard_1080p": {"ko": v1_std_ko, "en": v1_std_en},
            "edition_2_question_1080p": {"ko": v2_q_ko, "en": v2_q_en},
            "edition_3a_standard_shorts": {"ko": v3_sh_ko, "en": v3_sh_en},
            "edition_3b_question_shorts": {"ko": v4_qsh_ko, "en": v4_qsh_en},
            "youtube_bound_urls_count": yt_live_count,
            "single_videos_over_8min_midroll": len(midroll_eligible_topics),
            "domain_midroll_masterclasses_ready": len(midroll_compilations),
        },
        "midroll_masterclasses": midroll_compilations,
        "quota_infrastructure": {
            "active_gcp_token_pools": len(token_files),
            "daily_api_quota_units": daily_api_quota_units,
            "daily_auto_uploads_per_reset": daily_api_uploads_capacity,
            "quota_reset_time_kst": "매일 오후 5시 정각 (17:00 KST / 00:00 PST)",
        },
    }

    FINANCE_ENGINE_JSON.parent.mkdir(parents=True, exist_ok=True)
    FINANCE_ENGINE_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def inject_high_rpm_edtech_metadata() -> int:
    """
    모든 유튜브 메타데이터 패키지(*_youtube_meta.json, *_shorts_meta.json)에
    교육 분야 고단가(High-CPM) 키워드 태그가 누락 없이 포함되도록 보강합니다.
    """
    updated_count = 0
    for meta_file in sorted(YT_PKG_DIR.glob("*_meta.json")):
        try:
            mdata = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        changed = False
        for lc, kw_list in (("ko", HIGH_RPM_KEYWORDS_KO), ("en", HIGH_RPM_KEYWORDS_EN)):
            if lc in mdata and isinstance(mdata[lc], dict):
                cur_tags = list(mdata[lc].get("tags") or [])
                for kw in kw_list:
                    if kw not in cur_tags and len(cur_tags) < 28:
                        cur_tags.append(kw)
                        changed = True
                mdata[lc]["tags"] = cur_tags
        if changed:
            meta_file.write_text(json.dumps(mdata, ensure_ascii=False, indent=2), encoding="utf-8")
            updated_count += 1
    return updated_count


def run_autonomous_finance_cycle() -> dict:
    """
    24/7 근간 데몬(mathedu_foundation_daemon.py)에서 매 사이클 호출되는
    finance 에이전트 자율 수익화 최적화 루프입니다.
    """
    boosted_pkgs = inject_high_rpm_edtech_metadata()
    rep = analyze_revenue_pipeline()
    inv = rep["asset_inventory"]
    print(
        f"💼 [Finance Agent v2.0 · 월 1,000만 원 수익 엔진] "
        f"총 {inv['scripted_topics']}개 주제 / {inv['total_rendered_mp4_files']}편 MP4 자산 가동 중 "
        f"(8분+ 미드롤 본편 {inv['single_videos_over_8min_midroll']}편, 고단가 태그 보강 +{boosted_pkgs}건)",
        flush=True,
    )
    return rep


def cmd_status():
    rep = analyze_revenue_pipeline()
    inv = rep["asset_inventory"]
    q_info = rep["quota_infrastructure"]
    print("=" * 88)
    print("💼 [Finance Agent v2.0] 월 1,000만 원(연 1.2억 원) 유튜브 × 웹 광고 수익화 총괄 현황")
    print("=" * 88)
    print(f" • 총괄 책임 에이전트 : {rep['lead_agent']}")
    print(f" • 협업 에이전트 연합 : {', '.join(rep['collaborating_agents'])}")
    print(f" • 월간 목표 수익     : {rep['monthly_target_krw']:,}원 / 월")
    print("-" * 88)
    print(" 📊 [3-Track 월 1,000만 원 수익 포트폴리오 설계]")
    for k, v in rep["revenue_streams_blueprint"].items():
        print(f"   - {k}: 월 {v['target_krw']:,}원 ({v['share_pct']}%) | {v['strategy']}")
    print("-" * 88)
    print(" 🎬 [현재 축적된 수익 창출 영상 자산 (Evergreen Video Assets)]")
    print(f"   - 대본 완성 주제 수            : {inv['scripted_topics']} / {inv['total_target_topics']}개 주제")
    print(f"   - 누적 렌더링 완료 MP4 총합    : {inv['total_rendered_mp4_files']:,}편")
    print(f"   - ① 1080p 일반 설명 본편       : KO {inv['edition_1_standard_1080p']['ko']}편 / EN {inv['edition_1_standard_1080p']['en']}편")
    print(f"   - ② 1080p 질문하는 수업 본편   : KO {inv['edition_2_question_1080p']['ko']}편 / EN {inv['edition_2_question_1080p']['en']}편")
    print(f"   - ③-A 9:16 일반형 #Shorts      : KO {inv['edition_3a_standard_shorts']['ko']}편 / EN {inv['edition_3a_standard_shorts']['en']}편")
    print(f"   - ③-B 9:16 질문형 Q-#Shorts    : KO {inv['edition_3b_question_shorts']['ko']}편 / EN {inv['edition_3b_question_shorts']['en']}편")
    print(f"   - 8분+(480초) 미드롤 광고 본편 : {inv['single_videos_over_8min_midroll']}편 (단원별 합본 {inv['domain_midroll_masterclasses_ready']}개 준비)")
    print(f"   - GCP API 쿼터 풀 용량         : 프로젝트 {q_info['active_gcp_token_pools']}개 (일일 {q_info['daily_api_quota_units']:,} 유닛 / 하루 약 {q_info['daily_auto_uploads_per_reset']}편 업로드)")
    print("=" * 88)


def main():
    parser = argparse.ArgumentParser(description="mathedu & @min7014_ai Chief Ad Revenue Director (finance.py)")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("status")
    sub.add_parser("optimize")
    sub.add_parser("verify")

    p_ads = sub.add_parser("set-adsense")
    p_ads.add_argument("--client", required=True)
    p_ads.add_argument("--slot", default="")

    p_adf = sub.add_parser("set-adfit")
    p_adf.add_argument("--unit", required=True)

    args = parser.parse_args()
    if args.cmd == "optimize":
        run_autonomous_finance_cycle()
    elif args.cmd == "set-adsense":
        cfg = json.loads(AD_CONFIG_JSON.read_text(encoding="utf-8")) if AD_CONFIG_JSON.exists() else {}
        cfg.setdefault("adsense", {})["enabled"] = True
        cfg["adsense"]["clientId"] = args.client
        if args.slot:
            cfg["adsense"]["slotMain"] = args.slot
        AD_CONFIG_JSON.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        pub_id = args.client.replace("ca-pub-", "pub-")
        ADS_TXT.write_text(f"google.com, {pub_id}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
        print(f"✅ [AdSense Activated] {args.client} -> ad_config.json & ads.txt updated!")
    elif args.cmd == "set-adfit":
        cfg = json.loads(AD_CONFIG_JSON.read_text(encoding="utf-8")) if AD_CONFIG_JSON.exists() else {}
        cfg.setdefault("kakaoAdfit", {})["enabled"] = True
        cfg["kakaoAdfit"]["unitMain"] = args.unit
        AD_CONFIG_JSON.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ [Kakao AdFit Activated] {args.unit} -> ad_config.json updated!")
    else:
        cmd_status()


if __name__ == "__main__":
    main()
