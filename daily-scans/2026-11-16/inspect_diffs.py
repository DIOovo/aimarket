
import json, os, re
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-16"
diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json")))
excl = json.load(open(os.path.join(STORE, "excluded-non-templates.json")))

# print remaining sites of interest fully
sites = [
  "genjutsu.json","summrs.json","picturetovideo.json","starrd.json",
  "memefxai.json","rapvideo.json","kubflow.json","bolly.json",
  "tryatrend.json","memelry.json","aitrendvideo.json","ricebowl.json",
  "smew.json","remakeyourmeme.json"
]
for fn in sites:
    d = diff[fn]
    print("="*70)
    print(f"{d['site']} ({fn}) prev={d['prev']} raw={d['raw_now']} +{len(d['new'])} -{len(d['missing'])}")
    if d.get("missing"):
        for t in d["missing"]:
            print(f"  - MISSING {t.get('id_or_slug')} | {t.get('url')}")
    # For ricebowl only print count and URL path prefixes of new, plus any /trends/meme
    if fn == "ricebowl.json":
        from collections import Counter
        prefs = Counter()
        meme = []
        for t in d["new"]:
            p = urlparse(t["url"]).path
            top = "/" + "/".join([x for x in p.split("/") if x][:2])
            prefs[top] += 1
            if "/trends/meme" in p or p.startswith("/trends/"):
                meme.append(t)
        print("  path prefixes of NEW:")
        for k,v in prefs.most_common():
            print(f"    {k}: {v}")
        print(f"  new on /trends*: {len(meme)}")
        for t in meme:
            print(f"    + {t.get('id_or_slug')} | {t.get('url')}")
        # also show prev path prefixes
        prev = json.load(open(os.path.join(STORE, fn)))
        prefs2 = Counter()
        for t in prev["templates"]:
            p = urlparse(t["url"]).path
            top = "/" + "/".join([x for x in p.split("/") if x][:2])
            prefs2[top] += 1
        print("  PREV path prefixes:")
        for k,v in prefs2.most_common():
            print(f"    {k}: {v}")
        continue
    if fn == "memelry.json":
        # show URL patterns of new
        from collections import Counter
        prefs = Counter()
        for t in d["new"]:
            p = urlparse(t["url"]).path
            parts = [x for x in p.split("/") if x]
            top = "/" + (parts[0] if parts else "")
            # classify extension or first segment
            if "." in (parts[-1] if parts else ""):
                prefs["FILE:"+parts[-1].rsplit(".",1)[-1]] += 1
            else:
                prefs[top] += 1
        print("  new path prefixes:")
        for k,v in prefs.most_common():
            print(f"    {k}: {v}")
        # print all new
        for t in sorted(d["new"], key=lambda x: x.get("id_or_slug","")):
            print(f"  + {t.get('id_or_slug')} | {t.get('title','')} | {t.get('url')}")
        continue
    if fn == "picturetovideo.json":
        prev = json.load(open(os.path.join(STORE, fn)))
        print("  PREV templates:")
        for t in prev["templates"]:
            print(f"    * {t.get('id_or_slug')} | {t.get('url')}")
        for t in sorted(d["new"], key=lambda x: x.get("id_or_slug","")):
            print(f"  + {t.get('id_or_slug')} | {t.get('title','')} | {t.get('url')}")
        continue
    if fn == "rapvideo.json":
        prev = json.load(open(os.path.join(STORE, fn)))
        print("  PREV sample (first 8) and path prefixes:")
        from collections import Counter
        prefs = Counter()
        for t in prev["templates"]:
            p = urlparse(t["url"]).path
            top = "/" + "/".join([x for x in p.split("/") if x][:1])
            prefs[top] += 1
        for k,v in prefs.most_common():
            print(f"    prev {k}: {v}")
        for t in prev["templates"][:8]:
            print(f"    * {t.get('id_or_slug')} | {t.get('url')}")
        for t in sorted(d["new"], key=lambda x: x.get("id_or_slug","")):
            print(f"  + {t.get('id_or_slug')} | {t.get('title','')} | {t.get('url')}")
        continue
    for t in sorted(d["new"], key=lambda x: x.get("id_or_slug","")):
        print(f"  + {t.get('id_or_slug')} | {t.get('title','')} | {t.get('url')}")

print("\n======= excluded-non-templates keys / samples =======")
print("note:", excl.get("note"))
for fn, items in excl.get("by_file", {}).items():
    print(fn, "count", len(items) if isinstance(items, list) else type(items))
    if isinstance(items, list):
        for x in items[:8]:
            print("   ", x if not isinstance(x, dict) else {k:x.get(k) for k in list(x)[:6]})
    elif isinstance(items, dict):
        print("   keys", list(items.keys())[:10])
