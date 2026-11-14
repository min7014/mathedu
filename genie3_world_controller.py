#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genie3_world_controller.py
===============================================================================
🌐 [Spatial 3D World Camera Controller — 5% Pinpoint Spatial & Conic Track]
- 역할 분담 아키텍처 (95% Google Flow ULTRA 평면·대수 고정 카메라 + 5% 공간기하·원뿔곡선 1인칭 3D 카메라):
  1) 평면기하·대수·미적분 주력 단원(95%)은 기하 왜곡 0%가 검증된 Google Flow ULTRA 양단 고정 모션을 유지합니다.
  2) 2D 평면 그림만으로 입체감을 잡기 어려운 공간기하·원뿔곡선 특수 단원(삼수선의 정리, 정사영과 이면각,
     단델린의 구와 원뿔 단면, 직육면체 공간 대각선 등 5% 선별 트랙)에 한해 Act 1(첫 3초 스와이프 방어 훅)과
     Act 3(유레카 완결)에 1인칭 3D 공간 카메라 워킹 B-Roll을 적용합니다.
- 3대 필수 안전장치 완벽 내장:
  [Guard 1 · Rule 44 수학적 오류 ZERO]: 3D 공간 카메라 클립에는 글자·숫자·수식을 일절 넣지 않고 순수 공간 조형물로만
     사용하며, 정밀 수식·각도 라벨은 100% 파이썬 벡터 HUD로, 본 증명(Act 2)은 100% min7014.github.io 원문 PDF로 고정.
  [Guard 2 · 720p 24fps -> 1080p 30fps 마스터링]: 외부 720p/24fps 월드 클립 입력 시 FFmpeg Lanczos 업스케일 +
     unsharp(5:5:0.85) 광학 샤프닝 + 30fps 프레임 보간 마스터링을 자동 수행하여 1080p 방송급 선명도를 보장.
  [Guard 3 · Rule 50 & Rule 51]: 추가 유료 API 과금 0원(기존 구독 범위 내 운용 + 무결점 3D 유클리드 월드 카메라 엔진),
     대외 유튜브 메타데이터에 외부 AI/월드모델 브랜드명 노출 0건(auditor.py L1 하드 게이트 연동).
  [Rule 48 완전 무창 실행]: 최상단 silent_subprocess 강제 주입.
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent
NB_ASSETS_DIR = ROOT_DIR / "youtube_uploads" / "nano_banana_assets"
FLOW_CLIPS_DIR = ROOT_DIR / "youtube_uploads" / "flow_clips"
GENIE_CLIPS_DIR = ROOT_DIR / "youtube_uploads" / "genie_clips"
GENIE_STATE_FILE = ROOT_DIR / ".agents" / "genie3_world_state.json"

NB_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
GENIE_CLIPS_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_GENIE_URL = "https://labs.google/fx/projectgenie"

SPATIAL_3D_KEYWORDS = (
    "삼수선",
    "정사영",
    "이면각",
    "공간좌표",
    "공간도형",
    "공간에서",
    "직육면체",
    "정육면체",
    "정사면체",
    "사면체",
    "정팔면체",
    "원뿔",
    "단델린",
    "구의 방정식",
    "구면",
    "원기둥",
    "회전체",
)

ZERO_TEXT_SPATIAL_GUARD = (
    " Positioned on the LEFT TWO-THIRDS of the 16:9 dark midnight-navy studio environment "
    "(leaving clean dark navy space on the right third). "
    "Zero text, zero numbers, zero letters, zero mathematical symbols anywhere in the 3D world."
)


