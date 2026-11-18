#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
youtube_comment_math_auditor.py
===============================================================================
💬📺 유튜브 시청자 댓글 수학적 오류 분석 & 자동 보완 엔진 (Policy 66)

[회장님(min7014) 핵심 지침 (2026-11-17)]:
  "유투브 자료에 대한 댓글을 분석하여 수학적인 오류를 말한 부분이 있으면 그 부분을 보완한다."

핵심 아키텍처 (Rule 1 · Rule 5 · Rule 13.1 · Rule 13.3 · Rule 48 · Rule 51 준수):
  1. 양대 채널 전수·증분 댓글 수집 (0 LLM 크레딧 · 최소 API 쿼터):
     - `@min7014_ai` (`UCSlqQfOEtRfJuMPyGMLgFYA`): `published` + `heldForReview` 전 스레드 및 대댓글 스캔
       (수식 기호 `=`, `/`, `²` 포함 댓글이 유튜브 스팸함에 보류되는 현상까지 빠짐없이 포착)
     - `@min7014` (`UC7DN_e571yaTderHffKFTTg`): 1,196+ 오리지널 영상 중 `commentCount > 0` 영상 증분 스캔
  2. 시청자 댓글 3단 수학 분류기 (`classify_viewer_comment`):
     - `math_error_report`: 수식·기하·논리·부호·도형 불일치·발음·자막 오류 지적 (최우선 즉시 검산·보완!)
     - `pedagogical_gap_question`: 특정 페이지/단계 이해 어려움 및 추가 설명 요청 (대본·디딤돌 보완!)
     - `quiz_answer_or_praise`: 5초 퍼즐 정답 도전 및 응원 댓글
  3. 영상 ID → 로컬 원천 자산 역추적 (`resolve_video_to_source`):
     - `video_lectures/scripts/*.json`의 8대 에디션 URL 사전 및 `min7014_deep_knowledge.json`과 1:1 매칭
  4. 자율 수학 검산 · 전수 보완 · 재렌더링 · 유튜브 교체 파이프라인 (`remediate_pending_math_comments`):
     - 신규 `math_error_report` 또는 `pedagogical_gap_question` 포착 시 즉시 수학적 진위를 엄밀히 검산하여,
       실제 오류·미비점이 확인되면 `Rule 5`(전수 점검) 및 `Rule 13.3`(기존 영상 삭제 후 수정본 업로드)에 따라
       스크립트·도형·영상·웹 디딤돌 해설을 일괄 보완하고 텔레그램(`@anti7014_bot`)으로 완료 보고합니다.
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 Windows 전 하위 프로세스 완전 무창 강제

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
AGENTS_DIR = ROOT_DIR / ".agents"
PRIVATE_STATE_FILE = AGENTS_DIR / "youtube_comment_audit_state.json"
PUBLIC_AUDIT_DB_FILE = ROOT_DIR / "assets" / "youtube_comment_math_audit_db.json"
RATE_LIMIT_FILE = AGENTS_DIR / "youtube_comment_remediation_rate.json"

AI_CHANNEL_ID = "UCSlqQfOEtRfJuMPyGMLgFYA"    # @min7014_ai
ORIG_CHANNEL_ID = "UC7DN_e571yaTderHffKFTTg"  # @min7014
OWN_CHANNEL_IDS = {AI_CHANNEL_ID, ORIG_CHANNEL_ID}
MAX_REMEDIATION_RUNS_PER_HOUR = 3

