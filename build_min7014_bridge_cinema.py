#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_min7014_bridge_cinema.py
===============================================================================
🌉 [@min7014 (500 구독자) → @min7014_ai 채널 브릿지 특별 초대 시네마 생성기]
- 오랜 기간 한 땀 한 땀 빚어 온 @min7014 채널(916편 무언 동적 작도)의 진성 구독자 500분을
  말하고 질문하는 차세대 시각 수학 시네마 @min7014_ai 채널로 초대하는 전용 브릿지 패키지 생성
- 산출물 (전량 .gitignore 보호 경로 youtube_uploads/bridge_min7014_to_min7014_ai/ 저장 · Git 용량 0B):
  1) min7014_to_min7014_ai_bridge_1080p.mp4  (1920x1080, 16:9 본편 특별 초대 시네마)
  2) min7014_to_min7014_ai_bridge_shorts.mp4 (1080x1920, 9:16 모바일 구독자 깨우기 #Shorts)
  3) min7014_to_min7014_ai_bridge_thumb.png  (1280x720 고클릭률 비교·초대 썸네일)
  4) upload_kit_for_min7014.txt / .json      (@min7014 채널 즉시 복붙용 제목·설명·고정댓글·커뮤니티 공지)
- 무결성 준수:
  * Rule 13.1: 개인 성함·호칭 노출 ZERO (@min7014, @min7014_ai, 수학자료실 min7014.github.io만 표기)
  * Rule 13.2: .mp4/.png Git 커밋 ZERO (youtube_uploads/ 전용 출력)
  * Rule 28/37/51/52: 미지원 글리프(U+2794 등) ZERO, 강렬한 적색 UI ZERO, 외부 상표권 ZERO
  * Rule 48: silent_subprocess 완전 무창 실행
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 Windows 전 하위 프로세스 완전 무창 강제

import asyncio
import json
import math
import re
import shutil
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path

import edge_tts
import qrcode
from PIL import Image, ImageDraw, ImageFilter

import auditor
import creative_idea_cinema as cic
import min7014_video_maker as vmaker

ROOT_DIR = Path(__file__).resolve().parent
OUT_DIR = ROOT_DIR / "youtube_uploads" / "bridge_min7014_to_min7014_ai"

SUB_URL = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"
CHANNEL_URL = "https://www.youtube.com/@min7014_ai"
ARCHIVE_URL = "https://min7014.github.io/"


def _make_qr_rgba(url: str, box_px: int = 260) -> Image.Image:
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#081020", back_color="#ffffff").convert("RGBA")
    return qr_img.resize((box_px, box_px), Image.Resampling.NEAREST)


def _draw_centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font, fill) -> None:
    x0, y0, x1, y1 = box
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    tx = x0 + (x1 - x0 - tw) // 2 - bb[0]
    ty = y0 + (y1 - y0 - th) // 2 - bb[1]
    draw.text((tx, ty), text, font=font, fill=fill)


