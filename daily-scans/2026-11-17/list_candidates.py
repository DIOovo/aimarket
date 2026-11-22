
import json, os
STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-17"
diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json")))
filt = json.load(open("/workspace/competitor-scan-2026-11-15/filtered_out.json"))
yest = {}
for x in filt:
    yest.setdefault(x["file"], set()).add(x["item"]["id_or_slug"].lower())

# memelry 40
print("======= MEMELRY new not in yest filtered =======")
prev_slugs={t["id_or_slug"].lower() for t in json.load(open(os.path.join(STORE,"memelry.json")))["templates"]}
# also related existing?
for t in sorted(diff["memelry.json"]["new"], key=lambda x: x["id_or_slug"]):
    s=t["id_or_slug"].lower()
    if s in yest.get("memelry.json", set()):
        continue
    print(f"  + {s} | {t['url']}")

print("\n======= YEST ricebowl catalog new (17) vs curated ======")
cat=json.load(open("/workspace/competitor-scan-2026-11-15/ricebowl_catalog.json"))
print("claimed", cat["numberOfItems_claimed"], "catalog", len(cat["catalog"]))
print("NEW in catalog yesterday:")
for t in cat["new"]:
    print(" ", t)
print("\nYEST ricebowl curated from finalize CURATED / snapshots new_templates")
prev=json.load(open(os.path.join(STORE,"ricebowl.json")))
print("store new_templates:", prev.get("new_templates"))
print("store note:", prev.get("note"))
print("store count", prev["template_count"])

# makememe new not filtered
print("\n======= MAKEMEME new not yest filtered ======")
for t in diff["makememe.json"]["new"]:
    if t["id_or_slug"].lower() not in yest.get("makememe.json", set()):
        print(" ", t)

print("\n======= TRENDTEMPLATE new not yest filtered ======")
for t in diff["trendtemplate.json"]["new"]:
    if t["id_or_slug"].lower() not in yest.get("trendtemplate.json", set()):
        print(" ", t)

print("\n======= PICTURETOVIDEO new not yest filtered ======")
for t in diff["picturetovideo.json"]["new"]:
    if t["id_or_slug"].lower() not in yest.get("picturetovideo.json", set()):
        print(" ", t)

print("\n======= STARR D new not yest filtered ======")
for t in diff["starrd.json"]["new"]:
    if t["id_or_slug"].lower() not in yest.get("starrd.json", set()):
        print(" ", t)

print("\n======= BOLLY new not yest filtered ======")
for t in diff["bolly.json"]["new"]:
    if t["id_or_slug"].lower() not in yest.get("bolly.json", set()):
        print(" ", t)
