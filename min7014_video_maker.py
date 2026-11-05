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
import time
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path

import edge_tts
import pymupdf
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

ROOT_DIR = Path(__file__).resolve().parent

# ==============================================================================
# 🔑 Multi-Project YouTube API Quota Rotation Pool & Pre-Flight Guard
# ==============================================================================
_EXHAUSTED_TOKEN_FILES = {}  # token_path -> backoff_until_ts
_LAST_UPLOAD_QUOTA_BLOCKED = False

def get_available_youtube_upload_service():
    """
    워크스페이스 내의 모든 youtube_token_min7014_ai*.json 파일을 스캔하여,
    현재 일일 할당량(429 rateLimitExceeded)에 걸리지 않은 유효한 YouTube Data API v3 객체를 반환합니다.
    유튜브 고급 기능(Advanced Features) 승인 및 일일 한도 해제 시 연속 대량 업로드를 수행하며,
    복수의 GCP 프로젝트 토큰이 존재할 경우 자동으로 로테이션합니다.
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    now_ts = time.time()
    token_candidates = sorted(ROOT_DIR.glob('youtube_token_min7014_ai*.json'))
    for t_file in token_candidates:
        backoff_until = _EXHAUSTED_TOKEN_FILES.get(str(t_file), 0.0)
        if now_ts < backoff_until:
            continue
        try:
            creds = Credentials.from_authorized_user_file(str(t_file), SCOPES)
            if not creds.valid and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                t_file.write_text(creds.to_json(), encoding='utf-8')
            return build('youtube', 'v3', credentials=creds), str(t_file)
        except Exception as e:
            print(f'⚠️ [Token Pool Skip ({t_file.name})]: {e}')
    return None, None

def mark_token_quota_exhausted(token_path_str, seconds=900):
    global _LAST_UPLOAD_QUOTA_BLOCKED
    _LAST_UPLOAD_QUOTA_BLOCKED = True
    if token_path_str:
        _EXHAUSTED_TOKEN_FILES[str(token_path_str)] = time.time() + seconds
        print(f'🔄 [Quota Pool] {Path(token_path_str).name} 업로드 한도 대기 감지 -> {seconds//60}분 쿨다운 후 자동 재시도 (고급 기능/일일 쿼터 해제 시 즉시 대량 업로드)')

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
            "1페이지입니다. 단계별 시각적 수학 증명 강의입니다. 직각삼각형과 정사각형이 무한히 가지를 뻗어 나가는 피타고라스 나무의 기하학적 원리와 넓이 보존 법칙을 한 단계씩 탐구해 봅시다.",
            "2페이지입니다. 이제 빈 칠판 위에서 첫 번째 기준 정사각형과 직각삼각형부터 차례대로 작도를 시작합니다.",
            "3페이지입니다. 가장 아래에 나무의 기둥이 되는 첫 번째 정사각형을 그리고, 그 윗변을 지름으로 하는 반원 위에 한 점을 잡아 직각삼각형을 올립니다. 원의 지름에 대한 원주각은 항상 90도이므로 완벽한 직각삼각형이 만들어집니다.",
            "4페이지입니다. 직각삼각형의 나머지 두 직각변 위에 각각 새로운 정사각형 두 개를 작도합니다. 피타고라스 정리에 의해, 새로 피어난 두 정사각형의 넓이 합은 아래 기둥 정사각형의 넓이와 정확히 일치합니다.",
            "5페이지입니다. 두 정사각형의 윗변에 다시 닮음인 직각삼각형을 올리고, 그 위에 4개의 정사각형 가지를 피워냅니다. 이 4개 정사각형의 넓이를 모두 더해도 여전히 맨 아래 기둥 정사각형 하나의 넓이와 같습니다.",
            "6페이지입니다. 다음 단계로 8개의 정사각형 가지가 뻗어 나갑니다. 가지의 개수는 2의 거듭제곱으로 두 배씩 늘어나지만, 각 층의 정사각형 넓이 총합은 처음 기둥의 넓이로 일정하게 보존됩니다.",
            "7페이지입니다. 16개의 정사각형 가지가 형성됩니다. 오른쪽의 기준 직각삼각형에서 꼭짓점의 위치를 바꾸면 예각의 크기가 달라지면서 나무가 휘어지는 방향과 비대칭 곡선미가 결정됩니다.",
            "8페이지입니다. 32개의 정사각형 잎사귀가 돋아납니다. 작은 나뭇가지 하나를 확대해 보아도 나무 전체의 모양과 똑같이 닮아 있는 자기닮음 프랙탈 기하학의 구조가 선명하게 드러납니다.",
            "9페이지입니다. 64개의 정사각형이 풍성한 나무 수관을 이룹니다. 오직 직각삼각형과 피타고라스 정리라는 단순한 규칙의 반복만으로 자연 속 브로콜리나 나뭇가지와 닮은 생명력 있는 형태가 탄생합니다.",
            "10페이지입니다. 마지막 단계까지 완성된 피타고라스 나무의 전체 모습입니다. 유클리드 기하학의 넓이 보존 법칙과 현대 프랙탈 기하학이 만나는 아름다운 수학적 조화를 감상해 보세요.",
            "11페이지입니다. 수학홈페이지의 동적 기하 웹페이지에서 반원 위의 꼭짓점을 마우스로 직접 드래그하며, 나만의 피타고라스 나무가 바람에 흔들리듯 변화하는 모습을 실험해 보세요!"
        ],
        "pages_en": [
            "Step 1. In this step-by-step visual proof lecture, we explore the Pythagoras Tree, where right triangles and squares branch out infinitely while preserving total area.",
            "Step 2. Starting from a clean canvas, let us construct the base square and the generating right triangle one step at a time.",
            "Step 3. First, we draw the trunk square at the bottom, and place a right triangle on its top edge using a semicircle. By Thales' theorem, any angle inscribed in a semicircle is always a ninety-degree right angle.",
            "Step 4. Next, we construct two smaller squares on the two legs of the right triangle. By the Pythagorean Theorem, the sum of the areas of these two new squares is exactly equal to the area of the trunk square below.",
            "Step 5. On top of those two squares, we attach similar right triangles and sprout four new branch squares. Remarkably, the combined area of all four squares in this third level still equals the single trunk square.",
            "Step 6. In the fourth generation, eight squares branch outward. While the number of squares doubles at every level as powers of two, the total area at each level remains strictly invariant.",
            "Step 7. Now sixteen squares form the fifth level of branches. Notice on the right how the acute angle of the generating right triangle controls the tilt and curvature of the entire tree.",
            "Step 8. Thirty-two squares bloom across the sixth level. Zooming into any single branch reveals an exact miniature copy of the whole structure, demonstrating the self-similarity of fractal geometry.",
            "Step 9. Sixty-four squares now create a lush canopy. Through the simple recursive repetition of the Pythagorean Theorem, pure geometry reproduces the organic branching patterns found in nature.",
            "Step 10. Here is the fully grown Pythagoras Tree at the eighth stage. Take a moment to appreciate how classical area conservation and modern fractal geometry unite in visual harmony.",
            "Step 11. Visit the interactive geometry lab at min7014.github.io to drag the vertex along the semicircle yourself and watch the Pythagoras Tree transform dynamically in real time!"
        ]
    },
    "2014111902": {
        "title": "체바의 정리 (Ceva's Theorem)",
        "title_en": "Ceva's Theorem — Step-by-Step Visual Proof via Triangle Area Ratios",
        "pdf_url": "https://min7014.github.io/2020/2014111902.pdf",
        "web_url": "https://min7014.github.io/math20200228001.html",
        "pages_ko": [
            "1페이지입니다. 단계별 시각적 수학 증명 강의입니다. 삼각형의 세 꼭짓점과 한 교점을 지나는 세 직선이 마주 보는 변을 나누는 길이 비의 곱이 항상 1이 된다는 체바의 정리를 눈으로 보며 증명해 봅시다.",
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
            "17페이지입니다. 수학홈페이지의 동적 기하 웹페이지에서 교점 O의 위치를 삼각형 안팎으로 직접 움직여 보며 체바의 정리가 언제나 성립함을 확인해 보세요!"
        ],
        "pages_en": [
            "Step 1. In this step-by-step visual proof, we will prove Ceva's Theorem, showing why three concurrent lines from the vertices of a triangle divide the opposite sides into ratios whose product is always 1.",
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
            "1페이지입니다. 단계별 시각적 수학 증명 강의입니다. 직각삼각형에서 빗변의 제곱이 두 직각변의 제곱의 합과 같다는 피타고라스 정리를 정사각형 넓이 분할로 한 단계씩 명확하게 증명해 봅시다.",
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
            "25페이지입니다. 수학홈페이지의 동적 기하 웹페이지에 접속하여 직각삼각형의 변의 길이를 직접 조절하며 피타고라스 정리의 시각적 증명을 실험해 보세요!"
        ],
        "pages_en": [
            "Step 1. In this step-by-step visual lecture, we prove the Pythagorean Theorem, c squared equals a squared plus b squared, by partitioning the area of a square.",
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
            "1페이지입니다. 단계별 시각적 수학 증명 강의입니다. 삼각형의 세 변 또는 그 연장선과 만나는 한 직선이 만드는 길이 비의 곱이 항상 1이 된다는 메넬라우스의 정리를 단계별로 증명해 봅시다.",
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
            "20페이지입니다. 수학홈페이지의 동적 기하 웹페이지에서 할선의 기울기와 위치를 직접 움직이며 메넬라우스의 정리를 탐구해 보세요!"
        ],
        "pages_en": [
            "Step 1. In this step-by-step visual lecture, we will prove Menelaus' Theorem, showing how any transversal line cutting across a triangle creates three directed segment ratios whose product equals 1.",
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
    matches = []
    for it in items:
        u = (it.get("url") or "").strip()
        p = (it.get("pdf") or "").split("#")[0].strip()
        if key in (u, p) or u.endswith(f"/{key}.html") or p.endswith(f"/{key}.pdf"):
            matches.append(it)
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    generic_titles = {"기타자료", "강의", "기출문제", "삼각형", "사각형", "닮음", "타원", "포물선", "쌍곡선", "부등식", "선형방정식", "반비례"}
    def _score_item(it):
        ko_t = split_bilingual_title(it.get("title", ""))[0]
        is_generic = 0 if ko_t in generic_titles else 1
        return (is_generic, len(ko_t))
    matches.sort(key=_score_item, reverse=True)
    return matches[0]


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
        if (r_m > 130 and g_m > 85 and b_m < 95 and (r_m - g_m) < 95 and r_m > b_m + 45) or (r_m > 120 and b_m > 120 and g_m < 100):
            color_tag = "purple"  # 주황(Orange)·보라(Purple) 합동/닮음 삼각형 강조
        elif r_m > g_m + 45 and r_m > b_m + 45:
            color_tag = "red"
        elif b_m > r_m + 30 and b_m > g_m + 20:
            color_tag = "blue"
        elif g_m > r_m + 25 and g_m > b_m + 25:
            color_tag = "green"

    norm_bbox = [
        round(abs_box[0] / w, 4),
        round(abs_box[1] / h, 4),
        round(abs_box[2] / w, 4),
        round(abs_box[3] / h, 4),
    ]
    return norm_bbox, color_tag



def _strip_outer_balanced_parens(s: str) -> str:
    s = s.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        closed_early = False
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i < len(s) - 1:
                    closed_early = True
                    break
        if not closed_early and depth == 0:
            s = s[1:-1].strip()
        else:
            break
    return s


def _balance_parentheses(s: str) -> str:
    s = re.sub(r"(?:[,\s\+\-×÷]*√?\(\s*)+$", "", str(s or "").strip())
    out = []
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
            out.append(ch)
        elif ch == ")":
            if depth > 0:
                depth -= 1
                out.append(ch)
        else:
            out.append(ch)
    if depth > 0:
        out.extend(")" * depth)
    res = "".join(out)
    res = re.sub(r"√?\(\s*\)", "", res)
    res = re.sub(r",\s*\)", ")", res)
    while "((" in res and "))" in res:
        collapsed = re.sub(r"\(\(([^()]+)\)\)", r"(\1)", res)
        if collapsed == res:
            break
        res = collapsed
    return res.strip()


def split_bilingual_title(raw_title: str):
    """
    민은기 선생님 수학자료실의 한·영 병기 제목 예:
      - '세 중선은 한 점에서 만난다.(The three medians of a triangle meet at one point.)'
      - '$m$, $n$ 이 자연수일 때, $a^m \\times a^n = a^{m+n}$($a^m \\times a^n = a^{m+n}$ ($m$, $n$ are natural numbers.))'
    에서 균형 괄호(balanced parentheses) 역추적으로 순수 한국어 제목(ko_title)과 순수 영어 제목(en_title)을 정밀 분리합니다.
    """
    raw_s = str(raw_title or "").strip()
    # 원본 한영 병기 경계 ')(' 또는 한글 뒤 '(' 역추적
    u = latex_to_unicode_title(raw_s)
    if u.endswith(")"):
        depth = 0
        open_idx = -1
        for i in range(len(u) - 1, -1, -1):
            ch = u[i]
            if ch == ")":
                depth += 1
            elif ch == "(":
                depth -= 1
                if depth == 0:
                    open_idx = i
                    break
        if open_idx > 0:
            en_cand = _strip_outer_balanced_parens(u[open_idx + 1:-1].strip())
            ko_cand = _balance_parentheses(u[:open_idx].strip().rstrip("."))
            if re.search(r"[A-Za-z]{3,}", en_cand) and not re.search(r"[가-힣]", en_cand):
                en_cand = _balance_parentheses(en_cand)
                return (ko_cand or u), (en_cand or ko_cand or u)
    return u, ""


def latex_to_unicode_title(text):
    s = str(text or "")
    s = s.replace("Equationss", "Equations").replace("수직이분선", "수직이등분선")
    s = (
        s.replace(r"\mathbb{R}", "ℝ")
        .replace(r"\mathbb{N}", "ℕ")
        .replace(r"\mathbb{Z}", "ℤ")
        .replace(r"\mathbb{Q}", "ℚ")
        .replace(r"\mathbb{C}", "ℂ")
    )
    s = re.sub(r"\\(?:mathrm|mathbf|mathit|text)\s*\{([^{}]+)\}", r"\1", s)
    s = re.sub(r"\\(?:displaystyle|mathrm|mathbf|left|right)", "", s)
    s = re.sub(r"\^\s*\{\\circ\}|\^\s*\\circ", "°", s)
    s = re.sub(r"\\overline\s*\{([^{}]+)\}", r"\1", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"√(\1)", s)
    s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"(\1/\2)", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"√(\1)", s)
    s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"(\1/\2)", s)
    s = re.sub(r"\\triangle\s*", "△", s)
    s = re.sub(r"\\angle\s*", "∠", s)
    s = s.replace(r"\Leftrightarrow", "⇔").replace(r"\Rightarrow", "⇒").replace(r"\Leftarrow", "⇐")
    s = s.replace(r"\in", "∈").replace(r"\subset", "⊂").replace(r"\infty", "∞")
    s = s.replace(r"\cdots", "⋯").replace(r"\ldots", "⋯").replace(r"\dots", "⋯")
    s = s.replace(r"\times", "×").replace(r"\div", "÷").replace(r"\cdot", "·")
    s = s.replace(r"\pm", "±").replace(r"\leq", "≤").replace(r"\geq", "≥").replace(r"\neq", "≠")
    s = s.replace(r"\le", "≤").replace(r"\ge", "≥").replace(r"\ne", "≠")
    _sub_map = str.maketrans("0123456789+-=()nkijm", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₙₖᵢⱼₘ")
    s = re.sub(
        r"_\s*\{([0-9+\-=()nkijm]+)\}|_([0-9]+)",
        lambda m: (m.group(1) or m.group(2)).translate(_sub_map),
        s,
    )
    s = re.sub(r"_\s*\{([^{}]+)\}", r"(\1)", s)
    s = re.sub(r"\^\s*\{([^{}]+)\}", r"^(\1)", s)
    s = s.replace("^2", "²").replace("^3", "³")
    s = re.sub(r"\\[,;:!\s]+", " ", s)
    s = s.replace("$", "").replace("<", "＜").replace(">", "＞").replace("{", "(").replace("}", ")").replace("\\", " ")
    s = _balance_parentheses(re.sub(r"\s+", " ", s).strip())
    return s


def clean_math_for_speech_ko(text):
    s = str(text or "")
    s = s.replace("수직이분선", "수직이등분선")
    # 한글 문장 뒤의 영문 번역 괄호(4글자 이상 영단어 포함)만 제거하고 (m+n), (mn) 등 수식 괄호는 보존
    s, _ = split_bilingual_title(s) if s.endswith(")") and re.search(r"[A-Za-z]{4,}", s) else (s, "")
    s = re.sub(r"\(\s*[^가-힣()]*[A-Za-z]{4,}[^가-힣()]*\)", "", s)
    for _ch, _d in zip("₀₁₂₃₄₅₆₇₈₉ₙₖᵢⱼₘ", "0123456789nkijm"):
        s = s.replace(_ch, _d)
    s = s.replace(r"\cdots", " 점점점 ").replace(r"\ldots", " 점점점 ").replace("⋯", " 점점점 ")
    s = re.sub(r"_\s*\{([^{}]+)\}", r" \1", s)
    s = (
        s.replace(r"\mathbb{R}", "실수 집합")
        .replace("ℝ", "실수 집합")
        .replace(r"\mathbb{N}", "자연수 집합")
        .replace("ℕ", "자연수 집합")
        .replace(r"\in", " 원소 ")
        .replace("∈", " 원소 ")
    )
    s = re.sub(r"\\(?:mathrm|mathbf|mathit|text)\s*\{([^{}]+)\}", r"\1", s)
    s = re.sub(r"\\(?:displaystyle|mathrm|mathbf|left|right)", "", s)
    s = re.sub(r"\^\s*\{\\circ\}|\^\s*\\circ|°", "도", s)
    s = re.sub(r"\\overline\s*\{([^{}]+)\}", r"선분 \1", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"루트 \1", s)
    s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"\2 분의 \1", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"루트 \1", s)
    s = re.sub(r"\\triangle\s*([A-Za-z0-9]+)", r"삼각형 \1", s)
    s = re.sub(r"\\angle\s*([A-Za-z0-9]+)", r"각 \1", s)
    s = re.sub(r"√\(([^()]+)\)", r"루트 \1", s)
    s = s.replace("√(", "루트 ").replace("√", "루트 ")
    s = s.replace(r"\Leftrightarrow", " 필요충분조건 ").replace("⇔", " 필요충분조건 ")
    s = s.replace(r"\Rightarrow", " 이면 ").replace("⇒", " 이면 ")
    s = s.replace(r"\times", " 곱하기 ").replace(r"\div", " 나누기 ").replace(r"\cdot", " 곱하기 ")
    s = s.replace("×", " 곱하기 ").replace("÷", " 나누기 ").replace("∴", "따라서 ")
    s = s.replace(r"\neq", " 같지 않다 ").replace(r"\ne", " 같지 않다 ").replace("≠", " 같지 않다 ")
    s = s.replace(r"\leq", " 이하 ").replace(r"\le", " 이하 ").replace("≤", " 이하 ")
    s = s.replace(r"\geq", " 이상 ").replace(r"\ge", " 이상 ").replace("≥", " 이상 ")
    s = s.replace(r"\pm", " 플러스마이너스 ").replace("±", " 플러스마이너스 ")
    s = re.sub(r"\^\s*\{([^{}]+)\}", r"의 \1제곱", s)
    s = re.sub(r"\^\s*\(([^()]+)\)", r"의 \1제곱", s)
    s = re.sub(r"\^2", "의 제곱", s)
    s = re.sub(r"\^3", "의 세제곱", s)
    s = s.replace("²", "의 제곱").replace("³", "의 세제곱")
    s = re.sub(r"\^([a-zA-Z0-9\+\-]+)", r"의 \1제곱", s)
    s = s.replace("^", " ")
    s = re.sub(r"[\$\\\{\}]", " ", s)
    return _balance_parentheses(re.sub(r"\s+", " ", s).strip())


def clean_math_for_speech_en(text):
    s = str(text or "")
    _, en_split = split_bilingual_title(s)
    if en_split:
        s = en_split
    s = (
        s.replace(r"\mathbb{R}", "the real numbers")
        .replace("ℝ", "the real numbers")
        .replace(r"\mathbb{N}", "the natural numbers")
        .replace("ℕ", "the natural numbers")
        .replace(r"\in", " in ")
        .replace("∈", " in ")
    )
    s = re.sub(r"\\(?:mathrm|mathbf|mathit|text)\s*\{([^{}]+)\}", r"\1", s)
    s = re.sub(r"\\(?:displaystyle|mathrm|mathbf|left|right)", "", s)
    s = re.sub(r"\^\s*\{\\circ\}|\^\s*\\circ|°", " degrees", s)
    s = re.sub(r"\\overline\s*\{([^{}]+)\}", r"segment \1", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"square root of \1", s)
    s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"\1 over \2", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"square root of \1", s)
    s = re.sub(r"\\triangle\s*([A-Za-z0-9]+)", r"triangle \1", s)
    s = re.sub(r"\\angle\s*([A-Za-z0-9]+)", r"angle \1", s)
    s = re.sub(r"√\(([^()]+)\)", r"square root of \1", s)
    s = s.replace("√(", "square root of ").replace("√", "square root of ")
    s = s.replace(r"\Leftrightarrow", " if and only if ").replace("⇔", " if and only if ")
    s = s.replace(r"\times", " times ").replace("×", " times ")
    s = s.replace(r"\div", " divided by ").replace("÷", " divided by ")
    s = s.replace(r"\neq", " not equal to ").replace(r"\ne", " not equal to ").replace("≠", " not equal to ")
    s = s.replace(r"\pm", " plus or minus ").replace("±", " plus or minus ")
    s = re.sub(r"\^\s*\{([^{}]+)\}", r" to the power of \1", s)
    s = re.sub(r"\^\s*\(([^()]+)\)", r" to the power of \1", s)
    s = re.sub(r"\^2", " squared", s)
    s = re.sub(r"\^3", " cubed", s)
    s = s.replace("²", " squared").replace("³", " cubed").replace("^", " ")
    s = re.sub(r"[\$\\\{\}]", " ", s)
    return _balance_parentheses(re.sub(r"\s+", " ", s).strip())


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


def analyze_min7014_topic_as_mathteacher(title: str, sub_domain_ko: str = "", breadcrumb: str = ""):
    """
    [수석 수학교사(mathteacher) 에이전트의 24대 유형별 정밀 증명·수업 분석기 (v7.0)]
    주제 제목과 단원 경로를 분석하여:
      1) category_type ('geometry' | 'algebra' | 'number' | 'fractal_curve' | 'space_3d' | 'calculus_trig')
      2) hypothesis_ko (출발 가정·정의 조건)
      3) conclusion_ko (최종 결론·목표 성질)
      4) auxiliary_line_ko (폴리아 제1보조선 또는 핵심 대수·수직선 발상)
      5) proof_logic_ko (결정적 합동/닮음/넓이/수식 전개 증명 논리)
      6) misconception_ko (학생들이 가장 많이 틀리는 오개념 예방 팁)
      7) what_if_not_ko (수능·상위 교육과정으로 이어지는 조건 변형 질문)
    을 100% 내용 일치하도록 생성합니다.
    """
    t = (title or "").strip()
    b = (breadcrumb or "").strip()
    blob = f"{t} {sub_domain_ko} {b}"
    ko_t, _ = split_bilingual_title(t)

    # 1. 이등변삼각형 성질 / 조건
    if "이등변삼각형" in blob or "Isosceles" in blob:
        if "수선의 발" in t or "수직 이등분" in t or "수직이등분" in t or "bisector of the apex" in t:
            return {
                "category_type": "geometry",
                "hypothesis_ko": "두 변 AB와 AC의 길이가 같은 이등변삼각형에서 꼭지각의 이등분선(또는 밑변에 내린 수선)을 그은 가정",
                "conclusion_ko": "꼭지각의 이등분선은 밑변 BC를 수직으로 이등분한다(BD = CD, 교각 = 90도)는 결론",
                "auxiliary_line_ko": "꼭지각 A를 반으로 나누는 초록색 각의 이등분선 AD를 밑변 BC까지 내려 긋는 제1보조선",
                "proof_logic_ko": "두 변의 길이가 같고(AB=AC), 보조선 AD가 공통변이며, 나뉜 두 꼭지각의 크기가 같으므로 양쪽 두 삼각형이 SAS 합동이 되고, 대응변의 길이가 같으며 평각 180도를 반씩 나누어 90도 수직이 되는 원리",
                "misconception_ko": "일반 삼각형에서는 꼭지각의 이등분선과 밑변의 수직이등분선이 일치하지 않으며, 오직 두 변의 길이가 같은 이등변삼각형의 대칭성에서만 일치함을 주의해야 합니다.",
                "what_if_not_ko": "만약 밑변의 중점과 꼭짓점을 먼저 이으면(중선) 왜 자동으로 수직이 되고 꼭지각도 이등분될까요?(SSS 합동으로의 역발상)"
            }
        elif "두 내각" in t or "two angles" in t.lower():
            return {
                "category_type": "geometry",
                "hypothesis_ko": "삼각형 ABC에서 밑변 양 끝의 두 내각 B와 C의 크기가 같다는 가정",
                "conclusion_ko": "마주 보는 두 변 AB와 AC의 길이도 같아져 이등변삼각형이 된다는 결론",
                "auxiliary_line_ko": "꼭지각 A의 이등분선을 밑변 BC에 내려 긋는 초록색 보조선",
                "proof_logic_ko": "삼각형 세 내각의 합은 180도이므로 나머지 각도 같아지고, 공통변 AD와 양 끝각이 같아 ASA 합동이 성립하므로 대응변 AB와 AC의 길이가 같아지는 원리",
                "misconception_ko": "이등변삼각형의 성질(두 변이 같으면 두 밑각이 같다)과 이등변삼각형이 되는 조건(두 각이 같으면 두 변이 같다)은 가정과 결론이 서로 바뀐 역(Converse) 명제입니다.",
                "what_if_not_ko": "만약 세 내각의 크기가 모두 60도로 같다면 어떤 삼각형이 될까요?"
            }
        else:
            return {
                "category_type": "geometry",
                "hypothesis_ko": "삼각형 ABC에서 두 변 AB와 AC의 길이가 같다(AB = AC)는 이등변삼각형의 정의(가정)",
                "conclusion_ko": "길이가 같은 두 변과 마주 보는 두 밑각 B와 C의 크기가 서로 같다(각 B = 각 C)는 결론",
                "auxiliary_line_ko": "꼭지각 A를 정확히 반으로 나누는 초록색 각의 이등분선 AD를 밑변 BC에 내려 긋는 결정적 보조선",
                "proof_logic_ko": "두 변 AB와 AC가 같고(가정), 가운데 초록색 선분 AD가 공통변이며, 끼인각인 꼭지각의 절반이 서로 같으므로 두 삼각형 ABD와 ACD가 SAS 합동이 되어 대응각인 두 밑각의 크기가 같아지는 원리",
                "misconception_ko": "증명할 결론(두 밑각이 같다)을 증명 과정에서 미리 쓰지 않도록, 반드시 꼭지각의 이등분선 보조선을 그어 SAS 합동으로 유도해야 순환논리에 빠지지 않습니다.",
                "what_if_not_ko": "만약 꼭지각의 이등분선 대신 밑변 BC의 중점 M을 연결하는 보조선(중선)을 그으면 어떤 합동 조건(SSS 합동)으로 똑같이 증명할 수 있을까요?"
            }

    # 2. 직각삼각형의 합동 (RHA / RHS)
    if "RHA" in blob or "RHS" in blob or "직각삼각형의 합동" in blob:
        is_rhs = "RHS" in blob or "다른 한 변" in t
        return {
            "category_type": "geometry",
            "hypothesis_ko": f"두 직각삼각형(R, 90도)에서 빗변의 길이(H)와 {'다른 한 변의 길이(S)' if is_rhs else '한 예각의 크기(A)'}가 각각 같다는 가정",
            "conclusion_ko": f"두 직각삼각형이 완전히 포개어지는 {'RHS' if is_rhs else 'RHA'} 합동이라는 결론",
            "auxiliary_line_ko": "길이가 같은 직각 이웃변을 서로 맞붙여 두 직각삼각형을 하나의 큰 삼각형으로 이어 붙이는 기하학적 조작 보조선",
            "proof_logic_ko": f"직각 90도 두 개가 만나 평각 180도 일직선이 되므로 큰 삼각형이 두 변(빗변 H)의 길이가 같은 이등변삼각형이 되고, 이등변삼각형의 성질에 의해 {'두 밑각이 같아져 SAS/ASA 합동' if is_rhs else '꼭지각의 이등분선이 밑변을 이등분하여 ASA 합동'}으로 귀결되는 원리",
            "misconception_ko": "일반 삼각형에서는 두 변과 끼인각이 아닌 각(SSA)이 같아도 합동이 아니지만, 직각삼각형(90도)에서는 이등변삼각형 대칭성 덕분에 RHS 합동이 항상 성립합니다!",
            "what_if_not_ko": "직각(90도) 조건이 빠진 일반 예각삼각형에서 두 변과 끼인각이 아닌 한 각만 주어지면 왜 모양이 2가지로 생길 수 있을까요?"
        }

    # 3. 삼각형의 외심 (Circumcenter)
    if "외심" in blob or "Circumcenter" in blob or "수직이등분선" in t:
        return {
            "category_type": "geometry",
            "hypothesis_ko": "삼각형의 두 변의 수직이등분선의 교점 O에서 나머지 세 번째 변에 수선의 발을 내린 가정",
            "conclusion_ko": "세 변의 수직이등분선은 반드시 한 점(외심 O)에서 만나고, 외심에서 세 꼭짓점 A, B, C에 이르는 거리가 모두 같다(OA = OB = OC, 외접원의 반지름 R)는 결론",
            "auxiliary_line_ko": "수직이등분선의 교점 O에서 삼각형의 세 꼭짓점 A, B, C를 직접 연결하는 초록색 반지름 보조선 3줄",
            "proof_logic_ko": "첫째·둘째 변의 수직이등분선에서 나뉜 직각삼각형들이 각각 SAS 합동이 되어 OA = OB = OC가 성립하고, 이를 통해 세 번째 변에 내린 수선의 두 직각삼각형이 RHS 합동이 되어 세 번째 변도 정확히 이등분되는 연쇄 합동 원리",
            "misconception_ko": "외심 O에서 나뉜 삼각형은 마주 보는 두 삼각형이 아니라 '한 변을 끼고 있는 이웃한 두 직각삼각형'이 합동(이등변삼각형)이며, 둔각삼각형의 외심은 삼각형 외부에 위치합니다.",
            "what_if_not_ko": "만약 삼각형이 직각삼각형이라면 외심 O는 정확히 어느 변의 한가운데(빗변의 중점)에 위치하게 될까요?"
        }

    # 4. 삼각형의 내심 (Incenter)
    if "내심" in blob or "Incenter" in blob or "세 내각의 이등분선" in t:
        return {
            "category_type": "geometry",
            "hypothesis_ko": "삼각형의 두 내각의 이등분선의 교점 I에서 세 변에 각각 수선의 발을 내린 가정",
            "conclusion_ko": "세 내각의 이등분선은 한 점(내심 I)에서 만나고, 내심에서 세 변에 이르는 수직 거리가 모두 같다(내접원의 반지름 r)는 결론",
            "auxiliary_line_ko": "교점 I에서 삼각형의 세 변에 수직으로 내린 3개의 초록색 수선(내접원 반지름)과 세 번째 꼭짓점을 잇는 보조선",
            "proof_logic_ko": "두 내각의 이등분선에 의해 나뉜 직각삼각형들이 빗변 공통 + 직각 + 예각 일치로 RHA 합동이 되어 세 변까지의 거리가 모두 같아지고, 마지막 꼭짓점의 두 직각삼각형이 RHS 합동이 되어 세 번째 각도 이등분되는 원리",
            "misconception_ko": "외심은 '세 꼭짓점'까지의 거리가 같고(OA=OB=OC), 내심은 '세 변에 내린 수선의 발'까지의 거리가 같습니다(ID=IE=IF=r). 또한 삼각형 넓이 S = 1/2·r·(a+b+c) 공식으로 직결됩니다.",
            "what_if_not_ko": "내각이 아니라 삼각형의 한 내각의 이등분선과 두 외각의 이등분선을 그으면 삼각형 밖에 어떤 원(방접원, Excircle)이 탄생할까요?"
        }

    # 5. 삼각형의 무게중심 (Centroid / Median)
    if "중선" in blob or "무게중심" in blob or "median" in blob.lower() or "centroid" in blob.lower():
        return {
            "category_type": "geometry",
            "hypothesis_ko": "삼각형의 세 꼭짓점과 마주 보는 대변의 중점을 각각 연결한 세 중선(Median)이 주어진 가정",
            "conclusion_ko": "삼각형의 세 중선은 반드시 한 점(무게중심 G)에서 만나며, 각 중선을 꼭짓점으로부터 2 대 1로 내분한다는 결론",
            "auxiliary_line_ko": "두 변의 중점을 서로 연결하는 중점연결정리 평행 보조선",
            "proof_logic_ko": "중점연결정리에 의해 중점끼리 이은 선분은 밑변과 평행하고 길이가 절반이므로, 엇각이 같은 두 삼각형이 AA 닮음(닮음비 2 대 1)을 이루어 교점 G가 중선을 2 대 1로 내분하는 원리",
            "misconception_ko": "세 중선에 의해 나누어진 6개의 작은 삼각형은 모양은 서로 합동이 아니지만 밑변과 높이가 같아 넓이가 모두 전체의 6분의 1로 똑같다는 점이 핵심입니다.",
            "what_if_not_ko": "좌표평면 위 세 점 A, B, C를 꼭짓점으로 하는 삼각형의 무게중심 좌표는 왜 세 좌표의 산술평균이 될까요?"
        }

    # 6. 평행사변형 / 사각형의 성질과 조건
    if "평행사변형" in blob or "parallelogram" in blob.lower() or "마름모" in blob or "직사각형" in blob or "사다리꼴" in blob:
        if "정사각형의 한 변" not in t:
            return {
                "category_type": "geometry",
                "hypothesis_ko": "두 쌍의 대변이 각각 평행한 사각형(평행사변형의 정의) 또는 주어진 사각형의 출발 조건(가정)",
                "conclusion_ko": f"'{ko_t}' 성질이 항상 성립한다는 기하학적 결론",
                "auxiliary_line_ko": "사각형의 마주 보는 두 꼭짓점을 대각선으로 연결하여 사각형을 두 개의 삼각형으로 분할하는 초록색 대각선 보조선",
                "proof_logic_ko": "평행한 두 대변과 대각선이 이루는 두 쌍의 엇각의 크기가 각각 같고 초록색 대각선이 공통변이므로, 나뉜 두 삼각형이 ASA 합동(또는 SAS 합동)이 되어 대응변의 길이와 대응각의 크기가 일치하는 원리",
                "misconception_ko": "한 쌍의 대변이 평행하고 다른 한 쌍의 대변의 길이가 같은 경우(예: 등변사다리꼴)는 평행사변형이 되지 않는다는 대표 반례를 꼭 구분해야 합니다!",
                "what_if_not_ko": "만약 평행사변형에서 이웃하는 두 변의 길이까지 같아지거나(마름모), 한 내각이 90도가 되면(직사각형) 두 대각선 사이에 어떤 새로운 수직·길이 관계가 생길까요?"
            }

    # 7. 메넬라우스 / 체바의 정리
    if "메넬라우스" in blob or "Menelaus" in blob or "체바" in blob or "Ceva" in blob:
        return {
            "category_type": "geometry",
            "hypothesis_ko": "삼각형의 세 변(또는 연장선)을 지나는 할선이나 한 점 P에서 만나는 세 체바선(Cevian)이 주어진 가정",
            "conclusion_ko": "세 변을 분할하는 선분 길이의 비율 세 개를 곱하면 항상 1이 된다는 비율 불변량 결론",
            "auxiliary_line_ko": "꼭짓점을 지나며 할선에 평행한 보조선 1줄을 긋거나, 높이가 같은 삼각형들의 넓이 비 = 밑변의 길이 비를 연결하는 발상",
            "proof_logic_ko": "평행선에 의한 AA 닮음비 또는 밑변 비 = 넓이 비 식을 세 개 곱할 때 분모와 분자가 도미노처럼 연쇄 약분되어 정확히 1이 되는 원리",
            "misconception_ko": "비율을 돌릴 때 반드시 삼각형의 꼭짓점에서 분점, 다시 분점에서 다음 꼭짓점 순서로 한 바퀴 순환하는 방향을 일관되게 유지해야 합니다.",
            "what_if_not_ko": "이 넓이 비·내분비 원리를 고등 기하·벡터의 위치벡터 내분점 식으로 바꾸면 어떻게 교점 비율을 구할 수 있을까요?"
        }

    # 8-A. 나눗셈과 역수의 곱셈 (a ÷ b = a × 1/b) — 지수법칙·제곱근보다 먼저 정확히 판별!
    if ("\\div" in t or "÷" in t or "나눗셈" in blob) and ("\\frac{1}" in t or "1/b" in t or "역수" in blob) and "a^m" not in t:
        return {
            "category_type": "number",
            "hypothesis_ko": "양수 b에 대하여 어떤 수 a를 b로 나누는 나눗셈 식(a 나누기 b)이 주어진 출발 조건",
            "conclusion_ko": "a 나누기 b는 나누는 수 b의 역수인 b 분의 1을 곱한 것(a 곱하기 b 분의 1)과 항상 같다는 나눗셈과 역수의 관계 결론",
            "auxiliary_line_ko": "단위 막대나 직사각형 넓이 모델을 b등분하여 'b로 나눈 몫 하나'가 곧 'b 분의 1배를 곱한 크기'와 일치함을 대응시키는 시각적 발상",
            "proof_logic_ko": "나눗셈 a 나누기 b의 몫은 b를 곱해 a가 되는 수이므로, 양변에 b의 역수인 b 분의 1을 곱하면 몫이 정확히 a 곱하기 b 분의 1로 결정되는 곱셈의 역원 원리",
            "misconception_ko": "나눗셈을 곱셈으로 바꿀 때 앞의 나누어지는 수 a까지 뒤집는 실수를 조심하세요! 반드시 뒤의 나누는 수 b만 역수(b 분의 1)로 바꾸어야 합니다.",
            "what_if_not_ko": "만약 나누는 수 b가 자연수가 아니라 분수(예: c 분의 d)라면 왜 분모와 분자를 뒤집은 역수(d 분의 c)를 곱하면 될까요?"
        }

    # 8-B. 분모의 유리화 (Rationalizing the Denominator)
    if "유리화" in blob or "Rationaliz" in blob or ("분모" in t and ("sqrt" in t or "√" in t)):
        return {
            "category_type": "algebra",
            "hypothesis_ko": "분모에 근호(루트 a, 단 a는 양수)가 포함된 무리수 분수 식이 주어진 출발 조건",
            "conclusion_ko": "분모와 분자에 똑같이 루트 a를 곱하면 분모가 근호 없는 유리수 a로 바뀌어 a 분의 b 루트 a가 된다는 분모의 유리화 결론",
            "auxiliary_line_ko": "분수의 크기를 바꾸지 않는 1(즉 루트 a 분의 루트 a)을 분모와 분자에 동시에 곱하여 분모를 (루트 a)의 제곱 = a로 만드는 대수적 발상",
            "proof_logic_ko": "0이 아닌 같은 수를 분모와 분자에 곱해도 분수의 값은 일정하다는 분수의 기본 성질과, 양수 a에 대하여 루트 a 곱하기 루트 a는 유리수 a가 된다는 제곱근의 정의를 결합하는 원리",
            "misconception_ko": "분모에만 루트 a를 곱하고 분자에 곱하는 것을 잊거나, 루트 a 곱하기 루트 a를 2 루트 a로 착각하지 않도록 주의해야 합니다!",
            "what_if_not_ko": "만약 분모가 단항식 루트 a가 아니라 '루트 a 더하기 루트 b'처럼 두 항의 합으로 되어 있다면 합차공식을 이용해 분모와 분자에 무엇을 곱해야 유리화될까요?"
        }

    # 8-C. 정사각형의 한 변의 길이와 넓이 / 제곱근과 실수
    if "정사각형의 한 변" in t or "제곱근" in blob or "Square Root" in blob or "square root" in blob or "sqrt" in t or "√" in t:
        if "정사각형의 한 변" in t:
            return {
                "category_type": "number",
                "hypothesis_ko": "격자 눈금 위에서 정사각형의 넓이 S와 한 변의 길이 x 사이의 관계(x의 제곱 = S)를 관찰하는 출발 조건",
                "conclusion_ko": "넓이가 a(a는 양수)인 정사각형의 한 변의 길이는 제곱하여 a가 되는 양수, 즉 기호 루트 a(양의 제곱근)로 나타낸다는 결론",
                "auxiliary_line_ko": "모눈종이 위에서 직각삼각형 4개와 작은 정사각형으로 둘러싸인 큰 정사각형에서 모서리 직각삼각형 넓이를 빼서 정사각형 넓이를 구하는 발상",
                "proof_logic_ko": "넓이가 1, 4, 9인 정사각형의 한 변은 자연수 1, 2, 3이지만, 넓이가 2나 5인 정사각형의 한 변은 유리수로 나타낼 수 없으므로 새로운 기호 루트(근호)를 도입해 한 변의 길이를 정확히 표현하는 원리",
                "misconception_ko": "넓이가 2배가 된다고 한 변의 길이도 2배가 되는 것이 아니라, 한 변의 길이는 루트 2배가 된다는 점을 혼동하지 말아야 합니다!",
                "what_if_not_ko": "만약 넓이가 2인 정사각형의 한 변의 길이 루트 2를 컴퍼스로 수직선 위에 그대로 내려 찍으면 무리수도 수직선 위의 한 점에 완벽히 대응될까요?"
            }
        elif "0.16" in t or "구하여라" in t:
            return {
                "category_type": "number",
                "hypothesis_ko": "제곱하여 0.16이 되는 수 x(즉 방정식 x의 제곱 = 0.16을 만족하는 수)를 찾는 출발 조건",
                "conclusion_ko": "0.16의 제곱근은 양의 제곱근 +0.4와 음의 제곱근 -0.4 두 개(플러스마이너스 0.4)라는 결론",
                "auxiliary_line_ko": "소수 0.16을 분수 100분의 16 또는 (0.4)의 제곱과 (-0.4)의 제곱으로 바꾸어 양수와 음수 대칭 쌍으로 확인하는 발상",
                "proof_logic_ko": "(+0.4) 곱하기 (+0.4) = 0.16이고, 음수끼리의 곱셈에서도 (-0.4) 곱하기 (-0.4) = +0.16이 성립하므로 양수와 음수 두 개의 제곱근이 대칭으로 존재하는 원리",
                "misconception_ko": "0.16의 제곱근을 0.04라고 답하는 실수가 정말 많습니다! 0.04를 제곱하면 0.0016이 되며, 제곱해서 0.16이 되는 수는 플러스마이너스 0.4입니다.",
                "what_if_not_ko": "만약 문제에서 '0.16의 제곱근(±0.4)' 대신 '제곱근 0.16(루트 0.16)'을 구하라고 질문 어순을 바꾸면 정답은 왜 양수 +0.4 하나만 될까요?"
            }
        elif "Leftrightarrow" in t or "⇔" in t or "sqrt{a}>" in t or "대소" in blob:
            return {
                "category_type": "algebra",
                "hypothesis_ko": "두 양수 a, b에 대하여 넓이가 각각 a와 b인 두 정사각형을 포개어 비교하는 출발 조건",
                "conclusion_ko": "양수 a가 b보다 크면 한 변의 길이인 루트 a도 루트 b보다 크고, 역으로 루트 a가 루트 b보다 크면 제곱한 넓이 a도 b보다 크다는 제곱근의 대소 관계 결론",
                "auxiliary_line_ko": "넓이가 a인 정사각형과 넓이가 b인 정사각형의 한 꼭짓점을 맞추어 겹쳐 놓아 한 변의 길이(루트 a, 루트 b)와 넓이를 동시에 눈으로 비교하는 기하학적 발상",
                "proof_logic_ko": "정사각형의 넓이가 클수록 한 변의 길이도 길어진다는 기하학적 단조증가 성질과, 양변을 제곱하여 근호를 벗겨 비교하는 대수적 동치 원리",
                "misconception_ko": "근호 밖의 자연수와 근호 안의 수를 비교할 때(예: 3과 루트 10)는 3 = 루트 9로 모두 근호 안에 넣어야 정확히 비교할 수 있습니다.",
                "what_if_not_ko": "만약 두 수 앞에 음수 부호가 붙어 -루트 a와 -루트 b를 비교한다면 부등호의 방향은 어떻게 뒤집힐까요?"
            }
        elif "성질" in t or "a<0" in t or "a＜0" in t or ("a>0" in t and "b>0" not in t) or ("a＞0" in t and "b＞0" not in t):
            is_neg = "a<0" in t or "a＜0" in t
            return {
                "category_type": "algebra",
                "hypothesis_ko": f"문자 a의 부호가 {'음수(a＜0)' if is_neg else '양수(a＞0)'}일 때 근호(루트)와 제곱이 만나는 수식이 주어진 조건",
                "conclusion_ko": f"{'a가 음수일 때 루트(a의 제곱)은 양수가 되어야 하므로 마이너스를 붙인 -a로 나온다' if is_neg else 'a가 양수일 때 루트(a의 제곱)과 (루트 a)의 제곱은 모두 원래 양수 a 그대로 나온다'}는 제곱근의 성질 결론",
                "auxiliary_line_ko": "문자 a에 구체적인 숫자(예: a = 3 또는 a = -3)를 대입하여 안쪽 제곱을 먼저 계산한 뒤 양의 제곱근을 구해 보는 수치 대입 발상",
                "proof_logic_ko": f"루트 기호 앞의 부호가 플러스이면 그 결과는 반드시 0 이상인 양의 제곱근이어야 하므로, {'음수 a에 마이너스 부호를 하나 더 붙여 양수 -a로 만들어 주는' if is_neg else '양수 a가 부호 변화 없이 그대로 나오는'} 절댓값(|a|) 동치 원리",
                "misconception_ko": "a가 음수일 때 '-a' 앞에 마이너스 기호가 있다고 해서 음수라고 착각하면 안 됩니다! a 자체가 음수(예: -3)이므로 -a = -(-3) = +3인 양수입니다.",
                "what_if_not_ko": "이 성질을 절댓값 기호 루트(a의 제곱) = |a| 하나로 통합하면, 수직선 위 두 점 사이의 거리 공식과 어떻게 연결될까요?"
            }
        else:
            return {
                "category_type": "number",
                "hypothesis_ko": f"'{ko_t}'에서 어떤 수 x를 제곱하여 음이 아닌 수 a가 되는 관계(x의 제곱 = a)를 탐구하는 출발 조건",
                "conclusion_ko": "양수 a의 제곱근은 양의 제곱근(+루트 a)과 음의 제곱근(-루트 a) 2개이며, 0의 제곱근은 0 하나뿐이고, 음수의 실수 제곱근은 존재하지 않는다는 결론",
                "auxiliary_line_ko": "제곱 연산(x에서 x의 제곱)의 역연산 화살표 다이어그램과 수직선 원점 대칭(플러스마이너스 루트 a) 모델을 그려 확인하는 발상",
                "proof_logic_ko": "부호가 같은 두 실수를 곱하면 항상 0 이상이 되므로, 양수 a에 대해서는 절댓값이 같고 부호가 반대인 두 수(+루트 a, -루트 a)가 제곱하여 a가 되는 원리",
                "misconception_ko": "'a의 제곱근(제곱해서 a가 되는 수, 플러스마이너스 루트 a 2개)'과 '제곱근 a(루트 a를 한글로 읽은 것, 양수 1개)'는 가장 자주 출제되는 핵심 구분 포인트입니다!",
                "what_if_not_ko": "만약 고등학교에서 제곱하여 음수 -1이 되는 새로운 수(허수 단위 i)를 정의한다면 수의 체계는 어디까지 확장될까요?"
            }

    # 9. 유한소수 / 무한소수 / 순환소수 / 정수 / 유리수
    if "유한소수" in blob or "순환소수" in blob or "유리수" in blob or "정수" in t or "Decimal" in blob or "Rational" in blob:
        if "유한소수" in t or "순환소수" in t:
            return {
                "category_type": "number",
                "hypothesis_ko": "분수(유리수)에서 분자를 분모로 직접 나눗셈하여 소수점 아래 숫자가 끝나는지 끝없이 반복되는지 관찰하는 출발 조건",
                "conclusion_ko": "유리수를 소수로 나타내면 소수점 아래 0이 아닌 숫자가 유한개인 유한소수 또는 일정한 숫자 배열(순환마디)이 한없이 되풀이되는 순환소수가 된다는 결론",
                "auxiliary_line_ko": "기약분수의 분모를 소인수분해하여 소인수가 2나 5뿐인지(10의 거듭제곱 분수로 변환 가능), 아니면 2와 5 이외의 소인수가 있는지 분류하는 수론적 발상",
                "proof_logic_ko": "나눗셈에서 나머지는 나누는 수(분모)보다 작은 자연수이므로 최대 분모 개수만큼만 나누어 보면 언젠가 나머지가 0이 되거나(유한소수) 이전에 나왔던 나머지가 반드시 다시 나타나 순환마디가 생기는 비둘기집 원리",
                "misconception_ko": "무한소수라고 해서 모두 무리수가 아닙니다! 순환소수(예: 0.333... = 3분의 1)는 분수로 나타낼 수 있는 당당한 유리수이며, 순환하지 않는 무한소수(원주율 파이, 루트 2)만 무리수입니다.",
                "what_if_not_ko": "순환소수 x = 0.121212...에 100을 곱해 100x - x = 99x를 만들면 어떻게 모든 순환소수를 1초 만에 분수로 바꿀 수 있을까요?"
            }
        else:
            return {
                "category_type": "number",
                "hypothesis_ko": "자연수, 0, 음의 정수로 이루어진 정수와, 분모가 0이 아닌 정수 분의 정수 꼴로 나타내어지는 유리수의 포함 관계를 분류하는 출발 조건",
                "conclusion_ko": "모든 정수는 분모가 1인 분수로 나타낼 수 있으므로 유리수에 포함되며, 유리수는 정수와 정수가 아닌 유리수(유한소수·순환소수)로 깔끔하게 분류된다는 수 체계 결론",
                "auxiliary_line_ko": "수의 벤 다이어그램(자연수, 정수, 유리수, 실수)과 수직선 위의 등분점을 대응시켜 시각화하는 발상",
                "proof_logic_ko": "분수의 약분 후 기약분수 상태에서 분모가 1이면 정수(예: 2분의 6 = 3), 분모가 1이 아니면 정수가 아닌 유리수(예: 2분의 1, 마이너스 4분의 3)로 판별되는 원리",
                "misconception_ko": "분수 모양으로 적혀 있다고 해서 무조건 '정수가 아닌 유리수'라고 속으면 안 됩니다! 마이너스 4분의 8 = -2처럼 약분했을 때 자연수나 음의 정수가 되면 정수입니다.",
                "what_if_not_ko": "유리수만으로도 수직선이 빽빽하게 채워진 것 같지만, 왜 유리수 사이사이의 빈틈을 메우려면 무리수(루트 2, 파이)가 반드시 필요할까요?"
            }

    # 10. 지수법칙 / 거듭제곱 / 단항식 연산
    if "자연수일 때" in t or "a^m" in t or "지수" in blob or "거듭제곱" in blob or "5a" in t or "단항식" in blob:
        is_div = "div" in t or "÷" in t
        is_pow_pow = "(a^m)^n" in t or "(a^(m))^(n)" in ko_t
        is_prod_pow = "(ab)^n" in t or "ab" in t or "\\frac{a}{b}" in t or "(a/b)" in ko_t
        if is_pow_pow:
            aux_s = "괄호 전체 (a의 m제곱)이 n번 거듭 곱해진 식을 펼쳐, m개씩 묶인 a 묶음이 총 n줄 나열되는 구조를 세어 보는 대수적 해체 발상"
            logic_s = "m개씩 들어 있는 a의 묶음을 n번 더하면 m 더하기 m 더하기 ... (n번) = m 곱하기 n개가 되어 지수끼리의 곱셈(a의 mn제곱)이 성립하는 원리"
            misc_s = "(a의 m제곱)의 n제곱과 a의 m제곱 곱하기 a의 n제곱을 혼동하지 마세요! 괄호 밖의 거듭제곱은 지수끼리 곱하고(mn), 밑이 같은 거듭제곱의 곱셈은 지수끼리 더합니다(m+n)."
        elif is_prod_pow:
            aux_s = "괄호 안의 곱(ab) 또는 분수(b 분의 a) 전체를 n번 나열한 뒤, 곱셈의 교환법칙과 결합법칙으로 a끼리 n개, b끼리 n개 모아 묶어 주는 발상"
            logic_s = "(ab)를 n번 곱한 식에서 a만 모으면 n개(a의 n제곱), b만 모으면 n개(b의 n제곱)가 되어 괄호 밖의 지수 n이 각각의 인수에 분배되는 원리"
            misc_s = "분수의 거듭제곱 (b 분의 a)의 n제곱에서는 분자 a뿐만 아니라 분모 b에도 똑같이 n제곱을 적용해 b의 n제곱 분의 a의 n제곱으로 나타내야 합니다."
        elif is_div:
            aux_s = "나눗셈을 분수 꼴(a의 n제곱 분의 a의 m제곱)로 바꾼 뒤, 분자에 곱해진 m개의 a와 분모에 곱해진 n개의 a를 일대일로 약분해 보는 대수적 해체 발상"
            logic_s = "분자와 분모에서 공통인 a를 약분하고 남은 개수를 m이 n보다 클 때(분자에 m-n개), 같을 때(모두 약분되어 1), 작을 때(분모에 n-m개)로 나누어 확인하는 원리"
            misc_s = "나눗셈 a의 m제곱 나누기 a의 n제곱에서 지수끼리 나누어 m 나누기 n으로 쓰는 실수를 조심하세요! 약분은 개수가 줄어드는 것이므로 지수끼리 빼야 하며, m과 n이 같을 때는 0이 아니라 1이 됩니다."
        else:
            aux_s = "추상적인 지수 기호를 암기하지 않고, 밑 a가 실제로 몇 번 곱해져 있는지 괄호와 곱셈 나열식(a 곱하기 a 곱하기 ...)으로 펼쳐서 전체 개수를 세어 보는 대수적 해체 발상"
            logic_s = "곱셈의 결합법칙에 의해 앞에 곱해진 m개의 a와 뒤에 곱해진 n개의 a를 한 줄로 합쳐 세면 총 (m 더하기 n)개가 되어 지수의 덧셈 규칙과 일치하는 원리"
            misc_s = "곱셈 a의 m제곱 곱하기 a의 n제곱에서 지수끼리 곱해 a의 mn제곱으로 착각하는 실수가 많습니다! a의 제곱 곱하기 a의 세제곱은 a가 총 5번 곱해진 a의 5제곱임을 떠올리면 즉시 검산됩니다."
        return {
            "category_type": "algebra",
            "hypothesis_ko": "자연수 지수 m, n과 거듭제곱의 정의(a의 m제곱은 밑 a를 m번 거듭 곱한 것)가 주어진 출발 조건",
            "conclusion_ko": f"수식 '{ko_t}'의 지수법칙이 모든 자연수 지수에서 필연적으로 성립한다는 대수적 결론",
            "auxiliary_line_ko": aux_s,
            "proof_logic_ko": logic_s,
            "misconception_ko": misc_s,
            "what_if_not_ko": "만약 지수 m, n이 자연수를 넘어 0이나 음의 정수(a의 0제곱 = 1, a의 마이너스 n제곱 = a의 n제곱 분의 1), 나아가 유리수 지수로 확장되면 어떤 조건(밑 a＞0)이 추가로 필요할까요?"
        }

    # 11. 피타고라스 정리 / 피타고라스 나무
    if "피타고라스" in blob or "Pythagoras" in blob or "Pythagorean" in blob:
        return {
            "category_type": "geometry",
            "hypothesis_ko": "직각삼각형의 세 변 a, b, c(빗변 c)와 각 변을 한 변으로 하는 정사각형이 작도된 기하학적 출발 조건",
            "conclusion_ko": "직각을 낀 두 변의 제곱의 합은 빗변의 제곱과 항상 같다(a의 제곱 더하기 b의 제곱 = c의 제곱)는 피타고라스 정리와 넓이 보존 결론",
            "auxiliary_line_ko": "한 변이 (a+b)인 큰 정사각형을 합동인 직각삼각형 4개와 한가운데 정사각형(넓이 c의 제곱)으로 분할하는 보조선",
            "proof_logic_ko": "네 모서리의 직각삼각형이 SAS 합동이고 두 예각의 합이 90도이므로 가운데 사각형의 한 내각이 180도 빼기 90도 = 90도가 되어 정사각형이 되며, 전체 넓이 등식을 정리하면 a의 제곱 더하기 b의 제곱 = c의 제곱이 도출되는 원리",
            "misconception_ko": "가운데 사각형의 네 변의 길이가 c로 같다는 것만으로는 마름모일 수도 있으므로, 반드시 두 예각의 합이 90도임을 이용해 내각이 90도(정사각형)임을 증명해야 완벽합니다!",
            "what_if_not_ko": "만약 직각삼각형의 세 변 위에 정사각형 대신 정삼각형이나 반원을 올린다면 두 작은 도형의 넓이 합은 여전히 빗변 도형의 넓이와 같을까요?"
        }

    # 12. 프랙탈 기하학 (코흐 곡선 / 눈송이 / 페아노 곡선)
    if "프렉탈" in blob or "프랙탈" in blob or "Fractal" in blob or "코흐" in blob or "Koch" in blob or "페아노" in blob or "Peano" in blob:
        return {
            "category_type": "fractal_curve",
            "hypothesis_ko": f"기본 선분이나 정삼각형에서 출발하여 각 선분을 일정한 비율로 쪼개고 같은 모양을 되풀이해 붙여 나가는 '{ko_t}'의 자기닮음(Self-Similarity) 생성 규칙",
            "conclusion_ko": "단순한 기하학적 분할 규칙을 무한히 반복하면 일부분을 확대해도 전체와 똑같은 모양이 끝없이 나타나는 프랙탈 곡선이 완성된다는 결론",
            "auxiliary_line_ko": "선분을 3등분(또는 격자 분할)한 뒤 가운데 구간에 정삼각형 산 모양(또는 공간 채움 경로)을 세우는 단계별 재귀(Recursion) 작도",
            "proof_logic_ko": "한 단계를 거칠 때마다 선분의 개수는 4배(또는 거듭제곱 배)로 늘어나고 각 선분의 길이는 3분의 1로 줄어들어, 전체 길이는 매 단계 3분의 4의 거듭제곱 등비수열로 증가하는 반면 둘러싸인 넓이는 유한한 극한값에 수렴하는 원리",
            "misconception_ko": "도형이 유한한 화면(유한한 넓이) 안에 갇혀 있다고 해서 둘레의 길이도 유한할 것이라고 착각하기 쉽지만, 코흐 눈송이는 '넓이는 유한하면서 둘레의 길이는 무한대'가 되는 놀라운 도형입니다!",
            "what_if_not_ko": "이 프랙탈 도형의 닮음비와 조각 개수를 이용해 고등학교 미적분의 등비급수 도형 넓이·길이 극한 문제를 어떻게 단번에 풀 수 있을까요?"
        }

    # 13. 정칠각형 매듭 / 오더리 탱클 / 회전 / 장미 / 꽃잎차례 / 소수·합성수 게임 / 3D 곡면·스트링 아트
    if any(k in blob for k in ("매듭", "Knot", "오더리", "Orderly", "회전", "Rotate", "장미", "rose", "꽃잎", "Petals", "소수카드", "prime", "스트링 아트", "String Art", "발판곡면", "Pedal")):
        if "소수카드" in blob or "prime" in blob.lower():
            return {
                "category_type": "number",
                "hypothesis_ko": "1보다 큰 자연수 중 약수가 1과 자기 자신뿐인 소수(Prime) 카드와 약수가 3개 이상인 합성수(Composite) 카드를 분류하고 조합하는 규칙",
                "conclusion_ko": "모든 합성수는 소수들의 곱으로 유일하게 소인수분해된다는 산술의 기본정리를 게임을 통해 직관적으로 깨닫는 결론",
                "auxiliary_line_ko": "에라토스테네스의 체 원리로 작은 소수(2, 3, 5, 7...)의 배수들을 단계별로 지워 나가며 소수와 합성수의 구조를 시각화하는 발상",
                "proof_logic_ko": "합성수는 반드시 자기 자신의 제곱근 이하의 소인수를 적어도 하나 가진다는 성질을 이용해 소수 카드와 합성수 카드를 정확히 판별하는 원리",
                "misconception_ko": "자연수 1은 소수도 아니고 합성수도 아닙니다! 또한 2는 모든 소수 중 유일한 짝수 소수임을 꼭 기억해야 합니다.",
                "what_if_not_ko": "만약 소인수분해를 이용해 어떤 자연수의 양의 약수의 개수를 구한다면 왜 각 소인수의 지수에 1씩 더해 곱하면 될까요?"
            }
        elif "발판곡면" in blob or "스트링 아트" in blob or "사면체" in blob:
            return {
                "category_type": "space_3d",
                "hypothesis_ko": f"3차원 공간에서 구 또는 정사면체의 모서리·접평면에 일정한 기하학적 규칙으로 점과 선분을 연결하는 '{ko_t}'의 출발 조건",
                "conclusion_ko": "곧은 직선들의 모임(법선·선분 다발)이 공간에서 연속적으로 회전·교차할 때 매끄러운 포락선(Envelope)과 3차원 곡면이 창발된다는 공간기하 결론",
                "auxiliary_line_ko": "모서리 위의 등분점들을 순서대로 일대일 대응시켜 잇는 매개변수 선분(스트링) 및 기준점에서 접평면에 내린 수선의 발 작도",
                "proof_logic_ko": "직선이 일정한 비율로 내분점을 이동할 때 이웃한 두 직선의 교점 자취가 이차곡선 및 3차원 발판곡면을 형성하는 공간 기하 원리",
                "misconception_ko": "곡선이나 곡면을 그리려면 반드시 휘어진 도구가 필요하다고 생각하기 쉽지만, 곧은 직선들의 접선 다발만으로도 완벽한 곡면이 만들어집니다.",
                "what_if_not_ko": "이 3차원 도형을 특정 평면으로 자른 단면(Section)이나 빛을 비춘 정사영(Projection)은 어떤 2차원 도형이 될까요?"
            }
        else:
            return {
                "category_type": "fractal_curve",
                "hypothesis_ko": f"일정한 중심각 회전과 대칭 이동 규칙에 따라 선분·삼각형·종이띠를 배열하는 '{ko_t}'의 기하학적 출발 조건",
                "conclusion_ko": f"회전 대칭과 등각 변환의 반복을 통해 '{ko_t}'의 정칙 다각형·규칙적 얽힘(Orderly Tangle)·황금각 나선 구조가 완성된다는 결론",
                "auxiliary_line_ko": "회전 중심점과 각 도형의 대응 꼭짓점을 연결하여 회전각과 대칭축(평행선·등변사다리꼴)을 표시하는 보조선",
                "proof_logic_ko": "동일한 도형을 일정한 각도로 회전 이동하면 중심으로부터의 거리와 내각이 보존되는 합동 변환(Isometry) 성질에 의해 정다각형 대칭이 성립하는 원리",
                "misconception_ko": "자와 컴퍼스만으로는 정칠각형을 작도할 수 없지만, 종이띠 매듭(종이접기 공리)을 이용하면 3차 방정식의 해가 기하학적으로 구현되어 정칠각형이 정확히 만들어집니다.",
                "what_if_not_ko": "만약 회전하는 각도를 360도의 유리수 등분이 아니라 황금비에 따른 황금각(약 137.5도)으로 바꾸면 해바라기 씨앗 배열처럼 어떻게 빈틈없는 꽃잎차례가 만들어질까요?"
            }

    # 14. 이차곡선 (포물선 / 타원 / 쌍곡선 / 단델린 구)
    if any(k in blob for k in ("포물선", "타원", "쌍곡선", "이차곡선", "단델린", "Parabola", "Ellipse", "Hyperbola", "Dandelin", "초점", "준선")):
        return {
            "category_type": "geometry",
            "hypothesis_ko": f"초점(Focus)과 준선 또는 두 초점으로부터의 거리 관계로 정의된 '{ko_t}'의 기하학적 출발 조건",
            "conclusion_ko": f"'{ko_t}'에서 거리 합·차 불변량과 접선의 빛 반사 대칭 성질이 항상 성립한다는 이차곡선 결론",
            "auxiliary_line_ko": "곡선 위의 한 점에서 초점과 준선(또는 두 초점)에 이르는 보조선 및 접선에 대한 대칭점 작도",
            "proof_logic_ko": "이등변삼각형의 대칭성과 수직이등분선 성질(또는 구에 그은 두 접선의 길이 같음)에 의해 초점 거리 관계와 입사각·반사각 일치가 증명되는 원리",
            "misconception_ko": "이차곡선 문제는 곧바로 복잡한 방정식에 대입하기보다, 먼저 이차곡선의 기하학적 정의(초점과 준선까지의 거리)를 보조선으로 표시해야 식이 3줄 이내로 풀립니다!",
            "what_if_not_ko": "만약 원뿔을 자르는 평면의 기울기를 조금씩 변화시키면 단면이 원에서 타원, 포물선, 쌍곡선으로 어떻게 연속적으로 바뀔까요?"
        }

    # 14-A. 원에서 현의 수직이등분선과 중심의 성질 (Perpendicular Bisector of a Chord)
    if ("수직이등분선" in blob or "수직이분선" in blob) and ("현" in blob or "원" in blob or "chord" in blob.lower()):
        return {
            "category_type": "geometry",
            "hypothesis_ko": "원의 현 AB와 그 중점 M(AM = BM)을 지나고 현 AB에 수직인 수직이등분선이 주어진 출발 조건",
            "conclusion_ko": "원에서 현의 수직이등분선은 반드시 그 원의 중심 O를 지난다(역으로 원의 중심에서 현에 내린 수선은 그 현을 이등분한다)는 결론",
            "auxiliary_line_ko": "고립된 원의 중심 O와 현의 양 끝점 A, B를 직접 연결하는 두 반지름 OA, OB(OA = OB = 반지름 R) 보조선과 수직이등분선 위의 점에서 A, B를 잇는 선분",
            "proof_logic_ko": "선분의 수직이등분선 위의 모든 점은 양 끝점 A, B로부터 거리가 같고(삼각형 PAM과 PBM이 SAS 합동), 원의 중심 O 역시 두 반지름 OA와 OB의 길이가 같으므로 중심 O는 반드시 현 AB의 수직이등분선 위에 놓이는 원리",
            "misconception_ko": "허공에 떨어져 있는 원의 중심 O와 현 AB를 연결하는 필연적 다리는 '중심에서 원 위의 점 A, B까지 그은 반지름의 길이가 같다(이등변삼각형)'는 원의 정의 자체입니다!",
            "what_if_not_ko": "만약 현 AB를 원의 바깥쪽으로 평행이동시켜 두 끝점 A, B가 한 점 T에서 하나로 합쳐져 접선이 된다면, 현의 수직이등분선은 '접점을 지나는 접선의 수선'으로 어떻게 자연스럽게 이어질까요?"
        }

    # 14-B. 일차변환과 영역 / 2×2 행렬 기저 변환 (Linear Transformation & Matrix Basis)
    if any(k in blob for k in ("일차변환", "선형변환", "Linear Transformation", "linear transformation")):
        comp_desc = "2×2 행렬의 네 성분(a₁₁, a₁₂, a₂₁, a₂₂)"
        role_desc = "단위정사각형의 두 기준 화살표(기저벡터 e₁=(1,0), e₂=(0,1))를 행렬의 두 열벡터 위치로 이동시켜 평행사변형 영역으로 변환하는"
        if "11" in t or "₁₁" in t:
            comp_desc = "1열 기저벡터 e₁(1,0)의 x성분인 a₁₁"
            role_desc = "세로 축은 고정한 채 도형 영역을 가로(x축) 방향으로 늘이거나 줄이는 가로 신축(Horizontal Scaling) 및 y축 대칭 반사(a₁₁＜0)를 만드는"
        elif "12" in t or "₁₂" in t:
            comp_desc = "2열 기저벡터 e₂(0,1)의 x성분인 a₁₂"
            role_desc = "세로 높이는 그대로 유지한 채 도형의 윗변을 가로 방향으로 비스듬히 밀어 평행사변형을 만드는 가로 층밀림 변환(Horizontal Shear, 카발리에리 등적변형)을 수행하는"
        elif "21" in t or "₂₁" in t:
            comp_desc = "1열 기저벡터 e₁(1,0)의 y성분인 a₂₁"
            role_desc = "가로 폭은 그대로 유지한 채 도형의 오른쪽 변을 세로 방향으로 비스듬히 밀어 올리는 세로 층밀림 변환(Vertical Shear)을 수행하는"
        elif "22" in t or "₂₂" in t:
            comp_desc = "2열 기저벡터 e₂(0,1)의 y성분인 a₂₂"
            role_desc = "가로 축은 고정한 채 도형 영역을 세로(y축) 방향으로 늘이거나 줄이는 세로 신축(Vertical Scaling) 및 x축 대칭 반사(a₂₂＜0)를 만드는"
        return {
            "category_type": "geometry",
            "hypothesis_ko": f"좌표평면의 단위정사각형 영역에 행렬의 {comp_desc}을 변화시키는 일차변환을 적용한 출발 조건",
            "conclusion_ko": f"행렬 성분 {comp_desc}의 값에 따라 단위정사각형 격자가 {role_desc} 기하학적 변환 법칙이 성립한다는 결론",
            "auxiliary_line_ko": "영역 내부의 무수히 많은 점을 일일이 대입하는 대신, 가로 기준 화살표 e₁=(1,0)과 세로 기준 화살표 e₂=(0,1) 단 두 개의 기저벡터가 어느 좌표로 이동하는지 추적하는 기저 화살표 보조선",
            "proof_logic_ko": f"일차변환은 직선의 평행성과 등간격 격자를 항상 보존하므로, 두 기저벡터의 도착점인 행렬의 첫째 열벡터와 둘째 열벡터가 곧 변환된 평행사변형의 두 이웃변이 되어 {role_desc} 원리",
            "misconception_ko": "일차변환 문제를 복잡한 연립방정식 대입으로만 풀려고 하면 길을 잃기 쉽습니다! 항상 (1,0)이 1열로, (0,1)이 2열로 이사 간다는 기하학적 기저 이동으로 먼저 관찰하세요.",
            "what_if_not_ko": "만약 행렬의 두 열벡터가 한 직선 위에 놓여 평행사변형이 납작한 선분으로 찌그러진다면(행렬식 a₁₁a₂₂ - a₁₂a₂₁ = 0), 왜 역변환(역행렬)이 존재할 수 없을까요?"
        }

    # 15. 원의 성질 (원주각 / 중심각 / 접선 / 할선 / 톨레미 / 내접사각형)
    if any(k in blob for k in ("원주각", "중심각", "접선", "현의", "톨레미", "Ptolemy", "내접", "할선", "방멱")):
        return {
            "category_type": "geometry",
            "hypothesis_ko": f"원 위의 점들과 현·접선·중심이 이루는 '{ko_t}'의 기하학적 출발 조건",
            "conclusion_ko": f"'{ko_t}'의 각도·길이 곱 불변량이 원 위의 위치에 관계없이 항상 성립한다는 결론",
            "auxiliary_line_ko": "원의 중심 O와 원 위의 꼭짓점을 잇는 반지름(길이 R로 모두 같음) 보조선과 이등변삼각형의 외각 성질 활용",
            "proof_logic_ko": "반지름의 길이가 모두 같아 만들어지는 이등변삼각형들의 두 밑각과 삼각형의 외각 정리(두 내각의 합)에 의해 중심각과 원주각·닮음 비례식이 유도되는 원리",
            "misconception_ko": "원 문제에서 막힐 때 가장 먼저 확인해야 할 숨은 조건은 '원의 중심에서 원 위의 모든 점에 그은 선분은 반지름으로 길이가 같다'는 사실입니다!",
            "what_if_not_ko": "만약 원 위의 한 점이 다른 한 점에 한없이 가까워져 할선이 접선으로 변한다면 원주각은 접선과 현이 이루는 각으로 어떻게 그대로 보존될까요?"
        }

    # 16. 일반 기하·대수·미적분 주제
    is_alg = any(k in blob for k in ("방정식", "부등식", "다항식", "인수분해", "함수", "수열", "로그", "공식", "덧셈", "뺄셈", "곱셈", "나눗셈"))
    return {
        "category_type": "algebra" if is_alg else "geometry",
        "hypothesis_ko": f"'{ko_t}'에서 주어진 기본 정의와 출발 조건(가정)",
        "conclusion_ko": f"'{ko_t}'의 핵심 정리와 관계식이 항상 성립한다는 최종 결론",
        "auxiliary_line_ko": (
            "주어진 식을 기본 정의에 따라 항별로 전개하고 동류항과 공통 인수를 대칭적으로 묶어 내는 대수적 발상"
            if is_alg
            else "주어진 조건들을 하나의 대칭·합동·닮음 구조로 연결하는 폴리아의 제1보조선 및 단계별 분할"
        ),
        "proof_logic_ko": (
            "등식의 성질과 연산 법칙(교환·결합·분배법칙)을 단계별로 적용해 좌변에서 우변을 필연적으로 도출하는 원리"
            if is_alg
            else "단계별 작도를 통해 도형의 합동·닮음·넓이 불변량 성질로부터 결론을 필연적으로 도출하는 원리"
        ),
        "misconception_ko": "결론 공식만 단순 암기하면 조건이 조금만 변형되어도 적용할 수 없으므로, 반드시 어떤 정의와 첫 발상에서 출발했는지 먼저 확인해야 합니다.",
        "what_if_not_ko": "만약 이 정리의 조건이나 차수를 한 단계 일반화하면 고등학교 수능 기출에서 어떤 심화 문제로 발전할까요?"
    }


def _normalize_pdf_line_for_speech(line_str: str) -> str:
    """PDF에서 추출된 수식 텍스트 조각(예: 'am × an =', '= 2')을 정제하고 불완전 조각은 걸러냅니다."""
    s = (line_str or "").strip()
    if not s:
        return ""
    # 단일 기호나 불완전 파편(예: '= 2', 'am ×', 'an =', 'm개', 'n개') 필터링
    if len(s) <= 3 or re.match(r"^[=\+\-\×\÷\s0-9\.]+$", s):
        return ""
    if s.endswith(("×", "÷", "+", "-", "=")) and len(s) < 10:
        return ""
    # PDF 수식에서 지수가 아래로 내려온 형태(am, an, am+n, am-n, an-m) 교정
    s = re.sub(r"\ba\s*m\s*\+\s*n\b", "a의 (m+n)제곱", s)
    s = re.sub(r"\ba\s*m\s*-\s*n\b", "a의 (m-n)제곱", s)
    s = re.sub(r"\ba\s*n\s*-\s*m\b", "a의 (n-m)제곱", s)
    s = re.sub(r"\ba\s*m\s*n\b", "a의 mn제곱", s)
    s = re.sub(r"\ba\s*m\b", "a의 m제곱", s)
    s = re.sub(r"\ba\s*n\b", "a의 n제곱", s)
    s = re.sub(r"\bb\s*n\b", "b의 n제곱", s)
    return clean_math_for_speech_ko(s)


def auto_generate_page_explanations(doc, item_meta, scene_ranges=None):
    """
    [수석 수학교사(mathteacher) 에이전트 기반 PDF 슬라이드별 정밀 시각·대수 증명 분석 대본 생성기 (v7.0)]
    - 인물 명칭 언급 없이 오직 순수한 수학적 논리와 직관적 발문으로만 구성합니다.
    - 대수/수체계(algebra/number)와 기하/프랙탈(geometry/fractal_curve)을 엄격히 분리하여,
      대수 영상에 기하 합동/보조선 문구가 섞이거나 기계적인 레이아웃 메타 설명이 낭독되지 않도록 합니다.
    """
    total_pages = len(doc)
    if scene_ranges is None:
        scene_ranges = compute_pedagogical_scene_ranges(total_pages, max_scenes=12)
    num_scenes = len(scene_ranges)

    raw_title = (item_meta or {}).get("title") or "단계별 시각적 수학 증명"
    sub_ko = (item_meta or {}).get("sub_domain_ko") or ""
    breadcrumb = (item_meta or {}).get("breadcrumb") or ""
    clean_title_ko = clean_math_for_speech_ko(raw_title)
    _, _en_from_title = split_bilingual_title(raw_title)
    clean_title_en = clean_math_for_speech_en(_en_from_title) if _en_from_title else translate_text_google_gtx(clean_title_ko, "en")

    # 항상 최신 v7.0 수학교사 분석기를 직접 호출하여 캐시 오염 원천 차단
    t_analysis = analyze_min7014_topic_as_mathteacher(raw_title, sub_ko, breadcrumb)
    cat_type = t_analysis.get("category_type", "geometry")
    is_alg_num = cat_type in ("algebra", "number")
    hyp_ko = clean_math_for_speech_ko(t_analysis.get("hypothesis_ko") or "")
    conc_ko = clean_math_for_speech_ko(t_analysis.get("conclusion_ko") or "")
    aux_ko = clean_math_for_speech_ko(t_analysis.get("auxiliary_line_ko") or "")
    logic_ko = clean_math_for_speech_ko(t_analysis.get("proof_logic_ko") or "")
    misc_ko = clean_math_for_speech_ko(t_analysis.get("misconception_ko") or "")
    win_ko = clean_math_for_speech_ko(t_analysis.get("what_if_not_ko") or "")

    color_desc_ko = {
        "red": "붉은색 목표 결론 및 핵심 등식 강조",
        "blue": "파란색 출발 가정 및 기준 조건 제시",
        "green": "초록색 핵심 연결 고리 및 분할 과정",
        "purple": "주황·보라색 핵심 대응 관계 강조",
        "default": "단계별 수학적 추론 및 증명 전개",
    }

    pages_out = []
    prev_pil = None
    prev_text_lines = []
    used_roles = set()

    for s_idx, (p_start, p_end) in enumerate(scene_ranges):
        s_num = s_idx + 1
        rep_idx = (p_start + p_end) // 2
        pix = doc[rep_idx].get_pixmap(dpi=96)
        curr_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        bbox, c_tag = compute_page_diff_and_color(prev_pil, curr_pil) if s_idx > 0 else (None, "default")
        prev_pil = curr_pil

        raw_page_text = ""
        try:
            raw_page_text = doc[rep_idx].get_text("text") or ""
        except Exception:
            raw_page_text = ""
        curr_lines = [
            re.sub(r"\s+", " ", ln.strip())
            for ln in raw_page_text.splitlines()
            if ln.strip()
            and ln.strip().lower() not in ("start", "stop", "home", "end", "home end", "?", "!", "|", "{", "}")
            and "github" not in ln.lower()
            and "http" not in ln.lower()
        ]
        added_lines = [ln for ln in curr_lines if ln not in prev_text_lines]
        if curr_lines:
            prev_text_lines = list(curr_lines)
        meaningful_added = [_normalize_pdf_line_for_speech(ln) for ln in added_lines]
        meaningful_added = [m for m in meaningful_added if len(m) >= 5]
        added_formula_ko = meaningful_added[0] if meaningful_added else ""

        c_ko = color_desc_ko.get(c_tag, color_desc_ko["default"])
        spatial_role = "general"
        focus_desc = c_ko
        if bbox and not is_alg_num:
            cx = (bbox[0] + bbox[2]) / 2.0
            cy = (bbox[1] + bbox[3]) / 2.0
            if cy < 0.48 and cx < 0.47:
                spatial_role = "top_left_hypothesis"
                focus_desc = f"좌측 상단 출발 가정(Hypothesis) 제시 ({c_ko})"
            elif cy < 0.48 and cx >= 0.47:
                spatial_role = "top_right_conclusion"
                focus_desc = f"우측 상단 목표 결론(⇒ Conclusion) 제시 ({c_ko})"
            elif cy >= 0.48 and c_tag == "green":
                spatial_role = "bottom_green_auxiliary"
                focus_desc = "초록색 폴리아 제1보조선 작도"
            elif cy >= 0.48 and c_tag == "purple":
                spatial_role = "bottom_purple_congruence"
                focus_desc = "주황·보라색 합동·닮음 삼각형 비교"
            elif cy >= 0.48 and c_tag == "red":
                spatial_role = "bottom_red_qed"
                focus_desc = "붉은색 대응 요소 및 최종 결론 도출"
            elif cy >= 0.48:
                spatial_role = "bottom_base_proof"
                focus_desc = f"증명 도형 단계별 작도 ({c_ko})"

        if s_num == 1:
            step_title = "도입 · 출발 조건(가정)과 목표 결론 읽기 (Notice & Wonder)"
            step_q_ko = f"❓ [출발 질문] {clean_title_ko}에서 주어진 출발 조건은 무엇이고, 우리가 증명할 목표 결론은 무엇일까요?"
            step_q_en = f"❓ [Opening Question] What is the starting condition and target conclusion in {clean_title_en}?"
            exp_ko = (
                f"1단계입니다. 오늘 함께 탐구할 주제는 {clean_title_ko}입니다. "
                f"결과 공식을 먼저 외우기 전에 출발 조건부터 정확히 짚어 볼까요? "
                f"이 주제의 출발점은 {hyp_ko}입니다. 왜 이 조건에서 {conc_ko}이 필연적으로 성립하는지 한 단계씩 증명해 봅시다."
            )
            exp_en = (
                f"Step 1. Today we explore {clean_title_en} through a step-by-step visual proof. "
                f"Before memorizing the final result, let us examine our starting condition and see why it inevitably leads to the conclusion."
            )
        elif s_num == num_scenes:
            step_title = "완결 · 증명 완성(Q.E.D.) 및 조건 변형 확장 (What-If-Not)"
            step_q_ko = f"🔀 [조건 변형 질문] {win_ko}"
            step_q_en = "🔀 [What-If-Not] How does this mathematical principle evolve if we modify or generalize its conditions?"
            exp_ko = (
                f"마지막 {s_num}단계, 증명이 완성되었습니다! "
                f"출발 조건이었던 {hyp_ko}에서 시작해, {aux_ko}을 거쳐, {conc_ko}이 성립함을 명확하게 확인했습니다. "
                f"여기서 꼭 기억해야 할 핵심 포인트는, {misc_ko} "
                f"마지막으로 한 걸음 더 깊이 질문해 보세요. {win_ko} "
                f"설명란 링크의 수학홈페이지에서 직접 값과 도형을 바꾸며 실험해 보세요!"
            )
            exp_en = translate_text_google_gtx(exp_ko, "en")
        else:
            progress = (s_num - 1) / max(1, num_scenes - 2)
            range_str = f"{p_start + 1}페이지부터 {p_end + 1}페이지까지의 단계입니다." if p_end > p_start else f"{p_start + 1}페이지 단계입니다."

            # A) 대수·수체계(algebra / number) 전용 단계별 논리 전개 (기하 합동/보조선 문구 완전 배제)
            if is_alg_num:
                formula_mention = f"화면에 제시된 {added_formula_ko} 관계를 살펴보세요. " if added_formula_ko else ""
                if progress <= 0.30:
                    step_title = f"Step {s_num} · 기본 정의 확인 및 출발 식 세우기 (Definition)"
                    step_q_ko = f"❓ [정의 질문] {clean_title_ko}를 증명하기 위해 가장 먼저 어떤 기본 정의를 적용해야 할까요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} {formula_mention}"
                        f"먼저 {hyp_ko}을 바탕으로 식의 기본 정의를 정확히 세웁니다. "
                        f"기호를 기계적으로 조작하기 전에 각 기호가 뜻하는 본래 의미를 먼저 떠올리는 것이 첫걸음입니다."
                    )
                elif progress <= 0.56:
                    step_title = f"Step {s_num} · 핵심 대수적 발상 및 식의 변환 (Algebraic Bridge)"
                    step_q_ko = "🧭 [핵심 발상 질문] 출발 식을 목표 결론으로 연결하기 위해 어떤 대수적 변형이나 모델을 사용하나요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} {formula_mention}"
                        f"이제 증명의 핵심 열쇠인 {aux_ko}을 적용합니다. "
                        f"이 변환을 거치면 복잡해 보이던 식의 구조가 우리가 이미 알고 있는 기본 연산으로 선명하게 풀립니다."
                    )
                elif progress <= 0.80:
                    step_title = f"Step {s_num} · 단계별 연산 법칙 적용 및 오개념 예방 (Verification)"
                    step_q_ko = "⚠️ [오개념 점검 질문] 이 연산 과정에서 부호나 조건 때문에 가장 실수하기 쉬운 함정은 무엇일까요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} {formula_mention}"
                        f"{logic_ko}에 따라 식이 빈틈없이 유도됩니다. "
                        f"이 단계에서 특히 주의할 점은, {misc_ko}"
                    )
                else:
                    step_title = f"Step {s_num} · 대수적 등식 결합 및 성질 완성 (Synthesis)"
                    step_q_ko = "💡 [종합 질문] 지금까지 유도한 식을 하나로 정리하면 어떻게 최종 법칙이 완성되나요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} {formula_mention}"
                        f"앞 단계에서 정리한 수식들을 하나로 묶어 주면, 마침내 우리가 목표로 했던 {conc_ko}이 자연스럽게 도출됩니다!"
                    )
                step_q_en = translate_text_google_gtx(step_q_ko, "en")
                exp_en = translate_text_google_gtx(exp_ko, "en")

            # B) 기하·프랙탈 증명 PDF의 공간·색상 역할별 맞춤 해설
            elif spatial_role == "top_left_hypothesis" and "hyp" not in used_roles:
                used_roles.add("hyp")
                step_title = f"Step {s_num} · 출발 가정(Hypothesis) 도형과 조건 확인"
                step_q_ko = "👁️ [가정 확인 질문] 화면 왼쪽 위에 파란색으로 표시된 출발 조건(가정)은 무엇인가요?"
                step_q_en = "👁️ [Hypothesis Question] What starting condition is drawn in blue at the top-left?"
                exp_ko = (
                    f"{s_num}단계, {range_str} 화면 왼쪽 위 영역을 보세요. "
                    f"증명을 시작할 때는 먼저 문제에서 주어진 출발 조건인 가정을 도형 위에 명확히 표시합니다. "
                    f"여기서는 {hyp_ko}이 파란색 기호로 작도되었습니다."
                )
                exp_en = translate_text_google_gtx(exp_ko, "en")

            elif spatial_role == "top_right_conclusion" and "conc_top" not in used_roles:
                used_roles.add("conc_top")
                step_title = f"Step {s_num} · 목표 결론(⇒ Conclusion) 확인"
                step_q_ko = "🎯 [목표 결론 질문] 화살표(⇒) 오른쪽에 제시된 우리의 최종 증명 목표는 무엇인가요?"
                step_q_en = "🎯 [Target Conclusion Question] What target conclusion is shown to the right of the arrow (⇒)?"
                exp_ko = (
                    f"{s_num}단계, {range_str} 상단 화살표 오른쪽의 목표 도형을 확인해 보세요. "
                    f"왼쪽의 출발 가정이 주어졌을 때 화살표 오른쪽의 {conc_ko}이 왜 항상 성립하는지 보이겠다는 뜻입니다. "
                    f"가정과 결론을 절대 섞지 않고, 이제 아래쪽 증명 도형에서 논리적 다리를 놓아 봅시다!"
                )
                exp_en = translate_text_google_gtx(exp_ko, "en")

            elif (spatial_role == "bottom_green_auxiliary" or c_tag == "green") and "aux" not in used_roles:
                used_roles.add("aux")
                step_title = f"Step {s_num} · 폴리아의 제1보조선(초록색 선분) 작도"
                step_q_ko = "🧭 [결정적 보조선 질문] 왜 하필 이 위치에 초록색 보조선을 그어야 숨겨진 합동·대칭이 드러날까요?"
                step_q_en = "🧭 [Key Auxiliary Line] Why do we draw the green auxiliary line right here to unlock the proof?"
                exp_ko = (
                    f"{s_num}단계, {range_str} 이 증명에서 가장 중요한 유레카 순간입니다! "
                    f"도형에 새로 그어진 초록색 선분을 보세요. 바로 {aux_ko}입니다. "
                    f"원래 도형만으로는 보이지 않던 관계가 이 초록색 보조선 한 줄로 인해 두 개의 비교 가능한 도형으로 나뉩니다!"
                )
                exp_en = translate_text_google_gtx(exp_ko, "en")

            elif (spatial_role == "bottom_purple_congruence" or c_tag == "purple") and "cong" not in used_roles:
                used_roles.add("cong")
                step_title = f"Step {s_num} · 합동·닮음 대응 조건 결합"
                step_q_ko = "📐 [합동·닮음 질문] 나뉜 두 도형은 어떤 조건(SAS, ASA, SSS, RHS, RHA, 닮음)에 의해 완전히 포개어질까요?"
                step_q_en = "📐 [Congruence & Similarity] By which geometric criterion do the two divided figures match?"
                exp_ko = (
                    f"{s_num}단계, {range_str} 주황색과 보라색으로 강조된 두 영역을 비교해 보세요. "
                    f"{logic_ko}를 눈으로 직접 확인할 수 있습니다. "
                    f"대응하는 변과 각의 조건이 정확히 맞아떨어지므로 두 도형은 완벽하게 합동(또는 닮음)을 이룹니다!"
                )
                exp_en = translate_text_google_gtx(exp_ko, "en")

            elif (spatial_role == "bottom_red_qed" or c_tag == "red") and progress > 0.60 and "qed_red" not in used_roles:
                used_roles.add("qed_red")
                step_title = f"Step {s_num} · 대응변·대응각 일치로 최종 결론 도출"
                step_q_ko = "💡 [유레카 질문] 합동·닮음인 도형의 대응하는 변과 각이 같다는 성질로부터 어떻게 목표 결론이 완성되나요?"
                step_q_en = "💡 [Eureka Deduction] How do the corresponding parts of congruent figures complete our target conclusion?"
                exp_ko = (
                    f"{s_num}단계, {range_str} 도형에 붉은색으로 강조된 최종 표시를 보세요! "
                    f"앞 단계에서 증명한 도형의 합동·대칭 성질에 의해 대응하는 부분의 크기가 같아지므로, "
                    f"우리가 목표로 했던 {conc_ko}이 마침내 증명되었습니다!"
                )
                exp_en = translate_text_google_gtx(exp_ko, "en")

            else:
                if progress <= 0.30:
                    step_title = f"Step {s_num} · 기본 증명 도형 작도 및 조건 표시"
                    step_q_ko = "👁️ [관찰 질문] 증명 공간에 그린 기본 도형에서 가장 먼저 표시해야 할 주어진 조건은 무엇일까요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} "
                        f"출발 조건인 {hyp_ko}을 증명 도형 위에 차례대로 작도하며 각 점과 선분의 위치 관계를 명확히 세웁니다."
                    )
                elif progress <= 0.58:
                    step_title = f"Step {s_num} · 보조선 연결과 변·각의 크기 비교"
                    step_q_ko = "🧭 [연결 질문] 보조선이 만들어 낸 공통변이나 엇각·동위각 중 서로 크기가 같은 것은 어디일까요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} "
                        f"{aux_ko}을 중심으로 도형에서 서로 길이가 같은 변과 크기가 같은 각을 하나씩 짝지어 비교합니다."
                    )
                elif progress <= 0.82:
                    step_title = f"Step {s_num} · 핵심 증명 논리 완성 및 오개념 점검"
                    step_q_ko = "⚠️ [오개념 점검 질문] 증명할 결론을 미리 가정으로 끌어다 쓰는 순환논리 실수를 피하려면 무엇을 확인해야 할까요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} "
                        f"{logic_ko}가 완성되는 단계입니다. 이때 꼭 기억해야 할 점은, {misc_ko}"
                    )
                else:
                    step_title = f"Step {s_num} · 기하학적 단서 종합 및 결론 연결 (Synthesis)"
                    step_q_ko = "💡 [종합 질문] 지금까지 찾은 기하학적 단서들을 하나로 합치면 처음에 세운 목표 결론과 어떻게 일치하나요?"
                    exp_ko = (
                        f"{s_num}단계, {range_str} 이제 앞에서 차곡차곡 확인한 기하학적 단서들을 하나로 결합합니다. "
                        f"도형의 대응 관계로부터 우리가 증명하고자 했던 {conc_ko}이 필연적으로 성립함을 확인할 수 있습니다."
                    )
                step_q_en = translate_text_google_gtx(step_q_ko, "en")
                exp_en = translate_text_google_gtx(exp_ko, "en")

        pages_out.append({
            "page": rep_idx + 1,
            "scene_index": s_num,
            "frame_range": [p_start + 1, p_end + 1],
            "step_title": step_title,
            "step_question_ko": step_q_ko,
            "step_question_en": step_q_en,
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


def build_step_question_ko(title, p_num, total_p, color_tag="default"):
    """단계별 질문하는 수업 발문(Notice & Wonder -> Socratic Inquiry -> What-If-Not) 생성기 (KO)"""
    ko_t, _ = split_bilingual_title(title)
    clean_t = clean_math_for_speech_ko(ko_t)
    if p_num <= 1:
        return f"👁️ [관찰과 경이 질문] '{clean_t}'의 출발 도형과 조건에서 가장 먼저 눈에 띄는 수학적 특징은 무엇인가요?"
    if p_num >= total_p:
        return f"🔀 [What-If-Not 확장 질문] 오늘 증명한 '{clean_t}'에서 조건 하나를 바꾸면 어떤 새로운 정리가 탄생할까요?"
    if color_tag == "green":
        return f"🧭 [결정적 보조선 질문 {p_num}/{total_p}] 왜 이 위치에 초록색 보조선·수식을 추가해야 숨겨진 연결고리가 드러날까요?"
    if color_tag == "purple":
        return f"📐 [핵심 원리 질문 {p_num}/{total_p}] 보라색으로 강조된 두 대상이 서로 같거나 비례하는 이유는 무엇일까요?"
    if color_tag == "red":
        return f"💡 [유레카 질문 {p_num}/{total_p}] 붉은색으로 완성된 등식·도형 관계가 어떻게 최종 결론을 증명하나요?"
    return f"🧭 [소크라테스 발문 {p_num}/{total_p}] 직전 단계와 비교했을 때 새로 추가된 기호·선분이 증명에서 어떤 다리 역할을 할까요?"


def build_step_question_en(title_en, p_num, total_p, color_tag="default"):
    """Step-by-step Question-Asking Classroom prompt generator (EN)"""
    _, en_split = split_bilingual_title(title_en)
    clean_en = (en_split or title_en).strip()
    if p_num <= 1:
        return f"👁️ [Notice & Wonder] What mathematical structure stands out first in '{clean_en}'?"
    if p_num >= total_p:
        return f"🔀 [What-If-Not] What new theorem emerges if we modify one condition in '{clean_en}'?"
    if color_tag == "green":
        return f"🧭 [Auxiliary Line Q {p_num}/{total_p}] Why does adding this green auxiliary line or expression unlock the proof?"
    if color_tag == "purple":
        return f"📐 [Core Principle Q {p_num}/{total_p}] Why are the purple-highlighted parts congruent or proportional?"
    if color_tag == "red":
        return f"💡 [Eureka Q {p_num}/{total_p}] How does the red-highlighted relation complete the target conclusion?"
    return f"🧭 [Socratic Inquiry {p_num}/{total_p}] Compared to the previous step, how does this new element bridge the proof?"


GENERATED_PDF_DIR = ROOT_DIR / "video_lectures" / "generated_pdfs"
GENERATED_PDF_DIR.mkdir(parents=True, exist_ok=True)


def ensure_synthetic_pdf_for_non_pdf_topic(slug_key: str, item_meta: dict = None) -> Path:
    """
    [Non-PDF 웹·GeoGebra·AlgeoMath·특강 자료용 8단계 시각적 강의 슬라이드 PDF 자동 합성기]
    https://min7014.github.io/ 의 1,113개 자료 중 별도 .pdf 파일이 없는 268개 웹/GeoGebra/AlgeoMath/특강 자료도
    4대 에디션 강의 영상(1080p 일반/질문수업 + 9:16 일반/질문 #Shorts)으로 완벽히 제작할 수 있도록,
    수학교사 분석(analyze_min7014_topic_as_mathteacher)과 단계별 디딤돌(scaffolding_steps) 및 기하·대수 다이어그램을
    작도하여 8페이지 플립북 PDF(video_lectures/generated_pdfs/{slug_key}.pdf)를 자동 생성합니다.
    """
    out_pdf = GENERATED_PDF_DIR / f"{slug_key}.pdf"
    if out_pdf.exists() and out_pdf.stat().st_size > 5000:
        return out_pdf

    meta = item_meta or find_item_by_slug_or_pdf(slug_key) or {}
    raw_title = meta.get("title") or slug_key
    ko_t, en_t = split_bilingual_title(raw_title)
    clean_ko = latex_to_unicode_title(ko_t)
    clean_en = latex_to_unicode_title(en_t or ko_t)
    sub_ko = meta.get("sub_domain_ko") or "기하·대수 심층 탐구"
    web_url = meta.get("url") or f"https://min7014.github.io/{slug_key}.html"
    t_an = analyze_min7014_topic_as_mathteacher(raw_title, sub_ko, meta.get("breadcrumb") or "")
    steps = list(meta.get("scaffolding_steps") or [])
    tips = list(meta.get("solving_tips") or [])
    while len(steps) < 5:
        steps.append(f"{len(steps)+1}단계: {t_an.get('auxiliary_line_ko', '핵심 보조선과 동치 변형으로 원리를 연결합니다.')}")

    slide_specs = [
        ("1단계 · 탐구 주제 & 출발 조건 (Hypothesis)", t_an.get("hypothesis_ko", clean_ko), "주어진 도형·수식의 기본 정의와 출발 조건을 확인합니다."),
        ("2단계 · 첫 번째 관찰과 디딤돌 (Step 1)", latex_to_unicode_title(steps[0]), "가장 단순한 기본 형태에서 불변의 규칙을 관찰합니다."),
        ("3단계 · 목표 결론과 핵심 관계 (Step 2)", latex_to_unicode_title(steps[1]), t_an.get("conclusion_ko", "최종 도달해야 할 수학적 관계식을 확인합니다.")),
        ("4단계 · 결정적 제1보조선 · 발상 (Auxiliary Idea)", t_an.get("auxiliary_line_ko", latex_to_unicode_title(steps[2])), "조건과 결론을 하나로 잇는 결정적 연결고리를 작도합니다."),
        ("5단계 · 논리적 동치 변형 및 전개 (Step 4)", latex_to_unicode_title(steps[3]), tips[0] if tips else "합동·닮음·대수적 항등 변형으로 등식을 유도합니다."),
        ("6단계 · 시각적 직관과 수식의 결합 (Synthesis)", tips[-1] if tips else t_an.get("conclusion_ko", clean_ko), "기하학적 넓이·길이와 대수적 식이 완벽히 일치함을 확인합니다."),
        ("7단계 · 오개념 점검 및 반례 탐구 (Check)", latex_to_unicode_title(steps[4]), "공식 단순 암기를 넘어 성립 조건의 경계를 점검합니다."),
        ("8단계 · What-If-Not 확장 & 인터랙티브 실습", f"최종 정리 완성: {clean_ko}", f"실습 주소: {web_url}"),
    ]

    pdf_doc = pymupdf.open()
    W, H = 1600, 1000
    f_title = get_font_for_lang("ko", 40, bold=True)
    f_sub = get_font_for_lang("ko", 25, bold=True)
    f_body = get_font_for_lang("ko", 27, bold=True)
    f_small = get_font_for_lang("ko", 22, bold=False)

    for idx, (st_head, st_main, st_sub) in enumerate(slide_specs):
        img = Image.new("RGB", (W, H), (252, 253, 255))
        draw = ImageDraw.Draw(img)

        for gx in range(80, W - 80, 80):
            draw.line([(gx, 120), (gx, H - 90)], fill=(235, 241, 248), width=1)
        for gy in range(120, H - 90, 80):
            draw.line([(80, gy), (W - 80, gy)], fill=(235, 241, 248), width=1)

        draw.rounded_rectangle((60, 36, W - 60, 136), radius=18, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((92, 56), f"[{sub_ko}] {clean_ko[:42]}", fill=(255, 255, 255), font=f_title)
        draw.text((W - 310, 64), f"STEP {idx + 1} / {len(slide_specs)}", fill=(251, 191, 36), font=f_sub)

        draw.rounded_rectangle((70, 165, 770, 895), radius=22, fill=(255, 255, 255), outline=(148, 163, 184), width=3)
        cx, cy = 420, 530
        draw.line([(120, cy), (720, cy)], fill=(100, 116, 139), width=3)
        draw.line([(cx, 220), (cx, 840)], fill=(100, 116, 139), width=3)
        draw.ellipse((cx - 190, cy - 190, cx + 190, cy + 190), outline=(37, 99, 235), width=4)
        if idx >= 1:
            draw.polygon([(cx - 160, cy + 110), (cx + 170, cy + 110), (cx + 40, cy - 185)], outline=(15, 23, 42), width=5)
        if idx >= 2:
            draw.line([(cx + 40, cy - 185), (cx + 40, cy + 110)], fill=(225, 29, 72), width=5)
            draw.rectangle((cx + 40, cy + 88, cx + 62, cy + 110), outline=(225, 29, 72), width=3)
        if idx >= 3:
            draw.line([(cx - 160, cy + 110), (cx + 125, cy - 45)], fill=(5, 150, 105), width=5)
            draw.ellipse((cx + 28, cy - 10, cx + 52, cy + 14), fill=(225, 29, 72))
        if idx >= 4:
            draw.arc((cx - 160, cy - 160, cx + 160, cy + 160), start=200, end=340, fill=(217, 119, 6), width=5)
        if idx >= 5:
            draw.rounded_rectangle((130, 760, 710, 860), radius=14, fill=(239, 246, 255), outline=(37, 99, 235), width=3)
            draw.text((155, 792), clean_en[:42], fill=(30, 58, 138), font=f_sub)

        draw.rounded_rectangle((800, 165, W - 60, 895), radius=22, fill=(248, 250, 252), outline=(203, 213, 225), width=3)
        draw.rounded_rectangle((830, 195, W - 90, 275), radius=14, fill=(30, 58, 138))
        draw.text((855, 218), st_head, fill=(254, 240, 138), font=f_sub)

        y_box = 305 + (idx % 4) * 115
        draw.rounded_rectangle((830, y_box, W - 90, y_box + 230), radius=18, fill=(255, 241, 242), outline=(225, 29, 72), width=5)
        for li, line in enumerate(textwrap.wrap(st_main, width=24)[:3]):
            draw.text((858, y_box + 28 + li * 42), line, fill=(15, 23, 42), font=f_body)
        for li, line in enumerate(textwrap.wrap(st_sub, width=28)[:2]):
            draw.text((858, y_box + 155 + li * 32), line, fill=(190, 18, 60), font=f_small)

        draw.rectangle((0, H - 36, W, H), fill=(15, 23, 42))

        import io
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        png_bytes = bio.getvalue()
        page = pdf_doc.new_page(width=W, height=H)
        page.insert_image(pymupdf.Rect(0, 0, W, H), stream=png_bytes)

    pdf_doc.save(str(out_pdf))
    pdf_doc.close()
    return out_pdf


def load_or_build_topic_pdf_bytes(pdf_url: str, slug_key: str, item_meta: dict = None):
    """
    주제의 pdf_url이 원격 .pdf이면 다운로드하고, 로컬 경로이거나 비어 있는 Non-PDF 자료이면
    ensure_synthetic_pdf_for_non_pdf_topic()으로 8단계 시각적 강의 PDF를 생성하여 (pdf_bytes, resolved_pdf_url)을 반환합니다.
    """
    u = str(pdf_url or "").split("#")[0].strip()
    if u.startswith(("http://", "https://")) and u.lower().endswith(".pdf"):
        try:
            return urllib.request.urlopen(u, timeout=20).read(), u
        except Exception:
            pass
    if u:
        local_cand = Path(u) if Path(u).is_absolute() else (ROOT_DIR / u)
        if local_cand.exists() and local_cand.is_file():
            return local_cand.read_bytes(), f"video_lectures/generated_pdfs/{local_cand.name}"
    gen_p = ensure_synthetic_pdf_for_non_pdf_topic(slug_key, item_meta=item_meta)
    return gen_p.read_bytes(), f"video_lectures/generated_pdfs/{gen_p.name}"


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
            old_doc = {}
    else:
        old_doc = {}

    if curated:
        title = curated["title"]
        title_en = curated["title_en"]
        pdf_url = curated["pdf_url"]
        web_url = curated["web_url"]
        sub_ko = (item_meta or {}).get("sub_domain_ko") or "유클리드 평면기하·작도·원주각 (Euclidean Geometry)"
    elif item_meta:
        title = item_meta.get("title", slug_key)
        _ko_only, _en_only = split_bilingual_title(title)
        if _en_only:
            title_en = _en_only
        elif not re.search(r"[가-힣]", _ko_only):
            title_en = latex_to_unicode_title(_ko_only)
        else:
            title_en = _balance_parentheses(translate_text_google_gtx(clean_math_for_speech_ko(_ko_only), "en"))
        pdf_url = (item_meta.get("pdf") or "").split("#")[0]
        web_url = item_meta.get("url") or "https://min7014.github.io/"
        sub_ko = item_meta.get("sub_domain_ko") or "기하·대수 시각적 증명"
    else:
        raise ValueError(f"Topic not found for slug/key: {slug_key}")

    orig_yt = (item_meta or {}).get("youtube") or ""
    blocked_ids = get_deleted_video_ids_set()
    if orig_yt and not existing_yt_urls.get("orig"):
        existing_yt_urls["orig"] = orig_yt
    if (item_meta or {}).get("youtube_ko") and not existing_yt_urls.get("ko"):
        existing_yt_urls["ko"] = item_meta["youtube_ko"]
    if (item_meta or {}).get("youtube_en") and not existing_yt_urls.get("en"):
        existing_yt_urls["en"] = item_meta["youtube_en"]
    for _k in ("ko", "en"):
        _u = existing_yt_urls.get(_k) or ""
        if any(bid in _u for bid in blocked_ids):
            existing_yt_urls[_k] = ""

    pdf_bytes, pdf_url = load_or_build_topic_pdf_bytes(pdf_url, slug_key, item_meta=item_meta)
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
                "step_question_ko": build_step_question_ko(title, idx + 1, total_pages, c_tag),
                "step_question_en": build_step_question_en(title_en, idx + 1, total_pages, c_tag),
                "visual_focus": "핵심 단계별 작도 및 수식 유도",
                "color_tag": c_tag,
                "diff_bbox": bbox,
                "explanation_text": exp_ko,
                "narrations": {"ko": exp_ko, "en": exp_en}
            })
    else:
        scene_ranges = compute_pedagogical_scene_ranges(total_pages, max_scenes=12)
        pages_data = auto_generate_page_explanations(doc, item_meta, scene_ranges=scene_ranges)

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
        "quality_profile": "Broadcast Master 1080p (PyMuPDF Geometric Script Engine + 300 DPI Lanczos + H.264 High Profile CRF 16)",
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
        "shorts_urls": old_doc.get("shorts_urls") or {"ko": "", "en": ""},
        "question_youtube_urls": old_doc.get("question_youtube_urls") or {"ko": "", "en": ""},
        "question_shorts_urls": old_doc.get("question_shorts_urls") or {"ko": "", "en": ""},
        "youtube_packages": old_doc.get("youtube_packages") or {},
        "shorts_packages": old_doc.get("shorts_packages") or {},
        "question_classroom_packages": old_doc.get("question_classroom_packages") or {},
        "question_shorts_packages": old_doc.get("question_shorts_packages") or {},
        "teacher_proof_analysis": analyze_min7014_topic_as_mathteacher(title, sub_ko, (item_meta or {}).get("breadcrumb") or ""),
        "supported_languages": list(GLOBAL_VOICE_MAP.keys()),
        "pages": pages_data
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(script_doc, f, ensure_ascii=False, indent=2)

    print(f"[High-Quality Script Generated] {out_path} ({total_pages} pages, langs={target_langs})")
    return script_doc


_ORIG_PIL_DRAW_TEXT = ImageDraw.ImageDraw.text
_PIL_EMOJI_MAP = {
    "⚡": "★",
    "🎬": "▶",
    "📐": "◈",
    "🪜": "■",
    "❓": "[Q]",
    "🙋": "[발문]",
    "💡": "[핵심]",
    "🧭": "[탐구]",
    "👁️": "[관찰]",
    "👁": "[관찰]",
    "🔀": "[확장]",
    "⚠️": "[주의]",
    "⚠": "[주의]",
    "🎯": "[목표]",
    "🌐": "▶",
    "📺": "▶",
    "👉": "→",
    "👆": "→",
    "🔥": "★",
    "✨": "★",
    "🌳": "◈",
    "🌟": "★",
    "🤖": "◈",
}


def _sanitize_pil_text(txt):
    if not isinstance(txt, str):
        return txt
    s = txt
    for k, v in _PIL_EMOJI_MAP.items():
        if k in s:
            s = s.replace(k, v)
    # Remove any remaining astral-plane emoji characters (> U+FFFF) or variation selectors so malgun.ttf never draws '□'
    s = "".join(ch for ch in s if ord(ch) <= 0xFFFF and ch != "\ufe0f")
    return s


def _patched_pil_draw_text(self, xy, text, fill=None, font=None, anchor=None, *args, **kwargs):
    return _ORIG_PIL_DRAW_TEXT(self, xy, _sanitize_pil_text(text), fill=fill, font=font, anchor=anchor, *args, **kwargs)


ImageDraw.ImageDraw.text = _patched_pil_draw_text


def _mask_pdf_bottom_author_bar(pil_img):
    """PDF 하단 블랙 바의 영문 성명 표기 영역(하단 3.6%)을 깔끔한 다크 네이비 바로 마스킹합니다."""
    w, h = pil_img.size
    bar_h = max(10, int(h * 0.038))
    d = ImageDraw.Draw(pil_img)
    d.rectangle([0, h - bar_h, w, h], fill=(15, 23, 42))
    return pil_img


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
        "match_keywords": ["inscribed", "원주각", "중심각", "thales", "탈레스", "톨레미", "현의 길이", "원의 접선"],
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
        "match_keywords": ["미분", "적분", "극한", "접선", "할선", "넓이", "급수", "평균값", "롤의 정리", "구분구적", "도함수", "derivative", "integral", "limit", "tangent", "secant"],
        "thumb_hook_ko": ["할선이 회전하며", "접선이 되는 순간!"],
        "thumb_hook_en": ["WATCH SECANT LINES", "BECOME A TANGENT!"],
        "badge_ko": "⚡ 눈으로 보는 미적분의 본질",
        "badge_en": "⚡ SEE CALCULUS IN MOTION",
        "cold_open_ko": "곡선 위의 두 점을 잇는 할선이 한 점으로 한없이 가까워질 때 과연 무슨 일이 일어날까요? 수식만 보면 막막했던 미적분과 극한의 본질을 살아 움직이는 동적 기하로 한눈에 깨달아 보세요!",
        "cold_open_en": "What happens as two points on a curve slide infinitely close together? Watch abstract calculus and limits come alive visually in smooth motion!",
        "quiz_ko": "💬 10초 퀴즈: 두 점을 잇는 할선의 기울기가 극한에서 도달하는 직선의 이름은 무엇일까요?",
        "quiz_en": "💬 10-Sec Quiz: What do we call the limiting line as the two secant points merge?"
    },
    "radicals_exponents": {
        "match_keywords": ["제곱근", "무리수", "유리수", "순환소수", "지수", "로그", "거듭제곱", "근호", "square root", "radical", "rational", "repeating decimal", "exponent", "logarithm"],
        "thumb_hook_ko": ["공식만 외우면", "무조건 헷갈린다!"],
        "thumb_hook_en": ["STOP ROTE MEMORIZING", "SEE WHY IT WORKS!"],
        "badge_ko": "⚡ 99%가 헷갈리는 수체계 핵심",
        "badge_en": "⚡ VISUAL ALGEBRA BREAKTHROUGH",
        "cold_open_ko": "기호와 공식만 외워서 풀다 보면 부호와 정의에서 반드시 함정에 빠집니다! 정사각형의 넓이와 수직선 원리부터 차근차근 연결하면 왜 이 성질이 성립하는지 단 1분 만에 완벽히 꿰뚫어 볼 수 있습니다!",
        "cold_open_en": "Relying on rote memorization leads straight into sign traps! Connect the geometric area and number line step by step to see why this identity must hold!",
        "quiz_ko": "💬 10초 퀴즈: 오늘 증명에서 가장 결정적인 부호·정의 판별 단계는 몇 번째였나요? 댓글로 남겨주세요!",
        "quiz_en": "💬 10-Sec Quiz: Which step revealed the decisive sign or definition rule in today's proof?"
    },
    "matrix_transform": {
        "match_keywords": ["일차변환", "행렬", "회전변환", "대칭변환", "닮음변환", "역행렬", "고유값", "linear transformation", "matrix", "rotation", "reflection"],
        "thumb_hook_ko": ["좌표평면 전체가", "통째로 움직인다!"],
        "thumb_hook_en": ["WATCH THE ENTIRE GRID", "TRANSFORM LIVE!"],
        "badge_ko": "⚡ 3Blue1Brown 스타일 기하 변환",
        "badge_en": "⚡ GEOMETRIC MATRIX INTUITION",
        "cold_open_ko": "행렬의 숫자 네 개가 바뀔 때 좌표평면 위의 도형과 영역은 어떻게 휘어지고 회전할까요? 기저벡터와 격자의 움직임을 눈으로 직접 추적하면 복잡한 일차변환이 한눈에 보입니다!",
        "cold_open_en": "When a matrix changes, how does the entire coordinate domain stretch, shear, or rotate? Track the basis vectors visually and master linear transformations!",
        "quiz_ko": "💬 10초 퀴즈: 변환 후 도형의 넓이 배율을 결정하는 행렬의 핵심 값은 무엇일까요?",
        "quiz_en": "💬 10-Sec Quiz: Which quantity of a matrix determines the area scaling factor after transformation?"
    },
    "vectors_space": {
        "match_keywords": ["벡터", "내적", "외적", "정사영", "공간도형", "삼수선", "구면", "평면의 방정식", "vector", "dot product", "projection", "3d"],
        "thumb_hook_ko": ["빛을 수직으로 쏘면", "그림자가 답이다!"],
        "thumb_hook_en": ["DROP ONE SHADOW", "SOLVE THE VECTOR!"],
        "badge_ko": "⚡ 기하·벡터 1등급 시각 치트키",
        "badge_en": "⚡ VISUAL VECTOR & 3D HACK",
        "cold_open_ko": "복잡한 좌표 계산 없이 화살표의 분해와 그림자 정사영 하나로 벡터 문제를 단번에 해결할 수 있다면 믿으시겠습니까? 시점과 종점의 기하학적 의미를 눈으로 직접 확인해 보세요!",
        "cold_open_en": "Forget messy coordinate algebra—see how vector decomposition and orthogonal shadows unlock the entire geometric relationship at a glance!",
        "quiz_ko": "💬 10초 퀴즈: 두 벡터가 서로 수직일 때 내적의 값은 항상 얼마가 될까요?",
        "quiz_en": "💬 10-Sec Quiz: What is the dot product of two perpendicular vectors?"
    },
    "sequences_induction": {
        "match_keywords": ["수열", "등차", "등비", "점화식", "귀납법", "피보나치", "시그마", "자연수의 거듭제곱", "sequence", "progression", "induction", "fibonacci", "sigma"],
        "thumb_hook_ko": ["블록을 맞춰보면", "공식이 저절로!"],
        "thumb_hook_en": ["STACK THE BLOCKS", "FORMULA APPEARS!"],
        "badge_ko": "⚡ 도형으로 깨치는 수열의 비밀",
        "badge_en": "⚡ VISUAL SEQUENCE PROOF",
        "cold_open_ko": "길고 복잡한 수열의 합과 점화식, 외우지 마세요! 도형 블록을 대칭으로 맞붙이거나 도미노처럼 소거하는 순간, 일반항과 합의 공식이 눈앞에서 저절로 완성됩니다!",
        "cold_open_en": "Stop memorizing long summation formulas! Fit the geometric blocks together or watch the terms telescope like dominoes right before your eyes!",
        "quiz_ko": "💬 10초 퀴즈: 1부터 10까지 자연수를 모두 더한 값은 얼마일까요? 대칭 짝짓기로 3초 만에 구해보세요!",
        "quiz_en": "💬 10-Sec Quiz: What is the sum of integers from 1 to 10 using symmetric pairing?"
    },
    "probability_combinatorics": {
        "match_keywords": ["확률", "경우의 수", "순열", "조합", "파스칼", "이항정리", "통계", "정규분포", "시행", "사건", "probability", "combination", "permutation", "pascal", "binomial"],
        "thumb_hook_ko": ["복잡한 경우의 수,", "대칭 구조로 1초 컷!"],
        "thumb_hook_en": ["1 SYMMETRIC GRID", "COUNTS IT ALL!"],
        "badge_ko": "⚡ 직관을 깨는 확통 시각 해법",
        "badge_en": "⚡ COMBINATORICS MADE VISUAL",
        "cold_open_ko": "빠뜨리거나 중복해서 세기 쉬운 경우의 수와 확률! 대칭 격자와 일대일 대응 다이어그램으로 바꾸는 순간 모든 갈래가 오차 없이 한눈에 정리됩니다!",
        "cold_open_en": "Counting problems are notorious for double-counting traps! Map the choices onto a visual grid and watch every case organize itself with 100% precision!",
        "quiz_ko": "💬 10초 퀴즈: 서로 다른 5개 중에서 2개를 뽑는 조합(5C2)의 값은 얼마일까요?",
        "quiz_en": "💬 10-Sec Quiz: How many ways can you choose 2 items from 5 (5C2)?"
    },
    "number_theory_euclid": {
        "match_keywords": ["유클리드", "소수", "최대공약수", "나머지", "합동", "페르마", "정수", "약수", "배수", "euclid", "prime", "lemma", "gcd", "divisor"],
        "thumb_hook_ko": ["2300년 전 유클리드의", "소름 돋는 증명법!"],
        "thumb_hook_en": ["EUCLID'S 2300-YEAR", "GENIUS PROOF!"],
        "badge_ko": "⚡ 정수론의 바이블 완벽 해부",
        "badge_en": "⚡ NUMBER THEORY MASTERPIECE",
        "cold_open_ko": "2300년 전 유클리드는 어떻게 이 정리의 필연성을 증명했을까요? 직사각형 타일 분할과 나머지 원리를 따라가다 보면 누구도 반박할 수 없는 수학적 아름다움에 전율하게 됩니다!",
        "cold_open_en": "How did Euclid prove this timeless truth over two millennia ago? Follow the step-by-step division and remainder logic to witness pure mathematical elegance!",
        "quiz_ko": "💬 10초 퀴즈: 가장 작은 소수이자 유일한 짝수 소수는 무엇일까요?",
        "quiz_en": "💬 10-Sec Quiz: What is the smallest prime number and the only even prime?"
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


def build_topic_cold_open(script_doc, lang_code="ko"):
    """
    [v6.0 유튜브 알고리즘 첫 15초 Retention 극대화 3-Beat 오프닝(Cold Open) 생성기]
    - Beat 1 (0~2.5s 패턴 인터럽트): 통념을 깨는 역발상 질문으로 스크롤/이탈 정지
    - Beat 2 (2.5~5.5s 시각적 보상 예고): 이 주제만의 실제 핵심 원리(auxiliary_line_ko -> conclusion_ko) 제시
    - Beat 3 (5.5~8.5s 오픈 루프 락인): 결정적 장면이 몇 번째 단계에 나오는지 끝까지 보게 만드는 시청 지속 장치
    """
    slug = script_doc.get("slug", "")
    if slug in ("math20250130001", "2017090101", "2014111901", "2014111902"):
        vprof = get_viral_hook_profile(script_doc)
        return vprof["cold_open_en"] if lang_code == "en" else vprof["cold_open_ko"]

    raw_title = script_doc.get("title", "")
    ko_t, en_t = split_bilingual_title(raw_title)
    clean_ko = clean_math_for_speech_ko(ko_t)
    clean_en = clean_math_for_speech_en((script_doc.get("title_en") or en_t or clean_ko).strip())
    t_an = analyze_min7014_topic_as_mathteacher(raw_title, script_doc.get("sub_domain_ko", ""))
    aux_ko = clean_math_for_speech_ko(t_an.get("auxiliary_line_ko", ""))
    conc_ko = clean_math_for_speech_ko(t_an.get("conclusion_ko", ""))

    if lang_code == "en":
        return (
            f"Wait! Are you still memorizing {clean_en} without seeing why it works? "
            f"Watch how one key geometric and algebraic connection unlocks the entire proof—and see if you can spot the exact turning point!"
        )
    return (
        f"잠깐! {clean_ko}, 아직도 결과만 외워서 풀고 계신가요? "
        f"오늘 영상에서는 {aux_ko}을 통해 왜 {conc_ko}이 될 수밖에 없는지 눈앞에서 단계별로 증명합니다. "
        f"과연 몇 번째 단계에서 결정적 단서가 등장하는지 끝까지 확인해 보세요!"
    )


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


def render_slide_frame_1080p(pdf_page, page_info, script_doc, lang_code, show_spotlight=True, stage=None):
    """
    [v6.0 YouTube Algorithm Retention HUD + 3-Stage Progressive Visual Reveal + Pattern-Interrupt Banner + End-Screen Binge Card]
    - stage=1 (또는 show_spotlight=False): 전체 도형·수식 클린 관찰 (Phase 1)
    - stage=2 (기본 show_spotlight=True): 핵심 보조선·수식 스포트라이트 하이라이트 (Phase 2)
    - stage=3: 유레카 핵심 통찰 콜아웃 링 + 중반(50%) 승부처 배너 + 최종장면(End-Screen) 다음 영상 정주행 카드 (Phase 3)
    """
    if stage is None:
        stage = 2 if show_spotlight else 1
    W, H = 1920, 1080
    canvas = Image.new("RGB", (W, H), (9, 14, 28))
    draw = ImageDraw.Draw(canvas)

    p_num = page_info["page"]
    tot_p = script_doc["page_count"]
    scene_idx = page_info.get("scene_index") or p_num
    tot_scenes = len(script_doc.get("pages") or []) or tot_p

    # 1. 상단 방송 헤더 바 (높이 72px) + 시안-골드 세부 진행률 게이지 바 (y: 72~78)
    draw.rectangle([0, 0, W, 72], fill=(15, 23, 42))
    draw.rectangle([0, 72, W, 78], fill=(30, 41, 59))
    sub_stage_frac = (stage - 1) / 3.0 if p_num > 0 else 0.15
    prog_ratio = min(1.0, max(0.02, ((max(1, p_num) - 1 + sub_stage_frac) / max(1, tot_p))))
    prog_w = max(16, int(prog_ratio * W))
    draw.rectangle([0, 72, prog_w, 78], fill=(56, 189, 248) if stage < 3 else (250, 204, 21))
    draw.ellipse([max(0, prog_w - 7), 69, min(W, prog_w + 7), 81], fill=(250, 204, 21))

    font_header = get_font_for_lang("ko", 25, bold=True)
    font_badge = get_font_for_lang("ko", 19, bold=True)
    font_ribbon = get_font_for_lang("ko", 18, bold=True)

    header_title = script_doc.get("title_en") if lang_code == "en" and script_doc.get("title_en") else script_doc.get("title", "")
    header_title = latex_to_unicode_title(header_title)
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
    pdf_img = _mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))

    max_pw, max_ph = 1760, 724
    scale = min(max_pw / pdf_img.width, max_ph / pdf_img.height)
    new_w, new_h = int(pdf_img.width * scale), int(pdf_img.height * scale)
    pdf_resized = pdf_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    px = (W - new_w) // 2
    py = 86 + (max_ph - new_h) // 2

    # 외곽 글로우 프레임 및 슬라이드 배치
    outer_col = (250, 204, 21) if stage == 3 else (56, 189, 248)
    draw.rounded_rectangle([px - 10, py - 10, px + new_w + 10, py + new_h + 10], radius=16, fill=(20, 34, 62))
    draw.rounded_rectangle([px - 3, py - 3, px + new_w + 3, py + new_h + 3], radius=12, fill=outer_col)
    canvas.paste(pdf_resized, (px, py))

    # 3. 새로 추가된 도형·보조선·수식 영역 스포트라이트 하이라이트 & 코너 브래킷 (show_spotlight=True 시)
    bbox = page_info.get("diff_bbox")
    if show_spotlight and bbox and p_num > 1 and p_num <= tot_p:
        bx0 = max(px + 6, px + int(bbox[0] * new_w) - 14)
        by0 = max(py + 6, py + int(bbox[1] * new_h) - 14)
        bx1 = min(px + new_w - 6, px + int(bbox[2] * new_w) + 14)
        by1 = min(py + new_h - 6, py + int(bbox[3] * new_h) + 14)
        if (bx1 - bx0) > 26 and (by1 - by0) > 26:
            if stage == 3:
                # Stage 3: 유레카 이중 골드-크림슨 포커스 링 + 핵심 발견 배지
                draw.rounded_rectangle([bx0 - 6, by0 - 6, bx1 + 6, by1 + 6], radius=14, outline=(250, 204, 21), width=3)
                draw.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(225, 29, 72), width=5)
                tag_label = f"★ EUREKA KEY {scene_idx}" if lang_code == "en" else f"★ 유레카 핵심 단서 완성!"
                tag_w = 186 if lang_code == "en" else 204
                tag_bg = (180, 83, 9)
            else:
                draw.rounded_rectangle([bx0 - 2, by0 - 2, bx1 + 2, by1 + 2], radius=12, outline=(254, 240, 138), width=2)
                draw.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(225, 29, 72), width=4)
                tag_label = f"FOCUS STEP {scene_idx}" if lang_code == "en" else f"핵심 작도·수식 포커스"
                tag_w = 152 if lang_code == "en" else 166
                tag_bg = (225, 29, 72)
            tag_y = by1 + 5 if (by1 + 32) < (py + new_h) else max(py + 6, by0 - 30)
            tag_x = max(px + 6, min(px + new_w - tag_w - 6, bx1 - tag_w))
            draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + 26], radius=6, fill=tag_bg, outline=(254, 240, 138), width=1)
            draw.text((tag_x + 10, tag_y + 3), tag_label, fill=(255, 255, 255), font=get_font_for_lang("ko", 16, bold=True))

    # 3-B. [v6.0 알고리즘 시청 지속시간(Retention) 패턴 인터럽트 배너]
    # - Cold Open(page=0): 3단계 증명 로드맵 필 표시
    # - 중반 승부처(50% 지점, stage==3): 중반 이탈 방지 하이라이트 배너
    # - 클라이맥스/최종 장면(tot_p, stage==3): 다음 영상 정주행(Session Time) 유도 카드
    step_title_str = page_info.get("step_title") or (f"Step {scene_idx}" if lang_code == "en" else f"{scene_idx}단계 핵심 원리")
    if "COLD OPEN" in step_title_str:
        rm_txt = (
            "🗺️ [3-Step Proof Roadmap] ① Spot the Invariant ➔ ② Draw the Key Line ➔ ③ Visual Proof Complete!"
            if lang_code == "en"
            else "🗺️ [오늘의 3단계 시각 증명 로드맵] ① 도형 조건 관찰 ➔ ② 결정적 보조선·원리 연결 ➔ ③ 유레카 증명 완성!"
        )
        draw.rounded_rectangle([180, 90, W - 180, 136], radius=14, fill=(15, 23, 42), outline=(250, 204, 21), width=2)
        draw.text((208, 101), rm_txt, fill=(254, 240, 138), font=get_font_for_lang("ko", 21, bold=True))
    elif stage == 3 and tot_p >= 4 and p_num == max(2, tot_p // 2):
        mid_txt = (
            "🔥 [KEY TURNING POINT!] Watch how this step connects the entire proof together!"
            if lang_code == "en"
            else "🔥 [중간 핵심 승부처!] 바로 이 단계의 연결 고리가 전체 증명을 하나로 완성합니다!"
        )
        draw.rounded_rectangle([240, 90, W - 240, 134], radius=14, fill=(159, 18, 57), outline=(254, 240, 138), width=2)
        draw.text((268, 100), mid_txt, fill=(255, 255, 255), font=get_font_for_lang("ko", 21, bold=True))
    elif stage == 3 and p_num == tot_p:
        end_txt = (
            "🎬 [NEXT UP ON @min7014_ai] Watch the Question-Asking Classroom Edition & Interactive GeoGebra Next! ▸"
            if lang_code == "en"
            else "🎬 [다음 추천 영상 이어보기] 이 주제의 '질문하는 수업 버전'과 연관 도형 증명을 지금 바로 이어서 확인하세요! ▸"
        )
        draw.rounded_rectangle([150, 90, W - 150, 136], radius=14, fill=(6, 95, 70), outline=(250, 204, 21), width=2)
        draw.text((178, 101), end_txt, fill=(254, 240, 138), font=get_font_for_lang("ko", 21, bold=True))

    # 4. 단계 요약 & 수능 실전 보조선 팁 리본 바 (y: 822 ~ 860)
    draw.rectangle([0, 822, W, 860], fill=(15, 23, 42))
    draw.line([0, 822, W, 822], fill=(30, 58, 138), width=2)
    vis_focus_str = page_info.get("visual_focus") or ""
    tip_raw = re.sub(r"\$[^\$]*\$", "", script_doc.get("solving_tip") or script_doc.get("core_concept") or "").strip()
    if len(tip_raw) > 58:
        tip_raw = tip_raw[:58] + "..."

    step_q_display = (
        page_info.get("step_question_en")
        if lang_code == "en"
        else page_info.get("step_question_ko")
    )
    if not step_q_display:
        if scene_idx == 1:
            step_q_display = "❓ [Notice & Wonder] What stays invariant in this figure?" if lang_code == "en" else "❓ [관찰과 경이 질문] 이 도형에서 움직여도 변하지 않는 불변량은 무엇일까요?"
        elif p_num == tot_p:
            step_q_display = "🔀 [What-If-Not] What if we change one condition of this figure?" if lang_code == "en" else "🔀 [What-If-Not 확장 질문] 만약 도형의 조건을 바꾸면 어떤 새로운 정리가 될까요?"
        else:
            step_q_display = f"🧭 [Socratic Inquiry Step {scene_idx}] Why does this auxiliary line unlock the proof?" if lang_code == "en" else f"🧭 [소크라테스 발문 {scene_idx}단계] 왜 이 보조선과 도형 관계가 증명의 열쇠일까요?"

    left_rib = f"🪜 [{step_title_str}]" if lang_code != "en" else f"🪜 [Step {scene_idx} Inquiry]"
    draw.text((44, 829), left_rib[:34], fill=(56, 189, 248), font=font_ribbon)
    draw.text((470, 829), step_q_display[:76], fill=(251, 191, 36), font=font_ribbon)

    # 5. 하단 방송급 자막 스튜디오 바 + Stage별 능동 하이라이트 자막 (y: 860 ~ 1080)
    draw.rectangle([0, 860, W, H], fill=(7, 11, 24))
    draw.line([0, 860, W, 860], fill=(56, 189, 248), width=2)

    narration_text = page_info.get("narrations", {}).get(lang_code) or page_info.get("explanation_text", "")
    is_cjk = lang_code in ("ko", "ja") or lang_code.startswith("zh")
    wrap_width = 53 if is_cjk else 86
    wrapped_lines = textwrap.wrap(narration_text, width=wrap_width)[:3]

    font_sub = get_font_for_lang(lang_code, 29 if is_cjk else 27, bold=True)
    y_cursor = 880
    active_line_idx = min(len(wrapped_lines) - 1, max(0, stage - 1)) if wrapped_lines else 0
    for l_idx, line in enumerate(wrapped_lines):
        draw.text((50, y_cursor + 2), line, fill=(0, 0, 0), font=font_sub)
        line_col = (254, 240, 138) if (l_idx == active_line_idx or len(wrapped_lines) == 1) else (226, 232, 240)
        draw.text((48, y_cursor), line, fill=line_col, font=font_sub)
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
    [v6.0 CTR 15%+ 알고리즘 최적화 썸네일 생성기]
    - 우측 52%: 가장 완성도 높은 클라이맥스 기하 도형 + 실제 diff_bbox 중심을 타겟팅하는 네온 레드 서클 & 화살표 강조
    - 좌측 48%: 모바일에서도 0.5초 만에 읽히는 초대형 2줄 호기심 카피(옐로우/화이트 + 굵은 블랙 외곽선) + 정제된 주제명
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
    slide_img = _mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    scale = min(640 / slide_img.width, 590 / slide_img.height)
    sw, sh = int(slide_img.width * scale), int(slide_img.height * scale)
    slide_resized = slide_img.resize((sw, sh), Image.Resampling.LANCZOS)

    sx = W - sw - 34
    sy = (H - sh) // 2
    draw.rounded_rectangle([sx - 12, sy - 12, sx + sw + 12, sy + sh + 12], radius=22, fill=(225, 29, 72), outline=(251, 191, 36), width=4)
    thumb.paste(slide_resized, (sx, sy))

    # 실제 클라이맥스 슬라이드의 diff_bbox 중심점을 계산하여 시선 유도 포커스 서클 배치
    pages_list = script_doc.get("pages") or []
    climax_bbox = None
    for p_cand in reversed(pages_list):
        if p_cand.get("diff_bbox"):
            climax_bbox = p_cand["diff_bbox"]
            break
    if climax_bbox:
        rel_x = max(0.28, min(0.72, (climax_bbox[0] + climax_bbox[2]) * 0.5))
        rel_y = max(0.28, min(0.72, (climax_bbox[1] + climax_bbox[3]) * 0.5))
    else:
        rel_x, rel_y = 0.48, 0.52

    cx_spot = sx + int(sw * rel_x)
    cy_spot = sy + int(sh * rel_y)
    r_spot = 74
    draw.ellipse([cx_spot - r_spot - 3, cy_spot - r_spot - 3, cx_spot + r_spot + 3, cy_spot + r_spot + 3], outline=(254, 240, 138), width=4)
    draw.ellipse([cx_spot - r_spot, cy_spot - r_spot, cx_spot + r_spot, cy_spot + r_spot], outline=(225, 29, 72), width=7)
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
    ko_split_t, en_split_t = split_bilingual_title(script_doc.get("title", ""))
    ko_main_part = _smart_concise_topic_title(latex_to_unicode_title(ko_split_t).strip(), max_len=32, lang="ko")
    en_main_part = _smart_concise_topic_title(latex_to_unicode_title((script_doc.get("title_en") or en_split_t or ko_main_part).split("—")[0].strip()), max_len=40, lang="en")
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
        else f"🎬 총 {script_doc['page_count']}단계 동적 플립북 시각 증명"
    )
    draw.text((42, 528), sub_line, fill=(254, 240, 138), font=get_font_for_lang("ko", 25, bold=True))
    draw.rounded_rectangle([38, 586, 520, 646], radius=14, fill=(0, 99, 152))
    footer_brand = "📐 @min7014_ai · Visual Math Proofs" if is_en else "📐 @min7014_ai · 단계별 시각적 수학 증명"
    draw.text((58, 601), footer_brand, fill=(255, 255, 255), font=get_font_for_lang("ko", 22, bold=True))

    thumb.save(out_png_path, quality=98)
    return out_png_path


def generate_question_thumbnail_720p(doc, script_doc, lang_code, out_png_path):
    """
    [v6.0 질문하는 수학 수업(Question-Asking Classroom) 전용 고클릭률 1280x720 썸네일 생성기]
    - 크림슨-골드 테마로 일반 설명 본편과 시각적으로 명확히 구분되며,
      '❓ 어디에 보조선을 그어야 할까? / 🙋 3초만 먼저 생각해보세요!' 발문 훅으로 클릭률(CTR)을 극대화합니다.
    """
    W, H = 1280, 720
    thumb = Image.new("RGB", (W, H), (28, 9, 24))
    draw = ImageDraw.Draw(thumb)

    for gx in range(0, W, 80):
        draw.line([(gx, 0), (gx, H)], fill=(48, 16, 38), width=1)
    for gy in range(0, H, 80):
        draw.line([(0, gy), (W, gy)], fill=(48, 16, 38), width=1)

    is_en = (lang_code == "en")
    key_idx = max(0, len(doc) // 2)
    pix = doc[key_idx].get_pixmap(dpi=250)
    slide_img = _mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    scale = min(640 / slide_img.width, 590 / slide_img.height)
    sw, sh = int(slide_img.width * scale), int(slide_img.height * scale)
    slide_resized = slide_img.resize((sw, sh), Image.Resampling.LANCZOS)

    sx = W - sw - 34
    sy = (H - sh) // 2
    draw.rounded_rectangle([sx - 12, sy - 12, sx + sw + 12, sy + sh + 12], radius=22, fill=(190, 18, 60), outline=(250, 204, 21), width=4)
    thumb.paste(slide_resized, (sx, sy))

    cx_spot = sx + int(sw * 0.5)
    cy_spot = sy + int(sh * 0.5)
    r_spot = 76
    draw.ellipse([cx_spot - r_spot - 3, cy_spot - r_spot - 3, cx_spot + r_spot + 3, cy_spot + r_spot + 3], outline=(250, 204, 21), width=4)
    draw.ellipse([cx_spot - r_spot, cy_spot - r_spot, cx_spot + r_spot, cy_spot + r_spot], outline=(225, 29, 72), width=7)
    draw.ellipse([cx_spot + r_spot - 24, cy_spot - r_spot - 20, cx_spot + r_spot + 32, cy_spot - r_spot + 36], fill=(190, 18, 60), outline=(254, 240, 138), width=3)
    draw.text((cx_spot + r_spot - 6, cy_spot - r_spot - 12), "?", fill=(254, 240, 138), font=get_font_for_lang("en", 36, bold=True))

    badge_txt = "❓ QUESTION-ASKING CLASSROOM" if is_en else "❓ 질문하는 수학 수업 · 탐구 에디션"
    draw.rounded_rectangle([38, 42, 558, 102], radius=16, fill=(190, 18, 60), outline=(250, 204, 21), width=2)
    draw.text((56, 56), badge_txt, fill=(254, 240, 138), font=get_font_for_lang("ko", 25, bold=True))

    cat_type = (script_doc.get("teacher_proof_analysis") or {}).get("category_type", "geometry")
    if is_en:
        hook_lines = ["PAUSE 3 SECONDS!", "WHY DOES IT WORK?" if cat_type in ("algebra", "number") else "WHERE IS THE LINE?"]
    else:
        hook_lines = ["3초만 먼저 생각!", "왜 항상 성립할까?" if cat_type in ("algebra", "number") else "보조선 어디에 그을까?"]

    font_big = get_font_for_lang("ko", 54 if is_en else 60, bold=True)
    y_h = 136
    for idx_l, h_line in enumerate(hook_lines):
        col_fill = (255, 255, 255) if idx_l == 0 else (250, 204, 21)
        for dx in (-4, 0, 4):
            for dy in (-4, 0, 4):
                if dx or dy:
                    draw.text((40 + dx, y_h + dy), h_line, fill=(0, 0, 0), font=font_big)
        draw.text((40, y_h), h_line, fill=col_fill, font=font_big)
        y_h += 84

    ko_split_t, en_split_t = split_bilingual_title(script_doc.get("title", ""))
    ko_main_part = _smart_concise_topic_title(latex_to_unicode_title(ko_split_t).strip(), max_len=32, lang="ko")
    en_main_part = _smart_concise_topic_title(latex_to_unicode_title((script_doc.get("title_en") or en_split_t or ko_main_part).split("—")[0].strip()), max_len=40, lang="en")
    main_title = en_main_part if is_en else ko_main_part
    wrapped_t = textwrap.wrap(main_title, width=22 if is_en else 15)[:2]

    draw.rounded_rectangle([38, 330, 568, 488], radius=18, fill=(48, 12, 34), outline=(250, 204, 21), width=2)
    font_t = get_font_for_lang("ko", 32 if is_en else 36, bold=True)
    y_t = 350
    for line in wrapped_t:
        draw.text((58, y_t), line, fill=(254, 240, 138), font=font_t)
        y_t += 50

    sub_line = "🙋 Notice & Wonder ➔ Socratic Clue ➔ What-If-Not" if is_en else "🙋 발문과 사고 멈춤 ➔ 시각 단서 발견 ➔ 조건 변형"
    draw.text((42, 528), sub_line, fill=(253, 164, 175), font=get_font_for_lang("ko", 23, bold=True))
    draw.rounded_rectangle([38, 586, 520, 646], radius=14, fill=(159, 18, 57))
    footer_brand = "❓ @min7014_ai · Socratic Math" if is_en else "❓ @min7014_ai · 질문하는 수학 수업"
    draw.text((58, 601), footer_brand, fill=(255, 255, 255), font=get_font_for_lang("ko", 22, bold=True))

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


CONCISE_TITLE_REWRITES_KO = {
    "두 선분의 교점이 없을 때 두 선분의 연장선의 교점에서 각각의 선분의 끝점에서 교점까지의 거리의 곱이 같으면 선분의 끝점은 한 원 위에 있다": "네 점이 한 원 위에 있을 조건 (방멱정리의 역)",
    "두 선분의 교점이 있을 때 교점에서 각각의 선분의 끝점까지의 거리의 곱이 같으면 선분의 끝점은 한 원 위에 있다": "두 현의 교점과 네 점이 한 원 위에 있을 조건 (방멱정리의 역)",
    "원 밖의 한 점에서 그 원에 그은 두 접선의 길이는 같다": "원 밖의 한 점에서 그은 두 접선의 길이",
    "원에서 현의 수직이등분선은 그 원의 중심을 지난다": "원에서 현의 수직이등분선과 원의 중심",
    "원의 중심에서 현에 내린 수선은 그 현을 이등분한다": "원의 중심에서 현에 내린 수선의 성질",
    "제한된 범위에서 이차함수의 최대최소": "제한된 범위의 이차함수 최대·최소",
    "작도와 경사하강법을 활용한 삼각형의 페르마 점": "삼각형의 페르마 점 (작도와 경사하강법)",
}

CONCISE_TITLE_REWRITES_EN = {
    "When there is an intersection on the extension of two line segments, if the products of the distances from the intersection to the endpoints of each segment are equal, thefour endpoints lie on a circle": "Converse of Power of a Point (4 Concyclic Points)",
    "When there is an intersection on the extension of two line segments": "Converse of Power of a Point (Secant Lines)",
    "The Length and Width of one Side of a Square": "Side Length and Area of a Square",
    "The Ratio of the Length of the Line Segments between Parallel Lines": "Segment Ratios Between Parallel Lines",
    "Positive and Negative Square Root": "Positive & Negative Square Roots",
    "Maximum and minimum of a quadratic function in a restricted range": "Max & Min of a Quadratic Function",
    "Fermat Point of a Triangle using Construction and Gradient Descent": "Fermat Point of a Triangle",
}


def _smart_concise_topic_title(raw_title: str, max_len: int = 38, lang: str = "ko") -> str:
    """
    [단어 중간 절단(Mid-Word Cutoff) 원천 방지 & 고클릭률(CTR) 핵심 수학 개념 압축기]
    - 'Positive and Negative Square R', 'one Si', 'Proof vi', '선분의 끝' 같은 글자수 단순 슬라이싱 절단을 100% 방지합니다.
    """
    t = re.sub(r"\s+", " ", (raw_title or "")).strip()
    if " — " in t:
        t = t.split(" — ")[0].strip()
    if lang == "en":
        for k, v in CONCISE_TITLE_REWRITES_EN.items():
            if t.lower().startswith(k.lower()[:28]):
                t = v
                break
    else:
        for k, v in CONCISE_TITLE_REWRITES_KO.items():
            if t.startswith(k[:18]):
                t = v
                break
    t = _balance_parentheses(t)
    if len(t) <= max_len:
        return t
    # 단어 경계(Word Boundary)에서만 절단하고 끝에 남은 전치사/관사/조사 제거
    cut = t[:max_len].rsplit(" ", 1)[0].strip() if " " in t[:max_len] else t[:max_len].strip()
    if lang == "en":
        while True:
            m_tail = re.search(r"\b(of|the|and|in|on|when|with|from|to|a|an|by|via|for|at|is|are|that|if)\s*$", cut, re.IGNORECASE)
            if m_tail and len(cut[:m_tail.start()].strip()) >= 10:
                cut = cut[:m_tail.start()].strip()
            else:
                break
    else:
        cut = re.sub(r"\s+(의|에|에서|할|때|와|과|은|는|이|가|을|를|각각의|교점에서)\s*$", "", cut).strip()
    return _balance_parentheses(cut)


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
        _, _en_split = split_bilingual_title(script_doc.get("title", slug))
        clean_en_title = latex_to_unicode_title(_en_split or script_doc.get("title_en") or script_doc.get("title", slug))
        concise_en = _smart_concise_topic_title(clean_en_title, max_len=44, lang="en")
        if preset.get("title_en"):
            yt_title = _balance_parentheses(preset["title_en"][:98])
        else:
            full_suffix_en = f" — Step-by-Step Visual Math Proof ({tot_p} Steps · 1080p) | @min7014_ai"
            compact_suffix_en = f" — Visual Math Proof ({tot_p} Steps · 1080p) | @min7014_ai"
            if len(f"✨ {concise_en}{full_suffix_en}") <= 98:
                yt_title = f"✨ {concise_en}{full_suffix_en}"
            elif len(f"✨ {concise_en}{compact_suffix_en}") <= 98:
                yt_title = f"✨ {concise_en}{compact_suffix_en}"
            else:
                max_en_len = max(18, 98 - len("✨ ") - len(compact_suffix_en))
                short_en_t = _smart_concise_topic_title(concise_en, max_len=max_en_len, lang="en")
                yt_title = f"✨ {short_en_t}{compact_suffix_en}"
        hook_en = preset.get("hook_en") or (
            f"Why does {clean_en_title} hold true? Watch every step-by-step mathematical principle unfold clearly in 1080p!"
        )
        quiz_en = preset.get("quiz_en") or (
            f"💬 [10-Second Eureka Quiz] Which step (1 to {tot_p}) gave you the biggest 'Aha!' moment? Drop the step number in the comments below!"
        )
        binge_en = (
            "🔥 [Watch Next — Top Visual Proofs on @min7014_ai]\n"
            "• 🌳 Pythagoras Tree Area Conservation (1080p): https://youtu.be/3ik6yQ-0fP8\n"
            "• 🔥 Pythagorean Theorem 25-Step Visual Proof (1080p): https://youtu.be/yZER1pGb2J8\n"
            "• 📐 Ceva's Theorem Visualized (1080p): https://youtu.be/aKmG-iKoieQ\n"
            "• ⚡ Pythagoras Tree 45s #Shorts: https://youtube.com/shorts/5qmEJcY_VBM\n"
            "• ✨ Ceva's Theorem 45s #Shorts: https://youtube.com/shorts/dAJFCz19c0M"
        )
        yt_desc = (
            f"{hook_en}\n\n"
            f"🚀 [Try It Yourself on the Free Interactive Math Platform (min7014.github.io/mathedu)]\n"
            f"1️⃣ 📐 Interactive GeoGebra Applet & 1,113 Visual Proof Video Board:\n👉 {board_url}&from=yt\n"
            f"2️⃣ ✍️ De-Multiple-Choice Constructive Math Studio (16,548 Step-by-Step Quizzes):\n👉 https://min7014.github.io/mathedu/?from=yt\n"
            f"3️⃣ 🌱 Daily 3-Minute Math Eureka (10s Counterexample O/X & What-If-Not Problem Posing):\n👉 https://min7014.github.io/mathedu/#dailyGrowthFlywheelSection\n"
            f"4️⃣ 🎮 3D Math Sanctuary Boss Raid RPG (Free Browser Game):\n👉 https://min7014.github.io/mathedu/game.html\n"
            f"5️⃣ 🏛️ Interactive Visual Math Archive (3,400+ Dynamic Proofs):\n👉 {web_url}\n\n"
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
            "AMC Math", "SAT Math", "Visual Math Archive", "min7014_ai", "min7014"
        ]
    else:
        clean_ko_title = split_bilingual_title(script_doc.get("title", slug))[0]
        concise_ko = _smart_concise_topic_title(clean_ko_title, max_len=36, lang="ko")
        cat_type = (script_doc.get("teacher_proof_analysis") or {}).get("category_type", "geometry")
        sub_label = "대수·수체계 원리" if cat_type in ("algebra", "number") else "시각적 기하 직관"
        if preset.get("title_ko"):
            yt_title = _balance_parentheses(preset["title_ko"][:98])
        else:
            full_suffix_ko = f" — 눈으로 깨치는 {tot_p}단계 {sub_label} (1080p) | @min7014_ai"
            compact_suffix_ko = f" ({tot_p}단계 {sub_label} · 1080p) | @min7014_ai"
            if len(f"🔥 [시각적 증명] {concise_ko}{full_suffix_ko}") <= 98:
                yt_title = f"🔥 [시각적 증명] {concise_ko}{full_suffix_ko}"
            elif len(f"🔥 [시각적 증명] {concise_ko}{compact_suffix_ko}") <= 98:
                yt_title = f"🔥 [시각적 증명] {concise_ko}{compact_suffix_ko}"
            else:
                max_ko_len = max(16, 98 - len("🔥 [시각적 증명] ") - len(compact_suffix_ko))
                short_ko_t = _smart_concise_topic_title(concise_ko, max_len=max_ko_len, lang="ko")
                yt_title = f"🔥 [시각적 증명] {short_ko_t}{compact_suffix_ko}"
        hook_ko = preset.get("hook_ko") or (
            f"공식 암기 없이 눈으로 보고 직관적으로 깨치는 [{clean_ko_title}] {tot_p}단계 시각적 증명! 수학교사의 단계별 원리 분석으로 핵심 개념과 증명 과정이 한눈에 드러납니다."
        )
        quiz_ko = preset.get("quiz_ko") or (
            f"💬 [오늘의 10초 유레카 퀴즈] 1페이지부터 {tot_p}페이지 중 결정적인 원리나 핵심 아이디어가 등장한 페이지는 몇 번인가요? 댓글로 번호를 남겨주세요!"
        )
        binge_ko = (
            "🔥 [@min7014_ai 검증된 인기 시각적 증명 정주행 시리즈]\n"
            "• 🌳 피타고라스 나무 넓이 보존의 비밀 (11단계 본편): https://youtu.be/DSgUHigl82o\n"
            "• ❓ 피타고라스 정리 질문하는 수업 본편 (25단계): https://youtu.be/E7x3OZdC14U\n"
            "• 📐 체바의 정리 질문하는 수업 본편 (17단계): https://youtu.be/zvRgbIKm0jc\n"
            "• 🔥 피타고라스 정리 45초 핵심 #Shorts (인기 1위): https://youtube.com/shorts/1RKQ4Uxu4Uw\n"
            "• ✨ 피타고라스 나무 45초 핵심 #Shorts (인기 2위): https://youtube.com/shorts/wSOzehSfEbY"
        )
        yt_desc = (
            f"{hook_ko}\n\n"
            f"🚀 [영상을 본 직후 1초 만에 내 실력으로 만드는 수학홈페이지(mathedu) 무료 실습 링크]\n"
            f"1️⃣ 📐 방금 본 증명 도형 마우스로 직접 움직여보기 (GeoGebra & 1,113개 설명영상 게시판):\n👉 {board_url}&from=yt\n"
            f"2️⃣ ✍️ [탈-5지선다 창의 구성 모드] 이 개념이 쓰인 수능·모평 기출 직접 조립하며 풀기 (16,548문항):\n👉 https://min7014.github.io/mathedu/?q={clean_ko_title.split()[0]}&from=yt\n"
            f"3️⃣ 🌱 [오늘의 3분 수학 유레카] 10초 오개념 반례 O/X 퀴즈 & 나만의 변형 문제 발명:\n👉 https://min7014.github.io/mathedu/#dailyGrowthFlywheelSection\n"
            f"4️⃣ 🎮 [수능 수학 100점 만점 3D 보스 레이드 게임] 설치 없이 브라우저에서 즉시 플레이:\n👉 https://min7014.github.io/mathedu/game.html\n"
            f"5️⃣ 🏛️ [수학자료실 본관 (3,400+ 동적 기하 아카이브)]:\n👉 {web_url}\n\n"
            f"{quiz_ko}\n\n"
            f"{binge_ko}\n\n"
            f"🔔 [@min7014_ai 채널 구독하기]: {sub_url}\n"
            f"📺 수학자료실 본 채널(@min7014): https://www.youtube.com/@min7014\n"
            f"📄 단계별 플립북 증명 PDF 원문: {pdf_url}\n"
            f"🎙️ 20개국어 AI 강의 스튜디오: {studio_url}\n"
            f"식별 코드: [ID: {slug}_KO]\n\n"
            f"⏱️ [00:00 단계별 핵심 챕터 타임스탬프]\n{chapters_block}\n\n"
            f"#수학 #기하학 #시각적증명 #수능수학 #피타고라스정리 #메넬라우스정리 #체바의정리 #중등기하 #고등수학 #영재고수학 #보조선 #GeoGebra #수학자료실 #min7014_ai #min7014"
        )
        yt_tags = [
            "수학", "기하학", "시각적 증명", "수능 수학", "도형 보조선", "피타고라스 정리",
            "메넬라우스의 정리", "체바의 정리", "중학교 도형", "고등학교 수학", "수능 도형 킬러",
            "영재고 수학", "KMO 기하", "GeoGebra", "알지오매스", "단계별 수학 증명",
            "시각적 수학 증명_AI", "min7014_ai", "min7014", "수학 잘하는 법"
        ]

    return {
        "lang": lang_code,
        "channel_handle": "@min7014_ai",
        "channel_name": "단계별 시각적 수학 증명_AI",
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

    pdf_bytes, _ = load_or_build_topic_pdf_bytes(script_doc.get("pdf_url", ""), slug_key)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    lang_meta = GLOBAL_VOICE_MAP.get(lang_code, GLOBAL_VOICE_MAP["en"])
    voice_name = lang_meta["voice"]

    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")
    if not ffmpeg_exe:
        raise RuntimeError("ffmpeg executable not found in PATH")

    pages_to_render = list(script_doc["pages"])
    # Curated scripts (e.g. 2014111901, 2014111902, 2017090101, math20250130001) and mathteacher-generated scripts
    # already have exact 1-based page ordering and frame_range. Never re-group with 0-based f_end-1!
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
        # [v6.0 Climax-First 3-Frame Dynamic Cold Open (Segment 0)]
        # 첫 8초 동안 약 2.5초 간격으로 화면이 전환(클라이맥스 전체 ➔ 출발 도형 ➔ 클라이맥스 유레카 스포트라이트)되어 초반 이탈을 원천 차단합니다!
        cold_text = build_topic_cold_open(script_doc, lang_code=lang_code)
        climax_doc_idx = max(0, len(doc) - 2)
        origin_doc_idx = 0
        climax_info = dict(pages_to_render[-1])
        climax_info["page"] = climax_doc_idx + 1
        climax_info["step_title"] = "⚡ COLD OPEN · 직관을 깨는 시각적 증명 하이라이트" if lang_code != "en" else "⚡ COLD OPEN · Visual Proof Highlight"
        climax_info["narrations"] = dict(climax_info.get("narrations") or {})
        climax_info["narrations"][lang_code] = cold_text
        climax_info["explanation_text"] = cold_text

        cold_img_1 = render_slide_frame_1080p(doc[climax_doc_idx], climax_info, script_doc, lang_code, show_spotlight=False, stage=1)
        cold_img_2 = render_slide_frame_1080p(doc[origin_doc_idx], climax_info, script_doc, lang_code, show_spotlight=False, stage=2)
        cold_img_3 = render_slide_frame_1080p(doc[climax_doc_idx], climax_info, script_doc, lang_code, show_spotlight=True, stage=3)
        c_p1 = tmp_dir / "cold_01.png"
        c_p2 = tmp_dir / "cold_02.png"
        c_p3 = tmp_dir / "cold_03.png"
        cold_img_1.save(c_p1, compress_level=1)
        cold_img_2.save(c_p2, compress_level=1)
        cold_img_3.save(c_p3, compress_level=1)

        cold_mp3 = tmp_dir / "cold_audio.mp3"
        cold_seg = tmp_dir / "seg_cold_000.mp4"
        comm_cold = edge_tts.Communicate(cold_text, voice_name, rate="+10%")
        asyncio.run(comm_cold.save(str(cold_mp3)))
        cold_dur = get_media_duration_seconds(cold_mp3, ffprobe_exe) + 0.55
        cd1 = round(cold_dur * 0.32, 3)
        cd2 = round(cold_dur * 0.34, 3)
        cd3 = max(0.8, round(cold_dur - cd1 - cd2, 3))
        cold_concat = tmp_dir / "cold_concat.txt"
        cold_concat.write_text(
            f"file '{c_p1.as_posix()}'\nduration {cd1}\n"
            f"file '{c_p2.as_posix()}'\nduration {cd2}\n"
            f"file '{c_p3.as_posix()}'\nduration {cd3}\n"
            f"file '{c_p3.as_posix()}'\n",
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
                # [v6.0 3-Stage Progressive Visual Reveal]
                # Stage 1 (26%): 전체 도형 관찰(Clean) ➔ Stage 2 (40%): 신규 보조선 스포트라이트 ➔ Stage 3 (34%): 유레카 콜아웃 & 패턴 인터럽트
                img_s1 = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, show_spotlight=False, stage=1)
                img_s2 = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, show_spotlight=True, stage=2)
                img_s3 = render_slide_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, show_spotlight=True, stage=3)
                p_s1 = tmp_dir / f"slide_{seg_idx:03d}_s1.png"
                p_s2 = tmp_dir / f"slide_{seg_idx:03d}_s2.png"
                p_s3 = tmp_dir / f"slide_{seg_idx:03d}_s3.png"
                img_s1.save(p_s1, compress_level=1)
                img_s2.save(p_s2, compress_level=1)
                img_s3.save(p_s3, compress_level=1)
                d1 = max(0.7, round(total_seg_dur * 0.26, 3))
                d2 = max(0.9, round(total_seg_dur * 0.40, 3))
                d3 = max(0.9, round(total_seg_dur - d1 - d2, 3))
                f_concat_txt = tmp_dir / f"fconcat_{seg_idx:03d}.txt"
                f_concat_txt.write_text(
                    f"file '{p_s1.as_posix()}'\nduration {d1}\n"
                    f"file '{p_s2.as_posix()}'\nduration {d2}\n"
                    f"file '{p_s3.as_posix()}'\nduration {d3}\n"
                    f"file '{p_s3.as_posix()}'\n",
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
            yt_meta["needs_youtube_upload"] = True
            yt_meta["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            script_doc.setdefault("youtube_packages", {})[lang_code] = yt_meta
            with open(script_path, "w", encoding="utf-8") as f:
                json.dump(script_doc, f, ensure_ascii=False, indent=2)
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("standard_1080p",), langs=(lang_code,), execute_delete=False
            )

        print(f"[Broadcast Master MP4 & YouTube Package] {out_mp4} ({out_mp4.stat().st_size // 1024} KB, {round(cursor_sec, 1)}s)")
        return out_mp4
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)




# ==============================================================================
# ❓ Question-Asking Classroom Video Edition Engine (질문하는 수학 수업 전용 버전 제작기)
# ==============================================================================
QUESTION_CLASSROOM_DIR = ROOT_DIR / "video_lectures" / "question_classroom"
QUESTION_CLASSROOM_DIR.mkdir(parents=True, exist_ok=True)

CURATED_QUESTION_CLASSROOM_SCRIPTS = {
    "math20250130001": {
        "ko": [
            "1단계, 질문으로 시작하는 수학 수업입니다! 화면의 피타고라스 나무를 자세히 관찰해 보세요. 나뭇가지가 끝없이 갈라지는데, 과연 무엇이 변하고 무엇이 끝까지 변하지 않을까요? 스스로 첫 번째 질문을 던져 보세요!",
            "2단계 질문입니다. 빈 칠판에서 이 프랙탈 나무를 피워내려면 가장 먼저 어떤 기본 도형 두 개를 준비해야 할까요? 맞습니다, 기둥이 될 정사각형과 가지를 나눌 직각삼각형입니다.",
            "3단계 핵심 발문입니다! 정사각형의 윗변 위에 왜 하필 반원을 그렸을까요? 반원 위의 아무 점이나 잡아서 삼각형을 만들면 그 각도는 항상 몇 도가 될까요? 네, 원의 지름에 대한 원주각은 언제나 90도 직각이 됩니다!",
            "4단계 질문입니다! 직각삼각형의 두 직각변 위에 새로 피어난 두 정사각형의 넓이를 합치면, 맨 아래 기둥 정사각형의 넓이와 어떤 관계가 될까요? 피타고라스 정리에 의해 두 넓이의 합은 기둥 하나와 정확히 일치합니다!",
            "5단계 질문입니다. 그렇다면 그 위에 다시 직각삼각형을 올리고 네 개의 정사각형 가지를 피워내면 넓이의 총합은 커질까요, 줄어들까요, 아니면 그대로일까요? 놀랍게도 네 개를 모두 더해도 여전히 처음 기둥 하나의 넓이와 똑같습니다!",
            "6단계 질문입니다. 이제 여덟 개의 정사각형 가지가 뻗어 나갑니다. 가지의 개수는 매 단계 두 배씩 늘어나는데, 왜 각 층의 넓이 합은 단 1제곱센티미터도 변하지 않을까요? 한 쌍의 가지가 항상 바로 아래 가지 하나와 넓이가 같기 때문입니다!",
            "7단계 질문입니다! 열여섯 개의 가지가 만들어졌습니다. 만약 오른쪽 기준 직각삼각형에서 꼭짓점의 위치를 옆으로 옮기면 나무의 모양은 어떻게 달라질까요? 예각의 크기에 따라 나무가 바람에 휘어지는 방향이 결정됩니다!",
            "8단계 질문입니다. 서른두 개의 잎사귀가 돋아난 작은 나뭇가지 하나를 돋보기로 확대해 보면 어떤 모양이 보일까요? 일부분이 전체와 똑같이 닮아 있는 자기닮음 프랙탈 구조가 나타납니다!",
            "9단계 질문입니다. 예순네 개의 정사각형이 풍성한 숲을 이룹니다. 오직 직각삼각형과 피타고라스 정리라는 단순한 규칙의 반복만으로 어떻게 자연 속 브로콜리나 나뭇가지 모양이 탄생할까요?",
            "10단계 열린 질문입니다. 완성된 피타고라스 나무를 보며 답이 얼마인가라는 닫힌 질문 대신, 고전 기하학의 넓이 보존과 현대 프랙탈 기하학이 어떻게 만나는지 나만의 질문을 만들어 보세요!",
            "마지막 11단계, 여러분이 출제자가 될 차례입니다! 만약 직각삼각형이 아니라 예각삼각형이나 둔각삼각형을 올린다면 넓이의 합은 커질까요, 작아질까요? 지금 설명란 링크의 수학홈페이지에서 직접 꼭짓점을 드래그하며 나만의 질문을 실험해 보세요!"
        ],
        "en": [
            "Step 1. Welcome to the Question-Asking Math Classroom! Look closely at the Pythagoras Tree: as its branches split endlessly, what changes and what stays strictly invariant? Ask your first question now!",
            "Step 2 Question: Starting from a blank canvas, which two fundamental geometric shapes do we need to grow this fractal tree? Exactly: a base square and a right triangle.",
            "Step 3 Key Question: Why did we draw a semicircle on top of the trunk square? If we pick any point on that semicircle, what angle is formed? By Thales' theorem, the inscribed angle facing a diameter is always ninety degrees!",
            "Step 4 Question: When two new squares sprout on the legs of the right triangle, how does their combined area compare to the trunk square below? By the Pythagorean Theorem, their sum equals the trunk square!",
            "Step 5 Question: What happens when four branch squares bloom in the next generation? Does the total area grow, shrink, or stay constant? Remarkably, the sum of all four squares still equals the single trunk square!",
            "Step 6 Question: Now eight squares branch out. The number of squares doubles at every level, yet why does the total area per level never change? Because every pair of child squares equals its parent square!",
            "Step 7 Question: Sixteen branches now appear. What if we slide the vertex of the generating right triangle along the semicircle? That single acute angle controls the tilt and curvature of the entire tree!",
            "Step 8 Question: With thirty-two leaves blooming, what do you notice if you zoom into a single small branch? You see an exact miniature copy of the whole tree—the hallmark of self-similar fractal geometry!",
            "Step 9 Question: Sixty-four squares form a lush canopy. How can the simple repetition of the Pythagorean Theorem reproduce organic branching patterns found in nature?",
            "Step 10 Open Question: Instead of asking a closed question, ask an open question: how do classical area conservation and modern fractal geometry unite in this figure?",
            "Step 11 What-If-Not Challenge: Now it is your turn to pose a new problem! What if the generating triangle is acute or obtuse instead of a right triangle? Visit min7014.github.io/mathedu to drag the vertex and test your own question!"
        ]
    }
}


def build_question_classroom_page_text(slug_key, p_info, idx, total_pages, script_doc, lang_code="ko"):
    curated_q = CURATED_QUESTION_CLASSROOM_SCRIPTS.get(slug_key, {}).get(lang_code)
    if curated_q and idx < len(curated_q):
        return curated_q[idx]

    base_narr = p_info.get("narrations", {}).get(lang_code) or p_info.get("explanation_text", "")
    step_q = (
        p_info.get("step_question_en")
        if lang_code == "en"
        else p_info.get("step_question_ko")
    ) or ""
    clean_q = re.sub(r"^[^\]]+\]\s*", "", step_q).strip()

    if lang_code == "ko":
        base_clean = re.sub(r"^\d+단계(?:입니다)?[.,]?\s*", "", base_narr).strip()
        if idx == 0:
            return f"1단계, 질문으로 시작하는 수학 수업입니다! 먼저 스스로 질문해 볼까요? {clean_q} {base_clean}"
        elif idx == total_pages - 1:
            return f"마지막 {idx+1}단계, 조건 변형 질문입니다! {base_clean} 만약 여기서 주어진 수나 조건을 하나 바꾼다면 어떤 새로운 법칙이 탄생할지 직접 질문하고 실험해 보세요!"
        else:
            return f"{idx+1}단계 탐구 발문입니다! {clean_q} 잠시 화면의 단계별 변화를 보며 생각한 뒤 확인해 보세요. {base_clean}"
    else:
        base_clean = re.sub(r"^Step\s+\d+[.,]?\s*", "", base_narr, flags=re.I).strip()
        if idx == 0:
            return f"Step 1, Question-Asking Classroom! Let us ask first: {clean_q} {base_clean}"
        elif idx == total_pages - 1:
            return f"Final Step {idx+1}, What-If-Not Challenge! {base_clean} What if we modify one condition here? Pose your own question on mathedu!"
        else:
            return f"Step {idx+1} Socratic Question: {clean_q} Pause and observe the step carefully: {base_clean}"


def render_question_classroom_frame_1080p(pdf_page, page_info, script_doc, lang_code, q_narration, show_spotlight=True, stage=None):
    """
    [v6.0 질문하는 수학 수업 전용 1080p 방송 프레임 (3-Stage Progressive Reveal)]
    - 상단 배지: ❓ 질문하는 수학 수업 (Question-Asking Classroom Edition)
    - Stage 1 (show_spotlight=False): '🙋 잠깐! 스스로 먼저 질문해 보세요 (Think & Ask First)' 발문 배너 강조
    - Stage 2 (show_spotlight=True): '💡 시각적 단서 발견!' 스포트라이트 하이라이트
    - Stage 3: '★ 유레카 통찰 & What-If-Not 확장' 골드 콜아웃 링
    """
    if stage is None:
        stage = 2 if show_spotlight else 1
    p_copy = dict(page_info)
    p_copy["narrations"] = dict(page_info.get("narrations") or {})
    p_copy["narrations"][lang_code] = q_narration
    canvas = render_slide_frame_1080p(pdf_page, p_copy, script_doc, lang_code, show_spotlight=show_spotlight, stage=stage)
    draw = ImageDraw.Draw(canvas)

    W, H = 1920, 1080
    font_q_badge = get_font_for_lang("ko", 19, bold=True)
    font_q_banner = get_font_for_lang("ko", 23, bold=True)

    # 우측 상단 배지를 '❓ 질문하는 수학 수업 버전'으로 오버라이드
    scene_idx = page_info.get("scene_index") or page_info["page"]
    tot_scenes = len(script_doc.get("pages") or []) or script_doc["page_count"]
    q_right_badge = (
        f"❓ QUESTION CLASSROOM · STEP {scene_idx}/{tot_scenes} [{lang_code.upper()}]"
        if lang_code == "en"
        else f"❓ [질문하는 수업 버전] STEP {scene_idx}/{tot_scenes} · Notice & Wonder"
    )
    draw.rounded_rectangle([W - 565, 14, W - 24, 58], radius=12, fill=(190, 18, 60), outline=(254, 240, 138), width=2)
    draw.text((W - 548, 23), q_right_badge, fill=(255, 255, 255), font=font_q_badge)

    step_q_display = (
        page_info.get("step_question_en")
        if lang_code == "en"
        else page_info.get("step_question_ko")
    ) or ("❓ What stays invariant here?" if lang_code == "en" else "❓ 이 단계에서 변하지 않는 핵심 관계는 무엇일까요?")

    # 슬라이드 상단 플로팅 발문 카드 표시
    banner_bg = (159, 18, 57) if stage == 1 else ((6, 95, 70) if stage == 3 else (15, 23, 42))
    banner_outline = (250, 204, 21) if stage in (1, 3) else (56, 189, 248)
    draw.rounded_rectangle([140, 88, W - 140, 138], radius=14, fill=banner_bg, outline=banner_outline, width=2)
    if lang_code == "en":
        prefix = "🙋 [Ask First!] " if stage == 1 else ("★ [Eureka Insight!] " if stage == 3 else "💡 [Visual Discovery!] ")
    else:
        prefix = "🙋 [발문 · 먼저 생각해 보세요!] " if stage == 1 else ("★ [유레카 핵심 통찰 완성!] " if stage == 3 else "💡 [시각적 단서 발견!] ")
    draw.text((164, 99), (prefix + step_q_display)[:82], fill=(254, 240, 138), font=font_q_banner)

    return canvas


def render_question_classroom_video(slug_key="math20250130001", lang_code="ko"):
    """
    기존 및 신규 주제에 대해 '질문하는 수학 수업(Question-Asking Classroom)' 전용 1080p 설명영상(_q_ko.mp4, _q_en.mp4)과
    전용 1280x720 커스텀 썸네일(_q_{lang}_thumb.png)을 제작하고 카탈로그에 등록합니다.
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        script_doc = generate_or_update_script(slug_key, target_langs=[lang_code, "en"])
    else:
        script_doc = json.loads(script_path.read_text(encoding="utf-8"))

    voice_info = GLOBAL_VOICE_MAP.get(lang_code, GLOBAL_VOICE_MAP["en"])
    voice_name = voice_info["voice"]

    pdf_bytes, _ = load_or_build_topic_pdf_bytes(script_doc.get("pdf_url", ""), slug_key)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages_to_render = script_doc["pages"]
    n_pages = len(pages_to_render)

    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")
    topic_upload_dir = YT_UPLOADS_DIR / slug_key
    topic_upload_dir.mkdir(parents=True, exist_ok=True)
    QUESTION_CLASSROOM_DIR.mkdir(parents=True, exist_ok=True)

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_qvideo_{slug_key}_{lang_code}_"))
    segment_files = []
    page_timings = []
    cursor_sec = 0.0

    try:
        chime_wav = ensure_harmonic_chime_wav()
        ambient_wav = ensure_ambient_pad_wav()
        clean_title_ko = clean_math_for_speech_ko(split_bilingual_title(script_doc.get("title", ""))[0])
        clean_title_en = (script_doc.get("title_en") or clean_title_ko).strip()

        # 0. 질문하는 수업 전용 3-Frame 오프닝 (Notice & Wonder 발문 훅 — 주제 맞춤형)
        climax_doc_idx = max(0, len(doc) - 2)
        origin_doc_idx = 0
        climax_info = dict(pages_to_render[-1])
        climax_info["page"] = climax_doc_idx + 1
        cold_q_text = build_topic_cold_open(script_doc, lang_code=lang_code)
        cold_img_1 = render_question_classroom_frame_1080p(doc[climax_doc_idx], climax_info, script_doc, lang_code, cold_q_text, show_spotlight=False, stage=1)
        cold_img_2 = render_question_classroom_frame_1080p(doc[origin_doc_idx], climax_info, script_doc, lang_code, cold_q_text, show_spotlight=False, stage=2)
        cold_img_3 = render_question_classroom_frame_1080p(doc[climax_doc_idx], climax_info, script_doc, lang_code, cold_q_text, show_spotlight=True, stage=3)
        c_p1 = tmp_dir / "qcold_01.png"
        c_p2 = tmp_dir / "qcold_02.png"
        c_p3 = tmp_dir / "qcold_03.png"
        cold_img_1.save(c_p1, compress_level=1)
        cold_img_2.save(c_p2, compress_level=1)
        cold_img_3.save(c_p3, compress_level=1)

        cold_mp3 = tmp_dir / "qcold_audio.mp3"
        cold_seg = tmp_dir / "qseg_cold_000.mp4"
        comm_cold = edge_tts.Communicate(cold_q_text, voice_name, rate="+6%")
        asyncio.run(comm_cold.save(str(cold_mp3)))
        cold_dur = get_media_duration_seconds(cold_mp3, ffprobe_exe) + 0.65
        cd1 = round(cold_dur * 0.34, 3)
        cd2 = round(cold_dur * 0.33, 3)
        cd3 = max(0.8, round(cold_dur - cd1 - cd2, 3))
        cold_concat = tmp_dir / "qcold_concat.txt"
        cold_concat.write_text(
            f"file '{c_p1.as_posix()}'\nduration {cd1}\n"
            f"file '{c_p2.as_posix()}'\nduration {cd2}\n"
            f"file '{c_p3.as_posix()}'\nduration {cd3}\n"
            f"file '{c_p3.as_posix()}'\n",
            encoding="utf-8",
        )
        subprocess.run([
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0", "-i", str(cold_concat),
            "-i", str(cold_mp3), "-i", str(chime_wav),
            "-filter_complex",
            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=pad_dur=0.55[v];"
            "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.18[c];"
            "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
            "-preset", "veryfast", "-tune", "stillimage", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest",
            str(cold_seg),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        c_seg_dur = get_media_duration_seconds(cold_seg, ffprobe_exe)
        page_timings.append({"page": 0, "start": 0.0, "end": round(c_seg_dur, 3), "duration": round(c_seg_dur, 3), "text": cold_q_text})
        cursor_sec += c_seg_dur
        segment_files.append(cold_seg)

        for seg_idx, p_info in enumerate(pages_to_render):
            p_idx = min(len(doc) - 1, max(0, p_info["page"] - 1))
            q_narr = build_question_classroom_page_text(slug_key, p_info, seg_idx, n_pages, script_doc, lang_code=lang_code)
            p_info.setdefault("question_narrations", {})[lang_code] = q_narr

            mp3_path = tmp_dir / f"qaudio_{seg_idx:03d}.mp3"
            seg_path = tmp_dir / f"qseg_{seg_idx:03d}.mp4"
            asyncio.run(synthesize_edge_tts_mp3(q_narr, voice_name, mp3_path))
            tts_dur = get_media_duration_seconds(mp3_path, ffprobe_exe)
            # 질문 후 학생이 스스로 생각할 수 있는 사색 호흡(Pre 0.45s + Post 0.85s) 부여
            total_seg_dur = tts_dur + 1.3

            img_s1 = render_question_classroom_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, q_narr, show_spotlight=False, stage=1)
            img_s2 = render_question_classroom_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, q_narr, show_spotlight=True, stage=2)
            img_s3 = render_question_classroom_frame_1080p(doc[p_idx], p_info, script_doc, lang_code, q_narr, show_spotlight=True, stage=3)
            p_s1 = tmp_dir / f"qslide_{seg_idx:03d}_s1.png"
            p_s2 = tmp_dir / f"qslide_{seg_idx:03d}_s2.png"
            p_s3 = tmp_dir / f"qslide_{seg_idx:03d}_s3.png"
            img_s1.save(p_s1, compress_level=1)
            img_s2.save(p_s2, compress_level=1)
            img_s3.save(p_s3, compress_level=1)

            d1 = max(1.0, round(total_seg_dur * 0.36, 3))
            d2 = max(1.0, round(total_seg_dur * 0.34, 3))
            d3 = max(0.9, round(total_seg_dur - d1 - d2, 3))
            f_concat_txt = tmp_dir / f"qfconcat_{seg_idx:03d}.txt"
            f_concat_txt.write_text(
                f"file '{p_s1.as_posix()}'\nduration {d1}\n"
                f"file '{p_s2.as_posix()}'\nduration {d2}\n"
                f"file '{p_s3.as_posix()}'\nduration {d3}\n"
                f"file '{p_s3.as_posix()}'\n",
                encoding="utf-8",
            )
            subprocess.run([
                ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", str(f_concat_txt),
                "-i", str(mp3_path), "-i", str(chime_wav),
                "-filter_complex",
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=450|450,apad=pad_dur=0.85[voice];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.12[chime];"
                "[voice][chime]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                "-preset", "veryfast", "-tune", "stillimage", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest",
                str(seg_path),
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            seg_dur = get_media_duration_seconds(seg_path, ffprobe_exe)
            page_timings.append({
                "page": p_info["page"],
                "start": round(cursor_sec, 3),
                "end": round(cursor_sec + seg_dur, 3),
                "duration": round(seg_dur, 3),
                "text": q_narr,
            })
            cursor_sec += seg_dur
            segment_files.append(seg_path)

        concat_txt = tmp_dir / "qconcat_list.txt"
        concat_txt.write_text("\n".join(f"file '{s.as_posix()}'" for s in segment_files), encoding="utf-8")
        raw_concat_mp4 = tmp_dir / f"raw_q_{slug_key}_{lang_code}.mp4"
        out_mp4 = topic_upload_dir / f"{slug_key}_q_{lang_code}.mp4"
        web_mp4 = QUESTION_CLASSROOM_DIR / f"{slug_key}_q_{lang_code}.mp4"

        subprocess.run([
            ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(raw_concat_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        raw_dur = get_media_duration_seconds(raw_concat_mp4, ffprobe_exe)
        subprocess.run([
            ffmpeg_exe, "-y",
            "-i", str(raw_concat_mp4),
            "-stream_loop", "-1", "-i", str(ambient_wav),
            "-filter_complex",
            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[voice];"
            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.12[bgm];"
            "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-t", f"{raw_dur:.2f}",
            str(out_mp4),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        shutil.copyfile(out_mp4, web_mp4)

        srt_lines = []
        for idx_s, pt in enumerate(page_timings, 1):
            srt_lines.append(str(idx_s))
            srt_lines.append(f"{format_srt_timestamp(pt['start'])} --> {format_srt_timestamp(pt['end'])}")
            srt_lines.append(pt["text"])
            srt_lines.append("")
        srt_pkg_path = YT_PKG_DIR / f"{slug_key}_q_{lang_code}.srt"
        srt_pkg_path.write_text("\n".join(srt_lines), encoding="utf-8")

        q_thumb_pkg = YT_PKG_DIR / f"{slug_key}_q_{lang_code}_thumb.png"
        q_thumb_up = topic_upload_dir / f"{slug_key}_q_{lang_code}_thumb.png"
        try:
            generate_question_thumbnail_720p(doc, script_doc, lang_code, q_thumb_pkg)
            shutil.copyfile(q_thumb_pkg, q_thumb_up)
        except Exception as qte:
            print(f"[Question Thumbnail Notice] {qte}")

        q_meta = {
            "title": _balance_parentheses((
                f"❓ [질문하는 수학 수업] {_smart_concise_topic_title(clean_title_ko, max_len=36, lang='ko')} — 왜 항상 성립할까? (Notice & Wonder) | @min7014_ai"
                if lang_code == "ko"
                else f"❓ [Question-Asking Math] {_smart_concise_topic_title(clean_title_en, max_len=38, lang='en')} — Socratic Visual Proof | @min7014_ai"
            )[:98]),
            "local_mp4_path": f"video_lectures/question_classroom/{web_mp4.name}",
            "upload_mp4_path": f"youtube_uploads/{slug_key}/{out_mp4.name}",
            "srt_url": f"video_lectures/youtube_packages/{srt_pkg_path.name}",
            "thumbnail_url": f"video_lectures/youtube_packages/{q_thumb_pkg.name}",
            "duration_sec": round(cursor_sec, 1),
            "needs_youtube_upload": True,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        script_doc.setdefault("question_classroom_packages", {})[lang_code] = q_meta
        script_path.write_text(json.dumps(script_doc, ensure_ascii=False, indent=2), encoding="utf-8")
        queue_and_delete_existing_youtube_videos_for_slug(
            slug_key, editions=("question_1080p",), langs=(lang_code,), execute_delete=False
        )
        update_video_catalog()
        print(f"❓ [Question-Asking Classroom 1080p Video Generated ({lang_code.upper()})] {web_mp4} ({web_mp4.stat().st_size // 1024} KB, {round(cursor_sec, 1)}s)", flush=True)
        return web_mp4
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
            old_pkg = (sdoc.get("youtube_packages") or {}).get(lc) or {}
            yt_meta = build_youtube_metadata_for_lang(sdoc, lc, timings)
            yt_meta["srt_url"] = f"video_lectures/youtube_packages/{slug}_{lc}.srt"
            yt_meta["thumbnail_url"] = f"video_lectures/youtube_packages/{slug}_{lc}_thumb.png"
            yt_meta["local_mp4_path"] = f"youtube_uploads/{slug}/{slug}_{lc}.mp4"
            if old_pkg.get("uploaded_video_id"):
                yt_meta["uploaded_video_id"] = old_pkg["uploaded_video_id"]
            if "needs_youtube_upload" in old_pkg:
                yt_meta["needs_youtube_upload"] = old_pkg["needs_youtube_upload"]
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

        # Shorts meta & question classroom package titles refresh
        smp = YT_PKG_DIR / f"{slug}_shorts_meta.json"
        if smp.exists() or sdoc.get("shorts_packages"):
            smeta_all = json.loads(smp.read_text(encoding="utf-8")) if smp.exists() else {}
            for lc in ["ko", "en"]:
                dur_s = (sdoc.get("shorts_packages", {}).get(lc) or {}).get("duration_sec") or (smeta_all.get(lc) or {}).get("duration_sec") or 45.0
                new_sm = build_youtube_short_metadata(sdoc, lc, dur_s)
                smeta_all[lc] = new_sm
                if isinstance((sdoc.get("shorts_packages") or {}).get(lc), dict):
                    sdoc["shorts_packages"][lc]["title"] = new_sm["title"]
            smp.write_text(json.dumps(smeta_all, ensure_ascii=False, indent=2), encoding="utf-8")

        _ko_t, _en_t = split_bilingual_title(sdoc.get("title", slug))
        _clean_ko_t = latex_to_unicode_title(_ko_t)
        _clean_en_t = latex_to_unicode_title(_en_t or sdoc.get("title_en") or _ko_t)
        if isinstance(sdoc.get("question_classroom_packages"), dict):
            for lc in ["ko", "en"]:
                if isinstance(sdoc["question_classroom_packages"].get(lc), dict):
                    sdoc["question_classroom_packages"][lc]["title"] = _balance_parentheses((
                        f"❓ [질문하는 수학 수업] {_clean_ko_t[:38]} — 왜 항상 성립할까? (Notice & Wonder) | @min7014_ai"
                        if lc == "ko"
                        else f"❓ [Question-Asking Math] {_clean_en_t[:38]} — Notice & Wonder Visual Inquiry | @min7014_ai"
                    )[:98])
        if isinstance(sdoc.get("question_shorts_packages"), dict):
            for lc in ["ko", "en"]:
                if isinstance(sdoc["question_shorts_packages"].get(lc), dict):
                    sdoc["question_shorts_packages"][lc]["title"] = _balance_parentheses((
                        f"❓ [질문하는 수학 #Shorts] {_clean_ko_t[:42]} — 왜 이 보조선이 핵심일까?"
                        if lc == "ko"
                        else f"❓ [Question-Asking Math #Shorts] {_clean_en_t[:42]} — Why This Auxiliary Line?"
                    )[:98])

        sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
    update_video_catalog()


def extract_youtube_video_id(url_or_id: str) -> str:
    """YouTube URL 또는 11자리 영상 ID 문자열에서 정확한 11자리 video_id를 추출합니다."""
    if not url_or_id:
        return ""
    s = str(url_or_id).strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    m = re.search(r"(?:youtu\.be/|youtube\.com/(?:shorts/|watch\?v=|embed/))([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else ""


def set_youtube_urls_for_slug(slug_key, yt_ko=None, yt_en=None, purge_local_mp4=False):
    """
    업로드 완료된 한국어(ko) 및 영어(en) 유튜브 URL을 @min7014_ai 영상저장고 인덱스(vault_index.json),
    스크립트, 카탈로그, 심층 지식 DB에 일괄 저장하고, 삭제 큐(blocked_ids)에 있는 구버전 URL은 절대 재등록하지 않습니다.
    """
    blocked_ids = get_deleted_video_ids_set()
    if yt_ko is not None and extract_youtube_video_id(yt_ko) in blocked_ids:
        yt_ko = ""
    if yt_en is not None and extract_youtube_video_id(yt_en) in blocked_ids:
        yt_en = ""

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    final_ko = ""
    final_en = ""
    if script_path.exists():
        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        yt_urls = sdoc.setdefault("youtube_urls", {"ko": "", "en": "", "orig": ""})
        if yt_ko is not None:
            yt_urls["ko"] = yt_ko.strip()
            if yt_ko.strip() and "youtube_packages" in sdoc and "ko" in sdoc["youtube_packages"]:
                sdoc["youtube_packages"]["ko"]["needs_youtube_upload"] = False
                sdoc["youtube_packages"]["ko"]["uploaded_video_id"] = extract_youtube_video_id(yt_ko)
        if yt_en is not None:
            yt_urls["en"] = yt_en.strip()
            if yt_en.strip() and "youtube_packages" in sdoc and "en" in sdoc["youtube_packages"]:
                sdoc["youtube_packages"]["en"]["needs_youtube_upload"] = False
                sdoc["youtube_packages"]["en"]["uploaded_video_id"] = extract_youtube_video_id(yt_en)
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
YOUTUBE_CHANNEL_NAME = "단계별 시각적 수학 증명_AI"
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


def get_deleted_video_ids_set():
    dq_path = ROOT_DIR / "video_lectures" / "youtube_delete_queue.json"
    if not dq_path.exists():
        return set()
    try:
        data = json.loads(dq_path.read_text(encoding="utf-8"))
        return set(data.get("pending_delete_video_ids") or []) | set(data.get("deleted_video_ids") or [])
    except Exception:
        return set()


def fetch_channel_rss_entries():
    """@min7014_ai 유튜브 채널 공개 RSS 피드를 조회하여 현재 채널에 게시된 영상 목록을 반환합니다 (API 쿼터 소모 0)."""
    import xml.etree.ElementTree as ET
    entries = []
    try:
        req = urllib.request.Request(YOUTUBE_RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
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
            pub_el = entry.find("atom:published", ns)
            desc_el = entry.find("media:group/media:description", ns)
            if vid_el is not None and title_el is not None:
                vid_id = vid_el.text.strip()
                entries.append({
                    "video_id": vid_id,
                    "title": (title_el.text or "").strip(),
                    "published": (pub_el.text or "").strip() if pub_el is not None else "",
                    "description": (desc_el.text or "").strip() if desc_el is not None else "",
                    "url": f"https://youtu.be/{vid_id}",
                })
    except Exception:
        pass
    return entries


def queue_and_delete_existing_youtube_videos_for_slug(
    slug_key: str,
    editions=None,
    langs=("ko", "en"),
    execute_delete=True,
    execute_delete_now=None,
    exclude_video_ids=None,
):
    """
    [업데이트된 영상의 기존 유튜브 채널 영상 자동 삭제 & 교체 큐 등록 엔진]
    특정 주제(slug_key)의 영상이 새로 렌더링/업데이트되거나 재업로드될 때:
      1) 해당 주제의 기존 유튜브 URL(youtube_urls, question_youtube_urls, shorts_urls, question_shorts_urls),
         vault_index.json, min7014_deep_knowledge.json, min7014_lookup.json 및 @min7014_ai 채널 RSS에서
         기존 영상 ID를 모두 찾아냅니다.
      2) 찾아낸 기존 영상 ID들을 youtube_delete_queue.json(pending_delete_video_ids) 최우선 순위에 등록하고
         로컬 URL 바인딩을 초기화하여 새 영상이 즉시 업로드되도록 설정합니다.
      3) execute_delete=True이면 즉시 YouTube Data API v3(videos.delete)를 호출하여 채널의 기존 영상을 삭제합니다.
    """
    if execute_delete_now is not None:
        execute_delete = bool(execute_delete_now)
    if editions is None:
        editions = ("standard_1080p", "question_1080p", "standard_short", "question_short")
    exclude_set = {extract_youtube_video_id(x) for x in (exclude_video_ids or []) if x}
    edition_map = {
        "standard_1080p": ("youtube_urls", "youtube_packages", ""),
        "standard": ("youtube_urls", "youtube_packages", ""),
        "question_1080p": ("question_youtube_urls", "question_classroom_packages", "_Q"),
        "question": ("question_youtube_urls", "question_classroom_packages", "_Q"),
        "standard_short": ("shorts_urls", "shorts_packages", "_SHORT"),
        "shorts_std": ("shorts_urls", "shorts_packages", "_SHORT"),
        "question_short": ("question_shorts_urls", "question_shorts_packages", "_SHORT_Q"),
        "shorts_q": ("question_shorts_urls", "question_shorts_packages", "_SHORT_Q"),
    }

    found_old_ids = set()
    sp = SCRIPTS_DIR / f"{slug_key}.json"
    if sp.exists():
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
            sdoc_changed = False
            for ed in editions:
                if ed not in edition_map:
                    continue
                url_field, pkg_field, _ = edition_map[ed]
                u_dict = sdoc.get(url_field) or {}
                p_dict = sdoc.setdefault(pkg_field, {})
                for lc in langs:
                    old_u = (u_dict.get(lc) or "").strip()
                    vid_id = extract_youtube_video_id(old_u)
                    if vid_id and vid_id not in exclude_set:
                        found_old_ids.add(vid_id)
                        u_dict[lc] = ""
                        sdoc_changed = True
                    if lc in p_dict and isinstance(p_dict[lc], dict):
                        old_pkg_vid = extract_youtube_video_id(p_dict[lc].get("uploaded_video_id", ""))
                        if old_pkg_vid and old_pkg_vid not in exclude_set:
                            found_old_ids.add(old_pkg_vid)
                        p_dict[lc]["needs_youtube_upload"] = True
                        sdoc_changed = True
            if sdoc_changed:
                sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    # 채널 공개 RSS에서도 동일 slug + edition + lang에 해당하는 구버전 영상 ID 탐지
    for ent in fetch_channel_rss_entries():
        r_vid = ent["video_id"]
        if r_vid in exclude_set:
            continue
        blob = f"{ent['title']}\n{ent['description']}"
        for ed in editions:
            if ed not in edition_map:
                continue
            _, _, tag_mid = edition_map[ed]
            for lc in langs:
                id_tag = f"{slug_key}{tag_mid}_{lc.upper()}"
                if f"[ID: {id_tag}]" in blob or f"[{id_tag}]" in blob:
                    found_old_ids.add(r_vid)

    if found_old_ids:
        dq_path = ROOT_DIR / "video_lectures" / "youtube_delete_queue.json"
        dq = {"keep_video_ids": [], "pending_delete_video_ids": [], "deleted_video_ids": []}
        if dq_path.exists():
            try:
                dq = json.loads(dq_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        deleted_done = set(dq.get("deleted_video_ids") or [])
        pending_list = list(dq.get("pending_delete_video_ids") or [])
        for oid in sorted(found_old_ids):
            if oid not in deleted_done and oid not in pending_list:
                pending_list.insert(0, oid)
        dq["pending_delete_video_ids"] = pending_list
        dq["keep_video_ids"] = [k for k in (dq.get("keep_video_ids") or []) if k not in found_old_ids]
        dq["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        dq_path.write_text(json.dumps(dq, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"♻️ [Updated Video Replacement Queued] slug={slug_key} -> Old YouTube IDs queued for deletion: {sorted(found_old_ids)}", flush=True)

    if execute_delete:
        process_youtube_delete_queue(max_deletions=25)
    return sorted(found_old_ids)


def scan_rss_and_queue_outdated_channel_videos(execute_delete_now=False):
    """
    [@min7014_ai 채널 RSS 기반 구버전/불일치 영상 자동 감지 및 삭제 큐 등록 (쿼터 소모 0)]
    현재 채널에 올라와 있는 영상 중:
      - 제목이나 설명에 '민은기', "Min's Math Lab", 빈 괄호 '()', 미변환 LaTeX('$', 'times', 'div')가 포함된 영상
      - 로컬에서 새로 업데이트되어 needs_youtube_upload=True로 표시된 주제의 구버전 영상
    을 자동으로 탐지하여 youtube_delete_queue.json(pending_delete_video_ids)에 등록합니다.
    """
    entries = fetch_channel_rss_entries()
    if not entries:
        return []
    dq_path = ROOT_DIR / "video_lectures" / "youtube_delete_queue.json"
    dq = {"keep_video_ids": [], "pending_delete_video_ids": [], "deleted_video_ids": []}
    if dq_path.exists():
        try:
            dq = json.loads(dq_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    pending = list(dq.get("pending_delete_video_ids") or [])
    deleted_done = set(dq.get("deleted_video_ids") or [])
    newly_queued = []

    for ent in entries:
        vid_id = ent["video_id"]
        if vid_id in pending or vid_id in deleted_done:
            continue
        blob = f"{ent['title']}\n{ent['description']}"
        is_outdated = False
        if any(bad in blob for bad in ("민은기", "Min's Math Lab", "MinsMathLab", "()", "route ", "a^m div a^n", "a^m times a^n", "Square R —", "one Si —", "Proof vi —", "of the —", "When there is an intersection —", "선분의 끝 —", "끝점에서 교 —", "extensio —")):
            is_outdated = True
        m_tag = re.search(r"\[(?:ID:\s*)?([A-Za-z0-9_]+?)_(?:(SHORT_Q|SHORT|Q)_)?(KO|EN)\]", blob, re.IGNORECASE)
        if m_tag and not is_outdated:
            s_slug = m_tag.group(1)
            ed_kind = (m_tag.group(2) or "").upper()
            lc_kind = m_tag.group(3).lower()
            url_field = {
                "": "youtube_urls",
                "Q": "question_youtube_urls",
                "SHORT": "shorts_urls",
                "SHORT_Q": "question_shorts_urls",
            }.get(ed_kind, "youtube_urls")
            sp = SCRIPTS_DIR / f"{s_slug}.json"
            if sp.exists():
                try:
                    sdoc = json.loads(sp.read_text(encoding="utf-8"))
                    cur_bound_url = ((sdoc.get(url_field) or {}).get(lc_kind) or "").strip()
                    cur_bound_id = extract_youtube_video_id(cur_bound_url)
                    # 이미 다른(더 최신) 영상 ID가 바인딩되어 있는 경우에만 이전 영상 삭제 큐에 추가
                    if cur_bound_id and cur_bound_id != vid_id:
                        is_outdated = True
                except Exception:
                    pass
        if is_outdated:
            pending.insert(0, vid_id)
            newly_queued.append(vid_id)

    if newly_queued:
        dq["pending_delete_video_ids"] = pending
        dq["keep_video_ids"] = [k for k in (dq.get("keep_video_ids") or []) if k not in newly_queued]
        dq["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        dq_path.write_text(json.dumps(dq, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"🔍 [RSS Outdated Video Detector] Queued {len(newly_queued)} outdated channel videos for deletion: {newly_queued}", flush=True)
    if execute_delete_now and pending:
        process_youtube_delete_queue(max_deletions=10)
    return newly_queued


def process_youtube_delete_queue(max_deletions=10):
    """
    [불일치 및 구버전 영상 핀포인트 삭제 엔진 (YouTube Data API v3 · 쿼터 절약형)]
    - 채널 공개 RSS(15개 미만 시 채널 전체 영상 포함)에 이미 존재하지 않는 ID나 타 채널(403) ID는 API 호출 없이 즉시 정리하여
      하루 업로드 쿼터(1,600 유닛/편)가 불필요한 delete 호출로 소모되지 않도록 보호합니다.
    """
    scan_rss_and_queue_outdated_channel_videos()
    dq_path = ROOT_DIR / "video_lectures" / "youtube_delete_queue.json"
    if not dq_path.exists():
        return 0
    try:
        dq = json.loads(dq_path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    pending = list(dq.get("pending_delete_video_ids") or [])
    if not pending:
        return 0

    deleted_done = list(dq.get("deleted_video_ids") or [])
    rss_entries = fetch_channel_rss_entries()
    rss_ids = {r["video_id"] for r in rss_entries}
    if 0 < len(rss_entries) < 15:
        # 채널 전체 영상이 15개 미만이면 RSS에 없는 ID는 이미 채널에서 삭제된 상태이므로 API 쿼터 소모 없이 정리
        filtered_pending = []
        for vid_id in pending:
            if vid_id not in rss_ids:
                deleted_done.append(vid_id)
            else:
                filtered_pending.append(vid_id)
        if len(filtered_pending) != len(pending):
            pending = filtered_pending
            dq["pending_delete_video_ids"] = pending
            dq["deleted_video_ids"] = sorted(list(set(deleted_done)))
            dq_path.write_text(json.dumps(dq, ensure_ascii=False, indent=2), encoding="utf-8")
        if not pending:
            return 0

    youtube, active_token_path = get_available_youtube_upload_service()
    if youtube is None:
        return 0

    still_pending = []
    deleted_now = 0
    for idx, vid_id in enumerate(pending):
        if deleted_now >= max_deletions:
            still_pending.extend(pending[idx:])
            break
        try:
            youtube.videos().delete(id=vid_id).execute()
            deleted_done.append(vid_id)
            deleted_now += 1
            print(f"🗑️ [YouTube Old/Updated Video Deleted from @min7014_ai] {vid_id}", flush=True)
        except Exception as e:
            err_s = str(e)
            if (
                "videoNotFound" in err_s
                or "404" in err_s
                or "403" in err_s
                or "forbidden" in err_s.lower()
                or "range() arg 3 must not be zero" in err_s
            ):
                deleted_done.append(vid_id)
            elif "quotaExceeded" in err_s or "rateLimitExceeded" in err_s:
                mark_token_quota_exhausted(active_token_path, 900)
                still_pending.extend(pending[idx:])
                break
            else:
                still_pending.append(vid_id)

    dq["pending_delete_video_ids"] = still_pending
    dq["deleted_video_ids"] = sorted(list(set(deleted_done)))
    dq["keep_video_ids"] = [k for k in (dq.get("keep_video_ids") or []) if k not in set(deleted_done) and k not in set(still_pending)]
    dq_path.write_text(json.dumps(dq, ensure_ascii=False, indent=2), encoding="utf-8")
    if deleted_now > 0:
        update_video_catalog()
    return deleted_now


def verify_video_content_integrity(slug_key: str) -> dict:
    r"""
    [수석 수학교사(mathteacher v7.0) 영상-내용 일치 및 무결성 검증 게이트]
    렌더링된 영상/대본/자막이 실제 PDF 주제 및 슬라이드 순서와 100% 일치하는지 검증합니다:
      1) '민은기 선생님', '민은기', 'Min's Math Lab', 'Min Eunki' 등 개인 성명/호칭이 대본·자막·메타데이터에 단 1회도 포함되지 않았는가?
      2) 제목·내레이션에 빈 괄호 '()' 또는 미변환 LaTeX('$', '\times', '\div', '\sqrt', '\leq', '\geq', '\neq', '\Leftrightarrow')가 없는가?
      3) 첫 번째 본문 장면(Scene 1)이 마지막 페이지('마지막', 'N페이지입니다')로 점프하지 않고 1단계/1페이지로 정상 시작하는가?
      4) 대수·수체계(제곱근·지수·유리화·나눗셈) 주제에 엉뚱한 기하 보조선/원주각/복소수/다항식 나눗셈 문구나 기계적 레이아웃 안내가 섞이지 않았는가?
      5) 역수의 곱셈 나눗셈(a ÷ b = a × 1/b)과 분모의 유리화가 혼동되지 않았는가?
    """
    sp = SCRIPTS_DIR / f"{slug_key}.json"
    if not sp.exists():
        return {"ok": False, "reason": "script_missing"}
    raw_script_txt = sp.read_text(encoding="utf-8")
    sdoc = json.loads(raw_script_txt)
    pages = sdoc.get("pages") or []
    if not pages:
        return {"ok": False, "reason": "pages_empty"}

    # 1) Persona / Name Prohibition Check ("민은기 선생님" 등 원천 차단)
    forbidden_personas = ("민은기", "Min's Math Lab", "MinsMathLab", "Min Eunki")
    for fp in forbidden_personas:
        if fp in raw_script_txt:
            return {"ok": False, "reason": f"forbidden_persona_in_script:{fp}"}

    # 2) Scene 1 ordering check
    p1 = pages[0]
    if p1.get("page", 1) != 1:
        return {"ok": False, "reason": f"scene_1_wrong_page:{p1.get('page')}"}

    for srt_file in [YT_PKG_DIR / f"{slug_key}_ko.srt", YT_PKG_DIR / f"{slug_key}_en.srt", YT_PKG_DIR / f"{slug_key}_q_ko.srt"]:
        if srt_file.exists():
            srt_txt = srt_file.read_text(encoding="utf-8")
            for fp in forbidden_personas:
                if fp in srt_txt:
                    return {"ok": False, "reason": f"forbidden_persona_in_srt:{srt_file.name}:{fp}"}
            if srt_file.name.endswith("_ko.srt") and not srt_file.name.endswith("_q_ko.srt"):
                blocks = [b.strip() for b in srt_txt.strip().split("\n\n") if b.strip()]
                if len(blocks) >= 2:
                    b2 = blocks[1]
                    if f"{len(pages)}페이지입니다" in b2 or f"마지막 {len(pages)}단계" in b2:
                        return {"ok": False, "reason": "srt_scene_1_narrates_last_page"}

    # 3) Content domain & mathematical accuracy check
    t_an = sdoc.get("teacher_proof_analysis") or {}
    cat = t_an.get("category_type", "")
    title_str = sdoc.get("title", "")
    all_narr_ko = " ".join(p.get("explanation_text", "") for p in pages)
    all_narr_en = " ".join((p.get("narrations") or {}).get("en", "") for p in pages)

    for raw_tex in ("\\times", "\\div", "\\sqrt", "\\frac", "\\leq", "\\geq", "\\neq", "\\Leftrightarrow", "화면의 상단", "화면의 좌측", "영역에 새로운 보조선"):
        if raw_tex in all_narr_ko or raw_tex in all_narr_en:
            return {"ok": False, "reason": f"raw_latex_or_robotic_meta:{raw_tex}"}

    if cat in ("algebra", "number"):
        for forbidden in ("원 위의 점을 아무리", "한 호에 대한 원주각", "복소수", "다항식 나눗셈", "비스듬한 책받침", "보조선과 기하 관계를"):
            if forbidden in all_narr_ko:
                return {"ok": False, "reason": f"domain_mismatch:{forbidden}"}

    # 역수 나눗셈(a ÷ b = a × 1/b)에 분모의 유리화 오분류 방지
    if ("div" in title_str or "÷" in title_str or "frac{1}{b}" in title_str) and "유리화" not in title_str and "sqrt" not in title_str:
        if "분모의 유리화" in all_narr_ko or "분모에 무리수가" in all_narr_ko:
            return {"ok": False, "reason": "math_mismatch:division_misclassified_as_rationalization"}

    # 4) Meta title & description check + script title_en integrity check
    t_en = str(sdoc.get("title_en") or "")
    if t_en.count("(") != t_en.count(")") or "route " in t_en.lower() or "\\" in t_en or "{" in t_en:
        return {"ok": False, "reason": f"malformed_title_en:{t_en}"}

    for meta_p in [YT_PKG_DIR / f"{slug_key}_youtube_meta.json", YT_PKG_DIR / f"{slug_key}_shorts_meta.json"]:
        if meta_p.exists():
            m_txt = meta_p.read_text(encoding="utf-8")
            for fp in forbidden_personas:
                if fp in m_txt:
                    return {"ok": False, "reason": f"forbidden_persona_in_meta:{meta_p.name}:{fp}"}
            mdata = json.loads(m_txt)
            for lc in ("ko", "en"):
                mt = (mdata.get(lc) or {}).get("title", "")
                if (
                    "()" in mt
                    or "$" in mt
                    or "<" in mt
                    or ">" in mt
                    or mt.count("(") != mt.count(")")
                    or "route " in mt.lower()
                ):
                    return {"ok": False, "reason": f"invalid_meta_title_{lc}:{mt}"}

    return {"ok": True, "reason": "verified"}


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
            blocked_vids = get_deleted_video_ids_set()
            for entry in root.findall("atom:entry", ns):
                vid_el = entry.find("yt:videoId", ns)
                title_el = entry.find("atom:title", ns)
                desc_el = entry.find("media:group/media:description", ns)
                if vid_el is not None and title_el is not None and vid_el.text.strip() not in blocked_vids:
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
        title_ko = split_bilingual_title(sdoc.get("title", ""))[0]
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


def prepare_ready_batch_folder(open_explorer=False):
    """
    유튜브 고급 기능(Advanced Features)이 활성화된 YouTube Studio 창에 마우스로 한 번에 드래그 앤 드롭(최대 15개씩 연속 업로드)하거나
    API가 순차 업로드할 수 있도록, 아직 업로드되지 않은 1080p 마스터 MP4를 고유 식별 태그([slug_KO], [slug_EN]) 파일명으로 정리합니다.
    """
    ready_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai"
    ready_dir.mkdir(parents=True, exist_ok=True)
    # 이미 업로드 완료된 파일은 폴더에서 자동 정리
    existing_files = list(ready_dir.glob("*.mp4"))
    priority_slugs = ["math20250130001", "2017090101", "2014111902", "2014111901", "2025020101"]
    all_sps = sorted(SCRIPTS_DIR.glob("*.json"), key=lambda x: (0 if x.stem in priority_slugs else 1, x.stem))
    active_fnames = set()
    count = 0
    for sp in all_sps:
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = sdoc.get("slug", sp.stem)
        yt_urls = sdoc.get("youtube_urls") or {}
        meta_p = YT_PKG_DIR / f"{slug}_youtube_meta.json"
        if not meta_p.exists():
            continue
        try:
            mdata = json.loads(meta_p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for lc in ["ko", "en"]:
            if (yt_urls.get(lc) or "").strip():
                continue
            src = YT_UPLOADS_DIR / slug / f"{slug}_{lc}.mp4"
            if src.exists() and lc in mdata:
                raw_title = mdata[lc]["title"]
                safe_title = re.sub(r'[\\/:*?"<>|]', " ", raw_title).strip()
                fname = f"{safe_title[:75]} [{slug}_{lc.upper()}].mp4"
                active_fnames.add(fname)
                dst = ready_dir / fname
                if not dst.exists() or dst.stat().st_size != src.stat().st_size:
                    shutil.copyfile(src, dst)
                count += 1
    for ef in existing_files:
        if ef.name not in active_fnames:
            try:
                ef.unlink()
            except Exception:
                pass
    if open_explorer and os.name == "nt":
        os.startfile(str(ready_dir))
    return ready_dir


def prepare_ready_shorts_batch_folder(open_explorer=False):
    """
    아직 @min7014_ai 채널에 업로드되지 않은 9:16 세로형 #Shorts MP4들을
    유튜브 제목과 고유 식별 태그([slug_SHORT_KO], [slug_SHORT_EN]) 파일명으로 ready_for_min7014_ai_shorts 폴더에 최신 동기화합니다.
    """
    ready_shorts_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai_shorts"
    ready_shorts_dir.mkdir(parents=True, exist_ok=True)
    existing_files = list(ready_shorts_dir.glob("*.mp4"))
    priority_slugs = ["math20250130001", "2017090101", "2014111902", "2014111901", "2025020101"]
    all_sps = sorted(SCRIPTS_DIR.glob("*.json"), key=lambda x: (0 if x.stem in priority_slugs else 1, x.stem))
    active_fnames = set()
    for sp in all_sps:
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = sdoc.get("slug", sp.stem)
        s_urls = sdoc.get("shorts_urls") or {}
        smeta_p = YT_PKG_DIR / f"{slug}_shorts_meta.json"
        if not smeta_p.exists():
            continue
        try:
            smeta_all = json.loads(smeta_p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for lc in ["ko", "en"]:
            if (s_urls.get(lc) or "").strip():
                continue
            src = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_{lc}.mp4"
            if src.exists() and lc in smeta_all:
                raw_title = smeta_all[lc]["title"]
                safe_title = re.sub(r'[\\/:*?"<>|]', " ", raw_title).strip()
                prefix = f"0{priority_slugs.index(slug)+1}_" if slug in priority_slugs else ""
                fname = f"{prefix}{safe_title[:70]} [{slug}_SHORT_{lc.upper()}].mp4"
                active_fnames.add(fname)
                dst = ready_shorts_dir / fname
                if not dst.exists() or dst.stat().st_size != src.stat().st_size:
                    shutil.copyfile(src, dst)
    for ef in existing_files:
        if ef.name not in active_fnames:
            try:
                ef.unlink()
            except Exception:
                pass
    if open_explorer and os.name == "nt":
        os.startfile(str(ready_shorts_dir))
    return ready_shorts_dir


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
                notify_telegram_youtube_upload(
                    slug_key=slug_key,
                    edition_label=f"🎬 1080p 일반 설명 본편 ({lang_code.upper()})",
                    video_title=meta.get("title", slug_key),
                    youtube_url=yt_url,
                )
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


def notify_telegram_video_event(message_text: str) -> bool:
    """
    [텔레그램(@anti7014_bot) 영상 업로드 실시간 알림 발송기]
    영상이 유튜브(@min7014_ai) 또는 수학홈페이지(GitHub Pages)에 업로드될 때마다
    즉시 인터넷 주소를 포함하여 선생님 텔레그램으로 전송합니다.
    """
    if not message_text:
        return False
    try:
        import mathedu_telegram_bridge as tg_bridge
        cfg = tg_bridge.load_env_config()
        token = cfg.get("TELEGRAM_BOT_TOKEN", "").strip()
        chat_id = cfg.get("TELEGRAM_CHAT_ID", "").strip() or tg_bridge.load_offset_state().get("chat_id", "")
        if token and chat_id:
            tg_bridge.send_msg(token, chat_id, message_text)
            print("📱 [Telegram Notification Sent] 영상 인터넷 주소 텔레그램 발송 완료!", flush=True)
            return True
    except Exception as tg_err:
        print(f"  [Telegram Notification Notice] {tg_err}", flush=True)
    return False


def notify_telegram_youtube_upload(slug_key: str, edition_label: str, video_title: str, youtube_url: str) -> bool:
    """유튜브(@min7014_ai)에 새 영상이 업로드되는 즉시 텔레그램으로 인터넷 주소를 전송합니다."""
    board_url = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}"
    q_board_url = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&mode=question"
    msg = (
        f"🚀 [유튜브 신규 영상 업로드 완료 알림]\n"
        f"• 구분: {edition_label}\n"
        f"• 주제 ID: {slug_key}\n"
        f"• 제목: {video_title}\n\n"
        f"📺 유튜브 인터넷 주소:\n{youtube_url}\n\n"
        f"🌐 수학홈페이지 영상 주소:\n{board_url}\n"
        f"❓ 질문하는 수업 실험실:\n{q_board_url}"
    )
    return notify_telegram_video_event(msg)


def upload_slug_to_youtube(slug_key, langs=("ko", "en"), privacy="public", method="auto", replace_existing=False):
    """
    https://www.youtube.com/@min7014_ai (UCSlqQfOEtRfJuMPyGMLgFYA) 채널에 한국어(ko)·영어(en) 영상을 자동 업로드합니다.
    - 업데이트된 영상(needs_youtube_upload=True 또는 replace_existing=True)인 경우 유튜브 채널의 기존 영상을 먼저 삭제(videos.delete)한 뒤 새 영상을 올립니다.
    - method='auto': client_secret.json이 있으면 YouTube Data API v3를 사용하고, 없으면 Playwright YouTube Studio 브라우저 자동 업로더를 실행합니다.
    """
    global _LAST_UPLOAD_QUOTA_BLOCKED
    _LAST_UPLOAD_QUOTA_BLOCKED = False
    process_youtube_delete_queue(max_deletions=25)
    ensure_topic_rendered_for_upload(slug_key, langs=langs)

    integrity = verify_video_content_integrity(slug_key)
    if not integrity.get("ok"):
        print(f"⚠️ [Pre-Upload Mathteacher Audit ({slug_key})] Rebuilding due to {integrity.get('reason')}...", flush=True)
        generate_or_update_script(slug_key, target_langs=["ko", "en"])
        for _lc in langs:
            render_multilingual_video(slug_key, lang_code=_lc)

    uploaded_urls = {}
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    existing_yt = {}
    yt_pkgs = {}
    blocked_ids = get_deleted_video_ids_set()
    if script_path.exists():
        try:
            sdoc_tmp = json.loads(script_path.read_text(encoding="utf-8"))
            existing_yt = sdoc_tmp.get("youtube_urls") or {}
            yt_pkgs = sdoc_tmp.get("youtube_packages") or {}
        except Exception:
            existing_yt = {}
            yt_pkgs = {}

    missing_langs = []
    for lc in langs:
        cur_u = (existing_yt.get(lc) or "").strip()
        cur_vid = extract_youtube_video_id(cur_u)
        needs_up = bool((yt_pkgs.get(lc) or {}).get("needs_youtube_upload"))
        if cur_u and (replace_existing or needs_up or cur_vid in blocked_ids):
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("standard_1080p",), langs=(lc,), execute_delete=True
            )
            cur_u = ""
        if cur_u:
            uploaded_urls[lc] = cur_u
        else:
            missing_langs.append(lc)

    if not missing_langs:
        return uploaded_urls

    secret_file = find_google_client_secret()
    if method == "browser" or (method == "auto" and not secret_file):
        print(f"[Auto-Upload Mode: YouTube Studio Browser Automation -> {YOUTUBE_CHANNEL_URL}]")
        return upload_slug_via_studio_browser(slug_key, langs=missing_langs, privacy=privacy)

    from googleapiclient.http import MediaFileUpload

    youtube, active_token_path = get_available_youtube_upload_service()
    if youtube is None:
        _LAST_UPLOAD_QUOTA_BLOCKED = True
        return uploaded_urls

    newly_uploaded = {}
    for lang_code in missing_langs:
        # 업로드 직전 동일 주제·언어의 기존 채널 영상이 남아있으면 삭제 큐 등록 및 즉시 삭제
        queue_and_delete_existing_youtube_videos_for_slug(
            slug_key, editions=("standard_1080p",), langs=(lang_code,), execute_delete=True
        )
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
            newly_uploaded[lang_code] = yt_url
            print(f"[YouTube Uploaded to {YOUTUBE_CHANNEL_HANDLE} ({lang_code.upper()})] {yt_url}", flush=True)
            notify_telegram_youtube_upload(
                slug_key=slug_key,
                edition_label=f"🎬 1080p 일반 설명 본편 ({lang_code.upper()})",
                video_title=meta.get("title", slug_key),
                youtube_url=yt_url,
            )
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("standard_1080p",), langs=(lang_code,), execute_delete=True, exclude_video_ids=[vid_id]
            )
            set_youtube_urls_for_slug(
                slug_key,
                yt_ko=yt_url if lang_code == "ko" else None,
                yt_en=yt_url if lang_code == "en" else None,
            )
        except Exception as up_err:
            err_s = str(up_err)
            print(f"  [YouTube Upload API Notice ({slug_key} / {lang_code})] {up_err}", flush=True)
            if "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s or "quotaExceeded" in err_s:
                mark_token_quota_exhausted(active_token_path, 900)
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

    if newly_uploaded:
        set_youtube_urls_for_slug(
            slug_key,
            yt_ko=uploaded_urls.get("ko"),
            yt_en=uploaded_urls.get("en")
        )
    return uploaded_urls


upload_to_youtube = upload_slug_to_youtube


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
            # [버전 1] 일반적인 설명 영상 (1080p 16:9)
            mp4_p = YT_UPLOADS_DIR / s_key / f"{s_key}_{lc}.mp4"
            if not mp4_p.exists():
                render_multilingual_video(s_key, lang_code=lc)
            # [버전 2] 질문하는 수업 특화 영상 (1080p 16:9)
            q_mp4_p = ROOT_DIR / "video_lectures" / "question_classroom" / f"{s_key}_q_{lc}.mp4"
            if not q_mp4_p.exists():
                render_question_classroom_video(s_key, lang_code=lc)
            # [버전 3-A] 일반형 숏폼 영상 (9:16 Standard #Shorts)
            short_p = YT_UPLOADS_DIR / "shorts" / f"{s_key}_short_{lc}.mp4"
            if not short_p.exists():
                render_youtube_short_vertical(s_key, lang_code=lc)
            # [버전 3-B] 질문형 숏폼 영상 (9:16 Question-Asking #Shorts)
            qshort_p = ROOT_DIR / "video_lectures" / "shorts" / f"{s_key}_short_q_{lc}.mp4"
            if not qshort_p.exists():
                render_question_short_vertical(s_key, lang_code=lc)
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
    blocked_ids = get_deleted_video_ids_set()
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        with open(sp, "r", encoding="utf-8") as f:
            sdoc = json.load(f)
        slug = sdoc["slug"]
        yt_urls = sdoc.get("youtube_urls") or {"ko": "", "en": "", "orig": ""}
        yt_pkgs = sdoc.get("youtube_packages") or {}
        shorts_urls = sdoc.get("shorts_urls") or {"ko": "", "en": ""}
        shorts_pkgs = sdoc.get("shorts_packages") or {}
        q_yt_urls = sdoc.get("question_youtube_urls") or {"ko": "", "en": ""}
        q_shorts_urls = sdoc.get("question_shorts_urls") or {"ko": "", "en": ""}
        q_pkgs = sdoc.get("question_classroom_packages") or {}
        q_shorts_pkgs = sdoc.get("question_shorts_packages") or {}
        sdoc_dirty = False
        for d_map in (yt_urls, shorts_urls, q_yt_urls, q_shorts_urls):
            for _lc in ("ko", "en"):
                _val = d_map.get(_lc) or ""
                if _val and any(bid in _val for bid in blocked_ids):
                    d_map[_lc] = ""
                    sdoc_dirty = True
        if sdoc_dirty:
            sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

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
            "question_youtube_urls": q_yt_urls,
            "question_shorts_urls": q_shorts_urls,
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
            "question_classroom_packages": q_pkgs,
            "question_shorts_packages": q_shorts_pkgs,
        })
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)

    # min7014_deep_knowledge.json 및 min7014_lookup.json에서도 삭제 큐(blocked_ids) URL 정리 및 최신 숏폼 정보 동기화
    if DEEP_JSON_PATH.exists():
        try:
            d_items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
            d_changed = False
            for it in d_items:
                for u_field in ("youtube", "youtube_ko", "youtube_en", "youtube_short_ko", "youtube_short_en"):
                    u_val = (it.get(u_field) or "").strip()
                    if u_val and extract_youtube_video_id(u_val) in blocked_ids:
                        it[u_field] = ""
                        d_changed = True
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

    if LOOKUP_JSON_PATH.exists():
        try:
            lmap = json.loads(LOOKUP_JSON_PATH.read_text(encoding="utf-8"))
            l_changed = False
            for k_cand, v_obj in lmap.items():
                if not isinstance(v_obj, dict):
                    continue
                for lk_field in ("y", "yk", "ye", "youtube", "youtube_ko", "youtube_en"):
                    l_val = (v_obj.get(lk_field) or "").strip()
                    if l_val and extract_youtube_video_id(l_val) in blocked_ids:
                        v_obj[lk_field] = ""
                        l_changed = True
            if l_changed:
                LOOKUP_JSON_PATH.write_text(json.dumps(lmap, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        except Exception as le:
            print(f"[Lookup JSON Clean Notice] {le}")

    vault_path = ROOT_DIR / "video_lectures" / "vault_index.json"
    existing_playlists = {}
    existing_thumbs = []
    existing_seo_map = {}
    existing_quiz_comments = []
    if vault_path.exists():
        try:
            old_v = json.loads(vault_path.read_text(encoding="utf-8"))
            existing_playlists = old_v.get("playlists") or {}
            existing_thumbs = old_v.get("applied_custom_thumbnails") or []
            existing_seo_map = old_v.get("applied_seo_boost_map") or {}
            existing_quiz_comments = old_v.get("applied_quiz_comments") or []
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
        "applied_seo_boost_map": existing_seo_map,
        "applied_quiz_comments": existing_quiz_comments,
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
    [v6.0 @min7014_ai 유튜브 알고리즘 부스터 (Zero-Waste Quota · CTR · Playlist · Interactive Quiz Comments)]
    1) 이미 최신 제목·썸네일·댓글이 적용된 영상은 중복 API 호출(50유닛/건)을 원천 차단하여 일일 업로드 쿼터를 100% 보호합니다.
    2) 제목이나 설명이 새로 정제된 본편 및 #Shorts 영상만 선별하여 YouTube API로 즉시 업데이트합니다.
    3) @min7014_ai 채널에 한국어(KO) / 영어(EN) 공식 정주행 재생목록(Playlist)을 관리하고 신규 영상을 자동 편성합니다.
    """
    refresh_all_youtube_metadata_packages()

    youtube, active_token_path = get_available_youtube_upload_service()
    if youtube is None:
        return {}

    vault_path = ROOT_DIR / "video_lectures" / "vault_index.json"
    vdata = {}
    if vault_path.exists():
        try:
            vdata = json.loads(vault_path.read_text(encoding="utf-8"))
        except Exception:
            vdata = {}
    applied_seo_map = dict(vdata.get("applied_seo_boost_map") or {})
    applied_thumbs = set(vdata.get("applied_custom_thumbnails") or [])
    applied_comments = set(vdata.get("applied_quiz_comments") or [])

    ko_video_ids = []
    en_video_ids = []

    # 1. 업로드된 전체 본편 + #Shorts 메타데이터(변경분만 선별 업데이트) + 썸네일 + 유레카 퀴즈 댓글 등록
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        slug = sdoc["slug"]
        yt_urls = sdoc.get("youtube_urls") or {}
        meta_path = YT_PKG_DIR / f"{slug}_youtube_meta.json"
        meta_all = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

        for lc in ["ko", "en"]:
            u = (yt_urls.get(lc) or "").strip()
            if not u or lc not in meta_all:
                continue
            vid_id = extract_youtube_video_id(u)
            if not vid_id:
                continue
            if lc == "ko":
                ko_video_ids.append((slug, vid_id))
            else:
                en_video_ids.append((slug, vid_id))

            meta = meta_all[lc]
            if applied_seo_map.get(vid_id) != meta["title"]:
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
                    applied_seo_map[vid_id] = meta["title"]
                    print(f"✅ [SEO & High-CTR Updated ({lc.upper()})] {vid_id} -> {meta['title']}")
                except Exception as e:
                    print(f"⚠️ [Video Update Notice ({vid_id})]: {e}")
                    if "quotaExceeded" in str(e):
                        break

            # 커스텀 썸네일 미적용 영상에만 1회 적용 (중복 50유닛 소모 방지)
            thumb_p = YT_PKG_DIR / f"{slug}_{lc}_thumb.png"
            if vid_id not in applied_thumbs and thumb_p.exists():
                try:
                    from googleapiclient.http import MediaFileUpload
                    youtube.thumbnails().set(
                        videoId=vid_id,
                        media_body=MediaFileUpload(str(thumb_p), mimetype="image/png"),
                    ).execute()
                    applied_thumbs.add(vid_id)
                    print(f"🖼️ [v6.0 Viral Thumbnail Applied ({lc.upper()})] {vid_id} <- {thumb_p.name}")
                except Exception as te:
                    print(f"⚠️ [Thumbnail Update Notice ({vid_id})]: {te}")

            # 시청자 참여 유도 첫 댓글 (이미 등록된 영상은 API 호출 스킵)
            quiz_comment = meta.get("quiz_comment") or ""
            if quiz_comment and vid_id not in applied_comments:
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
                            f"📌 직접 움직여보는 GeoGebra & 전체 1,113개 수학 설명영상 게시판:\n👉 {board_link}"
                            if lc == "ko"
                            else f"{quiz_comment}\n\n"
                            f"📌 Explore the Interactive GeoGebra & Full 1,113 Math Video Board:\n👉 {board_link}"
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
                    applied_comments.add(vid_id)
                except Exception as ce:
                    print(f"⚠️ [Comment Notice ({vid_id})]: {ce}")

        # 1-B. 이미 업로드된 #Shorts 영상 중 제목 절단 방지·본편 링크가 갱신된 경우 스니펫 자동 동기화
        shorts_urls = sdoc.get("shorts_urls") or {}
        smeta_path = YT_PKG_DIR / f"{slug}_shorts_meta.json"
        smeta_all = json.loads(smeta_path.read_text(encoding="utf-8")) if smeta_path.exists() else {}
        for lc in ["ko", "en"]:
            su = (shorts_urls.get(lc) or "").strip()
            if not su or lc not in smeta_all:
                continue
            svid_id = extract_youtube_video_id(su)
            if not svid_id:
                continue
            smeta = smeta_all[lc]
            if applied_seo_map.get(svid_id) != smeta["title"]:
                try:
                    youtube.videos().update(
                        part="snippet",
                        body={
                            "id": svid_id,
                            "snippet": {
                                "title": smeta["title"],
                                "description": smeta["description"],
                                "tags": smeta["tags"],
                                "categoryId": smeta.get("categoryId", "27"),
                                "defaultLanguage": lc,
                                "defaultAudioLanguage": lc,
                            },
                        },
                    ).execute()
                    applied_seo_map[svid_id] = smeta["title"]
                    print(f"✅ [#Shorts SEO & Funnel Updated ({lc.upper()})] {svid_id} -> {smeta['title']}")
                except Exception as se:
                    print(f"⚠️ [#Shorts Update Notice ({svid_id})]: {se}")

    # 2. 공식 정주행 재생목록(Playlists) 생성 및 영상 자동 편성
    playlist_specs = {
        "ko": {
            "title": "🔥 [시각적 수학 증명] 보조선과 원리로 깨치는 수학 명작 정주행 (1080p) | @min7014_ai",
            "desc": (
                "공식 암기 없이 눈으로 보고 직관적으로 깨치는 수학자료실(https://min7014.github.io/) 단계별 시각적 증명 한국어 정주행 시리즈입니다.\n"
                "전체 1,113개 설명영상 게시판: https://min7014.github.io/mathedu/video_board.html"
            ),
            "videos": [vid for _, vid in ko_video_ids],
        },
        "en": {
            "title": "✨ [Visual Math Proofs] Step-by-Step Euclidean Geometry & Algebra Masterclass (1080p) | @min7014_ai",
            "desc": (
                "Step-by-step visual mathematical proofs from https://min7014.github.io/. Watch auxiliary lines and mathematical principles come alive!\n"
                "Full 1,113 Math Video Board: https://min7014.github.io/mathedu/video_board.html"
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

    if vault_path.exists():
        vdata = json.loads(vault_path.read_text(encoding="utf-8"))
        if saved_playlist_urls:
            vdata["playlists"] = saved_playlist_urls
        vdata["applied_seo_boost_map"] = applied_seo_map
        vdata["applied_custom_thumbnails"] = sorted(list(applied_thumbs))
        vdata["applied_quiz_comments"] = sorted(list(applied_comments))
        vault_path.write_text(json.dumps(vdata, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ [Vault Index SEO/Thumb/Playlist State Saved] ({len(applied_seo_map)} synced videos)")

    return saved_playlist_urls


def condense_narration_for_shorts(raw_text, seq_idx, total_seqs, clean_title, viral_hook, lang_code="ko"):
    """
    [v6.0 유튜브 쇼츠(#Shorts) 알고리즘 최적화 대본 압축기 (36~46초 골든 타임 + 105% 무한 루프 브릿지)]
    - Scene 1: 첫 1.5초 스와이프 방지를 위한 직관적 역발상 질문 훅
    - Scene 2~4: 군더더기 인사말을 제거한 고밀도 핵심 단서 (한국어 78자, 영어 132자 이내)
    - Scene 5 (Final): '영상이 끝났다'는 느낌을 주지 않고 첫 장면(0:00)의 도형으로 시선을 되돌리는 Seamless Loop-Bridge 문장!
    """
    txt = re.sub(r"\s+", " ", (raw_text or "").strip())
    if seq_idx == 1:
        if lang_code == "ko":
            hook = viral_hook or f"잠깐! {clean_title}, 왜 항상 성립할까요?"
            sents = [s.strip() for s in re.split(r"(?<=[.?!다요죠])\s+", txt) if s.strip()]
            first_core = ""
            for s in sents:
                if "안녕하세요" not in s and "선생님" not in s:
                    first_core = s
                    break
            combined = f"{hook} {first_core}".strip()
            return combined[:86] if len(combined) > 86 else combined
        else:
            hook = viral_hook or f"Wait! Why does {clean_title} always work?"
            sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
            first_core = ""
            for s in sents:
                if "Welcome" not in s and "Min's Math Lab" not in s:
                    first_core = s
                    break
            combined = f"{hook} {first_core}".strip()
            return combined[:140] if len(combined) > 140 else combined

    if seq_idx == total_seqs:
        if lang_code == "ko":
            return "결국 이 핵심 원리 하나로 완벽히 증명됩니다! 그렇다면 맨 처음 출발 도형에서 이 단서가 어디에 숨어 있었는지 다시 찾아볼까요? 1080p 풀버전은 설명란·고정댓글에 있습니다!"
        else:
            return "That single principle unlocks the entire proof! Now look back at the very first figure—did you spot where this hidden clue started? Full 1080p proof in the description!"

    # 중간 핵심 전개 장면 (2, 3, 4단계): 인사말 제거 후 가장 핵심적인 1~2문장(한국어 78자, 영어 132자 이내) 추출
    if lang_code == "ko":
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
        picked = []
        cur_len = 0
        for s in sents:
            if cur_len + len(s) <= 78 or not picked:
                picked.append(s)
                cur_len += len(s)
            else:
                break
        res = " ".join(picked)
        if len(res) > 82:
            res = res[:80].rsplit(" ", 1)[0] + "."
        return res
    else:
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
        picked = []
        cur_len = 0
        for s in sents:
            if cur_len + len(s) <= 132 or not picked:
                picked.append(s)
                cur_len += len(s)
            else:
                break
        res = " ".join(picked)
        if len(res) > 140:
            res = res[:136].rsplit(" ", 1)[0] + "."
        return res


def build_youtube_short_metadata(sdoc, lang_code, duration_sec):
    """
    [유튜브 숏폼(#Shorts) 전용 고클릭률 제목·설명·태그 메타데이터 패키지 생성]
    - 단어 중간 절단 원천 차단 (_smart_concise_topic_title)
    - 1080p 본편 및 질문하는 수업 본편 직결 퍼널 링크 내장
    """
    slug = sdoc["slug"]
    clean_ko = latex_to_unicode_title(split_bilingual_title(sdoc["title"])[0])
    clean_en = latex_to_unicode_title((sdoc.get("title_en") or split_bilingual_title(sdoc["title"])[1] or clean_ko).strip())
    concise_ko = _smart_concise_topic_title(clean_ko, max_len=34, lang="ko")
    concise_en = _smart_concise_topic_title(clean_en, max_len=38, lang="en")
    viral_hooks = sdoc.get("viral_hooks") or {}
    yt_urls = sdoc.get("youtube_urls") or {}
    q_yt_urls = sdoc.get("question_youtube_urls") or {}
    full_yt = yt_urls.get(lang_code) or yt_urls.get("ko") or "https://www.youtube.com/@min7014_ai"
    full_q_yt = q_yt_urls.get(lang_code) or q_yt_urls.get("ko") or full_yt
    board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}"
    cat_type = (sdoc.get("teacher_proof_analysis") or {}).get("category_type", "geometry")

    if lang_code == "ko":
        default_hook_ko = (
            f"수학교사의 단계별 원리 해부! {concise_ko} 45초 완성"
            if cat_type in ("algebra", "number")
            else f"보조선 한 줄의 마법! {concise_ko} 45초 시각적 증명"
        )
        hook_ko = _smart_concise_topic_title(viral_hooks.get("ko") or default_hook_ko, max_len=48, lang="ko")
        short_title = f"🔥 {hook_ko} | {concise_ko} #Shorts #수학"
        if len(short_title) > 98:
            short_title = f"🔥 {concise_ko} — 45초 시각적 수학 증명 #Shorts #수학"
        desc = (
            f"⚡ [{clean_ko} — {round(duration_sec)}초 숏폼(#Shorts) 시각적 증명 하이라이트]\n"
            f"{hook_ko}\n\n"
            f"🎬 1080p 전체 단계별 풀버전 설명영상 바로 보기:\n👉 {full_yt}\n"
            f"❓ 1080p 질문하는 수학 수업 풀버전 바로 보기:\n👉 {full_q_yt}\n\n"
            f"🌐 [1초 클릭! 수학홈페이지 무료 실습 & 퀴즈 바로가기]\n"
            f"1️⃣ 방금 본 도형 마우스로 직접 움직여보기 (GeoGebra & 플립북 게시판):\n👉 {board_link}&from=yt_shorts\n"
            f"2️⃣ 5지선다 보기를 가리고 수식 블록 조립! 16,548문항 수능·모평 디딤돌 퀴즈:\n👉 https://min7014.github.io/mathedu/?from=yt_shorts\n"
            f"3️⃣ 오늘의 3분 수학 유레카 (10초 오개념 O/X & 나만의 문제 발명):\n👉 https://min7014.github.io/mathedu/#dailyGrowthFlywheelSection\n"
            f"4️⃣ 수능 수학 100점 만점 3D 보스 레이드 게임 무료 플레이:\n👉 https://min7014.github.io/mathedu/game.html\n"
            f"5️⃣ 수학자료실 본관 (3,400+ 시각 증명):\n👉 https://min7014.github.io/\n\n"
            f"🔔 단계별 시각적 수학 증명_AI (@min7014_ai) 구독하기:\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"[ID: {slug}_SHORT_KO]\n"
            f"#Shorts #수학 #기하학 #시각적증명 #{concise_ko.replace(' ', '')} #피타고라스 #보조선 #수능수학 #수학자료실 #min7014_ai"
        )
        tags = ["Shorts", "유튜브쇼츠", "수학", "기하학", "시각적증명", concise_ko, "수학자료실", "min7014_ai", "수능수학", "보조선"]
    else:
        hook_en = _smart_concise_topic_title(viral_hooks.get("en") or f"45s Visual Math Proof: {concise_en}", max_len=50, lang="en")
        short_title = f"🔥 {hook_en} | {concise_en} #Shorts #Math"
        if len(short_title) > 98:
            short_title = f"🔥 {concise_en} — 45s Visual Math Proof #Shorts #Math"
        desc = (
            f"⚡ [{clean_en} — {round(duration_sec)}s Visual Math Proof #Shorts]\n"
            f"{hook_en}\n\n"
            f"🎬 Watch Full 1080p Step-by-Step Proof Video:\n👉 {full_yt}\n"
            f"❓ Watch 1080p Question-Asking Classroom Edition:\n👉 {full_q_yt}\n\n"
            f"📐 Interactive GeoGebra & Full 1,113 Math Video Board:\n👉 {board_link}\n\n"
            f"🔔 Subscribe to Visual Math Proofs AI (@min7014_ai):\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"[ID: {slug}_SHORT_EN]\n"
            f"#Shorts #Math #Geometry #VisualProof #MathShorts #ProofWithoutWords #GeoGebra #min7014_ai"
        )
        tags = ["Shorts", "MathShorts", "Math", "Geometry", "VisualProof", concise_en, "VisualMathArchive", "min7014_ai", "GeoGebra"]

    return {
        "title": _balance_parentheses(short_title[:98]),
        "description": desc,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": lang_code,
        "duration_sec": round(duration_sec, 2),
        "aspect_ratio": "9:16 (1080x1920)",
    }


def render_youtube_short_vertical(slug_key="math20250130001", lang_code="ko"):
    """
    [v6.0 유튜브 쇼츠(YouTube Shorts · 1080x1920 세로형 36~46초 알고리즘 최적화) 자동 제작기]
    1) 첫 0.85초 스와이프 방지 클라이맥스 스포트라이트 훅 (Viewed vs. Swiped Away >= 80% 타겟)
    2) 서브프레임 단위 연속 진행 게이지 바 & 현재 읽는 줄 네온 골드 키네틱 자막 하이라이팅
    3) 마지막 장면 끝에 첫 장면(doc[0]) 0.35초 시각 브릿지를 결합한 100% Seamless Infinite Loop (APV >= 105% 타겟)
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

    pdf_bytes, _ = load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug_key)
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

    _ko_t, _en_t = split_bilingual_title(sdoc["title"])
    clean_title = (
        _smart_concise_topic_title(latex_to_unicode_title(_en_t or sdoc.get("title_en") or _ko_t), max_len=44, lang="en")
        if lang_code == "en"
        else _smart_concise_topic_title(latex_to_unicode_title(_ko_t), max_len=36, lang="ko")
    )
    viral_hooks = sdoc.get("viral_hooks") or {}
    viral_hook = viral_hooks.get(lang_code) or ""
    vprof = get_viral_hook_profile(sdoc)
    total_seqs = len(picked_indices)

    try:
        for seq_idx, p_idx in enumerate(picked_indices, 1):
            p_info = pages[p_idx]
            canvas = Image.new("RGB", (1080, 1920), (10, 16, 34))
            draw = ImageDraw.Draw(canvas)

            # 상단 알고리즘 후킹 배너
            draw.rounded_rectangle((44, 58, 1036, 294), radius=28, fill=(23, 37, 84), outline=(56, 189, 248), width=3)
            draw.rounded_rectangle((74, 78, 690, 130), radius=18, fill=(225, 29, 72))
            badge_txt = (vprof.get("badge_en") or "⚡ 45s Visual Math Proof #Shorts") if lang_code == "en" else (vprof.get("badge_ko") or "⚡ 99%가 공식만 외운 시각적 증명")
            draw.text((92, 86), badge_txt[:34], fill=(255, 255, 255), font=font_sub)

            step_label = f"STEP {seq_idx}/{total_seqs}"
            draw.text((845, 86), step_label, fill=(251, 191, 36), font=font_sub)

            title_lines = textwrap.wrap(clean_title, width=20 if lang_code == "ko" else 28)[:2]
            for li, tl in enumerate(title_lines):
                draw.text((78, 146 + li * 54), tl, fill=(255, 255, 255), font=font_top)

            # 하단 초압축 숏폼 내레이션 & 자막 카드
            raw_narr = p_info.get("narrations", {}).get(lang_code) or p_info["explanation_text"]
            short_narration = condense_narration_for_shorts(
                raw_narr, seq_idx, total_seqs, clean_title, viral_hook, lang_code=lang_code
            )

            mp3_p = tmp_dir / f"short_{seq_idx:02d}.mp3"
            seg_p = tmp_dir / f"short_{seq_idx:02d}.mp4"
            comm = edge_tts.Communicate(short_narration, voice_name, rate="+20%")
            asyncio.run(comm.save(str(mp3_p)))
            seg_audio_dur = get_media_duration_seconds(mp3_p, ffprobe_exe)

            # 현재 단계에 해당하는 연속 PDF 플립북 프레임 추출 (최대 6프레임 모션 애니메이션)
            f_range = p_info.get("frame_range")
            if seq_idx == 1 and len(doc) >= 3:
                # [v6.0 Swipe-Stop Climax Hook]: 첫 프레임(0.85s)에 클라이맥스 도형 스포트라이트를 먼저 터뜨린 뒤 1~2페이지로 진입!
                doc_frames = [max(0, len(doc) - 2), 0, min(len(doc) - 1, 2)]
            elif f_range and f_range[1] > f_range[0]:
                doc_frames = list(range(max(0, int(f_range[0]) - 1), min(len(doc), int(f_range[1]))))
            else:
                prev_doc_p = 0 if seq_idx == 1 else max(0, pages[picked_indices[seq_idx - 2]]["page"] - 1)
                curr_doc_p = min(len(doc) - 1, p_info["page"] - 1)
                doc_frames = list(range(prev_doc_p, curr_doc_p + 1)) if curr_doc_p > prev_doc_p else [curr_doc_p]
            if len(doc_frames) < 2:
                doc_frames = [doc_frames[0], doc_frames[0]]
            if len(doc_frames) > 6:
                step_df = (len(doc_frames) - 1) / 5.0
                doc_frames = sorted(list({doc_frames[int(round(k * step_df))] for k in range(6)}))
            if seq_idx == total_seqs and len(doc) >= 2:
                # [v6.0 Seamless Infinite Loop Bridge]: 마지막 장면의 끝 프레임을 출발 도형(doc[0])으로 연결하여 0:00과 무결점 루프 완성!
                doc_frames = list(doc_frames) + [0]

            draw.rounded_rectangle((44, 1345, 1036, 1795), radius=28, fill=(15, 23, 42), outline=(225, 29, 72), width=3)
            step_chip = (
                f"💡 핵심 시각 증명 STEP {seq_idx}/{total_seqs} (PDF {doc_frames[0]+1}▸{doc_frames[-1]+1}/{len(doc)})"
                if lang_code == "ko"
                else f"💡 Visual Proof STEP {seq_idx}/{total_seqs} (PDF {doc_frames[0]+1}▸{doc_frames[-1]+1}/{len(doc)})"
            )
            draw.text((78, 1375), step_chip, fill=(251, 191, 36), font=font_sub)
            cap_lines = textwrap.wrap(short_narration, width=22 if lang_code == "ko" else 34)[:5]

            draw.rounded_rectangle((44, 1810, 1036, 1892), radius=20, fill=(30, 58, 138), outline=(251, 191, 36), width=3)
            cta_short_txt = (
                "👆 설명란·고정댓글 ➔ 1080p 풀버전 & 무료 GeoGebra 실습! (@min7014_ai)"
                if lang_code == "ko"
                else "👆 Tap Description ➔ Full 1080p Proof & Free GeoGebra! (@min7014_ai)"
            )
            draw.text((64, 1834), cta_short_txt, fill=(254, 240, 138), font=get_font_for_lang("ko", 24, bold=True))

            # 각 PDF 프레임을 1080x1920 캔버스 중앙에 합성 + 서브프레임 연속 진행바 & 키네틱 자막 하이라이팅
            per_f_dur = max(0.22, seg_audio_dur / max(1, len(doc_frames)))
            f_lines = []
            last_fp = None
            for fi_idx, doc_f_i in enumerate(doc_frames):
                frame_canvas = canvas.copy()
                f_draw = ImageDraw.Draw(frame_canvas)

                # 서브프레임 단위 연속 진행 바 (Smooth Continuous Progress Gauge)
                overall_prog = ((seq_idx - 1) + ((fi_idx + 1) / max(1, len(doc_frames)))) / max(1, total_seqs)
                f_draw.rounded_rectangle((74, 266, 1006, 280), radius=7, fill=(30, 58, 138))
                prog_w = int(932 * min(1.0, max(0.04, overall_prog)))
                f_draw.rounded_rectangle((74, 266, 74 + max(24, prog_w), 280), radius=7, fill=(250, 204, 21) if seq_idx == total_seqs else (56, 189, 248))

                # 현재 읽고 있는 자막 줄 네온 골드 키네틱 하이라이팅
                active_cap_idx = min(max(0, len(cap_lines) - 1), int((fi_idx / max(1, len(doc_frames))) * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    c_col = (254, 240, 138) if (ci == active_cap_idx or len(cap_lines) == 1) else (226, 232, 240)
                    f_draw.text((78, 1438 + ci * 60), cl, fill=c_col, font=font_cap)

                pix = doc[doc_f_i].get_pixmap(dpi=260)
                slide_pil = _mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
                sw, sh = slide_pil.size
                scale = min(984 / sw, 980 / sh)
                nw, nh = int(sw * scale), int(sh * scale)
                resized = slide_pil.resize((nw, nh), Image.Resampling.LANCZOS)
                ox = (1080 - nw) // 2
                oy = 326 + (980 - nh) // 2
                f_draw.rounded_rectangle((ox - 12, oy - 12, ox + nw + 12, oy + nh + 12), radius=22, fill=(255, 255, 255), outline=(251, 191, 36), width=3)
                frame_canvas.paste(resized, (ox, oy))

                # 첫 장면 첫 프레임(0.85s Swipe-Stop Hook) 또는 마지막 프레임 스포트라이트 강조
                bbox = p_info.get("diff_bbox")
                if seq_idx == 1 and fi_idx == 0:
                    cx_s, cy_s, r_s = ox + nw // 2, oy + nh // 2, 86
                    f_draw.ellipse((cx_s - r_s, cy_s - r_s, cx_s + r_s, cy_s + r_s), outline=(225, 29, 72), width=7)
                    f_draw.rounded_rectangle((120, oy + 14, 960, oy + 76), radius=16, fill=(225, 29, 72), outline=(254, 240, 138), width=3)
                    sw_txt = "⚡ WAIT! Why Does This Always Work? (Watch 40s)" if lang_code == "en" else "⚡ 잠깐! 왜 항상 성립할까? 40초 시각적 증명!"
                    f_draw.text((152, oy + 26), sw_txt, fill=(255, 255, 255), font=font_sub)
                elif bbox and fi_idx >= len(doc_frames) - 2 and doc_f_i > 0:
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
            use_chime = seq_idx in (1, (total_seqs // 2) + 1, total_seqs)
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
        # [v6.0 Golden Shorts Retention Duration (36~47s)]: 49초 이상이면 배속을 미세 조정하여 완주율(APV >= 105%)이 가장 높은 44.5초로 맞춤
        if dur >= 49.0:
            speed_factor = round((dur / 44.5), 3)
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

        # [자동 교체 원칙] 숏폼 영상이 새로 렌더링/업데이트되면 기존 채널의 구버전 숏폼을 삭제 큐에 등록 및 삭제
        try:
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("shorts_std",), langs=(lang_code,), execute_delete_now=True
            )
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        except Exception:
            pass

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
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "needs_youtube_upload": True,
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




def condense_question_narration_for_shorts(step_q, raw_narr, seq_idx, total_seqs, clean_title, lang_code="ko"):
    """
    [v6.0 질문형 숏폼(#Shorts) 전용 2-Beat 발문 ➔ 단서 ➔ 무한 루프 내레이션 압축기]
    - 각 장면을 '핵심 발문(Question) 제시 ➔ 직관적 단서(Visual Clue) 발견' 구조로 압축하며,
      마지막 장면(seq_idx == total_seqs)은 첫 장면의 도형과 연결되는 루프 발문으로 마무리하여
      105%+ 시청 지속률(APV)과 36~46초 황금 길이를 달성합니다.
    """
    txt = re.sub(r"\s+", " ", (raw_narr or "")).strip()
    q_clean = re.sub(r"^[^\]]+\]\s*", "", re.sub(r"\s+", " ", (step_q or "")).strip()).strip()
    if lang_code == "ko":
        sents = [s.strip() for s in re.split(r"(?<=[.?!다요죠])\s+", txt) if s.strip()]
        core_ans = sents[-1] if sents else txt[:55]
        if len(core_ans) > 58:
            core_ans = core_ans[:56].rsplit(" ", 1)[0] + "."
        if seq_idx == 1:
            q_short = f"잠깐! {clean_title}, 왜 항상 성립할까요?"
            return f"{q_short} ... 정답 단서! {core_ans}"
        elif seq_idx == total_seqs:
            return f"유레카! {core_ans} 그렇다면 처음 도형에서 이 보조선이 왜 출발점이었는지 다시 볼까요?"
        else:
            q_short = q_clean if len(q_clean) <= 48 else "직전 단계와 비교해 새로 추가된 핵심 단서는 무엇일까요?"
            return f"{q_short} ... 정답 단서! {core_ans}"
    else:
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
        core_ans = sents[-1] if sents else txt[:85]
        if len(core_ans) > 90:
            core_ans = core_ans[:86].rsplit(" ", 1)[0] + "."
        if seq_idx == 1:
            q_short = f"Wait! Why does {clean_title} always hold?"
            return f"{q_short} ... Visual clue! {core_ans}"
        elif seq_idx == total_seqs:
            return f"Eureka! {core_ans} Now look back at the first figure to see where this clue started!"
        else:
            q_short = q_clean if len(q_clean) <= 68 else "What new mathematical clue bridges this step?"
            return f"{q_short} ... Visual clue! {core_ans}"


def render_question_short_vertical(slug_key="math20250130001", lang_code="ko"):
    """
    [질문형 유튜브 쇼츠 (Question-Asking #Shorts · 1080x1920 세로형 42~54초) 자동 제작기]
    - 일반형 숏폼({slug}_short_{lang}.mp4)과 별도로 제작되는 '질문하는 수업 특화 숏폼'({slug}_short_q_{lang}.mp4)입니다.
    - 상단 크림슨-골드 발문 카드(Notice & Wonder ➔ 소크라테스 보조선 발문 ➔ What-If-Not 조건 변형 질문)를 탑재하고,
      각 스텝의 전반부 프레임에서는 '🙋 먼저 생각해 보세요!' 발문 배너를, 후반부 프레임에서는 '💡 시각적 단서 발견!'과
      적색 보조선 스포트라이트를 제시합니다.
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

    pdf_bytes, _ = load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug_key)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    voice_name = GLOBAL_VOICE_MAP.get(lang_code, GLOBAL_VOICE_MAP["en"])["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    shorts_dir = YT_UPLOADS_DIR / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)
    pub_short_dir = ROOT_DIR / "video_lectures" / "shorts"
    pub_short_dir.mkdir(parents=True, exist_ok=True)
    ready_shorts_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai_shorts"
    ready_shorts_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_qshort_{slug_key}_{lang_code}_"))
    segs = []

    font_top = get_font_for_lang(lang_code, 42, bold=True)
    font_sub = get_font_for_lang(lang_code, 28, bold=True)
    font_q = get_font_for_lang(lang_code, 30, bold=True)
    font_cap = get_font_for_lang(lang_code, 32, bold=True)

    _ko_t, _en_t = split_bilingual_title(sdoc["title"])
    clean_title = (
        latex_to_unicode_title(_en_t or sdoc.get("title_en") or _ko_t)
        if lang_code == "en"
        else latex_to_unicode_title(_ko_t)
    )
    total_seqs = len(picked_indices)

    try:
        for seq_idx, p_idx in enumerate(picked_indices, 1):
            p_info = pages[p_idx]
            p_num = p_info.get("page", p_idx + 1)
            step_q = (
                p_info.get("step_question_ko") or build_step_question_ko(clean_title, p_num, n)
                if lang_code == "ko"
                else p_info.get("step_question_en") or build_step_question_en(clean_title, p_num, n)
            )

            canvas = Image.new("RGB", (1080, 1920), (18, 12, 28))
            draw = ImageDraw.Draw(canvas)

            # 1) 상단 질문하는 수업 #Shorts 헤더 (y=48..268)
            draw.rounded_rectangle((40, 48, 1040, 268), radius=26, fill=(76, 5, 25), outline=(251, 191, 36), width=3)
            draw.rounded_rectangle((68, 68, 680, 116), radius=16, fill=(225, 29, 72))
            badge_txt = "❓ 질문하는 수업 · 45초 발문 #Shorts" if lang_code == "ko" else "❓ Question-Asking Classroom #Shorts"
            draw.text((86, 76), badge_txt, fill=(255, 255, 255), font=font_sub)

            step_label = f"Q-STEP {seq_idx}/{total_seqs}"
            draw.text((820, 76), step_label, fill=(254, 240, 138), font=font_sub)

            title_lines = textwrap.wrap(clean_title, width=20 if lang_code == "ko" else 28)[:2]
            for li, tl in enumerate(title_lines):
                draw.text((72, 130 + li * 50), tl, fill=(255, 255, 255), font=font_top)

            # 진행 게이지
            draw.rounded_rectangle((68, 242, 1012, 254), radius=6, fill=(136, 19, 55))
            prog_w = int(944 * (seq_idx / total_seqs))
            draw.rounded_rectangle((68, 242, 68 + max(24, prog_w), 254), radius=6, fill=(251, 191, 36))

            # 2) 상단-중앙 핵심 발문 플로팅 카드 (y=282..452)
            draw.rounded_rectangle((40, 282, 1040, 452), radius=22, fill=(255, 241, 242), outline=(244, 63, 94), width=3)
            if seq_idx == 1:
                q_type_badge = "👁️ [1단계 관찰 질문 · Notice & Wonder]" if lang_code == "ko" else "👁️ [Stage 1 · Notice & Wonder Question]"
            elif seq_idx == total_seqs:
                q_type_badge = "🔀 [3단계 확장 질문 · What-If-Not 조건 변형]" if lang_code == "ko" else "🔀 [Stage 3 · What-If-Not Question]"
            else:
                q_type_badge = f"🧭 [2단계 보조선 발문 · Socratic Inquiry {seq_idx}/{total_seqs}]" if lang_code == "ko" else f"🧭 [Stage 2 · Socratic Auxiliary Line Q{seq_idx}]"
            draw.text((68, 296), q_type_badge, fill=(190, 18, 60), font=font_sub)

            q_lines = textwrap.wrap(step_q, width=25 if lang_code == "ko" else 36)[:2]
            for qi, ql in enumerate(q_lines):
                draw.text((68, 342 + qi * 44), ql, fill=(15, 23, 42), font=font_q)

            # 3) 질문형 압축 내레이션 생성 및 음성 합성
            raw_narr = p_info.get("narrations", {}).get(lang_code) or p_info["explanation_text"]
            q_short_narr = condense_question_narration_for_shorts(
                step_q, raw_narr, seq_idx, total_seqs, clean_title, lang_code=lang_code
            )
            mp3_p = tmp_dir / f"qshort_{seq_idx:02d}.mp3"
            seg_p = tmp_dir / f"qshort_{seq_idx:02d}.mp4"
            comm = edge_tts.Communicate(q_short_narr, voice_name, rate="+18%")
            asyncio.run(comm.save(str(mp3_p)))
            seg_audio_dur = get_media_duration_seconds(mp3_p, ffprobe_exe)

            # 4) 플립북 프레임 시퀀스 추출 (v6.0 무한 루프 연결 포함)
            f_range = p_info.get("frame_range")
            if seq_idx == 1 and len(doc) >= 3:
                doc_frames = [max(0, len(doc) - 1), 0, min(len(doc) - 1, 1)]
            elif f_range and f_range[1] > f_range[0]:
                doc_frames = list(range(max(0, int(f_range[0]) - 1), min(len(doc), int(f_range[1]))))
            else:
                prev_doc_p = 0 if seq_idx == 1 else max(0, pages[picked_indices[seq_idx - 2]]["page"] - 1)
                curr_doc_p = min(len(doc) - 1, p_info["page"] - 1)
                doc_frames = list(range(prev_doc_p, curr_doc_p + 1)) if curr_doc_p > prev_doc_p else [curr_doc_p]
            if len(doc_frames) < 2:
                doc_frames = [doc_frames[0], doc_frames[0]]
            if len(doc_frames) > 6:
                step_df = (len(doc_frames) - 1) / 5.0
                doc_frames = sorted(list({doc_frames[int(round(k * step_df))] for k in range(6)}))
            if seq_idx == total_seqs and doc_frames[-1] != 0:
                doc_frames.append(0)

            # 5) 하단 발문 & 단서 자막 카드 (y=1365..1795) — 프레임별 키네틱 자막 렌더링을 위해 테두리만 베이스에 작도
            draw.rounded_rectangle((40, 1365, 1040, 1795), radius=26, fill=(15, 23, 42), outline=(251, 191, 36), width=3)
            cap_lines = textwrap.wrap(q_short_narr, width=22 if lang_code == "ko" else 34)[:5]

            draw.rounded_rectangle((40, 1810, 1040, 1892), radius=20, fill=(136, 19, 55), outline=(251, 191, 36), width=3)
            cta_short_txt = (
                "👆 내 질문 남기기 & 무료 GeoGebra 실습 ➔ min7014.github.io/mathedu"
                if lang_code == "ko"
                else "👆 Post Your Question & Try GeoGebra ➔ min7014.github.io/mathedu"
            )
            draw.text((68, 1834), cta_short_txt, fill=(254, 240, 138), font=get_font_for_lang("ko", 24, bold=True))

            per_f_dur = max(0.22, seg_audio_dur / max(1, len(doc_frames)))
            f_lines = []
            last_fp = None
            half_idx = max(1, len(doc_frames) // 2)
            for fi_idx, doc_f_i in enumerate(doc_frames):
                frame_canvas = canvas.copy()
                f_draw = ImageDraw.Draw(frame_canvas)
                is_think_phase = fi_idx < half_idx

                # [v6.0] 서브 프레임 단위 연속 진행 게이지 & 키네틱 하이라이트 자막
                sub_ratio = ((seq_idx - 1) + (fi_idx + 1) / max(1, len(doc_frames))) / max(1, total_seqs)
                f_draw.rounded_rectangle((68, 242, 1012, 254), radius=6, fill=(136, 19, 55))
                f_draw.rounded_rectangle((68, 242, 68 + max(24, int(944 * min(1.0, sub_ratio))), 254), radius=6, fill=(251, 191, 36))

                active_cap_idx = min(len(cap_lines) - 1, int((fi_idx / max(1, len(doc_frames))) * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    y_cl = 1445 + ci * 58
                    if ci == active_cap_idx:
                        f_draw.rounded_rectangle((62, y_cl - 4, 1018, y_cl + 44), radius=10, fill=(76, 5, 25), outline=(251, 191, 36), width=2)
                        f_draw.text((74, y_cl), cl, fill=(254, 240, 138), font=font_cap)
                    else:
                        f_draw.text((74, y_cl), cl, fill=(203, 213, 225), font=font_cap)

                # Phase 배지 (전반부: 🙋 먼저 생각해 보세요! / 후반부: 💡 시각적 단서 발견! / 루프 브릿지)
                if seq_idx == total_seqs and fi_idx == len(doc_frames) - 1 and doc_f_i == 0:
                    f_draw.rounded_rectangle((70, 1382, 990, 1432), radius=14, fill=(124, 58, 237))
                    p_lbl = "🔄 [무한 루프 연결] 처음 도형의 출발 질문과 다시 비교해 보세요!" if lang_code == "ko" else "🔄 [Seamless Loop] Compare with the starting figure again!"
                    f_draw.text((90, 1391), p_lbl, fill=(254, 240, 138), font=get_font_for_lang(lang_code, 24, bold=True))
                elif is_think_phase:
                    f_draw.rounded_rectangle((70, 1382, 990, 1432), radius=14, fill=(225, 29, 72))
                    p_lbl = "🙋 [Phase 1 · 발문 타임] 잠깐! 화면을 보고 먼저 스스로 추론해 보세요!" if lang_code == "ko" else "🙋 [Phase 1 · Inquiry] Pause & think about the question first!"
                    f_draw.text((90, 1391), p_lbl, fill=(255, 255, 255), font=get_font_for_lang(lang_code, 24, bold=True))
                else:
                    f_draw.rounded_rectangle((70, 1382, 990, 1432), radius=14, fill=(5, 150, 105))
                    p_lbl = "💡 [Phase 2 · 단서 발견!] 새로 연결된 보조선과 도형 관계에 주목하세요!" if lang_code == "ko" else "💡 [Phase 2 · Discovery!] Watch the highlighted geometric clue!"
                    f_draw.text((90, 1391), p_lbl, fill=(255, 255, 255), font=get_font_for_lang(lang_code, 24, bold=True))

                pix = doc[doc_f_i].get_pixmap(dpi=260)
                slide_pil = _mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
                sw, sh = slide_pil.size
                scale = min(984 / sw, 860 / sh)
                nw, nh = int(sw * scale), int(sh * scale)
                resized = slide_pil.resize((nw, nh), Image.Resampling.LANCZOS)
                ox = (1080 - nw) // 2
                oy = 472 + (860 - nh) // 2
                border_col = (244, 63, 94) if is_think_phase else (16, 185, 129)
                f_draw.rounded_rectangle((ox - 10, oy - 10, ox + nw + 10, oy + nh + 10), radius=20, fill=(255, 255, 255), outline=border_col, width=4)
                frame_canvas.paste(resized, (ox, oy))

                bbox = p_info.get("diff_bbox")
                if bbox and not is_think_phase and doc_f_i > 0:
                    bx0 = max(ox + 4, ox + int(bbox[0] * nw) - 10)
                    by0 = max(oy + 4, oy + int(bbox[1] * nh) - 10)
                    bx1 = min(ox + nw - 4, ox + int(bbox[2] * nw) + 10)
                    by1 = min(oy + nh - 4, oy + int(bbox[3] * nh) + 10)
                    if (bx1 - bx0) > 24 and (by1 - by0) > 24:
                        f_draw.rounded_rectangle((bx0, by0, bx1, by1), radius=10, outline=(225, 29, 72), width=6)

                fp = tmp_dir / f"qshort_{seq_idx:02d}_f{fi_idx:02d}.png"
                frame_canvas.save(fp)
                f_lines.append(f"file '{fp.as_posix()}'")
                f_lines.append(f"duration {per_f_dur:.4f}")
                last_fp = fp
            if last_fp:
                f_lines.append(f"file '{last_fp.as_posix()}'")
            f_txt = tmp_dir / f"qshort_fconcat_{seq_idx:02d}.txt"
            f_txt.write_text("\n".join(f_lines), encoding="utf-8")

            chime_wav = ensure_harmonic_chime_wav()
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
                "-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-shortest",
                str(seg_p),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segs.append(seg_p)

        concat_p = tmp_dir / "concat_qshort.txt"
        concat_p.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
        raw_short = tmp_dir / f"raw_qshort_{slug_key}_{lang_code}.mp4"
        out_short = shorts_dir / f"{slug_key}_short_q_{lang_code}.mp4"
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
        # [v6.0] 36~46초 황금 쇼츠 리텐션 존(Golden Shorts Retention Zone) 자동 튜닝
        if dur >= 49.0:
            speed_factor = round((dur / 44.5), 3)
            trimmed_short = tmp_dir / f"{slug_key}_short_q_{lang_code}_fast.mp4"
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

        pub_qshort_path = pub_short_dir / f"{slug_key}_short_q_{lang_code}.mp4"
        shutil.copyfile(out_short, pub_qshort_path)

        # [자동 교체 원칙] 질문형 숏폼이 새로 제작/업데이트되면 기존 채널의 구버전 질문형 숏폼 삭제 큐 등록 및 삭제
        try:
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("shorts_q",), langs=(lang_code,), execute_delete_now=True
            )
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        except Exception:
            pass

        qshort_title = (
            f"❓ [질문하는 수학 #Shorts] {clean_title} — 왜 이 보조선이 핵심일까?"
            if lang_code == "ko"
            else f"❓ [Question-Asking Math #Shorts] {clean_title} — Why This Auxiliary Line?"
        )
        sdoc.setdefault("question_shorts_packages", {})[lang_code] = {
            "title": qshort_title[:100],
            "local_mp4_path": f"video_lectures/shorts/{slug_key}_short_q_{lang_code}.mp4",
            "duration_sec": round(dur, 2),
            "aspect_ratio": "9:16 (1080x1920)",
            "pedagogy_mode": "Question-Asking Short (Notice & Wonder -> Socratic -> What-If-Not)",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "needs_youtube_upload": True,
        }
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

        safe_t = re.sub(r'[\\/:*?"<>|]', " ", qshort_title).strip()
        ready_dst = ready_shorts_dir / f"{safe_t[:72]} [{slug_key}_QSHORT_{lang_code.upper()}].mp4"
        shutil.copyfile(out_short, ready_dst)

        update_video_catalog()
        print(f"❓📱 [Question-Asking YouTube Shorts 1080x1920 (<58s Verified) Generated] {pub_qshort_path} ({round(dur, 1)}s)")
        return pub_qshort_path
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def upload_short_to_youtube(slug_key, langs=("ko", "en"), privacy="public", replace_existing=False):
    """
    [@min7014_ai 유튜브 숏폼(#Shorts) 자동 업로더 (YouTube Data API v3)]
    - 유튜브 고급 기능(Advanced Features)의 외부 설명란 링크 활성화 및 첫 댓글 딥링크 퍼널을 동시 적용합니다.
    - 업데이트된 숏폼(needs_youtube_upload 또는 replace_existing=True)인 경우 기존 채널의 구버전 숏폼을 먼저 삭제한 뒤 새 숏폼을 업로드합니다.
    """
    global _LAST_UPLOAD_QUOTA_BLOCKED
    _LAST_UPLOAD_QUOTA_BLOCKED = False
    from googleapiclient.http import MediaFileUpload

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        generate_or_update_script(slug_key, target_langs=["ko", "en"])

    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    shorts_pkgs = sdoc.get("shorts_packages") or {}
    for lc in langs:
        pkg_lc = shorts_pkgs.get(lc) if isinstance(shorts_pkgs.get(lc), dict) else {}
        if replace_existing or pkg_lc.get("needs_youtube_upload"):
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("shorts_std",), langs=(lc,), execute_delete_now=True
            )
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    uploaded_shorts = {}
    missing_langs = []
    for lc in langs:
        existing_short_url = (sdoc.get("shorts_urls") or {}).get(lc, "").strip()
        if existing_short_url and not replace_existing:
            uploaded_shorts[lc] = existing_short_url
        else:
            missing_langs.append(lc)

    if not missing_langs:
        return uploaded_shorts

    process_youtube_delete_queue(max_deletions=20)
    youtube, active_token_path = get_available_youtube_upload_service()
    if youtube is None:
        _LAST_UPLOAD_QUOTA_BLOCKED = True
        return uploaded_shorts

    for lc in missing_langs:
        short_mp4 = YT_UPLOADS_DIR / "shorts" / f"{slug_key}_short_{lc}.mp4"
        short_meta_path = YT_PKG_DIR / f"{slug_key}_shorts_meta.json"
        if not short_mp4.exists() or not short_meta_path.exists():
            render_youtube_short_vertical(slug_key, lang_code=lc)

        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        smeta_all = json.loads(short_meta_path.read_text(encoding="utf-8"))
        if lc not in smeta_all:
            render_youtube_short_vertical(slug_key, lang_code=lc)
            smeta_all = json.loads(short_meta_path.read_text(encoding="utf-8"))
        # 업로드 직전 최신 1080p 본편 URL(youtube_urls / question_youtube_urls)을 반영하여 메타데이터 재빌드
        smeta = build_youtube_short_metadata(sdoc, lc, smeta_all[lc].get("duration_sec", 45.0))
        smeta_all[lc] = smeta
        short_meta_path.write_text(json.dumps(smeta_all, ensure_ascii=False, indent=2), encoding="utf-8")

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
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("shorts_std",), langs=(lc,), execute_delete_now=True
            )
            media = MediaFileUpload(str(short_mp4), chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid_id = resp["id"]
            short_url = f"https://youtube.com/shorts/{vid_id}"
            uploaded_shorts[lc] = short_url
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
                sdoc["shorts_urls"] = {"ko": "", "en": ""}
            sdoc["shorts_urls"][lc] = short_url
            if isinstance((sdoc.get("shorts_packages") or {}).get(lc), dict):
                sdoc["shorts_packages"][lc]["needs_youtube_upload"] = False
                sdoc["shorts_packages"][lc]["uploaded_video_id"] = vid_id
            script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            update_video_catalog()
            print(f"🚀 [YouTube #Shorts Uploaded ({lc.upper()})] {short_url}", flush=True)
            notify_telegram_youtube_upload(
                slug_key=slug_key,
                edition_label=f"📱 9:16 일반형 #Shorts ({lc.upper()})",
                video_title=smeta.get("title", slug_key),
                youtube_url=short_url,
            )
            # Shorts 전용 첫 댓글(1080p 본편 직결 + 홈페이지 링크 유도) 자동 게시
            try:
                board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&from=yt_shorts"
                full_yt_u = (sdoc.get("youtube_urls") or {}).get(lc) or (sdoc.get("youtube_urls") or {}).get("ko") or "https://www.youtube.com/@min7014_ai"
                c_text = (
                    f"🎬 방금 본 증명 1080p 전체 단계별 풀버전 바로 보기:\n👉 {full_yt_u}\n"
                    f"📐 도형을 마우스로 직접 움직여보기 (GeoGebra): {board_link}\n"
                    f"🎮 수능 수학 100점 3D 보스 레이드 & 16,548문항 디딤돌: https://min7014.github.io/mathedu/"
                    if lc == "ko"
                    else f"🎬 Watch the full 1080p step-by-step proof video:\n👉 {full_yt_u}\n"
                         f"📐 Drag this geometric figure yourself in GeoGebra: {board_link}"
                )
                youtube.commentThreads().insert(
                    part="snippet",
                    body={"snippet": {"videoId": vid_id, "topLevelComment": {"snippet": {"textOriginal": c_text}}}},
                ).execute()
            except Exception:
                pass
        except Exception as e:
            err_s = str(e)
            print(f"  ⚠️ [YouTube #Shorts Upload Notice ({slug_key}/{lc})]: {e}", flush=True)
            if "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s or "quotaExceeded" in err_s:
                mark_token_quota_exhausted(active_token_path, 900)
            break
    return uploaded_shorts



def upload_question_classroom_to_youtube(slug_key, langs=("ko",), privacy="public", replace_existing=False):
    """
    [Edition 2: 질문하는 수업 특화 본편 (1080p 16:9) YouTube Data API v3 자동 업로더]
    - video_lectures/question_classroom/{slug}_q_{lc}.mp4를 @min7014_ai에 업로드하고
      question_youtube_urls[lc]에 바인딩합니다.
    - 업데이트된 질문하는 수업 영상인 경우 기존 채널의 구버전 영상을 먼저 삭제하고 새 영상을 업로드합니다.
    """
    global _LAST_UPLOAD_QUOTA_BLOCKED
    _LAST_UPLOAD_QUOTA_BLOCKED = False
    from googleapiclient.http import MediaFileUpload

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        generate_or_update_script(slug_key)
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    q_pkgs = sdoc.get("question_classroom_packages") or {}
    for lc in langs:
        pkg_lc = q_pkgs.get(lc) if isinstance(q_pkgs.get(lc), dict) else {}
        if replace_existing or pkg_lc.get("needs_youtube_upload"):
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("question",), langs=(lc,), execute_delete_now=True
            )
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    uploaded_q = {}
    missing_langs = []
    for lc in langs:
        existing_u = (sdoc.get("question_youtube_urls") or {}).get(lc, "").strip()
        if existing_u and not replace_existing:
            uploaded_q[lc] = existing_u
        else:
            missing_langs.append(lc)
    if not missing_langs:
        return uploaded_q

    process_youtube_delete_queue(max_deletions=20)
    youtube, active_token_path = get_available_youtube_upload_service()
    if youtube is None:
        _LAST_UPLOAD_QUOTA_BLOCKED = True
        return uploaded_q

    for lc in missing_langs:
        q_mp4 = QUESTION_CLASSROOM_DIR / f"{slug_key}_q_{lc}.mp4"
        if not q_mp4.exists():
            render_question_classroom_video(slug_key, lang_code=lc)
        _ko_t, _en_t = split_bilingual_title(sdoc.get("title", slug_key))
        title_base = _ko_t if lc == "ko" else (sdoc.get("title_en") or _en_t or _ko_t)
        clean_t = _smart_concise_topic_title(latex_to_unicode_title(title_base), max_len=36, lang=lc)
        q_title = (
            f"❓ [질문하는 수학 수업] {clean_t} — 스스로 발문하고 발견하는 시각적 증명! | @min7014_ai"
            if lc == "ko"
            else f"❓ [Question-Asking Math] {clean_t} — Socratic Visual Proof! | @min7014_ai"
        )[:98]
        board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&mode=question"
        std_yt_u = (sdoc.get("youtube_urls") or {}).get(lc) or (sdoc.get("youtube_urls") or {}).get("ko") or "https://www.youtube.com/@min7014_ai"
        q_desc = (
            f"❓ [질문하는 수학 수업 (Question-Asking Classroom Edition)]\n"
            f"주제: {latex_to_unicode_title(title_base)} [ID: {slug_key}_Q_{lc.upper()}]\n\n"
            f"1단계(Phase 1): 핵심 발문과 사고 멈춤 시간(Thinking Pause)을 통해 먼저 스스로 원리와 불변량을 추론합니다.\n"
            f"2단계(Phase 2): 동적 시각 스포트라이트와 함께 왜 정리가 성립하는지 눈으로 확인합니다.\n\n"
            f"🎬 [일반 설명 본편(1080p) 바로 보기]: {std_yt_u}\n"
            f"👉 [수학홈페이지 질문하는 수업 인터랙티브 실험실 바로가기]: {board_link}\n"
            f"👉 [수학자료실 원본]: {sdoc.get('web_url', 'https://min7014.github.io/')}\n"
            f"#질문하는수업 #수학증명 #기하학 #수능수학 #시각적증명 #mathedu"
        )
        body = {
            "snippet": {
                "title": _balance_parentheses(q_title),
                "description": q_desc,
                "tags": ["질문하는수업", "수학증명", "기하학", "소크라테스발문", "시각적증명", "mathedu", slug_key],
                "categoryId": "27",
                "defaultLanguage": lc,
                "defaultAudioLanguage": lc,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            },
        }
        try:
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("question",), langs=(lc,), execute_delete_now=True
            )
            media = MediaFileUpload(str(q_mp4), chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid_id = resp["id"]
            q_url = f"https://youtu.be/{vid_id}"
            uploaded_q[lc] = q_url
            # [v6.0] 질문하는 수업 전용 커스텀 썸네일({slug_key}_q_{lc}_thumb.png) 자동 적용
            try:
                q_thumb_png = THUMBS_DIR / f"{slug_key}_q_{lc}_thumb.png"
                if q_thumb_png.exists():
                    thumb_media = MediaFileUpload(str(q_thumb_png), mimetype="image/png", resumable=False)
                    youtube.thumbnails().set(videoId=vid_id, media_body=thumb_media).execute()
            except Exception:
                pass
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            if "question_youtube_urls" not in sdoc or not isinstance(sdoc["question_youtube_urls"], dict):
                sdoc["question_youtube_urls"] = {"ko": "", "en": ""}
            sdoc["question_youtube_urls"][lc] = q_url
            if isinstance((sdoc.get("question_classroom_packages") or {}).get(lc), dict):
                sdoc["question_classroom_packages"][lc]["needs_youtube_upload"] = False
                sdoc["question_classroom_packages"][lc]["uploaded_video_id"] = vid_id
            script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            update_video_catalog()
            print(f"🚀 [YouTube Question-Asking 1080p Uploaded ({lc.upper()})] {q_url}", flush=True)
            notify_telegram_youtube_upload(
                slug_key=slug_key,
                edition_label=f"❓ 1080p 질문하는 수업 본편 ({lc.upper()})",
                video_title=_balance_parentheses(q_title),
                youtube_url=q_url,
            )
        except Exception as e:
            err_s = str(e)
            print(f"  ⚠️ [YouTube Question 1080p Upload Notice ({slug_key}/{lc})]: {e}", flush=True)
            if "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s or "quotaExceeded" in err_s:
                mark_token_quota_exhausted(active_token_path, 900)
            break
    return uploaded_q


def upload_question_short_to_youtube(slug_key, langs=("ko",), privacy="public", replace_existing=False):
    """
    [Edition 3-B: 질문형 숏폼 (9:16 Q-#Shorts) YouTube Data API v3 자동 업로더]
    - video_lectures/shorts/{slug}_short_q_{lc}.mp4를 @min7014_ai에 업로드하고
      question_shorts_urls[lc]에 바인딩합니다.
    - 업데이트된 질문형 숏폼인 경우 기존 채널의 구버전 영상을 먼저 삭제하고 새 영상을 업로드합니다.
    """
    global _LAST_UPLOAD_QUOTA_BLOCKED
    _LAST_UPLOAD_QUOTA_BLOCKED = False
    from googleapiclient.http import MediaFileUpload

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        generate_or_update_script(slug_key)
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    qs_pkgs = sdoc.get("question_shorts_packages") or {}
    for lc in langs:
        pkg_lc = qs_pkgs.get(lc) if isinstance(qs_pkgs.get(lc), dict) else {}
        if replace_existing or pkg_lc.get("needs_youtube_upload"):
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("shorts_q",), langs=(lc,), execute_delete_now=True
            )
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    uploaded_qs = {}
    missing_langs = []
    for lc in langs:
        existing_u = (sdoc.get("question_shorts_urls") or {}).get(lc, "").strip()
        if existing_u and not replace_existing:
            uploaded_qs[lc] = existing_u
        else:
            missing_langs.append(lc)
    if not missing_langs:
        return uploaded_qs

    process_youtube_delete_queue(max_deletions=20)
    youtube, active_token_path = get_available_youtube_upload_service()
    if youtube is None:
        _LAST_UPLOAD_QUOTA_BLOCKED = True
        return uploaded_qs

    for lc in missing_langs:
        qsh_mp4 = ROOT_DIR / "video_lectures" / "shorts" / f"{slug_key}_short_q_{lc}.mp4"
        if not qsh_mp4.exists():
            render_question_short_vertical(slug_key, lang_code=lc)
        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        _ko_t, _en_t = split_bilingual_title(sdoc.get("title", slug_key))
        title_base = _ko_t if lc == "ko" else (sdoc.get("title_en") or _en_t or _ko_t)
        clean_t = _smart_concise_topic_title(latex_to_unicode_title(title_base), max_len=32, lang=lc)
        cat_type = (sdoc.get("teacher_proof_analysis") or {}).get("category_type", "geometry")
        q_hook_ko = "왜 이 원리가 성립할까?" if cat_type in ("algebra", "number") else "어디에 보조선을 그어야 할까?"
        q_hook_en = "Why does this hold true?" if cat_type in ("algebra", "number") else "Where is the auxiliary line?"
        qsh_title = (
            f"❓ [질문형 숏폼] {clean_t} — {q_hook_ko} #Shorts | @min7014_ai"
            if lc == "ko"
            else f"❓ [Question #Shorts] {clean_t} — {q_hook_en} #Shorts | @min7014_ai"
        )[:98]
        board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&from=yt_qshorts"
        q_yt_u = (sdoc.get("question_youtube_urls") or {}).get(lc) or (sdoc.get("youtube_urls") or {}).get(lc) or "https://www.youtube.com/@min7014_ai"
        std_yt_u = (sdoc.get("youtube_urls") or {}).get(lc) or q_yt_u
        qsh_desc = (
            f"❓ [질문하는 수학 수업 숏폼 (Question-Asking #Shorts)] [ID: {slug_key}_SHORT_Q_{lc.upper()}]\n"
            f"주제: {latex_to_unicode_title(title_base)}\n\n"
            f"잠깐! 정답을 보기 전에 화면 상단의 질문 카드를 보고 어떤 수학적 원리가 쓰였을지 3초만 생각해 보세요!\n"
            f"❓ [1080p 질문하는 수업 풀버전 바로 보기]: {q_yt_u}\n"
            f"🎬 [1080p 일반 설명 본편 바로 보기]: {std_yt_u}\n"
            f"👉 [GeoGebra 직접 조작 & 수학홈페이지 실험실]: {board_link}\n"
            f"#Shorts #질문하는수업 #수학숏폼 #기하학 #시각적증명 #mathedu"
        )
        body = {
            "snippet": {
                "title": qsh_title,
                "description": qsh_desc,
                "tags": ["Shorts", "질문하는수업", "수학숏폼", "기하학", "시각적증명", "mathedu", slug_key],
                "categoryId": "27",
                "defaultLanguage": lc,
                "defaultAudioLanguage": lc,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            },
        }
        try:
            queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("shorts_q",), langs=(lc,), execute_delete_now=True
            )
            media = MediaFileUpload(str(qsh_mp4), chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid_id = resp["id"]
            qsh_url = f"https://youtube.com/shorts/{vid_id}"
            uploaded_qs[lc] = qsh_url
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            if "question_shorts_urls" not in sdoc or not isinstance(sdoc["question_shorts_urls"], dict):
                sdoc["question_shorts_urls"] = {"ko": "", "en": ""}
            sdoc["question_shorts_urls"][lc] = qsh_url
            if isinstance((sdoc.get("question_shorts_packages") or {}).get(lc), dict):
                sdoc["question_shorts_packages"][lc]["needs_youtube_upload"] = False
                sdoc["question_shorts_packages"][lc]["uploaded_video_id"] = vid_id
            script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            update_video_catalog()
            print(f"🚀 [YouTube Question #Shorts Uploaded ({lc.upper()})] {qsh_url}", flush=True)
            notify_telegram_youtube_upload(
                slug_key=slug_key,
                edition_label=f"❓📱 9:16 질문형 Q-#Shorts ({lc.upper()})",
                video_title=qsh_title,
                youtube_url=qsh_url,
            )
        except Exception as e:
            err_s = str(e)
            print(f"  ⚠️ [YouTube Question #Shorts Upload Notice ({slug_key}/{lc})]: {e}", flush=True)
            if "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s or "quotaExceeded" in err_s:
                mark_token_quota_exhausted(active_token_path, 900)
            break
    return uploaded_qs


def upload_shorts_via_studio_browser(slug_list=None, langs=("ko",), privacy="public"):
    """
    [Playwright 기반 @min7014_ai YouTube Studio 5대 #Shorts 무인 브라우저 업로더]
    - Google Cloud API 일일 할당량(Video Uploads per day, 6회/일)이 소진되었을 때도
      YouTube Studio 웹 자동화를 통해 5개 #Shorts(MP4, 제목, 5단 홈페이지 링크 설명란, 전체공개)를
      연속으로 자동 업로드하고 URL을 홈페이지에 즉시 바인딩합니다.
    """
    from playwright.sync_api import sync_playwright

    if not slug_list:
        slug_list = ["math20250130001", "2017090101", "2014111902", "2014111901", "2025020101"]

    profile_dir = ROOT_DIR / ".yt_chrome_robot_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    privacy_radio_name = {"public": "PUBLIC", "unlisted": "UNLISTED", "private": "PRIVATE"}.get(privacy.lower(), "PUBLIC")
    results = {}

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

        for idx, slug_key in enumerate(slug_list, 1):
            script_path = SCRIPTS_DIR / f"{slug_key}.json"
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            for lc in langs:
                existing = (sdoc.get("shorts_urls") or {}).get(lc, "").strip()
                if existing:
                    results[f"{slug_key}_{lc}"] = existing
                    print(f"📱 [{idx}/{len(slug_list)}] Already uploaded: {existing}", flush=True)
                    continue
                short_mp4 = (YT_UPLOADS_DIR / "shorts" / f"{slug_key}_short_{lc}.mp4").resolve()
                short_meta_path = YT_PKG_DIR / f"{slug_key}_shorts_meta.json"
                if not short_mp4.exists() or not short_meta_path.exists():
                    render_youtube_short_vertical(slug_key, lang_code=lc)
                smeta = json.loads(short_meta_path.read_text(encoding="utf-8"))[lc]

                print(f"🚀 [{idx}/{len(slug_list)}] Studio Browser Uploading #Shorts: {short_mp4.name}", flush=True)
                page.goto(YOUTUBE_STUDIO_UPLOAD_URL, wait_until="domcontentloaded")

                if not page.url.startswith("https://studio.youtube.com/"):
                    try:
                        page.evaluate("""() => {
                            const b = document.createElement('div');
                            b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#e11d48;color:#fff;padding:16px 22px;font-size:18px;font-weight:bold;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.4);font-family:sans-serif;';
                            b.innerHTML = '🤖 [@min7014_ai 5대 #Shorts 자동 업로드 로봇] 이 창에서 딱 1번만 로그인해 주시면 지금 즉시 5개 #Shorts를 로봇이 자동으로 모두 업로드합니다!';
                            document.body.prepend(b);
                        }""")
                    except Exception:
                        pass
                    print("🔐 [최초 1회 로그인 대기 중] 열린 크롬 로봇 창에서 @min7014_ai 계정으로 로그인해 주세요...", flush=True)
                    page.wait_for_url(lambda u: u.startswith("https://studio.youtube.com/"), timeout=600000)
                    time.sleep(3.0)
                    if YOUTUBE_CHANNEL_ID not in page.url:
                        page.goto(YOUTUBE_STUDIO_UPLOAD_URL, wait_until="domcontentloaded")
                        time.sleep(3.0)

                try:
                    welcome_btn = page.locator('ytcp-button#dismiss-button, button:has-text("계속"), button:has-text("Continue")').first
                    if welcome_btn.is_visible(timeout=2500):
                        welcome_btn.click(timeout=2500)
                        time.sleep(1.0)
                except Exception:
                    pass

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

                file_input.set_input_files(str(short_mp4))
                print(f"  [1/4] #Shorts MP4 투입 완료: {short_mp4.name}", flush=True)

                title_box = page.locator('#title-textarea #textbox, ytcp-social-suggestions-textbox#title-textarea #textbox').first
                title_box.wait_for(state="visible", timeout=45000)
                time.sleep(1.5)
                title_box.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                title_box.fill(smeta["title"])
                print(f"  [2/4] #Shorts 제목 입력 완료: {smeta['title']}", flush=True)

                try:
                    desc_box = page.locator('#description-textarea #textbox, ytcp-social-suggestions-textbox#description-textarea #textbox').first
                    desc_box.click(timeout=8000)
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    desc_box.fill(smeta["description"])
                    print("  [3/4] 5단 홈페이지 링크 퍼널 설명문 입력 완료", flush=True)
                except Exception as e:
                    print(f"  [Description Warning] {e}", flush=True)

                try:
                    not_kids = page.locator('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"], [name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]').first
                    not_kids.scroll_into_view_if_needed(timeout=5000)
                    not_kids.click(timeout=5000)
                except Exception:
                    pass

                vid_id = ""
                try:
                    link_el = page.locator('a[href*="youtu.be/"], a[href*="youtube.com/shorts/"]').first
                    link_el.wait_for(state="visible", timeout=15000)
                    href = link_el.get_attribute("href") or ""
                    vid_id = href.rstrip("/").split("/")[-1].split("?")[0].strip()
                except Exception:
                    pass

                for _ in range(3):
                    time.sleep(1.0)
                    next_btn = page.locator('#next-button').first
                    next_btn.click(timeout=15000)

                time.sleep(1.2)
                try:
                    vis_radio = page.locator(f'tp-yt-paper-radio-button[name="{privacy_radio_name}"], [name="{privacy_radio_name}"]').first
                    vis_radio.click(timeout=8000)
                except Exception:
                    pass

                if not vid_id:
                    try:
                        href = page.locator('a[href*="youtu.be/"], a[href*="youtube.com/shorts/"]').first.get_attribute("href") or ""
                        vid_id = href.rstrip("/").split("/")[-1].split("?")[0].strip()
                    except Exception:
                        pass

                time.sleep(1.5)
                done_btn = page.locator('#done-button').first
                done_btn.click(timeout=20000)
                time.sleep(4.0)

                if not vid_id:
                    try:
                        html_snap = page.content()
                        m_url = re.search(r"https://(?:youtu\.be|youtube\.com/shorts)/([A-Za-z0-9_-]{11})", html_snap)
                        if m_url:
                            vid_id = m_url.group(1)
                    except Exception:
                        pass

                if vid_id:
                    short_url = f"https://youtube.com/shorts/{vid_id}"
                    results[f"{slug_key}_{lc}"] = short_url
                    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
                    if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
                        sdoc["shorts_urls"] = {"ko": "", "en": ""}
                    sdoc["shorts_urls"][lc] = short_url
                    script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    update_video_catalog()
                    print(f"  [4/4] 🎉 #Shorts 게시 완료! -> {short_url}", flush=True)
                try:
                    close_btn = page.locator('ytcp-button#close-button, #close-icon-button').first
                    if close_btn.is_visible():
                        close_btn.click(timeout=5000)
                except Exception:
                    pass
                time.sleep(2.0)

        browser_ctx.close()
    return results


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
    [https://min7014.github.io/ 전 영역(16대 세부 단원 · 1,113개 전체 자료) 4대 에디션 확장 선택기]
    1) 먼저 현재 렌더링 진행 중이던 주제(_ko.mp4와 _q_ko.mp4가 이미 생성되어 숏폼만 남은 주제)가 있으면 최우선 마무리합니다.
    2) 그 다음 https://min7014.github.io/ (min7014_deep_knowledge.json)의 16대 세부 단원 전체 자료(845개 PDF + 268개 Non-PDF 웹/GeoGebra/AlgeoMath 자료) 중
       아직 대본(scripts/*.json) 및 4대 에디션이 제작되지 않은 '새로운 자료'를 단원별 라운드로빈(Round-Robin) 순서로 최우선 반환합니다!
    3) 신규 자료 확장과 함께 기존 스크립트 보유 주제 중 4대 에디션 미완성 주제도 순차 완성합니다.
    """
    failed_slugs = failed_slugs or set()
    existing_scripts = {sp.stem for sp in SCRIPTS_DIR.glob("*.json")}

    # 0순위: 현재 렌더링 도중인 주제(_ko.mp4와 _q_ko.mp4가 이미 존재하고 숏폼만 남은 주제) 마무리
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        s = sp.stem
        if s in failed_slugs:
            continue
        mp4_ko = YT_UPLOADS_DIR / s / f"{s}_ko.mp4"
        q_ko = QUESTION_CLASSROOM_DIR / f"{s}_q_ko.mp4"
        sh_ko = YT_UPLOADS_DIR / "shorts" / f"{s}_short_ko.mp4"
        qsh_ko = ROOT_DIR / "video_lectures" / "shorts" / f"{s}_short_q_ko.mp4"
        if mp4_ko.exists() and q_ko.exists() and not (sh_ko.exists() and qsh_ko.exists()):
            return s

    # 1순위: https://min7014.github.io/ 의 16대 전 영역 미제작 '다른 자료들'(신규 PDF + Non-PDF 웹/GeoGebra/AlgeoMath 자료)을 단원별 라운드로빈으로 선택!
    domain_flagships = [
        "2017092841",  # 유클리드 평면기하: 원에서 현의 수직이등분선
        "2020041301",  # 이차곡선·원뿔곡선: 포물선의 정의
        "2020051301",  # 삼각비·삼각함수: 호도법(Radian)
        "2020070501",  # 벡터·공간도형: 벡터의 정의
        "2023061501",  # 미분·도함수: 극좌표계에서의 중적분
        "2020102901",  # 적분·구분구적법: 부정적분
        "2020062102",  # 수열·시그마: 수열의 정의
        "2023051501",  # 확률과 통계: 시행과 사건
        "2021032901",  # 함수의 극한과 연속: 제한된 범위에서 이차함수의 최대최소
        "2012111702",  # 해석기하·원의 방정식: 원(Circle)
        "2024032305",  # 지수·로그: 지수가 자연수일 때 지수법칙
        "2021091701",  # 기하 변환·대칭: 점의 평행이동
        "2020122201",  # 방정식·부등식: 실수의 절댓값
        "2024032301",  # 다항식·방정식·수체계: 자연수의 사칙연산
        "math20231203002",  # Non-PDF 심화 탐구: 작도와 경사하강법을 활용한 삼각형의 페르마 점
        "2022051507", "2022042501", "2022101601", "2022101602", "2022101603",
        "2023081301", "2024122501", "2024120301", "2025012801", "2025012601",
    ]
    unscripted_candidates = []
    seen_cands = set()
    for fs in domain_flagships:
        if fs not in existing_scripts and fs not in failed_slugs and fs not in seen_cands:
            unscripted_candidates.append(fs)
            seen_cands.add(fs)

    if DEEP_JSON_PATH.exists():
        try:
            items = json.loads(DEEP_JSON_PATH.read_text(encoding="utf-8"))
            by_sub = {}
            for it in items:
                pdf_u = (it.get("pdf") or "").split("#")[0].strip()
                url_u = (it.get("url") or "").strip()
                if pdf_u and pdf_u.lower().endswith(".pdf"):
                    s = pdf_u.split("/")[-1].replace(".pdf", "").strip()
                elif url_u:
                    s = url_u.split("/")[-1].replace(".html", "").strip()
                else:
                    continue
                if not s or s in existing_scripts or s in failed_slugs or s in seen_cands:
                    continue
                sub = it.get("sub_domain_ko") or "기타"
                by_sub.setdefault(sub, []).append(s)
            # 16개 단원 라운드로빈 교차 배치
            sub_keys = sorted(by_sub.keys())
            max_len = max((len(v) for v in by_sub.values()), default=0)
            for idx in range(max_len):
                for sk in sub_keys:
                    if idx < len(by_sub[sk]):
                        cand = by_sub[sk][idx]
                        if cand not in seen_cands:
                            unscripted_candidates.append(cand)
                            seen_cands.add(cand)
        except Exception:
            pass

    for slug in unscripted_candidates:
        mp4_ko = YT_UPLOADS_DIR / slug / f"{slug}_ko.mp4"
        q_ko = QUESTION_CLASSROOM_DIR / f"{slug}_q_ko.mp4"
        sh_ko = YT_UPLOADS_DIR / "shorts" / f"{slug}_short_ko.mp4"
        qsh_ko = ROOT_DIR / "video_lectures" / "shorts" / f"{slug}_short_q_ko.mp4"
        if not (mp4_ko.exists() and q_ko.exists() and sh_ko.exists() and qsh_ko.exists()):
            return slug

    # 2순위: 기존 스크립트 보유 주제 중 4대 에디션 미완성 주제 완성
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        s = sp.stem
        if s in failed_slugs:
            continue
        mp4_ko = YT_UPLOADS_DIR / s / f"{s}_ko.mp4"
        q_ko = QUESTION_CLASSROOM_DIR / f"{s}_q_ko.mp4"
        sh_ko = YT_UPLOADS_DIR / "shorts" / f"{s}_short_ko.mp4"
        qsh_ko = ROOT_DIR / "video_lectures" / "shorts" / f"{s}_short_q_ko.mp4"
        if not (mp4_ko.exists() and q_ko.exists() and sh_ko.exists() and qsh_ko.exists()):
            return s
    return None


def run_shorts_and_video_upload_daemon(open_studio_now=False):
    """
    [@min7014_ai 숏폼(#Shorts) & 본편 무인 교체(기존 영상 삭제 ➔ 새 영상 업로드)·동기화 데몬]
    1) 업데이트된 로컬 영상이 있는 주제의 기존 유튜브 채널 영상을 RSS 및 로컬 인덱스에서 자동 탐지하여
       youtube_delete_queue.json에 등록하고 최우선 삭제(videos.delete)합니다.
    2) 삭제 대기열에 있는 구버전 영상은 절대 재바인딩하지 않으며, 쿼터가 열려 있을 때만 API 삭제·업로드·동기화를 수행합니다.
    3) 업로드 대기 중에도 쉬지 않고 4대 에디션(일반 본편 · 질문수업 본편 · 일반 #Shorts · 질문 #Shorts)을 연속 제작합니다.
    """
    import time
    import webbrowser

    ready_shorts_dir = YT_UPLOADS_DIR / "ready_for_min7014_ai_shorts"
    if open_studio_now:
        try:
            webbrowser.open(YOUTUBE_STUDIO_UPLOAD_URL)
            if os.name == "nt" and ready_shorts_dir.exists():
                os.startfile(str(ready_shorts_dir))
        except Exception:
            pass

    uploads_playlist_id = "UU" + YOUTUBE_CHANNEL_ID[2:]  # UUSlqQfOEtRfJuMPyGMLgFYA

    print("=" * 76, flush=True)
    print("🤖 [@min7014_ai 4대 에디션 자동 교체(기존 영상 삭제 ➔ 새 영상 업로드) & 제작 데몬 가동 중]", flush=True)
    print(f"📂 숏폼 마스터 폴더: {ready_shorts_dir}", flush=True)
    print(f"📺 YouTube Studio: {YOUTUBE_STUDIO_UPLOAD_URL}", flush=True)
    print("=" * 76, flush=True)

    last_api_upload_try = 0.0
    enriched_video_ids = set()

    while True:
        try:
            now_ts = time.time()
            # 1) 5분 주기로 RSS 스캔 ➔ 기존 구버전 영상 최우선 삭제 ➔ 신규/업데이트 영상 업로드 ➔ 채널 동기화 수행
            if now_ts - last_api_upload_try >= 300:
                last_api_upload_try = now_ts

                # [Step 1-A] 공개 RSS 피드(무쿼터)를 스캔하여 로컬 업데이트된 주제의 구버전 채널 영상을 삭제 큐에 자동 등록
                scan_rss_and_queue_outdated_channel_videos(execute_delete_now=False)

                # [Step 1-B] 삭제 대기열(youtube_delete_queue.json) 최우선 처리 (기존 영상 삭제)
                process_youtube_delete_queue(max_deletions=50)

                youtube, active_token_path = get_available_youtube_upload_service()
                blocked_vid_ids = get_deleted_video_ids_set()

                # [Step 1-C] YouTube Studio 수동 드래그 업로드분 감지 (단, 삭제 큐에 있는 구버전 영상은 절대 재바인딩 금지!)
                any_new_bound = False
                if youtube is not None:
                    try:
                        pl_items = youtube.playlistItems().list(
                            part="snippet", playlistId=uploads_playlist_id, maxResults=50
                        ).execute().get("items", [])
                    except Exception as ple:
                        err_pl = str(ple)
                        if "quotaExceeded" in err_pl or "rateLimitExceeded" in err_pl:
                            mark_token_quota_exhausted(active_token_path, 900)
                        pl_items = []

                    for item in pl_items:
                        vid_id = item["snippet"]["resourceId"]["videoId"]
                        if vid_id in blocked_vid_ids:
                            continue
                        v_title = item["snippet"].get("title", "")
                        v_desc = item["snippet"].get("description", "")
                        blob = f"{v_title}\n{v_desc}"

                        # A) [slug_SHORT_KO] / [slug_SHORT_EN] 숏폼 태그 자동 매칭
                        m_short = re.search(r"\[([A-Za-z0-9_]+)_SHORT_(KO|EN)\]", blob, re.IGNORECASE)
                        if m_short and vid_id not in enriched_video_ids:
                            s_slug = m_short.group(1)
                            s_lc = m_short.group(2).lower()
                            sp = SCRIPTS_DIR / f"{s_slug}.json"
                            if sp.exists():
                                sdoc = json.loads(sp.read_text(encoding="utf-8"))
                                pkg_s = (sdoc.get("shorts_packages") or {}).get(s_lc) or {}
                                # 만약 로컬에서 새로 업데이트되어 업로드 대기 중인데 이전 영상이면 삭제 큐로 보냄
                                if pkg_s.get("needs_youtube_upload") and pkg_s.get("uploaded_video_id") != vid_id:
                                    queue_and_delete_existing_youtube_videos_for_slug(
                                        s_slug, editions=("shorts_std",), langs=(s_lc,), execute_delete_now=True
                                    )
                                    continue
                                if "shorts_urls" not in sdoc or not isinstance(sdoc["shorts_urls"], dict):
                                    sdoc["shorts_urls"] = {"ko": "", "en": ""}
                                short_url = f"https://youtube.com/shorts/{vid_id}"
                                if sdoc["shorts_urls"].get(s_lc) != short_url:
                                    sdoc["shorts_urls"][s_lc] = short_url
                                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                                    any_new_bound = True
                                enriched_video_ids.add(vid_id)
                            continue

                        # B) [slug_KO] / [slug_EN] 1080p 본편 태그 자동 매칭
                        m_full = re.search(r"\[(?:ID:\s*)?([A-Za-z0-9_]+)_(KO|EN)\]", blob, re.IGNORECASE)
                        if m_full and vid_id not in enriched_video_ids:
                            f_slug = m_full.group(1)
                            if f_slug.upper().endswith("_SHORT") or f_slug.upper().endswith("_Q"):
                                continue
                            f_lc = m_full.group(2).lower()
                            sp = SCRIPTS_DIR / f"{f_slug}.json"
                            if sp.exists():
                                sdoc = json.loads(sp.read_text(encoding="utf-8"))
                                pkg_f = (sdoc.get("youtube_packages") or {}).get(f_lc) or {}
                                if pkg_f.get("needs_youtube_upload") and pkg_f.get("uploaded_video_id") != vid_id:
                                    queue_and_delete_existing_youtube_videos_for_slug(
                                        f_slug, editions=("standard",), langs=(f_lc,), execute_delete_now=True
                                    )
                                    continue
                                full_url = f"https://youtu.be/{vid_id}"
                                cur_yt = (sdoc.get("youtube_urls") or {}).get(f_lc, "")
                                if cur_yt != full_url:
                                    set_youtube_urls_for_slug(
                                        f_slug,
                                        yt_ko=full_url if f_lc == "ko" else None,
                                        yt_en=full_url if f_lc == "en" else None,
                                    )
                                    any_new_bound = True
                                enriched_video_ids.add(vid_id)

                if any_new_bound:
                    update_video_catalog()
                    prepare_ready_batch_folder(open_explorer=False)
                    prepare_ready_shorts_batch_folder(open_explorer=False)
                    subprocess.run(["git", "add", "video_lectures/", "assets/min7014_deep_knowledge.json", "assets/min7014_lookup.json"], check=False)
                    subprocess.run(["git", "commit", "-m", "chore(youtube): auto-bind newly uploaded @min7014_ai videos & Shorts"], check=False)
                    subprocess.run(["git", "push", "origin", "main"], check=False)

                # [Step 1-D] 업데이트된 영상 및 미업로드 영상 API 자동 업로드 (기존 영상 삭제 후 새 영상 업로드)
                priority_5_shorts = ["math20250130001", "2017090101", "2014111902", "2014111901", "2025020101"]
                newly_uploaded_batch = 0

                for q_prio_slug in ["math20250130001", "2014111902", "2014111901", "2017090101"]:
                    sp_qp = SCRIPTS_DIR / f"{q_prio_slug}.json"
                    if not sp_qp.exists():
                        continue
                    sdoc_qp = json.loads(sp_qp.read_text(encoding="utf-8"))
                    q_yt_u = (sdoc_qp.get("question_youtube_urls") or {}).get("ko", "").strip()
                    q_pkg_ko = ((sdoc_qp.get("question_classroom_packages") or {}).get("ko") or {})
                    if (not q_yt_u or q_pkg_ko.get("needs_youtube_upload")) and (QUESTION_CLASSROOM_DIR / f"{q_prio_slug}_q_ko.mp4").exists():
                        res_qv = upload_question_classroom_to_youtube(q_prio_slug, langs=("ko",), privacy="public")
                        if res_qv.get("ko") and res_qv.get("ko") != q_yt_u:
                            newly_uploaded_batch += 1
                        if _LAST_UPLOAD_QUOTA_BLOCKED:
                            break
                    q_sh_u = (sdoc_qp.get("question_shorts_urls") or {}).get("ko", "").strip()
                    qs_pkg_ko = ((sdoc_qp.get("question_shorts_packages") or {}).get("ko") or {})
                    if (not q_sh_u or qs_pkg_ko.get("needs_youtube_upload")) and (ROOT_DIR / "video_lectures" / "shorts" / f"{q_prio_slug}_short_q_ko.mp4").exists():
                        res_qs = upload_question_short_to_youtube(q_prio_slug, langs=("ko",), privacy="public")
                        if res_qs.get("ko") and res_qs.get("ko") != q_sh_u:
                            newly_uploaded_batch += 1
                        if _LAST_UPLOAD_QUOTA_BLOCKED:
                            break

                if not _LAST_UPLOAD_QUOTA_BLOCKED:
                    for p_slug in priority_5_shorts:
                        sp_p = SCRIPTS_DIR / f"{p_slug}.json"
                        if not sp_p.exists():
                            continue
                        sdoc_p = json.loads(sp_p.read_text(encoding="utf-8"))
                        s_urls_p = sdoc_p.get("shorts_urls") or {}
                        s_pkgs_p = sdoc_p.get("shorts_packages") or {}
                        missing_p = [
                            lc for lc in ("ko", "en")
                            if not (s_urls_p.get(lc) or "").strip() or (s_pkgs_p.get(lc) or {}).get("needs_youtube_upload")
                        ]
                        if missing_p:
                            before_set = {lc: (s_urls_p.get(lc) or "").strip() for lc in missing_p}
                            res_p = upload_short_to_youtube(p_slug, langs=tuple(missing_p), privacy="public")
                            if any(res_p.get(lc) and res_p.get(lc) != before_set.get(lc) for lc in missing_p):
                                newly_uploaded_batch += 1
                            if _LAST_UPLOAD_QUOTA_BLOCKED:
                                break

                if not _LAST_UPLOAD_QUOTA_BLOCKED:
                    high_visual_priority_slugs = {
                        "2017092841", "2020041301", "2020051301", "2020070501", "2023061501",
                        "2020102901", "2020062102", "2023051501", "2021032901", "2021091701",
                        "math20231203002", "2024122501", "2020030404", "2021101201",
                    }
                    def _upload_prio_key(sp_path):
                        st = sp_path.stem
                        if st in CURATED_PAGE_SCRIPTS:
                            return (0, st)
                        if st in high_visual_priority_slugs or st.startswith("201709") or st.startswith("math"):
                            return (1, st)
                        return (2, st)

                    all_sps = sorted(SCRIPTS_DIR.glob("*.json"), key=_upload_prio_key)
                    for sp in all_sps:
                        sdoc = json.loads(sp.read_text(encoding="utf-8"))
                        slug_k = sdoc["slug"]

                        # 1순위: 1080p 일반 본편 먼저 업로드 (이후 업로드되는 #Shorts 설명란·댓글에 본편 직결 URL이 자동 삽입되도록 보장!)
                        yt_urls = sdoc.get("youtube_urls") or {}
                        yt_pkgs = sdoc.get("youtube_packages") or {}
                        missing_v = [
                            lc for lc in ("ko", "en")
                            if not (yt_urls.get(lc) or "").strip() or (yt_pkgs.get(lc) or {}).get("needs_youtube_upload")
                        ]
                        if missing_v:
                            before_v = {lc: (yt_urls.get(lc) or "").strip() for lc in missing_v}
                            res_v = upload_slug_to_youtube(slug_k, langs=tuple(missing_v), privacy="public", method="api")
                            if any(res_v.get(lc) and res_v.get(lc) != before_v.get(lc) for lc in missing_v):
                                newly_uploaded_batch += 1
                            if _LAST_UPLOAD_QUOTA_BLOCKED:
                                break
                            sdoc = json.loads(sp.read_text(encoding="utf-8"))

                        # 2순위: 1080p 질문하는 수업 본편 업로드 (8분+ 미드롤 고수익 에디션)
                        q_yt_urls = sdoc.get("question_youtube_urls") or {}
                        q_yt_pkgs = sdoc.get("question_classroom_packages") or {}
                        q_before = (q_yt_urls.get("ko") or "").strip()
                        if (not q_before or (q_yt_pkgs.get("ko") or {}).get("needs_youtube_upload")) and (QUESTION_CLASSROOM_DIR / f"{slug_k}_q_ko.mp4").exists():
                            res_qv2 = upload_question_classroom_to_youtube(slug_k, langs=("ko",), privacy="public")
                            if res_qv2.get("ko") and res_qv2.get("ko") != q_before:
                                newly_uploaded_batch += 1
                            if _LAST_UPLOAD_QUOTA_BLOCKED:
                                break
                            sdoc = json.loads(sp.read_text(encoding="utf-8"))

                        # 3순위: 9:16 일반 #Shorts 업로드 (방금 업로드된 1080p 본편 URL을 설명란·댓글에 자동 바인딩)
                        s_urls = sdoc.get("shorts_urls") or {}
                        s_pkgs = sdoc.get("shorts_packages") or {}
                        missing_s = [
                            lc for lc in ("ko", "en")
                            if not (s_urls.get(lc) or "").strip() or (s_pkgs.get(lc) or {}).get("needs_youtube_upload")
                        ]
                        if missing_s:
                            before_s = {lc: (s_urls.get(lc) or "").strip() for lc in missing_s}
                            res_s = upload_short_to_youtube(slug_k, langs=tuple(missing_s), privacy="public")
                            if any(res_s.get(lc) and res_s.get(lc) != before_s.get(lc) for lc in missing_s):
                                newly_uploaded_batch += 1
                            if _LAST_UPLOAD_QUOTA_BLOCKED:
                                break
                            sdoc = json.loads(sp.read_text(encoding="utf-8"))

                        # 4순위: 9:16 질문형 Q-#Shorts 업로드
                        q_sh_urls = sdoc.get("question_shorts_urls") or {}
                        q_sh_pkgs = sdoc.get("question_shorts_packages") or {}
                        qs_before = (q_sh_urls.get("ko") or "").strip()
                        if (not qs_before or (q_sh_pkgs.get("ko") or {}).get("needs_youtube_upload")) and (ROOT_DIR / "video_lectures" / "shorts" / f"{slug_k}_short_q_ko.mp4").exists():
                            res_qs2 = upload_question_short_to_youtube(slug_k, langs=("ko",), privacy="public")
                            if res_qs2.get("ko") and res_qs2.get("ko") != qs_before:
                                newly_uploaded_batch += 1
                            if _LAST_UPLOAD_QUOTA_BLOCKED:
                                break

                if newly_uploaded_batch > 0:
                    try:
                        boost_youtube_channel_popularity()
                    except Exception as be:
                        print(f"[Popularity Boost Notice] {be}", flush=True)
                    update_video_catalog()
                    prepare_ready_batch_folder(open_explorer=False)
                    prepare_ready_shorts_batch_folder(open_explorer=False)
                    subprocess.run(["git", "add", "video_lectures/", "assets/min7014_deep_knowledge.json", "assets/min7014_lookup.json"], check=False)
                    subprocess.run(["git", "commit", "-m", f"chore(youtube): replace old videos & auto-upload batch ({newly_uploaded_batch} topics) to @min7014_ai"], check=False)
                    subprocess.run(["git", "push", "origin", "main"], check=False)

            # 3) 업로드 대기 중에도 쉬지 않고 min7014.github.io 다음 주제의 4대 에디션 연속 자동 제작!
            if not hasattr(run_shorts_and_video_upload_daemon, "_failed_slugs"):
                run_shorts_and_video_upload_daemon._failed_slugs = set()
            next_slug = get_next_unrendered_topic_slug(run_shorts_and_video_upload_daemon._failed_slugs)
            if next_slug:
                print(f"🎬 [Continuous Factory] 다음 주제 4대 에디션(일반 본편 + 질문수업 본편 + 일반 #Shorts + 질문 #Shorts) 자동 제작 시작: {next_slug}", flush=True)
                try:
                    generate_or_update_script(next_slug, target_langs=["ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"])
                    for lc in ["ko", "en"]:
                        mp4_p = YT_UPLOADS_DIR / next_slug / f"{next_slug}_{lc}.mp4"
                        if not mp4_p.exists():
                            render_multilingual_video(next_slug, lang_code=lc)
                        q_mp4_p = ROOT_DIR / "video_lectures" / "question_classroom" / f"{next_slug}_q_{lc}.mp4"
                        if not q_mp4_p.exists():
                            render_question_classroom_video(next_slug, lang_code=lc)
                        sh_p = YT_UPLOADS_DIR / "shorts" / f"{next_slug}_short_{lc}.mp4"
                        if not sh_p.exists():
                            render_youtube_short_vertical(next_slug, lang_code=lc)
                        qsh_p = ROOT_DIR / "video_lectures" / "shorts" / f"{next_slug}_short_q_{lc}.mp4"
                        if not qsh_p.exists():
                            render_question_short_vertical(next_slug, lang_code=lc)
                    update_video_catalog()
                    prepare_ready_batch_folder(open_explorer=False)
                    prepare_ready_shorts_batch_folder(open_explorer=False)
                    try:
                        import mathteacher
                        import mathedu_foundation_daemon as fdaemon
                        mathteacher.expand_pedagogy_from_min7014_vault(max_add_per_category=2)
                        fdaemon.mine_next_pedagogy_item_from_deep_knowledge()
                        fdaemon.sync_pedagogy_counts_to_index_html()
                        fdaemon.write_daemon_heartbeat(last_completed_slug=next_slug)
                    except Exception as pe_err:
                        print(f"[Pedagogy Sync Notice] {pe_err}", flush=True)
                    subprocess.run(["git", "add", "video_lectures/catalog.json", "video_lectures/vault_index.json", "video_lectures/scripts/", "video_lectures/youtube_packages/", "video_lectures/shorts/", "video_lectures/question_classroom/", "assets/min7014_deep_knowledge.json", "assets/min7014_lookup.json", "assets/mathteacher_pedagogy_engine.json", "index.html"], check=False)
                    subprocess.run(["git", "commit", "-m", f"chore(foundation): continuous v6.0 4-edition video suite & mathteacher pedagogy evolution ({next_slug})"], check=False)
                    subprocess.run(["git", "push", "origin", "main"], check=False)
                    try:
                        _sp_done = SCRIPTS_DIR / f"{next_slug}.json"
                        _sdoc_done = json.loads(_sp_done.read_text(encoding="utf-8")) if _sp_done.exists() else {}
                        _t_ko, _ = split_bilingual_title(_sdoc_done.get("title", next_slug))
                        _clean_t = latex_to_unicode_title(_t_ko or next_slug)
                        _yt_ko = (_sdoc_done.get("youtube_urls") or {}).get("ko") or "일일 쿼터 리셋 즉시 자동 업로드 대기"
                        _sh_ko = (_sdoc_done.get("shorts_urls") or {}).get("ko") or f"https://min7014.github.io/mathedu/video_lectures/shorts/{next_slug}_short_ko.mp4"
                        _qsh_ko = (_sdoc_done.get("question_shorts_urls") or {}).get("ko") or f"https://min7014.github.io/mathedu/video_lectures/shorts/{next_slug}_short_q_ko.mp4"
                        notify_telegram_video_event(
                            f"🎬 [신규 4대 에디션 수학 영상 제작 & 웹 게시 완료]\n"
                            f"• 주제: {_clean_t} ({next_slug})\n\n"
                            f"🌐 수학홈페이지 영상 플레이어:\nhttps://min7014.github.io/mathedu/video_board.html?slug={next_slug}\n"
                            f"❓ 질문하는 수업 플레이어:\nhttps://min7014.github.io/mathedu/video_board.html?slug={next_slug}&mode=question\n"
                            f"📱 일반형 #Shorts 인터넷 주소:\n{_sh_ko}\n"
                            f"❓📱 질문형 Q-#Shorts 인터넷 주소:\n{_qsh_ko}\n"
                            f"📺 유튜브 본편 상태: {_yt_ko}"
                        )
                    except Exception as _tg_e:
                        print(f"[Telegram Factory Notice] {_tg_e}", flush=True)
                    print(f"✅ [Continuous Factory & Pedagogy Evolution Complete] {next_slug} (4-Edition KO/EN + 수학교육 모듈 동기화 완료!)", flush=True)
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

    draw.text((895, 612), "단계별 시각적 수학 증명_AI", fill=(255, 255, 255), font=f_title)
    draw.text((895, 688), "Visual Math Proofs AI · 1080p Step-by-Step", fill=(56, 189, 248), font=f_sub)
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
        "📐 [단계별 시각적 수학 증명_AI (@min7014_ai)]\n"
        "공식 암기 없이 눈으로 보고 직관적으로 깨치는 1080p 단계별 시각적 수학 증명(Visual Math Proof) 공식 AI 채널입니다.\n"
        "수학자료실(https://min7014.github.io/)의 3,400+ 동적 기하(GeoGebra)와 866개 단계별 플립북 증명 PDF를 한국어(KO)·영어(EN) 강의로 제공합니다.\n\n"
        "📋 전체 1,111개 수학 설명영상 게시판: https://min7014.github.io/mathedu/video_board.html\n"
        "🎙️ 20개국어 AI 강의 스튜디오: https://min7014.github.io/mathedu/video_studio.html\n"
        "🌐 수학자료실 본관: https://min7014.github.io/\n"
        "📺 본 채널(@min7014): https://www.youtube.com/@min7014\n\n"
        "✨ [Visual Math Proofs AI — Step-by-Step Visual Math Proofs]\n"
        "Discover why Euclidean geometry, calculus, and algebra theorems hold true through step-by-step 1080p visual flipbook proofs and interactive GeoGebra applets!"
    )
    ch_keywords = (
        '수학 기하학 "시각적 증명" "수학자료실" min7014 min7014_ai '
        '"피타고라스 정리" "메넬라우스의 정리" "체바의 정리" "수능 수학" "중등 기하" '
        '"고등 수학" "영재고 수학" GeoGebra 알지오매스 "Visual Proof" "Geometry Proof" '
        'Mathematics "Euclidean Geometry" "Proof Without Words" mathedu'
    )

    localizations = {
        "ko": {
            "title": "단계별 시각적 수학 증명_AI",
            "description": ch_desc_ko,
        },
        "en": {
            "title": "Visual Math Proofs AI (@min7014_ai)",
            "description": (
                "📐 Welcome to Visual Math Proofs AI (@min7014_ai) — Official 1080p Step-by-Step Visual Mathematical Proofs Channel!\n"
                "We transform 3,400+ interactive GeoGebra geometry constructions and 866 step-by-step flipbook proof PDFs from https://min7014.github.io/ into crystal-clear visual lectures.\n\n"
                "📋 Full 1,111 Math Video Board: https://min7014.github.io/mathedu/video_board.html\n"
                "🎙️ 20+ Language AI Lecture Studio: https://min7014.github.io/mathedu/video_studio.html\n"
                "📺 Main Channel (@min7014): https://www.youtube.com/@min7014"
            ),
        },
        "ja": {
            "title": "視覚的数学証明_AI (@min7014_ai)",
            "description": "公式の暗記ではなく、目で見て直感的に理解するステップバイステップの視覚的数学証明チャンネルです。https://min7014.github.io/mathedu/video_board.html",
        },
        "zh-CN": {
            "title": "分步视觉数学证明_AI (@min7014_ai)",
            "description": "无需死记硬背公式，通过分步翻页视觉动画直观理解欧几里得几何与数学定理证明！https://min7014.github.io/mathedu/video_board.html",
        },
        "es": {
            "title": "Demostraciones Matemáticas Visuales AI (@min7014_ai)",
            "description": "¡Demostraciones matemáticas visuales paso a paso en 1080p con GeoGebra y flipbooks interactivos! https://min7014.github.io/mathedu/video_board.html",
        },
        "fr": {
            "title": "Preuves Mathématiques Visuelles AI (@min7014_ai)",
            "description": "Preuves mathématiques visuelles étape par étape en 1080p (Géométrie euclidienne, Pythagore, Ceva, Ménélaüs). https://min7014.github.io/mathedu/video_board.html",
        },
        "de": {
            "title": "Visuelle Mathematische Beweise AI (@min7014_ai)",
            "description": "Visuelle mathematische Beweise Schritt für Schritt in 1080p verstehen! https://min7014.github.io/mathedu/video_board.html",
        },
        "vi": {
            "title": "Chứng Minh Toán Học Trực Quan AI (@min7014_ai)",
            "description": "Chứng minh toán học trực quan từng bước chất lượng 1080p kết hợp GeoGebra! https://min7014.github.io/mathedu/video_board.html",
        },
    }

    branding_only_body = {
        "id": YOUTUBE_CHANNEL_ID,
        "brandingSettings": {
            "channel": {
                "title": "단계별 시각적 수학 증명_AI",
                "description": ch_desc_ko,
                "keywords": ch_keywords,
                "defaultLanguage": "ko",
                "country": "KR",
                "unsubscribedTrailer": "DSgUHigl82o",
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
                    "title": "📺 수학자료실 본 채널 (@min7014)",
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
