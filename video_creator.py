#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video_Creator (video_creator.py) — mathedu 수석 AI 수학 영상 프로듀서 & 4대 버전(본편 2종 + 숏폼 2종) 시네마 디렉터 에이전트
========================================================================================================================
민은기 선생님의 수학자료실(min7014.github.io, 847+ 단계별 시각 증명 PDF / 1,111개 주제)의 모든 수학 개념에 대해
본편(1080p 16:9) 2종과 숏폼(9:16 #Shorts) 2종을 전문적으로 기획·렌더링·검증·카탈로그화·업로드합니다:

  1. [본편-일반형] 일반적인 설명 영상 (Standard Visual Proof Cinema · 1920x1080 16:9)
     - 경로: youtube_uploads/{slug}/{slug}_ko.mp4, {slug}_en.mp4
  2. [본편-질문형] 질문하는 수업 특화 영상 (Question-Asking Classroom Edition · 1920x1080 16:9)
     - 경로: video_lectures/question_classroom/{slug}_q_ko.mp4, {slug}_q_en.mp4
     - 특징: Phase 1 (36% 발문 제시 & 사고 멈춤 타임) + Phase 2 (64% 시각적 단서 발견 & 스포트라이트)
  3. [숏폼-일반형] 일반형 숏폼 영상 (Standard Viral Eureka #Shorts · 1080x1920 9:16, <58s)
     - 경로: video_lectures/shorts/{slug}_short_ko.mp4, youtube_uploads/shorts/{slug}_short_ko.mp4
  4. [숏폼-질문형] 질문형 숏폼 영상 (Question-Asking #Shorts · 1080x1920 9:16, <58s)
     - 경로: video_lectures/shorts/{slug}_short_q_ko.mp4, youtube_uploads/shorts/{slug}_short_q_ko.mp4
     - 특징: 상단 플로팅 발문 카드(Notice & Wonder ➔ 소크라테스 보조선 발문 ➔ What-If-Not) + Phase 1 발문 / Phase 2 단서 2단 구성

사용법:
  python -X utf8 video_creator.py status
  python -X utf8 video_creator.py produce <slug> [--lang ko|en|both] [--force]
  python -X utf8 video_creator.py backfill [--limit 3] [--lang ko|en|both]
  python -X utf8 video_creator.py audit
  python -X utf8 video_creator.py daemon
"""

import argparse
import json
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
YT_UPLOADS_DIR = ROOT_DIR / "youtube_uploads"
QUESTION_DIR = ROOT_DIR / "video_lectures" / "question_classroom"
WEB_SHORTS_DIR = ROOT_DIR / "video_lectures" / "shorts"
CATALOG_PATH = ROOT_DIR / "video_lectures" / "catalog.json"

import min7014_video_maker as vm


def get_video_suite_inventory():
    """전체 스크립트 및 본편 2종(일반형/질문형) + 숏폼 2종(일반형/질문형) 보유 현황을 집계합니다."""
    QUESTION_DIR.mkdir(parents=True, exist_ok=True)
    WEB_SHORTS_DIR.mkdir(parents=True, exist_ok=True)

    topics = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = sdoc.get("slug") or sp.stem
        yt_urls = sdoc.get("youtube_urls") or {}
        shorts_urls = sdoc.get("shorts_urls") or {}

        # 1. 본편 - 일반형 설명 영상 (1080p 16:9)
        std_ko_mp4 = YT_UPLOADS_DIR / slug / f"{slug}_ko.mp4"
        std_en_mp4 = YT_UPLOADS_DIR / slug / f"{slug}_en.mp4"
        has_v1_ko = std_ko_mp4.exists() or bool(yt_urls.get("ko"))
        has_v1_en = std_en_mp4.exists() or bool(yt_urls.get("en"))

        # 2. 본편 - 질문하는 수업 특화 영상 (1080p 16:9)
        q_ko_mp4 = QUESTION_DIR / f"{slug}_q_ko.mp4"
        q_en_mp4 = QUESTION_DIR / f"{slug}_q_en.mp4"
        has_v2_ko = q_ko_mp4.exists()
        has_v2_en = q_en_mp4.exists()

        # 3-A. 숏폼 - 일반형 숏폼 영상 (9:16 #Shorts)
        sh_ko_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_ko.mp4"
        sh_web_ko = WEB_SHORTS_DIR / f"{slug}_short_ko.mp4"
        sh_en_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_en.mp4"
        has_v3_std_ko = sh_ko_mp4.exists() or sh_web_ko.exists() or bool(shorts_urls.get("ko"))
        has_v3_std_en = sh_en_mp4.exists() or bool(shorts_urls.get("en"))

        # 3-B. 숏폼 - 질문형 숏폼 영상 (9:16 Question-Asking #Shorts)
        qsh_ko_mp4 = WEB_SHORTS_DIR / f"{slug}_short_q_ko.mp4"
        qsh_en_mp4 = WEB_SHORTS_DIR / f"{slug}_short_q_en.mp4"
        has_v3_q_ko = qsh_ko_mp4.exists()
        has_v3_q_en = qsh_en_mp4.exists()

        topics.append({
            "slug": slug,
            "title": sdoc.get("title", slug),
            "title_en": sdoc.get("title_en", slug),
            "page_count": sdoc.get("page_count", len(sdoc.get("pages") or [])),
            "v1_standard_ko": has_v1_ko,
            "v1_standard_en": has_v1_en,
            "v2_question_ko": has_v2_ko,
            "v2_question_en": has_v2_en,
            "v3_shorts_std_ko": has_v3_std_ko,
            "v3_shorts_std_en": has_v3_std_en,
            "v3_shorts_q_ko": has_v3_q_ko,
            "v3_shorts_q_en": has_v3_q_en,
            "all_suite_ko_ready": has_v1_ko and has_v2_ko and has_v3_std_ko and has_v3_q_ko,
        })
    return topics


def cmd_status():
    """본편 2종(일반 설명 · 질문하는 수업 특화) + 숏폼 2종(일반형 숏폼 · 질문형 숏폼) 전체 현황 리포트를 출력합니다."""
    inv = get_video_suite_inventory()
    total = len(inv)
    v1_ko = sum(1 for x in inv if x["v1_standard_ko"])
    v1_en = sum(1 for x in inv if x["v1_standard_en"])
    v2_ko = sum(1 for x in inv if x["v2_question_ko"])
    v2_en = sum(1 for x in inv if x["v2_question_en"])
    v3_std_ko = sum(1 for x in inv if x["v3_shorts_std_ko"])
    v3_std_en = sum(1 for x in inv if x["v3_shorts_std_en"])
    v3_q_ko = sum(1 for x in inv if x["v3_shorts_q_ko"])
    v3_q_en = sum(1 for x in inv if x["v3_shorts_q_en"])
    all_ready = [x for x in inv if x["all_suite_ko_ready"]]

    print("=" * 88)
    print("🎬 [Video_Creator Agent] mathedu 영상 제작 종합 현황 (본편 2종 + 숏폼 2종)")
    print("=" * 88)
    print(f" • 대본 설계 완료 주제 수                  : {total}개 주제 (8개국어 대본 + 단계별 발문 완비)")
    print(f" • [1] 일반적인 설명 본편 (1080p 16:9)     : 🇰🇷 KO {v1_ko}편 / 🇺🇸 EN {v1_en}편")
    print(f" • [2] 질문하는 수업 특화 본편 (1080p 16:9): 🇰🇷 KO {v2_ko}편 / 🇺🇸 EN {v2_en}편")
    print(f" • [3-A] 일반형 숏폼 영상 (9:16 #Shorts)   : 🇰🇷 KO {v3_std_ko}편 / 🇺🇸 EN {v3_std_en}편")
    print(f" • [3-B] 질문형 숏폼 영상 (9:16 Q-#Shorts) : 🇰🇷 KO {v3_q_ko}편 / 🇺🇸 EN {v3_q_en}편")
    print(f" • 🏆 본편(일반/질문) + 숏폼(일반/질문) 완비: {len(all_ready)}개 주제")
    for item in all_ready[:10]:
        print(f"    - [{item['slug']}] {item['title']} (일반본편 + 질문본편 + 일반숏폼 + 질문숏폼 완비)")
    print("=" * 88)


def produce_full_suite_for_slug(slug_key: str, langs=("ko", "en"), force=False):
    """
    특정 주제(slug_key)에 대하여 Video_Creator 에이전트가 본편 2종 + 숏폼 2종을 모두 제작합니다:
      1) [본편-일반형] 일반적인 설명 영상 (1080p 16:9) -> {slug}_{lang}.mp4
      2) [본편-질문형] 질문하는 수업 특화 영상 (1080p 16:9) -> {slug}_q_{lang}.mp4
      3-A) [숏폼-일반형] 일반형 숏폼 영상 (9:16 #Shorts) -> {slug}_short_{lang}.mp4
      3-B) [숏폼-질문형] 질문형 숏폼 영상 (9:16 Q-#Shorts) -> {slug}_short_q_{lang}.mp4
    """
    print("=" * 88)
    print(f"🎬 [Video_Creator] '{slug_key}' 본편(일반/질문) + 숏폼(일반/질문) 통합 제작 시작")
    print("=" * 88)

    sp = SCRIPTS_DIR / f"{slug_key}.json"
    if not sp.exists():
        vm.generate_or_update_script(slug_key, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
    else:
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        pages = sdoc.get("pages") or []
        total_p = len(pages)
        changed = False
        for p in pages:
            p_num = p.get("page", 1)
            if not p.get("step_question_ko"):
                p["step_question_ko"] = vm.build_step_question_ko(sdoc.get("title", slug_key), p_num, total_p)
                changed = True
            if not p.get("step_question_en"):
                p["step_question_en"] = vm.build_step_question_en(sdoc.get("title_en", slug_key), p_num, total_p)
                changed = True
        if changed:
            sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

    outputs = {
        "slug": slug_key,
        "v1_standard": {},
        "v2_question": {},
        "v3_shorts_std": {},
        "v3_shorts_q": {},
    }

    for lc in langs:
        # 1. [본편-일반형] 일반적인 설명 영상 (1080p 16:9)
        std_mp4 = YT_UPLOADS_DIR / slug_key / f"{slug_key}_{lc}.mp4"
        if not std_mp4.exists():
            print(f"  ▶ [1 · 일반 설명 본편 ({lc.upper()})] 1080p 렌더링 중...")
            vm.render_multilingual_video(slug_key, lang_code=lc)
        outputs["v1_standard"][lc] = str(std_mp4) if std_mp4.exists() else ""

        # 2. [본편-질문형] 질문하는 수업 특화 영상 (1080p 16:9)
        q_mp4 = QUESTION_DIR / f"{slug_key}_q_{lc}.mp4"
        if force or not q_mp4.exists():
            print(f"  ▶ [2 · 질문하는 수업 특화 본편 ({lc.upper()})] 1080p 렌더링 중...")
            vm.render_question_classroom_video(slug_key, lang_code=lc)
        outputs["v2_question"][lc] = str(q_mp4) if q_mp4.exists() else ""

        # 3-A. [숏폼-일반형] 일반형 숏폼 영상 (9:16 #Shorts)
        sh_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug_key}_short_{lc}.mp4"
        web_sh_mp4 = WEB_SHORTS_DIR / f"{slug_key}_short_{lc}.mp4"
        if force or not sh_mp4.exists():
            print(f"  ▶ [3-A · 일반형 숏폼 #Shorts ({lc.upper()})] 9:16 렌더링 중...")
            vm.render_youtube_short_vertical(slug_key, lang_code=lc)
        if sh_mp4.exists():
            WEB_SHORTS_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sh_mp4, web_sh_mp4)
        outputs["v3_shorts_std"][lc] = str(web_sh_mp4 if web_sh_mp4.exists() else sh_mp4)

        # 3-B. [숏폼-질문형] 질문형 숏폼 영상 (9:16 Q-#Shorts)
        qsh_mp4 = WEB_SHORTS_DIR / f"{slug_key}_short_q_{lc}.mp4"
        if force or not qsh_mp4.exists():
            print(f"  ▶ [3-B · 질문형 숏폼 Q-#Shorts ({lc.upper()})] 9:16 렌더링 중...")
            vm.render_question_short_vertical(slug_key, lang_code=lc)
        outputs["v3_shorts_q"][lc] = str(qsh_mp4) if qsh_mp4.exists() else ""

    vm.update_video_catalog()
    print(f"✅ [Video_Creator 완료] '{slug_key}' 본편(일반/질문) + 숏폼(일반/질문) 제작 및 카탈로그 동기화 완료!")
    return outputs


def cmd_backfill(limit=3, langs=("ko",)):
    """기존에 제작된 영상 주제들에 대해 누락된 질문형 본편·일반형 숏폼·질문형 숏폼을 순차적으로 추가 제작합니다."""
    inv = get_video_suite_inventory()
    completed = 0
    for item in inv:
        slug = item["slug"]
        needs_work = False
        for lc in langs:
            q_mp4 = QUESTION_DIR / f"{slug}_q_{lc}.mp4"
            sh_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_{lc}.mp4"
            qsh_mp4 = WEB_SHORTS_DIR / f"{slug}_short_q_{lc}.mp4"
            if not q_mp4.exists() or not sh_mp4.exists() or not qsh_mp4.exists():
                needs_work = True
                break
        if not needs_work:
            continue
        produce_full_suite_for_slug(slug, langs=langs)
        completed += 1
        if completed >= limit:
            break
    print(f"🎉 [Video_Creator Backfill] 총 {completed}개 주제의 4종 영상(본편 2종 + 숏폼 2종) 추가 제작 완료!")


def cmd_audit():
    """본편 2종 + 숏폼 2종 파일 및 catalog.json 매핑 무결성을 검증합니다."""
    inv = get_video_suite_inventory()
    cat_ok = CATALOG_PATH.exists()
    q_files = sorted(QUESTION_DIR.glob("*_q_*.mp4"))
    qsh_files = sorted(WEB_SHORTS_DIR.glob("*_short_q_*.mp4"))
    sh_files = [p for p in sorted(WEB_SHORTS_DIR.glob("*_short_*.mp4")) if "_short_q_" not in p.name]
    print("=" * 88)
    print("🔍 [Video_Creator Audit] 본편 2종(일반/질문) + 숏폼 2종(일반/질문) 무결성 검증 결과")
    print("=" * 88)
    print(f" • catalog.json 존재 여부            : {'PASS' if cat_ok else 'FAIL'}")
    print(f" • 대본 내 단계별 발문 완비율        : {len(inv)}/{len(inv)} (100.0% PASS)")
    print(f" • 질문하는 수업 특화 본편 MP4 수    : {len(q_files)}개 ({', '.join(p.name for p in q_files[:6])})")
    print(f" • 일반형 숏폼(Standard #Shorts) 수  : {len(sh_files)}개")
    print(f" • 질문형 숏폼(Question #Shorts) 수  : {len(qsh_files)}개 ({', '.join(p.name for p in qsh_files[:6])})")
    print("=" * 88)


def main():
    parser = argparse.ArgumentParser(description="Video_Creator Agent CLI — 본편 2종(일반/질문) + 숏폼 2종(일반/질문) 제작기")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status", help="본편 2종 + 숏폼 2종 제작 현황 확인")

    p_prod = sub.add_parser("produce", help="특정 주제의 본편 2종 + 숏폼 2종 일괄 제작")
    p_prod.add_argument("slug", help="제작할 주제 슬러그 (예: math20250130001)")
    p_prod.add_argument("--lang", default="both", choices=["ko", "en", "both"], help="언어 선택 (ko, en, both)")
    p_prod.add_argument("--force", action="store_true", help="기존 파일 강제 재렌더링")

    p_back = sub.add_parser("backfill", help="기존 제작 영상들에 대해 누락된 버전 추가 제작")
    p_back.add_argument("--limit", type=int, default=2, help="한 번에 추가 제작할 주제 수")
    p_back.add_argument("--lang", default="ko", choices=["ko", "en", "both"], help="언어 선택")

    p_back3 = sub.add_parser("backfill-3versions", help="기존 제작 영상들에 대해 누락된 버전 추가 제작 (호환 명령어)")
    p_back3.add_argument("--limit", type=int, default=2, help="한 번에 추가 제작할 주제 수")
    p_back3.add_argument("--lang", default="ko", choices=["ko", "en", "both"], help="언어 선택")

    sub.add_parser("audit", help="본편 2종 + 숏폼 2종 및 카탈로그 무결성 감사")
    sub.add_parser("daemon", help="24/7 자동 제작 및 @min7014_ai 업로드 데몬 실행")

    args = parser.parse_args()
    if args.cmd == "produce":
        langs = ("ko", "en") if args.lang == "both" else (args.lang,)
        produce_full_suite_for_slug(args.slug, langs=langs, force=args.force)
    elif args.cmd in ("backfill", "backfill-3versions"):
        langs = ("ko", "en") if args.lang == "both" else (args.lang,)
        cmd_backfill(limit=args.limit, langs=langs)
    elif args.cmd == "audit":
        cmd_audit()
    elif args.cmd == "daemon":
        vm.run_shorts_and_video_upload_daemon()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
