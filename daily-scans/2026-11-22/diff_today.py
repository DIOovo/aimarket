#!/usr/bin/env python3
import json, os
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
FETCH = "/workspace/competitor-scan-2026-11-22/fetch_results.json"
fetch = json.load(open(FETCH, encoding="utf-8"))

def url_key(u):
    p = urlparse(u)
    path = p.path.rstrip("/") or "/"
    return (p.netloc.lower().removeprefix("www.") + path).lower()

diff = {}
for fn, res in fetch.items():
    prev = json.load(open(os.path.join(STORE, fn), encoding="utf-8"))
    prev_templates = prev.get("templates", [])
    prev_by_key = {url_key(t["url"]): t for t in prev_templates}
    prev_slugs = {t["id_or_slug"].lower() for t in prev_templates}
    cur = res["templates"] if res.get("fetch_ok") else prev_templates
    cur_by_key = {url_key(t["url"]): t for t in cur}
    cur_slugs = {t["id_or_slug"].lower() for t in cur}
    new_items = []
    for k, t in cur_by_key.items():
        if k not in prev_by_key and t["id_or_slug"].lower() not in prev_slugs:
            new_items.append(t)
    removed = []
    if res.get("fetch_ok"):
        for k, t in prev_by_key.items():
            if k not in cur_by_key and t["id_or_slug"].lower() not in cur_slugs:
                removed.append(t)
    diff[fn] = {
        "site": res["site"],
        "fetch_ok": res.get("fetch_ok"),
        "prev": len(prev_templates),
        "cur": len(cur),
        "new_count": len(new_items),
        "removed_count": len(removed),
        "notes": res.get("notes", []),
        "new": new_items,
        "removed": removed,
    }

rows = sorted(diff.items(), key=lambda kv: (-kv[1]["new_count"], kv[0]))
print(f"{'file':22} {'prev':>5} {'cur':>5} {'new':>5} {'rm':>4} ok  site")
total_new = total_rm = 0
for fn, d in rows:
    total_new += d["new_count"]
    total_rm += d["removed_count"]
    print(f"{fn:22} {d['prev']:5} {d['cur']:5} {d['new_count']:5} {d['removed_count']:4} {'Y' if d['fetch_ok'] else 'N'}  {d['site']}")
    show = d["new"] if d["new_count"] <= 40 else d["new"][:40]
    for t in show:
        print(f"    + {t['id_or_slug']}  {t['url']}")
    if d["new_count"] > 40:
        print(f"    ... and {d['new_count']-40} more")
    for t in d["removed"][:15]:
        print(f"    - {t['id_or_slug']}  {t['url']}")
    if len(d["removed"]) > 15:
        print(f"    ... and {len(d['removed'])-15} more removed")

print(f"\nTOTAL new={total_new} removed={total_rm}")
json.dump(diff, open("/workspace/competitor-scan-2026-11-22/diff_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote diff_raw.json")
