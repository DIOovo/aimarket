
import json, os, re
from collections import defaultdict
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-21"

diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json")))
checks = json.load(open(os.path.join(OUTDIR, "url_checks.json")))
check_map = {(c["file"], c["id_or_slug"].lower()): c for c in checks}

yest = defaultdict(set)
for x in json.load(open("/workspace/competitor-scan-2026-11-20/filtered_out.json")):
    yest[x["file"]].add(x["item"]["id_or_slug"].lower())

FILE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
            ".css", ".js", ".xml", ".txt", ".json", ".webmanifest", ".map")

print("======= Not in yest filter, not asset, not ricebowl, not in url_checks =======")
unchecked = []
for fn, d in diff.items():
    for t in d["new"]:
        slug = t["id_or_slug"].lower()
        path = (t.get("url") or "").lower()
        if fn == "ricebowl.json":
            continue
        if slug in yest[fn]:
            continue
        if any(slug.endswith(ext) or path.endswith(ext) for ext in FILE_EXT):
            continue
        if (fn, slug) not in check_map:
            unchecked.append((d["site"], fn, slug, t.get("url")))
print("count", len(unchecked))
for row in unchecked:
    print(" ", *row)

print("\n======= Checked items with meta =======")
for c in checks:
    if c.get("kind") == "keep_missing":
        print(f"KEEP {c['status']} {c['file']} {c['id_or_slug']} | {c.get('h1') or c.get('og') or c.get('title_page')} | {(c.get('desc') or '')[:180]}")
        continue
    print(f"CHK {c['status']} 404={c.get('looks_404')} {c['file']} {c['id_or_slug']}")
    print(f"    title: {(c.get('title_page') or '')[:120]}")
    print(f"    h1: {(c.get('h1') or '')[:120]}")
    print(f"    og: {(c.get('og') or '')[:120]}")
    print(f"    desc: {(c.get('desc') or '')[:220]}")