def _load_genie_state() -> dict:
    st = {
        "labs_url": PROJECT_GENIE_URL,
        "labs_access_status": "untested",
        "labs_last_checked": "",
        "mastered_clips": [],
    }
    if GENIE_STATE_FILE.exists():
        try:
            st.update(json.loads(GENIE_STATE_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return st


def _save_genie_state(st: dict) -> None:
    GENIE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    GENIE_STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def _is_valid_mp4(path: Path, min_bytes: int = 120_000) -> bool:
    if not path.exists() or path.stat().st_size < min_bytes:
        return False
    try:
        with path.open("rb") as fh:
            hdr = fh.read(12)
        return len(hdr) >= 8 and hdr[4:8] == b"ftyp"
    except Exception:
        return False


def is_spatial_3d_topic(sdoc_or_title: dict | str) -> bool:
    """5% 선별 적용 대상인 공간기하·원뿔곡선 입체 단원인지 판별합니다."""
    if isinstance(sdoc_or_title, dict):
        blob = f"{sdoc_or_title.get('title', '')} {sdoc_or_title.get('sub_domain_ko', '')} {sdoc_or_title.get('core_concept', '')}"
    else:
        blob = str(sdoc_or_title or "")
    return any(k in blob for k in SPATIAL_3D_KEYWORDS)


def detect_spatial_archetype(sdoc_or_title: dict | str) -> str:
    if isinstance(sdoc_or_title, dict):
        blob = f"{sdoc_or_title.get('title', '')} {sdoc_or_title.get('sub_domain_ko', '')}"
    else:
        blob = str(sdoc_or_title or "")
    if any(k in blob for k in ("삼수선", "수선의 발", "평면 밖의 점")):
        return "three_perpendiculars"
    if any(k in blob for k in ("정사영", "이면각")):
        return "orthogonal_projection"
    if any(k in blob for k in ("원뿔", "단델린", "타원의 정의", "포물선의 정의", "쌍곡선의 정의")):
        return "dandelin_cone"
    return "spatial_polyhedron"


def build_spatial_world_prompts(slug: str, sdoc_or_title: dict | str = "") -> dict:
    """공간기하 아키타입별 무문자(Text-Free) 3D 월드 프롬프트 및 Flow 3D 오브제 프롬프트 생성."""
    arch = detect_spatial_archetype(sdoc_or_title)
    if arch == "three_perpendiculars":
        world_p = (
            "Architectural dark midnight-navy museum hall containing a glowing translucent sapphire glass floor plane, "
            "a vertical brushed-gold pillar standing perpendicular to the sapphire floor, an emerald-teal crystal beam "
            "along the floor meeting a luminous cyan line at a crisp right angle, and a taut golden diagonal light ray "
            "connecting the top of the pillar to the intersection point." + ZERO_TEXT_SPATIAL_GUARD
        )
        cam_p = (
            "Smooth slow 3D orbital camera glide moving gently around the translucent sapphire plane and vertical golden pillar, "
            "keeping all straight crystal beams rigid and undeformed on dark midnight velvet. Zero text, zero numbers."
        )
    elif arch == "orthogonal_projection":
        world_p = (
            "Dark midnight-navy optical sanctuary featuring a luminous emerald-teal crystal square plate suspended at a 60-degree "
            "incline above a polished sapphire mirror floor, with vertical warm amber-gold light shafts projecting a crisp "
            "glowing golden shadow rectangle directly onto the floor plane." + ZERO_TEXT_SPATIAL_GUARD
        )
        cam_p = (
            "Smooth slow 3D side-orbital camera glide revealing the inclined emerald crystal square and its golden orthogonal "
            "shadow on the sapphire floor plane. Rigid crystal geometry, zero deformation, zero text, zero numbers."
        )
    elif arch == "dandelin_cone":
        world_p = (
            "Grand dark midnight-navy geometric observatory showcasing a tall translucent sapphire crystal cone sliced by an "
            "inclined emerald-teal glass plane forming a glowing elliptical rim, with two polished brushed-gold spheres nestled "
            "tangent inside the cone above and below the inclined slice plane." + ZERO_TEXT_SPATIAL_GUARD
        )
        cam_p = (
            "Smooth slow 3D orbital camera walk-around circling the translucent crystal cone, inclined emerald ellipse plane, "
            "and two tangent golden spheres inside the dark studio. Zero deformation, zero text, zero numbers."
        )
    else:
        world_p = (
            "Dark midnight-navy architectural gallery displaying a precision-crafted rectangular prism frame of brushed brass "
            "and translucent sapphire glass panels, illuminated by an emerald-teal base diagonal ray and a glowing amber-gold "
            "3D interior space-diagonal laser beam." + ZERO_TEXT_SPATIAL_GUARD
        )
        cam_p = (
            "Smooth slow 3D orbital parallax camera glide around the sapphire-and-brass rectangular prism and glowing interior "
            "space diagonal beam on dark midnight velvet. Zero deformation, zero text, zero numbers."
        )
    return {
        "slug": slug,
        "archetype": arch,
        "world_prompt": world_p,
        "flow_image_prompt": world_p,
        "flow_camera_prompt": cam_p,
    }


def master_genie_720p_to_1080p_30fps(raw_clip: Path, out_mp4: Path) -> Path | None:
    """
    [Guard 2 · 720p 24fps -> 1080p 30fps Lanczos + Unsharp 마스터링]:
    720p/24fps 월드 모델 추출 영상을 1920x1080 30fps H.264 High Profile(CRF 18)로 업스케일하고
    unsharp(5:5:0.85) 광학 엣지 샤프닝 및 우측 HUD 가독성 다크 벨벳 톤 보정을 수행합니다.
    """
    if not raw_clip.exists() or raw_clip.stat().st_size < 30_000:
        return None
    ffmpeg_exe = shutil.which("ffmpeg")
    if not ffmpeg_exe:
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            return None

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = out_mp4.with_name(out_mp4.stem + "_mastering_tmp.mp4")
    vf = (
        "scale=1920:1080:flags=lanczos,"
        "unsharp=5:5:0.85:5:5:0.0,"
        "eq=contrast=1.05:brightness=-0.015:saturation=1.06,"
        "fps=30,setsar=1,format=yuv420p"
    )
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i",
        str(raw_clip),
        "-an",
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-profile:v",
        "high",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(tmp_out),
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and _is_valid_mp4(tmp_out, min_bytes=100_000):
        shutil.move(str(tmp_out), str(out_mp4))
        if out_mp4.resolve().is_relative_to(ROOT_DIR.resolve()):
            st = _load_genie_state()
            rel = str(out_mp4.resolve().relative_to(ROOT_DIR.resolve())).replace("\\", "/")
            if rel not in (st.get("mastered_clips") or []):
                st.setdefault("mastered_clips", []).append(rel)
            _save_genie_state(st)
        return out_mp4
    if tmp_out.exists():
        tmp_out.unlink(missing_ok=True)
    return None


def ingest_external_genie_clip(slug: str, raw_clip_path: Path) -> Path | None:
    """Google Labs에서 수동/반자동 추출한 .mp4/.webm 클립을 즉시 1080p 30fps로 마스터링하여 바인딩합니다."""
    out_mp4 = GENIE_CLIPS_DIR / f"{slug}_genie_1080p.mp4"
    return master_genie_720p_to_1080p_30fps(raw_clip_path, out_mp4)


def probe_and_capture_project_genie_clip(
    slug: str,
    world_prompt: str,
    keyframe_png: Path | None = None,
    duration_sec: float = 5.0,
    camera_path: str = "orbit_right",
    headless: bool = True,
) -> dict:
    """
    Google Labs Project Genie (`https://labs.google/fx/projectgenie`) 무창 헤드리스 연동 및
    1인칭 WASD 카메라 워킹 캡처 시도. (계정 플랜 게이트 또는 헤드리스 WebGPU 제한 감지 시 즉시 폴백 반환)
    """
    from playwright.sync_api import sync_playwright
    import youtube_community_controller as ycc

    locked = False
    for _ in range(15):
        if ycc._acquire_robot_lock(240):
            locked = True
            break
        time.sleep(1.5)
    if not locked:
        return {"ok": False, "status": "robot_lock_busy"}

    st = _load_genie_state()
    try:
        with sync_playwright() as p:
            ctx = ycc._launch_robot_context(p, headless=headless)
            try:
                page = ctx.new_page()
                page.goto(PROJECT_GENIE_URL, wait_until="domcontentloaded", timeout=40000)
                time.sleep(4.5)

                # 쿠키 배너 정리
                for lbl in ("Agree", "Accept", "동의함"):
                    b = page.locator(f"button:has-text('{lbl}')")
                    if b.count() > 0:
                        try:
                            b.first.click(force=True, timeout=2000)
                            time.sleep(0.8)
                        except Exception:
                            pass

                # SSO 로그인 시도 (Welcome 모달의 'Sign in' 버튼 포함)
                body_now = page.evaluate("() => document.body ? document.body.innerText : ''")
                if "Sign in with Google" in body_now or "Sign in" in body_now:
                    page.evaluate(
                        """() => {
                            const c = document.querySelector('button[aria-label="Create your own"]');
                            if (c) c.click();
                        }"""
                    )
                    time.sleep(1.5)
                    page.evaluate(
                        """() => {
                            const btns = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
                            const s = btns.find(e => {
                                const t = (e.innerText || '').trim();
                                return t === 'Sign in' || t.includes('Sign in with Google');
                            });
                            if (s) s.click();
                        }"""
                    )
                    time.sleep(4.5)
                    for pg_i in list(ctx.pages):
                        if "accounts.google.com" in pg_i.url:
                            pg_i.evaluate(
                                """() => {
                                    const items = Array.from(document.querySelectorAll('[data-identifier]'));
                                    if (items.length > 0) items[0].click();
                                }"""
                            )
                            time.sleep(5.5)

                active_pg = ctx.pages[-1]
                if "labs.google" not in active_pg.url:
                    active_pg = page

                post_text = active_pg.evaluate("() => document.body ? document.body.innerText : ''")
                st["labs_last_checked"] = datetime.now().isoformat(timespec="seconds")

                if "You need a Google AI Ultra plan" in post_text or "Sign in or upgrade to get started" in post_text:
                    st["labs_access_status"] = "labs_plan_or_sso_gate"
                    _save_genie_state(st)
                    return {"ok": False, "status": "labs_plan_or_sso_gate"}

                # Create your own 진입 시도
                active_pg.evaluate(
                    """() => {
                        const c = document.querySelector('button[aria-label="Create your own"]');
                        if (c) c.click();
                    }"""
                )
                time.sleep(2.5)
                ta = active_pg.locator("textarea")
                if ta.count() == 0 or not ta.first.is_visible():
                    st["labs_access_status"] = "create_ui_unavailable_headless"
                    _save_genie_state(st)
                    return {"ok": False, "status": "create_ui_unavailable_headless"}

                if keyframe_png and keyframe_png.exists():
                    f_in = active_pg.locator("input[type='file']")
                    if f_in.count() > 0:
                        try:
                            f_in.first.set_input_files(str(keyframe_png))
                            time.sleep(2.5)
                        except Exception:
                            pass

                ta.first.fill(world_prompt)
                time.sleep(0.8)
                active_pg.keyboard.press("Enter")
                time.sleep(16.0)

                # MediaRecorder로 활성 3D 월드 캔버스 스트림을 캡처하면서 WASD 1인칭 카메라 워킹 수행
                has_stream = active_pg.evaluate(
                    """() => {
                        const cv = document.querySelector('canvas');
                        if (!cv || typeof cv.captureStream !== 'function') return false;
                        window.__genieChunks = [];
                        const stream = cv.captureStream(30);
                        const rec = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp9' });
                        rec.ondataavailable = (e) => { if (e.data && e.data.size > 0) window.__genieChunks.push(e.data); };
                        window.__genieRec = rec;
                        rec.start(200);
                        return true;
                    }"""
                )
                if not has_stream:
                    st["labs_access_status"] = "canvas_stream_unavailable"
                    _save_genie_state(st)
                    return {"ok": False, "status": "canvas_stream_unavailable"}

                active_pg.keyboard.down("KeyW")
                if camera_path == "orbit_left":
                    active_pg.keyboard.down("KeyA")
                else:
                    active_pg.keyboard.down("KeyD")
                time.sleep(max(2.5, float(duration_sec)))
                active_pg.keyboard.up("KeyW")
                active_pg.keyboard.up("KeyA")
                active_pg.keyboard.up("KeyD")

                b64_webm = active_pg.evaluate(
                    """async () => {
                        if (!window.__genieRec) return '';
                        await new Promise(r => { window.__genieRec.onstop = r; window.__genieRec.stop(); });
                        const blob = new Blob(window.__genieChunks, { type: 'video/webm' });
                        const buf = await blob.arrayBuffer();
                        const bytes = new Uint8Array(buf);
                        let bin = '';
                        for (let i = 0; i < bytes.byteLength; i++) bin += String.fromCharCode(bytes[i]);
                        return btoa(bin);
                    }"""
                )
                if not b64_webm or len(b64_webm) < 40_000:
                    return {"ok": False, "status": "empty_canvas_recording"}

                import base64
                raw_webm = GENIE_CLIPS_DIR / f"{slug}_genie_raw.webm"
                raw_webm.write_bytes(base64.b64decode(b64_webm))
                out_mp4 = GENIE_CLIPS_DIR / f"{slug}_genie_1080p.mp4"
                mastered = master_genie_720p_to_1080p_30fps(raw_webm, out_mp4)
                raw_webm.unlink(missing_ok=True)
                if mastered:
                    st["labs_access_status"] = "active_ok"
                    _save_genie_state(st)
                    return {"ok": True, "status": "captured_and_mastered", "out_mp4": str(mastered)}
                return {"ok": False, "status": "mastering_failed"}
            finally:
                ctx.close()
    except Exception as e:
        return {"ok": False, "status": f"error:{str(e)[:80]}"}
    finally:
        ycc._release_robot_lock()


# ==============================================================================
# 📐 무결점 3D 유클리드 월드 카메라 엔진 (1920x1080 · 30fps · 기하 오차 0.000%)
# ==============================================================================
def _project_3d(
    pt: tuple[float, float, float],
    yaw: float,
    pitch: float,
    cam_dist: float,
    focal: float = 1280.0,
    cx: float = 610.0,
    cy: float = 548.0,
) -> tuple[float, float, float]:
    """3D 공간 좌표 (x, y_up, z)를 회전·원근 투영하여 화면 (sx, sy, depth_z)로 변환합니다."""
    x, y, z = pt
    cyw, syw = math.cos(yaw), math.sin(yaw)
    x1 = x * cyw - z * syw
    z1 = x * syw + z * cyw

    cp, sp = math.cos(pitch), math.sin(pitch)
    y2 = y * cp - z1 * sp
    z2 = y * sp + z1 * cp + cam_dist
    z2 = max(0.8, z2)
    sc = focal / z2
    return (cx + x1 * sc, cy - y2 * sc, z2)


def _draw_glow_line(
    glow_draw: ImageDraw.ImageDraw,
    core_draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color_rgb: tuple[int, int, int],
    width: int = 5,
    glow_alpha: int = 165,
) -> None:
    glow_draw.line([p1, p2], fill=(*color_rgb, glow_alpha), width=width * 3 + 4)
    core_draw.line([p1, p2], fill=(*color_rgb, 255), width=width)


def _draw_glow_pin(
    glow_draw: ImageDraw.ImageDraw,
    core_draw: ImageDraw.ImageDraw,
    pt: tuple[float, float],
    radius: int,
    color_rgb: tuple[int, int, int],
) -> None:
    x, y = pt
    r_g = radius * 2.6
    glow_draw.ellipse((x - r_g, y - r_g, x + r_g, y + r_g), fill=(*color_rgb, 175))
    core_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 255, 255, 255), outline=(*color_rgb, 255), width=3)


