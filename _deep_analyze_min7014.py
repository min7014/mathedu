import urllib.request
import re
import json
import os

def clean_text(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def deep_analyze():
    print("Fetching master content index from https://min7014.github.io/2019080802.html...")
    req = urllib.request.Request('https://min7014.github.io/2019080802.html', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    print(f"Loaded master index: {len(html)} bytes, {len(html.splitlines())} lines")

    # We need to track category hierarchy as we parse.
    # In min7014's HTML, categories are structured with:
    # <details><summary>CategoryName<a href="...">...</a></summary>
    #   <ul><li>...items...</li></ul>
    # </details>

    # Let's write an accurate parser that walks through tokens:
    # <summary>, </summary>, <li>, </li>, <details>, </details>
    
    materials_by_url = {}
    category_stack = []
    
    # Token regex
    token_pattern = re.compile(r'(<details[^>]*>|<summary[^>]*>.*?</summary>|</details>|<li>.*?</li>)', re.DOTALL | re.IGNORECASE)
    
    for match in token_pattern.finditer(html):
        token = match.group(1)
        token_lower = token.lower()
        
        if token_lower.startswith('<details'):
            pass
        elif token_lower.startswith('<summary'):
            # Extract category title
            m = re.search(r'<summary[^>]*>(.*?)</summary>', token, re.DOTALL | re.IGNORECASE)
            if m:
                cat_raw = m.group(1)
                # Remove nested <a> tags like [고유주소]
                cat_title = re.sub(r'<a[^>]*>.*?</a>', '', cat_raw)
                cat_title = clean_text(cat_title)
                # English subtitle split
                category_stack.append(cat_title)
        elif token_lower.startswith('</details>'):
            if category_stack:
                category_stack.pop()
        elif token_lower.startswith('<li>'):
            # Parse list item
            # Find math URL
            math_m = re.search(r'<a\s+href=[\'"](https://min7014\.github\.io/math\d+\.html)[\'"][^>]*>(.*?)</a>', token, re.DOTALL)
            if not math_m:
                continue
                
            math_url = math_m.group(1).strip()
            raw_title = clean_text(math_m.group(2))
            
            if not raw_title or any(k in raw_title for k in ['[고유주소]', '수학자료실']):
                continue
                
            # Extract PDF
            pdf_m = re.search(r'href=[\'"](https://min7014\.github\.io/[^\'"]+\.pdf[^\'"]*)[\'"]', token)
            pdf = pdf_m.group(1) if pdf_m else ''
            
            # Extract YouTube
            yt_m = re.findall(r'href=[\'"](https://(?:youtu\.be|www\.youtube\.com)[^\'"]+)[\'"]', token)
            yt = yt_m[0] if yt_m else ''
            
            # Extract GeoGebra Tube
            ggb_m = re.search(r'href=[\'"](https://www\.geogebra\.org/[^\'"]+)[\'"]', token)
            geogebra = ggb_m.group(1) if ggb_m else ''
            
            # Extract AlgeoMath
            algeo_m = re.search(r'href=[\'"](https?://[^\'"]*(?:algeomath|me2\.do)[^\'"]*)[\'"]', token)
            algeomath = algeo_m.group(1) if algeo_m else ''
            
            # Current breadcrumb category
            current_cats = [c for c in category_stack if c]
            
            # Extract tags from title and category
            tags = list(current_cats)
            for kw in ['삼각함수', '코사인', '사인', '탄젠트', '미분', '도함수', '접선', '적분', '극한', '연속', '이차곡선', '포물선', '타원', '쌍곡선', '단델린', '수열', '등차', '등비', '확률', '통계', '벡터', '기하', '작도']:
                if (kw in raw_title or any(kw in c for c in current_cats)) and kw not in tags:
                    tags.append(kw)
            
            if math_url not in materials_by_url:
                materials_by_url[math_url] = {
                    'title': raw_title,
                    'url': math_url,
                    'pdf': pdf,
                    'youtube': yt,
                    'geogebra': geogebra,
                    'algeomath': algeomath,
                    'category': " > ".join(current_cats[-2:]) if current_cats else "일반 수학",
                    'tags': tags
                }
            else:
                existing = materials_by_url[math_url]
                if not existing['pdf'] and pdf:
                    existing['pdf'] = pdf
                if not existing['youtube'] and yt:
                    existing['youtube'] = yt
                if not existing['geogebra'] and geogebra:
                    existing['geogebra'] = geogebra
                if not existing['algeomath'] and algeomath:
                    existing['algeomath'] = algeomath
                if current_cats:
                    existing['category'] = " > ".join(current_cats[-2:])
                for t in tags:
                    if t not in existing['tags']:
                        existing['tags'].append(t)

    print(f"Extracted {len(materials_by_url)} rich materials with categories.")
    
    # Also merge with any existing materials from assets/min7014_materials.json
    existing_path = os.path.join('assets', 'min7014_materials.json')
    if os.path.exists(existing_path):
        with open(existing_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        print(f"Existing materials count in {existing_path}: {len(old_data)}")
        for old_item in old_data:
            u = old_item.get('url')
            if not u:
                continue
            if u not in materials_by_url:
                materials_by_url[u] = old_item
            else:
                cur = materials_by_url[u]
                if not cur.get('geogebra') and old_item.get('geogebra'):
                    cur['geogebra'] = old_item['geogebra']
                if not cur.get('pdf') and old_item.get('pdf'):
                    cur['pdf'] = old_item['pdf']
                if not cur.get('youtube') and old_item.get('youtube'):
                    cur['youtube'] = old_item['youtube']
                if not cur.get('algeomath') and old_item.get('algeomath'):
                    cur['algeomath'] = old_item['algeomath']
                for t in old_item.get('tags', []):
                    if t not in cur['tags']:
                        cur['tags'].append(t)

    # Let's count statistics
    final_list = list(materials_by_url.values())
    ggb_count = sum(1 for m in final_list if m.get('geogebra'))
    pdf_count = sum(1 for m in final_list if m.get('pdf'))
    yt_count = sum(1 for m in final_list if m.get('youtube'))
    algeo_count = sum(1 for m in final_list if m.get('algeomath'))

    print("=" * 60)
    print(f"Final Merged min7014 Material Database: {len(final_list)} items")
    print(f" - GeoGebra interactive: {ggb_count} items")
    print(f" - Visual Proof PDFs:    {pdf_count} items")
    print(f" - YouTube Lectures:     {yt_count} items")
    print(f" - AlgeoMath Models:     {algeo_count} items")
    print("=" * 60)

    # Save to assets/min7014_materials.json
    with open(existing_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved to {existing_path}!")

if __name__ == '__main__':
    deep_analyze()
