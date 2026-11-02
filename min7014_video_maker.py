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


def auto_generate_page_explanations(doc, item_meta):
    """임의의 min7014.github.io PDF에 대해 페이지별 위치·색상 변화와 수학적 원리를 결합해 고품질 한·영 설명 대본을 생성합니다."""
    total_pages = len(doc)
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
        "default": "핵심 기하 작도 및 관계식 전개",
    }
    color_desc_en = {
        "red": "highlighting the key segment and ratio in red",
        "blue": "constructing the blue reference figure and base segment",
        "green": "marking the corresponding green geometric region",
        "purple": "connecting the purple auxiliary line and angle relation",
        "default": "advancing the geometric construction and algebraic derivation",
    }

    pages_out = []
    prev_pil = None

    for idx in range(total_pages):
        p_num = idx + 1
        pix = doc[idx].get_pixmap(dpi=96)
        curr_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        bbox, c_tag = compute_page_diff_and_color(prev_pil, curr_pil) if idx > 0 else (None, "default")
        prev_pil = curr_pil

        c_ko = color_desc_ko.get(c_tag, color_desc_ko["default"])
        c_en = color_desc_en.get(c_tag, color_desc_en["default"])

        focus_desc = c_ko
        if bbox:
            cx = (bbox[0] + bbox[2]) / 2.0
            if cx > 0.54:
                focus_desc = f"우측 증명 수식 유도 ({c_ko})"
            elif cx < 0.46:
                focus_desc = f"좌측 도형 작도 ({c_ko})"

        if p_num == 1:
            step_title = "도입 · 주제 및 증명 목표"
            exp_ko = f"1페이지입니다. 민은기 선생님의 수학자료실 단계별 시각 증명 강의입니다. 이번 시간에는 {clean_title_ko}의 핵심 원리를 단계별로 증명해 봅시다. {core_ko}"
            exp_en = f"Step 1. Welcome to Min's Math Lab. In this step-by-step visual proof lecture, we explore {clean_title_en} and prove why this mathematical property holds."
        elif p_num == total_pages:
            step_title = "완결 · 실전 적용 및 웹 탐구 안내"
            tip_str = tips_ko[0] if tips_ko else "도형의 정의와 대칭 보조선을 기억하세요."
            exp_ko = f"마지막 {p_num}페이지입니다. 지금까지 단계별 플립북 작도를 통해 정리를 완벽히 증명했습니다. 실전 팁으로, {tip_str}"
            exp_en = f"Step {p_num}. We have completed the entire step-by-step visual proof! Visit min7014.github.io to interact with the dynamic figure yourself."
        elif p_num == 2 and (not bbox or (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) < 0.01):
            step_title = "기초 칠판 및 기준점 준비"
            exp_ko = "2페이지입니다. 이제 빈 칠판 위에서 기본 도형과 기준 꼭짓점을 하나씩 작도하며 증명을 시작하겠습니다."
            exp_en = "Step 2. Starting on a clean canvas, let us construct the reference figure and vertices one step at a time."
        else:
            progress = (p_num - 1) / max(1, total_pages - 2)
            if progress <= 0.28:
                step_title = "1단계 · 기본 도형 및 기준점 작도"
                s_hint = steps_ko[0] if len(steps_ko) > 0 else "기준 도형과 꼭짓점을 명확히 배치합니다."
                exp_ko = f"{p_num}페이지입니다. {focus_desc} 과정으로, 화면에 나타난 기본 도형과 기준점을 확인합니다. {s_hint}"
            elif progress <= 0.55:
                step_title = "2단계 · 핵심 보조선 및 기하적 대칭 연결"
                s_hint = steps_ko[1] if len(steps_ko) > 1 else vis_ko
                exp_ko = f"{p_num}페이지입니다. {focus_desc} 단계입니다. 새로 그어진 보조선과 각·선분의 대칭 관계를 눈여겨보세요. {s_hint}"
            elif progress <= 0.82:
                step_title = "3단계 · 비례식 및 대수적 등식 도출"
                s_hint = steps_ko[2] if len(steps_ko) > 2 else "도형의 성질을 비례식과 등식으로 변환합니다."
                exp_ko = f"{p_num}페이지입니다. {focus_desc} 과정입니다. 도형에서 확인한 합동·닮음·넓이 관계를 수식으로 연결합니다. {s_hint}"
            else:
                step_title = "4단계 · 수식 결합 및 정리 완성"
                s_hint = steps_ko[3] if len(steps_ko) > 3 else "유도한 관계식들을 결합하여 최종 정리를 완성합니다."
                exp_ko = f"{p_num}페이지입니다. {focus_desc} 마무리 단계입니다. 앞 단계의 조각들을 결합해 최종 결론을 도출합니다. {s_hint}"
            exp_en = translate_text_google_gtx(exp_ko, "en")

        pages_out.append({
            "page": p_num,
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
        pages_data = auto_generate_page_explanations(doc, item_meta)

    for p_obj in pages_data:
        base_ko = p_obj["explanation_text"]
        p_obj["narrations"]["ko"] = base_ko
        if "en" not in p_obj["narrations"] or not p_obj["narrations"]["en"]:
            p_obj["narrations"]["en"] = translate_text_google_gtx(base_ko, "en")
        for lang in target_langs:
            if lang in ("ko", "en"):
                continue
            p_obj["narrations"][lang] = translate_text_google_gtx(base_ko, lang)

    script_doc = {
        "slug": slug_key,
        "title": title,
        "title_en": title_en,
        "sub_domain_ko": sub_ko,
        "pdf_url": pdf_url,
        "web_url": web_url,
        "page_count": total_pages,
        "base_language": "ko",
        "quality_profile": "Broadcast Master 1080p (300 DPI Lanczos + H.264 High Profile CRF 16 + 48kHz/192kbps AAC)",
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


def render_slide_frame_1080p(pdf_page, page_info, script_doc, lang_code):
    """
    [초고화질 300 DPI 수퍼샘플링 + 스포트라이트 콜아웃 + 진행률 바]
    1920x1080 Full HD 방송급 강의 프레임을 생성합니다.
    """
    W, H = 1920, 1080
    canvas = Image.new("RGB", (W, H), (11, 17, 32))
    draw = ImageDraw.Draw(canvas)

    p_num = page_info["page"]
    tot_p = script_doc["page_count"]

    # 1. 상단 방송 헤더 바 (높이 74px) + 진행률 게이지 바 (y: 74~78)
    draw.rectangle([0, 0, W, 74], fill=(17, 25, 44))
    draw.rectangle([0, 74, W, 78], fill=(30, 41, 59))
    prog_w = int((p_num / max(1, tot_p)) * W)
    draw.rectangle([0, 74, prog_w, 78], fill=(56, 189, 248))

    font_header = get_font_for_lang("ko", 26, bold=True)
    font_badge = get_font_for_lang("ko", 21, bold=True)

    header_title = script_doc.get("title_en") if lang_code == "en" and script_doc.get("title_en") else script_doc.get("title", "")
    header_title = re.sub(r"\$[^\$]*\$", "", header_title).strip()
    # 좌측 상단 기하 삼각형 심볼 벡터 작도 (이모지 깨짐 방지)
    draw.polygon([(32, 50), (48, 22), (64, 50)], outline=(56, 189, 248), fill=(0, 99, 152))
    prefix_brand = "Min's Math Lab · " if lang_code == "en" else "민은기 선생님의 수학자료실 · "
    title_str = prefix_brand + header_title
    if len(title_str) > 58:
        title_str = title_str[:58] + "..."
    draw.text((76, 21), title_str, fill=(248, 250, 252), font=font_header)

    lang_meta = GLOBAL_VOICE_MAP.get(lang_code, {"name": lang_code, "flag": ""})
    lang_tag = lang_code.upper()
    right_badge = f"STEP {p_num} / {tot_p}   |   [{lang_tag}] {lang_meta['name']}"
    draw.rounded_rectangle([W - 486, 14, W - 28, 58], radius=12, fill=(0, 99, 152))
    draw.text((W - 468, 22), right_badge, fill=(255, 255, 255), font=font_badge)

    # 2. 중앙 PDF 페이지 300 DPI 초고해상도 렌더링 + Lanczos 리샘플링
    pix = pdf_page.get_pixmap(dpi=300)
    pdf_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    max_pw, max_ph = 1764, 756
    scale = min(max_pw / pdf_img.width, max_ph / pdf_img.height)
    new_w, new_h = int(pdf_img.width * scale), int(pdf_img.height * scale)
    pdf_resized = pdf_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    px = (W - new_w) // 2
    py = 90 + (max_ph - new_h) // 2

    # 은은한 외곽 글로우 프레임 및 슬라이드 배치
    draw.rounded_rectangle([px - 10, py - 10, px + new_w + 10, py + new_h + 10], radius=16, fill=(24, 38, 66))
    draw.rounded_rectangle([px - 4, py - 4, px + new_w + 4, py + new_h + 4], radius=12, fill=(56, 189, 248))
    canvas.paste(pdf_resized, (px, py))

    # 3. 새로 추가된 도형·보조선·수식 영역 스포트라이트 하이라이트 & [STEP k FOCUS] 배지
    bbox = page_info.get("diff_bbox")
    if bbox and p_num > 1 and p_num < tot_p:
        bx0 = max(px + 4, px + int(bbox[0] * new_w) - 12)
        by0 = max(py + 4, py + int(bbox[1] * new_h) - 12)
        bx1 = min(px + new_w - 4, px + int(bbox[2] * new_w) + 12)
        by1 = min(py + new_h - 4, py + int(bbox[3] * new_h) + 12)
        if (bx1 - bx0) > 26 and (by1 - by0) > 26:
            # 이중 골드·앰버 하이라이트 테두리 (위쪽 수식을 가리지 않도록 하단 우측에 STEP 배지 배치)
            draw.rounded_rectangle([bx0 - 2, by0 - 2, bx1 + 2, by1 + 2], radius=12, outline=(254, 240, 138), width=2)
            draw.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(245, 158, 11), width=4)
            tag_label = f"STEP {p_num} NEW" if lang_code == "en" else f"{p_num}단계 핵심 변화"
            tag_w = 136 if lang_code == "en" else 148
            tag_y = by1 + 4 if (by1 + 32) < (py + new_h) else max(py + 6, by0 - 30)
            tag_x = max(px + 6, min(px + new_w - tag_w - 6, bx1 - tag_w))
            draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + 26], radius=6, fill=(217, 119, 6))
            draw.text((tag_x + 10, tag_y + 3), tag_label, fill=(255, 255, 255), font=get_font_for_lang("ko", 16, bold=True))

    # 4. 하단 방송급 자막 바 (y: 862 ~ 1080)
    draw.rectangle([0, 862, W, H], fill=(7, 11, 24))
    draw.line([0, 862, W, 862], fill=(56, 189, 248), width=2)

    narration_text = page_info.get("narrations", {}).get(lang_code) or page_info.get("explanation_text", "")
    ko_ref_text = page_info.get("explanation_text", "")

    is_cjk = lang_code in ("ko", "ja") or lang_code.startswith("zh")
    wrap_width = 53 if is_cjk else 86
    wrapped_lines = textwrap.wrap(narration_text, width=wrap_width)[:3]

    font_sub = get_font_for_lang(lang_code, 29 if is_cjk else 27, bold=True)
    y_cursor = 882
    for line in wrapped_lines:
        # 가독성을 높이는 텍스트 그림자
        draw.text((50, y_cursor + 2), line, fill=(0, 0, 0), font=font_sub)
        draw.text((48, y_cursor), line, fill=(254, 240, 138), font=font_sub)
        y_cursor += 40

    if lang_code != "ko" and ko_ref_text:
        font_ko_sub = get_font_for_lang("ko", 20, bold=False)
        ko_one_line = ko_ref_text if len(ko_ref_text) <= 80 else (ko_ref_text[:80] + "...")
        draw.text((48, 1036), f"[한국어 원문] {ko_one_line}", fill=(148, 163, 184), font=font_ko_sub)

    return canvas


