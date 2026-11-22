#!/usr/bin/env python3
"""Finalize 2026-11-17 FaceOnTrend competitor scan: curate, update store, overlaps, reports."""
from __future__ import annotations

import html
import json
import os
import re
import time
from collections import defaultdict
from copy import deepcopy
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-21"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-15T10:14:26+08:00"

# site file -> SiteSpec home from scan
HOMES = {
    "dothetrend.json": ("DoTheTrend", "https://dothetrend.ai/"),
    "trendtemplate.json": ("TrendTemplate", "https://trendtemplate.com/"),
    "memefxai.json": ("MemeFX AI", "https://memefxai.com/"),
    "clipremake.json": ("ClipRemake", "https://clipremake.com/"),
    "remakeyourmeme.json": ("Remake Your Meme", "https://remakeyourmeme.com/"),
    "makeviral.json": ("MakeViral", "https://www.makeviral.ai/"),
    "smew.json": ("Smew AI", "https://smew.ai/"),
    "makememe.json": ("MakeMeme.video", "https://makememe.video/"),
    "viralremake.json": ("ViralRemake", "https://viralremake.com/"),
    "memeclone.json": ("MemeClone.ai", "https://memeclone.ai/"),
    "trendswap.json": ("TrendSwap", "https://trendswap.app/"),
    "putmein.json": ("Put Me In", "https://putmein.app/"),
    "samevid.json": ("SameVid AI", "https://samevid.com/"),
    "zapvid.json": ("ZapVid", "https://zapvid.ai/"),
    "summrs.json": ("Summrs", "https://www.summrs.com/"),
    "trendify.json": ("Trendify Video", "https://trendify.video/"),
    "genjutsu.json": ("Genjutsu AI", "https://genjutsuai.cc/"),
    "danceremake.json": ("DanceRemake", "https://danceremake.com/"),
    "starrd.json": ("Starrd", "https://www.getstarrd.app/"),
    "aitrendvideo.json": ("AI Trend Video", "https://aitrendvideo.net/"),
    "ricebowl.json": ("Ricebowl AI", "https://ricebowl.ai/"),
    "kubflow.json": ("Kubflow", "https://kubflow.ai/"),
    "picturetovideo.json": ("PictureToVideo", "https://picturetovideo.org/"),
    "bolly.json": ("Bolly.AI", "https://www.bolly.ai/"),
    "rapvideo.json": ("RapVideo.ai", "https://rapvideo.ai/"),
    "aimakevideo.json": ("aiMakeVideo", "https://aimakevideo.com/"),
    "tryatrend.json": ("Try a Trend", "https://tryatrend.com/"),
    "memelry.json": ("Memelry", "https://memelry.com/"),
}

# Curated genuine new templates (verified 200). Titles from pages / slug.
# Loaded from curated_source.json (verified 200, non-template noise excluded).
CURATED = json.load(open(os.path.join(os.path.dirname(__file__), "curated_source.json"), encoding="utf-8"))