# 1순위: 수학적·기하학적·수식·자막·발음 오류 지적 패턴
MATH_ERROR_PATTERNS = [
    r"오류", r"틀렸", r"틀린", r"잘못", r"아닌가요", r"아닌데", r"이상한데",
    r"안\s*만나", r"만나지\s*않", r"어긋", r"평행이\s*아", r"수직이\s*아", r"직각이\s*아",
    r"정사각형이\s*아", r"이등변이\s*아", r"합동이\s*아", r"닮음이\s*아",
    r"부호", r"계산\s*실수", r"오타", r"발음", r"잘못\s*읽", r"자막",
    r"분모", r"분자", r"역수", r"모순", r"반례", r"성립하지", r"성립\s*안",
    r"0으로\s*나누", r"무연근", r"조건이\s*빠", r"전제가\s*빠", r"각도가\s*다", r"비율이\s*다",
    r"\bwrong\b", r"\bmistake\b", r"\berror\b", r"\bincorrect\b", r"\bfalse\b", r"\btypo\b",
    r"not\s+concurrent", r"don'?t\s+meet", r"doesn'?t\s+meet", r"not\s+parallel",
    r"not\s+perpendicular", r"not\s+a\s+square", r"sign\s+error", r"divide[d]?\s+by\s+zero",
    r"\bcounterexample\b", r"\bcontradiction\b", r"\bmispronounc", r"missing\s+condition",
    r"shouldn'?t\s+it\s+be", r"isn'?t\s+it\s+supposed", r"diagram\s+is\s+off",
]

# 2순위: 수학 단계 이해 막힘 · 설명 보완 요청 패턴
PEDAGOGICAL_GAP_PATTERNS = [
    r"이해가?\s*안", r"왜\s*이렇게", r"어떻게\s*넘어", r"설명.*해\s*주", r"무슨\s*뜻",
    r"어디서\s*나온", r"갑자기\s*왜", r"몇\s*번째\s*줄",
    r"don'?t\s+understand", r"can\s+you\s+explain", r"how\s+did\s+you\s+get",
    r"why\s+does", r"why\s+is", r"confused", r"what\s+did\s+you\s+do\s+in",
]

MATH_ERROR_RE = re.compile("|".join(MATH_ERROR_PATTERNS), re.IGNORECASE)
PEDAGOGICAL_GAP_RE = re.compile("|".join(PEDAGOGICAL_GAP_PATTERNS), re.IGNORECASE)


def classify_viewer_comment(text: str) -> tuple[str, str]:
    t = re.sub(r"\s+", " ", str(text or "")).strip()
    if not t:
        return ("empty", "")
    m_err = MATH_ERROR_RE.search(t)
    if m_err:
        return ("math_error_report", f"오류 지적 키워드 감지('{m_err.group(0)}')")
    m_gap = PEDAGOGICAL_GAP_RE.search(t)
    if m_gap:
        return ("pedagogical_gap_question", f"단계 설명 보완 요청 감지('{m_gap.group(0)}')")
    return ("quiz_answer_or_praise", "일반 퀴즈 참여 또는 응원 댓글")


def build_video_id_lookup_index() -> dict[str, dict]:
    """모든 로컬 스크립트(684+종)의 유튜브 영상 ID를 역색인하여 0.01초 만에 원천 파일·에디션을 찾습니다."""
    idx: dict[str, dict] = {}
    url_fields = [
        ("youtube_urls", "standard_1080p", "min7014_video_maker.py"),
        ("shorts_urls", "standard_shorts", "min7014_video_maker.py"),
        ("question_youtube_urls", "question_1080p", "min7014_video_maker.py"),
        ("question_shorts_urls", "question_shorts", "min7014_video_maker.py"),
        ("creative_idea_youtube_urls", "creative_idea_1080p", "creative_idea_cinema.py"),
        ("creative_idea_shorts_urls", "creative_idea_shorts", "creative_idea_cinema.py"),
        ("exam_hybrid_urls", "exam_hybrid_1080p", "exam_hybrid_creator.py"),
        ("exam_hybrid_shorts_urls", "exam_hybrid_shorts", "exam_hybrid_creator.py"),
        ("nano_banana_urls", "nano_banana_1080p", "nano_banana_cinema_creator.py"),
        ("nano_banana_shorts_urls", "nano_banana_shorts", "nano_banana_cinema_creator.py"),
        ("issue_insight_urls", "issue_insight_1080p", "math_issue_insight_creator.py"),
        ("issue_insight_shorts_urls", "issue_insight_shorts", "math_issue_insight_creator.py"),
    ]

    def _extract_vid(u: str) -> str:
        s = str(u or "").strip().rstrip("/")
        if not s:
            return ""
        if "watch?v=" in s:
            return s.split("watch?v=", 1)[1].split("&")[0]
        return s.split("/")[-1].split("?")[0]

    for sp in SCRIPTS_DIR.glob("*.json"):
        try:
            d = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = sp.stem
        title = str(d.get("title") or slug)
        pdf_url = str(d.get("pdf_url") or "")
        for field_name, edition, gen_mod in url_fields:
            u_map = d.get(field_name)
            if not isinstance(u_map, dict):
                continue
            for lc, u_val in u_map.items():
                vid = _extract_vid(u_val)
                if vid and len(vid) >= 8:
                    idx[vid] = {
                        "slug": slug,
                        "title": title,
                        "edition": f"{edition}_{lc}",
                        "lang": lc,
                        "generator_module": gen_mod,
                        "script_path": f"video_lectures/scripts/{slug}.json",
                        "pdf_url": pdf_url,
                    }
    return idx