def generate_youtube_thumbnail_720p(doc, script_doc, lang_code, out_png_path):
    """유튜브 업로드용 1280x720 초고화질(300 DPI 원본 기반) 썸네일을 생성합니다."""
    W, H = 1280, 720
    thumb = Image.new("RGB", (W, H), (9, 15, 31))
    draw = ImageDraw.Draw(thumb)

    key_idx = max(0, len(doc) - 2)
    pix = doc[key_idx].get_pixmap(dpi=240)
    slide_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    scale = min(680 / slide_img.width, 600 / slide_img.height)
    sw, sh = int(slide_img.width * scale), int(slide_img.height * scale)
    slide_resized = slide_img.resize((sw, sh), Image.Resampling.LANCZOS)

    sx = W - sw - 38
    sy = (H - sh) // 2
    draw.rounded_rectangle([sx - 10, sy - 10, sx + sw + 10, sy + sh + 10], radius=20, fill=(56, 189, 248))
    thumb.paste(slide_resized, (sx, sy))

    is_en = (lang_code == "en")
    badge_bg = (220, 38, 38) if is_en else (0, 99, 152)
    badge_txt = "[EN] VISUAL MATH PROOF LECTURE" if is_en else "[KR] 단계별 시각 수학 증명 강의"
    draw.rounded_rectangle([42, 52, 510, 112], radius=14, fill=badge_bg)
    draw.text((62, 66), badge_txt, fill=(255, 255, 255), font=get_font_for_lang("ko", 24, bold=True))

    raw_ko_title = re.sub(r"\$[^\$]*\$", "", script_doc.get("title", "")).strip()
    ko_main_part = raw_ko_title.split("(")[0].strip() or raw_ko_title
    en_main_part = (script_doc.get("title_en") or raw_ko_title).split("—")[0].strip()

    main_title = en_main_part if is_en else ko_main_part
    wrapped_t = textwrap.wrap(main_title, width=18 if is_en else 12, break_long_words=False)[:3]
    y_t = 152
    font_t = get_font_for_lang("ko", 46 if is_en else 52, bold=True)
    for line in wrapped_t:
        draw.text((44, y_t + 3), line, fill=(0, 0, 0), font=font_t)
        draw.text((42, y_t), line, fill=(254, 240, 138), font=font_t)
        y_t += 68

    if not is_en and en_main_part:
        draw.text((42, y_t + 8), en_main_part, fill=(148, 163, 184), font=get_font_for_lang("ko", 25, bold=True))

    sub_line = (
        f"Total {script_doc['page_count']} Flipbook Steps · 1080p Master"
        if is_en
        else f"총 {script_doc['page_count']}페이지 한 단계씩 눈으로 보는 증명"
    )
    draw.text((42, 480), sub_line, fill=(56, 189, 248), font=get_font_for_lang("ko", 26, bold=True))
    draw.text((42, 532), "Min's Math Lab · https://min7014.github.io/", fill=(203, 213, 225), font=get_font_for_lang("ko", 22, bold=False))

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


