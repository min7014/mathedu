#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_submit_youtube_quota_extension.py
======================================
Google 본사 공식 「YouTube Data API v3 할당량 확장 감사 신청서 (Quota Extension Audit Form)」
(https://support.google.com/youtube/contact/yt_api_form?hl=en)
100% 자동 작성 · 증빙 이미지 6종 자동 생성 · 자동 제출(Auto-Submit) 엔진
"""

import json
import os
import subprocess
import silent_subprocess  # noqa: F401 — Windows 백그라운드 완전 무창 강제
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = ROOT_DIR / "youtube_uploads" / "quota_audit_evidence"
VIDEO_BOARD_HTML = ROOT_DIR / "video_board.html"
PRIVACY_HTML = ROOT_DIR / "privacy.html"
TERMS_HTML = ROOT_DIR / "terms.html"

GCP_PROJECT_NUMBER = "711696878912"
GCP_PROJECT_ID = "gen-lang-client-0830926645"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@min7014_ai"
PRIMARY_WEBSITE_URL = "https://min7014.github.io/mathedu/video_board.html"
PRIVACY_POLICY_URL = "https://min7014.github.io/mathedu/privacy.html"
TERMS_URL = "https://min7014.github.io/mathedu/terms.html"


def get_git_user_email() -> str:
    try:
        em = subprocess.check_output(["git", "config", "user.email"], cwd=str(ROOT_DIR)).decode("utf-8").strip()
        if "@" in em:
            return em
    except Exception:
        pass
    return "min7014@gmail.com"


def ensure_privacy_and_terms_links_in_video_board():
    if not VIDEO_BOARD_HTML.exists():
        return
    html = VIDEO_BOARD_HTML.read_text(encoding="utf-8")
    if 'href="privacy.html"' not in html:
        target = '<a href="https://min7014.github.io/" target="_blank" rel="noopener" class="nav-btn">📚 수학자료실 원본 ↗</a>'
        replacement = (
            target
            + '\n      <a href="privacy.html" class="nav-btn">🔒 Privacy Policy</a>'
            + '\n      <a href="terms.html" class="nav-btn">📜 Terms of Service</a>'
        )
        if target in html:
            html = html.replace(target, replacement, 1)
            VIDEO_BOARD_HTML.write_text(html, encoding="utf-8")


def _load_font(size: int):
    for fp in (
        "C:/Windows/Fonts/malgunbd.ttf",
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_architecture_and_user_flow_diagrams() -> dict:
    """
    Google YouTube API 감사 필수 첨부 파일(Architecture Diagram, User Flow Diagram, Upload Flow Diagram)을
    고해상도(1600x1000) PNG로 생성합니다.
    """
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    f_title = _load_font(34)
    f_sub = _load_font(22)
    f_body = _load_font(19)

    # 1. Architecture Diagram (evidence_5_architecture_diagram.png)
    arch_p = EVIDENCE_DIR / "evidence_5_architecture_diagram.png"
    img = Image.new("RGB", (1600, 1000), (11, 17, 32))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((30, 30, 1570, 970), radius=24, fill=(17, 28, 53), outline=(56, 189, 248), width=4)
    d.text((70, 60), "MathEdu Visual Mathematics Platform — YouTube Data API v3 System Architecture", font=f_title, fill=(56, 189, 248))
    d.text((70, 112), f"GCP Project Number: {GCP_PROJECT_NUMBER}  |  Project ID: {GCP_PROJECT_ID}  |  Official Channel: @min7014_ai", font=f_sub, fill=(251, 191, 36))

    boxes = [
        ((70, 200, 480, 520), "1. Content Source Vault\n(min7014.github.io)", [
            "• 1,113+ Original Math Topics",
            "• 847 Step-by-Step Visual Proof PDFs",
            "• 404 Interactive GeoGebra Applets",
            "• 457 AlgeoMath Constructions",
            "• 16,548 Stepping-Stone Quizzes",
        ], (16, 185, 129)),
        ((560, 200, 1020, 520), "2. MathEdu Video Creator Engine\n(Internal Server Pipeline)", [
            "• Renders 4 Educational Editions:",
            "  1) 1080p Standard Visual Proof (KO/EN)",
            "  2) 1080p Socratic Question Classroom",
            "  3) 9:16 Standard #Shorts",
            "  4) 9:16 Question-Asking Q-#Shorts",
            "• Internal Admin OAuth 2.0 Token Only",
        ], (56, 189, 248)),
        ((1100, 200, 1530, 520), "3. YouTube Data API v3\n(& Embedded Player)", [
            "• youtube.videos.insert (1,600u)",
            "• youtube.thumbnails.set (50u)",
            "• youtube.playlists / playlistItems",
            "• Publishes to @min7014_ai Channel",
            "• Embeds Public Videos on:",
            "  min7014.github.io/mathedu/",
        ], (244, 63, 94)),
    ]
    for (x0, y0, x1, y1), header, lines, col in boxes:
        d.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=(15, 23, 42), outline=col, width=3)
        d.text((x0 + 24, y0 + 22), header, font=f_sub, fill=col)
        yy = y0 + 95
        for ln in lines:
            d.text((x0 + 24, yy), ln, font=f_body, fill=(241, 245, 249))
            yy += 36

    # Arrows
    d.line([(480, 360), (560, 360)], fill=(251, 191, 36), width=6)
    d.line([(1020, 360), (1100, 360)], fill=(251, 191, 36), width=6)

    # Bottom Compliance Summary Box
    d.rounded_rectangle((70, 580, 1530, 910), radius=18, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    d.text((100, 608), "YouTube API Services Compliance & Data Governance Architecture", font=f_sub, fill=(16, 185, 129))
    comp_lines = [
        "1) Zero Third-Party OAuth Collection: Only the internal channel owner (@min7014_ai) authenticates via OAuth 2.0 to upload lectures.",
        "2) Students & Teachers Access 100% Free Public Embeds: No login or personal YouTube data is requested from website visitors.",
        "3) Daily Quota Need (500,000 units/day): 1,113 topics x 4 editions x Multilingual updates require ~250 video uploads/updates per day.",
        "4) Full Compliance Links Published at: https://min7014.github.io/mathedu/privacy.html  &  https://min7014.github.io/mathedu/terms.html",
    ]
    yy = 665
    for cl in comp_lines:
        d.text((100, yy), cl, font=f_body, fill=(226, 232, 240))
        yy += 52
    img.save(arch_p)

    # 2. User Flow Diagram (evidence_6_user_flow_diagram.png)
    flow_p = EVIDENCE_DIR / "evidence_6_user_flow_diagram.png"
    img2 = Image.new("RGB", (1600, 1000), (11, 17, 32))
    d2 = ImageDraw.Draw(img2)
    d2.rounded_rectangle((30, 30, 1570, 970), radius=24, fill=(17, 28, 53), outline=(251, 191, 36), width=4)
    d2.text((70, 60), "MathEdu Student & Teacher User Flow — YouTube Player & Curriculum Integration", font=f_title, fill=(251, 191, 36))
    d2.text((70, 112), "Primary Access URL: https://min7014.github.io/mathedu/video_board.html (100% Public, No Login Required)", font=f_sub, fill=(56, 189, 248))

    steps = [
        ("Step 1: Browse 1,113 Math Topics", "Students/teachers visit min7014.github.io/mathedu/video_board.html and filter by 16 math domains or 4 lecture editions."),
        ("Step 2: Watch Official YouTube Lecture", "Users click the YouTube link or embedded player to watch 1080p Visual Proofs, Question-Asking Classrooms, or #Shorts on @min7014_ai."),
        ("Step 3: Interactive GeoGebra & PDF Practice", "Alongside the YouTube video, students manipulate the live GeoGebra geometric construction and review the step-by-step PDF."),
        ("Step 4: Solve 16,548 Stepping-Stone Quizzes", "Students verify their mastery through elementary-to-advanced micro-scaffolding quizzes linked directly to each video."),
    ]
    yy = 195
    for st_title, st_desc in steps:
        d2.rounded_rectangle((90, yy, 1510, yy + 150), radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        d2.text((125, yy + 26), st_title, font=f_sub, fill=(56, 189, 248))
        d2.text((125, yy + 78), st_desc, font=f_body, fill=(241, 245, 249))
        yy += 180
    img2.save(flow_p)

    return {
        "arch": arch_p,
        "flow": flow_p,
    }


def _force_show_chrome_windows():
    """부모 프로세스의 SW_HIDE 상속으로 인해 크롬 창이 숨겨지는 현상을 방지하고 화면 최상단에 강제 표시합니다."""
    if os.name != "nt":
        return
    try:
        import ctypes
        u32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        def _cb(hwnd, _lparam):
            length = u32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                u32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value
                if any(k in title for k in ("YouTube", "Google", "Chrome", "Audit and Quota")):
                    u32.ShowWindow(hwnd, 9)  # SW_RESTORE
                    u32.ShowWindow(hwnd, 5)  # SW_SHOW
                    u32.SetForegroundWindow(hwnd)
            return True
        u32.EnumWindows(WNDENUMPROC(_cb), 0)
    except Exception:
        pass


def _launch_sys_browser(p, headless=False):
    args = [
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        "--new-window",
        "--remote-debugging-port=9233",
    ]
    for ch in ("chrome", "msedge"):
        try:
            return p.chromium.launch(channel=ch, headless=headless, ignore_default_args=["--enable-automation"], args=args)
        except Exception:
            continue
    return p.chromium.launch(headless=headless, args=args)


def capture_live_compliance_screenshots() -> dict:
    """
    Playwright Chromium(Chrome/Edge)을 사용하여 실제 privacy.html, video_board.html, terms.html의
    고해상도(1440x960) 증빙 스크린샷 4종을 촬영합니다.
    """
    from playwright.sync_api import sync_playwright

    ensure_privacy_and_terms_links_in_video_board()
    diag = generate_architecture_and_user_flow_diagrams()

    p_priv = EVIDENCE_DIR / "evidence_1_privacy_policy.png"
    p_home = EVIDENCE_DIR / "evidence_2_homepage_youtube.png"
    p_terms = EVIDENCE_DIR / "evidence_3_terms_of_service.png"
    p_embed = EVIDENCE_DIR / "evidence_4_player_upload_flow.png"

    if not (p_priv.exists() and p_home.exists() and p_terms.exists() and p_embed.exists()):
        with sync_playwright() as p:
            browser = _launch_sys_browser(p, headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 960})

            page.goto(PRIVACY_HTML.resolve().as_uri(), wait_until="load")
            time.sleep(0.5)
            page.screenshot(path=str(p_priv), full_page=True)

            page.goto(TERMS_HTML.resolve().as_uri(), wait_until="load")
            time.sleep(0.5)
            page.screenshot(path=str(p_terms), full_page=True)

            page.goto(VIDEO_BOARD_HTML.resolve().as_uri(), wait_until="load")
            time.sleep(1.2)
            page.screenshot(path=str(p_home), full_page=False)

            page.evaluate("window.scrollBy(0, 520)")
            time.sleep(0.8)
            page.screenshot(path=str(p_embed), full_page=False)

            browser.close()

    return {
        "upload_1_1": p_priv,
        "upload_1_2": p_home,
        "upload_1_3": p_terms,
        "upload_1_4": p_embed,
        "architecture_diagram": diag["arch"],
        "user_flow_diagram": diag["flow"],
    }


def fill_and_submit_youtube_quota_form(headless: bool = False) -> dict:
    """
    https://support.google.com/youtube/contact/yt_api_form?hl=en 에 접속하여
    모든 필수 항목을 자동으로 채우고 6종의 증빙 파일을 첨부한 뒤 제출(Submit)을 실행합니다.
    """
    from playwright.sync_api import sync_playwright

    shots = capture_live_compliance_screenshots()
    contact_email = get_git_user_email()
    from urllib.parse import urlencode
    prefill_params = {
        "hl": "en",
        "organization_country": "other",
        "industry_business_vertical": "education_and_e-learning",
        "youtube_data_api": "google_developer_documentation",
        "gcp_total_numbers": "project_1",
        "expected_api_1": "hundred_thousand",
    }
    form_url = "https://support.google.com/youtube/contact/yt_api_form?" + urlencode(prefill_params)

    result = {
        "form_url": form_url,
        "project_number": GCP_PROJECT_NUMBER,
        "project_id": GCP_PROJECT_ID,
        "contact_email": contact_email,
        "submitted": False,
        "confirmation_text": "",
        "screenshot_after_submit": str(EVIDENCE_DIR / "quota_form_submission_result.png"),
    }

    with sync_playwright() as p:
        browser = _launch_sys_browser(p, headless=headless)
        context = browser.new_context( no_viewport=True )
        page = context.new_page()
        try:
            page.bring_to_front()
        except Exception:
            pass
        print(f"🌐 [1/5] Google YouTube API 할당량 확장 신청서 접속 중: {form_url}", flush=True)
        page.goto(form_url, wait_until="networkidle", timeout=60000)
        try:
            page.bring_to_front()
            _force_show_chrome_windows()
        except Exception:
            pass
        time.sleep(2.0)

        def check_box(sel):
            try:
                page.evaluate("""(s) => {
                    const el = document.querySelector(s);
                    if (el && !el.checked) {
                        el.click();
                        if (!el.checked) {
                            el.checked = true;
                            el.dispatchEvent(new Event('change', {bubbles: true}));
                        }
                    }
                }""", sel)
                time.sleep(0.15)
            except Exception:
                pass

        def select_sc_dropdown(select_id, option_text):
            try:
                box = page.locator(f'[data-prefill-id="{select_id}"] .sc-select, #{select_id} ~ .sc-select').first
                if box.count() > 0:
                    box.scroll_into_view_if_needed(timeout=4000)
                    box.click(timeout=4000)
                    time.sleep(0.35)
                    opt = page.locator(f'[data-prefill-id="{select_id}"] li:has-text("{option_text}"), .sc-select-show li:has-text("{option_text}")').first
                    if opt.count() > 0:
                        opt.click(timeout=4000)
                        time.sleep(0.35)
                        return
                page.select_option(f"#{select_id}", label=option_text)
            except Exception as e:
                print(f"   [Dropdown Notice ({select_id})]: {e}", flush=True)

        def fill_val(sel, val):
            try:
                page.evaluate("""([s, v]) => {
                    const el = document.querySelector(s);
                    if (el) {
                        el.focus();
                        el.value = v;
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                        el.dispatchEvent(new Event('blur', {bubbles: true}));
                    }
                }""", [sel, val])
            except Exception:
                pass

        print("✍️ [2/5] 섹션 1~4 (조직 정보, 연락처, 비즈니스 모델, API 클라이언트 URL) 자동 입력 중...", flush=True)
        # Section 1: Request Type
        check_box("#first_section_header--show_1")
        check_box("#reason_for_filling--quota")

        # Section 2: Organization and Contact Information
        check_box("#second_section_header--show_2")
        check_box("#application_type--individual")
        fill_val("#full_name", "Eunki Min")
        fill_val("#organization_name", "MathEdu Visual Mathematics Research Lab")
        fill_val("#organization_website", PRIMARY_WEBSITE_URL)
        select_sc_dropdown("organization_country", "Other (please specify)")
        fill_val("#organization_country_other", "South Korea")
        fill_val("#organization_address", "Seoul, Republic of Korea")
        fill_val("#organization_city", "Seoul")
        fill_val("#organization_state_province", "Seoul")
        fill_val("#organization_postal_code", "04524")
        select_sc_dropdown("industry_business_vertical", "Education and E-Learning")
        check_box("#business_type--educational_institution")

        fill_val("#pimary_contact_name", "Eunki Min")
        fill_val("#organization_contact_email_address", contact_email)
        check_box("#primary_technical_contact_title--similar_primary_contact")
        fill_val("#primary_technical_contact_name", "Eunki Min")
        fill_val("#primary_technical_contact_email", contact_email)
        check_box("#primary_business_contact_header--similar_primary_contact")
        fill_val("#primary_business_contact_name", "Eunki Min")
        fill_val("#primary_business_contact_email", contact_email)

        # Section 3: Business Model and Google Contacts
        check_box("#third_section_header--show_3")
        fill_val(
            "#organization_work_related_yt",
            "MathEdu Visual Mathematics Platform (https://min7014.github.io/mathedu/video_board.html) is a free mathematics education platform containing 1,113 original step-by-step visual proof PDFs, 404 GeoGebra applets, and 16,548 interactive quizzes. We use YouTube Data API v3 solely to publish our own original 1080p & Shorts math proof lectures to our official YouTube channel (https://www.youtube.com/@min7014_ai) and organize them into curriculum playlists for students and teachers worldwide.",
        )
        check_box("#primary_audience--educators")
        check_box("#primary_audience--general_viewers")
        check_box("#client_revenue--free_service")
        check_box("#advertising_displayed--no")
        check_box("#commercial_use_approval--no")
        check_box("#google_youtube_partner_manager--no_google_representative")
        select_sc_dropdown("youtube_data_api", "Google Developer Documentation")
        fill_val("#content_owner_id", "N/A")
        fill_val("#associated_channel_url", YOUTUBE_CHANNEL_URL)
        fill_val("#google_ads_customer_ids", "N/A")

        # Section 4: API Client Overview and Access Information
        check_box("#fourth_section_header--show_4")
        fill_val("#api_client_form", "MathEdu Visual Math Lecture Publisher")
        check_box("#api_name_youtube_check--no")
        fill_val("#primary_access_url", PRIMARY_WEBSITE_URL)
        fill_val("#privacy_policy_url", PRIVACY_POLICY_URL)
        fill_val("#terms_of_service_url", TERMS_URL)
        check_box("#public_private_api--no")
        fill_val("#commercialize_api_demo_account", "Public educational website (no login required): https://min7014.github.io/mathedu/video_board.html")
        check_box("#acknowledgement--acknowledged")

        print(f"🔢 [3/5] 섹션 5 (GCP Project #{GCP_PROJECT_NUMBER}, 희망 쿼터 500,000 units/day) 자동 입력 중...", flush=True)
        # Section 5: Use Cases and Quota Extension Details
        check_box("#fifth_section_header--show_5")
        select_sc_dropdown("gcp_total_numbers", "1")
        time.sleep(0.5)
        fill_val("#google_cloud_project_1", GCP_PROJECT_NUMBER)
        check_box("#use_case_project_1--video_uploading")
        check_box("#use_case_project_1--education")
        check_box("#use_case_project_1--website")
        check_box("#auth_type_project_1--no")
        check_box("#analytics_acknowledgement_1--yes")
        select_sc_dropdown("expected_api_1", "10,000 to 100,000 requests per day")

        check_box("#endpoint_title_1--select_endpoint")
        check_box("#endpoints_selection_1--videos_insert")
        check_box("#endpoints_selection_1--channels_list")
        check_box("#endpoints_selection_1--channels_update")
        check_box("#endpoints_selection_1--comment_threads_insert")

        check_box("#project_1_requested_quota--default")
        fill_val("#default_per_day_project_1", "500000")
        fill_val(
            "#use_api_justification_project_1",
            "We have 1,113 original visual mathematics proof topics across 16 curriculum domains. Each topic is rendered in 4 educational editions (1080p Standard Visual Proof, 1080p Socratic Question-Asking Classroom, 9:16 Standard #Shorts, 9:16 Question-Asking Q-#Shorts) in Korean and English (total 8,904 educational videos), plus 35-minute domain Masterclass compilations. We require 500,000 daily quota units to publish, update thumbnails/captions/localizations, and organize playlists for up to 250 educational math videos per day.",
        )
        check_box("#videos_insert_checkbox_1--videos_insert")
        fill_val("#videos_insert_per_day_1", "400000")
        fill_val(
            "#videos_insert_justification_1",
            "Uploading 250 educational mathematics proof videos per day (across 1,113 topics x 4 editions x KO/EN) at 1,600 units per videos.insert call requires 400,000 units/day.",
        )

        # Section 6 & 7: Evidence Files & Attestations
        check_box("#evidence_section_header--show")
        check_box("#seventh_section_header--show")
        check_box("#policy_acknowledgement--api_service_terms")
        check_box("#policy_acknowledgement--google_privacy_policy")
        check_box("#policy_acknowledgement--current_future_compliance")
        check_box("#policy_acknowledgement--termination_understanding")
        check_box("#policy_acknowledgement--waiver")
        check_box("#truthfulness_attestation--accuracy")
        check_box("#data_usage_consent--submissiton_data")
        check_box("#data_usage_consent--supporting_recording_consent")

        print("📎 [4/5] 필수 증빙 스크린샷 및 아키텍처 다이어그램 6종 파일 첨부 중...", flush=True)
        for field_id, fpath in shots.items():
            try:
                inp = page.locator(f"#{field_id}")
                if inp.count() > 0:
                    inp.set_input_files(str(fpath))
                    print(f"   ✅ 첨부 완료: #{field_id} <- {fpath.name}", flush=True)
            except Exception as fe:
                print(f"   ⚠️ 첨부 안내 (#{field_id}): {fe}", flush=True)

        time.sleep(1.5)
        page.screenshot(path=str(EVIDENCE_DIR / "quota_form_before_submit.png"), full_page=False)

        print("🚀 [5/5] Google YouTube API 할당량 확장 신청서 전 항목 및 첨부파일 6종 입력 완료!", flush=True)
        try:
            submit_btn = page.locator('button.submit-button, input[type="submit"], button:has-text("Submit")').first
            if submit_btn.count() > 0:
                submit_btn.scroll_into_view_if_needed(timeout=5000)
                submit_btn.click(timeout=5000)
                time.sleep(2.0)
        except Exception as se:
            print(f"   ⚠️ 스크롤 안내: {se}", flush=True)

        body_txt = page.inner_text("body")
        if "Your email has been sent" not in body_txt and not headless:
            page.evaluate("""() => {
                const b = document.createElement('div');
                b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#0284c7;color:#fff;padding:16px 24px;font-size:18px;font-weight:bold;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,0.4);font-family:sans-serif;';
                b.innerHTML = '✅ [전 항목 + 증빙 파일 6종 100% 자동 입력 완료!] 화면 하단의 [로봇이 아닙니다(reCAPTCHA)] 체크 후 [Submit] 버튼만 눌러주시면 즉시 제출됩니다!';
                document.body.prepend(b);
            }""")
            _force_show_chrome_windows()
            print("⏳ [사용자 1클릭 대기 중] 열린 크롬 창 하단에서 reCAPTCHA 체크 후 [Submit]을 누르면 자동 감지 후 완료됩니다...", flush=True)
            for _ in range(300):
                try:
                    bt = page.inner_text("body")
                    if "Your email has been sent" in bt:
                        body_txt = bt
                        break
                except Exception:
                    break
                time.sleep(2.0)

        errs = []
        try:
            errs = page.evaluate("""() => {
                const out = [];
                document.querySelectorAll('.error-message, .sc-select-error, [aria-invalid="true"], .field-error').forEach(e => {
                    if (e.offsetParent !== null || e.getAttribute('aria-invalid') === 'true') {
                        const p = e.closest('.field, .prefill-container, div');
                        out.push((e.id || e.name || e.className) + ' -> ' + (p ? p.innerText.slice(0, 120).replace(/\\n+/g, ' ') : e.innerText));
                    }
                });
                return out;
            }""")
        except Exception:
            pass
        result["validation_notes"] = errs
        try:
            page.screenshot(path=str(EVIDENCE_DIR / "quota_form_bottom_result.png"), full_page=False)
        except Exception:
            pass
        if "Your email has been sent" in body_txt:
            result["submitted"] = True
            result["confirmation_text"] = "Your email has been sent"
        else:
            result["page_excerpt"] = body_txt[-800:]

        browser.close()

    out_json = EVIDENCE_DIR / "quota_submission_report.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return result


if __name__ == "__main__":
    fill_and_submit_youtube_quota_form(headless=False)
