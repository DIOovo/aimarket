#!/usr/bin/env python3
import json, os

OUT = "/workspace/competitor-scan-2026-11-17"
YEST = "/workspace/competitor-scan-2026-11-16"

diff = json.load(open(os.path.join(OUT, "diff_raw.json")))
yest_filtered = json.load(open(os.path.join(YEST, "filtered_out.json")))

ASSET_EXT = {".png",".jpg",".jpeg",".gif",".svg",".ico",".webp",".webmanifest",".json",".txt",".xml",".css",".js",".woff",".woff2",".map"}

filtered_keys = set()
for f in yest_filtered:
    slug = (f.get("item") or {}).get("id_or_slug","").lower()
    filtered_keys.add((f.get("file") or "", slug))
    filtered_keys.add((f.get("site") or "", slug))

remaining = {}
already_filtered = {}
lines = []
for fn, d in diff.items():
    new = d.get("new") or []
    still = []
    known = []
    for t in new:
        slug = (t.get("id_or_slug") or "").lower()
        url = (t.get("url") or "").lower()
        path = url.split("?",1)[0]
        is_asset = any(path.endswith(ext) for ext in ASSET_EXT)
        if (fn, slug) in filtered_keys or (d.get("site"), slug) in filtered_keys:
            known.append((t, "yest-filtered"))
        elif is_asset:
            known.append((t, "asset"))
        else:
            still.append(t)
    remaining[fn] = still
    already_filtered[fn] = known
    if still or d.get("missing"):
        lines.append("")
        lines.append("======== %s (%s) ======== " % (d["site"], fn))
        lines.append("raw_new=%d already_filtered=%d remaining=%d missing=%d" % (
            len(new), len(known), len(still), len(d.get("missing") or [])))
        for t in still:
            lines.append("  + %s | %s | %s" % (t.get("id_or_slug"), t.get("title",""), t.get("url")))
        miss = d.get("missing") or []
        for t in miss[:20]:
            lines.append("  - MISSING %s | %s" % (t.get("id_or_slug"), t.get("url")))
        if len(miss) > 20:
            lines.append("  - ... and %d more missing" % (len(miss)-20))

lines.append("")
lines.append("======= SITES WITH ONLY PREVIOUSLY-FILTERED OR NO REMAINING =======")
for fn, d in diff.items():
    still = remaining[fn]
    known = already_filtered[fn]
    if not still and not (d.get("missing") or []):
        lines.append("  %s: raw_new=%d all previously filtered/assets=%d" % (
            d["site"], len(d.get("new") or []), len(known)))

out = {fn: remaining[fn] for fn in remaining if remaining[fn]}
json.dump(out, open(os.path.join(OUT, "candidates_after_yest_filter.json"), "w"), ensure_ascii=False, indent=2)
lines.append("")
lines.append("Wrote candidates_after_yest_filter.json, total remaining %d" % sum(len(v) for v in out.values()))
print("\n".join(lines))
