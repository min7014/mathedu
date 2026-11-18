#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_global_proof_pages.py — Policy 68 §3-② static English visual-proof pages.

Deterministic, offline, zero LLM calls, zero paid services (GitHub Pages static).

Inputs (read-only):
  video_lectures/scripts/*.json   (title_en, teacher_proof_analysis *_en,
                                   pages[].narrations.en, pdf_url, web_url,
                                   youtube / shorts / question / cinematic URLs)
Outputs (owned by this generator):
  en/index.html                   6-branch English topic hub
  en/proofs/{english-slug}/index.html
  en/assets/en.css                shared lightweight stylesheet
  sitemap-en.xml                  EN pages + ko<->en hreflang alternates
  llms-en.txt                     English AI-discovery index
Additive, idempotent patches (marker-guarded):
  sitemap.xml        -> adds the /en/ hub URL with hreflang alternates
  robots.txt         -> adds "Sitemap: .../sitemap-en.xml"
  video-sitemap.xml  -> moves English videos of published topics to their
                        canonical English page URL (KO videos stay on the KO URL)

QUALITY GATE (Policy 68 Red-Team #3, doorway / thin-content defence):
  A topic is published only if it has a clean English title AND at least
  MIN_SPECIFIC_UNITS narration passages that are genuinely topic-specific.
  "Specific" is decided mechanically: every passage is shingled (6-word
  windows) across the whole corpus; words covered by shingles that recur in
  >= COMMON_DF different topics are template boilerplate, title words and
  quoted title paraphrases are ignored, and the remaining "novel" words must
  reach MIN_NOVEL_WORDS per passage and MIN_TOTAL_NOVEL per topic.
  Passages containing Hangul, honorifics, external trademarks or non-math
  domain terms are discarded before scoring.

Usage:
  python -X utf8 build_global_proof_pages.py            # build + validate
  python -X utf8 build_global_proof_pages.py --validate # validate only
"""
from __future__ import annotations

import collections
import datetime as _dt
import html
import json
import re
import shutil
import sys
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "video_lectures" / "scripts"
EN_DIR = ROOT / "en"
PROOFS_DIR = EN_DIR / "proofs"
SITEMAP_EN = ROOT / "sitemap-en.xml"
SITEMAP_MAIN = ROOT / "sitemap.xml"
VIDEO_SITEMAP = ROOT / "video-sitemap.xml"
ROBOTS = ROOT / "robots.txt"
LLMS_EN = ROOT / "llms-en.txt"

SITE = "https://min7014.github.io/mathedu/"
EN_HUB_URL = SITE + "en/"
CHANNEL_URL = "https://www.youtube.com/@min7014_ai"
SITE_NAME = "MathEdu Visual Proofs"

COMMON_DF = 6            # shingle seen in >= this many topics -> boilerplate
SHINGLE = 6
MIN_NOVEL_WORDS = 8      # per passage
MIN_SPECIFIC_UNITS = 3   # passages per topic
MIN_TOTAL_NOVEL = 60     # novel words per topic
RELATED_N = 5

HANGUL_RE = re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7a3]")
CJK_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")

# Rule 51 / auditor.py L1 (mirrored so this generator stays self-contained)
FORBIDDEN_TRADEMARK_RE = re.compile(
    r"\bSAT\b|\bAP\s*Calculus\b|\bCollege\s*Board\b|\bAMC\s*(?:8|10|12|Math)?\b|\bAIME\b|"
    r"\bIB\s*Math\b|\bOlympiad\b|\bIMO\b|\bNano\s*Banana\b|\bGoogle\s*Flow\b|\bVeo\s*3(?:\.\d+)?\b|"
    r"\bGemini\b|\bProject\s*Genie\b|\bGenie\s*3\b|\bGoogle\s*Vids\b|\bNotebookLM\b|\bMusicFX\b|"
    r"\bLyria\b|\b3Blue1Brown\b|\bVeritasium\b|\bKurzgesagt\b|\bMindYourDecisions\b|"
    r"\bMathologer\b|\bDuolingo\b|\bWordle\b|\bNetflix\b|\bCSAT\b|\bKICE\b|\bSuneung\b",
    re.IGNORECASE,
)
# Rule 13.1 personal honorifics
HONORIFIC_RE = re.compile(r"Min\s*Eun[\s-]*ki|Eun[\s-]*gi\s*Min|Teacher\s+Min\b|Mr\.?\s*Min\b|"
                          r"Min's\s*Math\s*Lab|min7014\s*teacher", re.IGNORECASE)
# Rule 2 domain isolation
NON_MATH_RE = re.compile(r"\bcrypto|\bbitcoin|\bforex\b|\btrading\b|\binvest(?:ing|ment)\b|"
                         r"\bS-NOVA\b|\bstock market\b", re.IGNORECASE)
# Generic template sentences named in the brief / seen in the corpus
GENERIC_PHRASES = (
    "introduce a key auxiliary line or symmetric algebraic decomposition",
    "apply step-by-step congruence, similarity, area conservation, or algebraic equivalence",
    "the core mathematical invariant and theorem of",
    "given geometric and algebraic definitions and starting conditions",
    "rote memorization of the final formula breaks down",
    "what new theorem emerges if we generalize one condition",
)

STEP_PREFIX_RES = (
    re.compile(r"^\s*(?:this is (?:a |the )?)?(?:step\s*)?\d+[\s-]*steps?\s*,?\s*\d+[\s-]*pages?(?:\s*step)?\s*[.:,]\s*", re.I),
    re.compile(r"^\s*step\s*\d+\s*(?:\(\s*(?:page\s*\d+|final\s*step)\s*\)|,?\s*page\s*\d+)?\s*[.:,]\s*", re.I),
    re.compile(r"^\s*\(?\s*final\s*step\s*\)?\s*[.:,]\s*", re.I),
    re.compile(r"^\s*page\s*\d+\s*[.:,]\s*", re.I),
)

STOPWORDS = set("""a an the of and or to in on at by for from with as is are was were be been being this that these those
it its we us our you your they them their he she his her i me my mine so then thus there here which who whom whose what
when where why how not no yes can could will would should shall may might must do does did done have has had having
into onto over under than also very just only each every any all both either neither one two three first second
step steps page pages let lets let's now see look let us same such more most other another itself""".split())

# 6 universal branches (Policy 68 Step 2) keyed by sub_domain_ko
BRANCHES = [
    ("geometry", "Geometry",
     "Euclidean constructions, congruence, similarity, circles, transformations and dynamic-geometry tools."),
    ("conics-vectors", "Conics & Vectors",
     "Parabolas, ellipses, hyperbolas, vectors and solid (3D) geometry."),
    ("algebra-functions", "Algebra & Functions",
     "Polynomials, number systems, equations, inequalities, sets and function graphs."),
    ("exp-log-trig-sequences", "Exponentials, Logs, Trig & Sequences",
     "Exponents and logarithms, trigonometric ratios and functions, sequences and series."),
    ("limits-calculus", "Limits & Calculus",
     "Limits and continuity, derivatives, mean-value theorems and integration."),
    ("probability-modeling", "Probability & Modeling",
     "Counting, probability, statistics and mathematical modeling."),
]
SUBDOMAIN_MAP = {
    "유클리드 평면기하": ("geometry", "Euclidean Plane Geometry"),
    "기하 변환·대칭": ("geometry", "Geometric Transformations & Symmetry"),
    "해석기하·원의 방정식": ("geometry", "Analytic Geometry & Circles"),
    "수학공학도구(GeoGebra·AlgeoMath·TikZ)": ("geometry", "Dynamic Geometry Tools"),
    "수학 특강·공학도구": ("geometry", "Dynamic Geometry Tools"),
    "이차곡선·원뿔곡선": ("conics-vectors", "Conic Sections"),
    "벡터·공간도형": ("conics-vectors", "Vectors & Solid Geometry"),
    "다항식·방정식·수체계": ("algebra-functions", "Polynomials, Equations & Number Systems"),
    "방정식·부등식": ("algebra-functions", "Equations & Inequalities"),
    "함수·집합·그래프": ("algebra-functions", "Functions, Sets & Graphs"),
    "지수·로그": ("exp-log-trig-sequences", "Exponentials & Logarithms"),
    "삼각비·삼각함수": ("exp-log-trig-sequences", "Trigonometry"),
    "수열·시그마": ("exp-log-trig-sequences", "Sequences & Series"),
    "함수의 극한과 연속": ("limits-calculus", "Limits & Continuity"),
    "미분·도함수": ("limits-calculus", "Differential Calculus"),
    "적분·구분구적법": ("limits-calculus", "Integral Calculus"),
    "확률과 통계": ("probability-modeling", "Probability & Statistics"),
}
CATEGORY_FALLBACK = {
    "geometry": "geometry", "space_3d": "conics-vectors", "algebra": "algebra-functions",
    "number": "algebra-functions", "calculus_trig": "limits-calculus",
    "fractal_curve": "probability-modeling", "math_engineering_tools": "geometry",
}
BRANCH_NAME = {k: n for k, n, _ in BRANCHES}

ANALYSIS_FIELDS = (
    ("hypothesis_en", "Starting condition"),
    ("conclusion_en", "What we prove"),
    ("auxiliary_line_en", "Key idea"),
    ("proof_logic_en", "Proof logic"),
    ("misconception_en", "Common misconception"),
    ("what_if_not_en", "What if not?"),
)

VIDEO_FIELDS = (  # (script key, label, is_short) — English @min7014_ai uploads only
    ("youtube_urls", "Full visual-proof lecture", False),
    ("nano_banana_urls", "Cinematic visual-proof edition", False),
    ("question_youtube_urls", "Question-first classroom edition", False),
    ("shorts_urls", "Short: the proof idea in under a minute", True),
    ("nano_banana_shorts_urls", "Short: cinematic proof idea", True),
    ("question_shorts_urls", "Short: spot the clue first", True),
)
PACKAGE_FOR = {
    "youtube_urls": "youtube_packages", "nano_banana_urls": "nano_banana_packages",
    "question_youtube_urls": "question_classroom_packages", "shorts_urls": "shorts_packages",
    "nano_banana_shorts_urls": "nano_banana_packages", "question_shorts_urls": "question_shorts_packages",
}

SYMBOL_WORDS = {"α": " alpha ", "β": " beta ", "γ": " gamma ", "θ": " theta ", "π": " pi ", "∞": " infinity ",
                "≠": " ne ", "≤": " le ", "≥": " ge ", "√": " sqrt ", "∑": " sum ", "∫": " integral ",
                "△": " triangle ", "∠": " angle ", "⊥": " perpendicular ", "∥": " parallel ", "²": " squared "}


# ----------------------------------------------------------------------------- helpers
def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", (s or "").lower())


def strip_step_prefix(text: str) -> str:
    t = (text or "").strip()
    for _ in range(4):
        before = t
        for rx in STEP_PREFIX_RES:
            t = rx.sub("", t, count=1)
        if t == before:
            break
    t = re.sub(r"\s+", " ", t).strip()
    if t and t[0].islower():
        t = t[0].upper() + t[1:]
    return t


def is_clean_en(text: str) -> bool:
    if not text or HANGUL_RE.search(text) or CJK_RE.search(text):
        return False
    if FORBIDDEN_TRADEMARK_RE.search(text) or HONORIFIC_RE.search(text) or NON_MATH_RE.search(text):
        return False
    low = text.lower()
    if any(g in low for g in GENERIC_PHRASES):
        return False
    letters = sum(ch.isascii() and ch.isalpha() for ch in text)
    return letters >= 0.6 * max(1, sum(ch.isalpha() for ch in text))


def title_ok(t: str) -> bool:
    if not t or len(t) < 8 or len(words(t)) < 2:
        return False
    if HANGUL_RE.search(t) or CJK_RE.search(t):
        return False
    if FORBIDDEN_TRADEMARK_RE.search(t) or HONORIFIC_RE.search(t) or NON_MATH_RE.search(t):
        return False
    return True


def shingles(ws: list[str]) -> list[str]:
    return [" ".join(ws[i:i + SHINGLE]) for i in range(len(ws) - SHINGLE + 1)]


def unquoted(text: str) -> str:
    # drop quoted title paraphrases: 'like this' / "like this" / “like this”
    t = re.sub(r"'[^']{4,240}'", " ", text)
    t = re.sub(r"\"[^\"]{4,240}\"", " ", t)
    return re.sub(r"“[^”]{4,240}”", " ", t)


def novelty(text: str, title_words: set[str], df: collections.Counter) -> int:
    ws = words(text)
    covered = [False] * len(ws)
    for i, sh in enumerate(shingles(ws)):
        if df[sh] >= COMMON_DF:
            for j in range(i, i + SHINGLE):
                covered[j] = True
    common_words = {w for w, c in zip(ws, covered) if c}
    novel = 0
    for w in words(unquoted(text)):
        if w in common_words or w in title_words or w in STOPWORDS or len(w) < 2:
            continue
        novel += 1
    return novel


def slugify(title: str) -> str:
    t = title
    for k, v in SYMBOL_WORDS.items():
        t = t.replace(k, v)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    parts = [p for p in t.split("-") if p]
    out = []
    for p in parts:
        if len("-".join(out + [p])) > 70:
            break
        out.append(p)
    return "-".join(out) or "proof"


def yt_id(url: str) -> str:
    if not url:
        return ""
    m = re.search(r"(?:youtu\.be/|v=|/shorts/|/embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else ""


def truncate(text: str, n: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    cut = text[:n - 1]
    cut = cut[:cut.rfind(" ")] if " " in cut else cut
    return cut.rstrip(",;:-— ") + "…"


def iso_duration(sec) -> str:
    try:
        s = int(round(float(sec)))
    except (TypeError, ValueError):
        return ""
    if s <= 0:
        return ""
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + f"{s}S"


def ko_url(slug: str) -> str:
    return f"{SITE}video_board.html?slug={urllib.parse.quote(slug)}"


def en_url(eslug: str) -> str:
    return f"{SITE}en/proofs/{eslug}/"


def safe_url(u: str) -> str:
    u = (u or "").strip()
    return u if re.match(r"^https://[A-Za-z0-9.-]+/", u) else ""


# ----------------------------------------------------------------------------- corpus
def load_corpus() -> list[dict]:
    topics = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        try:
            d = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = str(d.get("slug") or sp.stem).strip()
        title_en = re.sub(r"\s+", " ", str(d.get("title_en") or "")).strip()
        units = collections.OrderedDict()   # body -> [pages]
        dropped = 0
        total = 0
        for p in d.get("pages") or []:
            raw = ((p.get("narrations") or {}).get("en") or "").strip()
            if not raw:
                continue
            total += 1
            body = strip_step_prefix(raw)
            if not is_clean_en(body) or len(words(body)) < 8:
                dropped += 1
                continue
            units.setdefault(body, []).append(int(p.get("page") or 0))
        tpa = d.get("teacher_proof_analysis") or {}
        analysis = {}
        for key, _ in ANALYSIS_FIELDS:
            v = re.sub(r"\s+", " ", str(tpa.get(key) or "")).strip()
            if v and is_clean_en(v):
                analysis[key] = v
        topics.append({
            "slug": slug, "title_en": title_en, "doc": d, "units": units, "analysis": analysis,
            "en_pages_total": total, "en_pages_dropped": dropped,
            "mtime": _dt.datetime.fromtimestamp(sp.stat().st_mtime, _dt.timezone.utc).date().isoformat(),
        })
    return topics


def build_df(topics: list[dict]) -> collections.Counter:
    df = collections.Counter()
    for t in topics:
        seen = set()
        for body in list(t["units"]) + list(t["analysis"].values()):
            seen.update(shingles(words(body)))
        df.update(seen)
    return df


def score_topics(topics: list[dict], df: collections.Counter) -> None:
    for t in topics:
        tw = set(words(t["title_en"]))
        spec = []
        for body, pages in t["units"].items():
            n = novelty(body, tw, df)
            if n < MIN_NOVEL_WORDS:
                continue
            sh = set(shingles(words(body)))
            twin = None
            for u in spec:  # merge near-duplicate passages inside the same topic
                inter = len(sh & u["sh"])
                if sh and u["sh"] and inter / min(len(sh), len(u["sh"])) >= 0.6:
                    twin = u
                    break
            if twin:
                twin["pages"] = twin["pages"] + pages
                continue
            spec.append({"text": body, "pages": pages, "novel": n, "sh": sh})
        spec.sort(key=lambda u: min(u["pages"]) if u["pages"] else 0)
        t["specific"] = spec
        t["novel_total"] = sum(u["novel"] for u in spec)
        t["analysis_specific"] = {k: v for k, v in t["analysis"].items()
                                  if novelty(v, tw, df) >= 5}
        if not t["title_en"]:
            t["skip"] = "no English title"
        elif not title_ok(t["title_en"]):
            t["skip"] = "English title contaminated (Hangul/trademark)"
        elif t["en_pages_total"] == 0:
            t["skip"] = "no English narration"
        elif len(spec) < MIN_SPECIFIC_UNITS or t["novel_total"] < MIN_TOTAL_NOVEL:
            if t["en_pages_total"] and t["en_pages_dropped"] > t["en_pages_total"] / 2:
                t["skip"] = "English narration mostly Korean-contaminated"
            else:
                t["skip"] = "English narration is generic template boilerplate"
        else:
            t["skip"] = ""


def branch_of(d: dict) -> tuple[str, str]:
    sd = str(d.get("sub_domain_ko") or "").strip()
    if sd in SUBDOMAIN_MAP:
        return SUBDOMAIN_MAP[sd]
    cat = str((d.get("teacher_proof_analysis") or {}).get("category_type") or "")
    b = CATEGORY_FALLBACK.get(cat, "geometry")
    return b, BRANCH_NAME[b]


def videos_of(d: dict) -> list[dict]:
    out, seen = [], set()
    for key, label, is_short in VIDEO_FIELDS:
        url = ((d.get(key) or {}).get("en") or "").strip()
        vid = yt_id(url)
        if not vid or vid in seen:
            continue
        seen.add(vid)
        pkg = (d.get(PACKAGE_FOR[key]) or {}).get("en") or {}
        pkg_vid = str(pkg.get("uploaded_video_id") or "")
        same = pkg_vid == vid
        dur = pkg.get("total_duration_sec") or pkg.get("duration_sec") or (
            pkg.get("short_duration_sec") if is_short else pkg.get("long_duration_sec"))
        out.append({
            "id": vid, "label": label, "short": is_short,
            "url": (f"https://www.youtube.com/shorts/{vid}" if is_short else f"https://www.youtube.com/watch?v={vid}"),
            "duration": iso_duration(dur) if same else "",
            "date": str(pkg.get("updated_at") or "")[:10] if same else "",
        })
    return out


# ----------------------------------------------------------------------------- HTML
CSS = """:root{--bg:#0f1420;--panel:#171e2e;--ink:#e8ecf4;--mute:#9aa6bd;--gold:#e9c46a;--teal:#2ec4b6;--line:#26304a}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.62 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--teal)}a:hover{color:var(--gold)}
.top{display:flex;flex-wrap:wrap;gap:.6rem 1.2rem;align-items:center;justify-content:space-between;padding:.8rem 1.2rem;border-bottom:1px solid var(--line);background:#0b101a}
.top .brand{font-weight:700;color:var(--ink);text-decoration:none;letter-spacing:.2px}.top nav a{margin-left:1rem;font-size:.92rem}
main{max-width:880px;margin:0 auto;padding:1.4rem 1.2rem 3rem}
.crumbs{font-size:.86rem;color:var(--mute);margin-bottom:.6rem}.crumbs a{color:var(--mute)}
h1{font-size:1.85rem;line-height:1.25;margin:.2rem 0 .5rem}h2{font-size:1.25rem;margin:2.1rem 0 .7rem;color:var(--gold)}
.lede{color:var(--mute);margin:0 0 1.2rem}
.actions{display:flex;flex-wrap:wrap;gap:.6rem}.btn{display:inline-block;padding:.55rem .95rem;border:1px solid var(--line);border-radius:10px;background:var(--panel);text-decoration:none;font-size:.95rem}
.btn.primary{border-color:var(--teal)}
dl.glance{display:grid;grid-template-columns:minmax(120px,190px) 1fr;gap:.5rem 1rem;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem}
dl.glance dt{color:var(--gold);font-weight:600}dl.glance dd{margin:0}
ol.steps{list-style:none;padding:0;margin:0;counter-reset:s}ol.steps li{border-left:3px solid var(--line);padding:.2rem 0 .9rem 1rem;margin-left:.3rem}
ol.steps .rng{display:inline-block;font-size:.8rem;color:var(--bg);background:var(--teal);border-radius:6px;padding:0 .45rem;margin-bottom:.25rem}
ol.steps p{margin:.2rem 0 0}
ul.plain{padding-left:1.1rem}ul.plain li{margin:.3rem 0}
.branch{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.4rem 1.1rem 1rem;margin:1.2rem 0}
.branch h2{margin-top:.8rem}.branch p.desc{color:var(--mute);margin:.1rem 0 .6rem}
.tag{font-size:.78rem;color:var(--mute);margin-left:.35rem}
.map{display:flex;flex-wrap:wrap;gap:.5rem;margin:.6rem 0 0}
footer{border-top:1px solid var(--line);color:var(--mute);font-size:.86rem;padding:1.2rem;text-align:center}
@media (max-width:600px){h1{font-size:1.45rem}dl.glance{grid-template-columns:1fr}.top nav a{margin-left:0;margin-right:.9rem}}
"""


def head(title: str, desc: str, canonical: str, ko: str, css_rel: str, jsonld: list, og_image: str = "") -> str:
    ld = json.dumps(jsonld if len(jsonld) > 1 else jsonld[0], ensure_ascii=False, indent=1)
    ld = ld.replace("</", "<\\/")
    og_img = f'\n<meta property="og:image" content="{esc(og_image)}">' if og_image else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(canonical)}">
<link rel="alternate" hreflang="ko" href="{esc(ko)}">
<link rel="alternate" hreflang="x-default" href="{esc(canonical)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">{og_img}
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{css_rel}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header class="top"><a class="brand" href="{css_rel.replace('assets/en.css', '')}">{esc(SITE_NAME)}</a>
<nav><a href="{css_rel.replace('assets/en.css', '')}">All proofs</a><a href="{esc(ko)}" hreflang="ko">Korean version</a><a href="{CHANNEL_URL}" target="_blank" rel="noopener">YouTube channel</a></nav></header>
"""


FOOTER = """<footer>Free open educational resource for secondary-school students, teachers and adult learners.
Every proof is based on the original step-by-step visual proof published at <a href="https://min7014.github.io/" target="_blank" rel="noopener">min7014.github.io</a>.
Videos open on YouTube in a new tab.</footer>
</body>
</html>
"""


def step_range(pages: list[int]) -> str:
    if not pages:
        return ""
    ps = sorted(set(pages))
    run_end = ps[0]
    for p in ps[1:]:
        if p == run_end + 1:
            run_end = p
        else:
            break
    return f"Step {ps[0]}" if run_end == ps[0] else f"Steps {ps[0]}–{run_end}"


def render_proof(t: dict, related: list[dict]) -> str:
    d = t["doc"]
    slug, eslug, title = t["slug"], t["eslug"], t["title_en"]
    url, ko = en_url(eslug), ko_url(slug)
    bkey, bsub = t["branch"], t["sub_en"]
    bname = BRANCH_NAME[bkey]
    n_steps = int(d.get("page_count") or len(d.get("pages") or []) or 0)
    page_title = t["page_title"]
    desc = t["description"]
    pdf = safe_url(d.get("pdf_url") or "")
    web = safe_url(d.get("web_url") or "")
    mathlab = f"../../../mathlab.html?slug={urllib.parse.quote(slug)}&lang=en"
    board = f"../../../video_board.html?slug={urllib.parse.quote(slug)}&lang=en&from=en"
    vids = t["videos"]

    lr = {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": title, "headline": page_title, "description": desc, "url": url, "inLanguage": "en",
        "learningResourceType": "Visual proof", "educationalLevel": "Secondary school",
        "isAccessibleForFree": True, "teaches": title,
        "audience": {"@type": "EducationalAudience", "educationalRole": ["student", "teacher"]},
        "about": [bname, bsub],
        "numberOfSteps": n_steps or None,
        "isPartOf": {"@type": "CollectionPage", "name": "Step-by-Step Visual Math Proofs", "url": EN_HUB_URL},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE},
        "dateModified": t["mtime"],
    }
    if pdf:
        lr["isBasedOn"] = pdf
    if not lr["numberOfSteps"]:
        del lr["numberOfSteps"]
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Visual Proofs", "item": EN_HUB_URL},
            {"@type": "ListItem", "position": 2, "name": bname, "item": f"{EN_HUB_URL}#{bkey}"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    }
    jsonld = [lr, crumbs]
    og_image = ""
    if vids:
        v = vids[0]
        og_image = f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"
        vo = {
            "@context": "https://schema.org", "@type": "VideoObject",
            "name": truncate(f"{title} — Visual Proof", 100),
            "description": desc, "thumbnailUrl": [og_image], "contentUrl": v["url"],
            "inLanguage": "en", "isFamilyFriendly": True,
        }
        if v["date"]:
            vo["uploadDate"] = v["date"]
        if v["duration"]:
            vo["duration"] = v["duration"]
        lr["video"] = {"@type": "VideoObject", "url": v["url"]}
        jsonld.append(vo)

    out = [head(page_title, desc, url, ko, "../../assets/en.css", jsonld, og_image)]
    out.append("<main>\n")
    out.append(f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Visual Proofs</a> › '
               f'<a href="../../#{bkey}">{esc(bname)}</a> › {esc(truncate(title, 60))}</nav>\n')
    out.append(f"<h1>{esc(title)}</h1>\n")
    lede = f"{n_steps}-step visual proof · {esc(bname)} · {esc(bsub)}" if n_steps else f"Visual proof · {esc(bname)} · {esc(bsub)}"
    out.append(f'<p class="lede">{lede}</p>\n')
    out.append('<div class="actions">\n')
    if pdf:
        out.append(f'<a class="btn primary" href="{esc(pdf)}" target="_blank" rel="noopener">Original step-by-step proof (PDF)</a>\n')
    out.append(f'<a class="btn" href="{esc(mathlab)}">Construct it in MathLab</a>\n')
    out.append(f'<a class="btn" href="{esc(board)}">Split-screen study board</a>\n')
    if web:
        out.append(f'<a class="btn" href="{esc(web)}" target="_blank" rel="noopener">Source page &amp; applets</a>\n')
    out.append("</div>\n")

    if t["analysis_specific"]:
        out.append("<h2>Proof at a glance</h2>\n<dl class=\"glance\">\n")
        for key, label in ANALYSIS_FIELDS:
            v = t["analysis_specific"].get(key)
            if v:
                out.append(f"<dt>{esc(label)}</dt><dd>{esc(v)}</dd>\n")
        out.append("</dl>\n")

    out.append("<h2>Step-by-step walkthrough</h2>\n<ol class=\"steps\">\n")
    for u in t["specific"]:
        rng = step_range(u["pages"])
        rng_html = f'<span class="rng">{esc(rng)}</span>' if rng else ""
        out.append(f"<li>{rng_html}<p>{esc(u['text'])}</p></li>\n")
    out.append("</ol>\n")
    if pdf:
        out.append(f'<p>Follow every step with its figure in the <a href="{esc(pdf)}" target="_blank" rel="noopener">original proof PDF</a>, '
                   f'then rebuild the figure yourself in <a href="{esc(mathlab)}">MathLab</a>.</p>\n')

    if vids:
        out.append("<h2>Watch on YouTube</h2>\n<ul class=\"plain\">\n")
        for v in vids:
            out.append(f'<li><a href="{esc(v["url"])}" target="_blank" rel="noopener">{esc(v["label"])}</a></li>\n')
        out.append("</ul>\n")

    if related:
        out.append(f"<h2>More {esc(bname)} proofs</h2>\n<ul class=\"plain\">\n")
        for r in related:
            out.append(f'<li><a href="../{esc(r["eslug"])}/">{esc(r["title_en"])}</a></li>\n')
        out.append("</ul>\n")
    out.append("</main>\n")
    out.append(FOOTER)
    return "".join(out)


def render_hub(pub: list[dict]) -> str:
    by_branch = collections.defaultdict(list)
    for t in pub:
        by_branch[t["branch"]].append(t)
    for k in by_branch:
        by_branch[k].sort(key=lambda x: (x["sub_en"], x["title_en"].lower()))
    title = "Step-by-Step Visual Math Proofs — 6-Branch Topic Map"
    desc = (f"{len(pub)} free step-by-step visual math proofs in English, organized into six branches: geometry, "
            f"conics and vectors, algebra, exponentials/logs/trig/sequences, calculus, and probability.")
    item_list = {
        "@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc,
        "url": EN_HUB_URL, "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE},
        "mainEntity": {"@type": "ItemList", "numberOfItems": len(pub), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": en_url(t["eslug"]), "name": t["title_en"]}
            for i, t in enumerate(sorted(pub, key=lambda x: x["eslug"]))]},
    }
    out = [head(title, desc, EN_HUB_URL, SITE, "assets/en.css", [item_list])]
    out.append("<main>\n<h1>Step-by-Step Visual Math Proofs</h1>\n")
    out.append(f'<p class="lede">{len(pub)} proofs that show <em>why</em> a theorem must be true, one figure at a time. '
               "Read the walkthrough, open the original proof figures, then construct it yourself in MathLab.</p>\n")
    out.append('<nav class="map" aria-label="Topic map">\n')
    for k, name, _ in BRANCHES:
        out.append(f'<a class="btn" href="#{k}">{esc(name)} <span class="tag">{len(by_branch.get(k, []))}</span></a>\n')
    out.append("</nav>\n")
    for k, name, blurb in BRANCHES:
        items = by_branch.get(k, [])
        out.append(f'<section class="branch" id="{k}">\n<h2>{esc(name)}</h2>\n<p class="desc">{esc(blurb)}</p>\n')
        if not items:
            out.append("<p>English proofs for this branch are being prepared.</p>\n")
        else:
            out.append('<ul class="plain">\n')
            for t in items:
                tag = " ▶" if t["videos"] else ""
                out.append(f'<li><a href="proofs/{esc(t["eslug"])}/">{esc(t["title_en"])}</a>'
                           f'<span class="tag">{esc(t["sub_en"])}{tag}</span></li>\n')
            out.append("</ul>\n")
        out.append("</section>\n")
    out.append(f'<p>Prefer video? Every lecture is on <a href="{CHANNEL_URL}" target="_blank" rel="noopener">our YouTube channel</a> '
               '(▶ marks proofs with an English video).</p>\n</main>\n')
    out.append(FOOTER.replace('<footer>', '<footer>'))
    return "".join(out)


# ----------------------------------------------------------------------------- XML / txt
XHTML_NS = "http://www.w3.org/1999/xhtml"


def build_sitemap_en(pub: list[dict], hub_lastmod: str) -> str:
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']

    def entry(loc, en, ko, lastmod, prio):
        L.append("  <url>")
        L.append(f"    <loc>{esc(loc)}</loc>")
        L.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{esc(en)}"/>')
        L.append(f'    <xhtml:link rel="alternate" hreflang="ko" href="{esc(ko)}"/>')
        L.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{esc(en)}"/>')
        L.append(f"    <lastmod>{lastmod}</lastmod>")
        L.append(f"    <priority>{prio}</priority>")
        L.append("  </url>")

    entry(EN_HUB_URL, EN_HUB_URL, SITE, hub_lastmod, "0.9")
    for t in sorted(pub, key=lambda x: x["eslug"]):
        e, k = en_url(t["eslug"]), ko_url(t["slug"])
        entry(e, e, k, t["mtime"], "0.8")
        entry(k, e, k, t["mtime"], "0.6")   # reciprocal ko->en annotation (KO page itself is not editable here)
    L.append("</urlset>")
    return "\n".join(L) + "\n"


def build_llms_en(pub: list[dict]) -> str:
    by_branch = collections.defaultdict(list)
    for t in pub:
        by_branch[t["branch"]].append(t)
    L = ["# MathEdu — Step-by-Step Visual Math Proofs (English)", "",
         "> Free open educational resource. Each page explains why a theorem holds through a numbered sequence of "
         "figures, links the original step-by-step proof PDF, an interactive MathLab construction, and English "
         "YouTube lectures where available. Audience: secondary-school students, teachers and adult learners.", "",
         "## Hubs",
         f"- [English topic map (6 branches)]({EN_HUB_URL}): all English visual-proof pages grouped by branch.",
         f"- [Interactive MathLab]({SITE}mathlab.html?lang=en): dynamic geometry and function plotting.",
         f"- [Original proof archive](https://min7014.github.io/): source PDFs and dynamic-geometry applets.",
         f"- [YouTube channel]({CHANNEL_URL}): video lectures and shorts.",
         f"- [English sitemap]({SITE}sitemap-en.xml)", ""]
    for k, name, blurb in BRANCHES:
        items = sorted(by_branch.get(k, []), key=lambda x: x["title_en"].lower())
        if not items:
            continue
        L.append(f"## {name}")
        L.append(f"{blurb}")
        for t in items:
            L.append(f"- [{t['title_en']}]({en_url(t['eslug'])}): {truncate(t['description'], 150)}")
        L.append("")
    return "\n".join(L).rstrip() + "\n"


SITEMAP_MARK_BEGIN = "<!-- en-hub:begin (build_global_proof_pages.py) -->"
SITEMAP_MARK_END = "<!-- en-hub:end -->"


def patch_sitemap_main(hub_lastmod: str) -> str:
    if not SITEMAP_MAIN.exists():
        return "sitemap.xml missing (skipped)"
    s = SITEMAP_MAIN.read_text(encoding="utf-8")
    s = re.sub(r"[ \t]*" + re.escape(SITEMAP_MARK_BEGIN) + r".*?" + re.escape(SITEMAP_MARK_END) + r"[ \t]*\n?", "", s, flags=re.S)
    if 'xmlns:xhtml=' not in s:
        s = s.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:xhtml="http://www.w3.org/1999/xhtml"', 1)
    block = (f"  {SITEMAP_MARK_BEGIN}\n  <url>\n    <loc>{EN_HUB_URL}</loc>\n"
             f'    <xhtml:link rel="alternate" hreflang="en" href="{EN_HUB_URL}"/>\n'
             f'    <xhtml:link rel="alternate" hreflang="ko" href="{SITE}"/>\n'
             f'    <xhtml:link rel="alternate" hreflang="x-default" href="{EN_HUB_URL}"/>\n'
             f"    <lastmod>{hub_lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n"
             f"  </url>\n  {SITEMAP_MARK_END}\n")
    idx = s.rfind("</urlset>")
    s = s[:idx] + block + s[idx:]
    SITEMAP_MAIN.write_text(s, encoding="utf-8")
    return "sitemap.xml: /en/ hub URL + hreflang alternates (marker block)"


def patch_robots() -> str:
    if not ROBOTS.exists():
        return "robots.txt missing (skipped)"
    raw = ROBOTS.read_bytes()
    line = "Sitemap: https://min7014.github.io/mathedu/sitemap-en.xml"
    if line.encode() in raw:
        return "robots.txt: already lists sitemap-en.xml"
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    ROBOTS.write_bytes(raw.rstrip() + nl + line.encode() + nl)
    return "robots.txt: added sitemap-en.xml"


def patch_video_sitemap(pub: list[dict], all_topics: list[dict] | None = None) -> str:
    """Move English videos of published topics onto the canonical EN page URL (idempotent).
    Videos sitting on an /en/ URL that is no longer published are moved back to their KO URL."""
    if not VIDEO_SITEMAP.exists():
        return "video-sitemap.xml missing (skipped)"
    en_ids = {}
    for t in pub:
        for v in t["videos"]:
            en_ids[v["id"]] = en_url(t["eslug"])
    vid_slug = {}
    for t in all_topics or []:
        for v in videos_of(t["doc"]):
            vid_slug.setdefault(v["id"], t["slug"])
    valid_en = set(en_ids.values())
    NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    VNS = "http://www.google.com/schemas/sitemap-video/1.1"
    ET.register_namespace("", NS)
    ET.register_namespace("video", VNS)
    tree = ET.parse(VIDEO_SITEMAP)
    root = tree.getroot()
    moved = 0
    new_urls: dict[str, ET.Element] = {}
    for u in list(root.findall(f"{{{NS}}}url")):
        loc = (u.findtext(f"{{{NS}}}loc") or "").strip()
        new_urls.setdefault(loc, u)
    for u in list(root.findall(f"{{{NS}}}url")):
        loc = (u.findtext(f"{{{NS}}}loc") or "").strip()
        is_en = loc.startswith(SITE + "en/")
        if is_en and loc in valid_en:
            continue
        for v in list(u.findall(f"{{{VNS}}}video")):
            vid = yt_id(v.findtext(f"{{{VNS}}}content_loc") or "")
            target = en_ids.get(vid)
            if not target and is_en and vid in vid_slug:
                target = ko_url(vid_slug[vid])
            if not target or target == loc:
                continue
            dest = new_urls.get(target)
            if dest is None:
                dest = ET.SubElement(root, f"{{{NS}}}url")
                ET.SubElement(dest, f"{{{NS}}}loc").text = target
                new_urls[target] = dest
            u.remove(v)
            dest.append(v)
            moved += 1
        if not u.findall(f"{{{VNS}}}video"):
            root.remove(u)
            new_urls.pop(loc, None)
    ET.indent(tree, space="  ")
    tree.write(VIDEO_SITEMAP, encoding="UTF-8", xml_declaration=True)
    txt = VIDEO_SITEMAP.read_text(encoding="utf-8").replace("<?xml version='1.0' encoding='UTF-8'?>",
                                                             '<?xml version="1.0" encoding="UTF-8"?>')
    VIDEO_SITEMAP.write_text(txt.rstrip() + "\n", encoding="utf-8")
    return f"video-sitemap.xml: {moved} English video entries re-pointed to /en/proofs/ canonical URLs"


# ----------------------------------------------------------------------------- validation
class _Visible(__import__("html.parser").parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.text = []
        self.tags = collections.Counter()
        self.attr_hangul = []

    def handle_starttag(self, tag, attrs):
        self.tags[tag] += 1
        if tag in ("script", "style"):
            self.skip += 1
        for k, v in attrs:
            if k in ("alt", "title", "content", "aria-label") and v and HANGUL_RE.search(v):
                self.attr_hangul.append(v)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def validate() -> dict:
    problems = []
    pages = sorted(PROOFS_DIR.glob("*/index.html"))
    files = pages + ([EN_DIR / "index.html"] if (EN_DIR / "index.html").exists() else [])
    titles, descs = collections.Counter(), collections.Counter()
    max_kb = 0
    for f in files:
        s = f.read_text(encoding="utf-8")
        max_kb = max(max_kb, len(s.encode("utf-8")) // 1024)
        p = _Visible()
        p.feed(s)
        vis = " ".join(p.text)
        rel = f.relative_to(ROOT).as_posix()
        if p.tags["iframe"] or p.tags["video"] or p.tags["embed"] or p.tags["object"]:
            problems.append(f"{rel}: iframe/video/embed tag")
        if HANGUL_RE.search(vis) or p.attr_hangul:
            problems.append(f"{rel}: Hangul in visible text/attributes")
        if FORBIDDEN_TRADEMARK_RE.search(vis) or HONORIFIC_RE.search(vis) or NON_MATH_RE.search(vis):
            problems.append(f"{rel}: forbidden trademark/honorific/non-math term")
        if '<html lang="en">' not in s:
            problems.append(f"{rel}: missing html lang=en")
        for need in ('rel="canonical"', 'hreflang="en"', 'hreflang="ko"', 'hreflang="x-default"', "application/ld+json"):
            if need not in s:
                problems.append(f"{rel}: missing {need}")
        for m in re.finditer(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                problems.append(f"{rel}: JSON-LD invalid ({e})")
        tm = re.search(r"<title>(.*?)</title>", s, re.S)
        dm = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
        titles[tm.group(1) if tm else ""] += 1
        descs[dm.group(1) if dm else ""] += 1
        for a in re.finditer(r'<a [^>]*href="(https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^"]*)"[^>]*>', s):
            if 'target="_blank"' not in a.group(0):
                problems.append(f"{rel}: YouTube link without target=_blank")
    for k, c in titles.items():
        if c > 1:
            problems.append(f"duplicate <title> x{c}: {k[:80]}")
    for k, c in descs.items():
        if c > 1:
            problems.append(f"duplicate meta description x{c}: {k[:80]}")
    for x in (SITEMAP_EN, SITEMAP_MAIN, VIDEO_SITEMAP):
        if x.exists():
            try:
                ET.parse(x)
            except ET.ParseError as e:
                problems.append(f"{x.name}: XML not well-formed ({e})")
                continue
            for loc in re.findall(r"<loc>(https://min7014\.github\.io/mathedu/en/[^<]*)</loc>", x.read_text(encoding="utf-8")):
                relp = loc[len(SITE):]
                if not (ROOT / relp / "index.html").exists():
                    problems.append(f"{x.name}: dangling EN URL {loc}")
    if LLMS_EN.exists() and HANGUL_RE.search(LLMS_EN.read_text(encoding="utf-8")):
        problems.append("llms-en.txt: Hangul present")
    return {"pages": len(pages), "files_checked": len(files), "max_page_kb": max_kb, "problems": problems}


# ----------------------------------------------------------------------------- main
def build() -> dict:
    topics = load_corpus()
    df = build_df(topics)
    score_topics(topics, df)
    pub = [t for t in topics if not t["skip"]]

    # same English title published twice (re-edited lecture): keep only the richer one (anti-duplicate)
    best = {}
    tkey = lambda t: slugify(unicodedata.normalize("NFKC", t["title_en"]))  # noqa: E731
    for t in pub:
        key = tkey(t)
        if key not in best or (t["novel_total"], t["slug"]) > (best[key]["novel_total"], best[key]["slug"]):
            best[key] = t
    for t in pub:
        b = best[tkey(t)]
        if b is not t:
            t["skip"] = "duplicate English title of " + b["slug"]
    pub = [t for t in pub if not t["skip"]]

    used = set()
    title_count = collections.Counter(t["title_en"].lower() for t in pub)
    for t in pub:
        t["branch"], t["sub_en"] = branch_of(t["doc"])
        base = slugify(t["title_en"])
        toks = base.split("-")
        if len(toks) < 2 or sum(len(x) <= 1 for x in toks) / len(toks) > 0.4:
            base = f"{slugify(t['sub_en'])}-{t['slug']}"   # formula-only title -> readable, stable slug
        es = base if base not in used else f"{base}-{t['slug']}"
        used.add(es)
        t["eslug"] = es
        t["videos"] = videos_of(t["doc"])
        suffix = "" if "proof" in t["title_en"].lower() else " — Visual Proof"
        pt = f"{t['title_en']}{suffix}"
        if title_count[t["title_en"].lower()] > 1:
            pt += f" ({int(t['doc'].get('page_count') or 0)} steps)"
        t["page_title"] = pt
        lead = t["specific"][0]["text"]
        t["description"] = truncate(f"{t['title_en']}: {lead}" if t["title_en"].lower()[:30] not in lead.lower() else lead, 158)

    # unique descriptions guard
    dc = collections.Counter(t["description"] for t in pub)
    for t in pub:
        if dc[t["description"]] > 1:
            t["description"] = truncate(f"{t['title_en']} ({t['slug']}): {t['specific'][0]['text']}", 158)

    # clean output tree (owned)
    if PROOFS_DIR.exists():
        shutil.rmtree(PROOFS_DIR)
    (EN_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (EN_DIR / "assets" / "en.css").write_text(CSS, encoding="utf-8")

    by_branch = collections.defaultdict(list)
    for t in sorted(pub, key=lambda x: x["slug"]):
        by_branch[t["branch"]].append(t)
    for t in pub:
        peers = by_branch[t["branch"]]
        i = peers.index(t)
        rel = [p for p in (peers[i + 1:] + peers[:i]) if p is not t][:RELATED_N]
        out = PROOFS_DIR / t["eslug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_proof(t, rel), encoding="utf-8")

    hub_lastmod = max((t["mtime"] for t in pub), default=_dt.date.today().isoformat())
    (EN_DIR / "index.html").write_text(render_hub(pub), encoding="utf-8")
    SITEMAP_EN.write_text(build_sitemap_en(pub, hub_lastmod), encoding="utf-8")
    LLMS_EN.write_text(build_llms_en(pub), encoding="utf-8")
    patches = [patch_sitemap_main(hub_lastmod), patch_robots(), patch_video_sitemap(pub, topics)]

    skipped = collections.Counter(t["skip"].split(" of ")[0] for t in topics if t["skip"])
    return {
        "scripts": len(topics), "published": len(pub), "skipped": sum(skipped.values()),
        "skip_reasons": dict(skipped.most_common()),
        "with_video": sum(1 for t in pub if t["videos"]),
        "by_branch": {BRANCH_NAME[k]: len(v) for k, v in by_branch.items()},
        "patches": patches,
        "samples": [en_url(t["eslug"]) for t in sorted(pub, key=lambda x: -x["novel_total"])[:3]],
    }


def main(argv: list[str]) -> int:
    if "--validate" not in argv:
        rep = build()
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    val = validate()
    print(json.dumps({k: (v if k != "problems" else v[:40]) for k, v in val.items()}, ensure_ascii=False, indent=2))
    print("VALIDATION:", "PASS" if not val["problems"] else f"FAIL ({len(val['problems'])} problems)")
    return 0 if not val["problems"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
