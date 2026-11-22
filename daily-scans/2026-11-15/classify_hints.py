
import json, os, re
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-15"
diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json")))

# yesterday filtered
filt = json.load(open("/workspace/competitor-scan-2026-11-14/filtered_out.json"))
from collections import defaultdict, Counter
by = defaultdict(list)
for x in filt:
    by[x["file"]].append(x["item"]["id_or_slug"])
print("YESTERDAY FILTERED COUNTS")
for fn, slugs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    print(f"  {fn}: {len(slugs)}")
    if fn in {"memelry.json","samevid.json","ricebowl.json","picturetovideo.json","rapvideo.json","summrs.json","memefxai.json","starrd.json","bolly.json","aitrendvideo.json","makememe.json","trendtemplate.json"}:
        print("   ", ", ".join(slugs[:40]), ("..." if len(slugs)>40 else ""))

print("\n======= AI Trend Video new =======")
for t in diff["aitrendvideo.json"]["new"]:
    print(t)

print("\n======= AI Trend Video prev =======")
prev=json.load(open(os.path.join(STORE,"aitrendvideo.json")))
for t in prev["templates"]:
    print(t)

print("\n======= Kubflow prev =======")
prev=json.load(open(os.path.join(STORE,"kubflow.json")))
for t in prev["templates"]:
    print(t)

print("\n======= Bolly prev sample categories? ======")
prev=json.load(open(os.path.join(STORE,"bolly.json")))
# do they already have category-like slugs?
cats=["anime","brainrot","edits","football","kpop","meme","multi-person","dance"]
have={t["id_or_slug"].lower() for t in prev["templates"]}
print("category slugs already in prev?", {c: c in have for c in cats})
# path patterns
prefs=Counter()
for t in prev["templates"]:
    p=urlparse(t["url"]).path
    parts=[x for x in p.split("/") if x]
    prefs["/"+"/".join(parts[:1])] += 1
print("bolly prev prefixes", prefs)
# any short slugs
shorts=[t for t in prev["templates"] if t["id_or_slug"].count("-")<=0]
print("bolly short slugs count", len(shorts))
for t in shorts[:20]:
    print(" ", t["id_or_slug"], t["url"])

print("\n======= Starrd category-like already in prev? ======")
prev=json.load(open(os.path.join(STORE,"starrd.json")))
have={t["id_or_slug"].lower() for t in prev["templates"]}
cands=["action","anime","asmr","cars","crime","drama","gaming","henshin","holidays","music","nostalgia","pets","pranks","song","sports","trailers"]
print({c: c in have for c in cands})
# path pattern of prev
print("starrd sample urls:")
for t in prev["templates"][:5]:
    print(" ", t["url"])
# templates vs template
prefs=Counter(urlparse(t["url"]).path.split("/")[1] if urlparse(t["url"]).path.strip("/") else "" for t in prev["templates"])
print("starrd first path segment", prefs)

print("\n======= SameVid yesterday filtered intersection with today new ======")
today_new={t["id_or_slug"].lower() for t in diff["samevid.json"]["new"]}
yest=set(s.lower() for s in by.get("samevid.json",[]))
print("today new also in yest filtered", sorted(today_new & yest))
print("today new NOT in yest filtered:")
for t in diff["samevid.json"]["new"]:
    if t["id_or_slug"].lower() not in yest:
        print(" ", t["id_or_slug"], t["url"])

print("\n======= Memelry yesterday filtered intersection ======")
today_new={t["id_or_slug"].lower() for t in diff["memelry.json"]["new"]}
yest=set(s.lower() for s in by.get("memelry.json",[]))
print("overlap count", len(today_new & yest))
print("today new NOT in yest filtered count", len(today_new-yest))

# memelry prev cores to detect SEO variants
prev=json.load(open(os.path.join(STORE,"memelry.json")))
prev_slugs={t["id_or_slug"].lower() for t in prev["templates"]}
print("\nMemelry prev count", len(prev_slugs))

# check if new slugs look like SEO variants of prev or of each other
SEO_HINTS = ("from-photo","from-selfies","face-swap","without-editing","look-realistic","on-phone","one-time-payment","original-audio","two-people","with-friends","with-music","dance-moves","one-selfie","meme-origin","cost","privacy","affiliates","tools","how-to","what-is","vs-","alternative")

print("\n======= Ricebowl yesterday curated / catalog notes ======")
# ricebowl_catalog from yesterday
try:
    cat=json.load(open("/workspace/competitor-scan-2026-11-14/ricebowl_catalog.json"))
    print("catalog type", type(cat), (list(cat)[:20] if isinstance(cat,dict) else f"len {len(cat)}"))
    if isinstance(cat, dict):
        for k,v in cat.items():
            if k in ("items","templates","urls","catalog"):
                print(k, "len", len(v) if hasattr(v,"__len__") else v)
                if isinstance(v, list) and v:
                    print(" sample", v[0])
            elif not isinstance(v, (list,dict)):
                print(k, v)
            else:
                print(k, type(v), len(v))
    elif isinstance(cat, list) and cat:
        print("sample", cat[0], "len", len(cat))
except Exception as e:
    print("err", e)
