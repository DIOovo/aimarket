#!/usr/bin/env python3
import json, os, importlib.util
from collections import defaultdict

spec = importlib.util.spec_from_file_location("fin", "/workspace/competitor-scan-2026-11-20/finalize.py")
fin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fin)

fin.ALIASES.update({
    "rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "put-the-rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "im-the-one": "shoulder-carry-im-the-one",
    "im-the-one-shoulder-carry": "shoulder-carry-im-the-one",
    "cause-im-the-one": "shoulder-carry-im-the-one",
    "shoulder-carry": "shoulder-carry-im-the-one",
    "feel-the-pressure": "mourinho-pressure",
    "mourinho-pressure-original-audio": "mourinho-pressure",
    "catch-santa-on-camera": "santa-caught-on-camera",
    "jingle-bell-brazil-dance": "jingle-bell-brazil",
    "give-it-all-to-me": "give-it-all",
    "ai-cafe": "fancy-cafe",
    "gta-5-goodbye": "gta-farewell",
    "gta-6-farewell": "gta-farewell",
})

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
needles = [
    "car-drift", "james-bond", "gta-5-goodbye", "gta-6-farewell", "laisse-tomber",
    "me-and-my-girlfriend", "me-parece", "ps2-filter", "sidewalk-drop", "sunlight-eye",
    "chinese-time", "never-let-her-pay", "husband-emporium", "king-jin", "my-moon",
    "rollie", "shoulder-carry", "im-the-one", "cause-im-the-one", "jingle-bell-brazil",
    "dancing-snowman", "snowman-dance", "santa-caught", "santa-hug", "nutcracker",
    "fancy-cafe", "ai-cafe", "chaos", "dress-trend", "tattoo", "clayface", "mermaid",
    "ocarina", "prada", "sheru", "trouble-maker", "trump", "old-town-road", "teardrop",
    "fish-chop", "fish-cutting", "tricycle", "central-cee", "doja", "mans-not-hot",
    "what-if-you-fly", "feel-the-pressure", "mourinho", "give-it-all", "gta-6-loading",
    "rainbow", "jamaican", "bond",
]

hits = defaultdict(list)
for fn in os.listdir(STORE):
    if not fn.endswith(".json") or fn in ("ledger.json", "excluded-non-templates.json") or fn.startswith("overlaps"):
        continue
    d = json.load(open(os.path.join(STORE, fn)))
    site = d.get("site", fn)
    for t in d.get("templates") or []:
        slug = t["id_or_slug"].lower()
        title = (t.get("title") or "").lower()
        core = fin.core_key(slug, t.get("title") or "")
        blob = slug + " " + title + " " + core
        if any(n in blob for n in needles):
            hits[core or slug].append((site, t["id_or_slug"], t["url"]))

for k in sorted(hits):
    print("CORE %s (%d)" % (k, len(hits[k])))
    for site, slug, url in hits[k]:
        print("  %-20s %-50s %s" % (site, slug, url))
    print()