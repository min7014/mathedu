#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
google_flow_controller.py
===============================================================================
🎬 [Google Flow ULTRA Headless Automation Engine]
- 회장님(`min7014`)의 Google AI ULTRA 구독 계정(`https://flow.google.com/`)을
  100% 무창 헤드리스(`headless=True`, Rule 48)로 구동하여:
  1) Nano Banana 2.1 (16:9, x1, Flow 0크레딧 · Antigravity 0쿼터) 무결점 기하 오브제 키프레임 생성
  2) Veo 3.1 - Lite (동영상 · 프레임 모드 · 16:9 · 8초 · x1, Flow 5크레딧 · Antigravity 0쿼터)
     [시작 프레임 = 종료 프레임] 양단 기하 고정(Locked-Keyframe Seamless Loop) 실사 광학 모션 클립(.mp4) 생성
- Rule 44 (수학적 오류 ZERO): 생성 프롬프트에 텍스트·수식·숫자 금지 강제 + 양단 키프레임 고정으로 도형 왜곡 원천 차단.
- Rule 51 (상표권 보호): 대외 유튜브 메타데이터에는 모델명을 노출하지 않으며 순수 시각 배경 레이어로만 합성.
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import argparse
import io
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent
NB_ASSETS_DIR = ROOT_DIR / "youtube_uploads" / "nano_banana_assets"
FLOW_CLIPS_DIR = ROOT_DIR / "youtube_uploads" / "flow_clips"
FLOW_STATE_FILE = ROOT_DIR / ".agents" / "google_flow_state.json"

NB_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_PROJECT_URL = "https://flow.google.com/project/74842193-a73f-4209-989d-a080d583bbba"

ZERO_TEXT_GUARD_SUFFIX = (
    " Strict top-down or architectural studio lighting. "
    "Zero text, zero numbers, zero letters, zero mathematical symbols anywhere in the scene."
)

DEFAULT_LOCKED_MOTION_PROMPT = (
    "Locked static top-down 90-degree orthographic camera. All geometric lines, crystal pins, and brass rims remain "
    "100% stationary in exact position. Gentle luminous emerald-teal and warm amber-gold photonic light pulses shimmer "
    "and flow smoothly along the existing beams with subtle realistic sapphire glass reflections on dark midnight velvet. "
    "Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers."
)