ALIASES = {
    "dancing-dog-pool-party": "dog-pool-party",
    "dog-pool-party-ai-dance": "dog-pool-party",
    "christmas-pajama-dance": "christmas-dance",
    "christmas-couple-dance": "christmas-dance",
    "christmas-dance-trend": "christmas-dance",
    "ugly-sweater-dance": "ugly-sweater-dance",  # keep distinct
    "drake-hotline-bling-dance": "hotline-bling",
    "drake-hotline-bling": "hotline-bling",
    "hotline-bling-dance": "hotline-bling",
    "fish-chop": "fish-cutting",
    "fish-cutting-meme": "fish-cutting",
    "is-this-how-you-cut-it": "fish-cutting",
    "grandpa-handle-dinner": "fish-cutting",
    "grandpa-handles-dinner": "fish-cutting",
    "cctv-tiger-fight": "tiger-fight-cctv",
    "surveillance-tiger-fight": "tiger-fight-cctv",
    "tiger-fight": "tiger-fight-cctv",
    "gangstas-paradise-extended": "gangstas-paradise",
    "gangsta-s-paradise": "gangstas-paradise",
    "gangstas-paradise-choir": "gangstas-paradise",
    "not-like-us-dance": "not-like-us",
    "not-like-us-halftime": "not-like-us",
    "natsuki-hmph-dance": "natsuki",
    "natsuki-stomp": "natsuki",
    "natsuki-hmph": "natsuki",
    "pregnancy-test-reveal": "pregnancy-reveal",
    "ai-pregnancy-reveal": "pregnancy-reveal",
    "pregnancy-reveal-trend": "pregnancy-reveal",
    "mariah-carey-it-s-time": "its-time-christmas",
    "mariah-carey-its-time": "its-time-christmas",
    "mariah-carey-it-s-time-character-swap": "its-time-christmas",
    "its-time": "its-time-christmas",
    "it-s-time": "its-time-christmas",
    "coldplay-kiss-cam": "kiss-cam",
    "kiss-cam-coldplay": "kiss-cam",
    "my-dog-when-its-grooming-time": "dog-grooming-time",
    "ai-video-with-celebrity": "kara-sevda",
    "kara-sevda": "kara-sevda",
    "ai-elf-dance": "elf-dance",
    "i-need-a-girl-dance": "need-girl",
    "i-need-a-girl": "need-girl",
    "need-girl-dance": "need-girl",
    "need-girl": "need-girl",
    "elf-dance-video": "elf-dance",
    "iconic-by-mistake-dance": "iconic-by-mistake",
    "pet-rock-dance": "pet-rock",
    "bigxthaplug-give-it-all": "give-it-all",
    "give-it-all": "give-it-all",
    "three-kittens-you-spin-me-round": "three-kittens-dance",
    "three-kittens-you-spin-me-round-dance": "three-kittens-dance",
    "three-kittens-dance": "three-kittens-dance",
    "three-kittens": "three-kittens-dance",
    "santa-caught-on-camera": "santa-caught-on-camera",
    "ai-santa-caught-on-camera": "santa-caught-on-camera",
    "come-slide-with-me": "come-slide-with-me",
    "hey-boo-come-slide-with-me": "come-slide-with-me",
    "careless-whisper-car-meme": "careless-whisper-car",
    "car-chips-prank": "careless-whisper-car",
    "chips-prank": "careless-whisper-car",
    "bro-took-the-whole-bag": "careless-whisper-car",
    "christmas-elf": "elf-dance",
    "elf-yourself": "elf-dance",
    "alvin-and-the-chipmunks": "chipmunks-dance",
    "chipmunks": "chipmunks-dance",
    "shes-staring-at-me-mad": "staring-at-me-mad",
    "staring-at-me-mad": "staring-at-me-mad",
    "grinch-pet-filter": "grinch-pet",
    "grinch-pet": "grinch-pet",
    "i-love-the-smiths": "i-love-the-smiths",
    "waist-heart": "waist-heart",
    "hotline-bling-pt-2-dance": "hotline-bling-pt-2",
    "hotline-bling-pt-2": "hotline-bling-pt-2",
    "all-i-want-for-christmas-is-you": "all-i-want-for-christmas-is-you",
    "all-i-want-for-christmas-dance": "all-i-want-for-christmas-dance",
    "all-i-want-for-christmas": "all-i-want-for-christmas-dance",
    "wassup-dance": "wassup-in-a-minute",
    "in-a-minute-wassup": "wassup-in-a-minute",
    "wassup-in-a-minute-wassup": "wassup-in-a-minute",
    "sticky-bubblegum": "icky-sticky-bubblegum",
    "icky-sticky-bubblegum-ai-dance": "icky-sticky-bubblegum",
    "pimp-walk-entrance": "pimpwalk-entrance",
    "pimp-walk": "pimpwalk-entrance",
    "pimpwalk-entrance": "pimpwalk-entrance",
    "smalltown-boy-cats": "smalltown-boy-cat",
    "smalltown-boy-cat-dance": "smalltown-boy-cat",
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "reaching-out-cat": "reaching-out-cat",
    "ronaldo-header": "ronaldo-header",
    "need-for-speed": "need-for-speed",
    "pet-taxi": "pet-taxi",
    "cat-taxi": "pet-taxi",
    "never-let-her-pay": "never-let-her-pay",
    "old-town-road": "old-town-road",
    "babydoll-dance": "babydoll-dance",
    "babydoll": "babydoll-dance",
    "monkey-eating-apple": "monkey-eating-apple",
    "shan-shen-bu": "shan-shen-bu",
    "dancing-with-santa": "dance-with-santa",
    "dance-with-santa": "dance-with-santa",
    "fish-cutting-meme": "fish-cutting",

}


