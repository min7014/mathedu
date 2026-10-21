import json

local = json.load(open('/c/Users/min/Desktop/mathedu/board/index.json', encoding='utf-8'))
site = json.load(open('/c/Users/min/Desktop/mathedu/board/index_site.json', encoding='utf-8'))

print("local count:", len(local))
print("site count:", len(site))

local_slugs = {e['slug'] for e in local}
site_slugs = {e['slug'] for e in site}

print("only in site (new):", sorted(site_slugs - local_slugs))
print("only in local:", sorted(local_slugs - site_slugs))

for e in site:
    if e['slug'] not in local_slugs:
        print("NEW:", e['slug'], '|', e.get('title'), '|', e.get('time'))
