#!/usr/bin/env python3
"""
build_seo_suite.py
Automated SEO, Sitemap, RSS Feed & Crawlers Generator for mathedu (min7014)
Fulfilling the vision of "Hongik Ingan" (弘益人間) - Spreading Open Math Education Far and Wide across the Globe.
"""

import os, glob, re, json, sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(REPO_DIR, 'board')
BASE_URL = 'https://min7014.github.io/mathedu'

def extract_meta_from_html(filepath):
    """Extract title, description, and keywords from HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else os.path.basename(filepath)
        
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        desc = desc_match.group(1).strip() if desc_match else "3,400+ 시각적 수학 증명과 초등부터 수능까지 이어지는 인터랙티브 디딤돌 퀴즈"
        
        return title, desc
    except Exception as e:
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

# Welcoming AI Educational Search & Citation Crawlers (GPTBot, ClaudeBot, PerplexityBot, CCBot)
User-agent: GPTBot
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

# XML Sitemap and Educational RSS Feed
Sitemap: https://min7014.github.io/mathedu/sitemap.xml
"""
    dest = os.path.join(REPO_DIR, 'robots.txt')
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ robots.txt generated successfully!")

def generate_sitemap_and_feed():
    """Scan all quiz pages and generate comprehensive sitemap.xml and feed.xml."""
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    now_rfc822 = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Collect all pages
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
            'desc': '전체 65개 수능·모의평가 디딤돌 퀴즈를 인터넷 연결 없이 다운로드하여 푸는 오프라인 패키지'
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
    
    # Collect all board/*.html quiz files
    board_files = glob.glob(os.path.join(BOARD_DIR, '*.html'))
    board_files.sort(key=lambda p: os.path.basename(p))
    
    quizzes = []
    for bf in board_files:
        filename = os.path.basename(bf)
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
        
    # Generate sitemap.xml
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

    # Generate feed.xml (RSS 2.0)
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
    for q in quizzes[:30]:
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
    print(f"✅ feed.xml (RSS) generated with top {min(30, len(quizzes))} quizzes!")

if __name__ == '__main__':
    generate_robots_txt()
    generate_sitemap_and_feed()
