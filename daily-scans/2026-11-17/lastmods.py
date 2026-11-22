#!/usr/bin/env python3
import json, os, re
from collections import Counter
from xml.etree import ElementTree as ET
from urllib.parse import urlparse

OUT = "/workspace/competitor-scan-2026-11-17"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

def parse(path):
    xml = open(path, encoding="utf-8", errors="replace").read()
    if xml.startswith("xml "):
        xml = "<?" + xml
    elif not xml.lstrip().startswith("<"):
        m = re.search(r"<\?xml[\s\S]*|<urlset[\s\S]*|<sitemapindex[\s\S]*", xml)
        if m:
            xml = m.group(0)
        elif "xml version" in xml[:80]:
            xml = "<?" + xml[xml.find("xml version"):]
    try:
        root = ET.fromstring(xml)
    except Exception as e:
        print("PARSE FAIL", path, e)
        print("HEAD:", repr(xml[:120]))
        return []
    urls = []
    for url in list(root.findall("sm:url", NS)) or list(root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")) or list(root.findall("url")):
        loc = url.find("sm:loc", NS)
        if loc is None: loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is None: loc = url.find("loc")
        lastmod = url.find("sm:lastmod", NS)
        if lastmod is None: lastmod = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
        if lastmod is None: lastmod = url.find("lastmod")
        if loc is not None and loc.text:
            urls.append((loc.text.strip(), (lastmod.text.strip() if lastmod is not None and lastmod.text else "")))
    return urls

cands = json.load(open(os.path.join(OUT, "candidates_after_yest_filter.json")))

pmi = parse(os.path.join(OUT, "raw/putmein.app_sitemap.xml"))
print("putmein sitemap locs", len(pmi))
tmpl = [(loc, lm) for loc,lm in pmi if "/templates/" in loc]
print("template locs", len(tmpl))
print("lastmod counts for ALL putmein templates:")
c = Counter((lm[:10] if lm else "(none)") for _,lm in tmpl)
for k,v in sorted(c.items()):
    print(" ", k, v)

new_slugs = {t["id_or_slug"].lower() for t in cands["putmein.json"]}
by_slug = {}
for loc,lm in tmpl:
    slug = loc.rstrip("/").split("/")[-1].lower()
    by_slug[slug] = lm
print("\nlastmod for 86 NEW putmein:")
c2 = Counter()
details = []
for slug in new_slugs:
    lm = by_slug.get(slug, "?")
    key = lm[:10] if lm and lm != "?" else lm
    c2[key] += 1
    details.append((lm, slug))
for k,v in sorted(c2.items()):
    print(" ", k, v)
print("\nsample of each lastmod bucket:")
byk = {}
for lm,slug in details:
    key = (lm[:10] if lm and lm != "?" else lm)
    byk.setdefault(key, []).append(slug)
for k in sorted(byk):
    print(" ", k, "e.g.", ", ".join(byk[k][:5]), ("..." if len(byk[k])>5 else ""))

sitemap_map = {
    "trendtemplate.json": "trendtemplate.com_sitemap.xml",
    "makeviral.json": "www.makeviral.ai_sitemap.xml",
    "makememe.json": "makememe.video_sitemap.xml",
    "clipremake.json": "clipremake.com_sitemap.xml",
    "danceremake.json": "danceremake.com_sitemap.xml",
    "samevid.json": "samevid.com_sitemap.xml",
    "summrs.json": "www.summrs.com_sitemap.xml",
    "rapvideo.json": "rapvideo.ai_sitemap.xml",
    "memelry.json": "memelry.com_sitemap.xml",
    "zapvid.json": "zapvid.ai_sitemap.xml",
    "aimakevideo.json": "aimakevideo.com_sitemap.xml",
}

print("\n======= LASTMOD FOR OTHER CANDIDATES =======")
for fn, sm in sitemap_map.items():
    path = os.path.join(OUT, "raw", sm)
    items = parse(path)
    lmmap = {}
    for loc,lm in items:
        slug = loc.rstrip("/").split("/")[-1].lower()
        lmmap[slug] = lm
        lmmap[loc.rstrip("/").lower()] = lm
    print("\n--", fn, "parsed", len(items), "--")
    for t in cands.get(fn, []):
        slug = t["id_or_slug"].lower()
        url = (t.get("url") or "").rstrip("/").lower()
        lm = lmmap.get(slug) or lmmap.get(url) or "?"
        print(" ", lm, slug)
