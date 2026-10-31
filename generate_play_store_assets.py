#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_play_store_assets.py
Generates exact-specification Google Play Console graphic assets for mathedu 3D Math Quest Game:
1. assets/app_icon_192.png (192x192 PNG)
2. assets/play_store/feature_graphic_1024x500.png (1024x500 PNG, 24-bit RGB no alpha as required by Play Console)
3. assets/play_store/phone_screenshot_1_1080x1920.png (1080x1920 PNG, 9:16 Phone Screenshot 1: 3D Boss Raid)
4. assets/play_store/phone_screenshot_2_1080x1920.png (1080x1920 PNG, 9:16 Phone Screenshot 2: Micro-Scaffolding & Scratchpad)
5. assets/play_store/tablet_screenshot_1_1920x1080.png (1920x1080 PNG, 16:9 Tablet Screenshot: Full 3D Sanctuary & Archive)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
PLAY_DIR = ASSETS / "play_store"
PLAY_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size: int, bold: bool = True):
    candidates = [
        r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def build_icon_192():
    src = ASSETS / "app_icon_512.png"
    out = ASSETS / "app_icon_192.png"
    im = Image.open(src).convert("RGBA")
    im192 = im.resize((192, 192), Image.Resampling.LANCZOS)
    im192.save(out, "PNG")
    # Also save 512 icon copy in play_store folder for easy upload
    im.save(PLAY_DIR / "app_icon_512x512.png", "PNG")
    print(f"[OK] {out} (192x192) & {PLAY_DIR / 'app_icon_512x512.png'} (512x512)")


def build_feature_graphic():
    # Google Play Feature Graphic: 1024 x 500, 24-bit RGB PNG (no alpha)
    w, h = 1024, 500
    img = Image.new("RGB", (w, h), (7, 11, 25))
    draw = ImageDraw.Draw(img)

    # Cosmic gradient background
    for y in range(h):
        r = int(7 + (y / h) * 18)
        g = int(11 + (y / h) * 26)
        b = int(25 + (y / h) * 52)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Sacred geometric rings (Dandelin spheres & golden ratio motif)
    draw.ellipse([610, 30, 990, 410], outline=(56, 189, 248), width=3)
    draw.ellipse([650, 70, 950, 370], outline=(245, 158, 11), width=2)
    draw.polygon([(800, 20), (630, 430), (970, 430)], outline=(167, 139, 250), width=3)

    # Paste app icon on right center
    icon_path = ASSETS / "app_icon_512.png"
    if icon_path.exists():
        ic = Image.open(icon_path).convert("RGBA").resize((240, 240), Image.Resampling.LANCZOS)
        img.paste(ic, (680, 120), ic)

    # Typography on left
    f_badge = get_font(20, True)
    f_title = get_font(52, True)
    f_sub = get_font(26, True)
    f_desc = get_font(20, False)

    draw.rounded_rectangle([48, 52, 470, 94], radius=20, fill=(22, 37, 68), outline=(245, 158, 11), width=2)
    draw.text((66, 60), "👑 3D 인터랙티브 수학 RPG & 디딤돌 퀴즈", font=f_badge, fill=(253, 230, 138))

    draw.text((48, 118), "수학의 성전 3D", font=f_title, fill=(255, 255, 255))
    draw.text((48, 188), "초등 직관부터 수능 수학 100점까지!", font=f_sub, fill=(56, 189, 248))

    bullets = [
        "✔ 16,548문항 초등 눈높이 무장벽 디딤돌 사다리",
        "✔ 3,400+ 동적 기하 시각적 증명 & SVG 개념 도형",
        "✔ 3D 보스 레이드 · 아르키메데스의 사색 · 인게임 연습장",
        "✔ 학생·교사 100% 무료 열린 수학 아카이브 (mathedu)",
    ]
    y_pos = 248
    for b_txt in bullets:
        draw.text((52, y_pos), b_txt, font=f_desc, fill=(226, 232, 240))
        y_pos += 40

    out = PLAY_DIR / "feature_graphic_1024x500.png"
    img.save(out, "PNG")
    print(f"[OK] {out} (1024x500 RGB)")


def build_phone_screenshot_1():
    # 1080 x 1920 (9:16) — 3D Boss Raid & Dandelin Sacred Geometry Arena
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), (6, 10, 22))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        draw.line(
            [(0, y), (w, y)],
            fill=(int(6 + (y / h) * 14), int(10 + (y / h) * 20), int(22 + (y / h) * 40)),
        )

    f_top = get_font(34, True)
    f_h1 = get_font(58, True)
    f_sub = get_font(30, False)
    f_card_t = get_font(34, True)
    f_card_b = get_font(26, False)

    # Header promotional banner
    draw.rounded_rectangle([60, 70, 1020, 140], radius=35, fill=(16, 185, 129))
    draw.text((140, 84), "🎮 3D 수학 보스 레이드 & 깊은 사색(Deep Eureka)", font=f_top, fill=(6, 10, 22))

    draw.text((70, 175), "어려운 수능 4점 킬러 문항도", font=f_h1, fill=(255, 255, 255))
    draw.text((70, 250), "3D 보스전과 디딤돌로 정복!", font=f_h1, fill=(253, 230, 138))
    draw.text((70, 335), "시간에 쫓기지 않는 『아르키메데스의 사색 결계』와 『단델린 총공격』", font=f_sub, fill=(148, 163, 184))

    # Game Arena Frame
    draw.rounded_rectangle([55, 410, 1025, 1320], radius=36, fill=(13, 20, 40), outline=(56, 189, 248), width=4)

    # Boss HUD inside arena
    draw.rounded_rectangle([95, 450, 985, 555], radius=20, fill=(25, 18, 48), outline=(244, 63, 94), width=3)
    draw.text((125, 468), "👑 BOSS: 원뿔곡선의 수호자 아폴로니우스 (Lv.4 킬러)", font=f_card_t, fill=(253, 164, 175))
    draw.rounded_rectangle([125, 518, 955, 538], radius=10, fill=(51, 65, 85))
    draw.rounded_rectangle([125, 518, 720, 538], radius=10, fill=(244, 63, 94))

    # 3D Geometry Visual Centerpiece
    hero_path = ASSETS / "stitch_dandelin_hero.png"
    if hero_path.exists():
        hero = Image.open(hero_path).convert("RGB").resize((890, 480), Image.Resampling.LANCZOS)
        img.paste(hero, (95, 580))
    else:
        draw.ellipse([340, 620, 740, 1020], outline=(56, 189, 248), width=5)

    # Contemplation & Skill Bar
    draw.rounded_rectangle([95, 1090, 985, 1280], radius=24, fill=(17, 28, 56), outline=(245, 158, 11), width=3)
    draw.text((130, 1115), "🧘 아르키메데스의 사색 결계 가동 중 (타이머 정지 · DEEP EUREKA x1.5)", font=f_card_b, fill=(253, 230, 138))
    draw.text((130, 1165), "📐 [0단계 기호 번역기] 초점 F와 준선까지의 거리가 같다는 뜻이에요!", font=f_card_b, fill=(125, 211, 252))
    draw.text((130, 1215), "🎨 [데카르트 인게임 수학 연습장] 화면 위에 직접 보조선 작도 가능", font=f_card_b, fill=(167, 243, 208))

    # Bottom Feature Cards
    cards = [
        ("🪜 초등 눈높이 5~8단계 미세 디딤돌", "구구단·칸 세기부터 출발해 수능 본문항까지 스스로 도달하는 레고형 사다리"),
        ("🗺️ 도식화 흐름도 & 인라인 SVG 기하 도형", "모든 문항에 한눈에 보이는 시각적 도형 다이어그램과 논리 흐름도 탑재"),
        ("📚 민은기 선생님의 수학자료실 3,400+ 직결", "GeoGebra 동적 기하 앱렛·개념 증명 PDF·알지오매스 원클릭 탐구"),
    ]
    cy = 1365
    for ct, cb in cards:
        draw.rounded_rectangle([55, cy, 1025, cy + 155], radius=24, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
        draw.text((90, cy + 28), ct, font=f_card_t, fill=(248, 250, 252))
        draw.text((90, cy + 84), cb, font=f_card_b, fill=(148, 163, 184))
        cy += 175

    out = PLAY_DIR / "phone_screenshot_1_1080x1920.png"
    img.save(out, "PNG")
    print(f"[OK] {out} (1080x1920 RGB)")


def build_phone_screenshot_2():
    # 1080 x 1920 (9:16) — Elementary-to-CSAT Micro-Scaffolding & Visual SVG Proof
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), (9, 14, 28))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        draw.line(
            [(0, y), (w, y)],
            fill=(int(9 + (y / h) * 12), int(14 + (y / h) * 24), int(28 + (y / h) * 38)),
        )

    f_top = get_font(34, True)
    f_h1 = get_font(54, True)
    f_step_t = get_font(32, True)
    f_step_b = get_font(25, False)

    draw.rounded_rectangle([60, 70, 1020, 140], radius=35, fill=(56, 189, 248))
    draw.text((135, 84), "🪜 초등학생도 수능 문제를 푸는 무장벽 디딤돌 설계", font=f_top, fill=(6, 10, 22))

    draw.text((70, 175), "막히는 순간 친절하게 열리는", font=f_h1, fill=(255, 255, 255))
    draw.text((70, 248), "단계별 생각 징검다리 & 시각 도형", font=f_h1, fill=(110, 231, 183))

    steps = [
        ("STEP 1 · 초등 기초 직관 출발", "구체적인 작은 숫자를 넣어 규칙을 눈으로 먼저 확인해요.", (16, 185, 129)),
        ("STEP 2 · 기호의 친절한 번역", "낯선 시그마(∑)·로그(log)·미분 기호를 초등 사칙연산 약속으로 번역!", (56, 189, 248)),
        ("STEP 3 · 의도적 시각 도형(SVG) 작도", "수식을 막대 도형·수직선·직각삼각형 그림으로 바꾸어 직관적 이해!", (245, 158, 11)),
        ("STEP 4 · 레고 블록 누적 조립", "앞 단계에서 구한 조각들을 결합해 수능 4점 본문항 정답 도출!", (167, 139, 250)),
        ("FINAL · 도식화 풀이 흐름도 완성", "문제 조건 ➔ 핵심 공식 ➔ 정답 도출까지 한눈에 복습하는 마인드맵!", (244, 63, 94)),
    ]

    sy = 360
    for st_title, st_desc, color in steps:
        draw.rounded_rectangle([65, sy, 1015, sy + 240], radius=28, fill=(17, 25, 48), outline=color, width=4)
        draw.rounded_rectangle([95, sy + 28, 620, sy + 82], radius=16, fill=color)
        draw.text((115, sy + 36), st_title, font=f_step_t, fill=(9, 13, 22))
        draw.text((95, sy + 110), st_desc, font=f_step_b, fill=(226, 232, 240))
        draw.text((95, sy + 165), "✔ 힌트 · 폴리아 3단계 발문 · 오답 시 맞춤 교정 피드백 제공", font=f_step_b, fill=(148, 163, 184))
        sy += 280

    draw.rounded_rectangle([65, 1775, 1015, 1865], radius=22, fill=(30, 41, 59), outline=(253, 230, 138), width=2)
    draw.text((135, 1802), "🌟 오프라인 단독 실행 지원 · 회원가입 없이 100% 즉시 학습", font=f_step_t, fill=(253, 230, 138))

    out = PLAY_DIR / "phone_screenshot_2_1080x1920.png"
    img.save(out, "PNG")
    print(f"[OK] {out} (1080x1920 RGB)")


