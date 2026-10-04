import urllib.request
import re
import sys
import json
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def extract_all_catalog():
    url = 'https://min7014.github.io/2019080802.html'
    print(f"Fetching master catalog from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    print(f"Loaded master catalog: {len(html)} bytes")
    
    # Extract details blocks
    details_pattern = re.compile(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>', re.DOTALL | re.IGNORECASE)
    
    extracted_items = []
    seen_urls = set()
    
    for m in details_pattern.finditer(html):
        summary_html = m.group(1)
        body_html = m.group(2)
        cat_title = re.sub(r'<.*?>', '', summary_html).strip()
        cat_title = re.sub(r'\[고유주소\].*', '', cat_title).strip()
        
        # Split into li blocks
        lis = re.findall(r'<li>(.*?)</li>', body_html, re.DOTALL | re.IGNORECASE)
        for li in lis:
            # Find math link
            math_m = re.search(r'<a\s+href=[\'"](https://min7014\.github\.io/[^\'"]+)[\'"][^>]*>(.*?)</a>', li, re.DOTALL | re.IGNORECASE)
            if not math_m:
                continue
            
            raw_url = math_m.group(1).strip()
            raw_title = re.sub(r'<.*?>', '', math_m.group(2)).strip()
            raw_title = raw_title.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            
            if not raw_title or '[고유주소]' in raw_title:
                continue
                
            # PDF link
            pdf_m = re.search(r'href=[\'"](https://min7014\.github\.io/[^\'"]+\.pdf[^\'"]*)[\'"]', li, re.IGNORECASE)
            pdf = pdf_m.group(1).strip() if pdf_m else ''
            
            # YouTube link
            yt_m = re.search(r'href=[\'"](https://(?:youtu\.be|www\.youtube\.com)[^\'"]+)[\'"]', li, re.IGNORECASE)
            yt = yt_m.group(1).strip() if yt_m else ''
            
            # GeoGebra link
            ggb_m = re.search(r'href=[\'"](https://www\.geogebra\.org/[^\'"]+)[\'"]', li, re.IGNORECASE)
            ggb = ggb_m.group(1).strip() if ggb_m else ''
            
            # AlgeoMath link
            algeo_m = re.search(r'href=[\'"](https?://[^\'"]*(?:algeomath|me2\.do)[^\'"]*)[\'"]', li, re.IGNORECASE)
            algeo = algeo_m.group(1).strip() if algeo_m else ''
            
            key = (raw_title, raw_url)
            if key in seen_urls:
                continue
            seen_urls.add(key)
            
            extracted_items.append({
                'title': raw_title,
                'url': raw_url,
                'category': cat_title,
                'pdf': pdf,
                'youtube': yt,
                'geogebra': ggb,
                'algeomath': algeo
            })
            
    print(f"Extracted {len(extracted_items)} items from master catalog.")
    
    # Also check if existing assets/min7014_materials.json has more items
    try:
        with open('assets/min7014_materials.json', 'r', encoding='utf-8') as f:
            old_items = json.load(f)
        print(f"Found {len(old_items)} items in assets/min7014_materials.json")
        for old in old_items:
            k = (old.get('title', ''), old.get('url', ''))
            if k not in seen_urls and old.get('title') and old.get('url'):
                seen_urls.add(k)
                extracted_items.append({
                    'title': old.get('title'),
                    'url': old.get('url'),
                    'category': old.get('category', '일반 수학'),
                    'pdf': old.get('pdf', ''),
                    'youtube': old.get('youtube', ''),
                    'geogebra': old.get('geogebra', ''),
                    'algeomath': old.get('algeomath', '')
                })
    except Exception as e:
        print("Old items error:", e)
        
    print(f"Total merged catalog items: {len(extracted_items)}")
    return extracted_items

if __name__ == '__main__':
    items = extract_all_catalog()
    with open('min7014_full_catalog_raw.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print("Saved min7014_full_catalog_raw.json")
