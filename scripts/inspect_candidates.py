#!/usr/bin/env python3
import json, os, re
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"

def slugs(fn):
    data = json.load(open(os.path.join(STORE, fn), encoding="utf-8"))
    return {t["id_or_slug"].lower(): t for t in data["templates"]}

# Memelry: search existing for related stems
ml = slugs("memelry.json")
stems = [
    "mermaid", "saree", "wizard", "la-la-land", "lalaland", "good-chat", "goodchat",
    "titanic", "flying", "window-peeper", "dime-dime", "tiny-desk", "tinydesk",
    "rush-hour", "dog-pool", "wassup", "no-scrubs", "bulin", "central-cee",
    "gangnam", "coaches-thriller", "car-drift",
]
print("=== Memelry existing matches ===")
for stem in stems:
    hits = [s for s in ml if stem in s]
    print(f"  {stem}: {hits or 'NONE'}")

print("\n=== RapVideo existing slugs ===")
rv = slugs("rapvideo.json")
for s, t in sorted(rv.items()):
    print(f"  {s}\t{t['url']}")

print("\n=== SameVid related ===")
sv = slugs("samevid.json")
for stem in ["last-dance", "legacy", "the-last"]:
    hits = [s for s in sv if stem in s]
    print(f"  {stem}: {hits or 'NONE'}")

print("\n=== Starrd existing related ===")
st = slugs("starrd.json")
for stem in ["christmas-photo", "break-a-leg", "convertible", "faithful", "rush-hour", "truck-jump", "beautiful", "oil", "humiliating"]:
    hits = [s for s in st if stem in s]
    print(f"  {stem}: {hits or 'NONE'}")

print("\n=== Ricebowl existing count", len(slugs('ricebowl.json')))
print("\n=== PictureToVideo existing ===")
for s,t in slugs("picturetovideo.json").items():
    print(f"  {s}\t{t['url']}")
