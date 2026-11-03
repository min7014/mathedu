# -*- coding: utf-8 -*-
"""
min7014_video_maker.py — 민은기 선생님의 수학자료실(https://min7014.github.io/)
초고품질(Broadcast Master Quality) 단계별 플립북 PDF 강의 영상 제작 & 한국어(KO)·영어(EN) YouTube 저장 파이프라인

초고품질(High-Quality) 설계 기준:
  1. [대본 품질 극대화 (Master-Level Native KO & EN Pedagogical Scripts)]:
     - 각 페이지에서 새로 추가되는 기하 작도(보조선, 원호, 색상 변화, 비례식, 약분 과정)를
       수석 수학 교사의 직관적 발문과 정확한 수학 용어로 서술합니다.
     - 한국어(ko) 원본 대본과 함께, 유튜브 글로벌 저장용 영어(en) 대본 역시 기계 번역투를 배제한
       원어민 수학교육 표준 표현(3Blue1Brown / Khan Academy 스타일)으로 정밀 구성합니다.
  2. [영상 화질 극대화 (300 DPI Lanczos Supersampling + H.264 High Profile CRF 16 @ 30fps)]:
     - PDF 벡터 슬라이드를 300 DPI 초고해상도로 렌더링한 뒤 Lanczos 필터로 1920x1080 캔버스에 합성합니다.
     - 연속 페이지 간 픽셀 및 색상 변화(RGB Color Diff)를 감지하여 새로 등장한 도형·수식 위치에
       [STEP k FOCUS] 스포트라이트 하이라이트 박스와 상단 진행률 바(Progress Bar)를 작도합니다.
     - FFmpeg H.264 High Profile (CRF 16, 30fps, yuv420p, +faststart) 인코딩으로 수식 깨짐이 전혀 없는
       무손실급 화질을 보장합니다.
  3. [음향 및 호흡 품질 극대화 (48kHz / 192kbps Stereo AAC + 인지과학적 여백 설계)]:
     - 슬라이드가 넘어간 직후 0.35초의 시각적 관찰 호흡(Pre-speech delay)을 두고 음성을 시작하며,
       설명이 끝난 뒤 0.65초의 숙고 여운(Post-speech contemplation pause)을 두어 학습 효과를 극대화합니다.
  4. [한국어(KO) & 영어(EN) 버전 YouTube 저장 패키지 완비]:
     - youtube_uploads/<slug>/ 에 초고화질 _ko.mp4, _en.mp4 생성
     - video_lectures/youtube_packages/ 에 1280x720 HD 썸네일(_thumb.png), 밀리초 동기화 자막(.srt),
       유튜브 챕터 타임스탬프(00:00) 메타데이터(_youtube_meta.json) 생성 및 YouTube Data API v3 직접 업로드 지원
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path

import edge_tts
import pymupdf
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

ROOT_DIR = Path(__file__).resolve().parent
DEEP_JSON_PATH = ROOT_DIR / "assets" / "min7014_deep_knowledge.json"
LOOKUP_JSON_PATH = ROOT_DIR / "assets" / "min7014_lookup.json"
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
YT_PKG_DIR = ROOT_DIR / "video_lectures" / "youtube_packages"
YT_UPLOADS_DIR = ROOT_DIR / "youtube_uploads"
CATALOG_PATH = ROOT_DIR / "video_lectures" / "catalog.json"

SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
YT_PKG_DIR.mkdir(parents=True, exist_ok=True)
YT_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

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

# 대표 핵심 PDF에 대한 최고 품질 한국어(pages_ko) 및 원어민 수학교육 영어(pages_en) 페이지별 정밀 대본
CURATED_PAGE_SCRIPTS = {
    "math20250130001": {
        "title": "피타고라스 나무 (Pythagoras Tree)",
        "title_en": "The Pythagoras Tree — Step-by-Step Fractal Geometry & Area Conservation",
        "pdf_url": "https://min7014.github.io/2025/2025013001.pdf",
        "web_url": "https://min7014.github.io/math20250130001.html",
        "pages_ko": [
            "1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 직각삼각형과 정사각형이 무한히 가지를 뻗어 나가는 피타고라스 나무의 기하학적 원리와 넓이 보존 법칙을 한 단계씩 탐구해 봅시다.",
            "2페이지입니다. 이제 빈 칠판 위에서 첫 번째 기준 정사각형과 직각삼각형부터 차례대로 작도를 시작합니다.",
            "3페이지입니다. 가장 아래에 나무의 기둥이 되는 첫 번째 정사각형을 그리고, 그 윗변을 지름으로 하는 반원 위에 한 점을 잡아 직각삼각형을 올립니다. 원의 지름에 대한 원주각은 항상 90도이므로 완벽한 직각삼각형이 만들어집니다.",
            "4페이지입니다. 직각삼각형의 나머지 두 직각변 위에 각각 새로운 정사각형 두 개를 작도합니다. 피타고라스 정리에 의해, 새로 피어난 두 정사각형의 넓이 합은 아래 기둥 정사각형의 넓이와 정확히 일치합니다.",
            "5페이지입니다. 두 정사각형의 윗변에 다시 닮음인 직각삼각형을 올리고, 그 위에 4개의 정사각형 가지를 피워냅니다. 이 4개 정사각형의 넓이를 모두 더해도 여전히 맨 아래 기둥 정사각형 하나의 넓이와 같습니다.",
            "6페이지입니다. 다음 단계로 8개의 정사각형 가지가 뻗어 나갑니다. 가지의 개수는 2의 거듭제곱으로 두 배씩 늘어나지만, 각 층의 정사각형 넓이 총합은 처음 기둥의 넓이로 일정하게 보존됩니다.",
            "7페이지입니다. 16개의 정사각형 가지가 형성됩니다. 오른쪽의 기준 직각삼각형에서 꼭짓점의 위치를 바꾸면 예각의 크기가 달라지면서 나무가 휘어지는 방향과 비대칭 곡선미가 결정됩니다.",
            "8페이지입니다. 32개의 정사각형 잎사귀가 돋아납니다. 작은 나뭇가지 하나를 확대해 보아도 나무 전체의 모양과 똑같이 닮아 있는 자기닮음 프랙탈 기하학의 구조가 선명하게 드러납니다.",
            "9페이지입니다. 64개의 정사각형이 풍성한 나무 수관을 이룹니다. 오직 직각삼각형과 피타고라스 정리라는 단순한 규칙의 반복만으로 자연 속 브로콜리나 나뭇가지와 닮은 생명력 있는 형태가 탄생합니다.",
            "10페이지입니다. 마지막 단계까지 완성된 피타고라스 나무의 전체 모습입니다. 유클리드 기하학의 넓이 보존 법칙과 현대 프랙탈 기하학이 만나는 아름다운 수학적 조화를 감상해 보세요.",
            "11페이지입니다. 민은기 선생님의 수학자료실 웹페이지에서 반원 위의 꼭짓점을 마우스로 직접 드래그하며, 나만의 피타고라스 나무가 바람에 흔들리듯 변화하는 모습을 실험해 보세요!"
        ],
        "pages_en": [
            "Step 1. Welcome to Min's Math Lab. In this step-by-step visual proof lecture, we explore the Pythagoras Tree, where right triangles and squares branch out infinitely while preserving total area.",
            "Step 2. Starting from a clean canvas, let us construct the base square and the generating right triangle one step at a time.",
            "Step 3. First, we draw the trunk square at the bottom, and place a right triangle on its top edge using a semicircle. By Thales' theorem, any angle inscribed in a semicircle is always a ninety-degree right angle.",
            "Step 4. Next, we construct two smaller squares on the two legs of the right triangle. By the Pythagorean Theorem, the sum of the areas of these two new squares is exactly equal to the area of the trunk square below.",
            "Step 5. On top of those two squares, we attach similar right triangles and sprout four new branch squares. Remarkably, the combined area of all four squares in this third level still equals the single trunk square.",
            "Step 6. In the fourth generation, eight squares branch outward. While the number of squares doubles at every level as powers of two, the total area at each level remains strictly invariant.",
            "Step 7. Now sixteen squares form the fifth level of branches. Notice on the right how the acute angle of the generating right triangle controls the tilt and curvature of the entire tree.",
            "Step 8. Thirty-two squares bloom across the sixth level. Zooming into any single branch reveals an exact miniature copy of the whole structure, demonstrating the self-similarity of fractal geometry.",
            "Step 9. Sixty-four squares now create a lush canopy. Through the simple recursive repetition of the Pythagorean Theorem, pure geometry reproduces the organic branching patterns found in nature.",
            "Step 10. Here is the fully grown Pythagoras Tree at the eighth stage. Take a moment to appreciate how classical area conservation and modern fractal geometry unite in visual harmony.",
            "Step 11. Visit Min's Math Lab at min7014.github.io to drag the vertex along the semicircle yourself and watch the Pythagoras Tree transform dynamically in real time!"
        ]
    },
    "2014111902": {
        "title": "체바의 정리 (Ceva's Theorem)",
        "title_en": "Ceva's Theorem — Step-by-Step Visual Proof via Triangle Area Ratios",
        "pdf_url": "https://min7014.github.io/2020/2014111902.pdf",
        "web_url": "https://min7014.github.io/math20200228001.html",
        "pages_ko": [
            "1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 삼각형의 세 꼭짓점과 한 교점을 지나는 세 직선이 마주 보는 변을 나누는 길이 비의 곱이 항상 1이 된다는 체바의 정리를 눈으로 보며 증명해 봅시다.",
            "2페이지입니다. 빈 칠판 위에서 기준 삼각형과 교점을 차례대로 작도하며 증명을 시작합니다.",
            "3페이지입니다. 먼저 평면 위에 기준이 되는 삼각형 A B C를 작도합니다.",
            "4페이지입니다. 삼각형 A B C의 세 변을 포함하는 직선을 점선으로 연장하여 직선들의 위치 관계를 명확히 나타냅니다.",
            "5페이지입니다. 삼각형 A B C의 내부에 세 체바 선이 동시에 만날 교점 O를 하나 잡습니다.",
            "6페이지입니다. 세 꼭짓점 A, B, C에서 각각 교점 O를 지나는 직선을 그어, 마주 보는 변 BC, CA, AB와 만나는 교점을 각각 D, E, F라 표시합니다.",
            "7페이지입니다. 이제 꼭짓점 A에서 출발하여 변 AB 위의 분점 F까지 가는 선분 AF를 붉은색 호로 표시하고, 첫 번째 분수의 분자에 적습니다.",
            "8페이지입니다. 이어서 분점 F에서 꼭짓점 B까지 가는 선분 FB를 보라색 호로 표시하고 분모에 적어, 첫 번째 길이의 비 FB 분의 AF를 완성합니다.",
            "9페이지입니다. 계속해서 꼭짓점 B에서 변 BC 위의 분점 D까지 가는 선분 BD를 파란색 호로 표시하여 두 번째 분수의 분자에 놓습니다.",
            "10페이지입니다. 분점 D에서 꼭짓점 C까지 가는 선분 DC를 표시하여 두 번째 길이의 비 DC 분의 BD를 곱합니다.",
            "11페이지입니다. 이제 꼭짓점 C에서 변 CA 위의 분점 E까지 가는 선분 CE를 초록색 호로 표시하여 세 번째 분수의 분자에 놓습니다.",
            "12페이지입니다. 마지막으로 분점 E에서 처음 출발점인 꼭짓점 A로 돌아오는 선분 EA를 주황색 호로 표시하여 세 번째 비율 EA 분의 CE를 완성합니다.",
            "13페이지입니다. 꼭짓점과 분점을 교대로 징검다리처럼 한 바퀴 돈 세 비율, FB 분의 AF 곱하기 DC 분의 BD 곱하기 EA 분의 CE의 값이 항상 1이 된다는 것이 체바의 정리입니다.",
            "14페이지입니다. 왜 이 세 비율의 곱이 항상 1이 될까요? 선분 CO를 공통 밑변으로 하는 두 삼각형을 살펴보면, 밑변 AF 대 FB의 길이 비는 곧 삼각형 AOC의 넓이 대 삼각형 COB의 넓이 비와 같습니다.",
            "15페이지입니다. 똑같은 원리로 선분 AO를 공통 밑변으로 보면, 밑변 BD 대 DC의 길이 비는 삼각형 BOA의 넓이 대 삼각형 AOC의 넓이 비와 정확히 같습니다.",
            "16페이지입니다. 또한 선분 BO를 공통 밑변으로 보면, 선분 CE 대 EA의 길이 비는 삼각형 COB의 넓이 대 삼각형 BOA의 넓이 비와 같습니다. 이제 우변의 세 넓이 분수를 모두 곱하면 분모와 분자의 삼각형 AOC, COB, BOA 넓이가 완벽히 약분되어 1이 증명됩니다!",
            "17페이지입니다. 민은기 선생님의 수학자료실 웹페이지에서 교점 O의 위치를 삼각형 안팎으로 직접 움직여 보며 체바의 정리가 언제나 성립함을 확인해 보세요!"
        ],
        "pages_en": [
            "Step 1. Welcome to Min's Math Lab. In this step-by-step visual proof, we will prove Ceva's Theorem, showing why three concurrent lines from the vertices of a triangle divide the opposite sides into ratios whose product is always 1.",
            "Step 2. Starting on a clean board, we will construct our reference triangle and its interior intersection point step by step.",
            "Step 3. First, we construct a general reference triangle A B C on the plane.",
            "Step 4. We extend the three sides of triangle A B C with dashed lines to clearly visualize the lines containing each side.",
            "Step 5. Inside triangle A B C, we choose a point O where our three Cevians will intersect.",
            "Step 6. Drawing straight lines from vertices A, B, and C through point O, we label their intersections with the opposite sides BC, CA, and AB as points D, E, and F respectively.",
            "Step 7. Now let us trace around the perimeter. Starting at vertex A and moving to point F on side AB, we highlight segment AF with a red arc and place AF in the numerator of our first ratio.",
            "Step 8. Continuing from point F to vertex B, we highlight segment FB in purple and place it in the denominator, forming the first ratio AF over FB.",
            "Step 9. Next, from vertex B to point D on side BC, we mark segment BD with a blue arc as the numerator of our second ratio.",
            "Step 10. From point D to vertex C, we mark segment DC in the denominator, multiplying by the second ratio BD over DC.",
            "Step 11. Continuing around the triangle from vertex C to point E on side CA, we highlight segment CE in green as the third numerator.",
            "Step 12. Finally, returning from point E back to our starting vertex A, we highlight segment EA in orange to complete the third ratio CE over EA.",
            "Step 13. Ceva's Theorem states that as we alternate vertex-to-point-to-vertex all the way around the triangle, the product AF over FB, times BD over DC, times CE over EA, is always equal to 1.",
            "Step 14. Why does this product always equal 1? Looking at line CO as a shared base line, the segment ratio AF over FB equals the area of triangle AOC divided by the area of triangle COB.",
            "Step 15. By the exact same altitude principle along line AO, the ratio BD over DC equals the area of triangle BOA divided by the area of triangle AOC.",
            "Step 16. Likewise, along line BO, the ratio CE over EA equals the area of triangle COB divided by the area of triangle BOA. Multiplying all three area fractions together, every triangle area cancels in numerator and denominator, leaving exactly 1!",
            "Step 17. Visit min7014.github.io to drag the intersection point O interactively and verify that Ceva's Theorem holds for every configuration!"
        ]
    },
    "2017090101": {
        "title": "피타고라스 정리 (Pythagorean Theorem)",
        "title_en": "The Pythagorean Theorem — Step-by-Step Visual Proof by Square Area Partition",
        "pdf_url": "https://min7014.github.io/2020/2017090101.pdf",
        "web_url": "https://min7014.github.io/math20200113001.html",
        "pages_ko": [
            "1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 직각삼각형에서 빗변의 제곱이 두 직각변의 제곱의 합과 같다는 피타고라스 정리를 정사각형 넓이 분할로 한 단계씩 명확하게 증명해 봅시다.",
            "2페이지입니다. 빈 칠판 위에서 기준이 되는 직각삼각형 하나를 작도하는 것부터 시작합니다.",
            "3페이지입니다. 평면 위에 기준 삼각형 A B C를 그립니다.",
            "4페이지입니다. 꼭짓점 C의 내각이 90도인 직각삼각형임을 직각 기호로 명확히 표시합니다.",
            "5페이지입니다. 직각을 낀 가로 밑변 BC의 길이를 소문자 a라고 놓습니다.",
            "6페이지입니다. 직각을 낀 세로 높이 CA의 길이를 소문자 b라고 놓습니다.",
            "7페이지입니다. 직각과 마주 보는 가장 긴 변인 빗변 AB의 길이를 소문자 c라고 놓습니다.",
            "8페이지입니다. 이제 세로 변 CA를 위쪽으로 밑변 길이 a만큼 연장하여 끝점을 D라고 잡습니다. 그러면 전체 세로 변 CD의 길이는 a 더하기 b가 됩니다.",
            "9페이지입니다. 마찬가지로 가로 밑변 CB를 왼쪽으로 높이 길이 b만큼 연장하여 끝점을 F라고 잡습니다. 그러면 전체 가로 변 CF의 길이도 a 더하기 b가 됩니다.",
            "10페이지입니다. 한 변의 길이가 a 더하기 b이고 네 모서리가 모두 직각인 큰 정사각형 C D E F를 완성합니다.",
            "11페이지입니다. 큰 정사각형의 위쪽 변 DE 위에, 선분 EG의 길이가 a이고 선분 GD의 길이가 b가 되도록 분할점 G를 잡습니다.",
            "12페이지입니다. 왼쪽 변 EF 위에도 선분 EH의 길이가 b이고 선분 HF의 길이가 a가 되도록 분할점 H를 잡습니다.",
            "13페이지입니다. 이제 네 변 위의 분할점 A, G, H, B를 선분으로 차례대로 연결하면, 바깥쪽 모서리에 4개의 직각삼각형이 만들어지고 한가운데에 사각형 AGHB가 나타납니다.",
            "14페이지입니다. 모서리에 놓인 4개의 직각삼각형은 모두 두 직각변의 길이가 a와 b이고 끼인각이 90도이므로 SAS 합동입니다. 따라서 네 삼각형의 빗변 길이는 모두 c로 같습니다.",
            "15페이지입니다. 직각삼각형에서 두 예각의 합은 90도이므로, 일직선 평각 180도에서 양쪽 두 예각의 합 90도를 빼면 가운데 사각형 AGHB의 네 내각도 모두 정확히 90도 직각이 됩니다.",
            "16페이지입니다. 네 변의 길이가 모두 c로 같고 네 내각이 모두 90도 직각이므로, 가운데 기울어진 사각형 AGHB는 한 변의 길이가 c인 완벽한 정사각형입니다.",
            "17페이지입니다. 이제 넓이를 비교해 봅시다. 오른쪽 아래 직각삼각형 ABC 한 개의 넓이는 밑변 a 곱하기 높이 b 나누기 2, 즉 2분의 1 a b입니다.",
            "18페이지입니다. 합동인 4개의 직각삼각형 넓이를 모두 더하면 4 곱하기 2분의 1 a b가 됩니다.",
            "19페이지입니다. 여기에 한가운데 놓인 기울어진 정사각형 AGHB의 넓이 c 제곱을 붉은색으로 표시합니다.",
            "20페이지입니다. 네 직각삼각형의 넓이 4 곱하기 2분의 1 a b와 가운데 정사각형의 넓이 c 제곱을 더하는 식을 세웁니다.",
            "21페이지입니다. 이 내부 다섯 조각의 넓이 총합이 바깥쪽 전체 큰 정사각형의 넓이와 같다는 등호를 연결합니다.",
            "22페이지입니다. 한 변의 길이가 a 더하기 b인 전체 큰 정사각형의 넓이, 즉 괄호 a 더하기 b의 전체 제곱을 우변에 적어 넓이 등식을 완성합니다.",
            "23페이지입니다. 등식의 좌변과 우변을 각각 전개하여 정리하면, 좌변은 2ab 더하기 c 제곱이 되고 우변은 a 제곱 더하기 2ab 더하기 b 제곱이 됩니다.",
            "24페이지입니다. 이제 양변에 똑같이 들어 있는 네 직각삼각형의 넓이 2ab를 동시에 소거하면, 마침내 c 제곱은 a 제곱 더하기 b 제곱이라는 피타고라스 정리가 완성됩니다!",
            "25페이지입니다. 민은기 선생님의 수학자료실 웹페이지에 접속하여 직각삼각형의 변의 길이를 직접 조절하며 피타고라스 정리의 시각적 증명을 실험해 보세요!"
        ],
        "pages_en": [
            "Step 1. Welcome to Min's Math Lab. In this step-by-step visual lecture, we prove the Pythagorean Theorem, c squared equals a squared plus b squared, by partitioning the area of a square.",
            "Step 2. Starting on a blank board, we begin by constructing a single right triangle.",
            "Step 3. First, we draw our reference triangle A B C.",
            "Step 4. We mark the interior angle at vertex C as a ninety-degree right angle.",
            "Step 5. Let us label the horizontal base leg BC as length a.",
            "Step 6. Next, we label the vertical height leg CA as length b.",
            "Step 7. And we label the hypotenuse AB, opposite the right angle, as length c.",
            "Step 8. Now we extend the vertical side CA upward by length a to point D, so the total vertical length CD becomes a plus b.",
            "Step 9. Similarly, we extend the horizontal base CB to the left by length b to point F, making the total horizontal length CF also equal to a plus b.",
            "Step 10. We now complete the large outer square C D E F of side length a plus b, marking the right angles at its corners.",
            "Step 11. On the top side DE, we mark point G so that segment EG has length a and segment GD has length b.",
            "Step 12. On the left side EF, we mark point H so that segment EH has length b and segment HF has length a.",
            "Step 13. Connecting points A, G, H, and B with straight segments partitions the large square into four corner right triangles surrounding an inner quadrilateral AGHB.",
            "Step 14. All four corner right triangles share legs of lengths a and b with an included ninety-degree angle, so they are congruent by Side-Angle-Side congruence.",
            "Step 15. Because the two acute angles of each right triangle sum to ninety degrees, subtracting them from a straight 180-degree angle proves that every interior angle of quadrilateral AGHB is ninety degrees.",
            "Step 16. With all four sides equal to hypotenuse c and all four angles equal to ninety degrees, the inner figure AGHB is a true square of side length c.",
            "Step 17. Now let us calculate the area. The area of the bottom-right right triangle ABC is one-half a b.",
            "Step 18. Since all four corner right triangles are congruent, their combined area is 4 times one-half a b.",
            "Step 19. Meanwhile, we mark the area of the inner tilted square AGHB of side length c in red as c squared.",
            "Step 20. Adding the four corner triangles and the central square gives the sum of the pieces: 4 times one-half a b, plus c squared.",
            "Step 21. Next, we set this sum of the five interior pieces equal to the area of the entire outer square.",
            "Step 22. Since the outer square CDEF has side length a plus b, its total area on the right-hand side is the quantity a plus b squared.",
            "Step 23. Simplifying the left side gives 2 a b plus c squared, while expanding the right side yields a squared plus 2 a b plus b squared.",
            "Step 24. Subtracting the common area 2 a b from both sides leaves c squared equals a squared plus b squared, completing our visual proof of the Pythagorean Theorem!",
            "Step 25. Visit min7014.github.io to interactively resize the right triangle and explore this visual proof yourself!"
        ]
    },
    "2014111901": {
        "title": "메넬라우스의 정리 (Menelaus' Theorem)",
        "title_en": "Menelaus' Theorem — Step-by-Step Visual Proof with Parallel Auxiliary Line",
        "pdf_url": "https://min7014.github.io/2020/2014111901.pdf",
        "web_url": "https://min7014.github.io/math20200225001.html",
        "pages_ko": [
            "1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 삼각형의 세 변 또는 그 연장선과 만나는 한 직선이 만드는 길이 비의 곱이 항상 1이 된다는 메넬라우스의 정리를 단계별로 증명해 봅시다.",
            "2페이지입니다. 빈 칠판 위에서 기준 삼각형과 할선을 차례대로 작도하며 시작합니다.",
            "3페이지입니다. 먼저 평면 위에 기준이 되는 삼각형 A B C를 작도합니다.",
            "4페이지입니다. 삼각형 A B C의 세 변을 포함하는 직선을 점선으로 길게 연장합니다.",
            "5페이지입니다. 삼각형의 두 변과 나머지 한 변의 연장선을 동시에 가로지르는 보라색 직선 하나를 긋습니다.",
            "6페이지입니다. 이 직선이 변 AB와 만나는 점을 R, 변 AC와 만나는 점을 Q, 변 BC의 연장선과 만나는 점을 P라고 표시합니다.",
            "7페이지입니다. 이제 꼭짓점 A에서 분점 R까지의 선분 AR을 붉은색 호로 표시하여 첫 번째 분수의 분자에 놓습니다.",
            "8페이지입니다. 분점 R에서 꼭짓점 B까지의 선분 RB를 보라색 호로 표시하여 첫 번째 비율 RB 분의 AR을 완성합니다.",
            "9페이지입니다. 이어서 꼭짓점 B에서 바깥쪽 연장선 위의 교점 P까지 가는 긴 선분 BP를 파란색 호로 표시하여 두 번째 분자에 적습니다.",
            "10페이지입니다. 바깥 교점 P에서 다시 꼭짓점 C로 돌아오는 선분 PC를 표시하여 두 번째 비율 PC 분의 BP를 곱합니다.",
            "11페이지입니다. 계속해서 꼭짓점 C에서 분점 Q까지의 선분 CQ를 초록색 호로 표시하여 세 번째 분자에 놓습니다.",
            "12페이지입니다. 마지막으로 분점 Q에서 출발점인 꼭짓점 A로 돌아오는 선분 QA를 주황색 호로 표시하여 QA 분의 CQ를 곱합니다.",
            "13페이지입니다. 꼭짓점과 교점을 교대로 거쳐 삼각형을 한 바퀴 돌아온 세 비율, RB 분의 AR 곱하기 PC 분의 BP 곱하기 QA 분의 CQ의 곱은 항상 1이 됩니다.",
            "14페이지입니다. 이를 증명하기 위해 핵심 보조선 하나를 긋습니다! 꼭짓점 C를 지나면서 할선 RP와 평행한 직선을 그어 변 AB와 만나는 교점을 D라고 놓습니다.",
            "15페이지입니다. 삼각형 BPR에서 선분 DC와 직선 RP가 평행하므로, 평행선 사이의 선분 길이의 비에 의해 PC 분의 BP는 DR 분의 RB와 같습니다.",
            "16페이지입니다. 따라서 양변에 역수를 곱하면 PC 분의 BP 곱하기 RB 분의 DR은 1이 됩니다.",
            "17페이지입니다. 이번에는 삼각형 ARQ를 봅니다. 선분 DC와 선분 RQ가 평행하므로, 역시 평행선과 선분의 길이 비에 의해 QA 분의 CQ는 AR 분의 RD와 같습니다.",
            "18페이지입니다. 이를 정리하면 QA 분의 CQ 곱하기 RD 분의 AR도 1이 됩니다.",
            "19페이지입니다. 이제 원래의 메넬라우스 식에 PC 분의 BP 대신 DR 분의 RB를, QA 분의 CQ 대신 AR 분의 RD를 대입하면, 분모와 분자의 AR, RB, DR이 모두 깨끗하게 약분되어 1이 증명됩니다!",
            "20페이지입니다. 민은기 선생님의 수학자료실 웹페이지에서 할선의 기울기와 위치를 직접 움직이며 메넬라우스의 정리를 탐구해 보세요!"
        ],
        "pages_en": [
            "Step 1. Welcome to Min's Math Lab. In this step-by-step visual lecture, we will prove Menelaus' Theorem, showing how any transversal line cutting across a triangle creates three directed segment ratios whose product equals 1.",
            "Step 2. Starting from a blank canvas, let us construct triangle A B C and the transversal line step by step.",
            "Step 3. First, we draw a reference triangle A B C on the plane.",
            "Step 4. We extend all three sides of triangle A B C with dashed lines so that external intersections can be seen clearly.",
            "Step 5. Now we draw a purple transversal line that cuts across two sides of the triangle and the extension of the third side.",
            "Step 6. We label the intersection points: point R on side AB, point Q on side AC, and point P on the extension of side BC.",
            "Step 7. Let us trace the loop around the triangle. From vertex A to point R, we mark segment AR with a red arc as the first numerator.",
            "Step 8. From point R to vertex B, we mark segment RB in purple, completing the first ratio AR over RB.",
            "Step 9. Next, from vertex B all the way out to the external point P, we mark segment BP with a blue arc as the second numerator.",
            "Step 10. Returning from external point P to vertex C, we mark segment PC in the denominator, forming the second ratio BP over PC.",
            "Step 11. Continuing from vertex C to point Q on side AC, we highlight segment CQ in green as the third numerator.",
            "Step 12. Finally, from point Q back to the starting vertex A, we highlight segment QA in orange to complete the ratio CQ over QA.",
            "Step 13. Menelaus' Theorem states that around the cycle A to R to B to P to C to Q to A, the product AR over RB, times BP over PC, times CQ over QA, is always equal to 1.",
            "Step 14. How do we prove this? Here is the key auxiliary line: through vertex C, draw a line parallel to the transversal RP, intersecting side AB at point D!",
            "Step 15. In triangle BPR, because line DC is parallel to line RP, parallel line similarity tells us that BP over PC equals RB over DR.",
            "Step 16. Rearranging this first similarity equation shows that BP over PC times DR over RB equals 1.",
            "Step 17. Next, look at triangle ARQ. Since segment DC is parallel to segment RQ, similarity again gives CQ over QA equals RD over AR.",
            "Step 18. Rearranging this second relation shows that CQ over QA times AR over RD also equals 1.",
            "Step 19. Substituting RB over DR for BP over PC, and RD over AR for CQ over QA, every segment AR, RB, and RD cancels out in numerator and denominator, proving the product is 1!",
            "Step 20. Visit min7014.github.io to move the transversal line interactively and see Menelaus' Theorem in action!"
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


def compute_page_diff_and_color(prev_img, curr_img):
    """두 연속 PDF 페이지 사이의 변화 영역(bbox)과 새로 추가된 요소의 주요 색상(붉은 보조선, 파란 각도, 초록 영역 등)을 정밀 분석합니다."""
    if prev_img is None or curr_img is None:
        return None, "default"
    rgb_prev = prev_img.convert("RGB")
    rgb_curr = curr_img.convert("RGB")
    diff_rgb = ImageChops.difference(rgb_prev, rgb_curr)
    diff_l = diff_rgb.convert("L")

    w, h = diff_l.size
    crop_box = (int(w * 0.03), int(h * 0.09), int(w * 0.97), int(h * 0.91))
    cropped_l = diff_l.crop(crop_box)
    bw = cropped_l.point(lambda x: 255 if x > 28 else 0)
    bbox = bw.getbbox()
    if not bbox:
        return None, "default"

    x0, y0, x1, y1 = bbox
    abs_box = (x0 + crop_box[0], y0 + crop_box[1], x1 + crop_box[0], y1 + crop_box[1])

    # 새로 추가된 영역의 평균 RGB 색상 분석
    region_curr = rgb_curr.crop(abs_box)
    mask_region = bw.crop(bbox)
    stat = ImageStat.Stat(region_curr, mask_region)
    color_tag = "default"
    if stat.count and stat.count[0] > 0:
        r_m, g_m, b_m = stat.mean[:3]
        if r_m > g_m + 35 and r_m > b_m + 35:
            color_tag = "red"
        elif b_m > r_m + 30 and b_m > g_m + 20:
            color_tag = "blue"
        elif g_m > r_m + 25 and g_m > b_m + 25:
            color_tag = "green"
        elif r_m > 120 and b_m > 120 and g_m < 100:
            color_tag = "purple"

    norm_bbox = [
        round(abs_box[0] / w, 4),
        round(abs_box[1] / h, 4),
        round(abs_box[2] / w, 4),
        round(abs_box[3] / h, 4),
    ]
    return norm_bbox, color_tag


def clean_math_for_speech_ko(text):
    s = str(text or "")
    s = re.sub(r"\\(?:displaystyle|mathrm|mathbf|left|right)", "", s)
    s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"\2 분의 \1", s)
    s = re.sub(r"\\overline\s*\{([^{}]+)\}", r"선분 \1", s)
    s = re.sub(r"\\triangle\s*([A-Za-z0-9]+)", r"삼각형 \1", s)
    s = re.sub(r"\\angle\s*([A-Za-z0-9]+)", r"각 \1", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"루트 \1", s)
    s = re.sub(r"\^2", " 제곱", s)
    s = re.sub(r"[\$\\\{\}]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def clean_math_for_speech_en(text):
    s = str(text or "")
    s = re.sub(r"\\(?:displaystyle|mathrm|mathbf|left|right)", "", s)
    s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"\1 over \2", s)
    s = re.sub(r"\\overline\s*\{([^{}]+)\}", r"segment \1", s)
    s = re.sub(r"\\triangle\s*([A-Za-z0-9]+)", r"triangle \1", s)
    s = re.sub(r"\\angle\s*([A-Za-z0-9]+)", r"angle \1", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"square root of \1", s)
    s = re.sub(r"\^2", " squared", s)
    s = re.sub(r"[\$\\\{\}]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_baze_api_key():
    """환경변수 BAZE_API_KEY 또는 로컬 .baze_api_key 파일에서 BAZE AI Gateway 키를 로드합니다."""
    env_k = os.environ.get("BAZE_API_KEY", "").strip()
    if env_k:
        return env_k
    key_file = ROOT_DIR / ".baze_api_key"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    return ""


def compute_pedagogical_scene_ranges(total_pages, max_scenes=12):
    """
    [스마트 플립북 모션 그룹핑 엔진 (v2.0)]
    - 16페이지 이하의 단계별 증명 PDF는 1페이지 = 1장면으로 구성합니다.
    - 17페이지 이상의 다중 프레임 플립북 애니메이션 PDF(예: 123페이지 타원 빛 반사, 97페이지 포물선 빛 반사, 46페이지 할선 수렴)는
      전체 프레임을 max_scenes(기본 12개)의 핵심 교육 장면(Scene)으로 분할하여,
      각 장면 내레이션 동안 연속된 PDF 프레임들이 부드러운 3Blue1Brown 스타일 모션 애니메이션으로 재생되도록 합니다.
    """
    if total_pages <= 16:
        return [(i, i) for i in range(total_pages)]
    scenes = [(0, 0)]
    mid_pages = list(range(1, total_pages - 1))
    mid_slots = max_scenes - 2
    n_mid = len(mid_pages)
    for s_idx in range(mid_slots):
        start_i = int(round(s_idx * n_mid / mid_slots))
        end_i = int(round((s_idx + 1) * n_mid / mid_slots)) - 1
        end_i = max(start_i, min(n_mid - 1, end_i))
        scenes.append((mid_pages[start_i], mid_pages[end_i]))
    scenes.append((total_pages - 1, total_pages - 1))
    return scenes


def call_baze_vision_for_pdf_script(doc, item_meta, scene_ranges=None):
    """
    [BAZE AI Gateway (claude-sonnet-4-6 Vision) 기반 초고품질 시각 대본 & 유튜브 인기 후킹 생성기 (v2.0 Keyframe Sampler)]
    - 100페이지가 넘는 플립북 PDF도 최대 16개의 핵심 장면 대표 프레임(1520x1040 px 이내)으로 샘플링하여
      Claude 8000px 이미지 제한(HTTP 400) 없이 100% 비전 판독에 성공합니다.
    """
    import base64
    import io
    import math

    api_key = load_baze_api_key()
    if not api_key:
        return None

    total_pages = len(doc)
    if scene_ranges is None:
        scene_ranges = compute_pedagogical_scene_ranges(total_pages, max_scenes=12)
    num_scenes = len(scene_ranges)

    cols = 3 if num_scenes <= 12 else 4
    rows = math.ceil(num_scenes / cols)
    cell_w, cell_h = 380, 250
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (15, 23, 42))
    draw = ImageDraw.Draw(sheet)
    lbl_font = get_font_for_lang("en", 17, bold=True)

    for s_idx, (p_start, p_end) in enumerate(scene_ranges):
        r, c = divmod(s_idx, cols)
        rep_idx = (p_start + p_end) // 2
        pix = doc[rep_idx].get_pixmap(dpi=72)
        pil_p = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pil_p = pil_p.resize((cell_w - 12, cell_h - 32), Image.Resampling.LANCZOS)
        ox = c * cell_w + 6
        oy = r * cell_h + 26
        lbl = f"[Scene {s_idx + 1}/{num_scenes} · p.{p_start + 1}]" if p_start == p_end else f"[Scene {s_idx + 1}/{num_scenes} · Motion p.{p_start + 1}-{p_end + 1}]"
        draw.text((ox + 4, r * cell_h + 4), lbl, fill=(56, 189, 248), font=lbl_font)
        sheet.paste(pil_p, (ox, oy))

    buf = io.BytesIO()
    sheet.save(buf, format="JPEG", quality=82)
    b64_img = base64.b64encode(buf.getvalue()).decode("ascii")

    raw_title = (item_meta or {}).get("title") or "수학자료실 시각적 증명"
    core_concept = (item_meta or {}).get("core_concept") or ""

    prompt = (
        f"당신은 3Blue1Brown 스타일의 수석 수학 유튜버이자 민은기 선생님의 수학자료실(@min7014_ai) 총괄 디렉터입니다.\n"
        f"첨부된 스토리보드 이미지는 '{raw_title}' (총 {total_pages}프레임 플립북 PDF)를 {num_scenes}개의 핵심 장면(Scene 1 ~ Scene {num_scenes})으로 정리한 화면입니다.\n"
        f"참고 개념: {core_concept}\n\n"
        f"각 장면 슬라이드에 실제로 그려진 도형, 점/직선/원/타원/포물선/다각형의 이름, 색깔(빨강·파랑·초록·보라 등), 동적 움직임과 수식 변화를 정밀하게 관찰하여 아래 JSON 형식으로만 응답하세요(마크다운 코드블록 없이 순수 JSON만 출력):\n"
        f"{{\n"
        f'  "title_en": "자연스러운 영어 수학 주제명",\n'
        f'  "viral_title_ko": "유튜브 클릭률(CTR)을 극대화하는 한국어 제목 (이모지 포함, 85자 이내, 끝에 | @min7014_ai 포함)",\n'
        f'  "viral_title_en": "High-CTR English YouTube title (3Blue1Brown style, <= 85 chars, ending with | @min7014_ai)",\n'
        f'  "hook_ko": "유튜브 설명란 첫 2줄에 들어갈 강렬한 호기심 유발 질문과 핵심 통찰 (한국어 2문장)",\n'
        f'  "hook_en": "2-sentence curiosity-driven hook for the top of the English YouTube description",\n'
        f'  "quiz_ko": "💬 [오늘의 10초 유레카 퀴즈] 시청자가 댓글로 몇 번째 단계인지 답하고 싶게 만드는 구체적 질문 1문장",\n'
        f'  "quiz_en": "💬 [10-Second Eureka Quiz] Engaging question asking viewers to comment which step gave them the Eureka insight",\n'
        f'  "pages_ko": ["1단계입니다. ...", "2단계입니다. ...", "... 정확히 {num_scenes}개 문장 (수식 기호 없이 귀로 듣기만 해도 도형과 움직임이 그려지도록 생생하고 친절하게 서술)"],\n'
        f'  "pages_en": ["Step 1. ...", "Step 2. ...", "... exactly {num_scenes} native English sentences matching each scene"]\n'
        f"}}"
    )

    try:
        payload = {
            "model": "claude-sonnet-4-6",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.3,
        }
        req = urllib.request.Request(
            "https://api.baze.co/v1/gateway/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
            },
        )
        raw_resp = urllib.request.urlopen(req, timeout=22).read().decode("utf-8")
        resp_obj = json.loads(raw_resp)
        content = resp_obj["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
        parsed = json.loads(content)
        if len(parsed.get("pages_ko", [])) == num_scenes and len(parsed.get("pages_en", [])) == num_scenes:
            print(f"✨ [BAZE AI claude-sonnet-4-6 Vision Script Generated] ({num_scenes} scenes from {total_pages} PDF frames + Viral Hooks)")
            return parsed
    except Exception as e:
        print(f"  [BAZE Vision Notice] Fallback to local analyzer: {e}")
    return None


def auto_generate_page_explanations(doc, item_meta, baze_result=None, scene_ranges=None):
    """임의의 min7014.github.io PDF에 대해 장면(Scene)별 플립북 모션 범위·색상 변화와 수학적 원리를 결합해 고품질 한·영 설명 대본을 생성합니다."""
    total_pages = len(doc)
    if scene_ranges is None:
        scene_ranges = compute_pedagogical_scene_ranges(total_pages, max_scenes=12)
    num_scenes = len(scene_ranges)

    raw_title = (item_meta or {}).get("title") or "수학자료실 시각적 증명"
    clean_title_ko = clean_math_for_speech_ko(raw_title)
    clean_title_en = translate_text_google_gtx(clean_title_ko, "en")

    core_ko = clean_math_for_speech_ko((item_meta or {}).get("core_concept") or "")
    vis_ko = clean_math_for_speech_ko((item_meta or {}).get("visual_summary") or "")
    steps_ko = [clean_math_for_speech_ko(s) for s in ((item_meta or {}).get("scaffolding_steps") or [])]
    tips_ko = [clean_math_for_speech_ko(t) for t in ((item_meta or {}).get("solving_tips") or [])]

    color_desc_ko = {
        "red": "붉은색 강조 보조선과 핵심 길이 표시",
        "blue": "파란색 기본 도형 및 기준 선분 작도",
        "green": "초록색 대응 영역 및 비례 요소 표시",
        "purple": "보라색 보조선 및 각·닮음 대응 연결",
        "default": "핵심 기하 작도 및 연속 모션 전개",
    }

    pages_out = []
    prev_pil = None

    for s_idx, (p_start, p_end) in enumerate(scene_ranges):
        s_num = s_idx + 1
        rep_idx = (p_start + p_end) // 2
        pix = doc[rep_idx].get_pixmap(dpi=96)
        curr_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        bbox, c_tag = compute_page_diff_and_color(prev_pil, curr_pil) if s_idx > 0 else (None, "default")
        prev_pil = curr_pil

        c_ko = color_desc_ko.get(c_tag, color_desc_ko["default"])
        focus_desc = c_ko
        if bbox:
            cx = (bbox[0] + bbox[2]) / 2.0
            if cx > 0.54:
                focus_desc = f"우측 증명 수식 유도 ({c_ko})"
            elif cx < 0.46:
                focus_desc = f"좌측 동적 도형 작도 ({c_ko})"

        if baze_result and s_idx < len(baze_result.get("pages_ko", [])) and s_idx < len(baze_result.get("pages_en", [])):
            exp_ko = clean_math_for_speech_ko(baze_result["pages_ko"][s_idx])
            exp_en = clean_math_for_speech_en(baze_result["pages_en"][s_idx])
            step_title = "도입 · 주제 및 목표" if s_num == 1 else ("완결 · 웹 탐구 안내" if s_num == num_scenes else f"Step {s_num} · 동적 플립북 증명")
        elif s_num == 1:
            step_title = "도입 · 주제 및 증명 목표"
            exp_ko = f"1단계입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 이번 시간에는 {clean_title_ko}의 핵심 원리를 동적 플립북으로 증명해 봅시다. {core_ko}"
            exp_en = f"Step 1. Welcome to Min's Math Lab. In this dynamic visual proof lecture, we explore {clean_title_en} and see why this mathematical property holds."
        elif s_num == num_scenes:
            step_title = "완결 · 실전 적용 및 웹 탐구 안내"
            tip_str = tips_ko[0] if tips_ko else "도형의 정의와 대칭 보조선을 기억하세요."
            exp_ko = f"마지막 {s_num}단계입니다. 지금까지 총 {total_pages}프레임의 플립북 작도를 통해 정리를 완벽히 증명했습니다. 실전 팁으로, {tip_str}"
            exp_en = f"Step {s_num}. We have completed the entire {total_pages}-frame visual proof! Visit min7014.github.io to interact with the dynamic figure yourself."
        else:
            progress = (s_num - 1) / max(1, num_scenes - 2)
            range_str = f"{p_start + 1}페이지부터 {p_end + 1}페이지까지의 연속 움직임입니다." if p_end > p_start else f"{p_start + 1}페이지입니다."
            if progress <= 0.28:
                step_title = "1단계 · 기본 도형 및 기준점 작도"
                s_hint = steps_ko[0] if len(steps_ko) > 0 else "기준 도형과 꼭짓점을 명확히 배치합니다."
                exp_ko = f"{s_num}단계, {range_str} {focus_desc} 과정으로, 화면에 나타난 기본 도형과 기준점을 확인합니다. {s_hint}"
            elif progress <= 0.55:
                step_title = "2단계 · 핵심 보조선 및 동적 대칭 관찰"
                s_hint = steps_ko[1] if len(steps_ko) > 1 else vis_ko
                exp_ko = f"{s_num}단계, {range_str} {focus_desc} 단계입니다. 연속적으로 움직이는 보조선과 각·선분의 대칭 관계를 눈여겨보세요. {s_hint}"
            elif progress <= 0.82:
                step_title = "3단계 · 불변량 및 대수적 등식 도출"
                s_hint = steps_ko[2] if len(steps_ko) > 2 else "도형의 성질을 비례식과 등식으로 변환합니다."
                exp_ko = f"{s_num}단계, {range_str} {focus_desc} 과정입니다. 도형의 움직임 속에서 항상 일정하게 유지되는 합동·닮음·거리 관계를 수식으로 연결합니다. {s_hint}"
            else:
                step_title = "4단계 · 수식 결합 및 정리 완성"
                s_hint = steps_ko[3] if len(steps_ko) > 3 else "유도한 관계식들을 결합하여 최종 정리를 완성합니다."
                exp_ko = f"{s_num}단계, {range_str} {focus_desc} 마무리 단계입니다. 앞 단계의 조각들을 결합해 최종 결론을 도출합니다. {s_hint}"
            exp_en = translate_text_google_gtx(exp_ko, "en")

        pages_out.append({
            "page": rep_idx + 1,
            "scene_index": s_num,
            "frame_range": [p_start + 1, p_end + 1],
            "step_title": step_title,
            "visual_focus": focus_desc,
            "color_tag": c_tag,
            "diff_bbox": bbox,
            "explanation_text": exp_ko,
            "narrations": {"ko": exp_ko, "en": exp_en}
        })

    return pages_out


def translate_text_google_gtx(text_ko, target_lang):
    """한국어 설명 텍스트를 대상 국가 언어로 번역합니다."""
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
    [1단계: 최고 품질 설명 텍스트 대본(ko) 및 원어민급 영어 나레이션(en) 우선 생성]
    """
    if target_langs is None:
        target_langs = ["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"]

    curated = CURATED_PAGE_SCRIPTS.get(slug_key)
    item_meta = find_item_by_slug_or_pdf(slug_key)

    existing_yt_urls = {}
    out_path = SCRIPTS_DIR / f"{slug_key}.json"
    if out_path.exists():
        try:
            old_doc = json.loads(out_path.read_text(encoding="utf-8"))
            existing_yt_urls = old_doc.get("youtube_urls") or {}
        except Exception:
            pass

    if curated:
        title = curated["title"]
        title_en = curated["title_en"]
        pdf_url = curated["pdf_url"]
        web_url = curated["web_url"]
        sub_ko = (item_meta or {}).get("sub_domain_ko") or "유클리드 평면기하·작도·원주각 (Euclidean Geometry)"
    elif item_meta:
        title = item_meta.get("title", slug_key)
        title_en = translate_text_google_gtx(clean_math_for_speech_ko(title), "en")
        pdf_url = (item_meta.get("pdf") or "").split("#")[0]
        web_url = item_meta.get("url") or "https://min7014.github.io/"
        sub_ko = item_meta.get("sub_domain_ko") or "기하·대수 시각적 증명"
    else:
        raise ValueError(f"Topic not found for slug/key: {slug_key}")

    orig_yt = (item_meta or {}).get("youtube") or ""
    if orig_yt and not existing_yt_urls.get("orig"):
        existing_yt_urls["orig"] = orig_yt
    if (item_meta or {}).get("youtube_ko") and not existing_yt_urls.get("ko"):
        existing_yt_urls["ko"] = item_meta["youtube_ko"]
    if (item_meta or {}).get("youtube_en") and not existing_yt_urls.get("en"):
        existing_yt_urls["en"] = item_meta["youtube_en"]

    pdf_bytes = urllib.request.urlopen(pdf_url).read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)

    baze_result = None
    if curated and len(curated["pages_ko"]) == total_pages:
        pages_data = []
        prev_pil = None
        for idx in range(total_pages):
            exp_ko = curated["pages_ko"][idx]
            exp_en = curated["pages_en"][idx] if idx < len(curated.get("pages_en", [])) else translate_text_google_gtx(exp_ko, "en")
            pix = doc[idx].get_pixmap(dpi=96)
            curr_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            bbox, c_tag = compute_page_diff_and_color(prev_pil, curr_pil) if idx > 0 else (None, "default")
            prev_pil = curr_pil
            pages_data.append({
                "page": idx + 1,
                "step_title": "도입 · 주제 및 목표" if idx == 0 else ("완결 · 웹 탐구 안내" if idx == total_pages - 1 else f"Step {idx} · 시각적 작도 및 증명"),
                "visual_focus": "핵심 단계별 작도 및 수식 유도",
                "color_tag": c_tag,
                "diff_bbox": bbox,
                "explanation_text": exp_ko,
                "narrations": {"ko": exp_ko, "en": exp_en}
            })
    else:
        scene_ranges = compute_pedagogical_scene_ranges(total_pages, max_scenes=12)
        baze_result = call_baze_vision_for_pdf_script(doc, item_meta, scene_ranges=scene_ranges)
        if baze_result and baze_result.get("title_en"):
            title_en = baze_result["title_en"]
        pages_data = auto_generate_page_explanations(doc, item_meta, baze_result=baze_result, scene_ranges=scene_ranges)

    from concurrent.futures import ThreadPoolExecutor
    trans_jobs = []
    for p_obj in pages_data:
        base_ko = p_obj["explanation_text"]
        p_obj["narrations"]["ko"] = base_ko
        if "en" not in p_obj["narrations"] or not p_obj["narrations"]["en"]:
            trans_jobs.append((p_obj, "en", base_ko))
        for lang in target_langs:
            if lang in ("ko", "en"):
                continue
            trans_jobs.append((p_obj, lang, base_ko))
    if trans_jobs:
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = [(p_obj, lc, ex.submit(translate_text_google_gtx, txt, lc)) for (p_obj, lc, txt) in trans_jobs]
            for p_obj, lc, fut in futs:
                try:
                    p_obj["narrations"][lc] = fut.result(timeout=10)
                except Exception:
                    p_obj["narrations"][lc] = p_obj["explanation_text"]

    viral_hooks = VIRAL_HOOK_PRESETS.get(slug_key, {})
    if baze_result:
        viral_hooks = {
            "title_ko": baze_result.get("viral_title_ko") or viral_hooks.get("title_ko", ""),
            "title_en": baze_result.get("viral_title_en") or viral_hooks.get("title_en", ""),
            "hook_ko": baze_result.get("hook_ko") or viral_hooks.get("hook_ko", ""),
            "hook_en": baze_result.get("hook_en") or viral_hooks.get("hook_en", ""),
            "quiz_ko": baze_result.get("quiz_ko") or viral_hooks.get("quiz_ko", ""),
            "quiz_en": baze_result.get("quiz_en") or viral_hooks.get("quiz_en", ""),
        }

    script_doc = {
        "slug": slug_key,
        "title": title,
        "title_en": title_en,
        "sub_domain_ko": sub_ko,
        "core_concept": (item_meta or {}).get("core_concept") or "",
        "solving_tip": ((item_meta or {}).get("solving_tips") or [""])[0],
        "pdf_url": pdf_url,
        "web_url": web_url,
        "page_count": total_pages,
        "base_language": "ko",
        "quality_profile": "Broadcast Master 1080p (BAZE claude-sonnet-4-6 Vision Script + 300 DPI Lanczos + H.264 High Profile CRF 16)",
        "viral_hooks": viral_hooks,
        "storage_policy": {
            "ko": "YouTube (한국어 강의 영상 유튜브 저장·스트리밍)",
            "en": "YouTube (English Lecture Video Stored & Streamed on YouTube)",
            "other_languages": "Script-First Real-Time TTS & Studio Rendering"
        },
        "youtube_urls": {
            "ko": existing_yt_urls.get("ko", ""),
            "en": existing_yt_urls.get("en", ""),
            "orig": existing_yt_urls.get("orig", orig_yt)
        },
        "supported_languages": list(GLOBAL_VOICE_MAP.keys()),
        "pages": pages_data
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(script_doc, f, ensure_ascii=False, indent=2)

    print(f"[High-Quality Script Generated] {out_path} ({total_pages} pages, langs={target_langs})")
    return script_doc


def get_font_for_lang(lang_code, size, bold=False):
    win_fonts = Path(r"C:\Windows\Fonts")
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


VIRAL_HOOK_DB = {
    "pythagoras": {
        "match_keywords": ["pythagoras", "피타고라스", "직각삼각형", "right triangle", "넓이 보존"],
        "thumb_hook_ko": ["보조선 딱 1줄!", "넓이가 똑같다?!"],
        "thumb_hook_en": ["JUST 1 LINE?!", "EXACT SAME AREA!"],
        "badge_ko": "⚡ 99%가 공식만 외운 증명",
        "badge_en": "⚡ 99% ONLY MEMORIZED THIS",
        "cold_open_ko": "직각삼각형 위에 정사각형을 무한히 쌓아 올리면 넓이가 어떻게 될까요? 놀랍게도 보조선과 직각삼각형 하나면 두 정사각형의 넓이 합이 아래 기둥과 완벽히 같다는 걸 단 30초 만에 눈으로 볼 수 있습니다!",
        "cold_open_en": "What happens when you stack squares infinitely on a right triangle? Shockingly, you can visually prove in 30 seconds why the two branch squares equal the exact area of the trunk!",
        "quiz_ko": "💬 10초 퀴즈: 밑변이 3, 높이가 4일 때 빗변 정사각형의 넓이는? 댓글로 남겨보세요!",
        "quiz_en": "💬 10-Sec Quiz: If the legs are 3 and 4, what is the area of the hypotenuse square? Drop a comment!"
    },
    "ceva_menelaus": {
        "match_keywords": ["체바", "메넬라우스", "ceva", "menelaus", "넓이 비", "평행선"],
        "thumb_hook_ko": ["보조선 딱 1줄로", "전부 약분된다?!"],
        "thumb_hook_en": ["1 HIDDEN LINE", "CANCELS IT ALL!"],
        "badge_ko": "⚡ 상위 1% 도형 킬러 치트키",
        "badge_en": "⚡ OLYMPIAD GEOMETRY SECRET",
        "cold_open_ko": "복잡하게 얽힌 삼각형 선분 비율의 곱이 왜 언제나 정확히 1이 될까요? 보조선 딱 한 줄과 넓이 비를 연결하는 순간 모든 분수가 도미노처럼 약분되는 소름 돋는 증명을 확인해 보세요!",
        "cold_open_en": "Why does the product of these triangle segment ratios always equal 1? Draw one auxiliary line and watch every fraction cancel out like dominoes!",
        "quiz_ko": "💬 10초 퀴즈: 세 분수가 도미노처럼 약분되어 1이 되는 결정적 단계는 몇 번째인가요?",
        "quiz_en": "💬 10-Sec Quiz: At which step do all three ratios telescope and cancel to 1?"
    },
    "conic_dandelin": {
        "match_keywords": ["dandelin", "단델린", "타원", "포물선", "쌍곡선", "ellipse", "parabola", "hyperbola", "초점", "빛 반사"],
        "thumb_hook_ko": ["초점에서 쏜 빛이", "한 점에 모인다?!"],
        "thumb_hook_en": ["EVERY LIGHT RAY", "HITS ONE FOCUS!"],
        "badge_ko": "⚡ 교과서엔 없는 기하학 절정",
        "badge_en": "⚡ LEGENDARY VISUAL PROOF",
        "cold_open_ko": "한 초점에서 쏜 빛은 어느 방향으로 날아가든 곡면에 반사된 뒤 반드시 다른 초점 한 곳으로 모입니다! 접선 대칭과 단델린 구의 천재적 발상으로 이차곡선의 비밀을 단번에 증명해 봅니다!",
        "cold_open_en": "Every ray of light shot from one focus reflects off the curve and converges at the exact other focus! Witness the geometric symmetry behind conic sections!",
        "quiz_ko": "💬 10초 퀴즈: 타원 위의 점에서 두 초점까지의 거리 합은 무엇의 길이와 같을까요?",
        "quiz_en": "💬 10-Sec Quiz: The sum of distances to both foci equals which axis of the ellipse?"
    },
    "inscribed_circle": {
        "match_keywords": ["inscribed", "원주각", "중심각", "thales", "탈레스", "접선", "현", "톨레미", "원"],
        "thumb_hook_ko": ["어디로 움직여도", "각도가 똑같다?!"],
        "thumb_hook_en": ["MOVE IT ANYWHERE", "ANGLE NEVER CHANGES!"],
        "badge_ko": "⚡ 시험에 무조건 나오는 원의 성질",
        "badge_en": "⚡ THE ULTIMATE CIRCLE HACK",
        "cold_open_ko": "원 위의 점을 아무리 이리저리 움직여도 이 각도와 비례 관계는 단 1도조차 흔들리지 않습니다! 중심과 꼭짓점을 잇는 보조선 한 줄로 원 속에 숨겨진 불변량을 지금 바로 확인해 보세요!",
        "cold_open_en": "No matter where you drag this point along the circle, the geometric invariant never changes! With one auxiliary line, watch the hidden circle theorem unlock!",
        "quiz_ko": "💬 10초 퀴즈: 지름을 마주 보는 원주각은 항상 몇 도일까요? 댓글로 정답을 남겨주세요!",
        "quiz_en": "💬 10-Sec Quiz: What is the inscribed angle facing a diameter? Leave your answer in the comments!"
    },
    "viviani_polygon": {
        "match_keywords": ["viviani", "비비아니", "정삼각형", "정칠각형", "정오각형", "내각", "매듭", "작도"],
        "thumb_hook_ko": ["아무 데나 찍어도", "합이 일정하다?!"],
        "thumb_hook_en": ["HIDDEN SYMMETRY", "BLOWS YOUR MIND!"],
        "badge_ko": "⚡ 직관을 깨는 기하학 마술",
        "badge_en": "⚡ MIND-BLOWING GEOMETRY",
        "cold_open_ko": "자명해 보이는 도형 속에 수학자들도 감탄한 놀라운 대칭과 불변량이 숨어 있습니다! 도형을 분할하고 평행선을 긋는 순간 눈앞에서 완성되는 기하학의 마법을 직접 확인해 보세요!",
        "cold_open_en": "Inside this polygon lies a breathtaking symmetry and invariant that amazed mathematicians! Watch how auxiliary lines and area partitions complete the proof!",
        "quiz_ko": "💬 10초 퀴즈: 오늘 증명에서 가장 결정적인 역할을 한 보조선은 몇 번째 단계에 등장했나요?",
        "quiz_en": "💬 10-Sec Quiz: Which step introduced the key auxiliary line in this proof?"
    },
    "trigonometry": {
        "match_keywords": ["sin", "cos", "tan", "삼각함수", "사인", "코사인", "단위원", "덧셈정리"],
        "thumb_hook_ko": ["공식 외우지 마세요!", "직사각형 1개면 끝"],
        "thumb_hook_en": ["STOP MEMORIZING!", "1 BOX PROVES IT ALL"],
        "badge_ko": "⚡ 수능 1등급의 시각적 직관",
        "badge_en": "⚡ VISUAL TRIGONOMETRY HACK",
        "cold_open_ko": "복잡한 삼각함수 공식을 아직도 무작정 암기하고 계신가요? 직각삼각형을 직사각형 상자 안에 넣거나 원 위에 올리는 순간, 모든 사인 코사인 공식이 한눈에 퍼즐처럼 맞춰집니다!",
        "cold_open_en": "Still memorizing complicated trigonometry formulas by rote? Drop the triangles into a single bounding rectangle, and watch every sine and cosine identity snap together like LEGO!",
        "quiz_ko": "💬 10초 퀴즈: sin²θ + cos²θ 의 값은 각도에 상관없이 항상 얼마일까요?",
        "quiz_en": "💬 10-Sec Quiz: Regardless of the angle, what does sin²θ + cos²θ always equal?"
    },
    "calculus_series": {
        "match_keywords": ["미분", "적분", "극한", "접선", "할선", "넓이", "급수", "수열", "시그마"],
        "thumb_hook_ko": ["할선이 회전하며", "접선이 되는 순간!"],
        "thumb_hook_en": ["WATCH SECANT LINES", "BECOME A TANGENT!"],
        "badge_ko": "⚡ 눈으로 보는 미적분의 본질",
        "badge_en": "⚡ SEE CALCULUS IN MOTION",
        "cold_open_ko": "곡선 위의 두 점을 잇는 할선이 한 점으로 한없이 가까워질 때 과연 무슨 일이 일어날까요? 수식만 보면 막막했던 미적분과 극한의 본질을 살아 움직이는 동적 기하로 한눈에 깨달아 보세요!",
        "cold_open_en": "What happens as two points on a curve slide infinitely close together? Watch abstract calculus and limits come alive visually in smooth motion!",
        "quiz_ko": "💬 10초 퀴즈: 두 점을 잇는 할선의 기울기가 극한에서 도달하는 직선의 이름은 무엇일까요?",
        "quiz_en": "💬 10-Sec Quiz: What do we call the limiting line as the two secant points merge?"
    },
    "default": {
        "match_keywords": [],
        "thumb_hook_ko": ["보조선 딱 1줄!", "소름 돋는 증명"],
        "thumb_hook_en": ["JUST 1 HIDDEN LINE", "BLOWS YOUR MIND!"],
        "badge_ko": "⚡ 99%가 몰랐던 시각적 증명",
        "badge_en": "⚡ 99% NEVER SAW THIS PROOF",
        "cold_open_ko": "교과서에서는 복잡한 수식으로 길게 설명하지만, 기하학적 보조선 한 줄을 긋는 순간 단 30초 만에 눈으로 완벽히 증명됩니다! 끝까지 눈을 떼지 말고 도형의 변화를 따라와 보세요!",
        "cold_open_en": "Textbooks bury this in pages of dry algebra, but with one clever geometric line, you can see the entire proof unfold visually in 30 seconds!",
        "quiz_ko": "💬 오늘 본 시각적 증명 중 가장 놀라웠던 단계는 몇 번째 장면이었나요? 댓글로 알려주세요!",
        "quiz_en": "💬 Which step of this visual proof gave you the biggest 'Aha!' moment? Tell us in the comments!"
    },
}


def get_viral_hook_profile(script_doc):
    """주제 제목·단원·슬러그를 분석하여 최적의 VIRAL_HOOK_DB 프로필을 반환합니다."""
    blob = " ".join([
        str(script_doc.get("slug") or ""),
        str(script_doc.get("title") or ""),
        str(script_doc.get("title_en") or ""),
        str(script_doc.get("sub_domain_ko") or ""),
        str(script_doc.get("core_concept") or ""),
    ]).lower()
    for key, prof in VIRAL_HOOK_DB.items():
        if key == "default":
            continue
        for kw in prof["match_keywords"]:
            if kw.lower() in blob:
                return prof
    return VIRAL_HOOK_DB["default"]


def ensure_ambient_pad_wav():
    """
    [3Blue1Brown 스타일 -28dB 수학 사색 앰비언트 패드(Cmaj9 순정 화음 드론) 합성기]
    무음 구간(Dead Air)의 지루함을 없애고 시청 지속시간(Retention)을 높이는 90초 스테레오 배경 패드 WAV를 생성합니다.
    """
    import math
    import struct
    import wave

    pad_path = YT_PKG_DIR / "ambient_pad_48k.wav"
    if pad_path.exists() and pad_path.stat().st_size > 100000:
        return pad_path

    sr = 24000
    dur = 75.0
    n_samples = int(sr * dur)
    # C3(130.81), G3(196.00), B3(246.94), D4(293.66),E4(329.63)
    freqs = [(130.81, 0.34), (196.00, 0.26), (246.94, 0.16), (293.66, 0.14), (329.63, 0.10)]
    buf = bytearray()
    two_pi = 2.0 * math.pi
    for i in range(n_samples):
        t_sec = i / sr
        lfo = 0.78 + 0.22 * math.sin(two_pi * 0.16 * t_sec)
        val = sum(amp * math.sin(two_pi * f * t_sec) for f, amp in freqs) * lfo
        sample = max(-32767, min(32767, int(val * 1650)))  # 약 -26dB 은은한 배경음
        buf.extend(struct.pack("<hh", sample, sample))

    with wave.open(str(pad_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bytes(buf))
    return pad_path


def ensure_harmonic_chime_wav():
    """
    [수학적 순정 3화음(528Hz·660Hz·792Hz·1056Hz) 유레카 차임벨 오디오 합성기]
    핵심 단계 전환 및 증명 완성 순간에 은은하게 울리는 48kHz 스테레오 차임벨 WAV를 생성합니다.
    """
    import math
    import struct
    import wave

    chime_path = YT_PKG_DIR / "eureka_chime_48k.wav"
    if chime_path.exists() and chime_path.stat().st_size > 1000:
        return chime_path

    sr = 48000
    dur = 0.85
    n_samples = int(sr * dur)
    freqs = [(528.0, 0.42), (660.0, 0.30), (792.0, 0.20), (1056.0, 0.08)]
    buf = bytearray()
    for i in range(n_samples):
        t_sec = i / sr
        attack = min(1.0, t_sec / 0.018)
        decay = math.exp(-4.8 * t_sec)
        env = attack * decay
        val = sum(amp * math.sin(2.0 * math.pi * f * t_sec) for f, amp in freqs) * env
        sample = max(-32767, min(32767, int(val * 11000)))
        buf.extend(struct.pack("<hh", sample, sample))

    with wave.open(str(chime_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bytes(buf))
    return chime_path


def render_slide_frame_1080p(pdf_page, page_info, script_doc, lang_code, show_spotlight=True):
    """
    [v3.0 3Blue1Brown x Masterclass 방송급 HUD + 300 DPI 수퍼샘플링 + 코너 브래킷 스포트라이트 + 핵심 보조선 리본]
    1920x1080 Full HD 방송급 강의 프레임을 생성합니다.
    """
    W, H = 1920, 1080
    canvas = Image.new("RGB", (W, H), (9, 14, 28))
    draw = ImageDraw.Draw(canvas)

    p_num = page_info["page"]
    tot_p = script_doc["page_count"]
    scene_idx = page_info.get("scene_index") or p_num
    tot_scenes = len(script_doc.get("pages") or []) or tot_p

    # 1. 상단 방송 헤더 바 (높이 72px) + 시안-에메랄드 진행률 게이지 바 (y: 72~77)
    draw.rectangle([0, 0, W, 72], fill=(15, 23, 42))
    draw.rectangle([0, 72, W, 77], fill=(30, 41, 59))
    prog_w = max(12, int((p_num / max(1, tot_p)) * W))
    draw.rectangle([0, 72, prog_w, 77], fill=(56, 189, 248))
    draw.ellipse([max(0, prog_w - 6), 69, min(W, prog_w + 6), 80], fill=(250, 204, 21))

    font_header = get_font_for_lang("ko", 25, bold=True)
    font_badge = get_font_for_lang("ko", 19, bold=True)
    font_ribbon = get_font_for_lang("ko", 18, bold=True)

    header_title = script_doc.get("title_en") if lang_code == "en" and script_doc.get("title_en") else script_doc.get("title", "")
    header_title = re.sub(r"\$[^\$]*\$", "", header_title).strip()
    sub_dom = (script_doc.get("sub_domain_ko") or "시각적 수학 증명").split("(")[0].strip()

    # 좌측 상단 기하 엠블럼 + 단원 배지 + 제목
    draw.polygon([(26, 48), (42, 20), (58, 48)], outline=(56, 189, 248), fill=(225, 29, 72))
    dom_txt = f"[{sub_dom}]" if lang_code != "en" else "[Visual Proof]"
    draw.rounded_rectangle([70, 18, 70 + len(dom_txt) * 16 + 18, 54], radius=8, fill=(30, 58, 138), outline=(56, 189, 248), width=1)
    draw.text((79, 24), dom_txt, fill=(125, 211, 252), font=font_ribbon)

    tx_start = 70 + len(dom_txt) * 16 + 30
    title_str = header_title
    if len(title_str) > 46:
        title_str = title_str[:46] + "..."
    draw.text((tx_start, 20), title_str, fill=(248, 250, 252), font=font_header)

    lang_meta = GLOBAL_VOICE_MAP.get(lang_code, {"name": lang_code, "flag": ""})
    lang_tag = lang_code.upper()
    if tot_p > tot_scenes:
        right_badge = f"SCENE {scene_idx}/{tot_scenes} (FRAME {p_num}/{tot_p})  |  [{lang_tag}] 1080p"
    else:
        right_badge = f"STEP {p_num} / {tot_p}   |   [{lang_tag}] {lang_meta['name']}"
    draw.rounded_rectangle([W - 520, 14, W - 24, 58], radius=12, fill=(0, 99, 152), outline=(56, 189, 248), width=1)
    draw.text((W - 502, 23), right_badge, fill=(255, 255, 255), font=font_badge)

    # 2. 중앙 PDF 페이지 300 DPI 초고해상도 렌더링 + Lanczos 리샘플링 (y: 86 ~ 822)
    pix = pdf_page.get_pixmap(dpi=300)
    pdf_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    max_pw, max_ph = 1760, 724
    scale = min(max_pw / pdf_img.width, max_ph / pdf_img.height)
    new_w, new_h = int(pdf_img.width * scale), int(pdf_img.height * scale)
    pdf_resized = pdf_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    px = (W - new_w) // 2
    py = 86 + (max_ph - new_h) // 2

    # 외곽 글로우 프레임 및 슬라이드 배치
    draw.rounded_rectangle([px - 10, py - 10, px + new_w + 10, py + new_h + 10], radius=16, fill=(20, 34, 62))
    draw.rounded_rectangle([px - 3, py - 3, px + new_w + 3, py + new_h + 3], radius=12, fill=(56, 189, 248))
    canvas.paste(pdf_resized, (px, py))

    # 3. 새로 추가된 도형·보조선·수식 영역 스포트라이트 하이라이트 & 코너 브래킷 (show_spotlight=True 시)
    bbox = page_info.get("diff_bbox")
    if show_spotlight and bbox and p_num > 1 and p_num < tot_p:
        bx0 = max(px + 6, px + int(bbox[0] * new_w) - 14)
        by0 = max(py + 6, py + int(bbox[1] * new_h) - 14)
        bx1 = min(px + new_w - 6, px + int(bbox[2] * new_w) + 14)
        by1 = min(py + new_h - 6, py + int(bbox[3] * new_h) + 14)
        if (bx1 - bx0) > 26 and (by1 - by0) > 26:
            draw.rounded_rectangle([bx0 - 2, by0 - 2, bx1 + 2, by1 + 2], radius=12, outline=(254, 240, 138), width=2)
            draw.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(225, 29, 72), width=4)
            tag_label = f"FOCUS STEP {scene_idx}" if lang_code == "en" else f"핵심 작도·수식 포커스"
            tag_w = 152 if lang_code == "en" else 166
            tag_y = by1 + 5 if (by1 + 32) < (py + new_h) else max(py + 6, by0 - 30)
            tag_x = max(px + 6, min(px + new_w - tag_w - 6, bx1 - tag_w))
            draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + 26], radius=6, fill=(225, 29, 72))
            draw.text((tag_x + 10, tag_y + 3), tag_label, fill=(255, 255, 255), font=get_font_for_lang("ko", 16, bold=True))

    # 4. 단계 요약 & 수능 실전 보조선 팁 리본 바 (y: 822 ~ 860)
    draw.rectangle([0, 822, W, 860], fill=(15, 23, 42))
    draw.line([0, 822, W, 822], fill=(30, 58, 138), width=2)
    step_title_str = page_info.get("step_title") or (f"Step {scene_idx}" if lang_code == "en" else f"{scene_idx}단계 핵심 원리")
    vis_focus_str = page_info.get("visual_focus") or ""
    tip_raw = re.sub(r"\$[^\$]*\$", "", script_doc.get("solving_tip") or script_doc.get("core_concept") or "").strip()
    if len(tip_raw) > 58:
        tip_raw = tip_raw[:58] + "..."

    left_rib = f"🪜 [{step_title_str}]  {vis_focus_str}" if lang_code != "en" else f"🪜 [Step {scene_idx} Focus]  Dynamic Visual Proof & Geometric Invariant"
    draw.text((48, 829), left_rib[:68], fill=(56, 189, 248), font=font_ribbon)
    if tip_raw and lang_code == "ko":
        draw.text((W - 760, 829), f"💡 핵심 원리: {tip_raw}", fill=(251, 191, 36), font=font_ribbon)

    # 5. 하단 방송급 자막 스튜디오 바 (y: 860 ~ 1080)
    draw.rectangle([0, 860, W, H], fill=(7, 11, 24))
    draw.line([0, 860, W, 860], fill=(56, 189, 248), width=2)

    narration_text = page_info.get("narrations", {}).get(lang_code) or page_info.get("explanation_text", "")
    ko_ref_text = page_info.get("explanation_text", "")

    is_cjk = lang_code in ("ko", "ja") or lang_code.startswith("zh")
    wrap_width = 53 if is_cjk else 86
    wrapped_lines = textwrap.wrap(narration_text, width=wrap_width)[:3]

    font_sub = get_font_for_lang(lang_code, 29 if is_cjk else 27, bold=True)
    y_cursor = 880
    for line in wrapped_lines:
        draw.text((50, y_cursor + 2), line, fill=(0, 0, 0), font=font_sub)
        draw.text((48, y_cursor), line, fill=(254, 240, 138), font=font_sub)
        y_cursor += 40

    # 하단 고정 홈페이지 유입 프로모션 바 (y: 1030 ~ 1072)
    draw.rounded_rectangle([44, 1028, W - 44, 1070], radius=10, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
    font_cta = get_font_for_lang("ko", 20, bold=True)
    if lang_code == "ko":
        cta_left = "🌐 무료 동적 기하(GeoGebra) 조작 & 16,548문항 탈-5지선다 창의 퀴즈 👉 min7014.github.io/mathedu (설명란·고정댓글 클릭!)"
    else:
        cta_left = "🌐 Free Interactive GeoGebra & 16,548 Constructive Math Quizzes 👉 min7014.github.io/mathedu (Link in Description!)"
    draw.text((62, 1037), cta_left, fill=(125, 211, 252), font=font_cta)
    draw.text((W - 390, 1037), "📺 YouTube @min7014_ai", fill=(251, 191, 36), font=font_cta)

    return canvas


def generate_youtube_thumbnail_720p(doc, script_doc, lang_code, out_png_path):
    """
    [v4.0 CTR 14%+ 바이럴 썸네일 생성기]
    - 우측 52%: 가장 완성도 높은 클라이맥스 기하 도형 + 핵심 교점 네온 레드 서클 & 화살표 강조
    - 좌측 48%: 모바일에서도 0.5초 만에 읽히는 초대형 4단어 호기심 카피(옐로우/화이트 + 굵은 블랙 외곽선) + 주제명
    """
    W, H = 1280, 720
    thumb = Image.new("RGB", (W, H), (8, 13, 28))
    draw = ImageDraw.Draw(thumb)

    # 배경 기하 그리드 장식
    for gx in range(0, W, 80):
        draw.line([(gx, 0), (gx, H)], fill=(15, 25, 48), width=1)
    for gy in range(0, H, 80):
        draw.line([(0, gy), (W, gy)], fill=(15, 25, 48), width=1)

    vprof = get_viral_hook_profile(script_doc)
    is_en = (lang_code == "en")

    # 우측 클라이맥스 슬라이드 배치
    key_idx = max(0, len(doc) - 2)
    pix = doc[key_idx].get_pixmap(dpi=250)
    slide_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    scale = min(640 / slide_img.width, 590 / slide_img.height)
    sw, sh = int(slide_img.width * scale), int(slide_img.height * scale)
    slide_resized = slide_img.resize((sw, sh), Image.Resampling.LANCZOS)

    sx = W - sw - 34
    sy = (H - sh) // 2
    draw.rounded_rectangle([sx - 12, sy - 12, sx + sw + 12, sy + sh + 12], radius=22, fill=(225, 29, 72), outline=(251, 191, 36), width=4)
    thumb.paste(slide_resized, (sx, sy))

    # 도형 핵심 부위에 네온 레드 포커스 서클 + 화살표 + '?' 배지 작도 (시선 강제 유도)
    cx_spot = sx + int(sw * 0.48)
    cy_spot = sy + int(sh * 0.52)
    r_spot = 74
    draw.ellipse([cx_spot - r_spot - 3, cy_spot - r_spot - 3, cx_spot + r_spot + 3, cy_spot + r_spot + 3], outline=(254, 240, 138), width=4)
    draw.ellipse([cx_spot - r_spot, cy_spot - r_spot, cx_spot + r_spot, cy_spot + r_spot], outline=(225, 29, 72), width=7)
    # 굵은 빨간 화살표
    draw.line([(cx_spot - 125, cy_spot - 95), (cx_spot - 48, cy_spot - 38)], fill=(225, 29, 72), width=12)
    draw.polygon([(cx_spot - 32, cy_spot - 26), (cx_spot - 72, cy_spot - 32), (cx_spot - 46, cy_spot - 66)], fill=(225, 29, 72))
    draw.ellipse([cx_spot + r_spot - 22, cy_spot - r_spot - 18, cx_spot + r_spot + 30, cy_spot - r_spot + 34], fill=(225, 29, 72), outline=(255, 255, 255), width=3)
    draw.text((cx_spot + r_spot - 6, cy_spot - r_spot - 12), "?", fill=(255, 255, 255), font=get_font_for_lang("en", 34, bold=True))

    # 좌측 상단 후킹 배지
    badge_txt = vprof["badge_en"] if is_en else vprof["badge_ko"]
    draw.rounded_rectangle([38, 42, 548, 102], radius=16, fill=(225, 29, 72), outline=(254, 240, 138), width=2)
    draw.text((56, 56), badge_txt, fill=(255, 255, 255), font=get_font_for_lang("ko", 25, bold=True))

    # 좌측 초대형 2줄 바이럴 카피 (모바일 가독성 극대화)
    hook_lines = vprof["thumb_hook_en"] if is_en else vprof["thumb_hook_ko"]
    font_big = get_font_for_lang("ko", 56 if is_en else 64, bold=True)
    y_h = 136
    for idx_l, h_line in enumerate(hook_lines[:2]):
        col_fill = (255, 255, 255) if idx_l == 0 else (250, 204, 21)
        for dx in (-4, 0, 4):
            for dy in (-4, 0, 4):
                if dx or dy:
                    draw.text((40 + dx, y_h + dy), h_line, fill=(0, 0, 0), font=font_big)
        draw.text((40, y_h), h_line, fill=col_fill, font=font_big)
        y_h += 84

    # 중간 주제명 박스
    raw_ko_title = re.sub(r"\$[^\$]*\$", "", script_doc.get("title", "")).strip()
    ko_main_part = raw_ko_title.split("(")[0].strip() or raw_ko_title
    en_main_part = (script_doc.get("title_en") or raw_ko_title).split("—")[0].strip()
    main_title = en_main_part if is_en else ko_main_part
    wrapped_t = textwrap.wrap(main_title, width=22 if is_en else 15)[:2]

    draw.rounded_rectangle([38, 330, 568, 488], radius=18, fill=(17, 28, 56), outline=(56, 189, 248), width=2)
    font_t = get_font_for_lang("ko", 32 if is_en else 36, bold=True)
    y_t = 350
    for line in wrapped_t:
        draw.text((58, y_t), line, fill=(125, 211, 252), font=font_t)
        y_t += 50

    sub_line = (
        f"🎬 {script_doc['page_count']} Flipbook Steps · 1080p Visual Proof"
        if is_en
        else f"🎬 총 {script_doc['page_count']}프레임 동적 플립북 시각 증명"
    )
    draw.text((42, 528), sub_line, fill=(254, 240, 138), font=get_font_for_lang("ko", 25, bold=True))
    draw.rounded_rectangle([38, 586, 520, 646], radius=14, fill=(0, 99, 152))
    draw.text((58, 601), "📐 @min7014_ai · 민은기 선생님의 수학자료실", fill=(255, 255, 255), font=get_font_for_lang("ko", 22, bold=True))

    thumb.save(out_png_path, quality=98)
    return out_png_path


def format_srt_timestamp(seconds_val):
    hrs = int(seconds_val // 3600)
    mins = int((seconds_val % 3600) // 60)
    secs = int(seconds_val % 60)
    ms = int(round((seconds_val - int(seconds_val)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"


def format_yt_chapter_time(seconds_val):
    mins = int(seconds_val // 60)
    secs = int(seconds_val % 60)
    return f"{mins:02d}:{secs:02d}"


def get_media_duration_seconds(media_path, ffprobe_exe):
    if not ffprobe_exe:
        return 6.0
    try:
        cmd = [
            ffprobe_exe, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(media_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return max(1.0, float(res.stdout.strip()))
    except Exception:
        return 6.0


async def synthesize_edge_tts_mp3(text, voice_name, out_mp3_path):
    # 차분하고 또렷한 수석 교사 톤 (-2% rate)
    communicate = edge_tts.Communicate(text, voice_name, rate="-2%")
    await communicate.save(str(out_mp3_path))


VIRAL_HOOK_PRESETS = {
    "math20250130001": {
        "title_ko": "🌳 피타고라스 나무가 무한히 자라나도 넓이 합이 일정한 이유! (11단계 시각적 증명) | @min7014_ai",
        "title_en": "🌳 Why Does the Pythagoras Tree Preserve Area at Every Branch? (Visual Proof) | @min7014_ai",
        "hook_ko": "정사각형 위에 직각삼각형과 두 정사각형 가지를 계속 뻗어나가면 넓이의 합은 어떻게 될까요? 놀랍게도 매 단계 넓이가 완벽히 보존되는 프랙탈 기하학의 비밀을 11단계로 눈앞에서 증명합니다!",
        "hook_en": "What happens to the total area when a square branches into two smaller squares on a right triangle forever? Watch how the Pythagorean Theorem guarantees exact area conservation at every stage!",
        "quiz_ko": "💬 [오늘의 10초 유레카 퀴즈] 몇 번째 페이지에서 두 작은 정사각형의 넓이 합(a²+b²)이 아래 큰 정사각형 넓이(c²)와 같아진다는 결정적 단서가 등장했나요? 댓글로 페이지 번호를 남겨주세요!",
        "quiz_en": "💬 [10-Second Eureka Quiz] On which step did you see that the two smaller branch squares have the exact same combined area as the trunk square? Drop the step number in the comments!"
    },
    "2014111902": {
        "title_ko": "📐 [수능·경시 필수 도형] 체바의 정리, 삼각형 넓이 비 하나로 4분 만에 완벽 증명! | @min7014_ai",
        "title_en": "📐 Ceva's Theorem Visualized: A Stunning Proof Using Only Triangle Area Ratios! | @min7014_ai",
        "hook_ko": "삼각형의 세 꼭짓점에서 그은 세 선분이 한 점(교점)에서 만날 조건! 복잡해 보이는 체바의 정리 공식을 '높이가 같은 삼각형의 넓이 비' 하나로 명쾌하게 증명합니다.",
        "hook_en": "Why do three concurrent cevians in a triangle always multiply to 1 around the perimeter? Discover the most intuitive visual proof using only triangle area ratios!",
        "quiz_ko": "💬 [오늘의 10초 유레카 퀴즈] 세 분수의 곱이 전부 약분되어 '1'이 되는 순간은 몇 페이지인가요? 영상을 보며 찾은 번호를 댓글로 남겨주세요!",
        "quiz_en": "💬 [10-Second Eureka Quiz] At which step do the three area ratios cancel out to 1? Leave the step number in the comments below!"
    },
    "2017090101": {
        "title_ko": "🔥 [눈으로 보는 증명] 피타고라스 정리(a²+b²=c²), 정사각형 넓이 분할 25단계 완전 정복! | @min7014_ai",
        "title_en": "🔥 The Pythagorean Theorem (a²+b²=c²): 25-Step Visual Area Partition Proof! | @min7014_ai",
        "hook_ko": "공식만 외우던 피타고라스 정리(a²+b²=c²), 왜 항상 성립할까요? 한 변이 (a+b)인 큰 정사각형을 직각삼각형 4개와 가운데 정사각형으로 분할하여 누구나 100% 이해할 수 있게 증명합니다!",
        "hook_en": "Don't just memorize a² + b² = c²—see why it must be true! Watch a square of side (a+b) partition into four congruent right triangles and a tilted inner square of area c².",
        "quiz_ko": "💬 [오늘의 10초 유레카 퀴즈] 양변에서 똑같이 소거되는 네 직각삼각형의 넓이 합은 얼마인가요? (힌트: 2ab) 댓글로 정답을 남겨보세요!",
        "quiz_en": "💬 [10-Second Eureka Quiz] Why are all four interior angles of the central quadrilateral guaranteed to be 90 degrees? Share your insight in the comments!"
    },
    "2014111901": {
        "title_ko": "✨ [보조선 한 줄의 마법] 메넬라우스의 정리, 평행선 하나로 끝내는 20단계 시각 증명! | @min7014_ai",
        "title_en": "✨ Menelaus' Theorem: How One Parallel Auxiliary Line Unlocks the Proof! | @min7014_ai",
        "hook_ko": "어려운 기하 문제의 숨은 열쇠 '메넬라우스의 정리'! 꼭짓점 C를 지나며 할선에 평행한 보조선 단 한 줄을 그어 닮음비로 깔끔하게 약분되는 전율을 경험해 보세요.",
        "hook_en": "Menelaus' Theorem looks mysterious until you draw ONE parallel auxiliary line through vertex C! Watch every segment ratio telescope and cancel to 1 step by step.",
        "quiz_ko": "💬 [오늘의 10초 유레카 퀴즈] 증명의 핵심 열쇠인 '평행 보조선 CD'가 처음 등장하는 결정적 순간은 몇 페이지인가요? 댓글로 알려주세요!",
        "quiz_en": "💬 [10-Second Eureka Quiz] Which step introduces the parallel auxiliary line CD that unlocks the entire proof? Comment the step number below!"
    },
    "2025020101": {
        "title_ko": "🌟 [신비한 기하학] 종이띠로 접는 정칠각형 매듭(Regular Heptagonal Knot) 11단계 원리! | @min7014_ai",
        "title_en": "🌟 The Regular Heptagonal Knot: Hidden Euclidean Geometry in a Paper Strip! | @min7014_ai",
        "hook_ko": "자와 컴퍼스만으로는 작도할 수 없는 정칠각형을 긴 종이띠 매듭 하나로 완벽하게 만드는 기하학적 원리! 대칭성과 평행선 성질을 11단계 플립북으로 생생하게 확인하세요.",
        "hook_en": "A regular heptagon cannot be constructed with straightedge and compass alone—yet folding a simple paper strip into a knot forms a perfect regular heptagon! See the step-by-step geometry.",
        "quiz_ko": "💬 [오늘의 10초 유레카 퀴즈] 종이띠 매듭이 접히며 정칠각형의 대칭 윤곽이 완성되는 순간이 가장 인상 깊었던 페이지를 댓글로 남겨주세요!",
        "quiz_en": "💬 [10-Second Eureka Quiz] Have you ever tried folding a paper strip into a polygonal knot? Tell us your favorite step in the comments!"
    },
}


def build_youtube_metadata_for_lang(script_doc, lang_code, page_timings):
    """유튜브 알고리즘(클릭률 CTR, 시청 지속시간, 세션 연쇄 시청, 댓글 참여, 검색 SEO)에 최적화된 제목·설명·태그·자막을 생성합니다."""
    slug = script_doc["slug"]
    tot_p = script_doc["page_count"]
    pdf_url = script_doc["pdf_url"]
    web_url = script_doc.get("web_url") or "https://min7014.github.io/"
    studio_url = f"https://min7014.github.io/mathedu/video_studio.html?slug={slug}"
    board_url = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}"
    channel_url = "https://www.youtube.com/@min7014_ai"
    sub_url = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"
    channel_id = "UCSlqQfOEtRfJuMPyGMLgFYA"
    studio_upload_url = f"https://studio.youtube.com/channel/{channel_id}/videos/upload?d=ud"

    preset = script_doc.get("viral_hooks") or VIRAL_HOOK_PRESETS.get(slug, {})

    chapters = []
    for pt in page_timings:
        ts = format_yt_chapter_time(pt["start"])
        short_exp = pt["text"].replace("\n", " ").strip()
        if len(short_exp) > 62:
            short_exp = short_exp[:62] + "..."
        if lang_code == "en":
            chapters.append(f"{ts} Step {pt['page']}/{tot_p} — {short_exp}")
        else:
            chapters.append(f"{ts} {pt['page']}페이지/{tot_p} — {short_exp}")

    chapters_block = "\n".join(chapters)

    if lang_code == "en":
        clean_en_title = script_doc.get("title_en") or script_doc.get("title", slug)
        yt_title = preset.get("title_en") or f"✨ {clean_en_title} — Step-by-Step Visual Math Proof ({tot_p} Steps · 1080p) | @min7014_ai"
        if len(yt_title) > 98:
            yt_title = yt_title[:95] + "..."
        hook_en = preset.get("hook_en") or (
            f"Why does {clean_en_title} hold true? Watch every auxiliary line, angle, and algebraic cancellation unfold step by step in 1080p!"
        )
        quiz_en = preset.get("quiz_en") or (
            f"💬 [10-Second Eureka Quiz] Which step (1 to {tot_p}) gave you the biggest 'Aha!' moment? Drop the step number in the comments below!"
        )
        binge_en = (
            "🔥 [Watch Next — Popular Visual Proofs on @min7014_ai]\n"
            "• 🌳 Pythagoras Tree Area Conservation: https://youtu.be/9JKLflqrtDU\n"
            "• 🔥 Pythagorean Theorem (25-Step Area Proof): https://youtu.be/n9zyKwXXsbA\n"
            "• 📐 Ceva's Theorem via Area Ratios: https://youtu.be/ffNJhPRvh4Y\n"
            "• ✨ Menelaus' Theorem Parallel Line Proof: https://youtu.be/CjE2nyyzG2s\n"
            "• 🌟 Regular Heptagonal Knot Geometry: https://youtu.be/fXQJ8s1La-E"
        )
        yt_desc = (
            f"{hook_en}\n\n"
            f"🚀 [Try It Yourself on the Free Interactive Math Platform (min7014.github.io/mathedu)]\n"
            f"1️⃣ 📐 Interactive GeoGebra Applet & 1,113 Visual Proof Video Board:\n👉 {board_url}&from=yt\n"
            f"2️⃣ ✍️ De-Multiple-Choice Constructive Math Studio (16,548 Step-by-Step Quizzes):\n👉 https://min7014.github.io/mathedu/?from=yt\n"
            f"3️⃣ 🌱 Daily 3-Minute Math Eureka (10s Counterexample O/X & What-If-Not Problem Posing):\n👉 https://min7014.github.io/mathedu/#dailyGrowthFlywheelSection\n"
            f"4️⃣ 🎮 3D Math Sanctuary Boss Raid RPG (Free Browser Game):\n👉 https://min7014.github.io/mathedu/game.html\n"
            f"5️⃣ 🏛️ Min's Math Lab Main Archive (3,400+ Dynamic Proofs):\n👉 {web_url}\n\n"
            f"{quiz_en}\n\n"
            f"{binge_en}\n\n"
            f"🔔 Subscribe to @min7014_ai for Daily Visual Math Proofs: {sub_url}\n"
            f"📺 Main Channel (@min7014): https://www.youtube.com/@min7014\n"
            f"📄 Original Step-by-Step PDF: {pdf_url}\n"
            f"🎙️ 20+ Language AI Lecture Studio: {studio_url}\n"
            f"Topic ID: [ID: {slug}_EN]\n\n"
            f"⏱️ [00:00 Key Moments & Step-by-Step Chapters]\n{chapters_block}\n\n"
            f"#VisualProof #Geometry #Mathematics #PythagoreanTheorem #MathAnimation #3Blue1BrownStyle #GeoGebra #EuclideanGeometry #MathOlympiad #min7014_ai #min7014"
        )
        yt_tags = [
            "Visual Math Proof", "Geometry Proof", "Proof Without Words", "Euclidean Geometry",
            "Pythagorean Theorem", "Ceva Theorem", "Menelaus Theorem", "GeoGebra", "Math Animation",
            "3Blue1Brown style math", "Step by Step Math", "High School Geometry", "Math Olympiad",
            "AMC Math", "SAT Math", "Min's Math Lab", "min7014_ai", "min7014"
        ]
    else:
        clean_ko_title = re.sub(r"\$[^\$]*\$", "", script_doc.get("title", slug)).strip()
        yt_title = preset.get("title_ko") or f"🔥 [시각적 증명] {clean_ko_title} — 눈으로 깨치는 {tot_p}단계 기하 직관 (1080p) | @min7014_ai"
        if len(yt_title) > 98:
            yt_title = yt_title[:95] + "..."
        hook_ko = preset.get("hook_ko") or (
            f"공식 암기 없이 눈으로 보고 직관적으로 깨치는 [{clean_ko_title}] {tot_p}단계 시각적 증명! 보조선이 그어지는 순간 숨겨진 기하학적 대칭과 비례식이 한눈에 드러납니다."
        )
        quiz_ko = preset.get("quiz_ko") or (
            f"💬 [오늘의 10초 유레카 퀴즈] 1페이지부터 {tot_p}페이지 중 결정적인 보조선이나 핵심 아이디어가 등장한 페이지는 몇 번인가요? 댓글로 번호를 남겨주세요!"
        )
        binge_ko = (
            "🔥 [@min7014_ai 인기 시각적 증명 정주행 시리즈]\n"
            "• 🌳 피타고라스 나무 넓이 보존의 비밀 (11단계): https://youtu.be/bQO7fnT6aDU\n"
            "• 🔥 피타고라스 정리(a²+b²=c²) 넓이 분할 증명 (25단계): https://youtu.be/k6LBYa5SCiA\n"
            "• 📐 체바의 정리 삼각형 넓이 비 증명 (17단계): https://youtu.be/W_AWH-Gk89w\n"
            "• ✨ 메넬라우스의 정리 평행보조선 증명 (20단계): https://youtu.be/7zD66SWWceg\n"
            "• 🌟 정칠각형 종이띠 매듭 기하 원리 (11단계): https://youtu.be/Mq6s2JLV9mQ"
        )
        yt_desc = (
            f"{hook_ko}\n\n"
            f"🚀 [영상을 본 직후 1초 만에 내 실력으로 만드는 수학홈페이지(mathedu) 무료 실습 링크]\n"
            f"1️⃣ 📐 방금 본 증명 도형 마우스로 직접 움직여보기 (GeoGebra & 1,113개 설명영상 게시판):\n👉 {board_url}&from=yt\n"
            f"2️⃣ ✍️ [탈-5지선다 창의 구성 모드] 이 개념이 쓰인 수능·모평 기출 직접 조립하며 풀기 (16,548문항):\n👉 https://min7014.github.io/mathedu/?q={clean_ko_title.split()[0]}&from=yt\n"
            f"3️⃣ 🌱 [오늘의 3분 수학 유레카] 10초 오개념 반례 O/X 퀴즈 & 나만의 변형 문제 발명:\n👉 https://min7014.github.io/mathedu/#dailyGrowthFlywheelSection\n"
            f"4️⃣ 🎮 [수능 수학 100점 만점 3D 보스 레이드 게임] 설치 없이 브라우저에서 즉시 플레이:\n👉 https://min7014.github.io/mathedu/game.html\n"
            f"5️⃣ 🏛️ [민은기 선생님의 수학자료실 본관 (3,400+ 동적 기하 아카이브)]:\n👉 {web_url}\n\n"
            f"{quiz_ko}\n\n"
            f"{binge_ko}\n\n"
            f"🔔 [@min7014_ai 채널 구독하기]: {sub_url}\n"
            f"📺 민은기 선생님의 수학자료실 본 채널(@min7014): https://www.youtube.com/@min7014\n"
            f"📄 단계별 플립북 증명 PDF 원문: {pdf_url}\n"
            f"🎙️ 20개국어 AI 강의 스튜디오: {studio_url}\n"
            f"식별 코드: [ID: {slug}_KO]\n\n"
            f"⏱️ [00:00 단계별 핵심 챕터 타임스탬프]\n{chapters_block}\n\n"
            f"#수학 #기하학 #시각적증명 #수능수학 #피타고라스정리 #메넬라우스정리 #체바의정리 #중등기하 #고등수학 #영재고수학 #보조선 #GeoGebra #민은기선생님의수학자료실 #min7014_ai #min7014"
        )
        yt_tags = [
            "수학", "기하학", "시각적 증명", "수능 수학", "도형 보조선", "피타고라스 정리",
            "메넬라우스의 정리", "체바의 정리", "중학교 도형", "고등학교 수학", "수능 도형 킬러",
            "영재고 수학", "KMO 기하", "GeoGebra", "알지오매스", "민은기 선생님의 수학자료실",
            "민은기 선생님의 수학자료실_AI", "min7014_ai", "min7014", "수학 잘하는 법"
        ]

    return {
        "lang": lang_code,
        "channel_handle": "@min7014_ai",
        "channel_name": "민은기 선생님의 수학자료실_AI",
        "channel_id": channel_id,
        "channel_url": channel_url,
        "studio_upload_url": studio_upload_url,
        "title": yt_title,
        "description": yt_desc,
        "tags": yt_tags,
        "quiz_comment": quiz_en if lang_code == "en" else quiz_ko,
        "categoryId": "27",
        "defaultLanguage": lang_code,
        "chapters": chapters,
        "total_duration_sec": round(page_timings[-1]["end"], 2) if page_timings else 0
    }


def render_multilingual_video(slug_key, lang_code="ko", max_pages=None):
    """
    [초고품질 1080p MP4 렌더링 엔진]
    - 300 DPI Lanczos 슬라이드 + H.264 High Profile (CRF 16, 30fps) + 48kHz/192kbps Stereo AAC
    - 슬라이드 전환 직후 0.35초 시각 관찰 호흡 + 설명 후 0.65초 숙고 여운 포함
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        script_doc = generate_or_update_script(slug_key, target_langs=[lang_code, "en", "ko"])
    else:
        with open(script_path, "r", encoding="utf-8") as f:
            script_doc = json.load(f)
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
    ffprobe_exe = shutil.which("ffprobe")
    if not ffmpeg_exe:
        raise RuntimeError("ffmpeg executable not found in PATH")

    pages_to_render = list(script_doc["pages"])
    if len(pages_to_render) > 12 and not max_pages:
        ranges = compute_pedagogical_scene_ranges(len(doc), max_scenes=12)
        grouped = []
        for s_idx, (f_start, f_end) in enumerate(ranges, 1):
            # pick the representative page entry closest to f_end
            rep = next((x for x in pages_to_render if x["page"] == f_end), pages_to_render[min(len(pages_to_render)-1, f_end-1)])
            g_item = dict(rep)
            g_item["scene_index"] = s_idx
            g_item["frame_range"] = [f_start, f_end]
            grouped.append(g_item)
        pages_to_render = grouped
    if max_pages:
        pages_to_render = pages_to_render[:max_pages]

    topic_upload_dir = YT_UPLOADS_DIR / slug_key
    topic_upload_dir.mkdir(parents=True, exist_ok=True)

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_hq_{slug_key}_{lang_code}_"))
    segment_files = []
    page_timings = []
    cursor_sec = 0.0
    vprof = get_viral_hook_profile(script_doc)
    chime_wav = ensure_harmonic_chime_wav()
    ambient_wav = ensure_ambient_pad_wav()

    try:
        # [v4.0 Climax-First 3-Second Cold Open (Segment 0)]
        # 시작 즉시 가장 완성된 클라이맥스 기하 도형을 먼저 보여주며 호기심 유발 질문으로 첫 3초 이탈을 원천 차단합니다!
        cold_text = vprof["cold_open_en"] if lang_code == "en" else vprof["cold_open_ko"]
        climax_doc_idx = max(0, len(doc) - 2)
        climax_info = dict(pages_to_render[-1])
        climax_info["page"] = climax_doc_idx + 1
        climax_info["step_title"] = "⚡ COLD OPEN · 직관을 깨는 시각적 증명 하이라이트" if lang_code != "en" else "⚡ COLD OPEN · Visual Proof Highlight"
        climax_info["narrations"] = dict(climax_info.get("narrations") or {})
        climax_info["narrations"][lang_code] = cold_text
        climax_info["explanation_text"] = cold_text

        cold_img_clean = render_slide_frame_1080p(doc[climax_doc_idx], climax_info, script_doc, lang_code, show_spotlight=False)
        cold_img_spot = render_slide_frame_1080p(doc[climax_doc_idx], climax_info, script_doc, lang_code, show_spotlight=True)
        c_p1 = tmp_dir / "cold_01.png"
        c_p2 = tmp_dir / "cold_02.png"
        cold_img_clean.save(c_p1, compress_level=1)
        cold_img_spot.save(c_p2, compress_level=1)

        cold_mp3 = tmp_dir / "cold_audio.mp3"
        cold_seg = tmp_dir / "seg_cold_000.mp4"
        comm_cold = edge_tts.Communicate(cold_text, voice_name, rate="+10%")
        asyncio.run(comm_cold.save(str(cold_mp3)))
        cold_dur = get_media_duration_seconds(cold_mp3, ffprobe_exe) + 0.55
        cd1 = round(cold_dur * 0.4, 3)
        cd2 = round(cold_dur - cd1, 3)
        cold_concat = tmp_dir / "cold_concat.txt"
        cold_concat.write_text(
            f"file '{c_p1.as_posix()}'\nduration {cd1}\nfile '{c_p2.as_posix()}'\nduration {cd2}\nfile '{c_p2.as_posix()}'\n",
            encoding="utf-8",
        )
        cmd_cold = [
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0", "-i", str(cold_concat),
            "-i", str(cold_mp3),
            "-i", str(chime_wav),
            "-filter_complex",
            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=pad_dur=0.45[v];"
            "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.18[c];"
            "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
            "-preset", "veryfast", "-tune", "stillimage",
            "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-shortest",
            str(cold_seg),
        ]
        subprocess.run(cmd_cold, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        c_seg_dur = get_media_duration_seconds(cold_seg, ffprobe_exe)
        page_timings.append({
            "page": 0,
            "start": 0.0,
            "end": round(c_seg_dur, 3),
            "duration": round(c_seg_dur, 3),
            "text": cold_text,
        })
        cursor_sec += c_seg_dur
        segment_files.append(cold_seg)
        for seg_idx, p_info in enumerate(pages_to_render):
            p_idx = p_info["page"] - 1
            f_range = p_info.get("frame_range") or [p_info["page"], p_info["page"]]
            f_start, f_end = max(1, int(f_range[0])), min(len(doc), int(f_range[1]))
            narration = p_info.get("narrations", {}).get(lang_code) or p_info["explanation_text"]

            mp3_path = tmp_dir / f"audio_{seg_idx:03d}.mp3"
            seg_path = tmp_dir / f"seg_{seg_idx:03d}.mp4"
            asyncio.run(synthesize_edge_tts_mp3(narration, voice_name, mp3_path))
            tts_dur = get_media_duration_seconds(mp3_path, ffprobe_exe)
            total_seg_dur = tts_dur + 1.0  # 0.35s pre-delay + 0.65s post-pad

            # 다중 프레임 플립북 모션 장면(f_end > f_start)인 경우 연속 프레임을 렌더링하여 부드러운 모션 영상 합성
            frame_indices = list(range(f_start - 1, f_end))
            if len(frame_indices) > 8:
                # 장면당 최대 16개 연속 애니메이션 프레임 샘플링
                step_f = (len(frame_indices) - 1) / 7.0
                frame_indices = sorted(list({frame_indices[int(round(k * step_f))] for k in range(8)}))

            chime_wav = ensure_harmonic_chime_wav()
            use_chime = seg_idx in (0, len(pages_to_render) // 2, len(pages_to_render) - 1)
            audio_filter = (
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=350|350,apad=pad_dur=0.65[voice];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[chime];"
                "[voice][chime]amix=inputs=2:duration=first:dropout_transition=0[aout]"
                if use_chime
                else "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=350|350,apad=pad_dur=0.65[aout]"
            )

            if len(frame_indices) <= 1:
                # 2-Phase Dynamic Frame Sequence: 초기 28%는 전체 도형 관찰(Clean), 이후 72%는 신규 보조선 스포트라이트 강조(Spotlight)
                img_clean = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, show_spotlight=False)
                img_spot = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, show_spotlight=True)
                p_clean = tmp_dir / f"slide_{seg_idx:03d}_clean.png"
                p_spot = tmp_dir / f"slide_{seg_idx:03d}_spot.png"
                img_clean.save(p_clean, compress_level=1)
                img_spot.save(p_spot, compress_level=1)
                d1 = max(0.8, round(total_seg_dur * 0.28, 3))
                d2 = max(1.0, round(total_seg_dur - d1, 3))
                f_concat_txt = tmp_dir / f"fconcat_{seg_idx:03d}.txt"
                f_concat_txt.write_text(
                    f"file '{p_clean.as_posix()}'\nduration {d1}\nfile '{p_spot.as_posix()}'\nduration {d2}\nfile '{p_spot.as_posix()}'\n",
                    encoding="utf-8",
                )
                cmd = [
                    ffmpeg_exe, "-y",
                    "-f", "concat", "-safe", "0", "-i", str(f_concat_txt),
                    "-i", str(mp3_path),
                ]
                if use_chime:
                    cmd.extend(["-i", str(chime_wav)])
                cmd.extend([
                    "-filter_complex", audio_filter,
                    "-map", "0:v", "-map", "[aout]",
                    "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                    "-preset", "veryfast", "-tune", "stillimage",
                    "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-shortest",
                    str(seg_path)
                ])
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                per_frame_dur = max(0.18, total_seg_dur / len(frame_indices))
                f_concat_lines = []
                last_f_path = None
                for sub_i, f_doc_idx in enumerate(frame_indices):
                    sub_info = dict(p_info)
                    sub_info["page"] = f_doc_idx + 1
                    sub_img = render_slide_frame_1080p(doc[f_doc_idx], sub_info, script_doc, lang_code)
                    f_path = tmp_dir / f"slide_{seg_idx:03d}_f{sub_i:02d}.png"
                    sub_img.save(f_path, compress_level=1)
                    f_concat_lines.append(f"file '{f_path.as_posix()}'")
                    f_concat_lines.append(f"duration {per_frame_dur:.4f}")
                    last_f_path = f_path
                if last_f_path:
                    f_concat_lines.append(f"file '{last_f_path.as_posix()}'")
                f_concat_txt = tmp_dir / f"fconcat_{seg_idx:03d}.txt"
                f_concat_txt.write_text("\n".join(f_concat_lines), encoding="utf-8")
                cmd = [
                    ffmpeg_exe, "-y",
                    "-f", "concat", "-safe", "0", "-i", str(f_concat_txt),
                    "-i", str(mp3_path),
                    "-filter_complex", "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=350|350,apad=pad_dur=0.65[aout]",
                    "-map", "0:v", "-map", "[aout]",
                    "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                    "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-shortest",
                    str(seg_path)
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            seg_dur = get_media_duration_seconds(seg_path, ffprobe_exe)
            page_timings.append({
                "page": p_info["page"],
                "start": round(cursor_sec, 3),
                "end": round(cursor_sec + seg_dur, 3),
                "duration": round(seg_dur, 3),
                "text": narration
            })
            cursor_sec += seg_dur
            segment_files.append(seg_path)

        concat_txt = tmp_dir / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as cf:
            for seg in segment_files:
                cf.write(f"file '{seg.as_posix()}'\n")

        raw_concat_mp4 = tmp_dir / f"raw_concat_{slug_key}_{lang_code}.mp4"
        out_mp4 = topic_upload_dir / f"{slug_key}_{lang_code}.mp4"
        cmd_concat = [
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(raw_concat_mp4)
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 전체 영상 오디오에 -28dB 수학 사색 앰비언트 패드를 믹싱하여 무음 구간 지루함을 완벽 제거
        raw_dur = get_media_duration_seconds(raw_concat_mp4, ffprobe_exe)
        cmd_bgm = [
            ffmpeg_exe, "-y",
            "-i", str(raw_concat_mp4),
            "-stream_loop", "-1", "-i", str(ambient_wav),
            "-filter_complex",
            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[voice];"
            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.12[bgm];"
            "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart",
            "-t", f"{raw_dur:.2f}",
            str(out_mp4)
        ]
        subprocess.run(cmd_bgm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        srt_lines = []
        for idx, pt in enumerate(page_timings, 1):
            srt_lines.append(str(idx))
            srt_lines.append(f"{format_srt_timestamp(pt['start'])} --> {format_srt_timestamp(pt['end'])}")
            srt_lines.append(pt["text"])
            srt_lines.append("")
        srt_content = "\n".join(srt_lines)

        srt_pkg_path = YT_PKG_DIR / f"{slug_key}_{lang_code}.srt"
        srt_up_path = topic_upload_dir / f"{slug_key}_{lang_code}.srt"
        srt_pkg_path.write_text(srt_content, encoding="utf-8")
        srt_up_path.write_text(srt_content, encoding="utf-8")

        if lang_code in ("ko", "en"):
            thumb_pkg_path = YT_PKG_DIR / f"{slug_key}_{lang_code}_thumb.png"
            thumb_up_path = topic_upload_dir / f"{slug_key}_{lang_code}_thumb.png"
            generate_youtube_thumbnail_720p(doc, script_doc, lang_code, thumb_pkg_path)
            shutil.copyfile(thumb_pkg_path, thumb_up_path)

            yt_meta = build_youtube_metadata_for_lang(script_doc, lang_code, page_timings)
            yt_meta["srt_url"] = f"video_lectures/youtube_packages/{srt_pkg_path.name}"
            yt_meta["thumbnail_url"] = f"video_lectures/youtube_packages/{thumb_pkg_path.name}"
            yt_meta["local_mp4_path"] = f"youtube_uploads/{slug_key}/{out_mp4.name}"

            meta_json_path = YT_PKG_DIR / f"{slug_key}_youtube_meta.json"
            full_meta = {}
            if meta_json_path.exists():
                try:
                    full_meta = json.loads(meta_json_path.read_text(encoding="utf-8"))
                except Exception:
                    full_meta = {}
            full_meta[lang_code] = yt_meta
            meta_json_path.write_text(json.dumps(full_meta, ensure_ascii=False, indent=2), encoding="utf-8")
            (topic_upload_dir / f"{slug_key}_youtube_meta.json").write_text(
                json.dumps(full_meta, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            info_txt = (
                f"=== YouTube Channel: {yt_meta['channel_url']} ({yt_meta['channel_name']}) ===\n"
                f"=== Direct Upload Studio: {yt_meta['studio_upload_url']} ===\n"
                f"=== Video File: youtube_uploads/{slug_key}/{slug_key}_{lang_code}.mp4 ===\n"
                f"=== Thumbnail (1280x720): video_lectures/youtube_packages/{slug_key}_{lang_code}_thumb.png ===\n"
                f"=== Subtitle SRT: video_lectures/youtube_packages/{slug_key}_{lang_code}.srt ===\n\n"
                f"[TITLE]\n{yt_meta['title']}\n\n"
                f"[DESCRIPTION]\n{yt_meta['description']}\n\n"
                f"[TAGS]\n{', '.join(yt_meta['tags'])}\n"
            )
            (YT_PKG_DIR / f"{slug_key}_{lang_code}_youtube_info.txt").write_text(info_txt, encoding="utf-8")
            (topic_upload_dir / f"{slug_key}_{lang_code}_youtube_info.txt").write_text(info_txt, encoding="utf-8")

            for p_obj, pt in zip(script_doc["pages"], page_timings):
                p_obj.setdefault("durations", {})[lang_code] = pt["duration"]
            script_doc.setdefault("youtube_packages", {})[lang_code] = yt_meta
            with open(script_path, "w", encoding="utf-8") as f:
                json.dump(script_doc, f, ensure_ascii=False, indent=2)

        print(f"[Broadcast Master MP4 & YouTube Package] {out_mp4} ({out_mp4.stat().st_size // 1024} KB, {round(cursor_sec, 1)}s)")
        return out_mp4
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def refresh_all_youtube_metadata_packages():
    """기존 렌더링된 MP4의 타임스탬프를 유지하면서 @min7014 채널 메타데이터와 안내 파일을 일괄 갱신합니다."""
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        slug = sdoc["slug"]
        mp = YT_PKG_DIR / f"{slug}_youtube_meta.json"
        mdata = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
        up_dir = YT_UPLOADS_DIR / slug
        up_dir.mkdir(parents=True, exist_ok=True)
        for lc in ["ko", "en"]:
            timings = []
            cur = 0.0
            for p in sdoc["pages"]:
                dur = p.get("durations", {}).get(lc, 12.0)
                timings.append({
                    "page": p["page"],
                    "start": round(cur, 3),
                    "end": round(cur + dur, 3),
                    "duration": dur,
                    "text": p.get("narrations", {}).get(lc, p["explanation_text"]),
                })
                cur += dur
            yt_meta = build_youtube_metadata_for_lang(sdoc, lc, timings)
            yt_meta["srt_url"] = f"video_lectures/youtube_packages/{slug}_{lc}.srt"
            yt_meta["thumbnail_url"] = f"video_lectures/youtube_packages/{slug}_{lc}_thumb.png"
            yt_meta["local_mp4_path"] = f"youtube_uploads/{slug}/{slug}_{lc}.mp4"
            mdata[lc] = yt_meta
            sdoc.setdefault("youtube_packages", {})[lc] = yt_meta
            info_txt = (
                f"=== YouTube Channel: {yt_meta['channel_url']} ({yt_meta['channel_name']}) ===\n"
                f"=== Direct Upload Studio: {yt_meta['studio_upload_url']} ===\n"
                f"=== Video File: youtube_uploads/{slug}/{slug}_{lc}.mp4 ===\n"
                f"=== Thumbnail (1280x720): video_lectures/youtube_packages/{slug}_{lc}_thumb.png ===\n"
                f"=== Subtitle SRT: video_lectures/youtube_packages/{slug}_{lc}.srt ===\n\n"
                f"[TITLE]\n{yt_meta['title']}\n\n"
                f"[DESCRIPTION]\n{yt_meta['description']}\n\n"
                f"[TAGS]\n{', '.join(yt_meta['tags'])}\n"
            )
            (YT_PKG_DIR / f"{slug}_{lc}_youtube_info.txt").write_text(info_txt, encoding="utf-8")
            (up_dir / f"{slug}_{lc}_youtube_info.txt").write_text(info_txt, encoding="utf-8")
        mp.write_text(json.dumps(mdata, ensure_ascii=False, indent=2), encoding="utf-8")
        (up_dir / f"{slug}_youtube_meta.json").write_text(json.dumps(mdata, ensure_ascii=False, indent=2), encoding="utf-8")
        sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
    update_video_catalog()


def set_youtube_urls_for_slug(slug_key, yt_ko=None, yt_en=None, purge_local_mp4=False):
    """
    업로드 완료된 한국어(ko) 및 영어(en) 유튜브 URL을 @min7014_ai 영상저장고 인덱스(vault_index.json),
    스크립트, 카탈로그, 심층 지식 DB에 일괄 저장하고, 두 언어 모두 유튜브 저장고에 올라간 경우
    로컬 임시 MP4를 자동 정리하여 @min7014_ai를 영구 클라우드 영상저장고로 활용합니다.
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    final_ko = ""
    final_en = ""
    if script_path.exists():
        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        yt_urls = sdoc.setdefault("youtube_urls", {"ko": "", "en": "", "orig": ""})
        if yt_ko is not None:
            yt_urls["ko"] = yt_ko.strip()
        if yt_en is not None:
            yt_urls["en"] = yt_en.strip()
        final_ko = yt_urls.get("ko", "")
        final_en = yt_urls.get("en", "")
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

    matched_web_slugs = [slug_key]
    if DEEP_JSON_PATH.exists():
        items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
        changed = False
        for it in items:
            u = (it.get("url") or "").strip()
            p = (it.get("pdf") or "").split("#")[0].strip()
            if slug_key in (u, p) or u.endswith(f"/{slug_key}.html") or p.endswith(f"/{slug_key}.pdf"):
                w_slug = u.split("/")[-1].replace(".html", "").strip()
                if w_slug and w_slug not in matched_web_slugs:
                    matched_web_slugs.append(w_slug)
                if yt_ko is not None and it.get("youtube_ko") != yt_ko.strip():
                    it["youtube_ko"] = yt_ko.strip()
                    changed = True
                if yt_en is not None and it.get("youtube_en") != yt_en.strip():
                    it["youtube_en"] = yt_en.strip()
                    changed = True
        if changed:
            DEEP_JSON_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    if LOOKUP_JSON_PATH.exists():
        lmap = json.load(open(LOOKUP_JSON_PATH, "r", encoding="utf-8"))
        l_changed = False
        for k_candidate in matched_web_slugs:
            if k_candidate in lmap:
                if yt_ko is not None:
                    lmap[k_candidate]["yk"] = yt_ko.strip()
                if yt_en is not None:
                    lmap[k_candidate]["ye"] = yt_en.strip()
                l_changed = True
        if l_changed:
            LOOKUP_JSON_PATH.write_text(json.dumps(lmap, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # 한국어(ko)와 영어(en) 모두 @min7014_ai 영상저장고에 업로드 완료되면 로컬 MP4 용량 자동 회수
    if purge_local_mp4 and final_ko and final_en:
        up_dir = YT_UPLOADS_DIR / slug_key
        if up_dir.exists():
            for mp4_file in up_dir.glob("*.mp4"):
                try:
                    mp4_file.unlink()
                    print(f"  [Vault Offload] @min7014_ai 저장 완료 -> 로컬 MP4 정리: {mp4_file.name}")
                except Exception:
                    pass

    update_video_catalog()
    print(f"[@min7014_ai Video Vault Registered] slug={slug_key} -> ko={yt_ko}, en={yt_en}")


YOUTUBE_CHANNEL_HANDLE = "@min7014_ai"
YOUTUBE_CHANNEL_NAME = "민은기 선생님의 수학자료실_AI"
YOUTUBE_CHANNEL_ID = "UCSlqQfOEtRfJuMPyGMLgFYA"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@min7014_ai"
YOUTUBE_STUDIO_UPLOAD_URL = f"https://studio.youtube.com/channel/{YOUTUBE_CHANNEL_ID}/videos/upload?d=ud"
YOUTUBE_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
MAIN_CHANNEL_URL = "https://www.youtube.com/@min7014"
MAIN_CHANNEL_ID = "UC7DN_e571yaTderHffKFTTg"


def find_google_client_secret():
    """프로젝트 루트, 다운로드 폴더, 바탕화면에서 Google OAuth client_secret*.json을 자동 탐색합니다."""
    exact_candidates = [
        ROOT_DIR / "youtube_client_secret.json",
        ROOT_DIR / "client_secret.json",
        Path.home() / "youtube_client_secret.json",
        Path.home() / "client_secret.json",
    ]
    for p in exact_candidates:
        if p.exists():
            return p
    for search_dir in [ROOT_DIR, Path.home() / "Downloads", Path.home() / "Desktop"]:
        if search_dir.exists():
            matches = sorted(search_dir.glob("client_secret*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
            if matches:
                target = ROOT_DIR / "youtube_client_secret.json"
                shutil.copyfile(matches[0], target)
                return target
    return None


def sync_youtube_channel_rss():
    """https://www.youtube.com/@min7014_ai (UCSlqQfOEtRfJuMPyGMLgFYA) 공개 RSS 피드를 조회하여 업로드된 한국어·영어 영상을 자동 매칭합니다."""
    import xml.etree.ElementTree as ET
    entries = []
    for rss_url in [YOUTUBE_RSS_URL]:
        try:
            req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(req, timeout=15).read()
            root = ET.fromstring(raw)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "yt": "http://www.youtube.com/xml/schemas/2015",
                "media": "http://search.yahoo.com/mrss/",
            }
            for entry in root.findall("atom:entry", ns):
                vid_el = entry.find("yt:videoId", ns)
                title_el = entry.find("atom:title", ns)
                desc_el = entry.find("media:group/media:description", ns)
                if vid_el is not None and title_el is not None:
                    entries.append({
                        "video_id": vid_el.text.strip(),
                        "title": (title_el.text or "").strip(),
                        "description": (desc_el.text or "").strip() if desc_el is not None else "",
                        "url": f"https://youtu.be/{vid_el.text.strip()}",
                    })
        except Exception as e:
            print(f"[RSS Notice] {rss_url}: {e}")

    matched_count = 0
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        slug = sdoc["slug"]
        title_ko = re.sub(r"\$[^\$]*\$", "", sdoc.get("title", "")).strip()
        title_en = (sdoc.get("title_en") or "").strip()
        found_ko = None
        found_en = None
        found_short_ko = None
        found_short_en = None
        for ent in entries:
            blob = f"{ent['title']}\n{ent['description']}"
            vid_id = ent["video_id"]
            if f"[ID: {slug}_SHORT_KO]" in blob or f"[{slug}_SHORT_KO]" in blob or (slug in blob and "#Shorts" in blob and ("#수학" in blob or "시각적" in blob)):
                found_short_ko = f"https://youtube.com/shorts/{vid_id}"
            elif f"[ID: {slug}_SHORT_EN]" in blob or f"[{slug}_SHORT_EN]" in blob or (slug in blob and "#Shorts" in blob and ("#Math" in blob or "Visual" in blob)):
                found_short_en = f"https://youtube.com/shorts/{vid_id}"
            elif f"[ID: {slug}_KO]" in blob or f"[{slug}_KO]" in blob or (slug in blob and ("단계별" in ent["title"] or "수학자료실" in ent["title"])):
                found_ko = ent["url"]
            elif f"[ID: {slug}_EN]" in blob or f"[{slug}_EN]" in blob or (slug in blob and ("Visual Proof" in ent["title"] or "Min's Math Lab" in ent["title"])):
                found_en = ent["url"]
            elif title_ko and len(title_ko) >= 3 and title_ko in ent["title"] and "Visual Proof" not in ent["title"]:
                if "#Shorts" in ent["title"]:
                    found_short_ko = f"https://youtube.com/shorts/{vid_id}"
                else:
                    found_ko = ent["url"]
            elif title_en and len(title_en) >= 5 and title_en.lower() in ent["title"].lower():
                if "#shorts" in ent["title"].lower():
                    found_short_en = f"https://youtube.com/shorts/{vid_id}"
                else:
                    found_en = ent["url"]
        if found_short_ko or found_short_en:
            if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
                sdoc["shorts_urls"] = {"ko": "", "en": ""}
            if found_short_ko:
                sdoc["shorts_urls"]["ko"] = found_short_ko
            if found_short_en:
                sdoc["shorts_urls"]["en"] = found_short_en
            sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            update_video_catalog()
            matched_count += 1
        if found_ko or found_en:
            set_youtube_urls_for_slug(slug, yt_ko=found_ko, yt_en=found_en)
            matched_count += 1
    print(f"[@min7014_ai Channel RSS Sync] Checked {len(entries)} videos on {YOUTUBE_CHANNEL_URL} -> Matched {matched_count} topics.")
    return matched_count


def prepare_ready_batch_folder(open_explorer=True):
    """
    이미 로그인된 크롬 YouTube Studio 창에 마우스로 한 번에 전체 드래그 앤 드롭(최대 15개 동시 업로드)할 수 있도록
    유튜브 제목과 고유 식별 태그([slug_KO], [slug_EN])가 파일명으로 지정된 마스터 MP4 모음 폴더를 생성합니다.
    """
    ready_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai"
    ready_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        slug = sdoc["slug"]
        meta_p = YT_PKG_DIR / f"{slug}_youtube_meta.json"
        if not meta_p.exists():
            continue
        mdata = json.loads(meta_p.read_text(encoding="utf-8"))
        for lc in ["ko", "en"]:
            src = YT_UPLOADS_DIR / slug / f"{slug}_{lc}.mp4"
            if src.exists() and lc in mdata:
                raw_title = mdata[lc]["title"]
                safe_title = re.sub(r'[\\/:*?"<>|]', " ", raw_title).strip()
                fname = f"{safe_title[:78]} [{slug}_{lc.upper()}].mp4"
                dst = ready_dir / fname
                shutil.copyfile(src, dst)
                count += 1
                print(f"[Ready for 1-Drag Upload] {dst.name}")
    if open_explorer and os.name == "nt":
        os.startfile(str(ready_dir))
    return ready_dir


def open_youtube_studio_for_min7014(slug_key="math20250130001"):
    """@min7014_ai 공식 YouTube Studio 업로드 창과 로컬 youtube_uploads 폴더를 즉시 엽니다."""
    import webbrowser
    target_dir = YT_UPLOADS_DIR / slug_key
    if not target_dir.exists():
        target_dir = YT_UPLOADS_DIR
    print(f"[Opening @min7014_ai YouTube Studio] {YOUTUBE_STUDIO_UPLOAD_URL}")
    print(f"[Opening Local Master MP4 Folder] {target_dir}")
    webbrowser.open(YOUTUBE_STUDIO_UPLOAD_URL)
    if os.name == "nt":
        os.startfile(str(target_dir))


def ensure_topic_rendered_for_upload(slug_key, langs=("ko", "en")):
    """특정 슬러그의 대본 JSON 및 한국어/영어 1080p 마스터 MP4·썸네일·SRT 패키지가 없으면 즉시 자동 생성합니다."""
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        generate_or_update_script(slug_key, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
    for lc in langs:
        mp4_path = YT_UPLOADS_DIR / slug_key / f"{slug_key}_{lc}.mp4"
        meta_path = YT_PKG_DIR / f"{slug_key}_youtube_meta.json"
        if not mp4_path.exists() or not meta_path.exists():
            render_multilingual_video(slug_key, lang_code=lc)


def upload_slug_via_studio_browser(slug_key, langs=("ko", "en"), privacy="public"):
    """
    [Playwright 기반 @min7014_ai YouTube Studio 자동 업로더]
    - Google Cloud client_secret.json 없이도 브라우저 자동화로 https://www.youtube.com/@min7014_ai (UCSlqQfOEtRfJuMPyGMLgFYA)에
      한국어(ko)·영어(en) MP4 영상, 제목, 타임스탬프 설명문, 썸네일, 공개 설정을 자동으로 입력·게시합니다.
    - 최초 1회 실행 시 전용 프로필(.yt_studio_profile_min7014_ai)에서 구글 로그인만 완료하면 이후에는 로그인 없이 자동 업로드됩니다.
    """
    import time
    from playwright.sync_api import sync_playwright

    ensure_topic_rendered_for_upload(slug_key, langs=langs)
    meta_path = YT_PKG_DIR / f"{slug_key}_youtube_meta.json"
    meta_all = json.loads(meta_path.read_text(encoding="utf-8"))

    profile_dir = ROOT_DIR / ".yt_chrome_robot_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    uploaded_urls = {}

    privacy_radio_name = {
        "public": "PUBLIC",
        "unlisted": "UNLISTED",
        "private": "PRIVATE",
    }.get(privacy.lower(), "PUBLIC")

    with sync_playwright() as p:
        browser_ctx = None
        for ch_name in ["chrome", "msedge"]:
            try:
                browser_ctx = p.chromium.launch_persistent_context(
                    user_data_dir=str(profile_dir),
                    channel=ch_name,
                    headless=False,
                    ignore_default_args=["--enable-automation"],
                    args=["--disable-blink-features=AutomationControlled", "--start-maximized"],
                    no_viewport=True,
                )
                break
            except Exception:
                continue
        if browser_ctx is None:
            browser_ctx = p.chromium.launch_persistent_context(
                user_data_dir=str(profile_dir),
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=["--disable-blink-features=AutomationControlled"],
            )

        page = browser_ctx.pages[0] if browser_ctx.pages else browser_ctx.new_page()
        try:
            page.bring_to_front()
        except Exception:
            pass

        for lang_code in langs:
            mp4_path = (YT_UPLOADS_DIR / slug_key / f"{slug_key}_{lang_code}.mp4").resolve()
            thumb_path = (YT_PKG_DIR / f"{slug_key}_{lang_code}_thumb.png").resolve()
            meta = meta_all[lang_code]

            print(f"[Studio Auto-Upload -> {YOUTUBE_CHANNEL_HANDLE}] Navigating to {YOUTUBE_STUDIO_UPLOAD_URL} ({slug_key}_{lang_code}.mp4)")
            page.goto(YOUTUBE_STUDIO_UPLOAD_URL, wait_until="domcontentloaded")

            # 만약 구글 로그인이 안 되어 있다면 화면 상단에 친절한 안내 배너를 띄우고 사용자가 1회 로그인할 때까지 대기 (최대 10분)
            if not page.url.startswith("https://studio.youtube.com/"):
                try:
                    page.evaluate("""() => {
                        const b = document.createElement('div');
                        b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#006398;color:#fff;padding:14px 20px;font-size:17px;font-weight:bold;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.3);font-family:sans-serif;';
                        b.innerHTML = '🤖 [자동 업로드 로봇 전용 창] 이 창에서 딱 1번만 로그인해 주시면, 지금부터 모든 영상을 로봇이 스스로 클릭하여 자동 업로드합니다!';
                        document.body.prepend(b);
                    }""")
                except Exception:
                    pass
                print("=" * 72)
                print(f"🔐 [최초 1회 로그인 대기 중] 새로 열린 로봇 전용 크롬 창에서 로그인해 주세요.")
                print("=" * 72)
                page.wait_for_url(lambda u: u.startswith("https://studio.youtube.com/"), timeout=600000)
                time.sleep(3.0)
                if YOUTUBE_CHANNEL_ID not in page.url:
                    page.goto(YOUTUBE_STUDIO_UPLOAD_URL, wait_until="domcontentloaded")
                    time.sleep(3.0)

            # 신규 채널 환영 팝업("계속" / "Continue") 자동 닫기
            try:
                welcome_btn = page.locator('ytcp-button#dismiss-button, button:has-text("계속"), button:has-text("Continue")').first
                if welcome_btn.is_visible(timeout=3000):
                    welcome_btn.click(timeout=3000)
                    time.sleep(1.0)
            except Exception:
                pass

            # 업로드 모달의 input[type="file"] 대기 (모달이 닫혀 있으면 만들기->동영상 업로드 자동 클릭)
            try:
                file_input = page.locator('ytcp-uploads-file-picker input[type="file"], input[name="Filedata"], input[type="file"]').first
                file_input.wait_for(state="attached", timeout=8000)
            except Exception:
                try:
                    create_btn = page.locator('ytcp-button#create-icon, #create-icon, ytcp-button#upload-icon, #upload-icon, button[aria-label*="만들기"], button[aria-label*="Create"]').first
                    create_btn.click(timeout=8000)
                    time.sleep(1.0)
                    upload_item = page.locator('tp-yt-paper-item#text-item-0, tp-yt-paper-item:has-text("동영상 업로드"), tp-yt-paper-item:has-text("Upload videos")').first
                    if upload_item.is_visible(timeout=3000):
                        upload_item.click(timeout=5000)
                except Exception:
                    pass
                file_input = page.locator('input[type="file"]').first
                file_input.wait_for(state="attached", timeout=60000)

            file_input.set_input_files(str(mp4_path))
            print(f"  [1/5] MP4 파일 투입 완료: {mp4_path.name}")

            # 제목 입력란 대기 및 입력
            title_box = page.locator('#title-textarea #textbox, ytcp-social-suggestions-textbox#title-textarea #textbox').first
            title_box.wait_for(state="visible", timeout=45000)
            time.sleep(1.5)
            title_box.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            title_box.fill(meta["title"])
            print(f"  [2/5] 제목 자동 입력 완료: {meta['title']}")

            # 설명 입력란 입력
            try:
                desc_box = page.locator('#description-textarea #textbox, ytcp-social-suggestions-textbox#description-textarea #textbox').first
                desc_box.click(timeout=8000)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                desc_box.fill(meta["description"])
                print("  [3/5] 타임스탬프(00:00) 챕터 설명문 자동 입력 완료")
            except Exception as e:
                print(f"  [Description Warning] {e}")

            # 썸네일 업로드 시도
            if thumb_path.exists():
                try:
                    thumb_input = page.locator('ytcp-thumbnails-compact-editor-uploader input[type="file"], input#file-loader').first
                    if thumb_input.count() > 0:
                        thumb_input.set_input_files(str(thumb_path))
                        print(f"  [Thumbnail] 1280x720 썸네일 등록 완료: {thumb_path.name}")
                except Exception:
                    pass

            # 아동용 아님(VIDEO_MADE_FOR_KIDS_NOT_MFK) 선택
            try:
                not_kids = page.locator('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"], [name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]').first
                not_kids.scroll_into_view_if_needed(timeout=5000)
                not_kids.click(timeout=5000)
            except Exception:
                pass

            # 업로드된 영상 고유 URL 추출 시도
            yt_url = ""
            try:
                link_el = page.locator('a.style-scope.ytcp-video-info[href*="youtu.be"], a[href*="youtu.be/"]').first
                link_el.wait_for(state="visible", timeout=15000)
                href = link_el.get_attribute("href") or ""
                if "youtu.be/" in href:
                    yt_url = href.strip()
            except Exception:
                pass

            # 다음(Next) 버튼 3회 클릭 -> 공개 상태 선택 -> 게시(Done) 클릭
            for step_i in range(3):
                time.sleep(1.0)
                next_btn = page.locator('#next-button').first
                next_btn.click(timeout=15000)

            time.sleep(1.2)
            try:
                vis_radio = page.locator(f'tp-yt-paper-radio-button[name="{privacy_radio_name}"], [name="{privacy_radio_name}"]').first
                vis_radio.click(timeout=8000)
            except Exception:
                pass

            if not yt_url:
                try:
                    href = page.locator('a[href*="youtu.be/"]').first.get_attribute("href") or ""
                    if "youtu.be/" in href:
                        yt_url = href.strip()
                except Exception:
                    pass

            time.sleep(1.5)
            done_btn = page.locator('#done-button').first
            done_btn.click(timeout=20000)
            print(f"  [4/5] @min7014_ai 게시(Publish) 클릭 완료! ({yt_url or 'URL 동기화 대기'})")

            # 게시 완료 다이얼로그 대기 후 닫기
            time.sleep(4.0)
            if not yt_url:
                try:
                    html_snap = page.content()
                    m_url = re.search(r"https://youtu\.be/[A-Za-z0-9_-]{11}", html_snap)
                    if m_url:
                        yt_url = m_url.group(0)
                except Exception:
                    pass
            try:
                close_btn = page.locator('ytcp-button#close-button, #close-icon-button').first
                if close_btn.is_visible():
                    close_btn.click(timeout=5000)
            except Exception:
                pass

            if yt_url:
                uploaded_urls[lang_code] = yt_url
                print(f"  [5/5] YouTube URL 확보 완료 ({lang_code.upper()}): {yt_url}")
            time.sleep(2.0)

        browser_ctx.close()

    if uploaded_urls:
        set_youtube_urls_for_slug(
            slug_key,
            yt_ko=uploaded_urls.get("ko"),
            yt_en=uploaded_urls.get("en"),
        )
    else:
        sync_youtube_channel_rss()
    return uploaded_urls


def upload_slug_to_youtube(slug_key, langs=("ko", "en"), privacy="public", method="auto"):
    """
    https://www.youtube.com/@min7014_ai (UCSlqQfOEtRfJuMPyGMLgFYA) 채널에 한국어(ko)·영어(en) 영상을 자동 업로드합니다.
    - method='auto': client_secret.json이 있으면 YouTube Data API v3를 사용하고, 없으면 Playwright YouTube Studio 브라우저 자동 업로더를 실행합니다.
    """
    ensure_topic_rendered_for_upload(slug_key, langs=langs)
    secret_file = find_google_client_secret()

    if method == "browser" or (method == "auto" and not secret_file):
        print(f"[Auto-Upload Mode: YouTube Studio Browser Automation -> {YOUTUBE_CHANNEL_URL}]")
        return upload_slug_via_studio_browser(slug_key, langs=langs, privacy=privacy)

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]

    token_file = ROOT_DIR / "youtube_token_min7014_ai.json"
    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(f"[Google OAuth] 아래 인증 주소를 크롬에서 열어 {YOUTUBE_CHANNEL_URL} ({YOUTUBE_CHANNEL_NAME}) 계정을 선택해 허용해 주세요...", flush=True)
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_file), SCOPES)
            creds = flow.run_local_server(port=8089, open_browser=False)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    youtube = build("youtube", "v3", credentials=creds)
    try:
        ch_resp = youtube.channels().list(part="snippet", mine=True).execute()
        ch_items = ch_resp.get("items", [])
        if ch_items:
            auth_ch_id = ch_items[0]["id"]
            auth_ch_title = ch_items[0]["snippet"].get("title", "")
            auth_custom = ch_items[0]["snippet"].get("customUrl", "")
            print(f"[Authenticated YouTube Channel] {auth_ch_title} ({auth_custom}, ID={auth_ch_id})")
            if auth_ch_id != YOUTUBE_CHANNEL_ID:
                print(f"  [주의] 현재 로그인된 채널({auth_custom})이 목표 AI 채널({YOUTUBE_CHANNEL_HANDLE}: {YOUTUBE_CHANNEL_ID})과 다릅니다.")
    except Exception as e:
        print(f"[Channel Check Notice] {e}")

    uploaded_urls = {}
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    existing_yt = {}
    if script_path.exists():
        try:
            existing_yt = json.loads(script_path.read_text(encoding="utf-8")).get("youtube_urls") or {}
        except Exception:
            existing_yt = {}

    for lang_code in langs:
        if existing_yt.get(lang_code):
            uploaded_urls[lang_code] = existing_yt[lang_code]
            print(f"[Already in @min7014_ai Vault ({lang_code.upper()})] {existing_yt[lang_code]}")
            continue

        mp4_path = YT_UPLOADS_DIR / slug_key / f"{slug_key}_{lang_code}.mp4"
        if not mp4_path.exists():
            render_multilingual_video(slug_key, lang_code=lang_code)

        meta_path = YT_PKG_DIR / f"{slug_key}_youtube_meta.json"
        meta_all = json.loads(meta_path.read_text(encoding="utf-8"))
        meta = meta_all[lang_code]

        body = {
            "snippet": {
                "title": meta["title"],
                "description": meta["description"],
                "tags": meta["tags"],
                "categoryId": meta.get("categoryId", "27"),
                "defaultLanguage": lang_code,
                "defaultAudioLanguage": lang_code,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            },
        }

        try:
            media = MediaFileUpload(str(mp4_path), chunksize=-1, resumable=True, mimetype="video/mp4")
            req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = req.execute()
            vid_id = resp["id"]
            yt_url = f"https://youtu.be/{vid_id}"
            uploaded_urls[lang_code] = yt_url
            print(f"[YouTube Uploaded to {YOUTUBE_CHANNEL_HANDLE} ({lang_code.upper()})] {yt_url}", flush=True)
            set_youtube_urls_for_slug(
                slug_key,
                yt_ko=yt_url if lang_code == "ko" else None,
                yt_en=yt_url if lang_code == "en" else None,
            )
        except Exception as up_err:
            print(f"  [YouTube Upload API Notice ({slug_key} / {lang_code})] {up_err}", flush=True)
            break

        thumb_path = YT_PKG_DIR / f"{slug_key}_{lang_code}_thumb.png"
        if thumb_path.exists():
            try:
                youtube.thumbnails().set(
                    videoId=vid_id,
                    media_body=MediaFileUpload(str(thumb_path), mimetype="image/png")
                ).execute()
            except Exception as e:
                print(f"  [Thumbnail Warning] {e}")

        srt_path = YT_PKG_DIR / f"{slug_key}_{lang_code}.srt"
        if srt_path.exists():
            try:
                youtube.captions().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "videoId": vid_id,
                            "language": lang_code,
                            "name": "Korean Step-by-Step" if lang_code == "ko" else "English Step-by-Step",
                            "isDraft": False,
                        }
                    },
                    media_body=MediaFileUpload(str(srt_path), mimetype="application/octet-stream")
                ).execute()
            except Exception as e:
                print(f"  [Caption Warning] {e}")

    if uploaded_urls:
        set_youtube_urls_for_slug(
            slug_key,
            yt_ko=uploaded_urls.get("ko"),
            yt_en=uploaded_urls.get("en")
        )
    return uploaded_urls


def get_next_pending_slugs(count=1):
    """
    866개 전체 PDF 자료 중 아직 @min7014_ai 유튜브 URL(ko/en)이 등록되지 않은 주제를 우선순위대로 반환합니다.
    1순위: 이미 1080p MP4가 렌더링된 대표 주제(math20250130001, 2014111902, 2017090101, 2014111901)
    2순위: min7014_deep_knowledge.json의 전체 PDF 자료
    """
    pending = []
    priority_slugs = ["math20250130001", "2014111902", "2017090101", "2014111901"]

    for p_slug in priority_slugs:
        sp = SCRIPTS_DIR / f"{p_slug}.json"
        if sp.exists():
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
            yt_u = sdoc.get("youtube_urls") or {}
            if not yt_u.get("ko") or not yt_u.get("en"):
                pending.append(p_slug)
        else:
            pending.append(p_slug)
        if len(pending) >= count:
            return pending[:count]

    if DEEP_JSON_PATH.exists():
        items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
        for it in items:
            pdf_u = (it.get("pdf") or "").split("#")[0].strip()
            if not pdf_u:
                continue
            slug = pdf_u.split("/")[-1].replace(".pdf", "").strip()
            if not slug or slug in pending:
                continue
            if it.get("youtube_ko") and it.get("youtube_en"):
                continue
            sp = SCRIPTS_DIR / f"{slug}.json"
            if sp.exists():
                sdoc = json.loads(sp.read_text(encoding="utf-8"))
                yt_u = sdoc.get("youtube_urls") or {}
                if yt_u.get("ko") and yt_u.get("en"):
                    continue
            pending.append(slug)
            if len(pending) >= count:
                break
    return pending[:count]


def auto_pipeline_batch(count=1, specific_slug=None, privacy="public", upload_enable=True, git_push=False):
    """
    [완전 자동화 AI 영상 생성 & @min7014_ai 업로드 파이프라인]
    1) PDF 다운로드 및 픽셀 변화·수식 기반 8개국어 대본 자동 생성
    2) 1080p Broadcast Master 한국어(_ko.mp4) & 영어(_en.mp4) + 1280x720 썸네일 + SRT 자막 자동 생성
    3) https://www.youtube.com/@min7014_ai 채널로 자동 업로드 및 사이트 카탈로그 자동 반영
    """
    target_slugs = [specific_slug] if specific_slug else get_next_pending_slugs(count=count)
    results = []
    for idx, s_key in enumerate(target_slugs, 1):
        print("=" * 72)
        print(f"🚀 [{idx}/{len(target_slugs)}] AI 자동 영상 생성 & @min7014_ai 업로드 파이프라인 가동: {s_key}")
        print("=" * 72)
        generate_or_update_script(s_key, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
        for lc in ["ko", "en"]:
            mp4_p = YT_UPLOADS_DIR / s_key / f"{s_key}_{lc}.mp4"
            if not mp4_p.exists():
                render_multilingual_video(s_key, lang_code=lc)
            short_p = YT_UPLOADS_DIR / "shorts" / f"{s_key}_short_{lc}.mp4"
            if not short_p.exists():
                render_youtube_short_vertical(s_key, lang_code=lc)
        update_video_catalog()
        uploaded = {}
        if upload_enable:
            uploaded = upload_slug_to_youtube(s_key, langs=("ko", "en"), privacy=privacy, method="auto")
        results.append({"slug": s_key, "uploaded_urls": uploaded})

    if git_push:
        try:
            subprocess.run([
                "git", "add",
                "video_lectures/catalog.json",
                "video_lectures/vault_index.json",
                "video_lectures/scripts/",
                "video_lectures/youtube_packages/",
                "assets/min7014_deep_knowledge.json",
                "assets/min7014_lookup.json",
            ], check=False)
            subprocess.run(["git", "commit", "-m", f"chore(youtube-ai): auto-sync @min7014_ai videos ({', '.join(target_slugs)})"], check=False)
            subprocess.run(["git", "push", "origin", "main"], check=False)
        except Exception as e:
            print(f"[Git Push Notice] {e}")
    return results


def update_video_catalog():
    scripts = []
    short_by_slug = {}
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        with open(sp, "r", encoding="utf-8") as f:
            sdoc = json.load(f)
        slug = sdoc["slug"]
        yt_urls = sdoc.get("youtube_urls") or {"ko": "", "en": "", "orig": ""}
        yt_pkgs = sdoc.get("youtube_packages") or {}
        shorts_urls = sdoc.get("shorts_urls") or {"ko": "", "en": ""}
        shorts_pkgs = sdoc.get("shorts_packages") or {}

        # 로컬에 생성된 숏폼(youtube_uploads/shorts -> video_lectures/shorts/{slug}_short_{lc}.mp4) 자동 동기화
        for lc in ["ko", "en"]:
            sp_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_{lc}.mp4"
            if not sp_mp4.exists():
                sp_mp4 = ROOT_DIR / "video_lectures" / "shorts" / f"{slug}_short_{lc}.mp4"
            if sp_mp4.exists():
                pub_short_dir = ROOT_DIR / "video_lectures" / "shorts"
                pub_short_dir.mkdir(parents=True, exist_ok=True)
                pub_dst = pub_short_dir / f"{slug}_short_{lc}.mp4"
                try:
                    if sp_mp4.resolve() != pub_dst.resolve():
                        if not pub_dst.exists() or sp_mp4.stat().st_size != pub_dst.stat().st_size:
                            shutil.copyfile(sp_mp4, pub_dst)
                except Exception:
                    pass
                if lc not in shorts_pkgs:
                    shorts_pkgs[lc] = {
                        "title": f"🔥 {sdoc['title'] if lc == 'ko' else (sdoc.get('title_en') or sdoc['title'])} #Shorts",
                        "local_mp4_path": f"video_lectures/shorts/{slug}_short_{lc}.mp4",
                        "aspect_ratio": "9:16 (1080x1920)",
                    }
                else:
                    shorts_pkgs[lc]["local_mp4_path"] = f"video_lectures/shorts/{slug}_short_{lc}.mp4"

        short_by_slug[slug] = {
            "shorts_urls": shorts_urls,
            "shorts_packages": shorts_pkgs,
        }

        scripts.append({
            "slug": slug,
            "title": sdoc["title"],
            "title_en": sdoc.get("title_en", ""),
            "sub_domain_ko": sdoc.get("sub_domain_ko", ""),
            "pdf_url": sdoc["pdf_url"],
            "web_url": sdoc.get("web_url", ""),
            "page_count": sdoc["page_count"],
            "quality_profile": sdoc.get("quality_profile", "Broadcast Master 1080p"),
            "script_url": f"video_lectures/scripts/{sp.name}",
            "available_langs": list(sdoc["pages"][0].get("narrations", {}).keys()) if sdoc.get("pages") else ["ko"],
            "youtube_channel": {
                "handle": YOUTUBE_CHANNEL_HANDLE,
                "name": YOUTUBE_CHANNEL_NAME,
                "channel_id": YOUTUBE_CHANNEL_ID,
                "channel_url": YOUTUBE_CHANNEL_URL,
                "studio_upload_url": YOUTUBE_STUDIO_UPLOAD_URL,
                "main_channel_url": MAIN_CHANNEL_URL,
            },
            "youtube_urls": yt_urls,
            "shorts_urls": shorts_urls,
            "youtube_packages": {
                k: {
                    "title": v.get("title", ""),
                    "srt_url": v.get("srt_url", ""),
                    "thumbnail_url": v.get("thumbnail_url", ""),
                    "local_mp4_path": v.get("local_mp4_path", ""),
                    "total_duration_sec": v.get("total_duration_sec", 0)
                }
                for k, v in yt_pkgs.items()
            },
            "shorts_packages": shorts_pkgs,
        })
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)

    # min7014_deep_knowledge.json에도 숏폼 정보 동기화
    if DEEP_JSON_PATH.exists() and short_by_slug:
        try:
            d_items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
            d_changed = False
            for it in d_items:
                pdf_u = (it.get("pdf") or "").split("#")[0].strip()
                p_slug = pdf_u.split("/")[-1].replace(".pdf", "") if pdf_u else ""
                w_slug = (it.get("url") or "").rstrip("/").split("/")[-1]
                matched_s = p_slug if p_slug in short_by_slug else (w_slug if w_slug in short_by_slug else "")
                if matched_s:
                    s_info = short_by_slug[matched_s]
                    s_urls = s_info["shorts_urls"]
                    s_pkgs = s_info["shorts_packages"]
                    if s_urls.get("ko") and it.get("youtube_short_ko") != s_urls["ko"]:
                        it["youtube_short_ko"] = s_urls["ko"]
                        d_changed = True
                    if s_urls.get("en") and it.get("youtube_short_en") != s_urls["en"]:
                        it["youtube_short_en"] = s_urls["en"]
                        d_changed = True
                    if s_pkgs.get("ko", {}).get("local_mp4_path") and it.get("short_mp4_ko") != s_pkgs["ko"]["local_mp4_path"]:
                        it["short_mp4_ko"] = s_pkgs["ko"]["local_mp4_path"]
                        d_changed = True
                    if s_pkgs.get("en", {}).get("local_mp4_path") and it.get("short_mp4_en") != s_pkgs["en"]["local_mp4_path"]:
                        it["short_mp4_en"] = s_pkgs["en"]["local_mp4_path"]
                        d_changed = True
            if d_changed:
                DEEP_JSON_PATH.write_text(json.dumps(d_items, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as de:
            print(f"[Deep JSON Shorts Sync Notice] {de}")

    vault_path = ROOT_DIR / "video_lectures" / "vault_index.json"
    existing_playlists = {}
    existing_thumbs = []
    if vault_path.exists():
        try:
            old_v = json.loads(vault_path.read_text(encoding="utf-8"))
            existing_playlists = old_v.get("playlists") or {}
            existing_thumbs = old_v.get("applied_custom_thumbnails") or []
        except Exception:
            pass

    vault_index = {
        "vault_channel_name": YOUTUBE_CHANNEL_NAME,
        "vault_channel_handle": YOUTUBE_CHANNEL_HANDLE,
        "vault_channel_id": YOUTUBE_CHANNEL_ID,
        "vault_channel_url": YOUTUBE_CHANNEL_URL,
        "studio_upload_url": YOUTUBE_STUDIO_UPLOAD_URL,
        "rss_feed_url": YOUTUBE_RSS_URL,
        "playlists": existing_playlists,
        "applied_custom_thumbnails": existing_thumbs,
        "channel_settings_optimized": True,
        "total_indexed_topics": len(scripts),
        "vault_entries": {
            s["slug"]: {
                "title": s["title"],
                "title_en": s["title_en"],
                "page_count": s["page_count"],
                "pdf_url": s["pdf_url"],
                "youtube_ko": s["youtube_urls"].get("ko", ""),
                "youtube_en": s["youtube_urls"].get("en", ""),
                "youtube_orig": s["youtube_urls"].get("orig", ""),
                "youtube_short_ko": s.get("shorts_urls", {}).get("ko", ""),
                "youtube_short_en": s.get("shorts_urls", {}).get("en", ""),
                "short_mp4_ko": s.get("shorts_packages", {}).get("ko", {}).get("local_mp4_path", ""),
                "short_mp4_en": s.get("shorts_packages", {}).get("en", {}).get("local_mp4_path", ""),
                "vault_stored": bool(s["youtube_urls"].get("ko") and s["youtube_urls"].get("en")),
            }
            for s in scripts
        },
    }
    vault_path.write_text(json.dumps(vault_index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Catalog & @min7014_ai Video Vault Updated] {CATALOG_PATH} / {vault_path} ({len(scripts)} topics)")


def boost_youtube_channel_popularity():
    """
    [@min7014_ai 유튜브 인기 영상 부스터 (YouTube Algorithm SEO · CTR · Playlist · Interactive Quiz Comments)]
    1) 이미 업로드된 모든 영상의 제목(고클릭률 훅), 설명문(정주행 추천 링크·00:00 챕터·유레카 퀴즈), 20+ 검색 태그를 최신화합니다.
    2) @min7014_ai 채널에 한국어(KO) / 영어(EN) 공식 정주행 재생목록(Playlist)을 생성하고 모든 업로드 영상을 자동 편성합니다.
    3) 각 영상에 시청자 댓글 참여를 유도하는 [오늘의 10초 유레카 퀴즈] 공식 첫 댓글을 자동 게시합니다.
    """
    refresh_all_youtube_metadata_packages()

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    token_file = ROOT_DIR / "youtube_token_min7014_ai.json"
    if not token_file.exists():
        raise RuntimeError("youtube_token_min7014_ai.json not found.")
    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_file.write_text(creds.to_json(), encoding="utf-8")

    youtube = build("youtube", "v3", credentials=creds)

    ko_video_ids = []
    en_video_ids = []

    # 1. 업로드된 전체 영상 메타데이터(제목·설명·태그·언어) 최적화 업데이트 + 유레카 퀴즈 댓글 등록
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        slug = sdoc["slug"]
        yt_urls = sdoc.get("youtube_urls") or {}
        meta_path = YT_PKG_DIR / f"{slug}_youtube_meta.json"
        if not meta_path.exists():
            continue
        meta_all = json.loads(meta_path.read_text(encoding="utf-8"))

        for lc in ["ko", "en"]:
            u = (yt_urls.get(lc) or "").strip()
            if not u or lc not in meta_all:
                continue
            vid_id = u.split("/")[-1].split("?")[0].strip()
            if not vid_id:
                continue
            if lc == "ko":
                ko_video_ids.append((slug, vid_id))
            else:
                en_video_ids.append((slug, vid_id))

            meta = meta_all[lc]
            try:
                youtube.videos().update(
                    part="snippet",
                    body={
                        "id": vid_id,
                        "snippet": {
                            "title": meta["title"],
                            "description": meta["description"],
                            "tags": meta["tags"],
                            "categoryId": meta.get("categoryId", "27"),
                            "defaultLanguage": lc,
                            "defaultAudioLanguage": lc,
                        },
                    },
                ).execute()
                print(f"✅ [SEO & High-CTR Updated ({lc.upper()})] {vid_id} -> {meta['title']}")
            except Exception as e:
                print(f"⚠️ [Video Update Notice ({vid_id})]: {e}")

            # v4.0 CTR 14%+ 커스텀 썸네일 즉시 교체 적용
            thumb_p = YT_PKG_DIR / f"{slug}_{lc}_thumb.png"
            if thumb_p.exists():
                try:
                    from googleapiclient.http import MediaFileUpload
                    youtube.thumbnails().set(
                        videoId=vid_id,
                        media_body=MediaFileUpload(str(thumb_p), mimetype="image/png"),
                    ).execute()
                    print(f"🖼️ [v4.0 Viral Thumbnail Replaced ({lc.upper()})] {vid_id} <- {thumb_p.name}")
                except Exception as te:
                    print(f"⚠️ [Thumbnail Update Notice ({vid_id})]: {te}")

            # 시청자 참여 유도 첫 댓글 (중복 방지 확인)
            quiz_comment = meta.get("quiz_comment") or ""
            if quiz_comment:
                try:
                    existing_comments = youtube.commentThreads().list(
                        part="snippet", videoId=vid_id, maxResults=10
                    ).execute().get("items", [])
                    already_posted = any(
                        "유레카 퀴즈" in c["snippet"]["topLevelComment"]["snippet"].get("textOriginal", "")
                        or "Eureka Quiz" in c["snippet"]["topLevelComment"]["snippet"].get("textOriginal", "")
                        for c in existing_comments
                    )
                    if not already_posted:
                        board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}"
                        full_comment = (
                            f"{quiz_comment}\n\n"
                            f"📌 직접 움직여보는 GeoGebra & 전체 1,111개 수학 설명영상 게시판:\n👉 {board_link}"
                            if lc == "ko"
                            else f"{quiz_comment}\n\n"
                            f"📌 Explore the Interactive GeoGebra & Full 1,111 Math Video Board:\n👉 {board_link}"
                        )
                        youtube.commentThreads().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "videoId": vid_id,
                                    "topLevelComment": {
                                        "snippet": {
                                            "textOriginal": full_comment
                                        }
                                    },
                                }
                            },
                        ).execute()
                        print(f"💬 [Interactive Eureka Quiz Comment Posted ({lc.upper()})] {vid_id}")
                    else:
                        print(f"💬 [Comment Already Active ({lc.upper()})] {vid_id}")
                except Exception as ce:
                    print(f"⚠️ [Comment Notice ({vid_id})]: {ce}")

    # 2. 공식 정주행 재생목록(Playlists) 생성 및 영상 자동 편성
    playlist_specs = {
        "ko": {
            "title": "🔥 [시각적 수학 증명] 보조선 한 줄로 깨치는 기하학 명작 정주행 (1080p) | 민은기 선생님의 수학자료실_AI",
            "desc": (
                "공식 암기 없이 눈으로 보고 직관적으로 깨치는 민은기 선생님의 수학자료실(https://min7014.github.io/) 단계별 시각적 증명 한국어 정주행 시리즈입니다.\n"
                "전체 1,111개 설명영상 게시판: https://min7014.github.io/mathedu/video_board.html"
            ),
            "videos": [vid for _, vid in ko_video_ids],
        },
        "en": {
            "title": "✨ [Visual Math Proofs] Step-by-Step Euclidean Geometry & Fractal Masterclass (1080p) | Min's Math Lab AI",
            "desc": (
                "Step-by-step visual mathematical proofs from Min's Math Lab (https://min7014.github.io/). Watch auxiliary lines and geometric ratios come alive!\n"
                "Full 1,111 Math Video Board: https://min7014.github.io/mathedu/video_board.html"
            ),
            "videos": [vid for _, vid in en_video_ids],
        },
    }

    existing_pls = {}
    try:
        pl_resp = youtube.playlists().list(part="snippet", mine=True, maxResults=50).execute()
        for it in pl_resp.get("items", []):
            existing_pls[it["snippet"]["title"]] = it["id"]
    except Exception as pe:
        print(f"⚠️ [Playlist List Notice]: {pe}")

    saved_playlist_urls = {}
    for lc, pspec in playlist_specs.items():
        pl_id = existing_pls.get(pspec["title"])
        if not pl_id:
            try:
                created = youtube.playlists().insert(
                    part="snippet,status",
                    body={
                        "snippet": {
                            "title": pspec["title"],
                            "description": pspec["desc"],
                            "defaultLanguage": lc,
                        },
                        "status": {"privacyStatus": "public"},
                    },
                ).execute()
                pl_id = created["id"]
                print(f"📂 [Official Playlist Created ({lc.upper()})] https://www.youtube.com/playlist?list={pl_id}")
            except Exception as ce:
                print(f"⚠️ [Playlist Create Notice ({lc})]: {ce}")
                continue
        else:
            print(f"📂 [Official Playlist Found ({lc.upper()})] https://www.youtube.com/playlist?list={pl_id}")

        saved_playlist_urls[lc] = f"https://www.youtube.com/playlist?list={pl_id}"

        # 재생목록 내부 기존 영상 확인 후 누락된 영상 추가
        in_pl = set()
        try:
            pl_items = youtube.playlistItems().list(
                part="snippet", playlistId=pl_id, maxResults=50
            ).execute().get("items", [])
            in_pl = {x["snippet"]["resourceId"]["videoId"] for x in pl_items}
        except Exception:
            in_pl = set()

        for vid_id in pspec["videos"]:
            if vid_id not in in_pl:
                try:
                    youtube.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": pl_id,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": vid_id,
                                },
                            }
                        },
                    ).execute()
                    print(f"  ➕ Added video {vid_id} to {lc.upper()} Playlist ({pl_id})")
                except Exception as ie:
                    print(f"  ⚠️ [Playlist Insert Notice ({pl_id}/{vid_id})]: {ie}")

    vault_path = ROOT_DIR / "video_lectures" / "vault_index.json"
    if vault_path.exists():
        vdata = json.loads(vault_path.read_text(encoding="utf-8"))
        vdata["playlists"] = saved_playlist_urls
        vault_path.write_text(json.dumps(vdata, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ [Vault Index Playlists Saved] {saved_playlist_urls}")

    return saved_playlist_urls


def condense_narration_for_shorts(raw_text, seq_idx, total_seqs, clean_title, viral_hook, lang_code="ko"):
    """
    [숏폼(#Shorts) 전용 55초 이내 무결성 대본 압축기]
    - YouTube Shorts 규격(9:16 세로형, 60초 미만 필수 · 최적 완주율 35~52초)을 100% 충족하도록
      각 하이라이트 장면(총 5장면)의 내레이션을 1~2문장(7~10초 분량)의 핵심 통찰로 압축합니다.
    """
    txt = re.sub(r"\s+", " ", (raw_text or "").strip())
    if seq_idx == 1:
        if lang_code == "ko":
            hook = viral_hook or f"{clean_title}, 공식 암기 없이 눈으로 바로 깨쳐 볼까요?"
            # 첫 문장 또는 핵심 안내 결합
            sents = [s.strip() for s in re.split(r"(?<=[.?!다요죠])\s+", txt) if s.strip()]
            first_core = ""
            for s in sents:
                if "안녕하세요" not in s and "선생님" not in s:
                    first_core = s
                    break
            combined = f"{hook} {first_core}".strip()
            return combined[:95] if len(combined) > 95 else combined
        else:
            hook = viral_hook or f"Can we prove {clean_title} visually in 45 seconds?"
            sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
            first_core = ""
            for s in sents:
                if "Welcome" not in s and "Min's Math Lab" not in s:
                    first_core = s
                    break
            combined = f"{hook} {first_core}".strip()
            return combined[:155] if len(combined) > 155 else combined

    if seq_idx == total_seqs:
        if lang_code == "ko":
            return "보조선과 기하 직관만으로 완벽 증명 완료! 1080p 풀버전 강의와 직접 움직이는 지오지브라는 채널과 설명란 링크에서 바로 체험해 보세요!"
        else:
            return "Visual proof complete! Watch the full 1080p lecture and try the interactive GeoGebra via the link in the description!"

    # 중간 핵심 전개 장면 (2, 3, 4단계): 인사말 제거 후 가장 핵심적인 1~2문장(한국어 85자, 영어 145자 이내) 추출
    if lang_code == "ko":
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
        picked = []
        cur_len = 0
        for s in sents:
            if cur_len + len(s) <= 88 or not picked:
                picked.append(s)
                cur_len += len(s)
            else:
                break
        res = " ".join(picked)
        if len(res) > 92:
            res = res[:90].rsplit(" ", 1)[0] + "."
        return res
    else:
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
        picked = []
        cur_len = 0
        for s in sents:
            if cur_len + len(s) <= 145 or not picked:
                picked.append(s)
                cur_len += len(s)
            else:
                break
        res = " ".join(picked)
        if len(res) > 155:
            res = res[:150].rsplit(" ", 1)[0] + "."
        return res


def build_youtube_short_metadata(sdoc, lang_code, duration_sec):
    """
    [유튜브 숏폼(#Shorts) 전용 고클릭률 제목·설명·태그 메타데이터 패키지 생성]
    """
    slug = sdoc["slug"]
    clean_ko = re.sub(r"\$[^\$]*\$", "", sdoc["title"]).strip()
    clean_en = (sdoc.get("title_en") or clean_ko).strip()
    viral_hooks = sdoc.get("viral_hooks") or {}
    yt_urls = sdoc.get("youtube_urls") or {}
    full_yt = yt_urls.get(lang_code) or yt_urls.get("ko") or "https://www.youtube.com/@min7014_ai"
    board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}"

    if lang_code == "ko":
        hook_ko = (viral_hooks.get("ko") or f"보조선 한 줄의 마법! {clean_ko} 45초 시각적 증명").strip()
        short_title = f"🔥 {hook_ko} | {clean_ko} #Shorts #수학"
        if len(short_title) > 98:
            short_title = f"🔥 {clean_ko} — 45초 시각적 수학 증명 하이라이트 #Shorts #수학"
        desc = (
            f"⚡ [{clean_ko} — {round(duration_sec)}초 숏폼(#Shorts) 시각적 증명 하이라이트]\n"
            f"{hook_ko}\n\n"
            f"🌐 [1초 클릭! 민은기 선생님의 수학홈페이지 무료 실습 & 퀴즈 바로가기]\n"
            f"1️⃣ 방금 본 도형 마우스로 직접 움직여보기 (GeoGebra & 플립북 게시판):\n👉 {board_link}&from=yt_shorts\n"
            f"2️⃣ 5지선다 보기를 가리고 수식 블록 조립! 16,548문항 수능·모평 디딤돌 퀴즈:\n👉 https://min7014.github.io/mathedu/?from=yt_shorts\n"
            f"3️⃣ 오늘의 3분 수학 유레카 (10초 오개념 O/X & 나만의 문제 발명):\n👉 https://min7014.github.io/mathedu/#dailyGrowthFlywheelSection\n"
            f"4️⃣ 수능 수학 100점 만점 3D 보스 레이드 게임 무료 플레이:\n👉 https://min7014.github.io/mathedu/game.html\n"
            f"5️⃣ 민은기 선생님의 수학자료실 본관 (3,400+ 시각 증명):\n👉 https://min7014.github.io/\n\n"
            f"🎬 1080p 전체 단계별 풀버전 설명영상 바로 보기:\n👉 {full_yt}\n"
            f"🔔 민은기 선생님의 수학자료실_AI (@min7014_ai) 구독하기:\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"[ID: {slug}_SHORT_KO]\n"
            f"#Shorts #수학 #기하학 #시각적증명 #{clean_ko.replace(' ', '')} #피타고라스 #보조선 #수능수학 #민은기선생님의수학자료실 #min7014_ai"
        )
        tags = ["Shorts", "유튜브쇼츠", "수학", "기하학", "시각적증명", clean_ko, "민은기선생님의수학자료실", "min7014_ai", "수능수학", "보조선"]
    else:
        hook_en = (viral_hooks.get("en") or f"45s Visual Math Proof: {clean_en}").strip()
        short_title = f"🔥 {hook_en} | {clean_en} #Shorts #Math"
        if len(short_title) > 98:
            short_title = f"🔥 {clean_en} — 45s Visual Math Proof Highlight #Shorts #Math"
        desc = (
            f"⚡ [{clean_en} — {round(duration_sec)}s Visual Math Proof #Shorts]\n"
            f"{hook_en}\n\n"
            f"🎬 Watch Full 1080p Step-by-Step Proof Video:\n👉 {full_yt}\n\n"
            f"📐 Interactive GeoGebra & Full 1,111 Math Video Board:\n👉 {board_link}\n\n"
            f"🔔 Subscribe to Min's Math Lab AI (@min7014_ai):\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"[ID: {slug}_SHORT_EN]\n"
            f"#Shorts #Math #Geometry #VisualProof #MathShorts #ProofWithoutWords #GeoGebra #min7014_ai"
        )
        tags = ["Shorts", "MathShorts", "Math", "Geometry", "VisualProof", clean_en, "MinsMathLab", "min7014_ai", "GeoGebra"]

    return {
        "title": short_title[:100],
        "description": desc,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": lang_code,
        "duration_sec": round(duration_sec, 2),
        "aspect_ratio": "9:16 (1080x1920)",
    }


def render_youtube_short_vertical(slug_key="math20250130001", lang_code="ko"):
    """
    [유튜브 쇼츠(YouTube Shorts · 1080x1920 세로형 40~54초 하이라이트) 자동 제작기]
    - 도입(1페이지) -> 핵심 보조선/전개(중간 3페이지) -> 최종 정리 완성(마지막 페이지)의 핵심 5장면을 추출하고,
      내레이션을 숏폼 전용 초압축 대본으로 구성하여 60초 미만(40~54초) 모바일 세로형(1080x1920) Shorts 영상을 생성합니다.
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        generate_or_update_script(slug_key, target_langs=["ko", "en"])
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    pages = sdoc["pages"]
    n = len(pages)
    if n <= 5:
        picked_indices = list(range(n))
    else:
        picked_indices = sorted(list({0, max(1, n // 4), n // 2, min(n - 2, (3 * n) // 4), n - 1}))

    pdf_bytes = urllib.request.urlopen(sdoc["pdf_url"]).read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    voice_name = GLOBAL_VOICE_MAP.get(lang_code, GLOBAL_VOICE_MAP["en"])["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    shorts_dir = YT_UPLOADS_DIR / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)
    ready_shorts_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai_shorts"
    ready_shorts_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_short_{slug_key}_{lang_code}_"))
    segs = []

    font_top = get_font_for_lang(lang_code, 44, bold=True)
    font_sub = get_font_for_lang(lang_code, 30, bold=True)
    font_cap = get_font_for_lang(lang_code, 34, bold=True)

    clean_title = (
        (sdoc.get("title_en") or sdoc["title"])
        if lang_code == "en"
        else re.sub(r"\$[^\$]*\$", "", sdoc["title"]).strip()
    )
    viral_hooks = sdoc.get("viral_hooks") or {}
    viral_hook = viral_hooks.get(lang_code) or ""
    total_seqs = len(picked_indices)

    try:
        for seq_idx, p_idx in enumerate(picked_indices, 1):
            p_info = pages[p_idx]
            canvas = Image.new("RGB", (1080, 1920), (10, 16, 34))
            draw = ImageDraw.Draw(canvas)

            # 상단 후킹 배너 + 진행률 게이지 바
            draw.rounded_rectangle((44, 58, 1036, 294), radius=28, fill=(23, 37, 84), outline=(56, 189, 248), width=3)
            draw.rounded_rectangle((74, 80, 540, 130), radius=18, fill=(225, 29, 72))
            badge_txt = "⚡ 45초 시각적 증명 #Shorts" if lang_code == "ko" else "⚡ 45s Visual Proof #Shorts"
            draw.text((94, 88), badge_txt, fill=(255, 255, 255), font=font_sub)

            step_label = f"STEP {seq_idx}/{total_seqs}"
            draw.text((845, 88), step_label, fill=(251, 191, 36), font=font_sub)

            title_lines = textwrap.wrap(clean_title, width=20 if lang_code == "ko" else 28)[:2]
            for li, tl in enumerate(title_lines):
                draw.text((78, 146 + li * 54), tl, fill=(255, 255, 255), font=font_top)

            # 상단 진행 바 (Progress Gauge)
            draw.rounded_rectangle((74, 266, 1006, 280), radius=7, fill=(30, 58, 138))
            prog_w = int(932 * (seq_idx / total_seqs))
            draw.rounded_rectangle((74, 266, 74 + max(24, prog_w), 280), radius=7, fill=(56, 189, 248))

            # 하단 초압축 숏폼 내레이션 & 자막 카드
            raw_narr = p_info.get("narrations", {}).get(lang_code) or p_info["explanation_text"]
            short_narration = condense_narration_for_shorts(
                raw_narr, seq_idx, total_seqs, clean_title, viral_hook, lang_code=lang_code
            )

            mp3_p = tmp_dir / f"short_{seq_idx:02d}.mp3"
            seg_p = tmp_dir / f"short_{seq_idx:02d}.mp4"
            comm = edge_tts.Communicate(short_narration, voice_name, rate="+18%")
            asyncio.run(comm.save(str(mp3_p)))
            seg_audio_dur = get_media_duration_seconds(mp3_p, ffprobe_exe)

            # 현재 단계에 해당하는 연속 PDF 플립북 프레임 추출 (최대 6프레임 모션 애니메이션)
            f_range = p_info.get("frame_range")
            if seq_idx == 1 and len(doc) >= 3:
                # [v4.0 Climax-First Hook]: 첫 장면은 완성된 클라이맥스 도형 프레임을 먼저 보여준 뒤 1~2페이지로 진입!
                doc_frames = [max(0, len(doc) - 2), 0, min(len(doc) - 1, 2)]
            elif f_range and f_range[1] > f_range[0]:
                doc_frames = list(range(max(0, int(f_range[0]) - 1), min(len(doc), int(f_range[1]))))
            else:
                prev_doc_p = 0 if seq_idx == 1 else max(0, pages[picked_indices[seq_idx - 2]]["page"] - 1)
                curr_doc_p = min(len(doc) - 1, p_info["page"] - 1)
                doc_frames = list(range(prev_doc_p, curr_doc_p + 1)) if curr_doc_p > prev_doc_p else [curr_doc_p]
            if len(doc_frames) > 6:
                step_df = (len(doc_frames) - 1) / 5.0
                doc_frames = sorted(list({doc_frames[int(round(k * step_df))] for k in range(6)}))

            draw.rounded_rectangle((44, 1345, 1036, 1795), radius=28, fill=(15, 23, 42), outline=(225, 29, 72), width=3)
            step_chip = (
                f"🔥 핵심 단계 {seq_idx}/{total_seqs} · 동적 플립북 (p.{doc_frames[0]+1}▸{doc_frames[-1]+1}/{len(doc)})"
                if lang_code == "ko"
                else f"🔥 KEY INSIGHT {seq_idx}/{total_seqs} · Flipbook Motion (p.{doc_frames[0]+1}▸{doc_frames[-1]+1}/{len(doc)})"
            )
            draw.text((78, 1375), step_chip, fill=(251, 191, 36), font=font_sub)
            cap_lines = textwrap.wrap(short_narration, width=22 if lang_code == "ko" else 34)[:5]
            for ci, cl in enumerate(cap_lines):
                draw.text((78, 1438 + ci * 60), cl, fill=(248, 250, 252), font=font_cap)

            draw.rounded_rectangle((44, 1810, 1036, 1892), radius=20, fill=(30, 58, 138), outline=(251, 191, 36), width=3)
            cta_short_txt = (
                "👆 설명란·댓글 링크 ➔ 무료 GeoGebra 실습 & 기출 도전! (min7014.github.io/mathedu)"
                if lang_code == "ko"
                else "👆 Tap Description Link ➔ Free GeoGebra & Math Quizzes! (min7014.github.io/mathedu)"
            )
            draw.text((68, 1834), cta_short_txt, fill=(254, 240, 138), font=get_font_for_lang("ko", 24, bold=True))

            # 각 PDF 프레임을 1080x1920 캔버스 중앙에 합성하여 모션 시퀀스 생성
            per_f_dur = max(0.22, seg_audio_dur / max(1, len(doc_frames)))
            f_lines = []
            last_fp = None
            for fi_idx, doc_f_i in enumerate(doc_frames):
                frame_canvas = canvas.copy()
                f_draw = ImageDraw.Draw(frame_canvas)
                pix = doc[doc_f_i].get_pixmap(dpi=260)
                slide_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                sw, sh = slide_pil.size
                scale = min(984 / sw, 980 / sh)
                nw, nh = int(sw * scale), int(sh * scale)
                resized = slide_pil.resize((nw, nh), Image.Resampling.LANCZOS)
                ox = (1080 - nw) // 2
                oy = 326 + (980 - nh) // 2
                f_draw.rounded_rectangle((ox - 12, oy - 12, ox + nw + 12, oy + nh + 12), radius=22, fill=(255, 255, 255), outline=(251, 191, 36), width=3)
                frame_canvas.paste(resized, (ox, oy))
                # 마지막 프레임에서 스포트라이트 박스 표시
                bbox = p_info.get("diff_bbox")
                if bbox and fi_idx == len(doc_frames) - 1 and doc_f_i > 0:
                    bx0 = max(ox + 4, ox + int(bbox[0] * nw) - 10)
                    by0 = max(oy + 4, oy + int(bbox[1] * nh) - 10)
                    bx1 = min(ox + nw - 4, ox + int(bbox[2] * nw) + 10)
                    by1 = min(oy + nh - 4, oy + int(bbox[3] * nh) + 10)
                    if (bx1 - bx0) > 24 and (by1 - by0) > 24:
                        f_draw.rounded_rectangle((bx0, by0, bx1, by1), radius=10, outline=(225, 29, 72), width=5)
                fp = tmp_dir / f"short_{seq_idx:02d}_f{fi_idx:02d}.png"
                frame_canvas.save(fp)
                f_lines.append(f"file '{fp.as_posix()}'")
                f_lines.append(f"duration {per_f_dur:.4f}")
                last_fp = fp
            if last_fp:
                f_lines.append(f"file '{last_fp.as_posix()}'")
            f_txt = tmp_dir / f"short_fconcat_{seq_idx:02d}.txt"
            f_txt.write_text("\n".join(f_lines), encoding="utf-8")

            chime_wav = ensure_harmonic_chime_wav()
            use_chime = seq_idx in (1, total_seqs)
            cmd = [
                ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", str(f_txt),
                "-i", str(mp3_p),
            ]
            if use_chime:
                cmd.extend([
                    "-i", str(chime_wav),
                    "-filter_complex",
                    "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                    "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[c];"
                    "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                    "-map", "0:v", "-map", "[aout]",
                ])
            else:
                cmd.extend(["-map", "0:v", "-map", "1:a"])
            cmd.extend([
                "-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-shortest",
                str(seg_p),
            ])
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segs.append(seg_p)

        concat_p = tmp_dir / "concat.txt"
        concat_p.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
        raw_short = tmp_dir / f"raw_short_{slug_key}_{lang_code}.mp4"
        out_short = shorts_dir / f"{slug_key}_short_{lang_code}.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_p), "-c", "copy", str(raw_short)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        ambient_wav = ensure_ambient_pad_wav()
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-i", str(raw_short),
                "-stream_loop", "-1", "-i", str(ambient_wav),
                "-filter_complex",
                "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[bgm];"
                "[v][bgm]amix=inputs=2:duration=first:dropout_transition=1[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                str(out_short),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        dur = get_media_duration_seconds(out_short, ffprobe_exe)
        # 만약 58초를 초과하면 자동으로 오디오/비디오 배속(atempo/setpts)을 미세 조정하여 54초 이내로 무결성 보장
        if dur >= 58.0:
            speed_factor = round((dur / 53.0), 3)
            trimmed_short = tmp_dir / f"{slug_key}_short_{lang_code}_fast.mp4"
            subprocess.run(
                [
                    ffmpeg_exe, "-y", "-i", str(out_short),
                    "-filter_complex", f"[0:v]setpts=PTS/{speed_factor}[v];[0:a]atempo={min(2.0, speed_factor)}[a]",
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(trimmed_short),
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            shutil.copyfile(trimmed_short, out_short)
            dur = get_media_duration_seconds(out_short, ffprobe_exe)

        # 숏폼 메타데이터 및 대본 JSON 업데이트
        short_meta = build_youtube_short_metadata(sdoc, lang_code, dur)
        short_meta_path = YT_PKG_DIR / f"{slug_key}_shorts_meta.json"
        existing_smeta = {}
        if short_meta_path.exists():
            try:
                existing_smeta = json.loads(short_meta_path.read_text(encoding="utf-8"))
            except Exception:
                existing_smeta = {}
        existing_smeta[lang_code] = short_meta
        short_meta_path.write_text(json.dumps(existing_smeta, ensure_ascii=False, indent=2), encoding="utf-8")

        if "shorts_packages" not in sdoc or not isinstance(sdoc["shorts_packages"], dict):
            sdoc["shorts_packages"] = {}
        if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
            sdoc["shorts_urls"] = {"ko": "", "en": ""}
        pub_short_dir = ROOT_DIR / "video_lectures" / "shorts"
        pub_short_dir.mkdir(parents=True, exist_ok=True)
        pub_short_path = pub_short_dir / f"{slug_key}_short_{lang_code}.mp4"
        shutil.copyfile(out_short, pub_short_path)
        sdoc["shorts_packages"][lang_code] = {
            "title": short_meta["title"],
            "local_mp4_path": f"video_lectures/shorts/{slug_key}_short_{lang_code}.mp4",
            "duration_sec": round(dur, 2),
            "aspect_ratio": "9:16 (1080x1920)",
        }
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

        # 1-Drag 업로드 폴더에도 자동 복사
        safe_t = re.sub(r'[\\/:*?"<>|]', " ", short_meta["title"]).strip()
        ready_dst = ready_shorts_dir / f"{safe_t[:75]} [{slug_key}_SHORT_{lang_code.upper()}].mp4"
        shutil.copyfile(out_short, ready_dst)

        update_video_catalog()
        print(f"📱 [YouTube Shorts 1080x1920 (<58s Verified) Generated] {out_short} ({round(dur, 1)}s) -> {short_meta['title']}")
        return out_short
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def upload_short_to_youtube(slug_key, langs=("ko", "en"), privacy="public"):
    """
    [@min7014_ai 유튜브 숏폼(#Shorts) 자동 업로더 (YouTube Data API v3)]
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    token_file = ROOT_DIR / "youtube_token_min7014_ai.json"
    if not token_file.exists():
        raise RuntimeError("youtube_token_min7014_ai.json not found.")
    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_file.write_text(creds.to_json(), encoding="utf-8")

    youtube = build("youtube", "v3", credentials=creds)
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        generate_or_update_script(slug_key, target_langs=["ko", "en"])

    uploaded_shorts = {}
    for lc in langs:
        short_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug_key}_short_{lc}.mp4"
        short_meta_path = YT_PKG_DIR / f"{slug_key}_shorts_meta.json"
        if not short_mp4.exists() or not short_meta_path.exists():
            render_youtube_short_vertical(slug_key, lang_code=lc)

        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        existing_short_url = (sdoc.get("shorts_urls") or {}).get(lc, "").strip()
        if existing_short_url:
            uploaded_shorts[lc] = existing_short_url
            print(f"📱 [Shorts Already Uploaded ({lc.upper()})] {existing_short_url}")
            continue

        smeta_all = json.loads(short_meta_path.read_text(encoding="utf-8"))
        if lc not in smeta_all:
            render_youtube_short_vertical(slug_key, lang_code=lc)
            smeta_all = json.loads(short_meta_path.read_text(encoding="utf-8"))
        smeta = smeta_all[lc]

        body = {
            "snippet": {
                "title": smeta["title"],
                "description": smeta["description"],
                "tags": smeta["tags"],
                "categoryId": smeta.get("categoryId", "27"),
                "defaultLanguage": lc,
                "defaultAudioLanguage": lc,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            },
        }
        try:
            media = MediaFileUpload(str(short_mp4), chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid_id = resp["id"]
            short_url = f"https://youtube.com/shorts/{vid_id}"
            uploaded_shorts[lc] = short_url
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
                sdoc["shorts_urls"] = {"ko": "", "en": ""}
            sdoc["shorts_urls"][lc] = short_url
            script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            update_video_catalog()
            print(f"🚀 [YouTube #Shorts Uploaded ({lc.upper()})] {short_url}")
        except Exception as e:
            err_s = str(e)
            print(f"  ⚠️ [YouTube #Shorts Upload Notice ({slug_key}/{lc})]: {e}")
            if "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s:
                upload_short_to_youtube._backoff_until = time.time() + 1800
            break
    return uploaded_shorts


def build_all_shorts(upload=False, privacy="public"):
    """
    대본이 생성된 모든 대표 주제(7개 주제 × 한국어/영어 = 14개 숏폼)의 1080x1920 세로형 #Shorts 마스터 MP4를 일괄 제작합니다.
    """
    results = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        slug = sp.stem
        for lc in ["ko", "en"]:
            out_p = render_youtube_short_vertical(slug, lang_code=lc)
            results.append(str(out_p))
        if upload:
            upload_short_to_youtube(slug, langs=("ko", "en"), privacy=privacy)
    update_video_catalog()
    return results


def get_next_unrendered_topic_slug(failed_slugs=None):
    """
    min7014_deep_knowledge.json의 847개 PDF 주제 중 아직 1080p 본편(_ko/_en.mp4) 또는 9:16 숏폼(_short_ko/_short_en.mp4)이
    제작되지 않은 다음 주제를 우선순위에 따라 반환합니다.
    """
    failed_slugs = failed_slugs or set()
    flagship_priority = [
        "2022051507", "2022042501", "2022101601", "2022101602", "2022101603",
        "2023081301", "2024122501", "2024120301", "2025012801", "2025012601",
    ]
    candidates = list(flagship_priority)
    if DEEP_JSON_PATH.exists():
        try:
            items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
            for it in items:
                pdf_u = (it.get("pdf") or "").split("#")[0].strip()
                if not pdf_u or not pdf_u.lower().endswith(".pdf"):
                    continue
                s = pdf_u.split("/")[-1].replace(".pdf", "").strip()
                if s and s not in candidates:
                    candidates.append(s)
        except Exception:
            pass

    for slug in candidates:
        if slug in failed_slugs:
            continue
        sp = SCRIPTS_DIR / f"{slug}.json"
        has_yt_both = False
        if sp.exists():
            try:
                sdoc = json.loads(sp.read_text(encoding="utf-8"))
                yt_u = sdoc.get("youtube_urls") or {}
                has_yt_both = bool(yt_u.get("ko") and yt_u.get("en"))
            except Exception:
                pass
        mp4_ko = YT_UPLOADS_DIR / slug / f"{slug}_ko.mp4"
        mp4_en = YT_UPLOADS_DIR / slug / f"{slug}_en.mp4"
        sh_ko = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_ko.mp4"
        sh_en = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_en.mp4"
        need_1080p = (not has_yt_both) and (not mp4_ko.exists() or not mp4_en.exists())
        need_shorts = (not sh_ko.exists() or not sh_en.exists())
        if need_1080p or need_shorts:
            return slug
    return None


def run_shorts_and_video_upload_daemon(open_studio_now=False):
    """
    [@min7014_ai 숏폼(#Shorts) & 본편 무인 업로드·동기화 데몬]
    1) 즉시 YouTube Studio 업로드 창과 14개 숏폼 폴더(ready_for_min7014_ai_shorts)를 열어,
       사용자가 마우스로 드래그 앤 드롭하거나 3단계 고급 기능을 켜면 즉시 감지합니다.
    2) 채널에 새 숏폼/영상이 올라오는 즉시 API(videos.update)로 설명문·태그·유레카 댓글을 자동 완성하고
       video_board.html에 링크를 실시간 등록 및 Git Push 합니다.
    3) 동시에 롤링 24시간 업로드 제한이 풀리는 즉시 대기 중인 14개 숏폼과 미업로드 본편을 API로 자동 업로드합니다.
    """
    import time
    import webbrowser
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    ready_shorts_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai_shorts"
    if open_studio_now:
        try:
            webbrowser.open(YOUTUBE_STUDIO_UPLOAD_URL)
            if os.name == "nt" and ready_shorts_dir.exists():
                os.startfile(str(ready_shorts_dir))
        except Exception:
            pass

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    token_file = ROOT_DIR / "youtube_token_min7014_ai.json"
    uploads_playlist_id = "UU" + YOUTUBE_CHANNEL_ID[2:]  # UUSlqQfOEtRfJuMPyGMLgFYA

    print("=" * 76, flush=True)
    print("🤖 [@min7014_ai 숏폼(#Shorts) 14편 자동 업로드 & 실시간 감지 데몬 가동 중]", flush=True)
    print(f"📂 숏폼 마스터 폴더: {ready_shorts_dir}", flush=True)
    print(f"📺 YouTube Studio: {YOUTUBE_STUDIO_UPLOAD_URL}", flush=True)
    print("=" * 76, flush=True)

    last_api_upload_try = 0.0
    enriched_video_ids = set()

    while True:
        try:
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
            if not creds.valid and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                token_file.write_text(creds.to_json(), encoding="utf-8")
            youtube = build("youtube", "v3", credentials=creds)

            # 1) 채널 업로드 재생목록(UUSlqQfOEtRfJuMPyGMLgFYA) 조회하여 새로 올라온 숏폼/본편 즉시 감지 & 메타데이터 완성
            pl_items = youtube.playlistItems().list(
                part="snippet", playlistId=uploads_playlist_id, maxResults=50
            ).execute().get("items", [])

            any_new_bound = False
            for item in pl_items:
                vid_id = item["snippet"]["resourceId"]["videoId"]
                v_title = item["snippet"].get("title", "")
                v_desc = item["snippet"].get("description", "")
                blob = f"{v_title}\n{v_desc}"

                # [slug_SHORT_KO] / [slug_SHORT_EN] / [slug_KO] / [slug_EN] 태그 자동 매칭
                m_short = re.search(r"\[([A-Za-z0-9_]+)_SHORT_(KO|EN)\]", blob, re.IGNORECASE)
                if m_short and vid_id not in enriched_video_ids:
                    s_slug = m_short.group(1)
                    s_lc = m_short.group(2).lower()
                    sp = SCRIPTS_DIR / f"{s_slug}.json"
                    smeta_p = YT_PKG_DIR / f"{s_slug}_shorts_meta.json"
                    if sp.exists() and smeta_p.exists():
                        sdoc = json.loads(sp.read_text(encoding="utf-8"))
                        smeta = json.loads(smeta_p.read_text(encoding="utf-8")).get(s_lc)
                        if smeta:
                            try:
                                youtube.videos().update(
                                    part="snippet",
                                    body={
                                        "id": vid_id,
                                        "snippet": {
                                            "title": smeta["title"],
                                            "description": smeta["description"],
                                            "tags": smeta["tags"],
                                            "categoryId": "27",
                                            "defaultLanguage": s_lc,
                                            "defaultAudioLanguage": s_lc,
                                        },
                                    },
                                ).execute()
                                print(f"✨ [Shorts Metadata Auto-Enriched ({s_lc.upper()})] https://youtube.com/shorts/{vid_id}", flush=True)
                            except Exception as ue:
                                print(f"  [Shorts Update Notice ({vid_id})]: {ue}", flush=True)
                        if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
                            sdoc["shorts_urls"] = {"ko": "", "en": ""}
                        short_url = f"https://youtube.com/shorts/{vid_id}"
                        if sdoc["shorts_urls"].get(s_lc) != short_url:
                            sdoc["shorts_urls"][s_lc] = short_url
                            sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                            any_new_bound = True
                        enriched_video_ids.add(vid_id)

            if any_new_bound:
                update_video_catalog()
                subprocess.run(["git", "add", "video_lectures/", "assets/min7014_deep_knowledge.json"], check=False)
                subprocess.run(["git", "commit", "-m", "chore(shorts): auto-bind uploaded @min7014_ai YouTube Shorts URLs"], check=False)
                subprocess.run(["git", "push", "origin", "main"], check=False)
                print("✅ [Git Auto-Push Complete] Newly uploaded #Shorts bound to video_board.html!", flush=True)

            # 2) 10분마다 API 직접 업로드 재시도 (롤링 24시간 한도 해제 시 즉시 숏폼 & 본편 자동 업로드)
            now_ts = time.time()
            if now_ts - last_api_upload_try >= 300:
                last_api_upload_try = now_ts
                # [Priority 1] 5대 대표 #Shorts 우선 업로드 보장
                priority_5_shorts = ["math20250130001", "2017090101", "2014111902", "2014111901", "2025020101"]
                quota_blocked = False
                for p_slug in priority_5_shorts:
                    sp_p = SCRIPTS_DIR / f"{p_slug}.json"
                    if not sp_p.exists():
                        continue
                    sdoc_p = json.loads(sp_p.read_text(encoding="utf-8"))
                    s_urls_p = sdoc_p.get("shorts_urls") or {}
                    if not s_urls_p.get("ko"):
                        res_p = upload_short_to_youtube(p_slug, langs=("ko",), privacy="public")
                        if not res_p:
                            quota_blocked = True
                            break
                        else:
                            subprocess.run(["git", "add", "video_lectures/", "assets/min7014_deep_knowledge.json"], check=False)
                            subprocess.run(["git", "commit", "-m", f"chore(shorts): auto-upload {p_slug} #Shorts to @min7014_ai"], check=False)
                            subprocess.run(["git", "push", "origin", "main"], check=False)
                if not quota_blocked:
                    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
                        sdoc = json.loads(sp.read_text(encoding="utf-8"))
                        s_urls = sdoc.get("shorts_urls") or {}
                        if not s_urls.get("ko") or not s_urls.get("en"):
                            res = upload_short_to_youtube(sdoc["slug"], langs=("ko", "en"), privacy="public")
                            if not res:
                                break
                            else:
                                subprocess.run(["git", "add", "video_lectures/", "assets/min7014_deep_knowledge.json"], check=False)
                                subprocess.run(["git", "commit", "-m", f"chore(shorts): auto-upload {sdoc['slug']} #Shorts to @min7014_ai"], check=False)
                                subprocess.run(["git", "push", "origin", "main"], check=False)
                        yt_urls = sdoc.get("youtube_urls") or {}
                        if not yt_urls.get("ko") or not yt_urls.get("en"):
                            res_v = upload_slug_to_youtube(sdoc["slug"], langs=("ko", "en"), privacy="public", method="api")
                            if not res_v:
                                break

            # 3) 업로드 대기 중에도 쉬지 않고 min7014.github.io 다음 주제의 1080p 설명영상(KO/EN) + 9:16 숏폼(KO/EN) 연속 자동 제작!
            if not hasattr(run_shorts_and_video_upload_daemon, "_failed_slugs"):
                run_shorts_and_video_upload_daemon._failed_slugs = set()
            next_slug = get_next_unrendered_topic_slug(run_shorts_and_video_upload_daemon._failed_slugs)
            if next_slug:
                print(f"🎬 [Continuous Factory] 다음 주제 1080p 설명영상 + 9:16 #Shorts 자동 제작 시작: {next_slug}", flush=True)
                try:
                    generate_or_update_script(next_slug, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
                    for lc in ["ko", "en"]:
                        mp4_p = YT_UPLOADS_DIR / next_slug / f"{next_slug}_{lc}.mp4"
                        if not mp4_p.exists():
                            render_multilingual_video(next_slug, lang_code=lc)
                        sh_p = YT_UPLOADS_DIR / "shorts" / f"{next_slug}_short_{lc}.mp4"
                        if not sh_p.exists():
                            render_youtube_short_vertical(next_slug, lang_code=lc)
                    update_video_catalog()
                    try:
                        import mathteacher
                        import mathedu_foundation_daemon as fdaemon
                        mathteacher.expand_pedagogy_from_min7014_vault(max_add_per_category=2)
                        fdaemon.mine_next_pedagogy_item_from_deep_knowledge()
                        fdaemon.sync_pedagogy_counts_to_index_html()
                        fdaemon.write_daemon_heartbeat(last_completed_slug=next_slug)
                    except Exception as pe_err:
                        print(f"[Pedagogy Sync Notice] {pe_err}", flush=True)
                    subprocess.run(["git", "add", "video_lectures/catalog.json", "video_lectures/vault_index.json", "video_lectures/scripts/", "video_lectures/youtube_packages/", "video_lectures/shorts/", "assets/min7014_deep_knowledge.json", "assets/mathteacher_pedagogy_engine.json", "index.html"], check=False)
                    subprocess.run(["git", "commit", "-m", f"chore(foundation): continuous v4.0 video/shorts & mathteacher pedagogy evolution ({next_slug})"], check=False)
                    subprocess.run(["git", "push", "origin", "main"], check=False)
                    print(f"✅ [Continuous Factory & Pedagogy Evolution Complete] {next_slug} (1080p KO/EN + #Shorts KO/EN + 수학교육 모듈 동기화 완료!)", flush=True)
                except Exception as prod_err:
                    print(f"⚠️ [Continuous Factory Skip ({next_slug})]: {prod_err}", flush=True)
                    run_shorts_and_video_upload_daemon._failed_slugs.add(next_slug)
        except Exception as de:
            print(f"[Daemon Notice] {de}", flush=True)

        time.sleep(10.0)


def generate_channel_banner_2560x1440():
    """
    [YouTube 공식 채널 배너(2560x1440, Safe Area 1546x423) 아트워크 자동 생성]
    - TV(2560x1440), 데스크톱(2560x423), 태블릿(1855x423), 모바일(1546x423) 모든 기기에서
      핵심 채널 타이틀과 기하 증명 카드가 잘리지 않고 선명하게 보이도록 작도합니다.
    """
    out_path = YT_PKG_DIR / "min7014_ai_channel_banner_2560x1440.png"
    W, H = 2560, 1440
    img = Image.new("RGB", (W, H), (10, 18, 38))
    draw = ImageDraw.Draw(img)

    # 배경 기하 격자 및 황금비 동심원 아트워크
    for gx in range(0, W, 128):
        draw.line([(gx, 0), (gx, H)], fill=(18, 32, 64), width=2)
    for gy in range(0, H, 128):
        draw.line([(0, gy), (W, gy)], fill=(18, 32, 64), width=2)

    for rad in [280, 450, 680, 920]:
        draw.ellipse((W // 2 - rad, H // 2 - rad, W // 2 + rad, H // 2 + rad), outline=(24, 48, 92), width=3)

    # 데스크톱/모바일 안전 영역(Safe Zone: y=508..931, x=507..2053) 강조 카드
    draw.rectangle((0, 500, W, 940), fill=(15, 23, 42))
    draw.line([(0, 500), (W, 500)], fill=(56, 189, 248), width=4)
    draw.line([(0, 940), (W, 940)], fill=(225, 29, 72), width=4)

    # 좌·우측에 실제 대표 시각 증명 썸네일 카드 배치 (Safe Area 내부 좌우 날개)
    thumb_left = YT_PKG_DIR / "math20250130001_ko_thumb.png"
    thumb_right = YT_PKG_DIR / "2017090101_ko_thumb.png"
    if thumb_left.exists():
        try:
            tl = Image.open(thumb_left).convert("RGB").resize((320, 180), Image.Resampling.LANCZOS)
            draw.rounded_rectangle((526, 624, 854, 812), radius=14, fill=(56, 189, 248))
            img.paste(tl, (530, 628))
        except Exception:
            pass
    if thumb_right.exists():
        try:
            tr = Image.open(thumb_right).convert("RGB").resize((320, 180), Image.Resampling.LANCZOS)
            draw.rounded_rectangle((1706, 624, 2034, 812), radius=14, fill=(225, 29, 72))
            img.paste(tr, (1710, 628))
        except Exception:
            pass

    f_badge = get_font_for_lang("en", 26, bold=True)
    f_title = get_font_for_lang("ko", 54, bold=True)
    f_sub = get_font_for_lang("en", 30, bold=True)
    f_info = get_font_for_lang("ko", 26, bold=True)

    # 중앙 안전 영역(x=880..1680) 핵심 타이포그래피
    draw.rounded_rectangle((900, 538, 1660, 588), radius=24, fill=(225, 29, 72))
    draw.text((932, 548), "🤖 VISUAL MATH PROOF VAULT · @min7014_ai", fill=(255, 255, 255), font=f_badge)

    draw.text((895, 612), "민은기 선생님의 수학자료실_AI", fill=(255, 255, 255), font=f_title)
    draw.text((895, 688), "Min's Math Lab AI · 1080p Visual Proofs", fill=(56, 189, 248), font=f_sub)
    draw.text((895, 742), "📐 눈으로 깨치는 단계별 기하·대수·미적분 증명 (KO / EN)", fill=(251, 191, 36), font=f_info)
    draw.text((895, 786), "🌐 https://min7014.github.io/ · 1,111+ Math Topics", fill=(203, 213, 225), font=f_info)

    img.save(out_path, format="PNG", optimize=True)
    print(f"🖼️ [Channel Banner 2560x1440 Generated] {out_path} ({out_path.stat().st_size // 1024} KB)")
    return out_path


def generate_channel_watermark_150x150():
    """
    [영상 우측 하단 상시 구독 워터마크(150x150 PNG) 자동 생성]
    """
    out_path = YT_PKG_DIR / "min7014_ai_watermark_150x150.png"
    img = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((6, 6, 144, 144), radius=28, fill=(225, 29, 72, 235), outline=(255, 255, 255, 255), width=4)
    f_top = get_font_for_lang("en", 22, bold=True)
    f_mid = get_font_for_lang("ko", 28, bold=True)
    f_bot = get_font_for_lang("en", 16, bold=True)

    draw.text((26, 20), "📐 MATH", fill=(254, 240, 138, 255), font=f_top)
    draw.text((22, 54), "구독하기", fill=(255, 255, 255, 255), font=f_mid)
    draw.text((16, 100), "@min7014_ai", fill=(224, 242, 254, 255), font=f_bot)

    img.save(out_path, format="PNG")
    print(f"💧 [Channel Subscribe Watermark 150x150 Generated] {out_path}")
    return out_path


def optimize_youtube_channel_settings():
    """
    [@min7014_ai 유튜브 채널 내부 설정 전수 최적화 (YouTube Data API v3)]
    1) 채널 브랜딩(채널 설명문, 핵심 검색 키워드 25+, 국가 KR, 기본 언어 ko, 비구독자 대표 예고편 영상) 설정
    2) 전 세계 8개국어(ko, en, ja, zh-CN, es, fr, de, vi) 다국어 채널명·채널 설명(Localizations) 등록
    3) 2560x1440 커스텀 채널 배너 아트 업로드 및 적용 (channelBanners.insert)
    4) 전 영상 우측 하단 [구독하기] 인비디오 워터마크 적용 (watermarks.set)
    5) 채널 홈 화면 섹션 레이아웃(한국어 정주행 재생목록, 영어 정주행 재생목록, 인기 업로드, 최신 업로드, 본 채널 @min7014 연계) 구성
    6) 업로드된 10개 전체 영상에 1280x720 HD 커스텀 썸네일 일괄 적용 (thumbnails.set)
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    token_file = ROOT_DIR / "youtube_token_min7014_ai.json"
    if not token_file.exists():
        raise RuntimeError("youtube_token_min7014_ai.json not found.")
    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_file.write_text(creds.to_json(), encoding="utf-8")

    youtube = build("youtube", "v3", credentials=creds)

    # 1. 커스텀 채널 배너(2560x1440) 생성 및 업로드
    banner_url = None
    try:
        banner_path = generate_channel_banner_2560x1440()
        b_resp = youtube.channelBanners().insert(
            media_body=MediaFileUpload(str(banner_path), mimetype="image/png", resumable=True)
        ).execute()
        banner_url = b_resp.get("url")
        print(f"✅ [Channel Banner Uploaded] {banner_url}")
    except Exception as e:
        print(f"⚠️ [Channel Banner Upload Notice]: {e}")

    # 2. 채널 내부 브랜딩·키워드·대표 예고편·8개국어 다국어 프로필 업데이트
    ch_desc_ko = (
        "📐 [민은기 선생님의 수학자료실_AI (@min7014_ai)]\n"
        "공식 암기 없이 눈으로 보고 직관적으로 깨치는 1080p 단계별 시각적 수학 증명(Visual Math Proof) 공식 AI 채널입니다.\n"
        "민은기 선생님의 수학자료실(https://min7014.github.io/)의 3,400+ 동적 기하(GeoGebra)와 866개 단계별 플립북 증명 PDF를 한국어(KO)·영어(EN) 강의로 제공합니다.\n\n"
        "📋 전체 1,111개 수학 설명영상 게시판: https://min7014.github.io/mathedu/video_board.html\n"
        "🎙️ 20개국어 AI 강의 스튜디오: https://min7014.github.io/mathedu/video_studio.html\n"
        "🌐 수학자료실 본관: https://min7014.github.io/\n"
        "📺 본 채널(@min7014): https://www.youtube.com/@min7014\n\n"
        "✨ [Min's Math Lab AI — Step-by-Step Visual Math Proofs]\n"
        "Discover why Euclidean geometry, calculus, and algebra theorems hold true through step-by-step 1080p visual flipbook proofs and interactive GeoGebra applets!"
    )
    ch_keywords = (
        '수학 기하학 "시각적 증명" "민은기 선생님의 수학자료실" min7014 min7014_ai '
        '"피타고라스 정리" "메넬라우스의 정리" "체바의 정리" "수능 수학" "중등 기하" '
        '"고등 수학" "영재고 수학" GeoGebra 알지오매스 "Visual Proof" "Geometry Proof" '
        'Mathematics "Euclidean Geometry" "Proof Without Words" mathedu'
    )

    localizations = {
        "ko": {
            "title": "민은기 선생님의 수학자료실_AI",
            "description": ch_desc_ko,
        },
        "en": {
            "title": "Min's Math Lab AI (@min7014_ai)",
            "description": (
                "📐 Welcome to Min's Math Lab AI (@min7014_ai) — Official 1080p Step-by-Step Visual Mathematical Proofs Channel!\n"
                "We transform 3,400+ interactive GeoGebra geometry constructions and 866 step-by-step flipbook proof PDFs from https://min7014.github.io/ into crystal-clear visual lectures.\n\n"
                "📋 Full 1,111 Math Video Board: https://min7014.github.io/mathedu/video_board.html\n"
                "🎙️ 20+ Language AI Lecture Studio: https://min7014.github.io/mathedu/video_studio.html\n"
                "📺 Main Channel (@min7014): https://www.youtube.com/@min7014"
            ),
        },
        "ja": {
            "title": "ミン・ウンギ先生の数学資料室_AI (@min7014_ai)",
            "description": "公式の暗記ではなく、目で見て直感的に理解するステップバイステップの視覚的数学証明チャンネルです。https://min7014.github.io/mathedu/video_board.html",
        },
        "zh-CN": {
            "title": "闵恩基老师的数学资料室_AI (@min7014_ai)",
            "description": "无需死记硬背公式，通过分步翻页视觉动画直观理解欧几里得几何与数学定理证明！https://min7014.github.io/mathedu/video_board.html",
        },
        "es": {
            "title": "Laboratorio de Matemáticas de Min AI (@min7014_ai)",
            "description": "¡Demostraciones matemáticas visuales paso a paso en 1080p con GeoGebra y flipbooks interactivos! https://min7014.github.io/mathedu/video_board.html",
        },
        "fr": {
            "title": "Laboratoire de Maths de Min AI (@min7014_ai)",
            "description": "Preuves mathématiques visuelles étape par étape en 1080p (Géométrie euclidienne, Pythagore, Ceva, Ménélaüs). https://min7014.github.io/mathedu/video_board.html",
        },
        "de": {
            "title": "Mins Mathe-Labor AI (@min7014_ai)",
            "description": "Visuelle mathematische Beweise Schritt für Schritt in 1080p verstehen! https://min7014.github.io/mathedu/video_board.html",
        },
        "vi": {
            "title": "Phòng Thí Nghiệm Toán Học Min AI (@min7014_ai)",
            "description": "Chứng minh toán học trực quan từng bước chất lượng 1080p kết hợp GeoGebra! https://min7014.github.io/mathedu/video_board.html",
        },
    }

    branding_only_body = {
        "id": YOUTUBE_CHANNEL_ID,
        "brandingSettings": {
            "channel": {
                "title": "민은기 선생님의 수학자료실_AI",
                "description": ch_desc_ko,
                "keywords": ch_keywords,
                "defaultLanguage": "ko",
                "country": "KR",
                "unsubscribedTrailer": "bQO7fnT6aDU",
            }
        },
    }
    if banner_url:
        branding_only_body["brandingSettings"]["image"] = {"bannerExternalUrl": banner_url}

    try:
        youtube.channels().update(
            part="brandingSettings",
            body=branding_only_body,
        ).execute()
        print("✅ [Channel Branding, Keywords, Country(KR), Trailer(bQO7fnT6aDU) & Banner Applied!]")
    except Exception as e:
        print(f"⚠️ [Channel Branding Update Notice]: {e}")
        if "image" in branding_only_body["brandingSettings"]:
            del branding_only_body["brandingSettings"]["image"]
            try:
                youtube.channels().update(part="brandingSettings", body=branding_only_body).execute()
                print("✅ [Channel Branding, Keywords & Trailer Updated (Fallback)!]")
            except Exception as e2:
                print(f"⚠️ [Channel Branding Fallback Notice]: {e2}")

    # 2-B. 전 세계 8개국어 다국어 채널명·채널 설명(Localizations) 별도 호출 업데이트
    try:
        youtube.channels().update(
            part="localizations",
            body={
                "id": YOUTUBE_CHANNEL_ID,
                "localizations": localizations,
            },
        ).execute()
        print("✅ [Channel 8-Language Localizations (ko, en, ja, zh-CN, es, fr, de, vi) Updated!]")
    except Exception as e:
        print(f"⚠️ [Channel Localizations Notice]: {e}")

    # 2-C. 채널 전체 기본값: 아동용 아님(selfDeclaredMadeForKids=False) 설정 (댓글·알림·재생목록 제한 방지)
    try:
        youtube.channels().update(
            part="status",
            body={
                "id": YOUTUBE_CHANNEL_ID,
                "status": {
                    "selfDeclaredMadeForKids": False,
                },
            },
        ).execute()
        print("✅ [Channel Status: selfDeclaredMadeForKids=False Configured!]")
    except Exception as e:
        print(f"⚠️ [Channel Status Notice]: {e}")

    # 3. 인비디오 구독 워터마크(150x150 PNG) 등록
    try:
        wm_path = generate_channel_watermark_150x150()
        try:
            youtube.watermarks().set(
                channelId=YOUTUBE_CHANNEL_ID,
                body={
                    "timing": {
                        "type": "offsetFromStart",
                        "offsetMs": 0,
                    },
                    "position": {
                        "type": "corner",
                        "cornerPosition": "bottomRight",
                    },
                },
                media_body=MediaFileUpload(str(wm_path), mimetype="image/png", resumable=False),
            ).execute()
        except ValueError as ve:
            # httplib2 bug on HTTP 204 No Content gzip response after watermark upload succeeds
            if "range() arg 3 must not be zero" not in str(ve):
                raise
        print("✅ [In-Video Subscribe Watermark Set on @min7014_ai (HTTP 204 Applied)!]")
    except Exception as e:
        print(f"⚠️ [Watermark Set Notice]: {e}")

    # 4. 채널 홈 화면 섹션(Channel Sections) 최적화 구성
    try:
        existing_secs = youtube.channelSections().list(part="id,snippet", mine=True).execute().get("items", [])

        sections_to_add = [
            {
                "snippet": {"type": "singlePlaylist", "position": 0},
                "contentDetails": {"playlists": ["PLQfKuD3IPx1c"]},
            },
            {
                "snippet": {"type": "singlePlaylist", "position": 1},
                "contentDetails": {"playlists": ["PLA4FYpQnYlJQ"]},
            },
            {
                "snippet": {"type": "popularUploads", "position": 2},
            },
            {
                "snippet": {"type": "recentUploads", "position": 3},
            },
            {
                "snippet": {
                    "type": "multipleChannels",
                    "title": "📺 민은기 선생님의 수학자료실 본 채널 (@min7014)",
                    "position": 4,
                },
                "contentDetails": {"channels": [MAIN_CHANNEL_ID]},
            },
        ]

        if not existing_secs:
            for sec_body in sections_to_add:
                try:
                    parts = "snippet,contentDetails" if "contentDetails" in sec_body else "snippet"
                    youtube.channelSections().insert(part=parts, body=sec_body).execute()
                    print(f"📑 [Channel Home Section Added] {sec_body['snippet']['type']}")
                except Exception as se:
                    print(f"  ⚠️ [Section Insert Notice ({sec_body['snippet']['type']})]: {se}")
        else:
            print(f"📑 [Channel Sections Already Active] ({len(existing_secs)} sections)")
    except Exception as e:
        print(f"⚠️ [Channel Sections Notice]: {e}")

    # 5. 업로드된 영상에 1280x720 HD 커스텀 썸네일 적용 (이미 적용 완료된 영상은 중복 호출 스킵)
    vault_path = ROOT_DIR / "video_lectures" / "vault_index.json"
    vdata = {}
    if vault_path.exists():
        try:
            vdata = json.loads(vault_path.read_text(encoding="utf-8"))
        except Exception:
            vdata = {}
    applied_thumbs = set(vdata.get("applied_custom_thumbnails") or [
        "7zD66SWWceg", "CjE2nyyzG2s", "W_AWH-Gk89w", "ffNJhPRvh4Y",
        "k6LBYa5SCiA", "n9zyKwXXsbA", "Mq6s2JLV9mQ", "fXQJ8s1La-E", "bQO7fnT6aDU"
    ])

    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        slug = sdoc["slug"]
        yt_urls = sdoc.get("youtube_urls") or {}
        for lc in ["ko", "en"]:
            u = (yt_urls.get(lc) or "").strip()
            if not u:
                continue
            vid_id = u.split("/")[-1].split("?")[0].strip()
            if vid_id in applied_thumbs:
                print(f"🖼️ [1280x720 HD Custom Thumbnail Already Active ({lc.upper()})] {vid_id}")
                continue
            thumb_p = YT_PKG_DIR / f"{slug}_{lc}_thumb.png"
            if vid_id and thumb_p.exists():
                try:
                    youtube.thumbnails().set(
                        videoId=vid_id,
                        media_body=MediaFileUpload(str(thumb_p), mimetype="image/png", resumable=False),
                    ).execute()
                    applied_thumbs.add(vid_id)
                    print(f"🖼️ [1280x720 HD Custom Thumbnail Applied ({lc.upper()})] {vid_id} <- {thumb_p.name}")
                except Exception as te:
                    print(f"  ⚠️ [Thumbnail Notice ({vid_id})]: {te}")

    if vdata:
        vdata["applied_custom_thumbnails"] = sorted(list(applied_thumbs))
        vdata["channel_settings_optimized"] = True
        vault_path.write_text(json.dumps(vdata, ensure_ascii=False, indent=2), encoding="utf-8")


def watch_for_client_secret_and_auto_upload(privacy="public", open_gcp=True):
    """
    [100% 무인 YouTube Data API v3 업로드 감시 데몬]
    - 현재 로그인된 일반 크롬 브라우저에 Google Cloud OAuth 자격 증명 페이지를 열고,
      다운로드 폴더(Downloads)에 client_secret*.json 파일이 내려받아지는 즉시 자동 감지하여
      @min7014_ai 채널로 모든 한국어·영어 영상을 무인 업로드합니다.
    """
    import time
    import webbrowser

    if open_gcp and not find_google_client_secret():
        webbrowser.open("https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        webbrowser.open("https://console.cloud.google.com/apis/credentials")

    print("=" * 72)
    print("🤖 [@min7014_ai 무인 자동 업로드 감시기 가동 중]")
    print("1) 열린 크롬 탭(YouTube Data API v3)에서 [사용(Enable)] 클릭")
    print("2) [사용자 인증 정보 만들기 -> OAuth 클라이언트 ID -> 데스크톱 앱] 생성 후 [JSON 다운로드] 클릭")
    print("   -> 다운로드 폴더(Downloads)에 저장되는 즉시 자동으로 감지하여 @min7014_ai 업로드를 시작합니다!")
    print("=" * 72)

    while True:
        secret = find_google_client_secret()
        if secret:
            print(f"✅ Google OAuth 파일 감지 완료: {secret}")
            slugs = ["math20250130001", "2014111902", "2017090101", "2014111901"]
            for s_key in slugs:
                try:
                    upload_slug_to_youtube(s_key, langs=("ko", "en"), privacy=privacy, method="api")
                except Exception as e:
                    print(f"[Upload Notice ({s_key})] {e}")
            break
        # 동시에 사용자가 수동 드래그 업로드한 경우에도 RSS 피드에서 자동 감지
        try:
            matched = sync_youtube_channel_rss()
            if matched > 0:
                print(f"✅ @min7014_ai RSS 피드에서 {matched}개 주제 업로드 감지 및 사이트 자동 등록 완료!")
        except Exception:
            pass
        time.sleep(4.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="min7014.github.io Broadcast-Quality Script-First & @min7014_ai YouTube Auto-Uploader")
    parser.add_argument("--slug", type=str, default="math20250130001", help="Topic slug or PDF ID")
    parser.add_argument("--step", type=str, choices=["script", "video", "both"], default="both")
    parser.add_argument("--langs", type=str, default="ko,en,ja,es,zh-CN,fr,de,vi")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"], help="YouTube privacy status")
    parser.add_argument("--build-flagship", action="store_true", help="Generate flagship multi-language scripts and Master-Quality KR/EN YouTube packages")
    parser.add_argument("--upload-youtube", action="store_true", help="Upload rendered KR and EN videos directly to https://www.youtube.com/@min7014_ai")
    parser.add_argument("--upload-all", action="store_true", help="Upload all rendered topics in youtube_uploads/ to https://www.youtube.com/@min7014_ai")
    parser.add_argument("--watch-oauth", action="store_true", help="Watch Downloads for client_secret*.json and RSS feed to auto-upload & sync to @min7014_ai")
    parser.add_argument("--auto-pipeline", action="store_true", help="Automatically generate scripts, render 1080p KR/EN videos, and upload to @min7014_ai")
    parser.add_argument("--count", type=int, default=1, help="Number of pending PDF topics to process in --auto-pipeline mode")
    parser.add_argument("--git-push", action="store_true", help="Automatically commit and push updated catalog/scripts after upload")
    parser.add_argument("--sync-channel", action="store_true", help="Sync uploaded video URLs from https://www.youtube.com/@min7014_ai RSS feed")
    parser.add_argument("--open-studio", action="store_true", help="Open https://www.youtube.com/@min7014_ai YouTube Studio upload modal and local MP4 folder")
    parser.add_argument("--set-youtube-ko", type=str, default=None, help="Bind uploaded Korean YouTube URL for --slug")
    parser.add_argument("--set-youtube-en", type=str, default=None, help="Bind uploaded English YouTube URL for --slug")
    parser.add_argument("--boost-youtube", action="store_true", help="Upgrade all live @min7014_ai videos with high-CTR titles, SEO tags, playlists, and Eureka quiz comments")
    parser.add_argument("--optimize-channel", action="store_true", help="Optimize @min7014_ai internal channel settings (Banner, Watermark, Keywords, Trailer, 8-Lang Localizations, Sections, Custom Thumbnails)")
    parser.add_argument("--build-shorts", action="store_true", help="Generate 1080x1920 vertical YouTube Shorts (#Shorts) for --slug")
    parser.add_argument("--build-all-shorts", action="store_true", help="Generate 1080x1920 vertical YouTube Shorts (#Shorts) for all scripted topics")
    parser.add_argument("--upload-shorts", action="store_true", help="Upload rendered YouTube Shorts (#Shorts) to @min7014_ai")
    parser.add_argument("--daemon-shorts", action="store_true", help="Run background daemon to auto-upload & auto-enrich YouTube #Shorts on @min7014_ai")
    args = parser.parse_args()

    if args.set_youtube_ko is not None or args.set_youtube_en is not None:
        set_youtube_urls_for_slug(args.slug, yt_ko=args.set_youtube_ko, yt_en=args.set_youtube_en)
    elif args.daemon_shorts:
        run_shorts_and_video_upload_daemon(open_studio_now=False)
    elif args.optimize_channel:
        optimize_youtube_channel_settings()
    elif args.boost_youtube:
        boost_youtube_channel_popularity()
    elif args.build_all_shorts:
        build_all_shorts(upload=args.upload_shorts, privacy=args.privacy)
    elif args.upload_shorts:
        upload_short_to_youtube(args.slug, langs=("ko", "en"), privacy=args.privacy)
    elif args.build_shorts:
        for lc in ["ko", "en"]:
            render_youtube_short_vertical(args.slug, lang_code=lc)
    elif args.watch_oauth:
        watch_for_client_secret_and_auto_upload(privacy=args.privacy, open_gcp=True)
    elif args.sync_channel:
        sync_youtube_channel_rss()
    elif args.open_studio:
        open_youtube_studio_for_min7014(args.slug)
    elif args.auto_pipeline:
        spec = args.slug if "--slug" in sys.argv else None
        auto_pipeline_batch(count=args.count, specific_slug=spec, privacy=args.privacy, upload_enable=True, git_push=args.git_push)
    elif args.upload_all:
        slugs_to_upload = ["math20250130001", "2014111902", "2017090101", "2014111901"]
        for s_key in slugs_to_upload:
            try:
                upload_slug_to_youtube(s_key, langs=("ko", "en"), privacy=args.privacy, method="api")
            except Exception as e:
                print(f"[Upload Error ({s_key})] {e}", flush=True)
        if args.git_push:
            subprocess.run(["git", "add", "video_lectures/", "assets/"], check=False)
            subprocess.run(["git", "commit", "-m", "chore(youtube-vault): auto-upload & bind @min7014_ai video URLs"], check=False)
            subprocess.run(["git", "push", "origin", "main"], check=False)
    elif args.upload_youtube:
        upload_slug_to_youtube(args.slug, langs=("ko", "en"), privacy=args.privacy)
    elif args.build_flagship:
        for fl_slug in ["math20250130001", "2014111902", "2017090101", "2014111901"]:
            generate_or_update_script(fl_slug, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
            for yt_lang in ["ko", "en"]:
                render_multilingual_video(fl_slug, lang_code=yt_lang)
        update_video_catalog()
    else:
        langs = [x.strip() for x in args.langs.split(",") if x.strip()]
        if args.step in ("script", "both"):
            generate_or_update_script(args.slug, target_langs=langs)
        if args.step in ("video", "both"):
            video_langs = [l for l in langs if l in ("ko", "en")] or langs
            for l_code in video_langs:
                render_multilingual_video(args.slug, lang_code=l_code)
        update_video_catalog()
