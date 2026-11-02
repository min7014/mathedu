# -*- coding: utf-8 -*-
"""
min7014_video_maker.py — 민은기 선생님의 수학자료실(https://min7014.github.io/)
단계별 플립북 PDF 기반 [설명 텍스트 대본 우선 생성 ➔ 전 세계 다국어 나레이션 변환 ➔ 1080p MP4 강의 영상 제작] 파이프라인

사용 예시:
  1) 설명 텍스트 대본(JSON) 생성 및 다국어(ko, en, ja, es, zh-CN, fr, de, vi) 나레이션 번역:
     python -X utf8 min7014_video_maker.py --slug math20250130001 --step script --langs ko,en,ja,es,zh-CN
  2) 생성된 대본을 바탕으로 각 나라 언어의 1080p MP4 강의 영상 렌더링:
     python -X utf8 min7014_video_maker.py --slug math20250130001 --step video --langs ko,en,ja,es
  3) 대표 핵심 자료 일괄 대본 + 다국어 MP4 샘플 생성:
     python -X utf8 min7014_video_maker.py --build-flagship
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path

import edge_tts
import pymupdf
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent
DEEP_JSON_PATH = ROOT_DIR / "assets" / "min7014_deep_knowledge.json"
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
VIDEOS_DIR = ROOT_DIR / "video_lectures" / "videos"
CATALOG_PATH = ROOT_DIR / "video_lectures" / "catalog.json"

SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# 20개국 이상 전 세계 다국어 Neural TTS 음성 매핑
GLOBAL_VOICE_MAP = {
    "ko": {"name": "한국어 (Korean)", "flag": "🇰🇷", "voice": "ko-KR-SunHiNeural", "bcp47": "ko-KR"},
    "en": {"name": "English (영어)", "flag": "🇺🇸", "voice": "en-US-AriaNeural", "bcp47": "en-US"},
    "ja": {"name": "日本語 (일본어)", "flag": "🇯🇵", "voice": "ja-JP-NanamiNeural", "bcp47": "ja-JP"},
    "zh-CN": {"name": "中文 (중국어)", "flag": "🇨🇳", "voice": "zh-CN-XiaoxiaoNeural", "bcp47": "zh-CN"},
    "es": {"name": "Español (스페인어)", "flag": "🇪🇸", "voice": "es-ES-ElviraNeural", "bcp47": "es-ES"},
    "fr": {"name": "Français (프랑스어)", "flag": "🇫🇷", "voice": "fr-FR-DeniseNeural", "bcp47": "fr-FR"},
    "de": {"name": "Deutsch (독일어)", "flag": "🇩🇪", "voice": "de-DE-KatjaNeural", "bcp47": "de-DE"},
    "vi": {"name": "Tiếng Việt (베트남어)", "flag": "🇻🇳", "voice": "vi-VN-HoaiMyNeural", "bcp47": "vi-VN"},
    "pt": {"name": "Português (포르투갈어)", "flag": "🇧🇷", "voice": "pt-BR-FranciscaNeural", "bcp47": "pt-BR"},
    "ru": {"name": "Русский (러시아어)", "flag": "🇷🇺", "voice": "ru-RU-SvetlanaNeural", "bcp47": "ru-RU"},
    "ar": {"name": "العربية (아랍어)", "flag": "🇸🇦", "voice": "ar-SA-ZariyahNeural", "bcp47": "ar-SA"},
    "hi": {"name": "हिन्दी (힌디어)", "flag": "🇮🇳", "voice": "hi-IN-SwaraNeural", "bcp47": "hi-IN"},
    "id": {"name": "Bahasa Indonesia (인도네시아어)", "flag": "🇮🇩", "voice": "id-ID-GadisNeural", "bcp47": "id-ID"},
    "tr": {"name": "Türkçe (튀르키예어)", "flag": "🇹🇷", "voice": "tr-TR-EmelNeural", "bcp47": "tr-TR"},
    "th": {"name": "ภาษาไทย (태국어)", "flag": "🇹🇭", "voice": "th-TH-PremwadeeNeural", "bcp47": "th-TH"},
    "it": {"name": "Italiano (이탈리아어)", "flag": "🇮🇹", "voice": "it-IT-ElsaNeural", "bcp47": "it-IT"},
}

# 대표 핵심 PDF에 대한 페이지별 정밀 한국어 설명 텍스트 대본 (1페이지 ~ 마지막 페이지)
CURATED_PAGE_SCRIPTS = {
    "math20250130001": {
        "title": "피타고라스 나무 (Pythagoras Tree)",
        "pdf_url": "https://min7014.github.io/2025/2025013001.pdf",
        "web_url": "https://min7014.github.io/math20250130001.html",
        "pages": [
            "1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의로, 직각삼각형과 정사각형이 무한히 뻗어 나가는 피타고라스 나무의 기하학적 원리를 알아봅시다.",
            "2페이지입니다. 이제 빈 칠판 위에서 첫 번째 기준 정사각형부터 한 단계씩 작도를 시작합니다.",
            "3페이지입니다. 가장 아래에 기둥이 되는 정사각형을 그리고, 그 윗변을 지름으로 하는 반원 위에 한 점을 잡아 직각삼각형을 올립니다. 원의 지름에 대한 원주각은 항상 90도입니다.",
            "4페이지입니다. 직각삼각형의 나머지 두 변 위에 각각 정사각형을 그립니다. 피타고라스 정리에 의해 새로 생긴 두 정사각형 넓이의 합은 아래 기둥 정사각형의 넓이와 정확히 같습니다.",
            "5페이지입니다. 두 정사각형의 윗변에 다시 닮음인 직각삼각형을 올리고 4개의 새로운 정사각형 가지를 피워냅니다. 이 4개 정사각형의 넓이 합 역시 맨 아래 기둥의 넓이와 같습니다.",
            "6페이지입니다. 4단계로 8개의 정사각형 가지가 뻗어 나갑니다. 단계가 올라가도 각 층의 정사각형 넓이 총합이 일정하게 보존된다는 점이 핵심입니다.",
            "7페이지입니다. 5단계로 16개의 정사각형 가지가 형성됩니다. 직각삼각형의 예각 크기에 따라 나무가 휘어지는 방향과 대칭성이 결정됩니다.",
            "8페이지입니다. 6단계로 32개의 정사각형 잎사귀가 돋아납니다. 작은 부분을 확대해도 전체 모양과 닮아 있는 자기닮음 프랙탈 기하학의 구조가 선명하게 나타납니다.",
            "9페이지입니다. 7단계로 64개의 정사각형이 풍성한 나무 수관을 이룹니다. 단순한 피타고라스 정리의 반복만으로 자연의 나뭇가지와 닮은 형태가 완성됩니다.",
            "10페이지입니다. 8단계까지 완성된 피타고라스 나무의 전체 모습입니다. 직각삼각형과 정사각형의 넓이 보존 법칙이 만들어낸 아름다운 기하학적 조화를 감상해 보세요.",
            "11페이지입니다. 민은기 선생님의 수학자료실 웹페이지에서 직각삼각형의 꼭짓점을 직접 마우스로 움직이며 나무의 모양 변화를 실험해 보세요!"
        ]
    },
    "2014111902": {
        "title": "체바의 정리 (Ceva's Theorem)",
        "pdf_url": "https://min7014.github.io/2020/2014111902.pdf",
        "web_url": "https://min7014.github.io/math20200228001.html",
        "pages": [
            "1페이지입니다. 삼각형의 세 꼭짓점과 내부의 한 점을 지나는 세 직선이 마주 보는 변을 나누는 길이 비의 곱이 1이 된다는 체바의 정리를 단계별로 증명해 봅시다.",
            "2페이지입니다. 빈 화면에서 기본 삼각형 작도부터 차례대로 시작합니다.",
            "3페이지입니다. 평면 위에 기준이 되는 삼각형 A B C를 작도합니다.",
            "4페이지입니다. 삼각형 A B C의 세 변을 포함하는 직선을 점선으로 연장하여 위치 관계를 명확히 합니다.",
            "5페이지입니다. 삼각형 A B C의 내부에 세 직선이 만날 교점 O를 하나 잡습니다.",
            "6페이지입니다. 세 꼭짓점 A, B, C에서 점 O를 지나는 직선을 그어 마주 보는 변 BC, CA, AB와 만나는 점을 각각 D, E, F라 합니다.",
            "7페이지입니다. 꼭짓점 A에서 출발하여 변 AB 위의 교점 F까지의 선분 AF를 붉은 호로 표시하고 첫 번째 분수의 분자에 놓습니다.",
            "8페이지입니다. 이어서 교점 F에서 꼭짓점 B까지의 선분 FB를 보라색 호로 표시하여 첫 번째 선분 길이의 비 FB 분의 AF를 완성합니다.",
            "9페이지입니다. 이제 꼭짓점 B에서 변 BC 위의 교점 D까지의 선분 BD를 파란 호로 표시하여 두 번째 분수의 분자에 적습니다.",
            "10페이지입니다. 교점 D에서 꼭짓점 C까지의 선분 DC를 표시하여 두 번째 길이의 비 DC 분의 BD를 곱합니다.",
            "11페이지입니다. 계속해서 꼭짓점 C에서 변 CA 위의 교점 E까지의 선분 CE를 초록 호로 표시합니다.",
            "12페이지입니다. 마지막으로 교점 E에서 처음 출발점인 꼭짓점 A로 돌아오는 선분 EA를 주황 호로 표시하여 EA 분의 CE를 곱합니다.",
            "13페이지입니다. 삼각형의 둘레를 한 바퀴 돌아온 세 비율, FB 분의 AF 곱하기 DC 분의 BD 곱하기 EA 분의 CE의 값이 항상 1이 된다는 것이 체바의 정리입니다.",
            "14페이지입니다. 왜 이 곱이 1이 될까요? 선분 CO를 공통 밑변으로 보면, 선분 AF 대 FB의 길이 비는 삼각형 AOC와 삼각형 COB의 넓이의 비와 같습니다.",
            "15페이지입니다. 같은 원리로 선분 AO를 공통 밑변으로 보면, 선분 BD 대 DC의 길이 비는 삼각형 BOA와 삼각형 AOC의 넓이의 비와 같습니다.",
            "16페이지입니다. 또한 선분 BO를 공통 밑변으로 보면 선분 CE 대 EA의 비는 삼각형 COB와 삼각형 BOA의 넓이 비와 같습니다. 이제 세 식을 모두 곱하면 분모와 분자의 세 삼각형 넓이가 모두 약분되어 정확히 1이 증명됩니다!",
            "17페이지입니다. 민은기 선생님의 수학자료실에서 교점 O의 위치를 직접 드래그하며 체바의 정리가 항상 성립함을 확인해 보세요!"
        ]
    },
    "2017090101": {
        "title": "피타고라스 정리 (Pythagorean Theorem)",
        "pdf_url": "https://min7014.github.io/2020/2017090101.pdf",
        "web_url": "https://min7014.github.io/math20200113001.html",
        "pages": [
            "1페이지입니다. 직각삼각형에서 빗변의 제곱이 두 직각변의 제곱의 합과 같다는 피타고라스 정리를 정사각형 넓이 분할로 눈으로 보며 증명해 봅시다.",
            "2페이지입니다. 빈 칠판에서 직각삼각형 하나를 그리는 것부터 출발합니다.",
            "3페이지입니다. 기준이 되는 삼각형 A B C를 작도합니다.",
            "4페이지입니다. 꼭짓점 C의 각이 90도인 직각삼각형임을 직각 기호로 표시합니다.",
            "5페이지입니다. 직각을 낀 밑변 BC의 길이를 소문자 a라고 놓습니다.",
            "6페이지입니다. 직각을 낀 높이 CA의 길이를 소문자 b라고 놓습니다.",
            "7페이지입니다. 직각과 마주 보는 가장 긴 변인 빗변 AB의 길이를 소문자 c라고 놓습니다.",
            "8페이지입니다. 이제 높이 CA를 위쪽으로 길이 a만큼 연장하여 점 D를 잡습니다. 그러면 전체 세로 변 CD의 길이는 a 더하기 b가 됩니다.",
            "9페이지입니다. 마찬가지로 밑변 CB를 왼쪽으로 길이 b만큼 연장하여 점 F를 잡습니다. 전체 가로 변 CF의 길이도 a 더하기 b가 됩니다.",
            "10페이지입니다. 한 변의 길이가 a 더하기 b인 큰 정사각형 C D E F를 완성합니다.",
            "11페이지입니다. 위쪽 변 DE 위에 선분 EG의 길이가 a, 선분 GD의 길이가 b가 되도록 점 G를 찍습니다.",
            "12페이지입니다. 왼쪽 변 EF 위에 선분 EH의 길이가 b, 선분 HF의 길이가 a가 되도록 점 H를 찍습니다.",
            "13페이지입니다. 네 점 A, G, H, B를 선분으로 연결하면, 큰 정사각형 가장자리에 4개의 직각삼각형이 만들어지고 가운데에 사각형 AGHB가 나타납니다.",
            "14페이지입니다. 가장자리의 네 직각삼각형은 두 직각변의 길이가 모두 a와 b이고 끼인각이 90도이므로 SAS 합동입니다.",
            "15페이지입니다. 직각삼각형의 두 예각의 합은 90도이므로, 평각 180도에서 두 예각을 빼면 안쪽 사각형 AGHB의 네 내각도 모두 90도 직각이 됩니다.",
            "16페이지입니다. 네 변의 길이가 모두 빗변 c로 같고 네 각이 모두 직각이므로, 가운데 사각형 AGHB는 한 변의 길이가 c인 정사각형입니다.",
            "17페이지입니다. 이제 넓이를 계산해 봅시다. 오른쪽 아래 직각삼각형 ABC 한 개의 넓이는 2분의 1 a b입니다.",
            "18페이지입니다. 합동인 네 직각삼각형의 넓이를 모두 더하면 4 곱하기 2분의 1 a b가 됩니다.",
            "19페이지입니다. 그리고 가운데 기울어진 정사각형 AGHB의 넓이는 한 변 c의 제곱인 c 제곱입니다.",
            "20페이지입니다. 따라서 큰 정사각형 내부 조각들의 넓이 합은 4 곱하기 2분의 1 a b 더하기 c 제곱입니다.",
            "21페이지입니다. 이 넓이 합은 한 변의 길이가 a 더하기 b인 전체 큰 정사각형의 넓이, 즉 괄호 a 더하기 b의 전체 제곱과 같아야 합니다.",
            "22페이지입니다. 양변을 전개하여 정리하면, 좌변은 2ab 더하기 c 제곱이 되고 우변은 a 제곱 더하기 2ab 더하기 b 제곱이 됩니다.",
            "23페이지입니다. 양변에서 똑같이 들어 있는 2ab를 소거하면, 마침내 c 제곱은 a 제곱 더하기 b 제곱이라는 피타고라스 정리가 완벽히 증명됩니다!",
            "24페이지입니다. 민은기 선생님의 수학자료실에서 직접 도형을 움직이며 피타고라스 정리의 시각적 증명을 복습해 보세요!"
        ]
    }
}


def load_deep_knowledge():
    if not DEEP_JSON_PATH.exists():
        return []
    with open(DEEP_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_item_by_slug_or_pdf(slug_or_url):
    items = load_deep_knowledge()
    key = str(slug_or_url).strip()
    for it in items:
        u = (it.get("url") or "").strip()
        p = (it.get("pdf") or "").split("#")[0].strip()
        if key in (u, p) or u.endswith(f"/{key}.html") or p.endswith(f"/{key}.pdf"):
            return it
    return None


def compute_page_diff_bbox(prev_img, curr_img):
    """두 연속 PDF 페이지 이미지 사이의 변화 영역(새로 작도된 보조선이나 수식 위치)을 검출합니다."""
    if prev_img is None or curr_img is None:
        return None
    diff = ImageChops.difference(prev_img.convert("RGB"), curr_img.convert("RGB")).convert("L")
    # 헤더(상단 8%)와 푸터(하단 7%)는 페이지 번호 변화 등이 있으므로 제외
    w, h = diff.size
    crop_box = (int(w * 0.03), int(h * 0.09), int(w * 0.97), int(h * 0.91))
    cropped = diff.crop(crop_box)
    # 임계값 처리
    bw = cropped.point(lambda x: 255 if x > 28 else 0)
    bbox = bw.getbbox()
    if not bbox:
        return None
    x0, y0, x1, y1 = bbox
    return [
        round((x0 + crop_box[0]) / w, 4),
        round((y0 + crop_box[1]) / h, 4),
        round((x1 + crop_box[0]) / w, 4),
        round((y1 + crop_box[1]) / h, 4),
    ]


def auto_generate_page_explanations(doc, item_meta):
    """임의의 min7014.github.io PDF에 대해 페이지별 변화 영역과 수학적 단계를 분석하여 설명 텍스트를 생성합니다."""
    total_pages = len(doc)
    title = (item_meta or {}).get("title") or "수학자료실 시각적 증명"
    clean_title = re.sub(r"\$[^\$]*\$", "", title).strip()
    sub_ko = (item_meta or {}).get("sub_domain_ko") or "기하·대수 시각적 증명"
    core = re.sub(r"\$[^\$]*\$", "핵심 수식", (item_meta or {}).get("core_concept") or "")
    vis = re.sub(r"\$[^\$]*\$", "", (item_meta or {}).get("visual_summary") or "")
    steps = (item_meta or {}).get("scaffolding_steps") or []
    tips = (item_meta or {}).get("solving_tips") or []

    pages_out = []
    prev_pil = None

    for idx in range(total_pages):
        p_num = idx + 1
        pix = doc[idx].get_pixmap(dpi=96)
        curr_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        bbox = compute_page_diff_bbox(prev_pil, curr_pil) if idx > 0 else None
        prev_pil = curr_pil

        # 변화 위치 분석 (왼쪽/중앙 도형 작도 vs 오른쪽 수식 전개)
        focus_desc = "핵심 도형 및 수식 전개"
        if bbox:
            cx = (bbox[0] + bbox[2]) / 2.0
            cy = (bbox[1] + bbox[3]) / 2.0
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area < 0.002:
                focus_desc = "화면 준비 및 미세 보조선 정렬"
            elif cx < 0.48:
                focus_desc = "왼쪽 기하 도형·보조선·점의 작도"
            elif cx > 0.55 and cy < 0.45:
                focus_desc = "오른쪽 상단 핵심 목표 관계식 제시"
            elif cx > 0.55:
                focus_desc = "오른쪽 대수적 비례식·증명 수식 유도"
            else:
                focus_desc = "중앙 도형의 대칭·합동·닮음 관계 표시"

        if p_num == 1:
            step_title = "도입 · 주제 및 목표 소개"
            exp_text = f"1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 이번 주제는 {clean_title}이며, {core}"
        elif p_num == total_pages:
            step_title = "완결 · 실전 적용 및 웹 실습 안내"
            tip_str = re.sub(r"\$[^\$]*\$", "", tips[0]) if tips else "도형의 정의와 대칭 보조선을 기억하세요."
            exp_text = f"마지막 {p_num}페이지입니다. 지금까지 단계별 플립북으로 증명을 완성했습니다. 실전 팁으로, {tip_str}"
        elif p_num == 2 and (not bbox or (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) < 0.01):
            step_title = "기초 칠판 준비"
            exp_text = "2페이지입니다. 빈 칠판 위에서 기본 도형과 기준점을 하나씩 작도하며 증명을 시작하겠습니다."
        else:
            progress = (p_num - 1) / max(1, total_pages - 2)
            if progress <= 0.28:
                phase_name = "1단계 기초 도형·기준점 작도"
                s_hint = re.sub(r"\$[^\$]*\$", "", steps[0]) if len(steps) > 0 else "기본 도형과 꼭짓점을 배치합니다."
                exp_text = f"{p_num}페이지입니다. [{focus_desc}] 단계로, {s_hint}"
            elif progress <= 0.55:
                phase_name = "2단계 보조선 및 기하적 성질 연결"
                s_hint = re.sub(r"\$[^\$]*\$", "", steps[1]) if len(steps) > 1 else vis
                exp_text = f"{p_num}페이지입니다. [{focus_desc}] 단계입니다. 새로 추가된 보조선과 각·선분의 대칭 관계를 관찰합니다. {s_hint}"
            elif progress <= 0.82:
                phase_name = "3단계 비례식·수식 관계 도출"
                s_hint = re.sub(r"\$[^\$]*\$", "", steps[2]) if len(steps) > 2 else "도형의 성질을 수식으로 번역합니다."
                exp_text = f"{p_num}페이지입니다. [{focus_desc}] 과정입니다. 앞에서 찾은 도형의 성질을 등식과 비례식으로 연결합니다. {s_hint}"
            else:
                phase_name = "4단계 수식 결합 및 정리 완성"
                s_hint = re.sub(r"\$[^\$]*\$", "", steps[3]) if len(steps) > 3 else "모든 조각을 결합해 최종 정리를 완성합니다."
                exp_text = f"{p_num}페이지입니다. [{focus_desc}] 마무리 단계입니다. 유도한 식들을 결합하여 최종 정리를 완성합니다. {s_hint}"
            step_title = phase_name

        pages_out.append({
            "page": p_num,
            "step_title": step_title,
            "visual_focus": focus_desc,
            "diff_bbox": bbox,
            "explanation_text": exp_text,
            "narrations": {"ko": exp_text}
        })

    return pages_out


def translate_text_google_gtx(text_ko, target_lang):
    """한국어 설명 텍스트를 전 세계 대상 언어로 자연스럽게 번역합니다."""
    if target_lang == "ko" or not text_ko.strip():
        return text_ko
    try:
        q = urllib.parse.quote(text_ko)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ko&tl={target_lang}&dt=t&q={q}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated = "".join(seg[0] for seg in data[0] if seg and seg[0])
            return translated.strip() or text_ko
    except Exception:
        return text_ko


def generate_or_update_script(slug_key, target_langs=None):
    """
    [1단계: 설명 텍스트 우선 생성]
    지정된 PDF 자료의 페이지별 한국어 설명 텍스트(explanation_text)를 먼저 생성하고,
    이를 바탕으로 요청된 다국어(target_langs) 나레이션 대본을 생성하여 JSON으로 저장합니다.
    """
    if target_langs is None:
        target_langs = ["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"]

    curated = CURATED_PAGE_SCRIPTS.get(slug_key)
    item_meta = find_item_by_slug_or_pdf(slug_key)

    if curated:
        title = curated["title"]
        pdf_url = curated["pdf_url"]
        web_url = curated["web_url"]
        sub_ko = (item_meta or {}).get("sub_domain_ko") or "유클리드 평면기하·작도·원주각 (Euclidean Geometry)"
    elif item_meta:
        title = item_meta.get("title", slug_key)
        pdf_url = (item_meta.get("pdf") or "").split("#")[0]
        web_url = item_meta.get("url") or "https://min7014.github.io/"
        sub_ko = item_meta.get("sub_domain_ko") or "기하·대수 시각적 증명"
    else:
        raise ValueError(f"Topic not found for slug/key: {slug_key}")

    pdf_bytes = urllib.request.urlopen(pdf_url).read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)

    if curated and len(curated["pages"]) == total_pages:
        pages_data = []
        prev_pil = None
        for idx, exp_ko in enumerate(curated["pages"]):
            pix = doc[idx].get_pixmap(dpi=96)
            curr_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            bbox = compute_page_diff_bbox(prev_pil, curr_pil) if idx > 0 else None
            prev_pil = curr_pil
            pages_data.append({
                "page": idx + 1,
                "step_title": "도입 · 주제 소개" if idx == 0 else ("완결 · 웹 탐구 안내" if idx == total_pages - 1 else f"Step {idx} · 시각적 작도 및 증명"),
                "visual_focus": "핵심 단계별 작도 및 수식 유도",
                "diff_bbox": bbox,
                "explanation_text": exp_ko,
                "narrations": {"ko": exp_ko}
            })
    else:
        pages_data = auto_generate_page_explanations(doc, item_meta)

    # 각 페이지의 기본 설명 텍스트(explanation_text)로부터 다국어 나레이션 생성
    for p_obj in pages_data:
        base_ko = p_obj["explanation_text"]
        p_obj["narrations"]["ko"] = base_ko
        for lang in target_langs:
            if lang == "ko":
                continue
            p_obj["narrations"][lang] = translate_text_google_gtx(base_ko, lang)

    script_doc = {
        "slug": slug_key,
        "title": title,
        "sub_domain_ko": sub_ko,
        "pdf_url": pdf_url,
        "web_url": web_url,
        "page_count": total_pages,
        "base_language": "ko",
        "supported_languages": list(GLOBAL_VOICE_MAP.keys()),
        "pages": pages_data
    }

    out_path = SCRIPTS_DIR / f"{slug_key}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(script_doc, f, ensure_ascii=False, indent=2)

    print(f"[Script Generated] {out_path} ({total_pages} pages, langs={target_langs})")
    return script_doc


def get_font_for_lang(lang_code, size, bold=False):
    win_fonts = Path(r"C:\Windows\Fonts")
    candidates = []
    if lang_code == "ja":
        candidates = ["msgothic.ttc", "malgun.ttf", "arial.ttf"]
    elif lang_code.startswith("zh"):
        candidates = ["msyh.ttc", "malgun.ttf", "arial.ttf"]
    elif lang_code == "ko":
        candidates = ["malgunbd.ttf" if bold else "malgun.ttf", "arial.ttf"]
    else:
        candidates = ["malgunbd.ttf" if bold else "malgun.ttf", "seguisb.ttf" if bold else "segoeui.ttf", "arial.ttf"]

    for fname in candidates:
        fpath = win_fonts / fname
        if fpath.exists():
            try:
                return ImageFont.truetype(str(fpath), size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_slide_frame_1080p(pdf_page, page_info, script_doc, lang_code):
    """
    1920x1080 Full HD 강의 영상 프레임을 생성합니다.
    - 상단 바: 민은기 선생님의 수학자료실 · 제목 · 현재 페이지(STEP k / N) · 언어 배지
    - 중앙 캔버스: 고해상도 PDF 슬라이드 + 새로 변화한 작도/수식 영역 골드 하이라이트
    - 하단 자막 바: 해당 국가 언어 나레이션 자막 (+ 외국어일 경우 한국어 원문 설명 병기)
    """
    W, H = 1920, 1080
    canvas = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(canvas)

    # 1. 상단 헤더 바 (높이 76px)
    draw.rectangle([0, 0, W, 76], fill=(19, 28, 49))
    draw.line([0, 76, W, 76], fill=(56, 189, 248), width=2)

    font_header = get_font_for_lang("ko", 26, bold=True)
    font_badge = get_font_for_lang("ko", 22, bold=True)

    title_str = f"📐 민은기 선생님의 수학자료실 · {script_doc.get('title', '')}"
    if len(title_str) > 52:
        title_str = title_str[:52] + "..."
    draw.text((32, 22), title_str, fill=(248, 250, 252), font=font_header)

    p_num = page_info["page"]
    tot_p = script_doc["page_count"]
    lang_meta = GLOBAL_VOICE_MAP.get(lang_code, {"name": lang_code, "flag": "🌐"})
    right_badge = f"STEP {p_num} / {tot_p}   |   {lang_meta['flag']} {lang_meta['name']}"
    draw.rounded_rectangle([W - 470, 16, W - 28, 60], radius=12, fill=(0, 99, 152))
    draw.text((W - 450, 24), right_badge, fill=(255, 255, 255), font=font_badge)

    # 2. 중앙 PDF 페이지 렌더링 영역 (y: 88 ~ 868, 높이 780px)
    pix = pdf_page.get_pixmap(dpi=200)
    pdf_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    max_pw, max_ph = 1760, 764
    scale = min(max_pw / pdf_img.width, max_ph / pdf_img.height)
    new_w, new_h = int(pdf_img.width * scale), int(pdf_img.height * scale)
    pdf_resized = pdf_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    px = (W - new_w) // 2
    py = 88 + (max_ph - new_h) // 2

    # 슬라이드 외곽 프레임 및 부착
    draw.rounded_rectangle([px - 6, py - 6, px + new_w + 6, py + new_h + 6], radius=14, fill=(56, 189, 248))
    canvas.paste(pdf_resized, (px, py))

    # 변화 영역(새로 추가된 도형·수식)에 은은한 골드 포커스 하이라이트 표시
    bbox = page_info.get("diff_bbox")
    if bbox and p_num > 1 and p_num < tot_p:
        bx0 = px + int(bbox[0] * new_w) - 10
        by0 = py + int(bbox[1] * new_h) - 10
        bx1 = px + int(bbox[2] * new_w) + 10
        by1 = py + int(bbox[3] * new_h) + 10
        if (bx1 - bx0) > 24 and (by1 - by0) > 24:
            draw.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(245, 158, 11), width=4)

    # 3. 하단 다국어 자막 바 (y: 866 ~ 1080)
    draw.rectangle([0, 866, W, H], fill=(9, 14, 28))
    draw.line([0, 866, W, 866], fill=(56, 189, 248), width=2)

    narration_text = page_info.get("narrations", {}).get(lang_code) or page_info.get("explanation_text", "")
    ko_ref_text = page_info.get("explanation_text", "")

    # 주요 자막 줄바꿈 및 출력
    is_cjk = lang_code in ("ko", "ja") or lang_code.startswith("zh")
    wrap_width = 54 if is_cjk else 88
    wrapped_lines = textwrap.wrap(narration_text, width=wrap_width)[:3]

    font_sub = get_font_for_lang(lang_code, 28 if is_cjk else 26, bold=True)
    y_cursor = 884
    for line in wrapped_lines:
        draw.text((48, y_cursor), line, fill=(254, 240, 138), font=font_sub)
        y_cursor += 38

    # 외국어 나레이션일 때 하단에 한국어 기준 설명 텍스트를 함께 표시
    if lang_code != "ko" and ko_ref_text:
        font_ko_sub = get_font_for_lang("ko", 20, bold=False)
        ko_one_line = ko_ref_text if len(ko_ref_text) <= 78 else (ko_ref_text[:78] + "...")
        draw.text((48, 1036), f"[한국어 원문 대본] {ko_one_line}", fill=(148, 163, 184), font=font_ko_sub)

    return canvas


async def synthesize_edge_tts_mp3(text, voice_name, out_mp3_path):
    communicate = edge_tts.Communicate(text, voice_name, rate="+4%")
    await communicate.save(str(out_mp3_path))


def render_multilingual_video(slug_key, lang_code="ko", max_pages=None):
    """
    [2단계: 다국어 나레이션 음성 합성 및 1080p MP4 강의 영상 제작]
    저장된 설명 대본 JSON을 읽어 지정된 언어(lang_code)로 각 페이지 음성을 생성하고
    1080p MP4 동영상으로 결합합니다.
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        script_doc = generate_or_update_script(slug_key, target_langs=[lang_code])
    else:
        with open(script_path, "r", encoding="utf-8") as f:
            script_doc = json.load(f)
        # 만약 해당 언어 번역본이 아직 없으면 번역 후 저장
        needs_save = False
        for p_obj in script_doc["pages"]:
            if lang_code not in p_obj.get("narrations", {}):
                p_obj.setdefault("narrations", {})[lang_code] = translate_text_google_gtx(
                    p_obj["explanation_text"], lang_code
                )
                needs_save = True
        if needs_save:
            with open(script_path, "w", encoding="utf-8") as f:
                json.dump(script_doc, f, ensure_ascii=False, indent=2)

    pdf_bytes = urllib.request.urlopen(script_doc["pdf_url"]).read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    lang_meta = GLOBAL_VOICE_MAP.get(lang_code, GLOBAL_VOICE_MAP["en"])
    voice_name = lang_meta["voice"]

    ffmpeg_exe = shutil.which("ffmpeg")
    if not ffmpeg_exe:
        raise RuntimeError("ffmpeg executable not found in PATH")

    pages_to_render = script_doc["pages"]
    if max_pages:
        pages_to_render = pages_to_render[:max_pages]

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_vid_{slug_key}_{lang_code}_"))
    segment_files = []

    try:
        for p_info in pages_to_render:
            p_idx = p_info["page"] - 1
            narration = p_info.get("narrations", {}).get(lang_code) or p_info["explanation_text"]

            slide_img = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code)
            img_path = tmp_dir / f"slide_{p_idx:03d}.png"
            mp3_path = tmp_dir / f"audio_{p_idx:03d}.mp3"
            seg_path = tmp_dir / f"seg_{p_idx:03d}.mp4"

            slide_img.save(img_path)
            asyncio.run(synthesize_edge_tts_mp3(narration, voice_name, mp3_path))

            # 각 페이지 이미지 + 나레이션 음성을 MP4 세그먼트로 인코딩 (음성 종료 후 0.45초 여운 추가)
            cmd = [
                ffmpeg_exe, "-y",
                "-loop", "1", "-i", str(img_path),
                "-i", str(mp3_path),
                "-filter_complex", "[1:a]apad=pad_dur=0.45[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage",
                "-crf", "24", "-pix_fmt", "yuv420p", "-r", "24",
                "-c:a", "aac", "-b:a", "128k",
                "-shortest",
                str(seg_path)
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segment_files.append(seg_path)

        concat_txt = tmp_dir / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as cf:
            for seg in segment_files:
                cf.write(f"file '{seg.as_posix()}'\n")

        out_mp4 = VIDEOS_DIR / f"{slug_key}_{lang_code}.mp4"
        cmd_concat = [
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            "-movflags", "+faststart",
            str(out_mp4)
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[Video Rendered] {out_mp4} ({out_mp4.stat().st_size // 1024} KB)")
        return out_mp4
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def update_video_catalog():
    scripts = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        with open(sp, "r", encoding="utf-8") as f:
            sdoc = json.load(f)
        slug = sdoc["slug"]
        avail_videos = {}
        for vp in VIDEOS_DIR.glob(f"{slug}_*.mp4"):
            lang_part = vp.stem.replace(f"{slug}_", "", 1)
            avail_videos[lang_part] = f"video_lectures/videos/{vp.name}"
        scripts.append({
            "slug": slug,
            "title": sdoc["title"],
            "sub_domain_ko": sdoc.get("sub_domain_ko", ""),
            "pdf_url": sdoc["pdf_url"],
            "web_url": sdoc.get("web_url", ""),
            "page_count": sdoc["page_count"],
            "script_url": f"video_lectures/scripts/{sp.name}",
            "available_langs": list(sdoc["pages"][0].get("narrations", {}).keys()) if sdoc.get("pages") else ["ko"],
            "rendered_videos": avail_videos
        })
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)
    print(f"[Catalog Updated] {CATALOG_PATH} ({len(scripts)} topics)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="min7014.github.io Multilingual Step-by-Step PDF Lecture Video Maker")
    parser.add_argument("--slug", type=str, default="math20250130001", help="Topic slug or PDF ID")
    parser.add_argument("--step", type=str, choices=["script", "video", "both"], default="both")
    parser.add_argument("--langs", type=str, default="ko,en,ja,es,zh-CN,fr,de,vi")
    parser.add_argument("--build-flagship", action="store_true", help="Generate flagship multi-language scripts and sample MP4s")
    args = parser.parse_args()

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]

    if args.build_flagship:
        # 1. 3대 핵심 자료(피타고라스 나무, 체바의 정리, 피타고라스 정리)의 8개국어 페이지별 대본 JSON 우선 생성
        for fl_slug in ["math20250130001", "2014111902", "2017090101"]:
            generate_or_update_script(fl_slug, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
        # 2. 피타고라스 나무(11페이지) 및 체바의 정리(17페이지)의 다국어(한국어, 영어, 일본어, 스페인어) 실제 1080p MP4 강의 영상 렌더링
        for v_lang in ["ko", "en", "ja", "es"]:
            render_multilingual_video("math20250130001", lang_code=v_lang)
        for v_lang in ["ko", "en"]:
            render_multilingual_video("2014111902", lang_code=v_lang)
        update_video_catalog()
    else:
        if args.step in ("script", "both"):
            generate_or_update_script(args.slug, target_langs=langs)
        if args.step in ("video", "both"):
            for l_code in langs:
                render_multilingual_video(args.slug, lang_code=l_code)
        update_video_catalog()
