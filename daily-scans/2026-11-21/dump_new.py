import json
d=json.load(open("diff_raw.json"))
need = [
    "samevid.json","memeclone.json","zapvid.json","genjutsu.json",
    "aitrendvideo.json","trendswap.json","summrs.json","picturetovideo.json",
    "aimakevideo.json","tryatrend.json","starrd.json","ricebowl.json","memelry.json"
]
lines=[]
for fn in need:
    v=d[fn]
    lines.append(f"\n======== {v['site']} +{len(v['new'])} -{len(v['missing'])} (prev {v['prev']} raw {v['raw_now']}) ========")
    for t in v["new"]:
        lines.append(f"  + {t.get('id_or_slug')} | {t.get('url')}")
    for t in v["missing"]:
        lines.append(f"  - MISSING {t.get('id_or_slug')} | {t.get('url')}")
open("new_remaining.txt","w").write("\n".join(lines)+"\n")
print("wrote", len(lines), "lines")
