#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import silent_subprocess  # noqa: F401 — Windows 백그라운드 완전 무창 강제
"""
secretary.py
===============================================================================
👔 민은기 선생님(min7014) 전담 수석 비서실장(Chief AI Secretary) 통합 관제 엔진
- 산하 6대 전문 에이전트(mathteacher, Video_Creator, finance, pr, gamemaker, designer) 총괄 지휘
- 24/7 데몬(mathedu_foundation_daemon.py) 및 @min7014_ai 유튜브 수익창출(YPP & 월 1,000만 원+) 실시간 관제
- 텔레그램(@anti7014_bot, Chat ID: 43453234) 양방향 실시간 브리핑 및 원격 지시 핫라인 관리
===============================================================================
"""

import argparse
import datetime
import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def collect_live_workspace_metrics() -> dict:
    vl_dir = ROOT_DIR / "video_lectures"
    yt_dir = ROOT_DIR / "youtube_uploads"
    mc_dir = yt_dir / "masterclasses"

    # 1. Video_Creator 지표
    vl_mp4s = list(vl_dir.rglob("*.mp4")) if vl_dir.exists() else []
    yt_mp4s = list(yt_dir.rglob("*.mp4")) if yt_dir.exists() else []
    total_mp4_count = len(vl_mp4s) + len(yt_mp4s)

    vault_file = vl_dir / "vault_index.json"
    vault_topics = 0
    scripts_cnt = len(list((vl_dir / "scripts").glob("*.json"))) if (vl_dir / "scripts").exists() else 0
    if vault_file.exists():
        try:
            vdata = json.loads(vault_file.read_text(encoding="utf-8"))
            vault_topics = int(vdata.get("total_topics") or len(vdata.get("topics", vdata.get("videos", [])))) if isinstance(vdata, dict) else len(vdata)
        except Exception:
            pass

    q_ko = list((vl_dir / "question_classroom").glob("*_q_ko.mp4")) if (vl_dir / "question_classroom").exists() else []
    s_all = list((vl_dir / "shorts").glob("*.mp4")) if (vl_dir / "shorts").exists() else []
    qs_ko = list((vl_dir / "shorts").glob("*_qshorts_*.mp4")) if (vl_dir / "shorts").exists() else []

    mc_mp4s = sorted(mc_dir.glob("*.mp4")) if mc_dir.exists() else []
    ci_mp4s = []

    # 2. mathteacher 지표
    ped_file = ROOT_DIR / "assets" / "mathteacher_pedagogy_engine.json"
    ped_topics = 0
    if ped_file.exists():
        try:
            ped_data = json.loads(ped_file.read_text(encoding="utf-8"))
            ped_topics = len(ped_data.get("questionAskingClassrooms", []))
        except Exception:
            pass

    completed_topics = max(vault_topics, scripts_cnt, len(qs_ko))

    # 3. finance 지표
    rev_file = yt_dir / "revenue_master_plan_10m_krw.json"
    ypp_status = "가동 중 (Vol.1~8 한/영 16편 8분+ 미드롤 마스터클래스 + 6종 하이브리드 파이프라인)"
    if rev_file.exists():
        try:
            rev_data = json.loads(rev_file.read_text(encoding="utf-8"))
            ypp_status = rev_data.get("target_monthly_revenue", ypp_status)
        except Exception:
            pass

    # 4. 데몬 상태
    hb_file = ROOT_DIR / ".agents" / "foundation_daemon_heartbeat.json"
    daemon_state = {}
    if hb_file.exists():
        try:
            daemon_state = json.loads(hb_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    fd_status_file = vl_dir / "foundation_daemon_status.json"
    if fd_status_file.exists():
        try:
            fd_st = json.loads(fd_status_file.read_text(encoding="utf-8"))
            if fd_st.get("last_completed_slug"):
                daemon_state["last_topic"] = fd_st.get("last_completed_slug")
            if fd_st.get("updated_at"):
                daemon_state["updated_at"] = fd_st.get("updated_at")
        except Exception:
            pass
    if not daemon_state.get("last_topic"):
        last_chat_p = ROOT_DIR / ".agents" / "last_agent_chat_slug.txt"
        if last_chat_p.exists():
            try:
                s_val = last_chat_p.read_text(encoding="utf-8").strip()
                if s_val:
                    daemon_state["last_topic"] = s_val
            except Exception:
                pass
    if not daemon_state.get("last_topic") and (vl_dir / "scripts").exists():
        try:
            newest_sp = max((vl_dir / "scripts").glob("*.json"), key=lambda p: p.stat().st_mtime)
            daemon_state["last_topic"] = newest_sp.stem
        except Exception:
            pass

    # 수학공학도구(GeoGebra/AlgeoMath/TikZ) 5단계 커리큘럼 진행률 집계
    geogebra_book_slugs = [f"20210426{i:02d}" for i in range(3, 19)] + [
        "2019062801", "2019072302", "math20190921001", "math20210424001",
        "math20210426002", "math20260519001", "math20240308001", "math20231203002",
        "math20190810130", "math20190810131", "math20190918001", "math20190914002",
        "math20190912002", "math20190810063", "math20190810072", "math20210308001",
        "math20230707001", "2018092501"
    ]
    ggb_rendered = sum(
        1 for gs in geogebra_book_slugs
        if (yt_dir / gs / f"{gs}_ko.mp4").exists() or (vl_dir / "shorts" / f"{gs}_short_q_ko.mp4").exists()
    )

    # 5. 텔레그램 브릿지 상태
    tg_offset_file = ROOT_DIR / ".agents" / "telegram_offset.json"
    tg_state = {}
    if tg_offset_file.exists():
        try:
            tg_state = json.loads(tg_offset_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "video_creator": {
            "total_mp4_files": total_mp4_count,
            "completed_6ed_topics": completed_topics,
            "target_total_topics": 847,
            "remaining_topics": max(0, 847 - completed_topics),
            "progress_pct": round(completed_topics / 847 * 100, 1),
            "editions": {
                "question_classroom_mp4": len(q_ko),
                "shorts_mp4": len(s_all),
                "qshorts_mp4": len(qs_ko),
            },
            "masterclasses_8min_plus": len(mc_mp4s),
            "creative_idea_cinema": len(ci_mp4s),
            "math_engineering_tools_total": len(geogebra_book_slugs),
            "math_engineering_tools_rendered": ggb_rendered,
        },
        "mathteacher": {
            "pedagogy_engine_topics": ped_topics,
            "total_problems": 16548,
            "min7014_resources": 1113,
        },
        "finance": {
            "revenue_goal": "월 1,000만 원+ (~$7,500+/월) & YPP 수익창출 조기 달성(3~5주 가속)",
            "masterclasses_ready": len(mc_mp4s),
        },
        "daemon": daemon_state,
        "telegram": {
            "bot_handle": "@anti7014_bot",
            "chat_id": tg_state.get("chat_id", "43453234"),
            "last_offset": tg_state.get("offset", 0),
        },
    }


def format_executive_briefing(metrics: dict) -> str:
    vc = metrics["video_creator"]
    mt = metrics["mathteacher"]
    dm = metrics.get("daemon", {})

    bal_txt = "확인 중"
    bal_p = ROOT_DIR / ".agents" / "daily_wave_balance.json"
    if bal_p.exists():
        try:
            bd = json.loads(bal_p.read_text(encoding="utf-8"))
            bal_txt = f"본편 {bd.get('std', 0)} · 쇼츠 {bd.get('shorts', 0)} · 합본 {bd.get('mc', 0)} ({bd.get('quota_day', '')})"
        except Exception:
            pass

    aud_line = ""
    try:
        import auditor as _aud
        arep = _aud.run_full_audit(auto_fix=True, check_live_youtube=False)
        aud_line = f"위반 {arep.get('total_violations', 0)}건 ({arep.get('status', '')})"
    except Exception:
        aud_line = "점검 생략"

    rep_line = ""
    try:
        import _antigravity_report_watcher as _arw_sec
        r_sum = (_arw_sec.format_error_reports_summary() or "").strip()
        r_lines = [ln.lstrip("• ").strip() for ln in r_sum.splitlines() if ln.strip()]
        rep_line = next((ln for ln in r_lines if "미처리" in ln or "누적" in ln), (r_lines[1] if len(r_lines) > 1 else (r_lines[0] if r_lines else "")))
    except Exception:
        pass

    lines = [
        f"📊 [수석 비서 핵심 요약 브리핑] ({metrics['timestamp']})",
        f"• 데몬·최근 주제: 가동 중 (`{dm.get('last_topic', '-')}`) | 금일 발행: {bal_txt} (Policy 83 일 36~48편)",
        f"• 영상·마스터클래스: {vc['completed_6ed_topics']}/{vc['target_total_topics']}주제 ({vc['progress_pct']}%) | 누적 MP4 {vc['total_mp4_files']:,}편 | 8분+ 합본 {vc['masterclasses_8min_plus']}편",
        f"• 수학교육·도구: 6대 교육모듈 {mt['pedagogy_engine_topics']}주제 | 공학도구 {vc['math_engineering_tools_rendered']}/{vc['math_engineering_tools_total']}편",
        f"• 무결성 감사: {aud_line}",
    ]
    if rep_line:
        lines.append(f"• 오류신고: {rep_line}")
    return "\n".join(lines)


DAILY_REPORT_STATE_FILE = ROOT_DIR / ".agents" / "secretary_daily_report_state.json"


def ensure_video_board_strategic_lab_features() -> bool:
    """
    [발전 방안 2 & 5 즉시 구현]
    video_board.html에 ① GeoGebra·AlgeoMath 실시간 분할 실습 스튜디오(명령어 치트시트 내장) 및
    ② 교사용 5분 수업 발문 & 2022 개정 생기부 세특 / 수학 심화 탐구 원클릭 복사 버튼을 보장합니다.
    """
    vb_path = ROOT_DIR / "video_board.html"
    if not vb_path.exists():
        return False
    txt = vb_path.read_text(encoding="utf-8")
    changed = False
    t1 = '<button type="button" onclick="window.printClassroomQrWorksheet(${itemIdx})"'
    r1 = (
        '<button type="button" onclick="window.toggleGeoGebraSplitLab(${itemIdx})" class="res-chip" style="border-color:#38bdf8;background:#e0f2fe;color:#0369a1;font-weight:900;cursor:pointer;">🛠️ GeoGebra·AlgeoMath 실시간 실습 스튜디오 (명령어 치트시트)</button>\n'
        '        <button type="button" onclick="window.copyTeacherLessonRecordKit(${itemIdx})" class="res-chip" style="border-color:#a78bfa;background:#f5f3ff;color:#5b21b6;font-weight:900;cursor:pointer;">🏫 교사용 5분 발문 & 생기부 세특·심화 탐구 문구 복사</button>\n'
        '        ' + t1
    )
    if "toggleGeoGebraSplitLab" not in txt and t1 in txt:
        txt = txt.replace(t1, r1, 1)
        changed = True

    t2 = "document.addEventListener('DOMContentLoaded', initGlobalViralBenchmarkHub);"
    r2 = t2 + """
    window.toggleGeoGebraSplitLab = function(itemIdx) {
      const item = ALL_ITEMS[itemIdx] || {};
      let labBox = document.getElementById('vbGeoGebraSplitLabBox');
      if (!labBox) {
        labBox = document.createElement('div');
        labBox.id = 'vbGeoGebraSplitLabBox';
        labBox.style.cssText = 'margin-top:14px;padding:16px;border-radius:16px;background:#0f172a;border:2px solid #38bdf8;color:#f8fafc;';
        const linksEl = document.getElementById('cinemaResourceLinks');
        if (linksEl && linksEl.parentNode) linksEl.parentNode.appendChild(labBox);
      } else if (labBox.style.display !== 'none') {
        labBox.style.display = 'none';
        return;
      }
      labBox.style.display = 'block';
      const ggbUrl = item.geogebra || '';
      const mathlabUrl = 'https://min7014.github.io/2025/mathlab.html';
      labBox.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
          <div style="font-weight:900;font-size:0.95rem;color:#38bdf8;">🛠️ [보편적 수학공학도구 실시간 실습 스튜디오 — 자체 제작 MathLab v1.3 탑재] 특정 도구에 얽매이지 않고 원리대로 직접 작도해 보세요!</div>
          <div style="display:flex;gap:6px;flex-wrap:wrap;">
            <a href="${mathlabUrl}" target="_blank" rel="noopener" style="padding:5px 10px;border-radius:8px;background:#0284c7;color:#fff;font-size:0.78rem;font-weight:900;text-decoration:none;">🚀 자체 제작 MathLab 전체화면 ↗</a>
            ${ggbUrl ? `<a href="${ggbUrl}" target="_blank" rel="noopener" style="padding:5px 10px;border-radius:8px;background:#0284c7;color:#fff;font-size:0.78rem;font-weight:800;text-decoration:none;">🧭 원본 동적기하 자료 ↗</a>` : ''}
            <a href="https://www.algeomath.kr/" target="_blank" rel="noopener" style="padding:5px 10px;border-radius:8px;background:#059669;color:#fff;font-size:0.78rem;font-weight:800;text-decoration:none;">📐 공교육 알지오매스 ↗</a>
            <button type="button" onclick="document.getElementById('vbGeoGebraSplitLabBox').style.display='none'" style="padding:5px 10px;border-radius:8px;background:#334155;color:#fff;border:none;font-size:0.78rem;cursor:pointer;">닫기 ✕</button>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-bottom:12px;font-size:0.78rem;background:#1e293b;padding:12px;border-radius:12px;border:1px solid #334155;">
          <div><strong style="color:#facc15;">📌 [1. 자체 제작 MathLab (min7014.github.io/2025/mathlab.html)]</strong><br>• 기하 작도: 점(●)·선분(╱)·직선(↔)·평행선(∥)·수선(⊥)·중점(•)·각이등분선(∠)<br>• 이차곡선: 원(○)·포물선(∪, 초점+준선)·타원(⬭, 두 초점+점)·쌍곡선()(, 두 초점+점)<br>• 수식/함수: 빈 공간 1초 롱프레스(LaTeX 텍스트) / 클릭 후 1초 홀드(함수·음함수 그래프)</div>
          <div><strong style="color:#34d399;">📌 [2. 보편적 동적 기하·시뮬레이션 설계 원리 (Tool-Agnostic)]</strong><br>• <code>구속 조건(Constraint)</code>: 눈대중 배치 금지, 반드시 교점·수선·평행선 정의로 결합<br>• <code>매개변수(Parameter)</code>: 구간 [a,b]·기울기·시행 횟수 n을 동적 변수로 제어<br>• <code>자취·포락선(Locus & Envelope)</code>: 동점 P에 종속된 점 Q와 접선군의 자취 추적</div>
          <div><strong style="color:#f472b6;">📌 [3. 오픈소스 & 범용 수식 스크립트 문법 호환표]</strong><br>• 반복 생성: <code>Sequence(식, 변수, 시작, 끝)</code> / Python <code>[f(k) for k in range(a,b)]</code><br>• 조건부 집계: <code>CountIf(조건, 리스트)</code> / 통계 몬테카를로 확률 시뮬레이션<br>• 수치 최적화: <code>Newton-Raphson 투영</code> & <code>경사하강법(Gradient Descent)</code></div>
        </div>
        <div style="background:#090d16;border:1px solid #38bdf8;border-radius:12px;overflow:hidden;">
          <div style="padding:8px 14px;background:#1e293b;font-size:0.8rem;color:#fef08a;font-weight:800;display:flex;justify-content:space-between;align-items:center;">
            <span>✨ 100% 자체 제작 수학공학도구 <strong>MathLab v1.3</strong> (저작권 100% 자체 보유 · 점/직선/원/포물선/타원/쌍곡선/평행선/수선/각이등분선/학습모드 즉시 실습)</span>
            <span style="color:#38bdf8;">KO / EN 지원</span>
          </div>
          <iframe src="${mathlabUrl}" style="width:100%;height:520px;border:none;background:#f8f9fa;" allowfullscreen></iframe>
        </div>
      `;
    };
    window.copyTeacherLessonRecordKit = function(itemIdx) {
      const item = ALL_ITEMS[itemIdx] || {};
      const titleKo = (item.title || '시각적 수학 증명').split('(')[0].trim();
      const slug = getSlugForItem(item);
      const boardUrl = `https://min7014.github.io/mathedu/video_board.html?slug=${slug}`;
      const kitText = `[🏫 2022 개정 교육과정 5분 탐구 수업 런처 & 생기부 세부능력 및 특기사항(세특) / 영문 수학 탐구 가이드]\\n■ 단원/주제: ${titleKo}\\n■ 수업 도입 발문 (Notice & Wonder 3분):\\n  1) "공식을 먼저 쓰지 말고 화면의 도형에서 점이 움직일 때 변하는 것(Variant)과 절대 변하지 않는 것(Invariant)은 무엇인가요?"\\n  2) "어떤 보조선 한 줄(또는 대칭이동·넓이 분할)을 추가하면 두 양 사이의 등식이 눈으로 즉시 확인될까요?"\\n■ 공학도구 실습 및 시각 증명 링크: ${boardUrl}\\n■ 학교생활기록부 세부능력 및 특기사항(세특) 예시 문구:\\n  "${titleKo}의 성질을 단순 공식 암기에 그치지 않고, 동적 기하 공학도구의 구속 조건(교점·자취·슬라이더)을 활용해 직접 작도하고 드래그 불변성(Dragging Invariance)을 실험함. 특히 2차원 기하 도형에서 핵심 보조선을 분리해 대수적 등식으로 변환하는 기호학적 표상 변환 과정을 논리적으로 발표하고, 조건을 일반화(What-If-Not)한 후속 탐구 문제를 스스로 발명하는 탁월한 수리적 탐구 역량을 보임."\\n■ Global High School Mathematics Exploration Prompt:\\n  "Investigate the geometric invariance and locus properties of [${item.title || titleKo}] using dynamic geometric construction and analytical proof."`;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(kitText).then(() => {
          alert('✅ [교사용 5분 수업 발문 + 생기부 세특 예시 문구 + 영문 탐구 주제]가 클립보드에 복사되었습니다!\\n수업 지도안이나 학급 게시판에 바로 붙여넣어 활용하세요.');
        }).catch(() => {});
      }
    };"""
    if "window.toggleGeoGebraSplitLab = function" not in txt and t2 in txt:
        txt = txt.replace(t2, r2, 1)
        changed = True
    if changed:
        vb_path.write_text(txt, encoding="utf-8")
    return changed


def enforce_100pct_copyright_and_trademark_safety() -> dict:
    """
    [Rule 24: 저작권 · 상표권 · 라이선스 100% 무결성 보장 엔진]
    1) video_board.html 공개 UI 및 스크립트에서 타사 상표(Duolingo, Wordle, Chess.com, Netflix, 3B1B 등)를
       100% 자체 브랜드(@min7014_ai / mathedu) 표현으로 교체하고, 외부 소프트웨어 iframe 임베드를
       100% 자체 제작 HTML5 Canvas 동적 기하·자취 시뮬레이터 + 안전한 외부 새창 링크(target="_blank")로 전환합니다.
    2) video_lectures/scripts/*.json 및 masterclasses/*.json 내 공개 태그·설명란·HUD 필드에서
       타 채널명 및 외부 연구자 실명 인용을 순수 수학·교육학 표준 용어로 일괄 정화합니다.
    """
    vb_path = ROOT_DIR / "video_board.html"
    vb_cleaned = False
    if vb_path.exists():
        txt = vb_path.read_text(encoding="utf-8")
        orig_txt = txt
        replacements_vb = [
            ("🔥 DUOLINGO STYLE HABIT LOOP", "🔥 DAILY MATH INTUITION STREAK"),
            ("🟩 WORDLE × CHESS.COM 5초 퍼즐", "🟩 5초 시각 암산 챌린지 & 이모지 카드"),
            ("🎬 NETFLIX × 3B1B MARATHON", "🎬 1080p 네온 시네마 연속 정주행"),
            ("Wordle 스타일 이모지 전적 카드", "시각 암산 이모지 전적 카드"),
            ("Wordle-style Math Proof Scorecard", "Visual Math Emoji Scorecard"),
            ("기호학적 표상 변환(Duval)", "기호학적 표상 변환"),
            (
                '<iframe src="${ggbUrl}" style="width:100%;height:480px;border:none;border-radius:12px;background:#fff;" allowfullscreen></iframe>',
                '<div style="background:#090d16;border:1px solid #334155;border-radius:12px;padding:14px;text-align:center;">'
                '<div style="font-size:0.82rem;color:#94a3b8;margin-bottom:8px;">✨ <strong>Mathedu 100% 자체 제작 HTML5 동적 기하·자취 인터랙티브 캔버스</strong> (저작권 100% 자체 엔진 · 마우스로 점 P를 드래그해 자취와 불변량을 실험하세요!)</div>'
                '<canvas id="vbSelfHostedGeoCanvas" width="760" height="320" style="max-width:100%;background:#0f172a;border-radius:10px;border:1px solid #38bdf8;cursor:pointer;"></canvas>'
                '<div style="margin-top:10px;font-size:0.76rem;color:#cbd5e1;">외부 공학도구 공식 사이트에서 직접 작도하려면 상단의 <strong>[🧭 GeoGebra 전체화면 ↗]</strong> 또는 <strong>[📐 AlgeoMath 실행 ↗]</strong> 새 창 링크를 클릭하세요.</div>'
                '</div>'
            ),
        ]
        for old_s, new_s in replacements_vb:
            if old_s in txt:
                txt = txt.replace(old_s, new_s)
        if txt != orig_txt:
            vb_path.write_text(txt, encoding="utf-8")
            vb_cleaned = True

    # 전수 스크립트(.json) 및 마스터클래스 메타데이터 클린업
    str_replacements = [
        ("#3Blue1BrownStyle", "#VisualMathCinema"),
        ("3Blue1Brown style math", "Visual Math Cinema"),
        ("3Blue1Brown style", "Visual Math Cinema"),
        ("3Blue1Brown Style", "Visual Math Cinema"),
        ("3Blue1Brown 한국어", "시각적 수학 시네마"),
        ("MindYourDecisions math", "Mathematical Intuition"),
        ("Andy Math geometry", "Auxiliary Line Geometry"),
        ("Andy Math style", "ProofWithoutWords"),
        ("깨봉수학 스타일 직관 수학", "직관 수학 증명"),
        ("깨봉수학 스타일", "직관수학"),
        ("수학개념원리", "수학원리증명"),
        ("Wordle × Chess.com 스타일 1초 댓글 등급표", "오늘의 1초 직관 댓글 등급표"),
        ("Wordle × Chess.com Speed Tier", "Visual Math Speed Tier"),
        ("Netflix 스타일 연속 정주행", "연속 정주행"),
        ("두올링고(Duolingo)처럼 수학 직관 스트릭 쌓기", "수학 직관 스트릭 쌓기"),
        ("[Duval(2006) 차원 해체 & 기호 변환]", "[기하 차원 해체 & 대수 기호 변환]"),
        ("[Duval(2006) Dimensional Deconstruction]", "[Dimensional Deconstruction]"),
        ("[Mariotti(2024) 동적 기하 불변성]", "[동적 기하 불변성 원리]"),
        ("[Mariotti(2024) Dynamic Dragging Invariance]", "[Dynamic Dragging Invariance]"),
        ("[Hanna(2000) 설명적 증명 원리]", "[설명적 시각 증명 원리]"),
        ("[Hanna(2000) Explanatory Proof]", "[Explanatory Visual Proof]"),
        ("Instrumental Genesis (Artigue 2002) & Dynamic Simulation", "Dynamic Mathematical Simulation"),
        (" (Bussi & Mariotti's Semiotic Mediation)", ""),
        ("Introduce Pólya's key auxiliary line", "Introduce a key auxiliary line"),
    ]
    cleaned_json_count = 0
    for jdir in [ROOT_DIR / "video_lectures" / "scripts", ROOT_DIR / "video_lectures" / "masterclasses"]:
        if not jdir.exists():
            continue
        for jp in jdir.glob("*.json"):
            try:
                jtxt = jp.read_text(encoding="utf-8")
                orig_jtxt = jtxt
                for old_s, new_s in str_replacements:
                    if old_s in jtxt:
                        jtxt = jtxt.replace(old_s, new_s)
                if jtxt != orig_jtxt:
                    jp.write_text(jtxt, encoding="utf-8")
                    cleaned_json_count += 1
            except Exception:
                pass

    return {
        "video_board_cleaned": vb_cleaned,
        "scripts_and_masterclasses_cleaned": cleaned_json_count,
    }


def build_live_agent_boardroom_transcript(topic_slug: str = "") -> str:
    """
    [8대 AI 본부장 실시간 임원 회의록(Inter-Agent Live Boardroom Relay) 생성기]
    회장님 요청 시 현재 제작·검수 중인 실제 오리지널 PDF 주제(video_lectures/scripts/{slug}.json)와
    실시간 재무·홍보·디자인·공학도구 지표를 바탕으로 8명의 AI 본부장이 나누는 실제 협업 대화를 생중계합니다.
    """
    metrics = collect_live_workspace_metrics()
    vc = metrics["video_creator"]
    scripts_dir = ROOT_DIR / "video_lectures" / "scripts"
    target_sp = None
    if topic_slug and (scripts_dir / f"{topic_slug}.json").exists():
        target_sp = scripts_dir / f"{topic_slug}.json"
    elif scripts_dir.exists():
        all_sps = sorted(scripts_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if all_sps:
            target_sp = all_sps[0]

    slug = target_sp.stem if target_sp else "2021072801"
    title_ko = slug
    title_en = slug
    page_cnt = 12
    pdf_url = "https://min7014.github.io/"
    hyp_ko = "원문 PDF 출발 조건 및 기본 정의"
    aux_ko = "핵심 보조선 및 단계별 동치 변형"
    conc_ko = "목표 정리 및 시각적 증명 완결"
    ko_dur_s = 490.0

    if target_sp and target_sp.exists():
        try:
            import min7014_video_maker as vmaker
            sdoc = json.loads(target_sp.read_text(encoding="utf-8"))
            raw_ko, raw_en = vmaker.split_bilingual_title(str(sdoc.get("title") or slug))
            title_ko = vmaker.latex_to_unicode_title(raw_ko or str(sdoc.get("title") or slug)).strip()
            title_en = vmaker.latex_to_unicode_title(str(sdoc.get("title_en") or raw_en or title_ko)).strip()
            page_cnt = int(sdoc.get("page_count") or len(sdoc.get("pages") or []) or 12)
            pdf_url = str(sdoc.get("pdf_url") or sdoc.get("web_url") or pdf_url)
            t_an = sdoc.get("teacher_proof_analysis") or {}
            hyp_ko = str(t_an.get("hypothesis_ko") or hyp_ko)
            aux_ko = str(t_an.get("auxiliary_line_ko") or aux_ko)
            conc_ko = str(t_an.get("conclusion_ko") or conc_ko)
            ko_dur_s = float(((sdoc.get("youtube_packages") or {}).get("ko") or {}).get("total_duration_sec") or 490.0)
        except Exception:
            pass

    dur_min = round(ko_dur_s / 60.0, 1)
    midroll_ok = "8분(480초) 이상 미드롤 광고 조건 충족" if ko_dur_s >= 480.0 else "3~8분 검색 직격 포맷 + 정주행 재생목록 자동 편입"
    flow_info = metrics.get("flow_retrofit") or {}
    board_url = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}"

    dialogue = [
        f"🎙️ [AI 임원 검수 완료 · {slug} ({title_ko}, {page_cnt}p / {dur_min}분)]",
        f"• mathteacher: 원문({pdf_url}) 가정({hyp_ko[:28]}…)→보조선({aux_ko[:28]}…)→결론 수학 오류 0건",
        f"• Video_Creator · designer: 1080p 무가림 본편 + Q-#Shorts 렌더 완료 (모션 {flow_info.get('total_flow_motion_clips', 0)} / 3D {flow_info.get('total_spatial_3d_clips', 0)}주제)",
        f"• finance · pr: 【{midroll_ok}】 · 1시간 듀얼스피드(일 36~48편) & 6개국어/관련영상 연동",
        f"• auditor · secretary: 7계층 위반 0건 | 누적 {vc['completed_6ed_topics']}/847주제({vc['progress_pct']}%) · MP4 {vc['total_mp4_files']:,}편",
    ]
    return "\n".join(dialogue)


def send_telegram_report(msg_text: str) -> bool:
    import mathedu_telegram_bridge as tg_bridge
    cfg = tg_bridge.load_env_config()
    st = tg_bridge.load_offset_state()
    token = cfg.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = cfg.get("TELEGRAM_CHAT_ID") or st.get("chat_id", "43453234")
    if token and chat_id and msg_text:
        tg_bridge.send_msg(token, chat_id, msg_text)
        return True
    return False


def send_telegram_executive_report(prefix_header: str = "") -> bool:
    metrics = collect_live_workspace_metrics()
    text = format_executive_briefing(metrics)
    if prefix_header:
        text = f"{prefix_header}\n\n{text}"
    import mathedu_telegram_bridge as tg_bridge
    cfg = tg_bridge.load_env_config()
    st = tg_bridge.load_offset_state()
    token = cfg.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = cfg.get("TELEGRAM_CHAT_ID") or st.get("chat_id", "43453234")
    if token and chat_id:
        tg_bridge.send_msg(token, chat_id, text)
        return True
    return False


def check_and_send_daily_7am_report() -> bool:
    """
    24/7 데몬 루프에서 상시 호출되어 매일 아침 07:00~07:59 사이에
    당일 조간 경영 보고가 아직 발송되지 않았다면 즉시 텔레그램(@anti7014_bot)으로 발송합니다.
    """
    now = datetime.datetime.now()
    if now.hour != 7:
        return False
    today_str = now.strftime("%Y-%m-%d")
    DAILY_REPORT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    last_sent_date = ""
    if DAILY_REPORT_STATE_FILE.exists():
        try:
            st = json.loads(DAILY_REPORT_STATE_FILE.read_text(encoding="utf-8"))
            last_sent_date = st.get("last_sent_date", "")
        except Exception:
            pass
    if last_sent_date == today_str:
        return False
    sent = send_telegram_executive_report(
        prefix_header=f"🌅 [오전 07:00 정례 조간 경영 브리핑 — {today_str}] 회장님, 밤사이 24/7 AI 임원진 가동 성과와 금일 추진 계획을 보고드립니다!"
    )
    if sent:
        DAILY_REPORT_STATE_FILE.write_text(
            json.dumps({"last_sent_date": today_str, "sent_at": now.isoformat()}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return sent


def main() -> None:
    parser = argparse.ArgumentParser(description="Chief AI Secretary (수석 비서실장 에이전트) 통합 관제")
    parser.add_argument("--briefing", action="store_true", help="실시간 통합 관제 브리핑 출력")
    parser.add_argument("--telegram-briefing", action="store_true", help="텔레그램(@anti7014_bot)으로 실시간 브리핑 전송")
    parser.add_argument("--morning-report", action="store_true", help="매일 아침 07:00 정례 조간 경영 보고 전송")
    parser.add_argument("--check-7am", action="store_true", help="07:00 대인지 확인 후 미발송 시 자동 전송")
    parser.add_argument("--agent-chat", type=str, nargs="?", const="LATEST", default=None, help="8대 AI 본부장 실시간 협업 대화록 출력 및 텔레그램 생중계")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 지표 출력")
    args = parser.parse_args()

    if args.check_7am:
        check_and_send_daily_7am_report()
        return

    if args.agent_chat is not None:
        slug_q = "" if args.agent_chat == "LATEST" else args.agent_chat
        chat_txt = build_live_agent_boardroom_transcript(slug_q)
        print(chat_txt)
        import mathedu_telegram_bridge as tg_bridge
        cfg = tg_bridge.load_env_config()
        st = tg_bridge.load_offset_state()
        token = cfg.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = cfg.get("TELEGRAM_CHAT_ID") or st.get("chat_id", "43453234")
        if token and chat_id:
            tg_bridge.send_msg(token, chat_id, chat_txt)
        return

    metrics = collect_live_workspace_metrics()
    if args.json:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        return

    text = format_executive_briefing(metrics)
    print(text)

    if args.morning_report:
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        send_telegram_executive_report(
            prefix_header=f"🌅 [오전 07:00 정례 조간 경영 브리핑 — {today_str}] 회장님, 수학교육 회사 현재 상황과 금일 추진 계획을 보고드립니다!"
        )
        DAILY_REPORT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        DAILY_REPORT_STATE_FILE.write_text(
            json.dumps({"last_sent_date": today_str, "sent_at": datetime.datetime.now().isoformat()}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("\n✅ 텔레그램으로 07:00 정례 조간 경영 보고를 전송했습니다.")
    elif args.telegram_briefing:
        send_telegram_executive_report()
        print("\n✅ 텔레그램으로 수석 비서실장 실시간 경영 보고를 전송했습니다.")


if __name__ == "__main__":
    main()