def _render_single_spatial_3d_frame(archetype: str, phase: float, width: int = 1920, height: int = 1080) -> Image.Image:
    """
    Rule 37 사색적 블루·에메랄드·앰버 골드 팔레트 + Rule 44 수학적 직교·접선 무결성 100% 보장
    1인칭 WASD 공간 카메라 워킹 프레임을 생성합니다 (글자·수식 0%).
    """
    # 기본 미드나잇 벨벳 스튜디오 배경
    base = Image.new("RGBA", (width, height), (8, 14, 28, 255))
    bg_d = ImageDraw.Draw(base)
    # 좌측 2/3 스튜디오 은은한 사파이어 스포트라이트 비네팅
    spot = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spot)
    sd.ellipse((110, 120, 1140, 960), fill=(18, 46, 92, 95))
    sd.ellipse((250, 240, 980, 840), fill=(14, 78, 128, 70))
    spot = spot.filter(ImageFilter.GaussianBlur(85))
    base = Image.alpha_composite(base, spot)

    poly_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    core_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pd = ImageDraw.Draw(poly_layer)
    gd = ImageDraw.Draw(glow_layer)
    cd = ImageDraw.Draw(core_layer)

    SAPPHIRE = (56, 189, 248)
    ROYAL = (2, 132, 199)
    EMERALD = (16, 185, 129)
    MINT = (110, 231, 183)
    GOLD = (250, 204, 21)
    AMBER = (245, 158, 11)

    # 부드러운 코사인 1인칭 드론 카메라 궤적 (전진 돌리 + 측면 공전 패럴랙스)
    ang = 2.0 * math.pi * phase
    pulse = 0.5 + 0.5 * math.sin(ang * 2.0)

    if archetype == "three_perpendiculars":
        # 삼수선의 정리: 평면 alpha (y = -0.85), 점 P(-0.55, 1.35, -0.35), 수선의 발 M(-0.55, -0.85, -0.35),
        # 평면 위 직선 a: x = 0.72, M에서 a에 내린 수선의 발 N(0.72, -0.85, -0.35) -> PN ⊥ a!
        yaw = -0.58 + 0.44 * math.sin(ang)
        pitch = 0.36 + 0.08 * math.cos(ang)
        dist = 5.45 - 0.38 * math.sin(ang)
        pr = lambda p: _project_3d(p, yaw, pitch, dist)[:2]

        y0 = -0.85
        plane_pts = [pr((-1.75, y0, -1.65)), pr((1.75, y0, -1.65)), pr((1.75, y0, 1.65)), pr((-1.75, y0, 1.65))]
        pd.polygon(plane_pts, fill=(14, 42, 84, 150), outline=(*SAPPHIRE, 195))
        # 평면 정밀 격자선
        for g in (-1.1, -0.55, 0.0, 0.55, 1.1):
            cd.line([pr((-1.75, y0, g)), pr((1.75, y0, g))], fill=(56, 189, 248, 52), width=2)
            cd.line([pr((g, y0, -1.65)), pr((g, y0, 1.65))], fill=(56, 189, 248, 52), width=2)

        P = (-0.58, 1.38, -0.25)
        M = (-0.58, y0, -0.25)
        N = (0.78, y0, -0.25)
        A1 = (0.78, y0, -1.62)
        A2 = (0.78, y0, 1.62)

        # 삼각형 PMN 반투명 유리면
        pd.polygon([pr(P), pr(M), pr(N)], fill=(16, 185, 129, 64))

        # 3D 직각 기호 1: PM ⊥ MN
        ra1 = 0.22
        cd.line(
            [pr((M[0], M[1] + ra1, M[2])), pr((M[0] + ra1, M[1] + ra1, M[2])), pr((M[0] + ra1, M[1], M[2]))],
            fill=(*GOLD, 235),
            width=3,
        )
        # 3D 직각 기호 2: MN ⊥ 직선 a
        ra2 = 0.22
        cd.line(
            [pr((N[0] - ra2, y0, N[2])), pr((N[0] - ra2, y0, N[2] + ra2)), pr((N[0], y0, N[2] + ra2))],
            fill=(*MINT, 235),
            width=3,
        )
        # 3D 직각 기호 3 (결론!): PN ⊥ 직선 a
        u_pn = (-1.36 / 2.61, 2.23 / 2.61, 0.0)
        q1 = (N[0] + u_pn[0] * 0.24, N[1] + u_pn[1] * 0.24, N[2])
        q2 = (q1[0], q1[1], N[2] - 0.24)
        q3 = (N[0], N[1], N[2] - 0.24)
        _draw_glow_line(gd, cd, pr(q1), pr(q2), GOLD, width=4, glow_alpha=180)
        _draw_glow_line(gd, cd, pr(q2), pr(q3), GOLD, width=4, glow_alpha=180)

        _draw_glow_line(gd, cd, pr(A1), pr(A2), SAPPHIRE, width=6)
        _draw_glow_line(gd, cd, pr(P), pr(M), AMBER, width=7)
        _draw_glow_line(gd, cd, pr(M), pr(N), EMERALD, width=7)
        _draw_glow_line(gd, cd, pr(P), pr(N), GOLD, width=8, glow_alpha=210)

        # 광자 이동 포인트 연출
        t_ph = (phase * 2.0) % 1.0
        photon = (P[0] + (N[0] - P[0]) * t_ph, P[1] + (N[1] - P[1]) * t_ph, P[2])
        _draw_glow_pin(gd, cd, pr(photon), 7, GOLD)
        for v_pt, col in ((P, GOLD), (M, AMBER), (N, EMERALD)):
            _draw_glow_pin(gd, cd, pr(v_pt), 9, col)

    elif archetype == "orthogonal_projection":
        # 정사각형의 정사영의 넓이: 바닥 사파이어 평면 위 황금 정사영 S' = S cos(60°)와 60° 기울어진 에메랄드 크리스탈 정사각형 S
        yaw = -0.65 + 0.52 * math.sin(ang)
        pitch = 0.34 + 0.10 * math.cos(ang)
        dist = 5.6 - 0.35 * math.sin(ang)
        pr = lambda p: _project_3d(p, yaw, pitch, dist)[:2]

        y0 = -0.95
        floor_pts = [pr((-1.85, y0, -1.6)), pr((1.85, y0, -1.6)), pr((1.85, y0, 1.6)), pr((-1.85, y0, 1.6))]
        pd.polygon(floor_pts, fill=(12, 38, 78, 155), outline=(*SAPPHIRE, 190))
        for g in (-1.0, -0.5, 0.0, 0.5, 1.0):
            cd.line([pr((-1.85, y0, g)), pr((1.85, y0, g))], fill=(56, 189, 248, 48), width=2)

        # 경사각 theta = 60도 (cos 60 = 0.5) 정사각형 한 변 L = 1.9
        L = 1.95
        theta = math.radians(60.0)
        x_base = -0.92
        x_top = x_base + L * math.cos(theta)
        y_hinge = y0 + 0.18
        y_top = y_hinge + L * math.sin(theta)
        z1, z2 = -0.95, 0.95

        sq3d = [(x_base, y_hinge, z1), (x_top, y_top, z1), (x_top, y_top, z2), (x_base, y_hinge, z2)]
        sh3d = [(x_base, y0, z1), (x_top, y0, z1), (x_top, y0, z2), (x_base, y0, z2)]

        # 황금 정사영 그림자 S'
        pd.polygon([pr(p) for p in sh3d], fill=(250, 204, 21, int(92 + 30 * pulse)), outline=(*GOLD, 235))
        for i in range(4):
            _draw_glow_line(gd, cd, pr(sh3d[i]), pr(sh3d[(i + 1) % 4]), GOLD, width=5)

        # 수직 투영 광선 기둥 4줄
        for up_p, dn_p in zip(sq3d, sh3d):
            _draw_glow_line(gd, cd, pr(up_p), pr(dn_p), SAPPHIRE, width=3, glow_alpha=125)

        # 상단 에메랄드 크리스탈 정사각형 S
        pd.polygon([pr(p) for p in sq3d], fill=(16, 185, 129, 108), outline=(*MINT, 245))
        for i in range(4):
            _draw_glow_line(gd, cd, pr(sq3d[i]), pr(sq3d[(i + 1) % 4]), EMERALD, width=7)
            _draw_glow_pin(gd, cd, pr(sq3d[i]), 7, EMERALD)
            _draw_glow_pin(gd, cd, pr(sh3d[i]), 6, GOLD)

    elif archetype == "dandelin_cone":
        # 원뿔과 단델린의 구: 크리스탈 원뿔 + 경사 단면 타원 + 정밀 해석기하 상·하 내접 황금 구 & 초점 F1, F2 접선 불변량
        yaw = -0.36 + 0.52 * math.sin(ang)
        pitch = 0.20 + 0.07 * math.cos(ang)
        dist = 6.35 - 0.30 * math.sin(ang)
        pr = lambda p: _project_3d(p, yaw, pitch, dist)[:2]

        apex = (0.0, 2.02, 0.0)
        k_slope = 0.40  # 반지름 r = k * (apex_y - y)
        y_bot = -1.85
        r_bot = k_slope * (apex[1] - y_bot)

        # 원뿔 모선 리브
        for idx_r in range(16):
            th = 2.0 * math.pi * idx_r / 16.0
            b_pt = (r_bot * math.cos(th), y_bot, r_bot * math.sin(th))
            col_rib = (*SAPPHIRE, 95 if idx_r % 2 == 0 else 46)
            cd.line([pr(apex), pr(b_pt)], fill=col_rib, width=2)

        # 하단 원뿔 밑면 링
        bot_ring = [pr((r_bot * math.cos(2 * math.pi * i / 48), y_bot, r_bot * math.sin(2 * math.pi * i / 48))) for i in range(49)]
        cd.line(bot_ring, fill=(*ROYAL, 175), width=3)

        # 경사 절단 평면: y = m_pl * x + y_c0 와 원뿔·내접구의 100% 해석적 동시 접합 방정식
        m_pl = 0.28
        y_c0 = 0.36
        c_pl = 1.0 / math.sqrt(1.0 + m_pl * m_pl)
        sin_a = k_slope / math.sqrt(1.0 + k_slope * k_slope)
        y_up = (y_c0 * c_pl + apex[1] * sin_a) / (c_pl + sin_a)
        r_up = (apex[1] - y_up) * sin_a
        y_dn = (y_c0 * c_pl - apex[1] * sin_a) / (c_pl - sin_a)
        r_dn = (apex[1] - y_dn) * sin_a

        for cy_s, r_s, sph_alpha in ((y_up, r_up, 132), (y_dn, r_dn, 112)):
            c_2d, c_2dy, z_d = _project_3d((0.0, cy_s, 0.0), yaw, pitch, dist)
            rad_px = int(1280.0 * r_s / z_d)
            gd.ellipse((c_2d - rad_px - 6, c_2dy - rad_px - 6, c_2d + rad_px + 6, c_2dy + rad_px + 6), fill=(*AMBER, 68))
            pd.ellipse((c_2d - rad_px, c_2dy - rad_px, c_2d + rad_px, c_2dy + rad_px), fill=(245, 158, 11, sph_alpha), outline=(*GOLD, 225), width=3)
            # 원뿔과 단델린 구가 만나 이루는 수평 접원(Tangent Circle)
            y_tan = apex[1] - (apex[1] - cy_s) / (1.0 + k_slope * k_slope)
            r_tan = k_slope * (apex[1] - y_tan)
            tan_ring = [pr((r_tan * math.cos(2 * math.pi * i / 48), y_tan, r_tan * math.sin(2 * math.pi * i / 48))) for i in range(49)]
            cd.line(tan_ring, fill=(*GOLD, 165), width=2)

        ell_3d = []
        for i in range(65):
            th = 2.0 * math.pi * i / 64.0
            r_th = (k_slope * (apex[1] - y_c0)) / (1.0 + k_slope * m_pl * math.cos(th))
            ex = r_th * math.cos(th)
            ez = r_th * math.sin(th)
            ey = y_c0 + m_pl * ex
            ell_3d.append((ex, ey, ez))

        pd.polygon([pr(p) for p in ell_3d[:-1]], fill=(16, 185, 129, 88))
        for i in range(len(ell_3d) - 1):
            _draw_glow_line(gd, cd, pr(ell_3d[i]), pr(ell_3d[i + 1]), EMERALD, width=6)

        # 두 단델린 내접구와 절단 평면의 정확한 접점 = 타원의 두 초점 F1, F2
        d_up = (y_up - y_c0) / (1.0 + m_pl * m_pl)
        d_dn = (y_dn - y_c0) / (1.0 + m_pl * m_pl)
        F1 = (m_pl * d_up, y_up - d_up, 0.0)
        F2 = (m_pl * d_dn, y_dn - d_dn, 0.0)
        p_idx = int((phase * 64) % 64)
        P_on = ell_3d[p_idx]
        # P를 지나는 원뿔 모선 위의 두 접원 교점 T_up, T_dn (|PF1| = |PT_up|, |PF2| = |PT_dn|)
        th_p = 2.0 * math.pi * p_idx / 64.0
        y_tup = apex[1] - (apex[1] - y_up) / (1.0 + k_slope * k_slope)
        r_tup = k_slope * (apex[1] - y_tup)
        y_tdn = apex[1] - (apex[1] - y_dn) / (1.0 + k_slope * k_slope)
        r_tdn = k_slope * (apex[1] - y_tdn)
        T_up = (r_tup * math.cos(th_p), y_tup, r_tup * math.sin(th_p))
        T_dn = (r_tdn * math.cos(th_p), y_tdn, r_tdn * math.sin(th_p))
        _draw_glow_line(gd, cd, pr(T_up), pr(T_dn), SAPPHIRE, width=4, glow_alpha=175)
        _draw_glow_line(gd, cd, pr(P_on), pr(F1), GOLD, width=6, glow_alpha=200)
        _draw_glow_line(gd, cd, pr(P_on), pr(F2), GOLD, width=6, glow_alpha=200)
        _draw_glow_pin(gd, cd, pr(F1), 8, GOLD)
        _draw_glow_pin(gd, cd, pr(F2), 8, GOLD)
        _draw_glow_pin(gd, cd, pr(P_on), 9, MINT)
        _draw_glow_pin(gd, cd, pr(apex), 7, SAPPHIRE)

    else:
        # 직육면체 공간 대각선 (6-3-5 비례): 밑면 피타고라스 직각삼각형 + 입체 내부 황금 대각선
        yaw = -0.62 + 0.50 * math.sin(ang)
        pitch = 0.30 + 0.09 * math.cos(ang)
        dist = 5.75 - 0.35 * math.sin(ang)
        pr = lambda p: _project_3d(p, yaw, pitch, dist)[:2]

        hx, hy, hz = 1.45, 1.15, 0.82
        verts = [
            (-hx, -hy, -hz),
            (hx, -hy, -hz),
            (hx, -hy, hz),
            (-hx, -hy, hz),
            (-hx, hy, -hz),
            (hx, hy, -hz),
            (hx, hy, hz),
            (-hx, hy, hz),
        ]
        pd.polygon([pr(verts[0]), pr(verts[1]), pr(verts[2]), pr(verts[3])], fill=(14, 44, 88, 138))
        pd.polygon([pr(verts[0]), pr(verts[2]), pr(verts[6])], fill=(16, 185, 129, 74))

        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        for i1, i2 in edges:
            _draw_glow_line(gd, cd, pr(verts[i1]), pr(verts[i2]), SAPPHIRE, width=4, glow_alpha=120)

        # 밑면 대각선(에메랄드) + 높이 모서리(앰버) + 공간 대각선(골드)
        _draw_glow_line(gd, cd, pr(verts[0]), pr(verts[2]), EMERALD, width=7)
        _draw_glow_line(gd, cd, pr(verts[2]), pr(verts[6]), AMBER, width=7)
        _draw_glow_line(gd, cd, pr(verts[0]), pr(verts[6]), GOLD, width=9, glow_alpha=215)
        for vi in (0, 2, 6):
            _draw_glow_pin(gd, cd, pr(verts[vi]), 9, GOLD if vi in (0, 6) else EMERALD)

    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(11))
    comp = Image.alpha_composite(base, poly_layer)
    comp = Image.alpha_composite(comp, glow_blurred)
    comp = Image.alpha_composite(comp, core_layer)

    # 우측 1/3 HUD 배치 구역 다크 인디고 벨벳 소프트 그라데이션 마감
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for x in range(1120, width):
        a = int(min(185, max(0, (x - 1120) / 380.0 * 175)))
        vd.line([(x, 0), (x, height)], fill=(7, 12, 26, a), width=1)
    comp = Image.alpha_composite(comp, vignette)
    return comp.convert("RGB")


