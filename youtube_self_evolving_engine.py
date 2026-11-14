import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
CLUSTER_WEIGHTS_FILE = ROOT_DIR / "youtube_uploads" / "self_evolving_cluster_weights.json"
PLAYLIST_STATE_FILE = ROOT_DIR / ".agents" / "playlist_synced_state.json"
LOCALIZATION_STATE_FILE = ROOT_DIR / ".agents" / "localized_videos_state.json"
CTR_DOCTOR_STATE_FILE = ROOT_DIR / ".agents" / "ctr_doctor_state.json"

TOPIC_CLUSTERS = {
    "circle_angles_tangent": ("원주각", "중심각", "접선", "접현각", "현", "활꼴", "원 내접", "inscribed angle", "central angle", "tangent", "chord", "circle"),
    "triangle_isosceles_congruence": ("이등변", "정삼각형", "합동", "닮음", "외심", "내심", "무게중심", "수심", "방심", "isosceles", "congruence", "similarity", "circumcenter", "incenter", "centroid"),
    "pythagoras_area_shear": ("피타고라스", "정사각형", "등적변형", "넓이", "히포크라테스", "pythagor", "area", "hypotenuse"),
    "ceva_menelaus_ratios": ("체바", "메넬라우스", "스튜어트", "파푸스", "중선", "내분", "외분", "각의 이등분선", "ceva", "menelaus", "stewart", "bisector"),
    "quadratic_inequality_algebra": ("이차부등식", "이차함수", "근의 공식", "판별식", "인수분해", "절댓값", "산술", "코시", "quadratic", "inequality", "parabola", "discriminant", "cauchy"),
    "sequences_induction": ("수열", "등차", "등비", "귀납법", "시그마", "자연수 거듭제곱", "피보나치", "arithmetic sequence", "geometric sequence", "induction", "fibonacci"),
    "calculus_limits_mvt": ("극한", "미분", "도함수", "평균값", "롤의 정리", "중간값", "접선의 방정식", "정적분", "limit", "derivative", "mean value", "rolle", "integral"),
    "conics_vectors": ("포물선", "타원", "쌍곡선", "초점", "준선", "이차곡선", "벡터", "정사영", "삼수선", "parabola", "ellipse", "hyperbola", "focus", "vector"),
}

CURATED_PLAYLIST_SPECS = [
    {
        "key": "ko_exam_killer",
        "lang": "ko",
        "title": "🎯 [도형·미적분 5초 해법] 공식 암기 타파 보조선 1줄 시각적 증명 정주행 | @min7014_ai",
        "desc": "방정식 세우다 시간 뺏기는 단골 도형·기하 함정 구조를 100% 자체 작도 보조선 시각 증명으로 5초 만에 꿰뚫는 정주행 재생목록입니다.",
        "match_clusters": ("circle_angles_tangent", "ceva_menelaus_ratios", "triangle_isosceles_congruence", "pythagoras_area_shear"),
    },
    {
        "key": "ko_algebra_calc",
        "lang": "ko",
        "title": "📈 [수열·이차부등식·미적분] 공식 암기 타파 5분 시각적 증명 정주행 | @min7014_ai",
        "desc": "무작정 외우던 등차·등비수열, 이차부등식, 평균값 정리, 미분·적분 핵심 원리를 도형과 그래프로 한눈에 이해하는 고효율 정주행 코스입니다.",
        "match_clusters": ("quadratic_inequality_algebra", "sequences_induction", "calculus_limits_mvt", "conics_vectors"),
    },
    {
        "key": "en_visual_geometry",
        "lang": "en",
        "title": "🔥 [Visual Geometry & Calculus] 5-Second Auxiliary Line Proofs (1080p) | @min7014_ai",
        "desc": "Stop memorizing formulas blindly! Master essential geometry, algebra, and calculus theorems through 100% original step-by-step visual proofs (https://min7014.github.io/).",
        "match_clusters": tuple(TOPIC_CLUSTERS.keys()),
    },
]