def _load_flow_state() -> dict:
    st = {"project_url": DEFAULT_PROJECT_URL, "generated_images": [], "generated_videos": []}
    if FLOW_STATE_FILE.exists():
        try:
            st.update(json.loads(FLOW_STATE_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return st


def _save_flow_state(st: dict) -> None:
    FLOW_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    FLOW_STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def _dismiss_flow_popups(page) -> None:
    for lbl in ["동의함", "Accept", "시작하기"]:
        loc = page.get_by_role("button", name=lbl)
        if loc.count() > 0 and loc.first.is_visible():
            try:
                loc.first.click(timeout=2000)
                time.sleep(0.8)
            except Exception:
                pass


def _open_flow_workspace(page, state: dict) -> str:
    target_url = state.get("project_url") or DEFAULT_PROJECT_URL
    page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
    time.sleep(5.0)
    _dismiss_flow_popups(page)

    if "/project/" not in page.url:
        for lbl in ["새 프로젝트", "New project"]:
            btn = page.get_by_text(lbl)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=8000)
                time.sleep(5.0)
                break
        _dismiss_flow_popups(page)

    if "/project/" in page.url and page.url != state.get("project_url"):
        state["project_url"] = page.url
        _save_flow_state(state)
    return page.url


def _upload_and_select_frame_in_modal(page, image_path: Path, prefer_latest_project_asset: bool = False) -> bool:
    """
    '프레임 이미지 선택' 모달이 열린 상태에서:
    1) `prefer_latest_project_asset=True`이고 이미 프로젝트 내에 방금 생성/업로드된 에셋이 선택되어 있으면 즉시 '프롬프트에 추가' 클릭.
    2) 그렇지 않으면 '미디어 업로드'로 로컬 1920x1080 검증 키프레임을 업로드하고,
       크롭/확인 오버레이('자르기 및 저장' / '저장' / '확인')가 뜨면 이를 먼저 승인한 뒤 '프롬프트에 추가'를 완료합니다.
    """
    time.sleep(1.2)
    if prefer_latest_project_asset:
        add_btn = page.locator("button.detail-add-to-prompt-btn, button:has-text('프롬프트에 추가')").last
        if add_btn.count() > 0 and add_btn.is_visible():
            page.evaluate("(el) => el.click()", add_btn.element_handle())
            time.sleep(1.2)
            return True

    up_btn = page.locator("button:has-text('미디어 업로드'), button:has-text('Upload')").first
    if up_btn.count() > 0 and up_btn.is_visible():
        try:
            with page.expect_file_chooser(timeout=8000) as fc_info:
                up_btn.click(timeout=5000)
            fc = fc_info.value
            fc.set_files(str(image_path))
            time.sleep(3.5)
        except Exception:
            f_in = page.locator("input[type='file']")
            if f_in.count() > 0:
                f_in.first.set_input_files(str(image_path))
                time.sleep(3.5)

        # Handle Google Flow's first-time upload consent modal OR crop/save dialog (.cdk-overlay-container)
        for _ in range(10):
            if page.locator(".blurred-backdrop").count() == 0:
                break
            overlay_btns = page.evaluate(
                """() => Array.from(document.querySelectorAll('.cdk-overlay-container button'))
                    .filter(b => b.offsetParent !== null && !b.disabled)
                    .map(b => ({txt: (b.innerText || '').trim(), aria: b.getAttribute('aria-label') || ''}))"""
            )
            clicked_overlay = False
            for kw in ["동의", "계속", "자르기", "저장", "확인", "완료", "Agree", "Continue", "Crop", "Save"]:
                cand = page.locator(f".cdk-overlay-container button:has-text('{kw}')")
                if cand.count() > 0 and cand.last.is_visible():
                    page.evaluate("(el) => el.click()", cand.last.element_handle())
                    clicked_overlay = True
                    time.sleep(2.5)
                    break
            if not clicked_overlay and overlay_btns:
                # Click last visible enabled button in top overlay dialog (usually primary confirm CTA)
                all_cands = page.locator(".cdk-overlay-container [role='dialog'] button, .cdk-overlay-popover button")
                if all_cands.count() > 0:
                    page.evaluate("(el) => el.click()", all_cands.last.element_handle())
                    time.sleep(2.5)
            time.sleep(0.8)

    # Check if upload+crop already auto-attached the frame and closed all modals
    for _ in range(8):
        if page.locator(".cdk-overlay-backdrop-showing").count() == 0:
            return True
        add_btn = page.locator("button.detail-add-to-prompt-btn, button:has-text('프롬프트에 추가'), button:has-text('Add to prompt')").last
        if add_btn.count() > 0 and add_btn.is_visible() and page.locator(".blurred-backdrop").count() == 0:
            page.evaluate("(el) => el.click()", add_btn.element_handle())
            time.sleep(1.2)
            return True
        time.sleep(1.0)

    page.keyboard.press("Escape")
    time.sleep(0.8)
    return False


def generate_flow_image_16x9(prompt: str, out_png: Path, headless: bool = True) -> Path | None:
    """
    Google Flow ULTRA의 Nano Banana 2.1 (16:9, x1, 0크레딧)로 무결점 기하 오브제 마스터 이미지를 생성하고
    1920x1080 고해상도 PNG로 정규화 저장합니다.
    """
    from playwright.sync_api import sync_playwright
    import youtube_community_controller as ycc

    clean_prompt = prompt.strip()
    if "zero text" not in clean_prompt.lower():
        clean_prompt += ZERO_TEXT_GUARD_SUFFIX

    if not ycc._acquire_robot_lock():
        return None

    st = _load_flow_state()
    try:
        with sync_playwright() as p:
            ctx = ycc._launch_robot_context(p, headless=headless)
            try:
                page = ctx.new_page()
                captured_images: list[tuple[int, bytes]] = []

                def _on_resp(resp):
                    ct = (resp.headers.get("content-type") or "").lower()
                    if ("image/png" in ct or "image/jpeg" in ct or "image/webp" in ct) and resp.status == 200:
                        if "flow-content.google" in resp.url or "aisandbox" in resp.url or "googleusercontent" in resp.url:
                            try:
                                b = resp.body()
                                if len(b) > 90_000:
                                    captured_images.append((len(b), b))
                            except Exception:
                                pass

                page.on("response", _on_resp)
                _open_flow_workspace(page, st)

                # Clear existing image count baseline
                before_srcs = set(
                    page.evaluate("""() => Array.from(document.querySelectorAll('img')).map(i => i.src).filter(Boolean)""")
                )
                captured_images.clear()

                # Configure: 이미지 -> 16:9 -> x1 (Nano Banana 2.1, 0 credits)
                trig = page.locator("button[aria-label='설정 트리거']").first
                trig.click(timeout=5000)
                time.sleep(1.0)
                page.locator("button[role='radio']:has-text('이미지')").first.click(timeout=5000)
                time.sleep(0.6)
                page.locator("button[role='radio']:has-text('16:9')").first.click(timeout=5000)
                time.sleep(0.5)
                page.locator("button[role='radio']:has-text('x1')").first.click(timeout=5000)
                time.sleep(0.5)
                page.keyboard.press("Escape")
                time.sleep(0.8)

                tb = page.locator("div[role='textbox'][aria-label='무엇을 만들고 싶으신가요?']").first
                tb.click(timeout=5000)
                tb.fill(clean_prompt)
                time.sleep(0.8)
                page.locator("button[aria-label='생성 시작']").first.click(timeout=5000)

                raw_bytes = None
                for _ in range(65):
                    time.sleep(1.0)
                    if captured_images and max(x[0] for x in captured_images) > 220_000:
                        time.sleep(1.5)
                        captured_images.sort(key=lambda x: x[0], reverse=True)
                        raw_bytes = captured_images[0][1]
                        break
                    curr_imgs = page.evaluate(
                        """() => Array.from(document.querySelectorAll('img')).map(i => ({src: i.src, w: i.naturalWidth}))"""
                    )
                    new_big = [i["src"] for i in curr_imgs if i["src"] not in before_srcs and i["w"] >= 800 and "flow-content.google" in i["src"]]
                    if new_big:
                        r = ctx.request.get(new_big[-1], timeout=30000)
                        if r.ok and len(r.body()) > 150_000:
                            raw_bytes = r.body()
                            break

                if not raw_bytes:
                    return None

                out_png.parent.mkdir(parents=True, exist_ok=True)
                im = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
                if im.size != (1920, 1080):
                    im = im.resize((1920, 1080), Image.Resampling.LANCZOS)
                im.save(out_png, quality=98)

                st.setdefault("generated_images", []).append(
                    {"out_png": str(out_png.relative_to(ROOT_DIR)).replace("\\", "/"), "ts": datetime.now().isoformat(timespec="seconds")}
                )
                _save_flow_state(st)
                return out_png
            finally:
                ctx.close()
    finally:
        ycc._release_robot_lock()


def generate_flow_locked_motion_clip(
    start_png: Path,
    out_mp4: Path,
    motion_prompt: str = DEFAULT_LOCKED_MOTION_PROMPT,
    lock_end_frame: bool = True,
    model_name: str = "Veo 3.1 - Lite",
    use_latest_project_asset: bool = False,
    headless: bool = True,
) -> Path | None:
    """
    검증된 1920x1080 기하 키프레임(`start_png`)을 Google Flow ULTRA의
    [동영상 -> 프레임 -> 16:9 -> Veo 3.1 - Lite (5크레딧) -> x1] 모드에서
    '시작' 프레임(및 `lock_end_frame=True` 시 '종료' 프레임)에 고정하여
    기하 왜곡 0% + 무한 심리스 루프가 가능한 8초 실사 광학 모션 비디오(`.mp4`)를 생성·저장합니다.
    """
    from playwright.sync_api import sync_playwright
    import youtube_community_controller as ycc

    if not start_png.exists():
        raise FileNotFoundError(f"Start frame not found: {start_png}")

    if not ycc._acquire_robot_lock():
        return None

    st = _load_flow_state()
    try:
        with sync_playwright() as p:
            ctx = ycc._launch_robot_context(p, headless=headless)
            try:
                page = ctx.new_page()
                captured_videos: list[tuple[int, bytes]] = []

                def _on_resp(resp):
                    ct = (resp.headers.get("content-type") or "").lower()
                    u = resp.url
                    if ("video/" in ct or "flow-content.google/video" in u or ".mp4" in u.lower()) and resp.status == 200:
                        try:
                            b = resp.body()
                            if len(b) > 250_000:
                                captured_videos.append((len(b), b))
                        except Exception:
                            pass

                page.on("response", _on_resp)
                _open_flow_workspace(page, st)

                before_asb_imgs = set(
                    page.evaluate(
                        """() => Array.from(document.querySelectorAll("img[src*='/asb/']")).map(i => i.src).filter(Boolean)"""
                    )
                )
                captured_videos.clear()

                # 1. Configure settings: 동영상 -> 프레임 -> 16:9 -> x1 -> Veo 3.1 - Lite
                trig = page.locator("button[aria-label='설정 트리거']").first
                trig.click(timeout=5000)
                time.sleep(1.0)
                page.locator("button[role='radio']:has-text('동영상')").first.click(timeout=5000)
                time.sleep(0.8)
                page.locator("button[role='radio']:has-text('프레임')").first.click(timeout=5000)
                time.sleep(0.7)
                page.locator("button[role='radio']:has-text('16:9')").first.click(timeout=5000)
                time.sleep(0.6)
                page.locator("button[role='radio']:has-text('x1')").first.click(timeout=5000)
                time.sleep(0.6)

                dd = page.locator("button[aria-label='모델 제품군 선택']").first
                dd.click(timeout=5000)
                time.sleep(0.7)
                opt = page.get_by_text(model_name, exact=False).last
                if opt.count() > 0 and opt.is_visible():
                    opt.click(timeout=5000)
                    time.sleep(0.8)
                page.keyboard.press("Escape")
                time.sleep(0.9)

                # Ensure no overlay backdrop remains open
                if page.locator(".cdk-overlay-backdrop-showing").count() > 0:
                    page.keyboard.press("Escape")
                    time.sleep(0.6)

                # 2. Attach Start Frame ('시작')
                start_slot = page.locator("button:has-text('시작')").last
                if start_slot.count() > 0 and start_slot.is_visible():
                    start_slot.click(timeout=5000)
                    _upload_and_select_frame_in_modal(page, start_png, prefer_latest_project_asset=use_latest_project_asset)

                # 3. Optionally lock End Frame ('종료') to the exact same uploaded asset for 100% loop invariance
                if lock_end_frame:
                    end_slot = page.locator("button:has-text('종료')").last
                    if end_slot.count() > 0 and end_slot.is_visible():
                        end_slot.click(timeout=5000)
                        _upload_and_select_frame_in_modal(page, start_png, prefer_latest_project_asset=True)

                if page.locator(".cdk-overlay-backdrop-showing").count() > 0:
                    page.keyboard.press("Escape")
                    time.sleep(0.8)

                # 4. Enter motion prompt & submit
                tb = page.locator("div[role='textbox'][aria-label='무엇을 만들고 싶으신가요?']").first
                tb.click(timeout=5000)
                tb.fill(motion_prompt)
                time.sleep(0.8)
                page.locator("button[aria-label='생성 시작']").first.click(timeout=5000)

                # 5. Poll up to 140s for new gallery card (img[src*='/asb/']), then open detail view / download button to fetch MP4!
                video_bytes = None
                for _ in range(70):
                    time.sleep(2.0)
                    if captured_videos and max(x[0] for x in captured_videos) > 250_000:
                        captured_videos.sort(key=lambda x: x[0], reverse=True)
                        video_bytes = captured_videos[0][1]
                        break

                    curr_asb = page.evaluate(
                        """() => Array.from(document.querySelectorAll("img[src*='/asb/']")).map(i => i.src).filter(Boolean)"""
                    )
                    new_asb = [u for u in curr_asb if u not in before_asb_imgs]
                    if new_asb:
                        # Click newest generated video card to trigger player stream + download button
                        card_img = page.locator("img[src*='/asb/']").first
                        if card_img.count() > 0 and card_img.is_visible():
                            card_img.click(timeout=5000)
                            time.sleep(2.5)
                        dl_btn = page.locator("button[aria-label='다운로드'], button[aria-label*='Download']").first
                        if dl_btn.count() > 0 and dl_btn.is_visible():
                            try:
                                with page.expect_download(timeout=30000) as dl_info:
                                    dl_btn.click(timeout=5000)
                                    time.sleep(0.8)
                                    sub_opt = page.locator("[role='menuitem']:has-text('720p'), [role='menuitem']:has-text('원본'), button:has-text('720p')").first
                                    if sub_opt.count() > 0 and sub_opt.is_visible():
                                        sub_opt.click(timeout=3000)
                                out_mp4.parent.mkdir(parents=True, exist_ok=True)
                                dl_info.value.save_as(str(out_mp4))
                                if out_mp4.exists() and out_mp4.stat().st_size > 200_000:
                                    video_bytes = out_mp4.read_bytes()
                                    break
                            except Exception:
                                pass
                        if captured_videos and max(x[0] for x in captured_videos) > 250_000:
                            captured_videos.sort(key=lambda x: x[0], reverse=True)
                            video_bytes = captured_videos[0][1]
                            break

                if not video_bytes:
                    return None

                out_mp4.parent.mkdir(parents=True, exist_ok=True)
                out_mp4.write_bytes(video_bytes)
                st.setdefault("generated_videos", []).append(
                    {
                        "out_mp4": str(out_mp4.relative_to(ROOT_DIR)).replace("\\", "/"),
                        "bytes": len(video_bytes),
                        "model": model_name,
                        "locked_loop": lock_end_frame,
                        "ts": datetime.now().isoformat(timespec="seconds"),
                    }
                )
                _save_flow_state(st)
                return out_mp4
            finally:
                ctx.close()
    finally:
        ycc._release_robot_lock()


def main():
    ap = argparse.ArgumentParser(description="Google Flow ULTRA Headless Controller")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("status")

    p_img = sub.add_parser("gen-image")
    p_img.add_argument("--slug", required=True)
    p_img.add_argument("--prompt", required=True)
    p_img.add_argument("--out", default="")

    p_vid = sub.add_parser("gen-video")
    p_vid.add_argument("--slug", required=True)
    p_vid.add_argument("--start-png", required=True)
    p_vid.add_argument("--prompt", default=DEFAULT_LOCKED_MOTION_PROMPT)
    p_vid.add_argument("--model", default="Veo 3.1 - Lite")
    p_vid.add_argument("--no-end-lock", action="store_true")
    p_vid.add_argument("--use-latest-project-asset", action="store_true")

    args = ap.parse_args()
    if args.cmd == "gen-image":
        out_p = Path(args.out) if args.out else (NB_ASSETS_DIR / f"nb_{args.slug}_flow.png")
        res = generate_flow_image_16x9(args.prompt, out_p)
        print(json.dumps({"ok": bool(res), "out_png": str(res) if res else ""}, ensure_ascii=False))
    elif args.cmd == "gen-video":
        out_v = FLOW_CLIPS_DIR / f"{args.slug}_flow.mp4"
        res = generate_flow_locked_motion_clip(
            Path(args.start_png),
            out_v,
            motion_prompt=args.prompt,
            lock_end_frame=not args.no_end_lock,
            model_name=args.model,
            use_latest_project_asset=args.use_latest_project_asset,
        )
        print(json.dumps({"ok": bool(res), "out_mp4": str(res) if res else "", "bytes": out_v.stat().st_size if out_v.exists() else 0}, ensure_ascii=False))
    else:
        st = _load_flow_state()
        clips = [p.name for p in sorted(FLOW_CLIPS_DIR.glob("*.mp4"))]
        print(json.dumps({"state": st, "flow_clips": clips}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
