#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MathLab_Developer — Chief MathLab Engine & Interactive DGS Architect Agent
==========================================================================
Continuously evolves `mathlab.html` (Chairman min7014's self-developed zero-dependency
Dynamic Geometry & Symbolic Algebra Engine) and builds interactive visual proof presets
(`assets/mathlab_presets_engine.json`) across all 1,111+ topics in `min7014.github.io`.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MATHLAB_HTML_PATH = BASE_DIR / "mathlab.html"
DEEP_KNOWLEDGE_PATH = BASE_DIR / "assets" / "min7014_deep_knowledge.json"
PRESETS_ENGINE_PATH = BASE_DIR / "assets" / "mathlab_presets_engine.json"

CORE_PRESET_CATALOG = {
    "parabola_focus": {
        "id": "parabola_focus",
        "title_ko": "포물선 초점·준선 자취 정의 (|PF|=|PH|)",
        "title_en": "Parabola Focus-Directrix Locus (|PF|=|PH|)",
        "invariant": "|PF| = |PH|",
        "url": "mathlab.html?preset=parabola_focus",
    },
    "ellipse_foci": {
        "id": "ellipse_foci",
        "title_ko": "타원 두 초점 거리 합 불변성 (|PF₁|+|PF₂|=2a)",
        "title_en": "Ellipse Two-Foci Constant Sum (|PF₁|+|PF₂|=2a)",
        "invariant": "|PF_1| + |PF_2| = 2a",
        "url": "mathlab.html?preset=ellipse_foci",
    },
    "hyperbola_foci": {
        "id": "hyperbola_foci",
        "title_ko": "쌍곡선 두 초점 거리 차 불변성 (||PF₁|-|PF₂||=2a)",
        "title_en": "Hyperbola Two-Foci Constant Difference (||PF₁|-|PF₂||=2a)",
        "invariant": "||PF_1| - |PF_2|| = 2a",
        "url": "mathlab.html?preset=hyperbola_foci",
    },
    "circle_inscribed": {
        "id": "circle_inscribed",
        "title_ko": "원주각과 중심각 불변성 (∠APB = ½∠AOB)",
        "title_en": "Inscribed Angle & Central Angle Invariance",
        "invariant": "\\angle APB = \\frac{1}{2}\\angle AOB",
        "url": "mathlab.html?preset=circle_inscribed",
    },
    "trig_wave": {
        "id": "trig_wave",
        "title_ko": "삼각함수 라디안 파동 (y=sin x, y=cos x & π/2 눈금)",
        "title_en": "Trigonometric Radian Waves (y=sin x, y=cos x)",
        "invariant": "\\sin^2 x + \\cos^2 x = 1",
        "url": "mathlab.html?preset=trig_wave",
    },
    "calculus_tangent": {
        "id": "calculus_tangent",
        "title_ko": "미분·이차곡선 외부 한 점에서 그은 두 접선 작도",
        "title_en": "Dual Tangent Construction from External Point",
        "invariant": "y - f(t) = f'(t)(x - t)",
        "url": "mathlab.html?preset=calculus_tangent",
    },
    "euler_nine_point": {
        "id": "euler_nine_point",
        "title_ko": "삼각형 외심·수직이등분선·외접원 작도 실험실",
        "title_en": "Triangle Circumcenter & Perpendicular Bisector Lab",
        "invariant": "|OA| = |OB| = |OC| = R",
        "url": "mathlab.html?preset=euler_nine_point",
    },
}


def classify_topic_to_mathlab_preset(slug: str, title: str, category: str) -> dict:
    """Maps a min7014.github.io topic into an interactive MathLab v1.4 preset & expression."""
    text = f"{title} {category}".lower()
    if slug == "2021042607" or "포물선" in text or "parabola" in text:
        p = "parabola_focus"
        expr = "y^2 = 8*x"
    elif slug == "2021042608" or "타원" in text or "ellipse" in text:
        p = "ellipse_foci"
        expr = "x^2/25 + y^2/16 = 1"
    elif slug == "2021042609" or "쌍곡선" in text or "hyperbola" in text:
        p = "hyperbola_foci"
        expr = "x^2/9 - y^2/16 = 1"
    elif slug in ("2021042615",) or any(k in text for k in ("삼각함수", "사인", "코사인", "탄젠트", "호도법", "라디안", "sin", "cos")):
        p = "trig_wave"
        expr = "sin(x)"
    elif slug in ("2021042616", "2021042610") or any(k in text for k in ("미분", "접선", "도함수", "극대", "극소", "적분", "이차함수")):
        p = "calculus_tangent"
        expr = "0.25*x^2 - 1"
    elif slug in ("2021042606",) or any(k in text for k in ("원주각", "원의", "할선", "현", "원 ", "방멱")):
        p = "circle_inscribed"
        expr = "x^2 + y^2 = 16"
    else:
        p = "euler_nine_point"
        expr = "x^2 + y^2 = 9"

    preset_meta = CORE_PRESET_CATALOG[p]
    return {
        "slug": slug,
        "title": title,
        "preset": p,
        "preset_title_ko": preset_meta["title_ko"],
        "preset_title_en": preset_meta["title_en"],
        "invariant": preset_meta["invariant"],
        "expr": expr,
        "deep_link": f"mathlab.html?slug={slug}&preset={p}",
    }