def render_deterministic_3d_spatial_camera_clip(
    slug: str,
    archetype: str,
    out_png: Path,
    out_mp4: Path,
    duration_sec: float = 6.0,
    fps: int = 30,
) -> tuple[Path, Path]:
    """
    1920x1080 마스터 키프레임(.png)과 1080p 30fps 무결점 1인칭 공간 카메라 워킹 비디오(.mp4)를
    임시 디스크 I/O 없이 FFmpeg rawvideo 파이프로 초고속 생성합니다.
    """
    ffmpeg_exe = shutil.which("ffmpeg")
    if not ffmpeg_exe:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    out_png.parent.mkdir(parents=True, exist_ok=True)
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    total_frames = max(60, int(round(duration_sec * fps)))
    key_frame_idx = total_frames // 5

    cmd = [
        ffmpeg_exe,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "1920x1080",
        "-r",
        str(fps),
        "-i",
        "-",
        "-an",
        "-vf",
        "unsharp=5:5:0.45:5:5:0.0,format=yuv420p",
        "-c:v",
        "libx264",
        "-profile:v",
        "high",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert proc.stdin is not None
    try:
        for idx in range(total_frames):
            ph = idx / float(total_frames)
            frm = _render_single_spatial_3d_frame(archetype, ph, 1920, 1080)
            if idx == key_frame_idx or (idx == 0 and not out_png.exists()):
                frm.resize((1920, 1080), Image.Resampling.LANCZOS).save(out_png, quality=96)
            proc.stdin.write(frm.tobytes())
    finally:
        proc.stdin.close()
        proc.wait(timeout=90)

    return out_png, out_mp4


def ensure_spatial_3d_camera_assets(
    bp: dict,
    try_live_labs: bool = False,
    try_google_flow_keyframe: bool = False,
    headless: bool = True,
) -> dict:
    """
    공간기하·원뿔곡선 특수 트랙 에셋 해결기:
    1) 이미 마스터링된 `{slug}_genie_1080p.mp4` 또는 수동 투입된 `{slug}_genie_raw.*` 확인 -> 즉시 1080p 30fps 마스터링.
    2) `try_live_labs=True`이고 Labs 세션이 활성 상태이면 Project Genie 실시간 WASD 월드 녹화 시도.
    3) 미확보 시 기하 오차 0.000%의 1080p 30fps 1인칭 유클리드 3D 월드 카메라 엔진으로 즉시 생성 (비용 0원).
    """
    slug = bp["slug"]
    art_p = NB_ASSETS_DIR / bp["art_file"]
    genie_mp4 = GENIE_CLIPS_DIR / (bp.get("genie_clip") or f"{slug}_genie_1080p.mp4")

    # 1. 외부 드롭인 원본(720p 24fps 등)이 있으면 즉시 1080p 30fps Lanczos+Unsharp 마스터링
    for ext in (".mp4", ".webm", ".mov"):
        raw_cand = GENIE_CLIPS_DIR / f"{slug}_genie_raw{ext}"
        if raw_cand.exists() and not _is_valid_mp4(genie_mp4):
            master_genie_720p_to_1080p_30fps(raw_cand, genie_mp4)

    prompts = build_spatial_world_prompts(slug, bp.get("title_ko") or slug)
    arch = bp.get("spatial_archetype") or prompts["archetype"]

    # 2. 선택적 Google Labs Project Genie 라이브 캡처
    st = _load_genie_state()
    if try_live_labs and not _is_valid_mp4(genie_mp4) and st.get("labs_access_status") not in ("labs_plan_or_sso_gate",):
        probe_and_capture_project_genie_clip(
            slug=slug,
            world_prompt=bp.get("genie_world_prompt") or prompts["world_prompt"],
            keyframe_png=art_p if art_p.exists() else None,
            duration_sec=5.0,
            headless=headless,
        )

    # 3. 선택적 Google Flow Nano Banana 2.1 3D 조각상 키프레임(0크레딧) 보조 생성
    if try_google_flow_keyframe and not art_p.exists():
        try:
            import google_flow_controller as gfc
            gfc.generate_flow_image_16x9(bp.get("flow_image_prompt") or prompts["flow_image_prompt"], art_p, headless=headless)
        except Exception:
            pass

    # 4. 무결점 1080p 30fps 3D 공간 카메라 워킹 클립 & 1920x1080 키프레임 보장
    if not _is_valid_mp4(genie_mp4) or not art_p.exists():
        tmp_png = Path(tempfile.gettempdir()) / f"nb_{slug}_3d_tmp.png"
        target_png = art_p if not art_p.exists() else tmp_png
        render_deterministic_3d_spatial_camera_clip(
            slug=slug,
            archetype=arch,
            out_png=target_png,
            out_mp4=genie_mp4,
            duration_sec=6.0,
            fps=30,
        )
        if tmp_png.exists():
            tmp_png.unlink(missing_ok=True)

    # L7 감사 규격(정확히 1920x1080) 보증
    if art_p.exists():
        with Image.open(art_p) as im:
            if im.size != (1920, 1080):
                im.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS).save(art_p, quality=96)

    return {
        "slug": slug,
        "archetype": arch,
        "art_png": str(art_p),
        "genie_1080p_mp4": str(genie_mp4),
        "ready": art_p.exists() and _is_valid_mp4(genie_mp4),
    }