def build_youtube_metadata_for_lang(script_doc, lang_code, page_timings):
    """유튜브 저장용 제목, 타임스탬프(00:00) 챕터 설명문, 태그, SRT 자막을 생성합니다."""
    slug = script_doc["slug"]
    tot_p = script_doc["page_count"]
    pdf_url = script_doc["pdf_url"]
    web_url = script_doc.get("web_url") or "https://min7014.github.io/"
    studio_url = f"https://min7014.github.io/mathedu/video_studio.html?slug={slug}"
    channel_url = "https://www.youtube.com/@min7014_ai"
    channel_id = "UCSlqQfOEtRfJuMPyGMLgFYA"
    studio_upload_url = f"https://studio.youtube.com/channel/{channel_id}/videos/upload?d=ud"

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
        yt_title = f"[Min's Math Lab AI @min7014_ai] {clean_en_title} (1080p Visual Proof)"
        if len(yt_title) > 98:
            yt_title = yt_title[:95] + "..."
        yt_desc = (
            f"📐 Step-by-Step AI Visual Mathematical Proof Lecture ({tot_p} Flipbook Pages · 1080p Broadcast Quality)\n"
            f"Topic: {clean_en_title} [ID: {slug}_EN]\n"
            f"🤖 Official AI Lecture Channel: {channel_url}\n"
            f"📺 Main Math Resource Channel: https://www.youtube.com/@min7014\n\n"
            f"🔗 Interactive GeoGebra & Original Flipbook PDF: {web_url}\n"
            f"📄 Direct PDF Link: {pdf_url}\n"
            f"🎬 Multilingual Lecture Studio (20+ Languages): {studio_url}\n\n"
            f"⏱️ [Step-by-Step Chapters]\n{chapters_block}\n\n"
            f"#min7014_ai #min7014 #MathProof #Geometry #VisualMath #MinsMathLab #StepByStepMath #Mathematics"
        )
        yt_tags = ["min7014_ai", "min7014", "Min's Math Lab", "Visual Math Proof", "Geometry Proof", "Mathematics", "GeoGebra", "Step by Step Math"]
    else:
        clean_ko_title = re.sub(r"\$[^\$]*\$", "", script_doc.get("title", slug)).strip()
        yt_title = f"[민은기 선생님의 수학자료실_AI] {clean_ko_title} — 단계별 시각 증명 강의 (1080p)"
        if len(yt_title) > 98:
            yt_title = yt_title[:95] + "..."
        yt_desc = (
            f"📐 민은기 선생님의 수학자료실(https://min7014.github.io/) AI 자동생성 단계별 플립북 PDF 해설 강의 (총 {tot_p}페이지 · 1080p 초고화질)\n"
            f"주제: {clean_ko_title} [ID: {slug}_KO]\n"
            f"🤖 AI 자동생성 강의 공식 채널: {channel_url}\n"
            f"📺 본 채널: https://www.youtube.com/@min7014\n\n"
            f"🔗 대화형 GeoGebra 실습 및 원문 보기: {web_url}\n"
            f"📄 단계별 증명 PDF 원문: {pdf_url}\n"
            f"🎬 전 세계 다국어 강의 영상 스튜디오: {studio_url}\n\n"
            f"⏱️ [페이지별 단계 타임스탬프]\n{chapters_block}\n\n"
            f"#min7014_ai #min7014 #민은기선생님의수학자료실 #수학증명 #기하학 #시각적증명 #수학교육 #GeoGebra #mathedu"
        )
        yt_tags = ["min7014_ai", "min7014", "민은기 선생님의 수학자료실_AI", "민은기 선생님의 수학자료실", "수학 증명", "기하 증명", "시각적 수학", "GeoGebra", "수능 수학", "mathedu"]

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

    pages_to_render = script_doc["pages"]
    if max_pages:
        pages_to_render = pages_to_render[:max_pages]

    topic_upload_dir = YT_UPLOADS_DIR / slug_key
    topic_upload_dir.mkdir(parents=True, exist_ok=True)

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_hq_{slug_key}_{lang_code}_"))
    segment_files = []
    page_timings = []
    cursor_sec = 0.0

    try:
        for p_info in pages_to_render:
            p_idx = p_info["page"] - 1
            narration = p_info.get("narrations", {}).get(lang_code) or p_info["explanation_text"]

            slide_img = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code)
            img_path = tmp_dir / f"slide_{p_idx:03d}.png"
            mp3_path = tmp_dir / f"audio_{p_idx:03d}.mp3"
            seg_path = tmp_dir / f"seg_{p_idx:03d}.mp4"

            slide_img.save(img_path, compress_level=1)
            asyncio.run(synthesize_edge_tts_mp3(narration, voice_name, mp3_path))

            # 초고화질 인코딩:
            # - 0.35초 시작 여백(adelay=350|350) + 0.65초 종료 여운(apad=pad_dur=0.65)
            # - H.264 High Profile, CRF 16 (무손실급 선명도), 30fps, 48kHz 192kbps Stereo AAC
            cmd = [
                ffmpeg_exe, "-y",
                "-loop", "1", "-framerate", "30", "-i", str(img_path),
                "-i", str(mp3_path),
                "-filter_complex", "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=350|350,apad=pad_dur=0.65[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                "-preset", "medium", "-tune", "stillimage",
                "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
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

        out_mp4 = topic_upload_dir / f"{slug_key}_{lang_code}.mp4"
        cmd_concat = [
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            "-movflags", "+faststart",
            str(out_mp4)
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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


def set_youtube_urls_for_slug(slug_key, yt_ko=None, yt_en=None):
    """업로드 완료된 한국어(ko) 및 영어(en) 유튜브 URL을 스크립트, 카탈로그, 심층 지식 DB에 일괄 저장합니다."""
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if script_path.exists():
        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        yt_urls = sdoc.setdefault("youtube_urls", {"ko": "", "en": "", "orig": ""})
        if yt_ko is not None:
            yt_urls["ko"] = yt_ko.strip()
        if yt_en is not None:
            yt_urls["en"] = yt_en.strip()
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

    if DEEP_JSON_PATH.exists():
        items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
        changed = False
        for it in items:
            u = (it.get("url") or "").strip()
            p = (it.get("pdf") or "").split("#")[0].strip()
            if slug_key in (u, p) or u.endswith(f"/{slug_key}.html") or p.endswith(f"/{slug_key}.pdf"):
                if yt_ko is not None:
                    it["youtube_ko"] = yt_ko.strip()
                if yt_en is not None:
                    it["youtube_en"] = yt_en.strip()
                changed = True
        if changed:
            DEEP_JSON_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    if LOOKUP_JSON_PATH.exists():
        lmap = json.loads(LOOKUP_JSON_PATH.read_text(encoding="utf-8"))
        if slug_key in lmap:
            if yt_ko is not None:
                lmap[slug_key]["yk"] = yt_ko.strip()
            if yt_en is not None:
                lmap[slug_key]["ye"] = yt_en.strip()
            LOOKUP_JSON_PATH.write_text(json.dumps(lmap, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    update_video_catalog()
    print(f"[YouTube URLs Registered] slug={slug_key} -> ko={yt_ko}, en={yt_en}")


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
    for rss_url in [YOUTUBE_RSS_URL, f"https://www.youtube.com/feeds/videos.xml?channel_id={MAIN_CHANNEL_ID}"]:
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
        for ent in entries:
            blob = f"{ent['title']}\n{ent['description']}"
            if f"[ID: {slug}_KO]" in blob or (slug in blob and ("단계별" in ent["title"] or "수학자료실" in ent["title"])):
                found_ko = ent["url"]
            elif f"[ID: {slug}_EN]" in blob or (slug in blob and ("Visual Proof" in ent["title"] or "Min's Math Lab" in ent["title"])):
                found_en = ent["url"]
            elif title_ko and len(title_ko) >= 3 and title_ko in ent["title"] and "Visual Proof" not in ent["title"]:
                found_ko = ent["url"]
            elif title_en and len(title_en) >= 5 and title_en.lower() in ent["title"].lower():
                found_en = ent["url"]
        if found_ko or found_en:
            set_youtube_urls_for_slug(slug, yt_ko=found_ko, yt_en=found_en)
            matched_count += 1
    print(f"[@min7014_ai Channel RSS Sync] Checked {len(entries)} videos on {YOUTUBE_CHANNEL_URL} -> Matched {matched_count} topics.")
    return matched_count


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

    profile_dir = ROOT_DIR / ".yt_studio_profile_min7014_ai"
    profile_dir.mkdir(parents=True, exist_ok=True)
    uploaded_urls = {}

    privacy_radio_name = {
        "public": "PUBLIC",
        "unlisted": "UNLISTED",
        "private": "PRIVATE",
    }.get(privacy.lower(), "PUBLIC")

    with sync_playwright() as p:
        browser_ctx = None
        for ch_name in ["msedge", "chrome"]:
            try:
                browser_ctx = p.chromium.launch_persistent_context(
                    user_data_dir=str(profile_dir),
                    channel=ch_name,
                    headless=False,
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
                args=["--disable-blink-features=AutomationControlled"],
            )

        page = browser_ctx.pages[0] if browser_ctx.pages else browser_ctx.new_page()

        for lang_code in langs:
            mp4_path = (YT_UPLOADS_DIR / slug_key / f"{slug_key}_{lang_code}.mp4").resolve()
            thumb_path = (YT_PKG_DIR / f"{slug_key}_{lang_code}_thumb.png").resolve()
            meta = meta_all[lang_code]

            print(f"[Studio Auto-Upload -> {YOUTUBE_CHANNEL_HANDLE}] Navigating to {YOUTUBE_STUDIO_UPLOAD_URL} ({slug_key}_{lang_code}.mp4)")
            page.goto(YOUTUBE_STUDIO_UPLOAD_URL, wait_until="domcontentloaded")

            # 만약 구글 로그인이 안 되어 있다면 사용자가 1회 로그인할 때까지 대기 (최대 5분)
            if "accounts.google.com" in page.url or "signin" in page.url.lower():
                print("=" * 72)
                print(f"🔐 [최초 1회 로그인 안내] 열린 브라우저 창에서 {YOUTUBE_CHANNEL_URL} 계정에 로그인해 주세요.")
                print("   (한 번 로그인하시면 세션이 저장되어 다음부터는 완전 자동으로 업로드됩니다.)")
                print("=" * 72)
                page.wait_for_url(lambda u: "studio.youtube.com" in u, timeout=300000)
                page.goto(YOUTUBE_STUDIO_UPLOAD_URL, wait_until="domcontentloaded")

            # 업로드 모달의 input[type="file"] 대기 (모달이 닫혀 있으면 만들기->동영상 업로드 클릭)
            try:
                file_input = page.locator('ytcp-uploads-file-picker input[type="file"], input[name="Filedata"]').first
                file_input.wait_for(state="attached", timeout=15000)
            except Exception:
                try:
                    page.locator('#create-icon, ytcp-button#create-icon').first.click(timeout=5000)
                    page.locator('tp-yt-paper-item#text-item-0').first.click(timeout=5000)
                except Exception:
                    pass
                file_input = page.locator('input[type="file"]').first
                file_input.wait_for(state="attached", timeout=30000)

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
            print(f"[Google OAuth] 브라우저에서 {YOUTUBE_CHANNEL_URL} ({YOUTUBE_CHANNEL_NAME}) 계정을 선택하여 로그인해 주세요...")
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_file), SCOPES)
            creds = flow.run_local_server(port=0)
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

    for lang_code in langs:
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

        media = MediaFileUpload(str(mp4_path), chunksize=-1, resumable=True, mimetype="video/mp4")
        req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        resp = req.execute()
        vid_id = resp["id"]
        yt_url = f"https://youtu.be/{vid_id}"
        uploaded_urls[lang_code] = yt_url
        print(f"[YouTube Uploaded to {YOUTUBE_CHANNEL_HANDLE} ({lang_code.upper()})] {yt_url}")

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
        update_video_catalog()
        uploaded = {}
        if upload_enable:
            uploaded = upload_slug_to_youtube(s_key, langs=("ko", "en"), privacy=privacy, method="auto")
        results.append({"slug": s_key, "uploaded_urls": uploaded})

    if git_push:
        try:
            subprocess.run(["git", "add", "video_lectures/catalog.json", "video_lectures/scripts/", "video_lectures/youtube_packages/", "data/"], check=False)
            subprocess.run(["git", "commit", "-m", f"chore(youtube-ai): auto-sync @min7014_ai videos ({', '.join(target_slugs)})"], check=False)
            subprocess.run(["git", "push", "origin", "main"], check=False)
        except Exception as e:
            print(f"[Git Push Notice] {e}")
    return results


def update_video_catalog():
    scripts = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        with open(sp, "r", encoding="utf-8") as f:
            sdoc = json.load(f)
        slug = sdoc["slug"]
        yt_urls = sdoc.get("youtube_urls") or {"ko": "", "en": "", "orig": ""}
        yt_pkgs = sdoc.get("youtube_packages") or {}

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
            "youtube_packages": {
                k: {
                    "title": v.get("title", ""),
                    "srt_url": v.get("srt_url", ""),
                    "thumbnail_url": v.get("thumbnail_url", ""),
                    "local_mp4_path": v.get("local_mp4_path", ""),
                    "total_duration_sec": v.get("total_duration_sec", 0)
                }
                for k, v in yt_pkgs.items()
            }
        })
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)
    print(f"[Catalog Updated] {CATALOG_PATH} ({len(scripts)} topics)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="min7014.github.io Broadcast-Quality Script-First & @min7014_ai YouTube Auto-Uploader")
    parser.add_argument("--slug", type=str, default="math20250130001", help="Topic slug or PDF ID")
    parser.add_argument("--step", type=str, choices=["script", "video", "both"], default="both")
    parser.add_argument("--langs", type=str, default="ko,en,ja,es,zh-CN,fr,de,vi")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"], help="YouTube privacy status")
    parser.add_argument("--build-flagship", action="store_true", help="Generate flagship multi-language scripts and Master-Quality KR/EN YouTube packages")
    parser.add_argument("--upload-youtube", action="store_true", help="Upload rendered KR and EN videos directly to https://www.youtube.com/@min7014_ai")
    parser.add_argument("--upload-all", action="store_true", help="Upload all rendered topics in youtube_uploads/ to https://www.youtube.com/@min7014_ai")
    parser.add_argument("--auto-pipeline", action="store_true", help="Automatically generate scripts, render 1080p KR/EN videos, and upload to @min7014_ai")
    parser.add_argument("--count", type=int, default=1, help="Number of pending PDF topics to process in --auto-pipeline mode")
    parser.add_argument("--git-push", action="store_true", help="Automatically commit and push updated catalog/scripts after upload")
    parser.add_argument("--sync-channel", action="store_true", help="Sync uploaded video URLs from https://www.youtube.com/@min7014_ai RSS feed")
    parser.add_argument("--open-studio", action="store_true", help="Open https://www.youtube.com/@min7014_ai YouTube Studio upload modal and local MP4 folder")
    parser.add_argument("--set-youtube-ko", type=str, default=None, help="Bind uploaded Korean YouTube URL for --slug")
    parser.add_argument("--set-youtube-en", type=str, default=None, help="Bind uploaded English YouTube URL for --slug")
    args = parser.parse_args()

    if args.set_youtube_ko is not None or args.set_youtube_en is not None:
        set_youtube_urls_for_slug(args.slug, yt_ko=args.set_youtube_ko, yt_en=args.set_youtube_en)
    elif args.sync_channel:
        sync_youtube_channel_rss()
    elif args.open_studio:
        open_youtube_studio_for_min7014(args.slug)
    elif args.auto_pipeline:
        spec = args.slug if "--slug" in sys.argv else None
        auto_pipeline_batch(count=args.count, specific_slug=spec, privacy=args.privacy, upload_enable=True, git_push=args.git_push)
    elif args.upload_all:
        slugs_to_upload = [d.name for d in sorted(YT_UPLOADS_DIR.iterdir()) if d.is_dir()] or ["math20250130001", "2014111902", "2017090101", "2014111901"]
        for s_key in slugs_to_upload:
            upload_slug_to_youtube(s_key, langs=("ko", "en"), privacy=args.privacy)
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