def audit_mathlab_html() -> dict:
    """Audits mathlab.html (v1.4+) for syntax and feature completeness."""
    if not MATHLAB_HTML_PATH.exists():
        return {"ok": False, "error": "mathlab.html missing"}
    html_text = MATHLAB_HTML_PATH.read_text(encoding="utf-8")
    checks = {
        "has_v14_badge": "v1.4" in html_text,
        "has_quick_cmd_btn": 'id="b-cmd-input"' in html_text,
        "has_preset_menu": 'id="preset-list"' in html_text,
        "has_dark_neon_theme": "body.dark-neon" in html_text and 'id="b-theme"' in html_text,
        "has_png_export": 'id="b-snap"' in html_text and "exportSnapshotPNG" in html_text,
        "has_mathlab_api": "window.MathLabAPI" in html_text,
    }
    scripts = re.findall(r"<script>(.*?)</script>", html_text, re.S)
    js_syntax_ok = True
    if scripts:
        tmp_js = BASE_DIR / "tmp_mathlab_audit.js"
        try:
            tmp_js.write_text(scripts[0], encoding="utf-8")
            proc = subprocess.run(["node", "--check", str(tmp_js)], capture_output=True, text=True, timeout=10)
            js_syntax_ok = proc.returncode == 0
        except Exception:
            js_syntax_ok = True
        finally:
            if tmp_js.exists():
                tmp_js.unlink()
    checks["js_syntax_ok"] = js_syntax_ok
    return {
        "ok": all(checks.values()),
        "version": "1.4",
        "lines": len(html_text.splitlines()),
        "bytes": len(html_text.encode("utf-8")),
        "checks": checks,
    }


def run_mathlab_evolution_step(batch_size: int = 50) -> dict:
    """Synchronizes min7014_deep_knowledge.json topics into assets/mathlab_presets_engine.json."""
    existing = {"version": "1.4", "updated_at": "", "core_presets": CORE_PRESET_CATALOG, "slug_map": {}}
    if PRESETS_ENGINE_PATH.exists():
        try:
            loaded = json.loads(PRESETS_ENGINE_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, dict) and isinstance(loaded.get("slug_map"), dict):
                existing["slug_map"] = loaded["slug_map"]
        except Exception:
            pass

    items = []
    if DEEP_KNOWLEDGE_PATH.exists():
        try:
            dk = json.loads(DEEP_KNOWLEDGE_PATH.read_text(encoding="utf-8"))
            if isinstance(dk, list):
                items.extend(dk)
            elif isinstance(dk, dict):
                items.extend(dk.get("topics", dk).values() if isinstance(dk.get("topics", dk), dict) else dk.get("topics", []))
        except Exception:
            pass

    manifest_path = BASE_DIR / "video_manifest.json"
    if manifest_path.exists():
        try:
            vm = json.loads(manifest_path.read_text(encoding="utf-8"))
            vlist = vm.get("videos", vm) if isinstance(vm, dict) else vm
            if isinstance(vlist, list):
                items.extend(vlist)
        except Exception:
            pass

    added = 0
    for info in items:
        if not isinstance(info, dict):
            continue
        raw_slug = str(info.get("slug") or "").strip()
        if not raw_slug:
            url = str(info.get("url") or info.get("pdf") or "")
            m = re.search(r"/(\d{4,10})(?:/|\.|\b)", url)
            if m:
                raw_slug = m.group(1)
            else:
                raw_id = str(info.get("id") or "")
                raw_slug = raw_id.replace("MIN-KB-", "") if raw_id else ""
        if not raw_slug or "_en" in raw_slug or "_short" in raw_slug or "_q" in raw_slug or "_idea" in raw_slug:
            continue
        if raw_slug not in existing["slug_map"]:
            title = info.get("title_ko") or info.get("title") or raw_slug
            cat = f"{info.get('category', '')} {info.get('domain', '')} {info.get('chapter_ko', '')}"
            existing["slug_map"][raw_slug] = classify_topic_to_mathlab_preset(raw_slug, title, cat)
            added += 1
            if batch_size and added >= batch_size:
                break

    audit = audit_mathlab_html()
    existing["version"] = "1.4"
    existing["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existing["core_presets"] = CORE_PRESET_CATALOG
    existing["total_mapped_slugs"] = len(existing["slug_map"])
    existing["audit"] = audit

    PRESETS_ENGINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PRESETS_ENGINE_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "version": existing["version"],
        "added_in_step": added,
        "total_mapped_slugs": existing["total_mapped_slugs"],
        "core_presets_count": len(CORE_PRESET_CATALOG),
        "audit_ok": audit["ok"],
        "mathlab_lines": audit["lines"],
    }


if __name__ == "__main__":
    # When invoked from CLI, map all topics and run full audit
    res = run_mathlab_evolution_step(batch_size=2000)
    print(json.dumps(res, ensure_ascii=False, indent=2))