def get_spatial_genie_status_summary() -> dict:
    st = _load_genie_state()
    clips = sorted(
        p.stem.replace("_genie_1080p", "")
        for p in GENIE_CLIPS_DIR.glob("*_genie_1080p.mp4")
        if _is_valid_mp4(p)
    )
    return {
        "labs_url": PROJECT_GENIE_URL,
        "labs_access_status": st.get("labs_access_status", "untested"),
        "labs_last_checked": st.get("labs_last_checked", ""),
        "mastered_1080p30_spatial_clips": len(clips),
        "spatial_slugs": clips,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Spatial 3D World Camera & Genie 3 Mastering Controller")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("status")
    sub.add_parser("probe-labs")

    p_ing = sub.add_parser("ingest")
    p_ing.add_argument("--slug", required=True)
    p_ing.add_argument("--input", required=True)

    p_gen = sub.add_parser("build-spatial")
    p_gen.add_argument("--slug", required=True)
    p_gen.add_argument("--title", default="")
    p_gen.add_argument("--try-labs", action="store_true")
    p_gen.add_argument("--try-flow-art", action="store_true")

    args = ap.parse_args()
    if args.cmd == "probe-labs":
        p_info = build_spatial_world_prompts("2023011401", "삼수선의 정리")
        res = probe_and_capture_project_genie_clip("2023011401", p_info["world_prompt"], headless=True)
        print(json.dumps({"probe": res, "summary": get_spatial_genie_status_summary()}, ensure_ascii=False, indent=2))
    elif args.cmd == "ingest":
        out = ingest_external_genie_clip(args.slug, Path(args.input))
        print(json.dumps({"ok": bool(out), "out_mp4": str(out) if out else ""}, ensure_ascii=False))
    elif args.cmd == "build-spatial":
        bp_stub = {"slug": args.slug, "art_file": f"nb_{args.slug}_spatial.png", "title_ko": args.title or args.slug}
        res = ensure_spatial_3d_camera_assets(
            bp_stub,
            try_live_labs=args.try_labs,
            try_google_flow_keyframe=args.try_flow_art,
            headless=True,
        )
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(get_spatial_genie_status_summary(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
