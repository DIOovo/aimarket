#!/usr/bin/env python3
"""Finalize 2026-11-20 FaceOnTrend competitor scan."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import time
from collections import OrderedDict, defaultdict
from copy import deepcopy
from urllib.parse import urlparse

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-20"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-19T09:40:27+08:00"

spec = importlib.util.spec_from_file_location(
    "fin15", os.path.join(OUTDIR, "finalize.py")
)
fin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fin)

HOMES = fin.HOMES
core_key = fin.core_key
pretty_name = fin.pretty_name

# Extra aliases for today's collisions
fin.ALIASES.update({
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "mean-girls-jingle-bell-rock": "jingle-bell-rock",
    "pimpwalk-entrance": "pimp-walk-entrance",
    "monkey-eating-apple": "monkey-eating-apple",
    "reaching-out-cat": "reaching-out-cat",
    "give-it-all-to-me": "give-it-all",
    "rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "put-the-rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "shoulder-carry-im-the-one": "shoulder-carry-im-the-one",
    "im-the-one": "shoulder-carry-im-the-one",
    "im-the-one-shoulder-carry": "shoulder-carry-im-the-one",
    "feel-the-pressure": "mourinho-pressure",
    "mourinho-pressure": "mourinho-pressure",
    "mourinho-pressure-original-audio": "mourinho-pressure",
    "quiet-on-the-creek-dance": "quiet-on-the-creek",
    "jingle-bell-brazil-dance": "jingle-bell-brazil",
    "la-tormenta-de-arena": "te-he-perdido",
    "te-he-perdido": "te-he-perdido",
    "catch-santa-on-camera": "santa-caught-on-camera",
    "youre-under-arrest": "under-arrest-dance",
    "youre-under-arrest-dance": "under-arrest-dance",
    "under-arrest-dance": "under-arrest-dance",
    "tidal-wave-video": "tidal-wave",
    "su-gibi-git-su-gibi-gel": "tidal-wave",
    "christmas-pajama-dance": "christmas-dance",
    "smalltown-boy-ai-dance": "smalltown-boy-cat",
    "smalltown-boy": "smalltown-boy-cat",
    "cause-im-the-one": "shoulder-carry-im-the-one",
    "shoulder-carry": "shoulder-carry-im-the-one",
    "ai-cafe": "first-time-in-a-fancy-cafe",
    "first-time-in-a-fancy-cafe": "first-time-in-a-fancy-cafe",
    "mini-tricycle-crash": "tricycle-crash",
    "tricycle-crash": "tricycle-crash",
    "trouble-maker-dance": "trouble-maker",
    "gta-5-goodbye": "gta-farewell",
    "gta-6-farewell": "gta-farewell",
    "car-drift": "car-drift",
    "central-cee-doja": "central-cee-doja",
    "mans-not-hot": "mans-not-hot",
    "pterodactyl-juarez": "mexico-pterodactyl",
    "mexico-pterodactyl": "mexico-pterodactyl",
    "santa-nice-list": "santa-nice-list",
    "baby-face-filter": "baby-face-filter",
    "boxing-dog": "boxing-dog",
    "pixar-snow-globe": "pixar-snow-globe",
    "ai-snow-globe": "pixar-snow-globe",
    "more-like-a-quesadilla": "more-like-a-quesadilla",
    "yamal-dance": "yamal-dance",
    "funny-goalkeeper": "funny-goalkeeper",
    "kung-fu-goalkeeper": "funny-goalkeeper",
    "hot-chick-ice-cream": "hot-chick-ice-cream",
    "the-hot-chick-ice-cream-scene": "hot-chick-ice-cream",
    "me-and-my-girlfriend": "me-and-my-girlfriend",
    "a2o-lite-neon": "a2o-lite-neon",
    "dancing-with-santa": "dance-with-santa",
    "bat-smash-bottle-splash": "bat-smash-bottle-splash",
    "marble-hallway-dance": "marble-hallway-dance",
    "plane-wing-dance-backflip": "plane-wing-dance-backflip",
    "sunset-horse-ride": "sunset-horse-ride",
    "you-rock-my-world": "you-rock-my-world",
    "last-dance": "last-dance",
    "last-dance-trend": "last-dance",
    "atm-christmas-wish": "atm-christmas-wish",
    "gta-next-chapter": "gta-farewell",
    "gta-5-goodbye": "gta-farewell",
    "singing-pet": "singing-pet",
    "the-jawn": "the-jawn",
    "thats-the-jawn": "the-jawn",
    "champagne-birthday": "champagne-birthday",
    "dog-cake-smash": "dog-cake-smash",
    "st-tropez-dj": "st-tropez-dj",
    "need-for-speed-car": "need-for-speed",
    "need-for-speed-extended-car": "need-for-speed",
    "pet-taxi": "pet-taxi",
    "sheru-bhai": "sheru-bhai",
    "james-bond-reveal": "james-bond-reveal",
})
fin.NAME_OVERRIDE.update({
    "shoulder-carry-im-the-one": "Shoulder Carry / I'm the One / Rollie On My Wrist",
    "mourinho-pressure": "Mourinho Pressure / Feel The Pressure",
    "te-he-perdido": "Te He Perdido / La Tormenta de Arena",
    "tidal-wave": "Tidal Wave / Su Gibi Git Su Gibi Gel",
    "under-arrest-dance": "You're Under Arrest Dance",
    "quiet-on-the-creek": "Quiet on the Creek",
    "jingle-bell-brazil": "Jingle Bell Brazil Dance",
    "my-moon-my-man": "My Moon My Man",
    "give-it-all": "BigXthaPlug Give It All",
    "dance-with-santa": "Dance With Santa",
    "santa-caught-on-camera": "Catch Santa on Camera",
    "christmas-dance": "Christmas Pajama Dance",
    "reaching-out-cat": "Reaching Out Cat",
    "never-let-her-pay": "Never Let Her Pay",
    "wassup-in-a-minute": "Wassup in a Minute",
    "sticky-bubblegum": "Sticky Bubblegum",
    "reaching-out-cat": "Reaching Out Cat",
    "ronaldo-header": "Ronaldo Header",
    "need-for-speed": "Need for Speed",
    "pet-taxi": "Pet Taxi",
    "never-let-her-pay": "Never Let Her Pay",
    "jingle-bell-rock": "Jingle Bell Rock / Mean Girls",
    "give-it-all": "BigXthaPlug Give It All",
    "pimp-walk-entrance": "Pimp Walk Entrance",
    "monkey-eating-apple": "Monkey Eating Apple",
    "babydoll-dance": "Babydoll Dance",
    "shan-shen-bu": "Shan Shen Bu / 闪身步",
    "hotline-bling": "Hotline Bling",
    "first-time-in-a-fancy-cafe": "First Time in a Fancy Cafe",
    "tricycle-crash": "Mini Tricycle Crash",
    "trouble-maker": "Trouble Maker Dance",
    "gta-farewell": "GTA Goodbye / Farewell",
    "car-drift": "Car Drift",
    "james-bond-reveal": "James Bond Reveal",
    "king-jin": "King Jin",
    "husband-emporium": "Husband Emporium",
    "sheru-bhai": "Sheru Bhai",
    "clayface": "Clayface",
    "old-town-road": "Old Town Road",
    "gta-6-loading-screen": "GTA 6 Loading Screen",
    "what-if-you-fly": "What If You Fly",
    "central-cee-doja": "Central Cee Doja",
    "fish-cutting": "Fish Cutting / Grandpa Handles Dinner",
    "snowman-dance": "Snowman Dance",
    "mexico-pterodactyl": "Mexico Pterodactyl / Pterodactyl Juárez",
    "santa-nice-list": "Santa Nice List",
    "baby-face-filter": "Baby Face Filter",
    "boxing-dog": "Boxing Dog",
    "pixar-snow-globe": "Pixar Snow Globe",
    "more-like-a-quesadilla": "More Like a Quesadilla",
    "yamal-dance": "Yamal Dance / Y Que Fue",
    "funny-goalkeeper": "Funny / Kung Fu Goalkeeper",
    "hot-chick-ice-cream": "Hot Chick Ice Cream",
    "me-and-my-girlfriend": "Me and My Girlfriend",
    "a2o-lite-neon": "A2O Lite Neon",
    "bat-smash-bottle-splash": "Bat Smash Bottle Splash",
    "marble-hallway-dance": "Marble Hallway Dance",
    "plane-wing-dance-backflip": "Plane Wing Dance Backflip",
    "sunset-horse-ride": "Sunset Horse Ride",
    "you-rock-my-world": "You Rock My World",
    "last-dance": "Last Dance",
    "atm-christmas-wish": "ATM Christmas Wish",
    "singing-pet": "Singing Pet",
    "the-jawn": "The Jawn",
    "champagne-birthday": "Champagne Birthday",
    "dog-cake-smash": "Dog Cake Smash",
    "st-tropez-dj": "St Tropez DJ",
    "sheru-bhai": "Sheru Bhai",
    "need-for-speed": "Need for Speed",
    "pet-taxi": "Pet Taxi",
    "james-bond-reveal": "James Bond Reveal",
    "gta-farewell": "GTA 5 Goodbye / Next Chapter",
    "dance-with-santa": "Dance With Santa",
})

# Genuine day-over-day new templates (verified 200). Put Me In bulk is handled separately.
CURATED = json.load(open(os.path.join(OUTDIR, "curated_source.json"), encoding="utf-8"))
INVENTORY_ONLY = json.load(open(os.path.join(OUTDIR, "inventory_only.json"), encoding="utf-8"))

FILTER_REASONS = {
    ("makememe.json", "christmas-ai-video-trends"): "aggregation-hub",
    ("makememe.json", "questions"): "faq-page",
    ("memelry.json", "cortis-go-ai-from-photo"): "seo-variant-of-existing-template",
    ("memelry.json", "how-to-make-no-scrubs-ai-video"): "seo-howto-landing",
    ("memelry.json", "wassup-dance-face-expression-guide"): "guide-page",
    ("memelry.json", "wassup-dance-with-three-friends"): "seo-howto-landing",
    ("trendtemplate.json", "tiktok-ai-trends"): "aggregation-hub",
    ("memelry.json", "golf-dance-ai-photo-guide"): "guide-page",
    ("memelry.json", "mourinho-pressure-original-audio"): "seo-variant-of-existing-template",
    ("memelry.json", "gta-6-loading-screen-ai"): "static-image-not-video-template",
    ("memelry.json", "car-drift-photo-guide"): "guide-page",
    ("memelry.json", "central-cee-doja-ai-origin"): "seo-origin-landing",
    ("memelry.json", "central-cee-doja-photo-guide"): "guide-page",
    ("memelry.json", "mans-not-hot-ai-origin"): "seo-origin-landing",
    ("trendtemplate.json", "how-to-make-rooftop-groove-ai-video"): "seo-howto-landing",
    ("trendtemplate.json", "ai-christmas-video"): "aggregation-or-tool-hub",
    ("trendtemplate.json", "ai-dance"): "aggregation-or-tool-hub",
    ("trendtemplate.json", "ai-photo-creator"): "tool-page",
    ("trendtemplate.json", "ai-trend-templates"): "aggregation-hub",
    ("trendtemplate.json", "photo-template"): "tool-page",
    ("trendtemplate.json", "video-template-online"): "tool-page",
    ("trendtemplate.json", "refund-policy"): "legal-page",
    ("trendtemplate.json", "report"): "support-page",
    ("kubflow.json", "generations"): "app-tool-page",
    ("memelry.json", "atm-christmas-wish-meaning"): "seo-origin-landing",
    ("memelry.json", "gta-next-chapter-meaning"): "seo-origin-landing",
    ("memelry.json", "singing-pet-photo-guide"): "guide-page",
    ("memelry.json", "the-jawn-meaning"): "seo-origin-landing",
    ("starrd.json", "birthday"): "alias-of-champagne-birthday-ai-video",
    ("starrd.json", "effects"): "category-page-404",
    ("starrd.json", "famous"): "category-page-404",
}

# Drop slugs that were renamed or now redirect to another existing template.
STARRD_404 = {
        "ai-personal-trainer-prank": "page 404 on 2026-11-19",
        "ai-pool-boy-prank": "page 404 on 2026-11-19",
        "ai-repair-man-prank": "page 404 on 2026-11-19",
        "anime-hero-henshin-transformation": "page 404 on 2026-11-19",
        "big-guy-ai-dance": "page 404 on 2026-11-19",
        "chibi-anime-romance": "page 404 on 2026-11-19",
        "cleaning-lady": "page 404 on 2026-11-19",
        "cops-at-the-door": "page 404 on 2026-11-19",
        "dark-warrior-henshin-transformation": "page 404 on 2026-11-19",
        "fit-check-ai-video": "page 404 on 2026-11-19",
        "generate-a-man-next-to-me-ai-video": "page 404 on 2026-11-19",
        "homeless-man": "page 404 on 2026-11-19",
        "kitchen-fire": "page 404 on 2026-11-19",
        "nunchaku": "page 404 on 2026-11-19",
        "put-a-mind-chip-ai-video": "page 404 on 2026-11-19",
        "quiero-verte-venir-ai-dance": "page 404 on 2026-11-19",
        "samurai-henshin-transformation": "page 404 on 2026-11-19",
        "shirtless-plumber": "page 404 on 2026-11-19",
        "snake-in-the-kitchen": "page 404 on 2026-11-19",
        "tiptoeing-in-my-jordans-ai-video": "page 404 on 2026-11-19",
        "tokyo-drift-ai-dance": "page 404 on 2026-11-19",
        "vibes-ai-dance": "page 404 on 2026-11-19",
        "zombie-love-story-ai-video": "page 404 on 2026-11-19",
}
DROP_SLUGS = {
    "starrd.json": STARRD_404,
    "putmein.json": {
        "ateez-bad-dance-challenge-ai": "renamed to bad-dance-challenge-ai-trend",
        "bulin-47-dance-ai-trend": "renamed to dame-hombro-dance-ai-trend (redirect)",
        "catel-madatorricelli-ai-dance": "renamed to catel-courtyard-dance-ai-trend (redirect)",
    },
}

# Keep in inventory if missing from sitemap but page still 200.
KEEP_MISSING = {
    "summrs.json": {"bigfoot-vlog"},
    "tryatrend.json": {"ai-halloween-costume"},
}


def title_from_slug(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def build_notice(curated_new, nosmew, smew_only, total_new, putmein_bulk_count, putmein_total):
    by_site = OrderedDict()
    for x in curated_new:
        by_site.setdefault(x["site"], []).append(x)

    lines = []
    n_sites = len(by_site)
    lines.append("竞品模板日报（2026-11-19，上海时间）")
    lines.append("")
    lines.append(
        f"今日共 {total_new} 个新模板，分布在 {n_sites} 家。已核实页面可打开；"
        "解析误伤（分类页/聚合页/FAQ/SEO 变体/通用工具页）未计入。"
    )
    lines.append("")
    if putmein_bulk_count:
        lines.append(
            f"另：Put Me In 继续把 11-15 的 sitemap 回填写入快照（lastmod 均为 2026-11-15），"
            f"今日再入库 {putmein_bulk_count} 条（快照增至 {putmein_total}；不在此逐条列出）；"
            "与今日他站新增撞车的见文末「多家共有」。"
        )
        lines.append("")
    for site, items in by_site.items():
        lines.append(f"【{site}】{len(items)} 个")
        for x in items:
            it = x["item"]
            lines.append(f"- {it['title']}：{x['desc']}")
            lines.append(f"  {it['url']}")
        lines.append("")

    lines.append("【多家共有】")
    mutual = [o for o in nosmew if len(o["new_sites"]) >= 2]
    vs = [o for o in nosmew if len(o["new_sites"]) == 1]
    if not nosmew and not smew_only:
        lines.append("今日无多家共有")
    else:
        if mutual:
            lines.append("今日新增互相撞车：")
            for o in sorted(mutual, key=lambda x: (-x["site_count"], -len(x["new_sites"]), x["name"].lower())):
                bits = []
                for s in o["sites"]:
                    tag = "（新）" if s["is_new"] else "（存量）"
                    bits.append(f"{s['site']}{tag} {s['url']}")
                smew_note = ""
                if o.get("smew"):
                    smew_note = f" ｜ 另有 Smew AI（存量） {o['smew']['url']}"
                lines.append(
                    f"· {o['name']}（{o['site_count']} 家，今日新增 {len(o['new_sites'])} 家）："
                    + " ｜ ".join(bits) + smew_note
                )
            lines.append("")
        if vs:
            lines.append("今日新增与他站存量撞车：")
            for o in sorted(vs, key=lambda x: (-x["site_count"], x["name"].lower())):
                bits = []
                for s in o["sites"]:
                    tag = "（新）" if s["is_new"] else "（存量）"
                    bits.append(f"{s['site']}{tag} {s['url']}")
                smew_note = ""
                if o.get("smew"):
                    smew_note = f" ｜ 另有 Smew AI（存量） {o['smew']['url']}"
                lines.append(f"· {o['name']}（{o['site_count']} 家）：" + " ｜ ".join(bits) + smew_note)
            lines.append("")
        if smew_only:
            lines.append("今日新增只与 Smew AI 存量撞车：")
            for o in smew_only:
                news = [s for s in o["sites"] if s["is_new"]]
                smew = next(s for s in o["sites"] if s["site"] == "Smew AI")
                bits = [f"{s['site']}（新） {s['url']}" for s in news]
                bits.append(f"Smew AI（存量） {smew['url']}")
                lines.append(f"· {o['name']}（{o['site_count']} 家）：" + " ｜ ".join(bits))
    return "\n".join(lines).rstrip() + "\n"


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


def main():
    fetch = json.load(open(os.path.join(OUTDIR, "fetch_results.json")))
    prevs = {}
    for fn, (site, home) in HOMES.items():
        prevs[fn] = json.load(open(os.path.join(STORE, fn)))

    site_out = {}
    curated_new = []
    filtered = []
    notes_by_file = {}
    putmein_bulk = []

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

        genuine_slugs = {g["id_or_slug"].lower() for g in genuine}

        if fn == "putmein.json":
            # Catalog/sitemap backfill: add all new /templates/{slug} to inventory,
            # but do not treat as day-over-day "今日新上线" in the user digest.
            for t in raw_new:
                rec = {
                    "id_or_slug": t["id_or_slug"],
                    "title": t.get("title") or title_from_slug(t["id_or_slug"]),
                    "url": t["url"],
                }
                putmein_bulk.append(rec)
            genuine_for_store = list(putmein_bulk)
        else:
            genuine_for_store = list(genuine)
            inv_only = INVENTORY_ONLY.get(site, [])
            inv_slugs = set()
            for item in inv_only:
                rec = {"id_or_slug": item["id_or_slug"], "title": item["title"], "url": item["url"]}
                if rec["id_or_slug"].lower() not in {g["id_or_slug"].lower() for g in genuine_for_store}:
                    genuine_for_store.append(rec)
                    inv_slugs.add(rec["id_or_slug"].lower())
            skip_filter = genuine_slugs | inv_slugs
            for t in raw_new:
                if t["id_or_slug"].lower() not in skip_filter:
                    reason = FILTER_REASONS.get((fn, t["id_or_slug"].lower()), "parser-drift-or-non-template")
                    filtered.append({"site": site, "file": fn, "item": t, "reason": reason})

        fetch_ok = bool(fr.get("fetch_ok"))
        sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        sitemap_existed = bool(fr.get("sitemap_existed") or sitemap_urls)
        update_store = True
        site_notes = []

        if fn == "ricebowl.json":
            site_notes.append(
                "Meme catalog (/trends/meme ItemList) unchanged vs yesterday (84 claimed / 0 genuine new). "
                "Generic /app tool pages and parse junk not added."
            )
            fetch_ok = True
            sitemap_existed = True
            sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        elif fn == "remakeyourmeme.json":
            site_notes.append("Sitemap via WebFetch; box IP still 403; inventory unchanged (44).")
            fetch_ok = True
            sitemap_existed = True
            sitemap_urls = ["https://remakeyourmeme.com/sitemap.xml"]
        elif fn == "putmein.json" and putmein_bulk:
            site_notes.append(
                f"Put Me In inventory-only additions: {len(putmein_bulk)}; not listed in the daily digest."
            )
        elif fn == "starrd.json":
            inv_only = INVENTORY_ONLY.get(site, [])
            if inv_only:
                site_notes.append(
                    "Need for Speed (Extended) added to inventory as a longer cut, not listed separately in the digest."
                )
            site_notes.append(
                "Dropped 23 templates whose pages returned 404 today; not itemized in the digest."
            )

        drop_map = DROP_SLUGS.get(fn, {})
        keep_set = KEEP_MISSING.get(fn, set())
        removed_now = []

        templates = []
        for t0 in prev_tmpls:
            slug = t0["id_or_slug"].lower()
            if slug in drop_map:
                removed_now.append(t0)
                site_notes.append(f"Dropped {t0['id_or_slug']}: {drop_map[slug]}.")
                continue
            if fetch_ok and fn not in {"ricebowl.json", "remakeyourmeme.json"}:
                if slug not in now_slugs and slug not in {g["id_or_slug"].lower() for g in genuine_for_store}:
                    if slug in keep_set:
                        site_notes.append(
                            f"Kept {t0['id_or_slug']} despite missing from today's sitemap (page still 200)."
                        )
                        templates.append(t0)
                        continue
                    # default: keep rather than delete unverified disappearances
                    site_notes.append(
                        f"Kept {t0['id_or_slug']} despite missing from today's sitemap."
                    )
            templates.append(t0)

        have = {t0["id_or_slug"].lower() for t0 in templates}
        for g in genuine_for_store:
            if g["id_or_slug"].lower() not in have:
                templates.append({"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]})
                have.add(g["id_or_slug"].lower())
        templates.sort(key=lambda t0: t0["url"])

        rec = {
            "site": site,
            "home": home,
            "checked_at": CHECKED_AT,
            "sitemap_urls_found": sitemap_urls,
            "sitemap_existed": sitemap_existed,
            "template_count": len(templates),
            "templates": templates,
            "new_count": len(genuine_for_store),
            "removed_count": len(removed_now),
            "new_templates": [
                {"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]}
                for g in genuine_for_store
            ],
            "removed_templates": [
                {"id_or_slug": x["id_or_slug"], "title": x.get("title") or x["id_or_slug"], "url": x.get("url")}
                for x in removed_now
            ],
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
            "store_new": len(genuine_for_store),
            "filtered": sum(1 for x in filtered if x["file"] == fn),
        }
        site_out[fn] = rec

        with open(os.path.join(STORE, fn), "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
            f.write("\n")

    # Update excluded-non-templates with newly confirmed non-templates
    excl_path = os.path.join(STORE, "excluded-non-templates.json")
    excl = json.load(open(excl_path))
    by_file = excl.setdefault("by_file", {})
    extras = {
        "makememe.json": ["christmas-ai-video-trends", "questions"],
        "memelry.json": [
            "cortis-go-ai-from-photo",
            "how-to-make-no-scrubs-ai-video",
            "wassup-dance-face-expression-guide",
            "wassup-dance-with-three-friends",
            "atm-christmas-wish-meaning",
            "gta-next-chapter-meaning",
            "singing-pet-photo-guide",
            "the-jawn-meaning",
        ],
        "starrd.json": ["birthday", "effects", "famous"],
        "trendtemplate.json": [
            "ai-christmas-video", "ai-dance", "ai-photo-creator", "ai-trend-templates",
            "how-to-make-rooftop-groove-ai-video", "photo-template", "refund-policy",
            "report", "tiktok-ai-trends", "video-template-online",
        ],
        "kubflow.json": ["generations"],
    }
    for fn, slugs in extras.items():
        cur = list(by_file.get(fn, []))
        for s in slugs:
            if s not in cur:
                cur.append(s)
        by_file[fn] = cur
    with open(excl_path, "w", encoding="utf-8") as f:
        json.dump(excl, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ledger
    ledger_sites = []
    total_templates = 0
    total_store_new = 0
    total_digest_new = len(curated_new)
    for fn, (site, home) in HOMES.items():
        rec = site_out[fn]
        total_templates += rec["template_count"]
        new_c = rec["new_count"]
        total_store_new += new_c
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
        "total_new": total_store_new,
        "total_digest_new": total_digest_new,
        "putmein_bulk_new": len(putmein_bulk),
        "total_removed": 0,
        "sites_count": 28,
        "sites_updated": 28,
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
                "sites_updated": 28,
                "total_templates": total_templates,
                "total_new": total_store_new,
                "total_digest_new": total_digest_new,
                "putmein_bulk_new": len(putmein_bulk),
                "total_removed": 0,
            },
            "per_site": notes_by_file,
        }, f, ensure_ascii=False, indent=2)
        f.write("\n")

    curated_list = [{"site": x["site"], "file": x["file"], "item": x["item"], "desc": x["desc"]} for x in curated_new]
    with open(os.path.join(OUTDIR, "curated_new.json"), "w", encoding="utf-8") as f:
        json.dump(curated_list, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(OUTDIR, "filtered_out.json"), "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(OUTDIR, "putmein_bulk.json"), "w", encoding="utf-8") as f:
        json.dump(putmein_bulk, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Overlaps on CURRENT full inventories; "is_new" only for digest curated items
    new_index = {(x["site"], x["item"]["id_or_slug"].lower()): True for x in curated_new}

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
    overlaps.sort(key=lambda o: (-len(o["new_sites"]), -o["site_count"], o["name"].lower()))
    with open(os.path.join(OUTDIR, "overlaps-today.json"), "w", encoding="utf-8") as f:
        json.dump(overlaps, f, ensure_ascii=False, indent=2)
        f.write("\n")

    involving_new = [o for o in overlaps if o["new_sites"]]
    nosmew = []
    smew_only = []
    for o in involving_new:
        w = without_smew(o)
        if w and w["new_sites"] and w["site_count"] >= 2:
            nosmew.append(w)
        elif o["new_sites"] and any(s["site"] == "Smew AI" for s in o["sites"]):
            others = [s for s in o["sites"] if s["site"] != "Smew AI"]
            if others and all(s["is_new"] or s["site"] == "Smew AI" for s in o["sites"]) and len([s for s in o["sites"] if not s["is_new"] and s["site"] != "Smew AI"]) == 0:
                # only collide with Smew among stock, or only Smew + today's new
                if len([s for s in o["sites"] if (not s["is_new"])]) == 1 and any(s["site"]=="Smew AI" and not s["is_new"] for s in o["sites"]):
                    smew_only.append(o)

    mutual_ns = [o for o in nosmew if len(o["new_sites"]) >= 2]
    vs_ns = [o for o in nosmew if len(o["new_sites"]) == 1]

    lines = [
        f"去掉 [Smew AI](https://smew.ai/) 后，今天「多家共有」还剩 {len(nosmew)} 条："
        f"{len(mutual_ns)} 条是同一梗今天在多家新上线，{len(vs_ns)} 条是今日新增对上他站存量。"
    ]
    lines.append("")
    lines.append("一、今日新增互相撞车（同一梗今天在多家新上线）")
    lines.append("")
    if not mutual_ns:
        lines.append("（无）")
    else:
        for o in mutual_ns:
            bits = [f"{s['site']}{'（新）' if s['is_new'] else '（存量）'} {s['url']}" for s in o["sites"]]
            lines.append(f"- {o['name']}（{o['site_count']} 家）：" + " ｜ ".join(bits))
    lines.append("")
    lines.append("二、今日新增与他站存量撞车")
    lines.append("")
    if not vs_ns:
        lines.append("（无）")
    else:
        for o in vs_ns:
            bits = [f"{s['site']}{'（新）' if s['is_new'] else '（存量）'} {s['url']}" for s in o["sites"]]
            lines.append(f"- {o['name']}（{o['site_count']} 家）：" + " ｜ ".join(bits))
    with open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-19.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    putmein_total = site_out["putmein.json"]["template_count"]
    notice = build_notice(
        curated_new, nosmew, smew_only, total_digest_new,
        len(putmein_bulk), putmein_total,
    )
    with open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8") as f:
        f.write(notice)
    with open(os.path.join(OUTDIR, "竞品模板日报-2026-11-19.md"), "w", encoding="utf-8") as f:
        f.write(notice)

    print("checked_at", CHECKED_AT)
    print("digest_new", total_digest_new, "store_new", total_store_new, "putmein_bulk", len(putmein_bulk))
    print("total_templates", total_templates)
    print("filtered", len(filtered))
    print("overlaps", len(overlaps), "involving_new", len(involving_new),
          "nosmew", len(nosmew), "mutual_ns", len(mutual_ns), "smew_only", len(smew_only))
    print("NOTICE_CHARS", len(notice))


if __name__ == "__main__":
    main()