def _draw_blueprint_silent_construction(w: int, h: int, t_raw: float, center_xy: tuple[int, int] | None = None, radius: int | None = None) -> Image.Image:
    """@min7014 오리지널 916편의 감성을 담은 클래식 작도 모눈 + 컴퍼스·자 기하 작도 캔버스"""
    img = Image.new("RGB", (w, h), (11, 20, 36))
    draw = ImageDraw.Draw(img, "RGBA")

    step = 44
    for x in range(0, w, step):
        col = (56, 89, 130, 56) if (x // step) % 4 == 0 else (38, 62, 94, 32)
        draw.line([(x, 0), (x, h)], fill=col, width=1)
    for y in range(0, h, step):
        col = (56, 89, 130, 56) if (y // step) % 4 == 0 else (38, 62, 94, 32)
        draw.line([(0, y), (w, y)], fill=col, width=1)

    cx, cy = center_xy if center_xy else (int(w * 0.26), int(h * 0.52))
    r_main = radius if radius else int(min(w, h) * 0.20)

    draw.ellipse((cx - r_main, cy - r_main, cx + r_main, cy + r_main), outline=(148, 197, 235, 175), width=2)
    r_outer = int(r_main * 1.26)
    draw.arc((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer), start=200, end=345, fill=(125, 175, 215, 115), width=2)

    ang_a = math.radians(210)
    ang_b = math.radians(30)
    ang_c = math.radians(295 + 10 * math.sin(t_raw * math.pi))
    ax, ay = cx + r_main * math.cos(ang_a), cy + r_main * math.sin(ang_a)
    bx, by = cx + r_main * math.cos(ang_b), cy + r_main * math.sin(ang_b)
    px, py = cx + r_main * math.cos(ang_c), cy + r_main * math.sin(ang_c)

    poly_pts = []
    for k in range(7):
        th = math.radians(-90 + k * (360.0 / 7.0) + t_raw * 12.0)
        poly_pts.append((cx + r_outer * 0.92 * math.cos(th), cy + r_outer * 0.92 * math.sin(th)))
    for k in range(7):
        p1 = poly_pts[k]
        p2 = poly_pts[(k + 2) % 7]
        draw.line([p1, p2], fill=(148, 163, 184, 92), width=2)

    draw.polygon([(ax, ay), (bx, by), (px, py)], fill=(56, 189, 248, 36), outline=(226, 232, 240, 225))
    draw.line([(ax, ay), (bx, by)], fill=(186, 230, 253, 240), width=3)
    draw.line([(ax, ay), (px, py)], fill=(186, 230, 253, 240), width=3)
    draw.line([(bx, by), (px, py)], fill=(186, 230, 253, 240), width=3)

    f_lbl = vmaker.get_font_for_lang("ko", 19, bold=True)
    for vx, vy, lbl in [(ax, ay, "A"), (bx, by, "B"), (px, py, "P"), (cx, cy, "O")]:
        draw.ellipse((vx - 6, vy - 6, vx + 6, vy + 6), fill=(241, 245, 249, 255), outline=(56, 189, 248, 220), width=2)
        draw.text((vx + 10, vy - 18), lbl, fill=(203, 213, 225, 235), font=f_lbl)

    return img


def render_act1_evolution_scene(w: int, h: int, t_raw: float) -> Image.Image:
    """Act 1: 좌측 뷰포트(x=36..1256) 안에서 왼쪽 클래식 무언 작도(@min7014)와 오른쪽 네온 피타고라스 시네마(@min7014_ai)를 대조"""
    comp = _draw_blueprint_silent_construction(w, h, t_raw, center_xy=(332, 540), radius=178)

    # 우측 뷰포트 영역(x=636..1258, y=144..842) 안에 네온 피타고라스 나무가 또렷하게 중앙 배치되도록 합성
    neon_panel = cic.render_pure_procedural_scene(960, 720, "pythagoras_fractal", 1, 0.35 + 0.65 * t_raw, lang_code="ko")
    neon_crop = neon_panel.crop((60, 10, 682, 708))
    comp.paste(neon_crop, (636, 144))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    split_x = 636
    gd.line([(split_x, 144), (split_x, 842)], fill=(250, 204, 21, 235), width=10)
    gd.line([(split_x, 144), (split_x, 842)], fill=(56, 189, 248, 175), width=20)
    glow = glow.filter(ImageFilter.GaussianBlur(9))
    overlay = Image.alpha_composite(overlay, glow)

    od = ImageDraw.Draw(overlay)
    od.line([(split_x, 144), (split_x, 842)], fill=(255, 251, 235, 255), width=3)
    od.rounded_rectangle((36, 144, 1258, 842), radius=22, outline=(71, 85, 105, 190), width=2)

    f_tag = vmaker.get_font_for_lang("ko", 21, bold=True)
    f_sub = vmaker.get_font_for_lang("ko", 17, bold=True)
    f_arr = vmaker.get_font_for_lang("ko", 28, bold=True)

    # 좌측 상단 라벨 (@min7014) — x=56..608 (절대 우측 침범 없음)
    od.rounded_rectangle((56, 162, 608, 246), radius=16, fill=(15, 23, 42, 232), outline=(148, 163, 184, 225), width=2)
    od.text((76, 174), "@min7014 · 916편 한 땀 한 땀 작도", fill=(226, 232, 240, 255), font=f_tag)
    od.text((76, 208), "점 · 선 · 원으로 빚어 온 순수 기하학 원천", fill=(148, 163, 184, 245), font=f_sub)

    # 중앙 브릿지 화살표 배지
    od.rounded_rectangle((598, 466, 674, 526), radius=16, fill=(30, 58, 138, 245), outline=(250, 204, 21, 255), width=3)
    _draw_centered_text(od, (598, 466, 674, 526), "→", f_arr, (254, 240, 138, 255))

    # 우측 상단 라벨 (@min7014_ai) — x=664..1240 (x=1280 우측 HUD 카드와 완벽 분리!)
    od.rounded_rectangle((664, 162, 1240, 246), radius=16, fill=(17, 28, 62, 238), outline=(250, 204, 21, 245), width=2)
    od.text((684, 174), "@min7014_ai · 말하고 질문하는 시네마", fill=(254, 240, 138, 255), font=f_tag)
    od.text((684, 208), "단계별 음성 해설 + 네온 보조선 + 4초 발문", fill=(125, 211, 252, 255), font=f_sub)

    # 우측 하단 음성 파형 비주얼라이저 바 — x=664..1240
    od.rounded_rectangle((664, 756, 1240, 824), radius=14, fill=(10, 18, 36, 225), outline=(56, 189, 248, 215), width=2)
    od.text((684, 778), "VOICE + VISUAL PROOF", fill=(125, 211, 252, 255), font=f_sub)
    for bi in range(22):
        bh = int(8 + 16 * abs(math.sin(t_raw * math.pi * 3.0 + bi * 0.55)))
        bx = 936 + bi * 13
        od.rounded_rectangle((bx, 790 - bh, bx + 7, 790 + bh), radius=3, fill=(52, 211, 153, 245))

    return Image.alpha_composite(comp.convert("RGBA"), overlay).convert("RGB")


def render_act4_ecosystem_bento(w: int, h: int, t_raw: float) -> Image.Image:
    """Act 4: 황금나선 배경 위 4대 에디션 생태계 벤토 쇼케이스 (고대비 배지·깔끔한 암막 베일)"""
    bg = cic.render_pure_procedural_scene(w, h, "fibonacci_golden", 4, t_raw, lang_code="ko").convert("RGBA")
    veil = Image.new("RGBA", (w, h), (7, 12, 26, 212))
    canvas = Image.alpha_composite(bg, veil)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cards = [
        (
            "EDITION 01 · 1080p 단계별 본편",
            "눈으로 따라가는 시각적 증명",
            "보조선이 그어지는 이유와 등식의 필연성을\n한국어 · 영어 음성으로 차근차근 해설",
            (56, 189, 248),
        ),
        (
            "EDITION 02 · 질문하는 수학 수업",
            "4초 사고 멈춤 & 소크라테스 발문",
            "정답을 바로 주지 않고 스스로 보조선을\n상상하게 이끄는 탐구 중심 수업 시네마",
            (52, 211, 153),
        ),
        (
            "EDITION 03 · 45초 #Shorts & 마스터클래스",
            "핵심 직관 숏폼부터 30분 정주행까지",
            "출퇴근·등하굣길 45초 유레카 숏폼과\n단원 전체를 꿰뚫는 심층 마스터클래스",
            (250, 204, 21),
        ),
        (
            "EDITION 04 · 수학자료실 100% 연동",
            "min7014.github.io 1,113+ 원문 직결",
            "847+ 시각 증명 PDF · 동적 기하 작도 원문과\n창의 수식 조립 실습까지 완벽 연결",
            (167, 139, 250),
        ),
    ]

    f_tag = vmaker.get_font_for_lang("ko", 19, bold=True)
    f_title = vmaker.get_font_for_lang("ko", 26, bold=True)
    f_desc = vmaker.get_font_for_lang("ko", 20, bold=True)

    positions = [
        (56, 162, 638, 482),
        (666, 162, 1248, 482),
        (56, 508, 638, 828),
        (666, 508, 1248, 828),
    ]
    for idx, ((x0, y0, x1, y1), (badge, title, desc, rgb)) in enumerate(zip(positions, cards)):
        appear = t_raw >= idx * 0.18
        alpha_fill = 236 if appear else 175
        out_col = (*rgb, 245 if appear else 125)
        draw.rounded_rectangle((x0, y0, x1, y1), radius=22, fill=(12, 21, 42, alpha_fill), outline=out_col, width=3)
        # 짙은 네이비 배지 필 + 밝은 네온 테두리 & 텍스트로 100% 고대비 가독성 확보
        draw.rounded_rectangle((x0 + 24, y0 + 22, x0 + 468, y0 + 66), radius=12, fill=(18, 32, 66, 248), outline=(*rgb, 235), width=2)
        draw.text((x0 + 40, y0 + 32), badge, fill=(*rgb, 255), font=f_tag)
        draw.text((x0 + 28, y0 + 92), title, fill=(255, 255, 255, 255), font=f_title)
        for li, line in enumerate(desc.split("\n")):
            draw.text((x0 + 28, y0 + 152 + li * 40), line, fill=(203, 213, 225, 245), font=f_desc)

    return Image.alpha_composite(canvas, overlay).convert("RGB")


def render_act5_invitation_stage(w: int, h: int, t_raw: float) -> Image.Image:
    """Act 5: @min7014 500 구독자 → @min7014_ai 초대 메인 브릿지 카드 + 고대비 QR 코드 + 1클릭 구독 안내"""
    bg = cic.render_pure_procedural_scene(w, h, "pythagoras_fractal", 1, 0.75, lang_code="ko").convert("RGBA")
    veil = Image.new("RGBA", (w, h), (6, 11, 24, 218))
    canvas = Image.alpha_composite(bg, veil)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_h1 = vmaker.get_font_for_lang("ko", 33, bold=True)
    f_h2 = vmaker.get_font_for_lang("ko", 23, bold=True)
    f_body = vmaker.get_font_for_lang("ko", 20, bold=True)
    f_big = vmaker.get_font_for_lang("ko", 42, bold=True)
    f_cta = vmaker.get_font_for_lang("ko", 25, bold=True)

    # 좌측 원천 카드: @min7014
    draw.rounded_rectangle((64, 176, 540, 686), radius=26, fill=(15, 23, 42, 242), outline=(148, 163, 184, 230), width=3)
    draw.rounded_rectangle((92, 208, 360, 254), radius=12, fill=(30, 41, 59, 248), outline=(125, 211, 252, 210), width=2)
    draw.text((112, 219), "ORIGINAL ARCHIVE", fill=(186, 230, 253, 255), font=f_body)
    draw.text((92, 280), "@min7014", fill=(241, 245, 249, 255), font=f_big)
    src_lines = [
        "★ 916편의 한 땀 한 땀 기하 작도",
        "★ 500분의 순수 수학 사랑 구독자",
        "★ 모든 시각적 증명의 뿌리 원천",
        "★ 수학자료실 min7014.github.io",
    ]
    for i, sl in enumerate(src_lines):
        draw.text((92, 374 + i * 62), sl, fill=(203, 213, 225, 248), font=f_body)

    # 중앙 황금 브릿지 화살표 배지 (완벽 중앙 정렬)
    ax0, ax1, ay = 558, 698, 430
    draw.rounded_rectangle((ax0, ay - 36, ax1, ay + 36), radius=18, fill=(30, 58, 138, 242), outline=(250, 204, 21, 255), width=3)
    _draw_centered_text(draw, (ax0, ay - 36, ax1, ay + 36), "→ →", f_h1, (254, 240, 138, 255))

    # 우측 메인 초대 히어로 카드: @min7014_ai + 스캔 가능 QR 코드
    draw.rounded_rectangle((718, 166, 1856, 700), radius=30, fill=(13, 24, 54, 246), outline=(250, 204, 21, 255), width=4)
    draw.rounded_rectangle((754, 198, 1290, 248), radius=14, fill=(88, 28, 135, 248), outline=(250, 204, 21, 240), width=2)
    draw.text((776, 210), "NEW NEXT-GEN VISUAL MATH CINEMA", fill=(254, 240, 138, 255), font=f_body)

    draw.text((754, 270), "@min7014_ai", fill=(56, 189, 248, 255), font=vmaker.get_font_for_lang("ko", 48, bold=True))
    draw.text((754, 344), "말하고 질문하는 1080p 시각 수학 시네마", fill=(255, 255, 255, 255), font=f_h1)

    dest_lines = [
        "▶ 500+편 한국어 · 영어 단계별 음성 해설 완비",
        "▶ 스스로 보조선을 깨치는 [질문하는 수학 수업]",
        "▶ 45초 핵심 직관 #Shorts & 30분 마스터클래스",
        "▶ 지금 [구독] 누르고 첫 번째 가족이 되어 주세요!",
    ]
    for i, dl in enumerate(dest_lines):
        col = (254, 240, 138, 255) if i == 3 else (226, 232, 240, 250)
        draw.text((754, 418 + i * 56), dl, fill=col, font=f_h2)

    # 우측 QR 카드 박스
    qr_img = _make_qr_rgba(SUB_URL, box_px=256)
    qx, qy = 1536, 232
    draw.rounded_rectangle((qx - 18, qy - 18, qx + 256 + 18, qy + 256 + 76), radius=20, fill=(255, 255, 255, 252), outline=(56, 189, 248, 255), width=4)
    overlay.paste(qr_img, (qx, qy), qr_img)
    _draw_centered_text(draw, (qx - 14, qy + 262, qx + 270, qy + 294), "카메라 QR 즉시 구독", f_body, (15, 23, 42, 255))
    _draw_centered_text(draw, (qx - 14, qy + 294, qx + 270, qy + 324), "@min7014_ai", f_body, (30, 64, 175, 255))

    # 하단 1클릭 유도 골드-에메랄드 배너
    glow_w = 3 if int(t_raw * 6) % 2 == 0 else 5
    draw.rounded_rectangle((64, 732, 1856, 832), radius=22, fill=(16, 42, 67, 248), outline=(52, 211, 153, 255), width=glow_w)
    _draw_centered_text(
        draw,
        (64, 732, 1856, 832),
        "▶ 지금 영상 아래 [설명란 첫 줄] 또는 [고정댓글]의 @min7014_ai 링크를 클릭해 구독해 주세요!",
        f_cta,
        (254, 240, 138, 255),
    )

    return Image.alpha_composite(canvas, overlay).convert("RGB")


def build_bridge_acts_16x9() -> list[dict]:
    return [
        {
            "act": 1,
            "mode": "evolution_split",
            "badge": "SPECIAL INVITATION · 01",
            "headline": "한 땀 한 땀 916편의 도형들, 이제 말을 겁니다!",
            "key_formula": "@min7014 (916편) → @min7014_ai",
            "tts_narration": (
                "오랜 시간 한 땀 한 땀 점과 선을 이어 만든 구백열여섯 편의 기하 작도들을 기억하시나요? "
                "말없이 움직이던 그 순수한 도형들을 아껴 주신 오백 분의 구독자 여러분 덕분에, "
                "이제 도형들이 친절한 목소리와 빛나는 보조선으로 직접 말을 걸기 시작했습니다."
            ),
            "subtitles": [
                "오랜 시간 한 땀 한 땀 점과 선을 이어 만든 916편의 기하 작도들을 기억하시나요?",
                "말없이 움직이던 그 순수한 도형들을 아껴 주신 500분의 구독자 여러분 덕분에,",
                "이제 도형들이 친절한 목소리와 빛나는 보조선으로 직접 말을 걸기 시작했습니다!",
            ],
            "hud_notes": [
                "@min7014의 916편 동적 기하 작도 정신을 100% 계승",
                "무언 작도에서 단계별 음성 해설과 네온 보조선 시네마로 진화",
                "500분의 진성 구독자 여러분께 가장 먼저 드리는 초대장",
            ],
        },
        {
            "act": 2,
            "mode": "pythagoras_preview",
            "badge": "PREVIEW 01 · 넓이 불변량",
            "headline": "[미리보기 ①] 128개 가지가 뻗어도 넓이는 왜 25일까?",
            "key_formula": "Level 0 (25) = ... = Level 7 (25)",
            "tts_narration": (
                "새롭게 탄생한 min7014 에이아이 채널의 장면을 미리 만나 보실까요? "
                "하나의 정사각형 기둥에서 백스물여덟 개의 가지가 밤하늘의 숲처럼 피어납니다. "
                "놀랍게도 각 층에 피어난 정사각형 넓이를 모두 더하면, 언제나 맨 아래 뿌리 넓이 스물다섯과 완벽히 일치합니다!"
            ),
            "subtitles": [
                "새롭게 탄생한 @min7014_ai 채널의 장면을 미리 만나 보실까요?",
                "하나의 정사각형 기둥에서 128개의 가지가 밤하늘의 숲처럼 피어납니다.",
                "놀랍게도 각 층의 정사각형 넓이를 모두 더하면 언제나 뿌리 넓이 25와 완벽히 일치합니다!",
            ],
            "hud_notes": [
                "공식 암기 대신 3 · 4 · 5 스물다섯 칸 타일로 눈앞에서 확인",
                "가지가 기하급수로 갈라져도 흔들리지 않는 넓이 보존의 마법",
                "직관적인 시각 애니메이션과 명확한 수식 연결 해설",
            ],
        },
        {
            "act": 3,
            "mode": "ellipse_inquiry_preview",
            "badge": "PREVIEW 02 · 질문하는 수업",
            "headline": "[미리보기 ②] 타원 12줄기 빛과 스스로 깨치는 발문",
            "key_formula": "|PF₁| + |PF₂| = 2a (동시 도착!)",
            "tts_narration": (
                "타원의 한 초점에서 쏜 열두 줄기 빛은 왜 단 영점영일 초의 오차도 없이 반대편 초점에 동시에 도착할까요? "
                "새로운 채널은 정답부터 서둘러 알려주지 않습니다. "
                "보조선을 긋기 전 잠시 멈추어 스스로 질문을 던지게 하고, 접선 너머 대칭점을 잇는 단 한 줄의 보조선으로 유레카의 전율을 선물합니다."
            ),
            "subtitles": [
                "타원의 한 초점에서 쏜 12줄기 빛은 왜 오차 없이 반대편 초점에 동시에 도착할까요?",
                "새로운 @min7014_ai 채널은 정답 공식부터 서둘러 알려주지 않습니다.",
                "잠시 멈추어 스스로 질문하게 하고, 접선 대칭 보조선 한 줄로 유레카의 전율을 선물합니다!",
            ],
            "hud_notes": [
                "정답 제시 전 스스로 생각하게 만드는 [질문하는 수학 수업]",
                "접선 대칭이동 한 줄로 꺾인 빛의 경로를 일직선(2a)으로 해체",
                "교실 탐구 수업 도입 자료와 자기주도 심층 학습에 최적화",
            ],
        },
        {
            "act": 4,
            "mode": "ecosystem_bento",
            "badge": "4-EDITION ECOSYSTEM · 04",
            "headline": "500+편 한·영 시네마와 수학자료실 원문의 완벽 결합",
            "key_formula": "1080p 본편 × 질문수업 × #Shorts",
            "tts_narration": (
                "수학자료실에 축적된 천백여 개의 원문 아이디어가 한국어와 영어 일공팔공 피 본편, "
                "질문하는 수학 수업 특화편, 사십오 초 핵심 숏폼, 그리고 삼십 분 정주행 마스터클래스로 매일 새롭게 태어나고 있습니다. "
                "수업 시간의 탐구 발문 자료로도, 혼자 깊이 사색하는 수학 산책으로도 언제든 활용하실 수 있습니다."
            ),
            "subtitles": [
                "수학자료실(min7014.github.io)의 1,113+ 원문 아이디어가 한국어 · 영어 1080p 본편,",
                "질문하는 수학 수업 특화편, 45초 핵심 #Shorts, 30분 마스터클래스로 매일 태어납니다.",
                "교실 수업의 탐구 발문 자료로도, 혼자 깊이 사색하는 수학 산책으로도 완벽히 준비되어 있습니다!",
            ],
            "hud_notes": [],
        },
        {
            "act": 5,
            "mode": "final_invitation",
            "badge": "JOIN @min7014_ai · 05",
            "headline": "@min7014 500분의 첫 가족을 @min7014_ai로 초대합니다!",
            "key_formula": "설명란 첫 줄 · 고정댓글 링크 클릭!",
            "tts_narration": (
                "오랜 시간 묵묵히 도형의 아름다움을 함께 지켜봐 주신 오백 분의 구독자 여러분이 바로 이 새로운 여정의 가장 소중한 첫 번째 가족입니다. "
                "지금 화면의 큐알 코드를 스캔하시거나, 영상 아래 설명란 첫 줄과 고정댓글의 링크를 눌러 min7014 에이아이 채널의 구독 버튼을 눌러 주세요. "
                "살아 움직이는 다음 증명에서 바로 기다리고 있겠습니다!"
            ),
            "subtitles": [
                "오랜 시간 도형의 아름다움을 함께 지켜봐 주신 500분이 가장 소중한 첫 번째 가족입니다.",
                "지금 화면의 QR 코드를 스캔하거나, 설명란 첫 줄 · 고정댓글 링크로 @min7014_ai를 구독해 주세요!",
                "살아 움직이는 다음 시각 증명 시네마에서 바로 기다리고 있겠습니다!",
            ],
            "hud_notes": [],
        },
    ]


def render_1080p_bridge_video(out_mp4: Path) -> float:
    acts = build_bridge_acts_16x9()
    voice_name = vmaker.GLOBAL_VOICE_MAP["ko"]["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    f_badge = vmaker.get_font_for_lang("ko", 20, bold=True)
    f_head = vmaker.get_font_for_lang("ko", 26, bold=True)
    f_formula = vmaker.get_font_for_lang("ko", 20, bold=True)
    f_bul = vmaker.get_font_for_lang("ko", 21, bold=True)
    f_sub = vmaker.get_font_for_lang("ko", 29, bold=True)

    tmp_dir = Path(tempfile.mkdtemp(prefix="min7014_bridge_1080p_"))
    segs: list[Path] = []
    try:
        for act_info in acts:
            act_num = act_info["act"]
            mode = act_info["mode"]
            tts_narr = act_info["tts_narration"]
            sub_sents = act_info["subtitles"]

            mp3_p = tmp_dir / f"bridge_act_{act_num:02d}.mp3"
            seg_p = tmp_dir / f"bridge_act_{act_num:02d}.mp4"
            comm = edge_tts.Communicate(tts_narr, voice_name, rate="+6%")
            asyncio.run(comm.save(str(mp3_p)))
            dur_s = max(5.0, vmaker.get_media_duration_seconds(mp3_p, ffprobe_exe))

            num_frames = 24
            per_f_dur = dur_s / num_frames
            f_lines: list[str] = []
            last_fp = None

            # 문장 글자수 비율에 맞춰 자연스러운 자막 전환 시점 계산
            sent_weights = [max(1, len(s)) for s in sub_sents]
            total_w = sum(sent_weights)
            cum_bounds = []
            acc = 0.0
            for sw in sent_weights:
                acc += sw / total_w
                cum_bounds.append(acc)

            for fi in range(num_frames):
                t_raw = fi / max(1, num_frames - 1)
                if mode == "evolution_split":
                    scene_rgb = render_act1_evolution_scene(1920, 1080, t_raw)
                elif mode == "pythagoras_preview":
                    scene_rgb = cic.render_pure_procedural_scene(1920, 1080, "pythagoras_fractal", 1, t_raw, lang_code="ko")
                elif mode == "ellipse_inquiry_preview":
                    scene_rgb = cic.render_pure_procedural_scene(1920, 1080, "conic_reflection", 2, t_raw, lang_code="ko")
                elif mode == "ecosystem_bento":
                    scene_rgb = render_act4_ecosystem_bento(1920, 1080, t_raw)
                else:
                    scene_rgb = render_act5_invitation_stage(1920, 1080, t_raw)

                hud = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
                draw = ImageDraw.Draw(hud)

                # 상단 타이틀 바 (절단 없는 완결형 문장 배치)
                draw.rounded_rectangle((36, 22, 1884, 122), radius=20, fill=(10, 18, 36, 220), outline=(56, 189, 248, 225), width=2)
                draw.rounded_rectangle((56, 36, 444, 80), radius=12, fill=(88, 28, 135, 245), outline=(167, 139, 250, 220), width=2)
                _draw_centered_text(draw, (56, 36, 444, 80), cic.sanitize_glyphs(act_info["badge"]), f_badge, (254, 240, 138, 255))

                draw.rounded_rectangle((1524, 36, 1860, 80), radius=14, fill=(15, 118, 110, 245), outline=(250, 204, 21, 245), width=2)
                _draw_centered_text(draw, (1524, 36, 1860, 80), "★ @min7014 → @min7014_ai", f_badge, (254, 240, 138, 255))

                draw.text((466, 42), cic.sanitize_glyphs(act_info["headline"]), fill=(255, 255, 255, 255), font=f_head)

                overall_p = ((act_num - 1) + (fi + 1) / num_frames) / len(acts)
                draw.rounded_rectangle((56, 94, 1860, 108), radius=6, fill=(30, 41, 59, 220))
                draw.rounded_rectangle((56, 94, 56 + max(24, int(1804 * overall_p)), 108), radius=6, fill=(250, 204, 21, 255))

                # Act 1~3일 때 우측 글래스모피즘 인사이트 카드 표시
                if act_info["hud_notes"]:
                    draw.rounded_rectangle((1280, 144, 1884, 842), radius=24, fill=(10, 18, 36, 218), outline=(250, 204, 21, 220), width=2)
                    draw.rounded_rectangle((1304, 170, 1860, 262), radius=16, fill=(30, 58, 138, 230), outline=(56, 189, 248, 235), width=2)
                    draw.text((1324, 184), "★ BRIDGE HIGHLIGHT", fill=(125, 211, 252, 255), font=f_bul)
                    draw.text((1324, 220), cic.sanitize_glyphs(act_info["key_formula"]), fill=(254, 240, 138, 255), font=f_formula)

                    for bi, b_txt in enumerate(act_info["hud_notes"][:3]):
                        by0 = 290 + bi * 168
                        is_active_b = fi >= int(bi * (num_frames / 3))
                        b_fill = (23, 37, 84, 220) if is_active_b else (15, 23, 42, 170)
                        b_out = (52, 211, 153, 240) if is_active_b else (51, 65, 85, 180)
                        draw.rounded_rectangle((1304, by0, 1860, by0 + 146), radius=16, fill=b_fill, outline=b_out, width=2)
                        b_wrapped = textwrap.wrap(cic.sanitize_glyphs(b_txt), width=23)[:3]
                        for wl_i, wl in enumerate(b_wrapped):
                            draw.text(
                                (1326, by0 + 24 + wl_i * 38),
                                wl,
                                fill=(255, 255, 255, 255) if is_active_b else (148, 163, 184, 220),
                                font=f_bul,
                            )

                    draw.rounded_rectangle((1304, 794, 1860, 832), radius=10, fill=(15, 23, 42, 238), outline=(56, 189, 248, 220), width=1)
                    _draw_centered_text(draw, (1304, 794, 1860, 832), "★ 설명란 첫 줄 · 고정댓글 → @min7014_ai 바로가기", f_formula, (254, 240, 138, 255))
                elif mode == "ecosystem_bento":
                    draw.rounded_rectangle((1280, 162, 1884, 828), radius=24, fill=(10, 18, 36, 236), outline=(250, 204, 21, 240), width=3)
                    draw.text((1316, 196), "@min7014_ai 핵심 구성", fill=(254, 240, 138, 255), font=f_head)
                    summary_items = [
                        "★ 500+편 한·영 시각 증명 아카이브",
                        "★ 매주 신규 심층 시네마 업데이트",
                        "★ 교실 수업 · 자기주도 학습 100% 무료",
                        "★ 설명란 첫 줄 링크로 1초 구독!",
                    ]
                    for si, stxt in enumerate(summary_items):
                        draw.text((1316, 264 + si * 52), stxt, fill=(226, 232, 240, 250), font=f_bul)
                    qr_small = _make_qr_rgba(SUB_URL, box_px=230)
                    draw.rounded_rectangle((1452, 496, 1712, 798), radius=18, fill=(255, 255, 255, 252), outline=(56, 189, 248, 255), width=3)
                    hud.paste(qr_small, (1467, 512), qr_small)
                    _draw_centered_text(draw, (1452, 748, 1712, 792), "QR 스캔 @min7014_ai", f_formula, (15, 23, 42, 255))

                # 하단 시네마틱 문장 단위 동기화 자막 바 (절단 ZERO · 100% 중앙 수직 정렬)
                draw.rounded_rectangle((36, 868, 1884, 1054), radius=20, fill=(8, 14, 28, 235), outline=(56, 189, 248, 220), width=2)
                active_si = 0
                for si, cb in enumerate(cum_bounds):
                    if t_raw <= cb + 1e-6:
                        active_si = si
                        break
                cur_sent = cic.sanitize_glyphs(sub_sents[active_si])
                cur_lines = textwrap.wrap(cur_sent, width=52)
                total_h = len(cur_lines) * 48
                start_y = 868 + (186 - total_h) // 2
                for li, cl in enumerate(cur_lines):
                    _draw_centered_text(draw, (56, start_y + li * 48, 1864, start_y + (li + 1) * 48), cl, f_sub, (254, 240, 138, 255))

                frame_out = Image.alpha_composite(scene_rgb.convert("RGBA"), hud).convert("RGB")
                fp = tmp_dir / f"b1080_a{act_num:02d}_f{fi:02d}.png"
                frame_out.save(fp)
                f_lines.append(f"file '{fp.as_posix()}'")
                f_lines.append(f"duration {per_f_dur:.4f}")
                last_fp = fp

            if last_fp:
                f_lines.append(f"file '{last_fp.as_posix()}'")
            f_txt = tmp_dir / f"b1080_concat_{act_num:02d}.txt"
            f_txt.write_text("\n".join(f_lines), encoding="utf-8")

            chime_wav = vmaker.ensure_harmonic_chime_wav()
            cmd = [
                ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", str(f_txt),
                "-i", str(mp3_p),
                "-i", str(chime_wav),
                "-filter_complex",
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[c];"
                "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-shortest",
                str(seg_p),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segs.append(seg_p)

        concat_p = tmp_dir / "concat_all_1080p.txt"
        concat_p.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
        raw_mp4 = tmp_dir / "raw_bridge_1080p.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_p), "-c", "copy", str(raw_mp4)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        ambient_wav = vmaker.ensure_ambient_pad_wav()
        out_mp4.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-i", str(raw_mp4),
                "-stream_loop", "-1", "-i", str(ambient_wav),
                "-filter_complex",
                "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.12[bgm];"
                "[v][bgm]amix=inputs=2:duration=first:dropout_transition=1[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                str(out_mp4),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return vmaker.get_media_duration_seconds(out_mp4, ffprobe_exe)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def render_shorts_bridge_video(out_short_mp4: Path) -> float:
    """@min7014 모바일 숏폼 피드 구독자까지 깨우는 9:16 (<46s) 컴패니언 브릿지 #Shorts"""
    scenes = [
        {
            "idx": 1,
            "badge": "SPECIAL BRIDGE · 1/4",
            "title": "한 땀 한 땀 916편의 도형들이\n이제 말을 걸기 시작합니다!",
            "formula": "@min7014 → @min7014_ai",
            "archetype": "circle_invariants",
            "act_num": 2,
            "tts_narration": (
                "한 땀 한 땀 만든 구백열여섯 편의 무언 기하 작도를 기억하시나요? "
                "오백 분의 구독자 여러분 덕분에 이제 도형들이 친절한 목소리와 빛나는 보조선으로 살아났습니다!"
            ),
            "caption": "한 땀 한 땀 만든 916편의 무언 기하 작도들이 500분의 구독자 여러분 덕분에 친절한 목소리와 빛나는 보조선으로 살아났습니다!",
        },
        {
            "idx": 2,
            "badge": "EUREKA PREVIEW · 2/4",
            "title": "가지가 128개로 갈라져도\n넓이 합은 영원히 25!",
            "formula": "a² + b² = c² (넓이 보존 불변량)",
            "archetype": "pythagoras_fractal",
            "act_num": 1,
            "tts_narration": (
                "피타고라스 나무의 가지가 백스물여덟 개로 뻗어나가도 각 층의 넓이 합은 뿌리 정사각형 스물다섯과 완벽히 일치합니다!"
            ),
            "caption": "피타고라스 나무의 가지가 128개로 뻗어나가도 각 층의 넓이 합은 뿌리 정사각형 25와 완벽히 일치합니다!",
        },
        {
            "idx": 3,
            "badge": "QUESTION CLASS · 3/4",
            "title": "타원의 12줄기 빛 반사와\n스스로 깨치는 4초 질문 수업",
            "formula": "|PF₁| + |PF₂| = 2a (동시 초점 도착)",
            "archetype": "conic_reflection",
            "act_num": 2,
            "tts_narration": (
                "정답부터 외우지 않고 4초간 스스로 보조선을 상상하게 이끄는 질문하는 수학 수업도 매일 펼쳐집니다."
            ),
            "caption": "정답부터 외우지 않고 4초간 스스로 보조선을 상상하게 이끄는 [질문하는 수학 수업]도 매일 펼쳐집니다!",
        },
        {
            "idx": 4,
            "badge": "INVITATION · 4/4",
            "title": "@min7014 500분의 첫 가족을\n@min7014_ai로 초대합니다!",
            "formula": "고정댓글 · 설명란 링크 1클릭 구독!",
            "archetype": "pythagoras_fractal",
            "act_num": 1,
            "tts_narration": (
                "지금 바로 고정댓글과 설명란의 링크를 눌러 min7014 에이아이 채널을 구독하고 오백 편 이상의 시각 수학 시네마를 만나 보세요!"
            ),
            "caption": "지금 바로 고정댓글 · 설명란의 링크를 눌러 @min7014_ai 채널을 구독하고 500+편의 시각 수학 시네마를 만나 보세요!",
        },
    ]

    voice_name = vmaker.GLOBAL_VOICE_MAP["ko"]["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    f_top = vmaker.get_font_for_lang("ko", 38, bold=True)
    f_sub = vmaker.get_font_for_lang("ko", 24, bold=True)
    f_cap = vmaker.get_font_for_lang("ko", 31, bold=True)

    tmp_dir = Path(tempfile.mkdtemp(prefix="min7014_bridge_short_"))
    segs: list[Path] = []
    try:
        for sc in scenes:
            idx = sc["idx"]
            mp3_p = tmp_dir / f"bshort_{idx:02d}.mp3"
            seg_p = tmp_dir / f"bshort_{idx:02d}.mp4"
            comm = edge_tts.Communicate(sc["tts_narration"], voice_name, rate="+18%")
            asyncio.run(comm.save(str(mp3_p)))
            seg_dur = max(3.0, vmaker.get_media_duration_seconds(mp3_p, ffprobe_exe))

            num_frames = 14
            per_f_dur = seg_dur / num_frames
            f_lines: list[str] = []
            last_fp = None
            cap_lines = textwrap.wrap(cic.sanitize_glyphs(sc["caption"]), width=23)[:5]

            for fi in range(num_frames):
                t_raw = fi / max(1, num_frames - 1)
                scene_rgb = cic.render_pure_procedural_scene(1080, 1920, sc["archetype"], sc["act_num"], t_raw, lang_code="ko")
                hud = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
                draw = ImageDraw.Draw(hud)

                if idx == 4:
                    # 마지막 QR 초대 씬은 배경 수식이 카드 밖으로 비치지 않도록 은은한 딥네이비 베일 적용
                    draw.rectangle((0, 300, 1080, 1320), fill=(7, 12, 26, 190))

                # 상단 헤더 카드
                draw.rounded_rectangle((40, 56, 1040, 294), radius=26, fill=(10, 18, 36, 224), outline=(56, 189, 248, 235), width=3)
                draw.rounded_rectangle((68, 76, 620, 126), radius=16, fill=(88, 28, 135, 245))
                draw.text((86, 86), sc["badge"], fill=(254, 240, 138, 255), font=f_sub)
                draw.text((740, 86), "@min7014_ai", fill=(52, 211, 153, 255), font=f_sub)

                for li, tl in enumerate(sc["title"].split("\n")[:2]):
                    draw.text((72, 144 + li * 52), tl, fill=(255, 255, 255, 255), font=f_top)

                overall_p = ((idx - 1) + (fi + 1) / num_frames) / len(scenes)
                draw.rounded_rectangle((68, 262, 1012, 276), radius=6, fill=(30, 41, 59, 220))
                draw.rounded_rectangle((68, 262, 68 + max(24, int(944 * overall_p)), 276), radius=6, fill=(250, 204, 21, 255))

                if idx == 4:
                    draw.rounded_rectangle((140, 490, 940, 1185), radius=32, fill=(12, 22, 48, 248), outline=(250, 204, 21, 255), width=4)
                    qr_v = _make_qr_rgba(SUB_URL, box_px=340)
                    draw.rounded_rectangle((350, 550, 730, 930), radius=22, fill=(255, 255, 255, 255), outline=(56, 189, 248, 255), width=4)
                    hud.paste(qr_v, (370, 570), qr_v)
                    _draw_centered_text(draw, (140, 965, 940, 1035), "QR 스캔 또는 고정댓글 클릭!", f_top, (254, 240, 138, 255))
                    _draw_centered_text(draw, (140, 1045, 940, 1115), "youtube.com/@min7014_ai", f_cap, (125, 211, 252, 255))

                # 하단 자막 카드
                draw.rounded_rectangle((40, 1335, 1040, 1795), radius=26, fill=(8, 14, 28, 232), outline=(250, 204, 21, 225), width=3)
                draw.text((70, 1362), sc["formula"], fill=(56, 189, 248, 255), font=f_sub)
                draw.rounded_rectangle((708, 1352, 1016, 1404), radius=16, fill=(15, 118, 110, 245), outline=(254, 240, 138, 245), width=2)
                _draw_centered_text(draw, (708, 1352, 1016, 1404), "★ 구독 @min7014_ai", vmaker.get_font_for_lang("ko", 22, bold=True), (254, 240, 138, 255))

                active_ci = min(len(cap_lines) - 1, int(t_raw * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    c_col = (254, 240, 138, 255) if ci == active_ci else (203, 213, 225, 235)
                    draw.text((72, 1432 + ci * 60), cl, fill=c_col, font=f_cap)

                draw.rounded_rectangle((40, 1810, 1040, 1892), radius=20, fill=(30, 58, 138, 245), outline=(250, 204, 21, 245), width=3)
                _draw_centered_text(draw, (40, 1810, 1040, 1892), "▶ 고정댓글 첫 줄 @min7014_ai 링크에서 바로 만나요!", vmaker.get_font_for_lang("ko", 24, bold=True), (254, 240, 138, 255))

                frame_out = Image.alpha_composite(scene_rgb.convert("RGBA"), hud).convert("RGB")
                fp = tmp_dir / f"bshort_{idx:02d}_f{fi:02d}.png"
                frame_out.save(fp)
                f_lines.append(f"file '{fp.as_posix()}'")
                f_lines.append(f"duration {per_f_dur:.4f}")
                last_fp = fp

            if last_fp:
                f_lines.append(f"file '{last_fp.as_posix()}'")
            f_txt = tmp_dir / f"bshort_concat_{idx:02d}.txt"
            f_txt.write_text("\n".join(f_lines), encoding="utf-8")

            chime_wav = vmaker.ensure_harmonic_chime_wav()
            cmd = [
                ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", str(f_txt),
                "-i", str(mp3_p),
                "-i", str(chime_wav),
                "-filter_complex",
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[c];"
                "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-shortest",
                str(seg_p),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segs.append(seg_p)

        concat_p = tmp_dir / "concat_all_short.txt"
        concat_p.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
        raw_short = tmp_dir / "raw_bridge_short.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_p), "-c", "copy", str(raw_short)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        ambient_wav = vmaker.ensure_ambient_pad_wav()
        out_short_mp4.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-i", str(raw_short),
                "-stream_loop", "-1", "-i", str(ambient_wav),
                "-filter_complex",
                "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.13[bgm];"
                "[v][bgm]amix=inputs=2:duration=first:dropout_transition=1[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                str(out_short_mp4),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return vmaker.get_media_duration_seconds(out_short_mp4, ffprobe_exe)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def render_bridge_thumbnail(out_png: Path) -> Path:
    """1280x720 고클릭률 비교·초대 썸네일 (왼쪽 무언 작도 → 오른쪽 네온 피타고라스 나무 + 강렬한 호기심 카피)"""
    w, h = 1280, 720
    left_bg = _draw_blueprint_silent_construction(w, h, 0.45, center_xy=(265, 336), radius=145)
    right_bg = cic.render_pure_procedural_scene(w, h, "pythagoras_fractal", 1, 0.85, lang_code="ko")

    split_x = 520
    base = left_bg.copy()
    base.paste(right_bg.crop((split_x - 140, 0, w - 140, h)), (split_x, 0))

    rgba = base.convert("RGBA")
    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    vd.rectangle((0, 0, w, 118), fill=(6, 11, 24, 185))
    vd.rectangle((0, 470, w, h), fill=(6, 11, 24, 224))
    vd.line([(split_x, 110), (split_x, 472)], fill=(250, 204, 21, 255), width=6)
    rgba = Image.alpha_composite(rgba, veil)

    draw = ImageDraw.Draw(rgba)
    f_pill = vmaker.get_font_for_lang("ko", 26, bold=True)
    f_tag = vmaker.get_font_for_lang("ko", 23, bold=True)
    f_hero1 = vmaker.get_font_for_lang("ko", 52, bold=True)
    f_hero2 = vmaker.get_font_for_lang("ko", 56, bold=True)
    f_cta = vmaker.get_font_for_lang("ko", 30, bold=True)

    draw.rounded_rectangle((36, 24, 742, 90), radius=18, fill=(88, 28, 135, 245), outline=(250, 204, 21, 255), width=3)
    _draw_centered_text(draw, (36, 24, 742, 90), "★ @min7014 구독자 500분께 드리는 특별 초대", f_pill, (254, 240, 138, 255))

    draw.rounded_rectangle((36, 126, 468, 184), radius=14, fill=(15, 23, 42, 235), outline=(148, 163, 184, 230), width=2)
    _draw_centered_text(draw, (36, 126, 468, 184), "@min7014 · 916편 무언 작도", f_tag, (226, 232, 240, 255))

    draw.rounded_rectangle((476, 266, 564, 338), radius=18, fill=(30, 58, 138, 248), outline=(250, 204, 21, 255), width=3)
    _draw_centered_text(draw, (476, 266, 564, 338), "→", f_hero1, (254, 240, 138, 255))

    draw.rounded_rectangle((566, 126, 1244, 184), radius=14, fill=(15, 118, 110, 242), outline=(250, 204, 21, 250), width=3)
    _draw_centered_text(draw, (566, 126, 1244, 184), "@min7014_ai · 목소리 + 보조선 + 질문 시네마!", f_tag, (254, 240, 138, 255))

    draw.text((44, 492), "한 땀 한 땀 만든 도형들이", fill=(255, 255, 255, 255), font=f_hero1)
    draw.text((44, 562), "말하고 질문하기 시작했습니다!", fill=(250, 204, 21, 255), font=f_hero2)

    draw.rounded_rectangle((798, 636, 1246, 700), radius=16, fill=(30, 64, 175, 248), outline=(52, 211, 153, 255), width=3)
    _draw_centered_text(draw, (798, 636, 1246, 700), "▶ @min7014_ai 보러가기", f_cta, (255, 255, 255, 255))

    out_png.parent.mkdir(parents=True, exist_ok=True)
    rgba.convert("RGB").save(out_png, quality=95)
    return out_png


def build_upload_kit(dur_1080p: float, dur_short: float) -> dict:
    raw_title_main = "🔥 한 땀 한 땀 만든 916편의 도형들이 말을 걸기 시작했습니다! | @min7014 구독자 500분께 드리는 @min7014_ai 초대장"
    raw_title_short = "🔥 916편 무언 기하 작도의 놀라운 진화! 도형이 말하고 질문합니다 | @min7014_ai 초대 #Shorts #수학"

    raw_desc_main = f"""👇 지금 1클릭으로 새로운 시각 수학 시네마 @min7014_ai 구독하기!
{SUB_URL}

오랜 시간 @min7014 채널에서 한 땀 한 땀 점과 선으로 빚어 온 916편의 기하 작도를 아껴 주신 500분의 구독자 여러분, 진심으로 감사합니다.

말없이 움직이던 도형들이 이제 친절한 단계별 음성 해설, 빛나는 네온 보조선, 그리고 스스로 생각하게 이끄는 '질문하는 수학 수업(4초 발문)'을 만나 [@min7014_ai] 채널로 새롭게 태어났습니다!

🎬 [@min7014_ai 에서 지금 바로 만날 수 있는 대표 시각 증명]
• 새 채널 홈 & 전체 영상 둘러보기: {CHANNEL_URL}/videos
• 피타고라스 나무 1080p 단계별 시각적 증명: https://youtu.be/DSgUHigl82o
• 포물선의 정의와 빛 반사 1080p 시각적 증명: https://youtu.be/hgb_73tr-jQ
• 체바의 정리 1080p 단계별 시각적 증명: https://youtu.be/oq_CJWJ-Zrg
• 45초 핵심 직관 숏폼 (피타고라스 나무 #Shorts): https://youtube.com/shorts/wSOzehSfEbY

📚 [원문 수학자료실 100% 무료 연동]
• 수학자료실 원문 아카이브 (847+ 시각적 증명 PDF · 동적 작도): {ARCHIVE_URL}

⏱️ [챕터 안내]
00:00 한 땀 한 땀 빚어 온 916편의 도형들, 이제 말을 걸기 시작합니다
00:21 [미리보기 ①] 피타고라스 나무 — 128개 가지가 뻗어도 넓이 합은 왜 25일까?
00:42 [미리보기 ②] 타원의 12줄기 빛 반사와 스스로 깨치는 '질문하는 수학 수업'
01:05 500+편 한국어·영어 4대 에디션 시네마 × 수학자료실 원문 100% 직결
01:26 @min7014 500분의 첫 가족을 @min7014_ai로 초대합니다!

※ 본 영상의 모든 기하 작도와 시각적 증명 아이디어는 수학자료실({ARCHIVE_URL})에 축적된 오리지널 연구 저작물에 기반합니다.

#수학 #기하학 #시각적증명 #피타고라스나무 #이차곡선 #질문하는수업 #수학교육 #min7014 #min7014_ai"""

    raw_tags = [
        "수학", "기하학", "시각적증명", "피타고라스정리", "피타고라스나무",
        "타원의정의", "포물선", "체바의정리", "질문하는수학수업", "보조선",
        "수학교육", "동적기하", "min7014", "min7014_ai",
    ]

    gated_main = auditor.sanitize_and_gate_upload_payload(raw_title_main, raw_desc_main, raw_tags)
    gated_short = auditor.sanitize_and_gate_upload_payload(raw_title_short, raw_desc_main, raw_tags + ["Shorts"])

    pinned_comment = f"""🌟 [@min7014 500분의 소중한 구독자 여러분께]
오랜 시간 말없이 움직이던 기하 작도 영상들을 지켜봐 주셔서 정말 감사합니다!
도형이 직접 말을 걸고 질문을 던지는 새 채널 [@min7014_ai]는 아래 링크를 누르시면 1초 만에 구독하실 수 있습니다 👇

✅ @min7014_ai 1클릭 구독 바로가기: {SUB_URL}
🎬 피타고라스 나무 시각 증명 바로 보기: https://youtu.be/DSgUHigl82o

새 채널 구독 후 댓글로 "500명 첫 가족 출석!" 또는 가장 보고 싶은 수학 주제를 남겨 주시면 최우선으로 아름다운 시각 시네마로 제작해 드리겠습니다! 🙏✨"""

    community_post = f"""📢 [@min7014 구독자 500분께 드리는 특별한 초대장]

한 땀 한 땀 점과 선을 이어 만든 916편의 무언 기하 작도들을 기억하시나요?
그 도형들이 이제 친절한 목소리 해설과 빛나는 보조선, 그리고 스스로 깨치는 '질문하는 수학 수업'을 입고 [@min7014_ai] 채널로 새롭게 진화했습니다!

지금까지 500편 이상의 한국어·영어 1080p 시각 증명과 45초 핵심 직관 #Shorts가 준비되어 있습니다.
오랜 시간 이 채널을 지켜 주신 500분의 구독자 여러분이 새 채널의 가장 든든한 첫 가족이 되어 주세요!

👉 @min7014_ai 새 채널 바로가기 & 구독: {SUB_URL}"""

    kit = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "target_source_channel": "https://www.youtube.com/@min7014",
        "target_destination_channel": CHANNEL_URL,
        "subscribe_confirmation_url": SUB_URL,
        "files": {
            "main_1080p_mp4": str(OUT_DIR / "min7014_to_min7014_ai_bridge_1080p.mp4"),
            "companion_shorts_mp4": str(OUT_DIR / "min7014_to_min7014_ai_bridge_shorts.mp4"),
            "thumbnail_1280x720_png": str(OUT_DIR / "min7014_to_min7014_ai_bridge_thumb.png"),
        },
        "durations_sec": {
            "main_1080p": round(dur_1080p, 2),
            "companion_shorts": round(dur_short, 2),
        },
        "main_16x9_upload": gated_main,
        "companion_shorts_upload": gated_short,
        "pinned_comment": pinned_comment,
        "community_tab_post": community_post,
    }

    txt_report = "\n".join([
        "===============================================================================",
        "🌉 [@min7014 (500명) → @min7014_ai 브릿지 초대 영상 업로드 키트]",
        "===============================================================================",
        "",
        "[1] 📁 렌더링 완료 파일 경로",
        f"  • 16:9 본편 영상 (1080p): {kit['files']['main_1080p_mp4']} ({kit['durations_sec']['main_1080p']}초)",
        f"  • 16:9 전용 썸네일 (720p): {kit['files']['thumbnail_1280x720_png']}",
        f"  • 9:16 숏폼 영상 (#Shorts): {kit['files']['companion_shorts_mp4']} ({kit['durations_sec']['companion_shorts']}초)",
        "",
        "-------------------------------------------------------------------------------",
        "[2] 🎬 @min7014 업로드용 [16:9 본편 제목] (그대로 복사)",
        "-------------------------------------------------------------------------------",
        gated_main["title"],
        "",
        "-------------------------------------------------------------------------------",
        "[3] 📝 @min7014 업로드용 [설명란] (첫 줄 1클릭 구독 링크 배치 완료)",
        "-------------------------------------------------------------------------------",
        gated_main["description"],
        "",
        "-------------------------------------------------------------------------------",
        "[4] 📌 업로드 직후 달아둘 [고정댓글] (전환율 극대화 핵심 장치!)",
        "-------------------------------------------------------------------------------",
        pinned_comment,
        "",
        "-------------------------------------------------------------------------------",
        "[5] 📱 @min7014 [9:16 #Shorts 티저 제목] (모바일 휴면 구독자 동시 깨우기용)",
        "-------------------------------------------------------------------------------",
        gated_short["title"],
        "",
        "-------------------------------------------------------------------------------",
        "[6] 📣 @min7014 [게시물(커뮤니티 탭) 공지 문구]",
        "-------------------------------------------------------------------------------",
        community_post,
        "",
    ])

    (OUT_DIR / "upload_kit_for_min7014.json").write_text(
        json.dumps(kit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "upload_kit_for_min7014.txt").write_text(txt_report, encoding="utf-8")
    return kit


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mp4_1080p = OUT_DIR / "min7014_to_min7014_ai_bridge_1080p.mp4"
    mp4_short = OUT_DIR / "min7014_to_min7014_ai_bridge_shorts.mp4"
    thumb_png = OUT_DIR / "min7014_to_min7014_ai_bridge_thumb.png"

    print("[1/4] Rendering 1920x1080 Bridge Special Cinema MP4...")
    dur_1080p = render_1080p_bridge_video(mp4_1080p)
    print(f"  -> Done: {mp4_1080p} ({dur_1080p:.2f}s, {mp4_1080p.stat().st_size / (1024*1024):.2f} MB)")

    print("[2/4] Rendering 1080x1920 Companion Bridge #Shorts MP4...")
    dur_short = render_shorts_bridge_video(mp4_short)
    print(f"  -> Done: {mp4_short} ({dur_short:.2f}s, {mp4_short.stat().st_size / (1024*1024):.2f} MB)")

    print("[3/4] Rendering 1280x720 High-CTR Bridge Thumbnail PNG...")
    render_bridge_thumbnail(thumb_png)
    print(f"  -> Done: {thumb_png} ({thumb_png.stat().st_size / 1024:.1f} KB)")

    print("[4/4] Building Auditor-Gated @min7014 Upload Kit...")
    kit = build_upload_kit(dur_1080p, dur_short)
    print("  -> Title:", kit["main_16x9_upload"]["title"])
    print("ALL BRIDGE ASSETS GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