def sanitize_copyright_and_trademark_text(text: str) -> str:
    """
    [Rule 24 & Rule 51 — 저작권·상표권 무결성 기계적 가드레일]
    College Board(SAT, AP), MAA(AMC, AIME), IBO(IB), IMO/Olympiad 및 타사 브랜드 상표를
    100% 순수 일반 수학 학술 용어로 자동 치환합니다.
    """
    s = str(text or "")
    replacements = [
        (r"\[SAT\s*&\s*Olympiad\s*Math\]", "[Visual Geometry & Calculus]"),
        (r"\bSAT\s*&\s*Olympiad\b", "Visual Geometry & Algebra"),
        (r"\bSAT\s*Math\s*Prep\b", "High School Math Proof"),
        (r"\bSAT\s*Math\b", "Visual Math"),
        (r"\bSAT\b", "Geometry & Algebra"),
        (r"\bAP\s*Calculus\b", "Calculus Visual Proof"),
        (r"\bAMC\s*Math\b", "Problem Solving Math"),
        (r"\bAIME\b", "Advanced Math"),
        (r"\bAMC\b", "Deductive Math"),
        (r"\bIB\s*Math\b", "Advanced High School Math"),
        (r"\bMath\s*Olympiad\b", "Advanced Geometry"),
        (r"\bOlympiad[- ]grade\b", "Advanced"),
        (r"\bOlympiad\b", "Advanced"),
        (r"\bIMO\b", "Advanced Geometry"),
        (r"#SATMath\b", "#VisualMath"),
        (r"#OlympiadMath\b", "#GeometryProof"),
        (r"#MathOlympiad\b", "#EuclideanGeometry"),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", s).strip()


# Alias for cross-module callers (Rule 51)
sanitize_trademark_free_text = sanitize_copyright_and_trademark_text


def classify_text_cluster(text: str) -> str:
    low = (text or "").lower()
    for c_key, kws in TOPIC_CLUSTERS.items():
        if any(kw.lower() in low for kw in kws):
            return c_key
    return "general_visual_proof"


def compute_winning_cluster_weights(yt_service=None) -> dict:
    """
    [0-크레딧 자율 진화 엔진 #1 — 다윈식 승자 클러스터 가중치 학습기]
    채널의 실제 조회 속도( 일평균 조회수 = views / days_live )를 코호트·단원 클러스터별로 계산하여,
    유튜브 알고리즘이 현재 가장 강하게 밀어주는 단원 클러스터에 최대 3.5배 우선순위를 자동 부여합니다.
    """
    cluster_stats = {k: {"videos": 0, "views": 0, "velocity_sum": 0.0} for k in TOPIC_CLUSTERS}
    cluster_stats["general_visual_proof"] = {"videos": 0, "views": 0, "velocity_sum": 0.0}

    try:
        if yt_service is None:
            import min7014_video_maker as vm
            yt_service, _ = vm.get_available_youtube_upload_service()
        if yt_service is not None:
            ch = yt_service.channels().list(part="contentDetails", mine=True).execute()["items"][0]
            uploads_pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
            vids = []
            tok = None
            for _ in range(4):
                resp = yt_service.playlistItems().list(part="snippet,contentDetails", playlistId=uploads_pl, maxResults=50, pageToken=tok).execute()
                vids.extend(resp.get("items", []))
                tok = resp.get("nextPageToken")
                if not tok:
                    break
            now_utc = datetime.now(timezone.utc)
            for i in range(0, len(vids), 50):
                chunk = vids[i : i + 50]
                id_map = {it["contentDetails"]["videoId"]: it["snippet"] for it in chunk}
                st_items = yt_service.videos().list(part="statistics", id=",".join(id_map.keys())).execute().get("items", [])
                for st_it in st_items:
                    vid = st_it["id"]
                    snip = id_map.get(vid, {})
                    title = snip.get("title", "")
                    pub_str = snip.get("publishedAt", "")
                    days = 3.0
                    try:
                        dt = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                        days = max(0.5, (now_utc - dt).total_seconds() / 86400.0)
                    except Exception:
                        pass
                    vw = int((st_it.get("statistics") or {}).get("viewCount", 0))
                    c_key = classify_text_cluster(title)
                    cluster_stats[c_key]["videos"] += 1
                    cluster_stats[c_key]["views"] += vw
                    cluster_stats[c_key]["velocity_sum"] += (vw / days)
    except Exception:
        pass

    ranked = []
    for k, d in cluster_stats.items():
        cnt = max(1, d["videos"])
        avg_vel = round(d["velocity_sum"] / cnt, 3)
        avg_vw = round(d["views"] / cnt, 2)
        ranked.append((avg_vel, avg_vw, k, d["videos"], d["views"]))
    ranked.sort(reverse=True)

    max_vel = max(0.5, ranked[0][0]) if ranked else 1.0
    weights = {}
    for avg_vel, avg_vw, k, v_cnt, tot_vw in ranked:
        # 최소 1.0 ~ 최대 3.5배 부스트
        boost = round(1.0 + 2.5 * min(1.0, avg_vel / max_vel), 2) if v_cnt > 0 else 1.2
        weights[k] = {
            "boost_multiplier": boost,
            "avg_views_per_day": avg_vel,
            "avg_views": avg_vw,
            "videos": v_cnt,
            "total_views": tot_vw,
        }

    out = {
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "top_3_clusters": [r[2] for r in ranked[:3]],
        "clusters": weights,
    }
    CLUSTER_WEIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CLUSTER_WEIGHTS_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def get_slug_cluster_boost(title_text: str) -> float:
    c_key = classify_text_cluster(title_text)
    if CLUSTER_WEIGHTS_FILE.exists():
        try:
            doc = json.loads(CLUSTER_WEIGHTS_FILE.read_text(encoding="utf-8"))
            return float(((doc.get("clusters") or {}).get(c_key) or {}).get("boost_multiplier", 1.0))
        except Exception:
            pass
    return 1.0


def preferred_lang_order_for_current_hour() -> tuple[str, str]:
    """
    [0-크레딧 자율 진화 엔진 #2 — 한·미 학생 골든타임 시간대 자동 라우팅]
    - 한국 중·고등학생 방과후·야간 학습 피크 (15:00 ~ 23:59 KST): ('ko', 'en') 한국어 우선 발행
    - 미국·영국·글로벌 주간/저녁 학습 피크 (00:00 ~ 14:59 KST = 미 동부 10:00~00:59): ('en', 'ko') 고단가 영어권 우선 발행
    """
    hr = datetime.now().hour
    if 15 <= hr <= 23:
        return ("ko", "en")
    return ("en", "ko")


def sync_high_retention_binge_playlists(yt_service=None, max_items_to_add: int = 8) -> dict:
    """
    [0-크레딧 자율 진화 엔진 #3 — 정주행 재생목록(Session-Chaining) 자동 편성 & Rule 13.1 제목 정화]
    1 클릭 = 3~5편 연속 재생(유효 시청시간 4배 증폭)을 만들고 검색 상위에 재생목록을 노출시킵니다.
    """
    if yt_service is None:
        import min7014_video_maker as vm
        yt_service, _ = vm.get_available_youtube_upload_service()
    if yt_service is None:
        return {"added": 0, "playlists": 0}

    state = {"playlists": {}, "added_pairs": []}
    if PLAYLIST_STATE_FILE.exists():
        try:
            state.update(json.loads(PLAYLIST_STATE_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass

    existing = yt_service.playlists().list(part="snippet", mine=True, maxResults=50).execute().get("items", [])
    title_to_id = {}
    sanitized_legacy = 0
    for pl in existing:
        pid = pl["id"]
        snip = pl["snippet"]
        pt = snip.get("title", "")
        pd = snip.get("description", "")
        clean_pt = sanitize_copyright_and_trademark_text(pt)
        clean_pd = sanitize_copyright_and_trademark_text(pd)
        # Rule 13.1 & Rule 51 준수: 개인 호칭 및 외부 시험 등록상표(SAT, Olympiad, AMC, IB 등) 즉시 정화!
        clean_pt = re.sub(r"민은기\s*선생님의\s*수학자료실_AI|Min's\s*Math\s*Lab\s*AI", "@min7014_ai", clean_pt)
        clean_pt = re.sub(r"민은기\s*선생님[의]*", "", clean_pt).strip()
        clean_pd = re.sub(r"민은기\s*선생님의\s*수학자료실|Min's\s*Math\s*Lab", "@min7014_ai 시각적 수학 아카이브", clean_pd)
        clean_pd = re.sub(r"민은기\s*선생님[의]*", "", clean_pd).strip()
        if "SAT" in pt or "Olympiad" in pt or "내신·수능 4점" in pt:
            if "[Visual Geometry" in clean_pt or "SAT" in pt:
                clean_pt = "🔥 [Visual Geometry & Calculus] 5-Second Auxiliary Line Proofs (1080p) | @min7014_ai"
                clean_pd = "Stop memorizing formulas blindly! Master essential geometry, algebra, and calculus theorems through 100% original step-by-step visual proofs (https://min7014.github.io/)."
            elif "내신·수능 4점" in pt:
                clean_pt = "🎯 [도형·미적분 5초 해법] 공식 암기 타파 보조선 1줄 시각적 증명 정주행 | @min7014_ai"
                clean_pd = "방정식 세우다 시간 뺏기는 단골 도형·기하 함정 구조를 100% 자체 작도 보조선 시각 증명으로 5초 만에 꿰뚫는 정주행 재생목록입니다."
        if clean_pt != pt or clean_pd != pd:
            try:
                yt_service.playlists().update(
                    part="snippet",
                    body={"id": pid, "snippet": {"title": clean_pt[:140], "description": clean_pd[:4000]}},
                ).execute()
                pt = clean_pt
                sanitized_legacy += 1
            except Exception:
                pass
        title_to_id[pt] = pid

    # state 내 구 키(en_sat_olympiad) 자동 마이그레이션
    if "en_sat_olympiad" in state.get("playlists", {}):
        state["playlists"]["en_visual_geometry"] = state["playlists"].pop("en_sat_olympiad")

    for spec in CURATED_PLAYLIST_SPECS:
        k = spec["key"]
        if k in state["playlists"] and state["playlists"][k]:
            continue
        matched_id = None
        for pt, pid in title_to_id.items():
            if spec["title"][:22] in pt:
                matched_id = pid
                break
        if not matched_id:
            try:
                created = yt_service.playlists().insert(
                    part="snippet,status",
                    body={
                        "snippet": {"title": spec["title"], "description": spec["desc"], "defaultLanguage": spec["lang"]},
                        "status": {"privacyStatus": "public"},
                    },
                ).execute()
                matched_id = created["id"]
            except Exception:
                continue
        if matched_id:
            state["playlists"][k] = matched_id

    # 3~12분 핵심 본편 & 실전함정 하이브리드 본편을 해당 클러스터 재생목록에 자동 편입
    added_now = 0
    added_set = set(state.get("added_pairs") or [])
    scripts_dir = ROOT_DIR / "video_lectures" / "scripts"
    for sp in sorted(scripts_dir.glob("*.json")):
        if added_now >= max_items_to_add:
            break
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        t_all = f"{sdoc.get('title', '')} {sdoc.get('title_en', '')}"
        c_key = classify_text_cluster(t_all)

        # 1) Exam-Hybrid URLs 최우선 편입, 2) 3~11분 일반/질문 본편 편입
        for lc in ("ko", "en"):
            if added_now >= max_items_to_add:
                break
            urls_cand = []
            nb_u = ((sdoc.get("nano_banana_urls") or {}).get(lc) or "").strip()
            if nb_u:
                urls_cand.append(nb_u)
            eh_u = ((sdoc.get("exam_hybrid_urls") or {}).get(lc) or "").strip()
            if eh_u:
                urls_cand.append(eh_u)
            dur_s = float(((sdoc.get("youtube_packages") or {}).get(lc) or {}).get("total_duration_sec") or 0.0)
            std_u = ((sdoc.get("youtube_urls") or {}).get(lc) or "").strip()
            if std_u and (dur_s == 0.0 or 150.0 <= dur_s <= 680.0):
                urls_cand.append(std_u)

            for u in urls_cand:
                m_v = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", u)
                if not m_v:
                    continue
                vid = m_v.group(1)
                for spec in CURATED_PLAYLIST_SPECS:
                    if spec["lang"] != lc or c_key not in spec["match_clusters"]:
                        continue
                    pl_id = state["playlists"].get(spec["key"])
                    pair_key = f"{pl_id}:{vid}"
                    if not pl_id or pair_key in added_set:
                        continue
                    try:
                        yt_service.playlistItems().insert(
                            part="snippet",
                            body={"snippet": {"playlistId": pl_id, "resourceId": {"kind": "youtube#video", "videoId": vid}}},
                        ).execute()
                        added_set.add(pair_key)
                        added_now += 1
                        break
                    except Exception as e:
                        if "videoAlreadyInPlaylist" in str(e) or "409" in str(e) or "videoNotFound" in str(e):
                            added_set.add(pair_key)
                        break

    state["added_pairs"] = sorted(added_set)
    PLAYLIST_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PLAYLIST_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"playlists": len(state["playlists"]), "added_now": added_now, "total_chained": len(added_set), "sanitized_legacy": sanitized_legacy}


def inject_multilingual_localizations_on_top_videos(yt_service=None, max_updates: int = 4) -> int:
    """
    [0-크레딧 자율 진화 엔진 #4 — 글로벌 고단가 6개국어 메타데이터(localizations) 자동 주입기]
    신규 업로드 슬롯을 1개도 쓰지 않고(쿼터 단 50유닛), 상위 조회수 영상에 영·한·일·스페인·독일·포르투갈어
    현지화 제목·설명을 주입하여 고단가(RPM 2.5~4배) 글로벌 검색 노출을 증폭합니다.
    """
    if yt_service is None:
        import min7014_video_maker as vm
        yt_service, _ = vm.get_available_youtube_upload_service()
    if yt_service is None:
        return 0

    done = set()
    if LOCALIZATION_STATE_FILE.exists():
        try:
            done = set(json.loads(LOCALIZATION_STATE_FILE.read_text(encoding="utf-8")).get("localized_ids") or [])
        except Exception:
            pass

    # 실전함정 본편/쇼츠 및 스크립트 내 한·영 쌍 보유 영상 대상
    updated = 0
    scripts_dir = ROOT_DIR / "video_lectures" / "scripts"
    import min7014_video_maker as vm

    for sp in sorted(scripts_dir.glob("*.json")):
        if updated >= max_updates:
            break
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        ko_t, en_t = vm.split_bilingual_title(sdoc.get("title", ""))
        ko_clean = vm._smart_concise_topic_title(vm.latex_to_unicode_title(ko_t).strip(), max_len=44, lang="ko")
        en_clean = vm._smart_concise_topic_title(vm.latex_to_unicode_title((sdoc.get("title_en") or en_t or ko_clean).split("—")[0].strip()), max_len=58, lang="en")
        if not ko_clean or not en_clean:
            continue

        cand_urls = []
        for d_key in ("exam_hybrid_urls", "exam_hybrid_shorts_urls", "question_shorts_urls", "youtube_urls"):
            mp = sdoc.get(d_key) or {}
            for lc_k in ("ko", "en"):
                if (mp.get(lc_k) or "").strip():
                    cand_urls.append(mp[lc_k].strip())

        for u in cand_urls:
            if updated >= max_updates:
                break
            m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", u)
            if not m:
                continue
            vid = m.group(1)
            if vid in done:
                continue
            try:
                items = yt_service.videos().list(part="snippet,localizations", id=vid).execute().get("items", [])
                if not items:
                    done.add(vid)
                    continue
                v_obj = items[0]
                snip = v_obj["snippet"]
                is_short = "#shorts" in snip.get("title", "").lower() or "/shorts/" in u
                sh_tag = " #Shorts" if is_short else ""
                def_lang = snip.get("defaultLanguage") or ("ko" if re.search(r"[가-힣]", snip.get("title", "")) else "en")
                snip["defaultLanguage"] = def_lang

                locs = dict(v_obj.get("localizations") or {})
                locs["ko"] = {
                    "title": vm.sanitize_youtube_title(f"🔥 공식 암기 금지! 보조선 1줄 시각 해법 | {ko_clean}{sh_tag}"),
                    "description": snip.get("description", "")[:4000],
                }
                locs["en"] = {
                    "title": vm.sanitize_youtube_title(f"🔥 Don't Memorize! 5-Sec Visual Proof | {en_clean}{sh_tag}"),
                    "description": f"Step-by-step visual math proof of {en_clean}. Subscribe @min7014_ai for daily visual exam hacks!\nhttps://min7014.github.io/mathedu/",
                }
                locs["ja"] = {
                    "title": vm.sanitize_youtube_title(f"🔥 公式暗記不要！補助線1本の視覚的証明 | {en_clean}{sh_tag}"),
                    "description": f"図形で直感的に理解する数学の視覚的証明 ({en_clean}) | @min7014_ai",
                }
                locs["es"] = {
                    "title": vm.sanitize_youtube_title(f"🔥 ¡No memorices fórmulas! Demostración visual en 5s | {en_clean}{sh_tag}"),
                    "description": f"Demostración matemática visual paso a paso ({en_clean}) | @min7014_ai",
                }
                locs["de"] = {
                    "title": vm.sanitize_youtube_title(f"🔥 Nicht auswendig lernen! Visueller Mathe-Beweis | {en_clean}{sh_tag}"),
                    "description": f"Anschaulicher geometrischer Beweis Schritt für Schritt ({en_clean}) | @min7014_ai",
                }
                locs["pt"] = {
                    "title": vm.sanitize_youtube_title(f"🔥 Não decore fórmulas! Prova visual em 5 segundos | {en_clean}{sh_tag}"),
                    "description": f"Demonstração visual passo a passo de matemática ({en_clean}) | @min7014_ai",
                }
                yt_service.videos().update(
                    part="snippet,localizations",
                    body={"id": vid, "snippet": snip, "localizations": locs},
                ).execute()
                done.add(vid)
                updated += 1
            except Exception:
                done.add(vid)

    LOCALIZATION_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCALIZATION_STATE_FILE.write_text(json.dumps({"localized_ids": sorted(done)}, ensure_ascii=False, indent=2), encoding="utf-8")
    return updated


def evaluate_ai_subscription_roi_gate(subscribers: int, watch_hours: float, valid_shorts_views: int = 0) -> dict:
    """
    [재무 규율 엔진 — 월 11만 원 vs 30만 원 AI 요금제 손익분기 자동 판독기]
    """
    tier2_ready = (subscribers >= 1000) and (watch_hours >= 4000.0 or valid_shorts_views >= 10_000_000)
    if not tier2_ready:
        return {
            "recommended_plan_krw": 110000,
            "upgrade_to_300k_allowed": False,
            "annual_saved_krw": 2280000,
            "verdict_badge": "🟢 [재무 권고: 현행 월 11만 원 요금제 유지 (30만 원 상향 불필요 · 연 228만 원 절감)]",
            "reason": "현재 영상 렌더링·음성합성·업로드·클러스터 학습·다국어 주입·추이 추적 100%가 AI 크레딧 0원(로컬 파이썬)으로 자동 가동 중입니다. 정식 광고 수익(구독자 1,000명+시청시간 4,000시간 달성 후 월 실수령 45만 원+) 발생 전까지는 절대 고정비를 올리지 마십시오.",
        }
    return {
        "recommended_plan_krw": 300000,
        "upgrade_to_300k_allowed": True,
        "annual_saved_krw": 0,
        "verdict_badge": "🚀 [재무 권고: YPP 정식 수익화 관문 돌파! 월 정산액 45만 원 확인 시 30만 원 울트라 전환 가능]",
        "reason": "유튜브 자체 현금흐름만으로 AI 구독료를 충당하고 순이익이 남는 자생 구간에 진입했습니다.",
    }


def run_zero_credit_self_evolution_cycle(yt_service=None) -> dict:
    if yt_service is None:
        import min7014_video_maker as vm
        yt_service, _ = vm.get_available_youtube_upload_service()
    cw = compute_winning_cluster_weights(yt_service=yt_service)
    pl_res = sync_high_retention_binge_playlists(yt_service=yt_service, max_items_to_add=6)
    loc_cnt = inject_multilingual_localizations_on_top_videos(yt_service=yt_service, max_updates=3)
    return {
        "top_clusters": cw.get("top_3_clusters", []),
        "playlists": pl_res,
        "localized_videos_now": loc_cnt,
    }


if __name__ == "__main__":
    res = run_zero_credit_self_evolution_cycle()
    print(json.dumps(res, ensure_ascii=False, indent=2))
