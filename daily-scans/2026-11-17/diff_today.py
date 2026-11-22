
import json, os, re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-17"
fetch = json.load(open(os.path.join(OUTDIR, "fetch_results.json")))

xml = open(os.path.join(OUTDIR, "raw/remakeyourmeme.com_sitemap.xml")).read()
xml = xml.strip()
if xml.startswith("~~~"):
    pass
# strip markdown fence if present
if xml.lstrip().startswith("<?xml") is False:
    m = re.search(r"<\?xml[\s\S]*", xml)
    if m:
        xml = m.group(0)
    xml = re.sub(r"\s*~~~$", "", xml)

root = ET.fromstring(xml)
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = []
urls = root.findall("sm:url", ns) or root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url") or root.findall("url")
for url in urls:
    loc = url.find("sm:loc", ns)
    if loc is None:
        loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    if loc is None:
        loc = url.find("loc")
    lastmod = url.find("sm:lastmod", ns)
    if lastmod is None:
        lastmod = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
    if lastmod is None:
        lastmod = url.find("lastmod")
    if loc is not None and loc.text:
        locs.append((loc.text.strip(), (lastmod.text.strip() if lastmod is not None and lastmod.text else "")))

def title_from_slug(slug):
    s = slug.strip("/").split("/")[-1]
    s = re.sub(r"-", " ", s)
    return " ".join(w.capitalize() for w in s.split())

rym_templates = []
rym_non = []
for loc, lastmod in locs:
    p = urlparse(loc)
    parts = [x for x in p.path.strip("/").split("/") if x]
    if len(parts) >= 2 and parts[0] == "templates":
        slug = parts[1]
        rym_templates.append({
            "id_or_slug": slug,
            "title": title_from_slug(slug),
            "url": loc if loc.endswith("/") else loc + "/",
            "lastmod": lastmod,
        })
    else:
        rym_non.append((loc, lastmod))

print("=== Remake Your Meme sitemap ===")
print("total locs", len(locs), "templates", len(rym_templates), "non-template", len(rym_non))

prev_rym = json.load(open(os.path.join(STORE, "remakeyourmeme.json")))
prev_slugs = {t["id_or_slug"].lower(): t for t in prev_rym["templates"]}
print("prev count", len(prev_slugs))
now_slugs = {t["id_or_slug"].lower(): t for t in rym_templates}
new = [t for s,t in now_slugs.items() if s not in prev_slugs]
removed = [t for s,t in prev_slugs.items() if s not in now_slugs]
print("NEW:")
for t in new:
    print(" ", t["lastmod"], t["id_or_slug"], t["url"])
print("REMOVED/missing:")
for t in removed:
    print(" ", t["id_or_slug"], t["url"])

fetch["remakeyourmeme.json"] = {
    **fetch.get("remakeyourmeme.json", {}),
    "site": "Remake Your Meme",
    "file": "remakeyourmeme.json",
    "home": "https://remakeyourmeme.com/",
    "fetch_ok": True,
    "sitemap_existed": True,
    "sitemap_urls_found": ["https://remakeyourmeme.com/sitemap.xml"],
    "templates": [{"id_or_slug": t["id_or_slug"], "title": t["title"], "url": t["url"]} for t in rym_templates],
    "template_count": len(rym_templates),
    "notes": ["Sitemap via WebFetch; box IP 403"],
    "webfetch": True,
}
json.dump(fetch, open(os.path.join(OUTDIR, "fetch_results.json"), "w"), ensure_ascii=False, indent=2)
print("patched fetch_results.json")

print("\n======= RAW DIFF ALL SITES =======")

diff = {}
for fn, fr in fetch.items():
    if not str(fn).endswith(".json"):
        continue
    prev_path = os.path.join(STORE, fn)
    if not os.path.exists(prev_path):
        print("NO PREV", fn)
        continue
    prev = json.load(open(prev_path))
    prev_tmpls = prev.get("templates") or []
    prev_s = {t["id_or_slug"].lower(): t for t in prev_tmpls}
    raw_now = fr.get("templates") or []
    now_s = {t["id_or_slug"].lower(): t for t in raw_now}
    raw_new = [now_s[s] for s in now_s if s not in prev_s]
    raw_removed = [prev_s[s] for s in prev_s if s not in now_s]
    print(f"\n## {prev.get('site', fn)} ({fn}) prev={len(prev_tmpls)} raw_now={len(raw_now)} new={len(raw_new)} missing={len(raw_removed)} fetch_ok={fr.get('fetch_ok')} notes={fr.get('notes') or fr.get('note')}")
    for t in sorted(raw_new, key=lambda x: x.get("id_or_slug","")):
        print(f"  + {t.get('id_or_slug')} | {t.get('title','')} | {t.get('url')}")
    if raw_removed and len(raw_removed) <= 15:
        for t in raw_removed:
            print(f"  - MISSING {t.get('id_or_slug')} | {t.get('url')}")
    elif raw_removed:
        print(f"  - MISSING {len(raw_removed)} items, first 10:")
        for t in raw_removed[:10]:
            print(f"    - {t.get('id_or_slug')} | {t.get('url')}")
    diff[fn] = {
        "site": prev.get("site"),
        "prev": len(prev_s),
        "raw_now": len(now_s),
        "new": raw_new,
        "missing": raw_removed,
    }

json.dump(diff, open(os.path.join(OUTDIR, "diff_raw.json"), "w"), ensure_ascii=False, indent=2)
print("\nWrote diff_raw.json")
print("\nSUMMARY")
for fn, d in diff.items():
    if d["new"] or d["missing"]:
        print(f"  {d['site']}: +{len(d['new'])} -{len(d['missing'])} (prev {d['prev']} raw {d['raw_now']})")