def build_tablet_screenshot_1():
    # 1920 x 1080 (16:9) — Tablet / Chromebook Full 3D Sanctuary & 16,548 Problem Explorer
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), (7, 11, 24))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        draw.line(
            [(0, y), (w, y)],
            fill=(int(7 + (y / h) * 15), int(11 + (y / h) * 22), int(24 + (y / h) * 42)),
        )

    f_h1 = get_font(56, True)
    f_sub = get_font(30, True)
    f_body = get_font(26, False)

    draw.text((80, 60), "수학의 성전 3D · 태블릿 & 대화면 완벽 지원", font=f_h1, fill=(255, 255, 255))
    draw.text((80, 138), "16,548문항 단계별 디딤돌 퀴즈 × 3,400+ 동적 기하 증명 × 3D 보스 레이드", font=f_sub, fill=(56, 189, 248))

    # Left panel: 3D Arena preview
    draw.rounded_rectangle([80, 210, 1020, 990], radius=32, fill=(14, 22, 45), outline=(56, 189, 248), width=4)
    hero_path = ASSETS / "stitch_dandelin_hero.png"
    if hero_path.exists():
        hero = Image.open(hero_path).convert("RGB").resize((880, 520), Image.Resampling.LANCZOS)
        img.paste(hero, (110, 240))
    draw.text((115, 790), "⚔️ 3D 월드맵 5대 성소 & 보스 배틀 아레나", font=f_sub, fill=(253, 230, 138))
    draw.text((115, 845), "• 성좌 특성 트리 · 유클리드 성물 카드 · 데카르트 인게임 수학 연습장", font=f_body, fill=(226, 232, 240))
    draw.text((115, 895), "• 아르키메데스의 사색 결계로 깊은 수학적 사고와 유레카(DEEP EUREKA) 달성", font=f_body, fill=(167, 243, 208))

    # Right panel: Scaffolding & Teacher tools
    draw.rounded_rectangle([1060, 210, 1840, 990], radius=32, fill=(15, 23, 42), outline=(245, 158, 11), width=4)
    icon_path = ASSETS / "app_icon_512.png"
    if icon_path.exists():
        ic = Image.open(icon_path).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
        img.paste(ic, (1360, 245), ic)

    draw.text((1110, 455), "👩‍🏫 초등부터 수능 100점까지 완벽 연계", font=f_sub, fill=(255, 255, 255))
    r_items = [
        "1. 초등 기초 직관에서 출발하는 5~8단계 디딤돌",
        "2. 전 문항 인라인 SVG 도형 & 도식화 흐름도 해설",
        "3. 민은기 선생님의 수학자료실 3,400+ 직결",
        "4. 교실 수업용 실시간 QR 모드 & 오프라인 패키지",
        "5. 개인정보 수집 0건 · 학생 100% 안전 학습 환경",
    ]
    ry = 525
    for it in r_items:
        draw.text((1110, ry), it, font=f_body, fill=(203, 213, 225))
        ry += 68

    out = PLAY_DIR / "tablet_screenshot_1_1920x1080.png"
    img.save(out, "PNG")
    print(f"[OK] {out} (1920x1080 RGB)")


if __name__ == "__main__":
    build_icon_192()
    build_feature_graphic()
    build_phone_screenshot_1()
    build_phone_screenshot_2()
    build_tablet_screenshot_1()
