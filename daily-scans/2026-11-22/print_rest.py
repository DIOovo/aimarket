#!/usr/bin/env python3
import json, os, re
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
diff = json.load(open("/workspace/competitor-scan-2026-11-22/diff_raw.json", encoding="utf-8"))

for fn in ["samevid.json", "summrs.json", "memefxai.json", "rapvideo.json", "memelry.json"]:
    d = diff[fn]
    print("=" * 70)
    print(f"{fn} {d['site']} prev={d['prev']} cur={d['cur']} new={d['new_count']} rm={d['removed_count']}")
    for t in d["new"]:
        print(f"  + {t['id_or_slug']}\t{t['url']}")
    for t in d["removed"]:
        print(f"  - {t['id_or_slug']}\t{t['url']}")

prev = json.load(open(os.path.join(STORE, "remakeyourmeme.json"), encoding="utf-8"))
prev_slugs = {t["id_or_slug"].lower() for t in prev["templates"]}
print("=" * 70)
print("Remake Your Meme baseline slugs:", len(prev_slugs))
for t in prev["templates"]:
    print(f"  BASE {t['id_or_slug']}\t{t['url']}")

md = open("/workspace/competitor-scan-2026-11-22/raw/remakeyourmeme-sitemap-webfetch.md", encoding="utf-8").read()
urls = re.findall(r"https://remakeyourmeme\.com/templates/[^\s)>\"]+", md)
canon = []
seen = set()
for u in urls:
    u = u.rstrip(".,);")
    if u.rstrip("/").endswith("/templates"):
        continue
    key = u.rstrip("/").lower()
    if key in seen:
        continue
    seen.add(key)
    slug = key.rsplit("/", 1)[-1]
    canon.append((slug, u if u.endswith("/") else u + "/"))

print("=" * 70)
print(f"Remake Your Meme sitemap templates: {len(canon)}")
new = []
smslugs = {s for s, _ in canon}
for slug, u in canon:
    if slug not in prev_slugs:
        new.append((slug, u))
        print(f"  + NEW {slug}  {u}")
missing = []
for t in prev["templates"]:
    if t["id_or_slug"].lower() not in smslugs:
        missing.append(t)
        print(f"  - MISSING FROM SITEMAP {t['id_or_slug']}  {t['url']}")
print(f"rym new={len(new)} missing_from_sitemap={len(missing)}")
json.dump(
    {
        "new": [{"id_or_slug": s, "title": s, "url": u} for s, u in new],
        "missing": missing,
        "all": [{"id_or_slug": s, "url": u} for s, u in canon],
    },
    open("/workspace/competitor-scan-2026-11-22/rym_parse.json", "w", encoding="utf-8"),
    indent=2,
)