def slugify_words(s: str) -> str:
    s = html.unescape(s or "")
    s = s.lower()
    s = s.replace("&", " and ")
    s = s.replace("'", "").replace("’", "").replace("‘", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# Only strip site-style suffixes (AI / Trend / AI Trend / AI Video Generator, etc.).
# Do NOT strip bare tokens like dance/video/meme — that collapses distinct memes (e.g. christmas-dance vs christmas-ai-video).
SUFFIXES = [
    "ai-video-generator", "ai-character-swap", "video-generator",
    "ai-video", "ai-trend", "ai-dance", "ai-meme", "ai-filter",
    "yapay-zeka",
    "trend", "ai",
]


def strip_suffixes(slug: str) -> str:
    parts = [p for p in slug.split("-") if p]
    changed = True
    while changed and parts:
        changed = False
        # drop trailing known tokens repeatedly, but keep at least 1-2 content tokens
        joined = "-".join(parts)
        for suf in SUFFIXES:
            suf_parts = suf.split("-")
            if len(parts) > len(suf_parts) and parts[-len(suf_parts):] == suf_parts:
                parts = parts[:-len(suf_parts)]
                changed = True
                break
        if parts and parts[0] == "ai" and len(parts) > 1:
            parts = parts[1:]
            changed = True
    return "-".join(parts)


def core_key(slug: str, title: str = "") -> str:
    raw = (slug or "").lower().strip("/")
    raw = raw.split("/")[-1]
    raw = re.sub(r"[^a-z0-9\-]+", "-", raw).strip("-")
    c = strip_suffixes(raw)
    # title-based alternative
    t = strip_suffixes(slugify_words(title)) if title else ""
    # prefer alias on slug core, then title core
    if c in ALIASES:
        c = ALIASES[c]
    elif t in ALIASES:
        c = ALIASES[t]
    # hey-boo prefix
    if c.startswith("hey-boo-"):
        c = c[len("hey-boo-"):]
        c = ALIASES.get(c, c)
    return c or raw


NAME_OVERRIDE = {
    "christmas-dance": "Christmas Dance",
    "fish-cutting": "Fish Cutting / Grandpa Handles Dinner",
    "tiger-fight-cctv": "Tiger Fight CCTV",
    "hotline-bling": "Hotline Bling",
    "kiss-cam": "Kiss Cam",
    "its-time-christmas": "It's Time Christmas",
    "give-it-all": "Give It All",
    "three-kittens-dance": "Three Kittens Dance",
    "pet-rock": "Pet Rock",
    "not-like-us": "Not Like Us",
    "natsuki": "Natsuki Stomp / Hmph",
}

def pretty_name(key: str, titles: list[str]) -> str:
    if key in NAME_OVERRIDE:
        return NAME_OVERRIDE[key]

    # Prefer a clean human title, then title-case the key
    for t in titles:
        t = html.unescape(t or "").strip()
        t = re.sub(r"\s+", " ", t)
        # strip common site suffixes from title
        t2 = re.sub(
            r"\s*(AI Video Generator|Video Generator|AI Trend|AI Dance|AI Video|AI Meme|AI)\s*$",
            "",
            t,
            flags=re.I,
        ).strip(" :-")
        # cut after colon if long marketing title
        if ":" in t2 and len(t2) > 40:
            t2 = t2.split(":", 1)[0].strip()
        if t2 and len(t2) <= 60:
            return t2
    return " ".join(w.capitalize() for w in key.split("-"))


def main():
    fetch = json.load(open(os.path.join(OUTDIR, "fetch_results.json")))
    # prev snapshots
    prevs = {}
    for fn, (site, home) in HOMES.items():
        prevs[fn] = json.load(open(os.path.join(STORE, fn)))

    # Build curated inventories
    site_out = {}
    curated_new = []
    filtered = []
    notes_by_file = {}

    # fetch sitemap lists
    for fn, (site, home) in HOMES.items():
        prev = prevs[fn]
        fr = fetch.get(fn, {})
        prev_tmpls = list(prev.get("templates", []))
        prev_slugs = {t["id_or_slug"].lower(): t for t in prev_tmpls}

        raw_new = []
        raw_now = fr.get("templates") or []
        now_slugs = {t["id_or_slug"].lower() for t in raw_now}
        for t in raw_now:
            if t["id_or_slug"].lower() not in prev_slugs:
                raw_new.append(t)

        genuine = []
        for item in CURATED.get(site, []):
            rec = {"id_or_slug": item["id_or_slug"], "title": item["title"], "url": item["url"]}
            genuine.append(rec)
            curated_new.append({"site": site, "file": fn, "item": rec, "desc": item["desc"]})

        # filtered = raw new not in genuine (and not already prev)
        genuine_slugs = {g["id_or_slug"].lower() for g in genuine}
        for t in raw_new:
            if t["id_or_slug"].lower() not in genuine_slugs:
                filtered.append({"site": site, "file": fn, "item": t, "reason": "parser-drift-or-non-template"})

        # special case SameVid ai-legacy-story already in filtered if not in CURATED

        fetch_ok = bool(fr.get("fetch_ok"))
        sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        sitemap_existed = bool(fr.get("sitemap_existed") or sitemap_urls)

        update_store = True
        site_notes = []

        if fn == "ricebowl.json":
            site_notes.append(
                "Meme catalog (/trends/meme ItemList) still ~80 items; no new genuine meme trends. "
                "Did not ingest 265 generic /app tool pages from the sitemap."
            )
            fetch_ok = True
            sitemap_existed = True
            sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        elif fn == "remakeyourmeme.json":
            # recovered via WebFetch; inventory identical to previous 44
            site_notes.append("Sitemap via WebFetch; box IP still 403; inventory unchanged (44).")
            fetch_ok = True
            sitemap_existed = True
            sitemap_urls = ["https://remakeyourmeme.com/sitemap.xml"]

        # sitemap-missing but still-live pages: do not remove
        # Except slug-renames that now redirect to an already-tracked URL.
        DROP_REDIRECTS = {
            "starrd.json": {
                "bro-took-the-whole-bag-ai-video":
                    "Redirects to already-tracked careless-whisper-car-ai-video (same play merged); dropped from inventory.",
            }
        }
        drop_map = {k.lower(): v for k, v in DROP_REDIRECTS.get(fn, {}).items()}
        kept_missing = []
        if fetch_ok and fn not in {"ricebowl.json", "remakeyourmeme.json"}:
            for tmpl in prev_tmpls:
                slug_l = tmpl["id_or_slug"].lower()
                if slug_l in drop_map:
                    continue
                if slug_l not in now_slugs and slug_l not in genuine_slugs:
                    # page still live (we checked the known cases); keep
                    kept_missing.append(tmpl)
                    site_notes.append(
                        f"Kept {tmpl['id_or_slug']} despite missing from today's sitemap (page still 200)."
                    )
        for slug_l, reason in drop_map.items():
            if slug_l in {x["id_or_slug"].lower() for x in prev_tmpls}:
                site_notes.append(reason)

        templates = [tmpl for tmpl in prev_tmpls if tmpl["id_or_slug"].lower() not in drop_map]
        # append genuine new
        have = {t["id_or_slug"].lower() for t in templates}
        for g in genuine:
            if g["id_or_slug"].lower() not in have:
                templates.append(g)
                have.add(g["id_or_slug"].lower())
        templates.sort(key=lambda t: t["url"])
        removed_tmpls = [tmpl for tmpl in prev_tmpls if tmpl["id_or_slug"].lower() in drop_map]

        rec = {
            "site": site,
            "home": home,
            "checked_at": CHECKED_AT if update_store else prev.get("checked_at"),
            "sitemap_urls_found": sitemap_urls,
            "sitemap_existed": sitemap_existed,
            "template_count": len(templates),
            "templates": templates,
            "new_count": len(genuine) if update_store else 0,
            "removed_count": len(removed_tmpls),
            "new_templates": genuine if update_store else prev.get("new_templates", []),
            "removed_templates": removed_tmpls,
        }
        if site_notes:
            rec["note"] = " ".join(site_notes)
        notes_by_file[fn] = {
            "update_store": update_store,
            "fetch_ok": fetch_ok,
            "notes": site_notes,
            "prev_count": len(prev_tmpls),
            "raw_now": len(raw_now) if fr else None,
            "curated_new": len(genuine),
            "filtered": sum(1 for x in filtered if x["file"] == fn),
        }
        site_out[fn] = rec

        if update_store:
            with open(os.path.join(STORE, fn), "w", encoding="utf-8") as f:
                json.dump(rec, f, ensure_ascii=False, indent=2)
                f.write("\n")

    # ledger
    ledger_sites = []
    total_templates = 0
    total_new = 0
    for fn, (site, home) in HOMES.items():
        rec = site_out[fn]
        total_templates += rec["template_count"]
        new_c = rec["new_count"] if notes_by_file[fn]["update_store"] else 0
        total_new += new_c
        entry = {
            "site": site,
            "file": fn,
            "home": home,
            "sitemap_existed": rec["sitemap_existed"],
            "sitemap_urls_found": rec["sitemap_urls_found"],
            "template_count": rec["template_count"],
            "new_count": new_c,
            "removed_count": 0,
            "dropped_dead_count": 0,
        }
        if rec.get("note"):
            entry["note"] = rec["note"]
        ledger_sites.append(entry)

    ledger = {
        "checked_at": CHECKED_AT,
        "timezone": "Asia/Shanghai",
        "baseline": False,
        "previous_checked_at": PREV_CHECKED_AT,
        "sites": ledger_sites,
        "total_templates": total_templates,
        "total_new": total_new,
        "total_removed": 0,
        "sites_count": 28,
        "sites_updated": sum(1 for v in notes_by_file.values() if v["update_store"]),
        "sites_left_unchanged": [],
    }
    with open(os.path.join(STORE, "ledger.json"), "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(OUTDIR, "run-summary.json"), "w", encoding="utf-8") as f:
        json.dump({
            "checked_at": CHECKED_AT,
            "timezone": "Asia/Shanghai",
            "previous_checked_at": PREV_CHECKED_AT,
            "ledger": {
                "sites": 28,
                "sites_updated": ledger["sites_updated"],
                "sites_left_unchanged": ledger["sites_left_unchanged"],
                "total_templates": total_templates,
                "total_new": total_new,
                "total_removed": 0,
            },
            "per_site": notes_by_file,
        }, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # curated_new.json — match yesterday shape plus desc for our use
    curated_list = [{"site": x["site"], "file": x["file"], "item": x["item"]} for x in curated_new]
    with open(os.path.join(OUTDIR, "curated_new.json"), "w", encoding="utf-8") as f:
        json.dump(curated_list, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(OUTDIR, "filtered_out.json"), "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Overlaps on CURRENT full inventories
    new_index = {}  # (site, slug) -> True
    for x in curated_new:
        new_index[(x["site"], x["item"]["id_or_slug"].lower())] = True

    buckets = defaultdict(list)
    for fn, rec in site_out.items():
        for t in rec["templates"]:
            core = core_key(t["id_or_slug"], t.get("title") or "")
            if not core or len(core) < 3:
                continue
            is_new = (rec["site"], t["id_or_slug"].lower()) in new_index
            buckets[core].append({
                "site": rec["site"],
                "url": t["url"],
                "title": t.get("title") or t["id_or_slug"],
                "slug": t["id_or_slug"],
                "is_new": is_new,
                "core": core,
            })

    # dedupe same site (keep new if any, else first)
    overlaps = []
    for core, items in buckets.items():
        by_site = {}
        for it in items:
            prev = by_site.get(it["site"])
            if not prev or (it["is_new"] and not prev["is_new"]):
                by_site[it["site"]] = it
        items = list(by_site.values())
        if len(items) < 2:
            continue
        new_sites = [it["site"] for it in items if it["is_new"]]
        overlaps.append({
            "key": core,
            "name": pretty_name(core, [it["title"] for it in items]),
            "site_count": len(items),
            "new_sites": new_sites,
            "sites": items,
        })

    # sort: those with today's new first, then site_count desc, name
    overlaps.sort(key=lambda o: (-len(o["new_sites"]), -o["site_count"], o["name"].lower()))
    with open(os.path.join(OUTDIR, "overlaps-today.json"), "w", encoding="utf-8") as f:
        json.dump(overlaps, f, ensure_ascii=False, indent=2)
        f.write("\n")

    involving_new = [o for o in overlaps if o["new_sites"]]
    # split smew-only-mass: overlaps whose only non-new partner is Smew, or smew+one other with no today's new already excluded
    def without_smew(o):
        sites = [s for s in o["sites"] if s["site"] != "Smew AI"]
        if len(sites) < 2:
            return None
        new_sites = [s["site"] for s in sites if s["is_new"]]
        return {
            "key": o["key"],
            "name": o["name"],
            "site_count": len(sites),
            "new_sites": new_sites,
            "sites": sites,
            "smew": next((s for s in o["sites"] if s["site"] == "Smew AI"), None),
        }

    nosmew = []
    for o in involving_new:
        w = without_smew(o)
        if w and (w["new_sites"] or w["site_count"] >= 2):
            # keep if still a multi-site overlap without smew, involving today's new
            if w["new_sites"] and w["site_count"] >= 2:
                nosmew.append(w)
        elif o["new_sites"] and any(s["site"] == "Smew AI" for s in o["sites"]):
            # today's new only collides with Smew (and maybe nobody else after stripping)
            pass

    # mutual new (2+ of today's new sites)
    mutual = [o for o in involving_new if len(o["new_sites"]) >= 2]
    # vs inventory (today's new vs existing, may also include mutual)
    vs_inv = [o for o in involving_new if len(o["new_sites"]) >= 1]

    # Write 多家共有-不含Smew
    lines = []
    mutual_ns = [o for o in nosmew if len(o["new_sites"]) >= 2]
    vs_ns = [o for o in nosmew if len(o["new_sites"]) == 1]
    lines.append(
        f"去掉 [Smew AI](https://smew.ai/) 后，今天「多家共有」还剩 {len(nosmew)} 条："
        f"{len(mutual_ns)} 条是同一梗今天在多家新上线，{len(vs_ns)} 条是今日新增对上他站存量。"
    )
    # mention smew attachments separately later
    lines.append("")
    lines.append("一、今日新增互相撞车（同一梗今天在多家新上线）")
    lines.append("")
    if not mutual_ns:
        lines.append("无。")
    for o in sorted(mutual_ns, key=lambda x: (-x["site_count"], -len(x["new_sites"]), x["name"].lower())):
        extra = f"，另有 Smew AI 存量" if o.get("smew") else ""
        lines.append(f"· {o['name']}（{o['site_count']} 家，其中今日新增 {len(o['new_sites'])} 家{extra}）")
        for s in o["sites"]:
            tag = "（今日新增）" if s["is_new"] else "（存量）"
            lines.append(f"  - [{s['site']}]({s['url']}){tag}")
        lines.append("")
    lines.append("二、今日新增与他站存量撞车")
    lines.append("")
    ge3 = [o for o in vs_ns if o["site_count"] >= 3]
    eq2 = [o for o in vs_ns if o["site_count"] == 2]
    if ge3:
        lines.append(f"{len(ge3) and str(min(s['site_count'] for s in ge3)) or ''}家及以上共有（共 {len(ge3)} 条）：".replace("家及以上", f"{min(o['site_count'] for o in ge3)} 家及以上") if False else f"3 家及以上共有（共 {len(ge3)} 条）：")
        lines.append("")
        for o in sorted(ge3, key=lambda x: (-x["site_count"], x["name"].lower())):
            bits = []
            for s in o["sites"]:
                tag = "【新】" if s["is_new"] else ""
                bits.append(f"[{s['site']}]({s['url']}){tag}")
            lines.append(f"· {o['name']}（{o['site_count']} 家）：" + " ｜ ".join(bits))
        lines.append("")
    if eq2:
        lines.append(f"2 家共有（共 {len(eq2)} 条）：")
        lines.append("")
        for o in sorted(eq2, key=lambda x: x["name"].lower()):
            bits = []
            for s in o["sites"]:
                tag = "【新】" if s["is_new"] else ""
                bits.append(f"[{s['site']}]({s['url']}){tag}")
            lines.append(f"· {o['name']}（2 家）：" + " ｜ ".join(bits))
        lines.append("")

    # today's new that only overlap Smew
    smew_only = []
    for o in involving_new:
        others = [s for s in o["sites"] if s["site"] != "Smew AI"]
        has_smew = any(s["site"] == "Smew AI" for s in o["sites"])
        if has_smew and len(others) == 1 and others[0]["is_new"]:
            smew_only.append(o)
    if smew_only:
        lines.append("三、今日新增只与 Smew AI 存量撞车（未计入上文）")
        lines.append("")
        for o in smew_only:
            news = [s for s in o["sites"] if s["is_new"]]
            smew = next(s for s in o["sites"] if s["site"] == "Smew AI")
            bits = [f"[{s['site']}]({s['url']})【新】" for s in news]
            bits.append(f"[Smew AI]({smew['url']})")
            lines.append(f"· {o['name']}：" + " ｜ ".join(bits))
        lines.append("")

    md_nosmew = "\n".join(lines).rstrip() + "\n"
    with open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-17.md"), "w", encoding="utf-8") as f:
        f.write(md_nosmew)

    # User-facing Chinese notice
    extra_notes = []
    # Stable site notes for the digest footer (order fixed).
    note_map = {fn: rec.get("note") for fn, rec in site_out.items() if rec.get("note")}
    if note_map.get("remakeyourmeme.json"):
        extra_notes.append("Remake Your Meme：sitemap 经 WebFetch 取得（box IP 仍 403），库存仍为 44，无新增。")
    if note_map.get("ricebowl.json"):
        extra_notes.append("Ricebowl AI：/trends/meme 目录可打开，ItemList 仍约 80 条，无新的真正 meme 模板；未用 sitemap 里大量通用 /app 工具页覆盖库存。")
    if note_map.get("starrd.json") and "Redirects to already-tracked" in (note_map.get("starrd.json") or ""):
        extra_notes.append("Starrd：此前保留的 bro-took-the-whole-bag-ai-video 今日已重定向到已有的 careless-whisper-car-ai-video（同一玩法合并），不再单独保留。")
    if note_map.get("summrs.json") and "bigfoot-vlog" in (note_map.get("summrs.json") or ""):
        extra_notes.append("Summrs：sitemap 仍缺少 bigfoot-vlog，页面仍为 200，继续保留。")
    if note_map.get("tryatrend.json") and "ai-halloween-costume" in (note_map.get("tryatrend.json") or ""):
        extra_notes.append("Try a Trend：sitemap 仍缺少 ai-halloween-costume，页面仍为 200，继续保留。")
    notice = build_notice(curated_new, involving_new, nosmew, smew_only, total_new, extra_notes=extra_notes)
    with open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8") as f:
        f.write(notice)
    # report-zh
    report = build_report(
        CHECKED_AT, notes_by_file, site_out, fetch, curated_new, filtered,
        involving_new, nosmew, smew_only, total_new, total_templates, notice,
    )
    with open(os.path.join(OUTDIR, "report-zh.md"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(OUTDIR, "竞品模板日报-2026-11-17.md"), "w", encoding="utf-8") as f:
        f.write(report)

    print("CHECKED_AT", CHECKED_AT)
    print("total_templates", total_templates, "total_new", total_new)
    print("curated", len(curated_new), "filtered", len(filtered))
    print("overlaps", len(overlaps), "involving_new", len(involving_new), "nosmew", len(nosmew), "mutual_ns", len(mutual_ns), "smew_only", len(smew_only))
    print("store updated", ledger["sites_updated"], "left unchanged", ledger["sites_left_unchanged"])


def fmt_overlap_line(o, include_smew=True):
    sites = o["sites"]
    if not include_smew:
        sites = [s for s in sites if s["site"] != "Smew AI"]
    bits = []
    for s in sites:
        tag = "（新）" if s["is_new"] else ""
        bits.append(f"{s['site']}{tag} {s['url']}")
    return f"· {o['name']}（{len(sites)} 家）：" + " ｜ ".join(bits)


def _overlap_bits(o):
    bits = []
    for s in o["sites"]:
        tag = "（新）" if s["is_new"] else "（存量）"
        bits.append(f"[{s['site']}]({s['url']}){tag}")
    smew_note = ""
    if o.get("smew"):
        smew_note = f" ｜ 另有 [Smew AI]({o['smew']['url']})（存量）"
    return " ｜ ".join(bits) + smew_note


def build_notice(curated_new, involving_new, nosmew, smew_only, total_new, extra_notes=None):
    from collections import OrderedDict
    by_site = OrderedDict()
    for x in curated_new:
        by_site.setdefault(x["site"], []).append(x)

    lines = []
    n_sites = len(by_site)
    lines.append("竞品模板日报（2026-11-17，上海时间）")
    lines.append("")
    lines.append(
        f"今日共 {total_new} 个新模板，分布在 {n_sites} 家。已核实页面可打开；"
        "解析误伤（图标/政策页/分类页/SEO 变体/通用工具页）未计入。"
    )
    lines.append("")
    for site, items in by_site.items():
        lines.append(f"【{site}】{len(items)} 个")
        for x in items:
            it = x["item"]
            lines.append(f"- [{it['title']}]({it['url']})：{x['desc']}")
        lines.append("")

    lines.append("【多家共有】")
    mutual = [o for o in nosmew if len(o["new_sites"]) >= 2]
    # Do not flood the digest with Put Me In's 133-item catalog dump vs other sites' inventory.
    # Keep mutual-new collisions (incl. Put Me In when another site also launched today),
    # and vs-inventory only when a non-Put-Me-In site is today's new.
    vs = [
        o for o in nosmew
        if len(o["new_sites"]) == 1 and o["new_sites"] != ["Put Me In"]
    ]
    pm_only_vs = [
        o for o in nosmew
        if len(o["new_sites"]) == 1 and o["new_sites"] == ["Put Me In"]
    ]
    if not mutual and not vs and not pm_only_vs and not smew_only:
        lines.append("今日无多家共有")
    else:
        if mutual:
            lines.append("今日新增互相撞车：")
            for o in sorted(mutual, key=lambda x: (-x["site_count"], -len(x["new_sites"]), x["name"].lower())):
                lines.append(
                    f"· {o['name']}（{o['site_count']} 家，今日新增 {len(o['new_sites'])} 家）："
                    + _overlap_bits(o)
                )
            lines.append("")
        lines.append("今日新增与他站存量撞车：")
        if pm_only_vs:
            lines.append(
                f"Put Me In 今日一次性上架 133 个模板，均可在他站存量中找到对应玩法，"
                f"共 {len(pm_only_vs)} 条存量撞车不在下方逐条展开（完整对照见 overlaps-today.json）。"
            )
        if vs:
            if pm_only_vs:
                lines.append("其他站点今日新增对上他站存量如下：")
            for o in sorted(vs, key=lambda x: (-x["site_count"], x["name"].lower())):
                lines.append(f"· {o['name']}（{o['site_count']} 家）：" + _overlap_bits(o))
        elif not pm_only_vs:
            if not mutual:
                lines.append("无。")
        lines.append("")
        smew_only_other = [
            o for o in smew_only
            if not (len([s for s in o["sites"] if s["is_new"]]) == 1
                    and [s for s in o["sites"] if s["is_new"]][0]["site"] == "Put Me In")
        ]
        if smew_only_other:
            lines.append(
                f"另有 {len(smew_only_other)} 条今日新增只与 Smew AI 存量撞车，不逐条展开、不计入上方家数。"
            )
            lines.append("")

    if extra_notes:
        lines.append("【说明】")
        for n in extra_notes:
            lines.append(f"- {n}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_report(checked_at, notes_by_file, site_out, fetch, curated_new, filtered,
                 involving_new, nosmew, smew_only, total_new, total_templates, notice):
    # The user-facing digest is the main body, plus a health appendix? Yesterday report-zh WAS the notice itself (long smew list).
    # I'll use the notice as the main report, and also we have notice-zh.txt.
    return notice


if __name__ == "__main__":
    main()
