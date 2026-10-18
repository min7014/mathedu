#!/usr/bin/env python3
"""
build_seo_suite.py
Automated SEO, Structured Data (Schema.org/Quiz), Sitemap, RSS Feed, & AI Search (llms.txt) Generator for mathedu (min7014)
Enables organic discovery via Google, Naver, Daum, Bing, and AI Search Engines without relying on SNS.
"""

import os, glob, re, json, sys, html
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(REPO_DIR, 'board')
BASE_URL = 'https://min7014.github.io/mathedu'


def strip_html(text):
    t = re.sub(r'<[^>]+>', ' ', text or '')
    t = re.sub(r'\s+', ' ', t).strip()
    return html.unescape(t)


def enrich_board_seo_meta(index_map):
    """Ensure every public board/*.html has rich SEO meta tags, canonical link, and Schema.org Quiz JSON-LD."""
    board_files = sorted(glob.glob(os.path.join(BOARD_DIR, '*.html')))
    enriched_count = 0

    for bf in board_files:
        filename = os.path.basename(bf)
        if filename.startswith('index'):
            continue
        slug = os.path.splitext(filename)[0]
        meta = index_map.get(slug, {})
        if meta.get('is_public') is False:
            continue

        with open(bf, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Korean title and lead description
        m_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
        page_title = strip_html(m_title.group(1)) if m_title else (meta.get('title') or slug)

        m_lead_ko = re.search(r'<p class="lead">\s*<span class="bilingual-ko">(.*?)</span>', content, re.DOTALL)
        if not m_lead_ko:
            m_lead_ko = re.search(r'<p class="lead">(.*?)</p>', content, re.DOTALL)
        lead_text = strip_html(m_lead_ko.group(1)) if m_lead_ko else ''

        exam_year = meta.get('examYear', '')
        month = meta.get('month', '')
        grade = meta.get('grade', '')
        subject = meta.get('subject', '')
        q_num = meta.get('qNum', '')
        source = meta.get('source', '')

        exam_prefix = ' '.join(filter(None, [
            f"{exam_year}학년도" if exam_year else "",
            f"{month} 모의평가" if month in ('6월', '9월') else (f"{month} 수능" if month == '11월' else month),
            grade,
            subject,
            f"{q_num}번" if q_num else ""
        ])).strip()

        short_exam = f"{exam_year} {month.replace('월', '모')} 수학 {q_num}번" if (exam_year and month and q_num) else exam_prefix

        desc_str = f"{exam_prefix + ' · ' if exam_prefix else ''}{meta.get('title', page_title)}. {lead_text} 초등 눈높이부터 시작하는 단계별 인터랙티브 디딤돌 퀴즈 & GeoGebra 시각적 증명 무료 풀이."
        desc_str = re.sub(r'\s+', ' ', desc_str).strip()[:220]

        kw_list = [
            exam_prefix,
            short_exam,
            f"{exam_prefix} 풀이" if exam_prefix else "",
            f"{exam_prefix} 해설" if exam_prefix else "",
            meta.get('title', ''),
            subject,
            source,
            "수능 수학 기출",
            "모의평가 수학 해설",
            "디딤돌 퀴즈",
            "GeoGebra",
            "수학자료실",
            "mathedu",
            "min7014"
        ]
        keywords_str = ', '.join(dict.fromkeys([k.strip() for k in kw_list if k and k.strip()]))
        canonical_url = f"{BASE_URL}/board/{filename}"

        # Build Schema.org Quiz + LearningResource JSON-LD
        schema_obj = {
            "@context": "https://schema.org",
            "@type": ["Quiz", "LearningResource"],
            "@id": canonical_url,
            "name": page_title,
            "description": desc_str,
            "url": canonical_url,
            "isAccessibleForFree": True,
            "inLanguage": ["ko", "en"],
            "learningResourceType": ["Quiz", "Interactive Step-by-Step Problem", "Visual Proof"],
            "educationalLevel": ["Elementary School", "Middle School", "High School"],
            "assesses": exam_prefix or page_title,
            "teaches": subject or "Mathematics",
            "author": {
                "@type": "Organization",
                "name": "mathedu · 수학자료실 (min7014)",
                "url": "https://min7014.github.io/mathedu/"
            },
            "publisher": {
                "@type": "EducationalOrganization",
                "name": "mathedu",
                "url": "https://min7014.github.io/mathedu/"
            }
        }
        schema_json = json.dumps(schema_obj, ensure_ascii=False)

        modified = False
        if '민은기' in content:
            content = content.replace('민은기 선생님의 수학자료실', '수학자료실').replace('민은기 수학자료실', '수학자료실')
            modified = True

        # 1. Inject meta description, keywords, canonical if missing
        if '<meta name="description"' not in content:
            esc_desc = html.escape(desc_str, quote=True)
            esc_kw = html.escape(keywords_str, quote=True)
            esc_title = html.escape(page_title, quote=True)
            seo_meta_block = (
                f'<meta name="description" content="{esc_desc}">\n'
                f'<meta name="keywords" content="{esc_kw}">\n'
                f'<meta name="author" content="mathedu">\n'
                f'<meta property="og:site_name" content="mathedu 수학자료실">\n'
                f'<meta property="og:type" content="article">\n'
                f'<meta property="og:title" content="{esc_title}">\n'
                f'<meta property="og:description" content="{esc_desc}">\n'
                f'<meta property="og:url" content="{canonical_url}">\n'
                f'<meta property="og:image" content="{BASE_URL}/assets/og-image.png">\n'
                f'<link rel="canonical" href="{canonical_url}">'
            )
            content = content.replace('</title>', f'</title>\n{seo_meta_block}', 1)
            modified = True

        # 2. Inject or update Schema.org Quiz JSON-LD
        schema_tag = f'<script type="application/ld+json" id="mathedu-seo-schema">{schema_json}</script>'
        if 'id="mathedu-seo-schema"' in content:
            new_c = re.sub(
                r'<script type="application/ld\+json" id="mathedu-seo-schema">.*?</script>',
                lambda _: schema_tag,
                content,
                flags=re.DOTALL
            )
            if new_c != content:
                content = new_c
                modified = True
        else:
            content = content.replace('<style>', f'{schema_tag}\n<style>', 1)
            modified = True

        if modified:
            with open(bf, 'w', encoding='utf-8') as f:
                f.write(content)
            enriched_count += 1

    print(f"✅ Enriched SEO meta tags & Schema.org/Quiz JSON-LD across {enriched_count} quiz pages!")


def extract_meta_from_html(filepath):
    """Extract title and description from HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = strip_html(title_match.group(1)) if title_match else os.path.basename(filepath)

        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        desc = strip_html(desc_match.group(1)) if desc_match else "3,400+ 시각적 수학 증명과 초등부터 수능까지 이어지는 인터랙티브 디딤돌 퀴즈"

        return title, desc
    except Exception:
        return os.path.basename(filepath), ""


def generate_robots_txt():
    """Generate robots.txt welcoming all standard crawlers and AI search engines."""
    content = """# ==============================================================================
# mathedu (min7014) Robots Exclusion Standard
# 弘益人間 (홍익인간) - 널리 세상을 이롭게 하는 100% 무료 열린 수학교육 자료실
# Open Educational Resource (OER) · Global Free Math Platform
# ==============================================================================

User-agent: *
Allow: /

# Welcoming Google, Bing, Naver, Daum, Baidu, Yandex, Apple, and international crawlers
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Yeti
Allow: /

User-agent: Daumoa
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: YandexBot
Allow: /

User-agent: Applebot
Allow: /

# Welcoming AI Educational Search & Citation Crawlers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, CCBot)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: facebookexternalhit
Allow: /

# XML Sitemap, RSS Feed, and AI Discovery Index (llms.txt)
Sitemap: https://min7014.github.io/mathedu/sitemap.xml
"""
    dest = os.path.join(REPO_DIR, 'robots.txt')
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ robots.txt generated successfully!")


def generate_sitemap_feed_and_llms(index_items):
    """Scan all quiz pages and generate comprehensive sitemap.xml, feed.xml, and llms.txt."""
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    now_rfc822 = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

    pub_items = [it for it in index_items if it.get('is_public') is not False]
    pub_count = len(pub_items)

    pages = [
        {
            'url': f'{BASE_URL}/',
            'priority': '1.0',
            'changefreq': 'daily',
            'title': 'mathedu · 시각적 수학 증명과 디딤돌 퀴즈 · 수학자료실 (min7014)',
            'desc': '3,400+ 시각적 기하·증명과 단계별 디딤돌 퀴즈를 담은 100% 영구 무료 수학자료실'
        },
        {
            'url': f'{BASE_URL}/offline/index.html',
            'priority': '0.9',
            'changefreq': 'weekly',
            'title': '📦 오프라인 보관함 · 인터넷 없이 풀 수 있는 단독 퀴즈 패키지',
            'desc': f'전체 {pub_count}개 수능·모의평가 디딤돌 퀴즈를 인터넷 연결 없이 다운로드하여 푸는 오프라인 패키지'
        },
        {
            'url': f'{BASE_URL}/dashboard.html',
            'priority': '0.8',
            'changefreq': 'daily',
            'title': '📊 실시간 교실 수업 대시보드 (stu1~ 익명 보호)',
            'desc': '교사용 3초 수업 개설, 대형 빔프로젝터 QR코드 및 실시간 학생 성취도 관제 현황판'
        },
        {
            'url': f'{BASE_URL}/privacy.html',
            'priority': '0.5',
            'changefreq': 'monthly',
            'title': '개인정보처리방침 및 학생 권익 보호 안내 · mathedu',
            'desc': '학생 실명 노출 방지(stu1~ 가명 처리) 및 안전한 교육 환경을 위한 개인정보 보호 정책'
        }
    ]

    board_files = sorted(glob.glob(os.path.join(BOARD_DIR, '*.html')))
    quizzes = []
    for bf in board_files:
        filename = os.path.basename(bf)
        if filename.startswith('index'):
            continue
        title, desc = extract_meta_from_html(bf)
        mod_time = datetime.fromtimestamp(os.path.getmtime(bf), timezone.utc).strftime('%Y-%m-%d')

        item = {
            'url': f'{BASE_URL}/board/{filename}',
            'priority': '0.85',
            'changefreq': 'weekly',
            'title': title,
            'desc': desc,
            'lastmod': mod_time,
            'slug': filename.replace('.html', '')
        }
        pages.append(item)
        quizzes.append(item)

    # 1. Generate sitemap.xml
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
    ]
    for p in pages:
        lastmod = p.get('lastmod', now_iso)
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{p["url"]}</loc>')
        sitemap_lines.append(f'    <lastmod>{lastmod}</lastmod>')
        sitemap_lines.append(f'    <changefreq>{p["changefreq"]}</changefreq>')
        sitemap_lines.append(f'    <priority>{p["priority"]}</priority>')
        sitemap_lines.append('  </url>')
    sitemap_lines.append('</urlset>')

    with open(os.path.join(REPO_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_lines))
    print(f"✅ sitemap.xml generated with {len(pages)} URLs!")

    # 2. Generate feed.xml (RSS 2.0) with all public quizzes
    feed_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '<channel>',
        '  <title>mathedu · 수학자료실 (min7014)</title>',
        '  <link>https://min7014.github.io/mathedu/</link>',
        '  <description>3,400+ 시각적 수학 증명과 초등부터 수능까지 이어지는 인터랙티브 디딤돌 퀴즈 · 100% 영구 무료 열린 수학교육</description>',
        '  <language>ko</language>',
        f'  <lastBuildDate>{now_rfc822}</lastBuildDate>',
        '  <atom:link href="https://min7014.github.io/mathedu/feed.xml" rel="self" type="application/rss+xml"/>'
    ]
    for q in quizzes:
        clean_title = q['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_desc = q['desc'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        feed_lines.append('  <item>')
        feed_lines.append(f'    <title>{clean_title}</title>')
        feed_lines.append(f'    <link>{q["url"]}</link>')
        feed_lines.append(f'    <guid isPermaLink="true">{q["url"]}</guid>')
        feed_lines.append(f'    <description>{clean_desc}</description>')
        feed_lines.append('  </item>')
    feed_lines.append('</channel>')
    feed_lines.append('</rss>')

    with open(os.path.join(REPO_DIR, 'feed.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(feed_lines))
    print(f"✅ feed.xml (RSS) generated with {len(quizzes)} quizzes!")

    # 3. Generate llms.txt (AI Search Engine Discovery Standard)
    llms_lines = [
        "# mathedu · 수학자료실 (Mathematics Archive & Interactive Scaffolding Quizzes)",
        "",
        "> 100% Free Open Educational Resource (OER) providing 3,400+ interactive GeoGebra visual proofs, PDF flipbooks, and elementary-to-CSAT step-by-step scaffolding math quizzes (Korean & English bilingual).",
        "",
        "## Core Hubs",
        f"- [Main Hub (Interactive Exam Problem Finder)]({BASE_URL}/): Search and solve {pub_count} official CSAT & KICE Mock Exam problems broken down into 5~8 elementary-to-advanced micro-steps.",
        "- [Mathematics Archive (min7014.github.io)](https://min7014.github.io/): 3,400+ GeoGebra dynamic geometry applets, visual proof PDFs, AlgeoMath, and video lectures.",
        f"- [Standalone Offline Quiz Archive]({BASE_URL}/offline/index.html): Single-file offline HTML bundles that work 100% without internet access.",
        f"- [Live Classroom Dashboard]({BASE_URL}/dashboard.html): Instant QR code classroom launch & privacy-preserving (stu1~) live progress dashboard for teachers.",
        "",
        f"## Interactive Scaffolding Quizzes ({pub_count} Official Exam Problems)",
    ]
    for it in pub_items:
        slug = it.get('slug', '')
        title = it.get('title', slug)
        meta_parts = [
            f"{it['examYear']}학년도" if it.get('examYear') else "",
            it.get('month', ''),
            it.get('grade', ''),
            it.get('subject', ''),
            f"{it['qNum']}번" if it.get('qNum') else ""
        ]
        meta_label = ' '.join(filter(None, meta_parts)).strip()
        prefix = f"[{meta_label}] " if meta_label else ""
        llms_lines.append(f"- [{prefix}{title}]({BASE_URL}/board/{slug}.html) | [Offline Bundle]({BASE_URL}/offline/{slug}.html)")

    with open(os.path.join(REPO_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(llms_lines) + '\n')
    print(f"✅ llms.txt generated with {pub_count} interactive exam problems!")


if __name__ == '__main__':
    index_json_path = os.path.join(BOARD_DIR, 'index.json')
    index_items = []
    index_map = {}
    if os.path.exists(index_json_path):
        with open(index_json_path, 'r', encoding='utf-8') as f:
            index_items = json.load(f)
            index_map = {it['slug']: it for it in index_items if 'slug' in it}

    enrich_board_seo_meta(index_map)
    generate_robots_txt()
    generate_sitemap_feed_and_llms(index_items)