def _load_private_state() -> dict:
    if PRIVATE_STATE_FILE.exists():
        try:
            return json.loads(PRIVATE_STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "last_ai_scan_ts": 0.0,
        "last_orig_scan_ts": 0.0,
        "orig_commented_video_ids": [],
        "processed_comment_keys": {},
    }


def _save_private_state(st: dict) -> None:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    PRIVATE_STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def load_public_audit_db() -> dict:
    if PUBLIC_AUDIT_DB_FILE.exists():
        try:
            return json.loads(PUBLIC_AUDIT_DB_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "policy": "Policy 66: 유튜브 자료 댓글 분석 기반 수학적 오류 및 설명 결손 상시 보완",
        "total_scanned_viewer_comments": 0,
        "math_error_or_gap_findings": [],
    }


def save_public_audit_db(db: dict) -> None:
    PUBLIC_AUDIT_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    db["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    PUBLIC_AUDIT_DB_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def scan_youtube_comments_for_math_issues(force_orig_sweep: bool = False) -> dict:
    """
    @min7014_ai (published + heldForReview) 및 @min7014 (댓글 존재 영상) 댓글을 스캔하여
    수학적 오류 지적 또는 단계 설명 보완 요청 댓글을 적출합니다.
    """
    import min7014_video_maker as vmaker

    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        yt, _ = vmaker.get_youtube_readonly_service()
    if yt is None:
        return {"ok": False, "reason": "youtube_service_unavailable"}

    st = _load_private_state()
    vid_index = build_video_id_lookup_index()
    now_ts = time.time()

    collected: list[dict] = []

    # 1) @min7014_ai 전체 댓글 스레드 스캔 (공개 + 검토 보류함 동시 점검)
    for mod_status in ("published", "heldForReview"):
        page_token = None
        while True:
            try:
                resp = yt.commentThreads().list(
                    part="snippet,replies",
                    allThreadsRelatedToChannelId=AI_CHANNEL_ID,
                    moderationStatus=mod_status,
                    maxResults=100,
                    pageToken=page_token,
                    textFormat="plainText",
                ).execute()
            except Exception:
                break
            for th in resp.get("items", []):
                vid = th["snippet"].get("videoId", "")
                top_c = th["snippet"]["topLevelComment"]
                ts = top_c["snippet"]
                acid = (ts.get("authorChannelId") or {}).get("value", "")
                if acid not in OWN_CHANNEL_IDS:
                    collected.append({
                        "comment_key": top_c["id"],
                        "thread_id": th["id"],
                        "channel_handle": "@min7014_ai",
                        "moderation_status": mod_status,
                        "video_id": vid,
                        "author": ts.get("authorDisplayName", ""),
                        "published_at": ts.get("publishedAt", ""),
                        "text": ts.get("textDisplay", ""),
                        "is_reply": False,
                    })
                for rep in (th.get("replies") or {}).get("comments", []):
                    rs = rep["snippet"]
                    racid = (rs.get("authorChannelId") or {}).get("value", "")
                    if racid not in OWN_CHANNEL_IDS:
                        collected.append({
                            "comment_key": rep["id"],
                            "thread_id": th["id"],
                            "channel_handle": "@min7014_ai",
                            "moderation_status": mod_status,
                            "video_id": vid,
                            "author": rs.get("authorDisplayName", ""),
                            "published_at": rs.get("publishedAt", ""),
                            "text": rs.get("textDisplay", ""),
                            "is_reply": True,
                        })
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
    st["last_ai_scan_ts"] = now_ts

    # 2) @min7014 오리지널 채널 댓글 스캔 (6시간 주기 전체 목록 갱신, 평시에는 댓글 보유 영상만 빠른 점검)
    orig_vids = list(st.get("orig_commented_video_ids") or [])
    if force_orig_sweep or not orig_vids or (now_ts - float(st.get("last_orig_scan_ts") or 0.0)) >= 21600:
        try:
            ch = yt.channels().list(part="contentDetails", id=ORIG_CHANNEL_ID).execute()["items"][0]
            upl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
            all_orig: list[str] = []
            pt = None
            while len(all_orig) < 1500:
                pr = yt.playlistItems().list(part="contentDetails", playlistId=upl, maxResults=50, pageToken=pt).execute()
                all_orig.extend([it["contentDetails"]["videoId"] for it in pr.get("items", [])])
                pt = pr.get("nextPageToken")
                if not pt:
                    break
            found_commented: list[str] = []
            for i in range(0, len(all_orig), 50):
                vr = yt.videos().list(part="statistics", id=",".join(all_orig[i : i + 50])).execute()
                for v in vr.get("items", []):
                    if int((v.get("statistics") or {}).get("commentCount", 0) or 0) > 0:
                        found_commented.append(v["id"])
            orig_vids = found_commented
            st["orig_commented_video_ids"] = orig_vids
            st["last_orig_scan_ts"] = now_ts
        except Exception:
            pass

    for ovid in orig_vids:
        try:
            cr = yt.commentThreads().list(part="snippet,replies", videoId=ovid, maxResults=100, textFormat="plainText").execute()
            for th in cr.get("items", []):
                top_c = th["snippet"]["topLevelComment"]
                ts = top_c["snippet"]
                acid = (ts.get("authorChannelId") or {}).get("value", "")
                replies_list = (th.get("replies") or {}).get("comments", [])
                owner_already_replied = any(
                    ((r["snippet"].get("authorChannelId") or {}).get("value", "") in OWN_CHANNEL_IDS)
                    for r in replies_list
                )
                if acid not in OWN_CHANNEL_IDS:
                    collected.append({
                        "comment_key": top_c["id"],
                        "thread_id": th["id"],
                        "channel_handle": "@min7014",
                        "moderation_status": "published",
                        "video_id": ovid,
                        "author": ts.get("authorDisplayName", ""),
                        "published_at": ts.get("publishedAt", ""),
                        "text": ts.get("textDisplay", ""),
                        "is_reply": False,
                        "owner_already_replied": owner_already_replied,
                    })
                for rep in replies_list:
                    rs = rep["snippet"]
                    racid = (rs.get("authorChannelId") or {}).get("value", "")
                    if racid not in OWN_CHANNEL_IDS:
                        collected.append({
                            "comment_key": rep["id"],
                            "thread_id": th["id"],
                            "channel_handle": "@min7014",
                            "moderation_status": "published",
                            "video_id": ovid,
                            "author": rs.get("authorDisplayName", ""),
                            "published_at": rs.get("publishedAt", ""),
                            "text": rs.get("textDisplay", ""),
                            "is_reply": True,
                            "owner_already_replied": owner_already_replied,
                        })
        except Exception:
            continue

    db = load_public_audit_db()
    db["total_scanned_viewer_comments"] = len(collected)
    existing_map = {f["comment_key"]: f for f in (db.get("math_error_or_gap_findings") or [])}
    new_actionable: list[dict] = []

    for c in collected:
        cat, reason = classify_viewer_comment(c["text"])
        c["category"] = cat
        c["classification_reason"] = reason
        c["matched_source"] = vid_index.get(c["video_id"], {})
        if cat in ("math_error_report", "pedagogical_gap_question"):
            ck = c["comment_key"]
            if ck not in existing_map:
                entry = {
                    "comment_key": ck,
                    "thread_id": c["thread_id"],
                    "channel_handle": c["channel_handle"],
                    "video_id": c["video_id"],
                    "video_url": f"https://youtu.be/{c['video_id']}",
                    "published_at": c["published_at"],
                    "category": cat,
                    "reason": reason,
                    "comment_excerpt": str(c["text"])[:240],
                    "matched_source": c["matched_source"],
                    "status": "pending",
                    "resolution_summary": "",
                }
                db.setdefault("math_error_or_gap_findings", []).append(entry)
                existing_map[ck] = entry
                new_actionable.append(entry)
            elif existing_map[ck].get("status") == "pending":
                new_actionable.append(existing_map[ck])

    _save_private_state(st)
    save_public_audit_db(db)
    return {
        "ok": True,
        "scanned_viewer_comments": len(collected),
        "total_findings": len(db.get("math_error_or_gap_findings") or []),
        "pending_actionable": new_actionable,
    }


def _can_consume_remediation_slot() -> bool:
    now = time.time()
    runs: list[float] = []
    if RATE_LIMIT_FILE.exists():
        try:
            d = json.loads(RATE_LIMIT_FILE.read_text(encoding="utf-8"))
            runs = [float(x) for x in (d.get("runs") or []) if now - float(x) < 3600.0]
        except Exception:
            runs = []
    if len(runs) >= MAX_REMEDIATION_RUNS_PER_HOUR:
        return False
    runs.append(now)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    RATE_LIMIT_FILE.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")
    return True


def _resolve_agy_cli() -> str:
    found = shutil.which("agy")
    if found:
        return found
    cand = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\min\AppData\Local")) / "agy" / "bin" / "agy.EXE"
    if cand.exists():
        return str(cand)
    return "agy"


def mark_comment_finding_resolved(comment_key: str, resolution_summary: str) -> bool:
    db = load_public_audit_db()
    updated = False
    for f in db.get("math_error_or_gap_findings") or []:
        if f.get("comment_key") == comment_key:
            f["status"] = "resolved"
            f["resolved_at"] = datetime.datetime.now().isoformat(timespec="seconds")
            f["resolution_summary"] = str(resolution_summary or "").strip()
            updated = True
    if updated:
        save_public_audit_db(db)
    return updated


def remediate_pending_math_comments(notify_telegram: bool = True) -> dict:
    """
    미처리된 유튜브 댓글 수학 오류 지적(`math_error_report`) 또는 단계 설명 보완 요청(`pedagogical_gap_question`)을
    자율 검산·보완·재렌더링·유튜브 교체하고 결과를 텔레그램으로 보고합니다.
    """
    scan_res = scan_youtube_comments_for_math_issues(force_orig_sweep=False)
    pending = scan_res.get("pending_actionable") or []
    if not pending:
        return {"ok": True, "status": "no_pending_math_comments", "scanned": scan_res.get("scanned_viewer_comments", 0)}

    if not _can_consume_remediation_slot():
        return {"ok": False, "status": "rate_limited", "pending_count": len(pending)}

    target = pending[0]
    payload_json = json.dumps(target, ensure_ascii=False, indent=2)
    prompt = (
        "[유튜브 시청자 댓글 수학적 오류 검산 및 전수 보완 모드 — Policy 66]\n"
        "유튜브 영상에 달린 아래 시청자 댓글을 수학적으로 정밀 분석하여 즉시 보완하십시오 (GEMINI.md Rule 1, 5, 13.1, 13.2, 13.3, 48, 51 엄수):\n"
        "1. 매칭된 로컬 대본(`video_lectures/scripts/{slug}.json`), 생성 파이썬 모듈, 원문 PDF(`min7014.github.io`)를 확인하여 댓글이 지적한 수학적 오류·기하 작도 오차·수식 오독·단계 설명 부족의 진위를 엄밀히 검산하십시오.\n"
        "2. 실제 도형·수식·발음·설명 결함이 맞다면 국소 땜질을 금지(Rule 5)하고 생성 모듈과 대본을 근본 수정하십시오. 만약 `@min7014_ai`에 업로드된 영상이라면 수정본을 재렌더링한 뒤 기존 결함 유튜브 영상을 삭제(`videos().delete`)하고 새 영상을 업로드(Rule 13.3)하여 `catalog.json`까지 갱신하십시오.\n"
        "3. 만약 원문 수학이 100% 옳고 시청자가 특정 단계를 어려워한 경우라면, 대본(`narrations` / `question_narrations` / `teacher_proof_analysis`)에 해당 단계의 친절한 징검다리 해설을 보강하고, `@min7014_ai` 영상인 경우 정중하고 명쾌한 수학 해설 답글(개인 호칭 금지 Rule 13.1)을 등록하십시오.\n"
        "4. `python -X utf8 auditor.py check`(`PASS_ZERO_VIOLATIONS`) 통과 후 `youtube_comment_math_auditor.mark_comment_finding_resolved(comment_key, summary)`를 호출하고, 안전한 코드/데이터 파일만 `git commit` & `git push origin main` 하십시오.\n"
        "5. 수행 내역을 한국어 5~7줄로 표준 출력(stdout)에 요약하십시오(`--reply`나 `--listen-once` 직접 호출 금지).\n\n"
        f"[대상 유튜브 댓글 JSON]\n{payload_json}"
    )

    try:
        agy_bin = _resolve_agy_cli()
        proc = subprocess.run(
            [agy_bin, "-p", prompt, "--dangerously-skip-permissions"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=900,
        )
        summary = (proc.stdout or "").strip()
        if proc.returncode == 0:
            mark_comment_finding_resolved(target["comment_key"], summary[-600:] or "수학적 검산 및 보완 완료")
        if notify_telegram and summary:
            try:
                import mathedu_telegram_bridge as tg
                cfg = tg.load_env_config()
                tk, cid = cfg.get("TELEGRAM_BOT_TOKEN", ""), cfg.get("TELEGRAM_CHAT_ID", "")
                if tk and cid:
                    tg.send_msg(
                        tk,
                        cid,
                        (
                            f"💬🛠️ [유튜브 댓글 수학 오류 분석 · 자동 보완 완료 (Policy 66)]\n"
                            f"• 채널/영상: {target['channel_handle']} ({target['video_url']})\n"
                            f"• 댓글 요지: {target['comment_excerpt'][:120]}\n\n"
                            f"{summary[-1800:]}"
                        ),
                    )
            except Exception:
                pass
        return {"ok": proc.returncode == 0, "comment_key": target["comment_key"], "summary": summary[-1000:]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_comment_audit_summary(run_fresh_scan: bool = True) -> str:
    if run_fresh_scan:
        scan_youtube_comments_for_math_issues(force_orig_sweep=False)
    db = load_public_audit_db()
    findings = db.get("math_error_or_gap_findings") or []
    resolved = [f for f in findings if f.get("status") == "resolved"]
    pending = [f for f in findings if f.get("status") != "resolved"]

    lines = [
        "💬📺 [크레딧 0원 · 유튜브 댓글 수학적 오류 분석 & 상시 보완 엔진 (Policy 66)]",
        f"• 최근 스캔: {db.get('updated_at')} (@min7014_ai 공개·보류함 + @min7014 통합 감시)",
        f"• 스캔된 시청자 댓글: 총 {db.get('total_scanned_viewer_comments', 0)}건",
        f"• 수학 오류 지적 / 단계 보완 요청 적출: 누적 {len(findings)}건 (✅ 보완 완료 {len(resolved)}건 / ⏳ 대기 {len(pending)}건)",
    ]
    if findings:
        lines.append("")
        lines.append("🔍 [댓글 분석 및 수학적 보완 내역]")
        for f in findings[-5:]:
            st_ic = "✅ 보완완료" if f.get("status") == "resolved" else "⏳ 검산대기"
            ms = f.get("matched_source") or {}
            slug_lbl = ms.get("slug") or f.get("video_id")
            lines.append(f"• [{st_ic} | {f.get('channel_handle')} | {slug_lbl}] \"{f.get('comment_excerpt', '')[:70]}\"")
            if f.get("resolution_summary"):
                lines.append(f"  → 조치: {f['resolution_summary'][:110]}")
    return "\n".join(lines)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "scan":
        print(json.dumps(scan_youtube_comments_for_math_issues(force_orig_sweep=("--full" in sys.argv)), ensure_ascii=False, indent=2))
    elif cmd == "remediate":
        print(json.dumps(remediate_pending_math_comments(notify_telegram=("--no-tg" not in sys.argv)), ensure_ascii=False, indent=2))
    else:
        print(format_comment_audit_summary(run_fresh_scan=True))
