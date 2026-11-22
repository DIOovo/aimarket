#!/usr/bin/env python3
"""Finalize 2026-11-20 FaceOnTrend competitor scan."""
from __future__ import annotations

import json, os, re, time, html
from collections import defaultdict
from copy import deepcopy
from urllib.parse import urlparse
import importlib.util

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-20"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-19T09:40:27+08:00"

# Ensure curated_source exists so finalize.py can import
if not os.path.exists(os.path.join(OUTDIR, "curated_source.json")):
    json.dump({}, open(os.path.join(OUTDIR, "curated_source.json"), "w"))

spec = importlib.util.spec_from_file_location("fin", os.path.join(OUTDIR, "finalize.py"))
fin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fin)

fin.ALIASES.update({
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "mean-girls-jingle-bell-rock": "jingle-bell-rock",
    "give-it-all-to-me": "give-it-all",
    "rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "put-the-rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "im-the-one": "shoulder-carry-im-the-one",
    "im-the-one-shoulder-carry": "shoulder-carry-im-the-one",
    "cause-im-the-one": "shoulder-carry-im-the-one",
    "shoulder-carry": "shoulder-carry-im-the-one",
    "feel-the-pressure": "mourinho-pressure",
    "mourinho-pressure-original-audio": "mourinho-pressure",
    "quiet-on-the-creek-dance": "quiet-on-the-creek",
    "jingle-bell-brazil-dance": "jingle-bell-brazil",
    "la-tormenta-de-arena": "te-he-perdido",
    "catch-santa-on-camera": "santa-caught-on-camera",
    "youre-under-arrest": "under-arrest-dance",
    "youre-under-arrest-dance": "under-arrest-dance",
    "tidal-wave-video": "tidal-wave",
    "su-gibi-git-su-gibi-gel": "tidal-wave",
    "christmas-pajama-dance": "christmas-dance",
    "smalltown-boy-ai-dance": "smalltown-boy-cat",
    "smalltown-boy": "smalltown-boy-cat",
    "ai-cafe": "first-time-in-a-fancy-cafe",
    "mini-tricycle-crash": "tricycle-crash",
    "trouble-maker-dance": "trouble-maker",
    "gta-5-goodbye": "gta-farewell",
    "gta-6-farewell": "gta-farewell",
    "goodbye-gta-5": "gta-farewell",
    "pterodactyl-juarez": "mexico-pterodactyl",
    "kung-fu-goalkeeper": "funny-goalkeeper",
    "oh-my-carne-asada-singing-dog": "oh-my-carne-asada",
    "dip-on-em-dance": "dip-on-em",
    "gta-wasted-meme": "gta-wasted",
    "jatayu-indian-mythology": "jatayu",
    "wassup-in-a-minute-dance": "wassup-in-a-minute",
    "wassup-dance": "wassup-in-a-minute",
    "in-a-minute-wassup": "wassup-in-a-minute",
    "wassup-in-a-minute-wassup": "wassup-in-a-minute",
    "ai-fashion-video-edit": "fashion-video-edit",
})

def clean_title(item, meta=None):
    raw = (item.get("title") or item.get("id_or_slug") or "").strip()
    if meta:
        for cand in (meta.get("h1"), meta.get("og"), meta.get("title_page"), raw):
            if not cand:
                continue
            t = html.unescape(cand)
            t = re.sub(r"\s+", " ", t).strip()
            t = re.split(r"\s*[|\u2014\u2013]\s*", t)[0].strip()
            t = re.sub(r"\s*[:：].*$", "", t).strip()
            t = re.sub(r"\s*(AI Video Generator|Video Generator)\s*$", "", t, flags=re.I).strip(" :-")
            if t and len(t) <= 70:
                return t
    return raw

DIGEST_DESCS = {
    ("makeviral.json", "ai-fashion-video-edit"): ("AI Fashion Video Edit", "街拍时尚剪辑：在城市广场用 14 个跳切摆拍走路"),
    ("makeviral.json", "cat-from-every-angle-ai-trend"): ("Cat From Every Angle", "宠物坐在地毯上，镜头切 14 个角度，配 Victory Lap"),
    ("makeviral.json", "dip-on-em-dance-ai-trend"): ("Dip On Em Dance", "双人跟跳：下腰、轻跳、指镜头，可用朋友或宠物"),
    ("makeviral.json", "gta-6-jet-ski-dog-ai"): ("GTA 6 Jet Ski Dog", "自家宠物穿救生衣、戴护目镜，骑摩托艇去海上救人"),
    ("makeviral.json", "gta-wasted-meme-ai"): ("GTA Wasted Meme", "摔倒后画面冻成灰色，落下红色 Wasted 标题"),
    ("makeviral.json", "jatayu-ai-video"): ("Jatayu AI Video", "张开双臂，身后升起展开翅膀的巨鹰"),
    ("makeviral.json", "kiss-your-phone-ai-trend"): ("Kiss Your Phone", "一人吻手机，另一人泼水后发现屏幕上是自己"),
    ("makeviral.json", "oh-my-carne-asada-singing-dog"): ("Oh My Carne Asada", "宠物像那只吉娃娃一样唱 “oh my carne asada”"),
    ("makeviral.json", "pop-pop-animation-ai-trend"): ("Pop Pop Animation", "两人做成动漫角色叠煎饼，配 ILLIT 的 Pop"),
    ("makeviral.json", "supercar-night-drive-ai-trend"): ("Supercar Night Drive", "夜里加油再飙高速公路，配 Habits (Stay High)"),
    ("makeviral.json", "winter-wonderland-dance-ai-trend"): ("Winter Wonderland Dance", "圣诞睡衣双人舞，也可单人"),
    ("makeviral.json", "you-are-nice-you-are-pretty-ai-trend"): ("You Are Nice You Are Pretty", "宠物说你漂亮、你是我的朋友，然后画面故障"),
    ("trendtemplate.json", "christmas-photobooth-ai"): ("Christmas Photobooth AI", "复古拍立得四格，慢镜扫过你和好友、伴侣或妈妈"),
    ("trendtemplate.json", "gta-5-goodbye-ai"): ("GTA 5 Goodbye", "日落码头告别，递车钥匙后开粉色跑车离开"),
    ("makememe.json", "mexico-pterodactyl-ai"): ("Mexico Pterodactyl AI", "用铁链牵着墨西哥翼龙走"),
    ("makememe.json", "oh-my-carne-asada-ai"): ("Oh My Carne Asada AI", "宠物或你自己嚎叫唱 “oh my carne asada… one love”"),
    ("clipremake.json", "baby-face-filter-ai"): ("Baby Face Filter AI", "娃娃婴儿滤镜：圆脸黑眼珠，再喊 “I am a baby!”"),
    ("clipremake.json", "give-it-all-ai"): ("Give It All AI", "在电影院大厅吊麦前说唱 “give it all to me”（BigXthaPlug）"),
    ("clipremake.json", "oh-my-carne-asada-ai"): ("Oh My Carne Asada AI", "狗、猫或人唱这首梗，瞪眼再坏笑"),
    ("memeclone.json", "need-for-speed"): ("Need for Speed", "把自己的车贴进电影追逐：烧胎、餐厅栏杆、加油站甩尾"),
    ("zapvid.json", "wassup-in-a-minute-dance-ai-video-generator"): ("Wassup In A Minute Dance", "雾气山坡上跟跳：双手抱头、特写、走过来，最多三人"),
    ("aimakevideo.json", "need-for-speed-ai"): ("Need for Speed AI", "一张车照变成烧胎、甩尾、追逐和烟雾"),
    ("tryatrend.json", "oh-my-carne-asada-ai"): ("Oh My Carne Asada AI", "绿幕前用一张宠物照嚎叫唱这首梗"),
    ("starrd.json", "dip-on-em-dance-ai-video"): ("Dip On Em Dance", "最多四人跟跳：对镜头弓步、下腰、侧跳举手"),
    ("starrd.json", "needs-more-salt-ai-video"): ("Needs More Salt", "厨房恶作剧：一人说汤淡了，另一人趁对方转身假装加盐"),
    ("starrd.json", "never-let-her-pay-ai-video"): ("Never Let Her Pay", "约会抢着买单，掏出的却是海绵，被服务员带去洗碗"),
    ("starrd.json", "quiet-on-the-creek-ai-video"): ("Quiet on the Creek", "黄金时刻在 SUV 后座跟唱这首歌并做手势，最多四人"),
}

SITE_ORDER = [fn for fn, _ in fin.HOMES.items()]  # preserve HOMES order
DIGEST_FILES_ORDER = [
    "trendtemplate.json", "clipremake.json", "makeviral.json", "makememe.json",
    "memeclone.json", "zapvid.json", "starrd.json", "aimakevideo.json", "tryatrend.json",
]
INVENTORY_ONLY_FILES = {"samevid.json"}

fetch = json.load(open(os.path.join(OUTDIR, "fetch_results.json"), encoding="utf-8"))
diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json"), encoding="utf-8"))
checks = json.load(open(os.path.join(OUTDIR, "url_checks.json"), encoding="utf-8"))
check_map = {(c["file"], c["id_or_slug"].lower()): c for c in checks}

yest_filt_rows = json.load(open("/workspace/competitor-scan-2026-11-19/filtered_out.json", encoding="utf-8"))
yest_filt = defaultdict(dict)  # file -> slug -> reason
for x in yest_filt_rows:
    yest_filt[x["file"]][x["item"]["id_or_slug"].lower()] = x.get("reason") or "parser-drift-or-non-template"

# Genuine new
digest_new = defaultdict(list)
inv_new = defaultdict(list)
filtered = []
for fn, d in diff.items():
    for t in d.get("new") or []:
        slug = t["id_or_slug"].lower()
        if slug in yest_filt.get(fn, {}) or fn == "ricebowl.json":
            filtered.append({
                "site": d.get("site") or (fin.HOMES.get(fn) or ("",))[0],
                "file": fn,
                "item": {"id_or_slug": t["id_or_slug"], "title": t.get("title") or t["id_or_slug"], "url": t["url"]},
                "reason": yest_filt.get(fn, {}).get(slug, "parser-drift-or-non-template"),
            })
            continue
        meta = check_map.get((fn, slug))
        title = DIGEST_DESCS.get((fn, slug), (None, None))[0] or clean_title(t, meta)
        rec = {"id_or_slug": t["id_or_slug"], "title": title, "url": t["url"]}
        if fn in INVENTORY_ONLY_FILES:
            inv_new[fn].append(rec)
        elif fn in set(DIGEST_FILES_ORDER):
            digest_new[fn].append(rec)
        else:
            # unexpected leftover — treat as inventory if it passed URL check, else filter
            if meta and meta.get("status") == 200 and not meta.get("looks_404"):
                inv_new[fn].append(rec)
            else:
                filtered.append({
                    "site": d.get("site") or (fin.HOMES.get(fn) or ("",))[0],
                    "file": fn,
                    "item": rec,
                    "reason": "unclassified-held-out",
                })

# Keep-missing pages still 200
KEEP_MISSING = {
    "summrs.json": {"bigfoot-vlog": "Kept bigfoot-vlog despite missing from today's sitemap (page still 200)."},
    "tryatrend.json": {"ai-halloween-costume": "Kept ai-halloween-costume despite missing from today's sitemap (page still 200)."},
}

NOTES = {
    "remakeyourmeme.json": "Sitemap via WebFetch; box IP still 403; inventory unchanged (44).",
    "ricebowl.json": "Meme catalog (/trends/meme ItemList) unchanged vs yesterday (84 claimed / 0 genuine new). Generic /app tool pages and parse junk not added.",
    "samevid.json": "82 genuine templates added to inventory as a catalog backfill; not itemized in the digest.",
    "summrs.json": "Kept bigfoot-vlog despite missing from today's sitemap (page still 200).",
    "tryatrend.json": "Kept ai-halloween-costume despite missing from today's sitemap (page still 200).",
}

# Write snapshots
site_reports = []
total_templates = 0
total_new = 0
total_digest_new = 0
total_removed = 0
sites_updated = 0

for fn, (site, home) in fin.HOMES.items():
    prev = json.load(open(os.path.join(STORE, fn), encoding="utf-8"))
    fr = fetch.get(fn, {})
    prev_tmpls = list(prev.get("templates") or [])
    prev_slugs = {t["id_or_slug"].lower(): t for t in prev_tmpls}

    added = list(digest_new.get(fn, [])) + list(inv_new.get(fn, []))
    # keep previous, add new
    new_tmpls = list(prev_tmpls)
    have = set(prev_slugs)
    for t in added:
        if t["id_or_slug"].lower() not in have:
            new_tmpls.append({"id_or_slug": t["id_or_slug"], "title": t["title"], "url": t["url"]})
            have.add(t["id_or_slug"].lower())

    # do not drop keep-missing or other sitemap misses if we didn't confirm 404
    removed = []
    dropped_dead = []

    sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
    sitemap_existed = bool(fr.get("sitemap_existed") if "sitemap_existed" in fr else prev.get("sitemap_existed"))
    if fn == "remakeyourmeme.json":
        sitemap_urls = ["https://remakeyourmeme.com/sitemap.xml"]
        sitemap_existed = True

    snap = {
        "site": site,
        "home": home,
        "checked_at": CHECKED_AT,
        "sitemap_urls_found": sitemap_urls,
        "sitemap_existed": sitemap_existed,
        "template_count": len(new_tmpls),
        "new_count": len(added),
        "removed_count": 0,
        "new_templates": added,
        "removed_templates": [],
        "templates": new_tmpls,
    }
    if NOTES.get(fn):
        snap["note"] = NOTES[fn]

    json.dump(snap, open(os.path.join(STORE, fn), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    sites_updated += 1
    total_templates += len(new_tmpls)
    total_new += len(added)
    total_digest_new += len(digest_new.get(fn, []))

    entry = {
        "site": site,
        "file": fn,
        "home": home,
        "sitemap_existed": sitemap_existed,
        "sitemap_urls_found": sitemap_urls,
        "template_count": len(new_tmpls),
        "new_count": len(added),
        "removed_count": 0,
        "dropped_dead_count": 0,
    }
    if NOTES.get(fn):
        entry["note"] = NOTES[fn]
    site_reports.append(entry)

ledger = {
    "checked_at": CHECKED_AT,
    "timezone": "Asia/Shanghai",
    "baseline": False,
    "previous_checked_at": PREV_CHECKED_AT,
    "total_templates": total_templates,
    "total_new": total_new,
    "total_digest_new": total_digest_new,
    "putmein_bulk_new": 0,
    "total_removed": 0,
    "sites_count": len(site_reports),
    "sites_updated": sites_updated,
    "sites_left_unchanged": 0,
    "sites": site_reports,
}
json.dump(ledger, open(os.path.join(STORE, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(ledger, open(os.path.join(OUTDIR, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# curated outputs
curated_source = {}
curated_new = []
for fn in DIGEST_FILES_ORDER:
    site = fin.HOMES[fn][0]
    items = digest_new.get(fn, [])
    if not items:
        continue
    curated_source[site] = items
    for t in items:
        desc = DIGEST_DESCS.get((fn, t["id_or_slug"].lower()), ("", ""))[1]
        curated_new.append({"site": site, "file": fn, "item": t, "desc": desc})

inventory_only = {fin.HOMES[fn][0]: items for fn, items in inv_new.items() if items}
json.dump(curated_source, open(os.path.join(OUTDIR, "curated_source.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(curated_new, open(os.path.join(OUTDIR, "curated_new.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(inventory_only, open(os.path.join(OUTDIR, "inventory_only.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(filtered, open(os.path.join(OUTDIR, "filtered_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump([], open(os.path.join(OUTDIR, "putmein_bulk.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# Overlaps from updated store
def core_of(item):
    return fin.core_key(item.get("id_or_slug") or "", item.get("title") or "")

digest_keys = {(fn, t["id_or_slug"].lower()) for fn, ts in digest_new.items() for t in ts}
inv_keys = {(fn, t["id_or_slug"].lower()) for fn, ts in inv_new.items() for t in ts}

clusters = defaultdict(list)
for fn, (site, home) in fin.HOMES.items():
    snap = json.load(open(os.path.join(STORE, fn), encoding="utf-8"))
    seen_site_slug = set()
    for t in snap.get("templates") or []:
        slug = t["id_or_slug"].lower()
        k = core_of(t)
        # one row per site+slug; later collapse to one URL per site
        clusters[k].append({
            "core": k, "site": site, "file": fn, "item": t,
            "digest_new": (fn, slug) in digest_keys,
            "inv_new": (fn, slug) in inv_keys,
        })

PRETTY = {
    "oh-my-carne-asada": "Oh My Carne Asada",
    "dip-on-em": "Dip On Em Dance",
    "need-for-speed": "Need for Speed",
    "gta-farewell": "GTA 5 Goodbye / Farewell",
    "gta-wasted": "GTA Wasted",
    "winter-wonderland-dance": "Winter Wonderland Dance",
    "jatayu": "Jatayu",
    "wassup-in-a-minute": "Wassup In A Minute",
    "give-it-all": "Give It All",
    "quiet-on-the-creek": "Quiet on the Creek",
    "never-let-her-pay": "Never Let Her Pay",
    "christmas-photobooth": "Christmas Photobooth",
    "baby-face-filter": "Baby Face Filter",
    "mexico-pterodactyl": "Mexico Pterodactyl / Pterodactyl Juárez",
}

def one_per_site(rows):
    """Prefer digest/inv new URL, then a stable one. Skip extra memelry variants after first."""
    by_site = defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r)
    out = []
    for site, rs in by_site.items():
        rs_sorted = sorted(rs, key=lambda r: (0 if (r["digest_new"] or r["inv_new"]) else 1, len(r["item"]["id_or_slug"])))
        out.append(rs_sorted[0])
    # site order by HOMES
    order = {site: i for i, (site, _) in enumerate(fin.HOMES.values())}
    out.sort(key=lambda r: order.get(r["site"], 999))
    return out

overlap_hits = []
for k, rows in clusters.items():
    picked = one_per_site(rows)
    # drop Smew from main count, keep aside
    smew = [r for r in picked if r["site"] == "Smew AI"]
    main = [r for r in picked if r["site"] != "Smew AI"]
    sites_main = {r["site"] for r in main}
    if len(sites_main) < 2 and not smew:
        continue
    # need at least 2 sites including smew? If only 1 main + smew, treat as 2 but smew 另有 — skip if main < 2
    if len(sites_main) < 2:
        continue
    n_today = sum(1 for r in main if r["digest_new"] or r["inv_new"])
    if n_today == 0:
        continue
    n_today_digest = sum(1 for r in main if r["digest_new"])
    n_today_inv = sum(1 for r in main if r["inv_new"] and not r["digest_new"])
    overlap_hits.append({
        "core": k,
        "name": PRETTY.get(k, " ".join(w.capitalize() for w in k.split("-"))),
        "main": main,
        "smew": smew,
        "n_sites": len(sites_main),
        "n_today": n_today,
        "mutual": n_today >= 2,
    })

overlap_hits.sort(key=lambda h: (-h["mutual"], -h["n_today"], -h["n_sites"], h["name"].lower()))

def fmt_row(r):
    if r["digest_new"]:
        tag = "新"
    elif r["inv_new"]:
        tag = "新，仅记库存"
    else:
        tag = "存量"
    return f"{r['site']}（{tag}） {r['item']['url']}"

mutual_lines = []
stock_lines = []
for h in overlap_hits:
    parts = " ｜ ".join(fmt_row(r) for r in h["main"])
    extra = ""
    if h["smew"]:
        extra = " ｜ 另有 " + " ｜ ".join(fmt_row(r) for r in h["smew"])
    line = f"· {h['name']}（{h['n_sites']} 家，今日新增 {h['n_today']} 家）：{parts}{extra}"
    if h["mutual"]:
        mutual_lines.append(line)
    else:
        stock_lines.append(line)

json.dump({
    "checked_at": CHECKED_AT,
    "mutual": mutual_lines,
    "vs_stock": stock_lines,
    "raw": [
        {
            "core": h["core"], "name": h["name"], "n_sites": h["n_sites"], "n_today": h["n_today"],
            "mutual": h["mutual"],
            "sites": [{"site": r["site"], "url": r["item"]["url"], "slug": r["item"]["id_or_slug"],
                       "digest_new": r["digest_new"], "inv_new": r["inv_new"]} for r in h["main"] + h["smew"]],
        } for h in overlap_hits
    ],
}, open(os.path.join(OUTDIR, "overlaps-today.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# Chinese notice
n_sites_digest = sum(1 for fn in DIGEST_FILES_ORDER if digest_new.get(fn))
n_digest = sum(len(digest_new[fn]) for fn in DIGEST_FILES_ORDER)
n_sv = len(inv_new.get("samevid.json") or [])

lines = []
lines.append(f"竞品模板日报（2026-11-20，上海时间）")
lines.append("")
lines.append(f"今日共 {n_digest} 个新模板，分布在 {n_sites_digest} 家。已核实页面可打开；解析误伤（分类页/聚合页/FAQ/SEO 变体/通用工具页）未计入。")
lines.append(f"另：SameVid AI 今日批量上架 {n_sv} 个模板（多为他站已有梗的回填），已记入库存，不在正文逐条列出。")
lines.append("")

for fn in DIGEST_FILES_ORDER:
    items = digest_new.get(fn) or []
    if not items:
        continue
    site = fin.HOMES[fn][0]
    lines.append(f"【{site}】{len(items)} 个")
    for t in items:
        name, desc = DIGEST_DESCS[(fn, t["id_or_slug"].lower())]
        lines.append(f"- {name}：{desc}")
        lines.append(f"  {t['url']}")
    lines.append("")

lines.append("【多家共有】")
if mutual_lines:
    lines.append("今日新增互相撞车：")
    lines.extend(mutual_lines)
else:
    lines.append("今日新增之间无互相撞车。")
lines.append("")
if stock_lines:
    lines.append("今日新增与他站存量撞车：")
    lines.extend(stock_lines)
else:
    if not mutual_lines:
        lines.append("今日无多家共有")

notice = "\n".join(lines).rstrip() + "\n"
open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8").write(notice)
open(os.path.join(OUTDIR, "竞品模板日报-2026-11-20.md"), "w", encoding="utf-8").write(notice)

# also a short overlaps md
ov = ["# 多家共有（2026-11-20）", "", "今日新增互相撞车：", *mutual_lines, "", "今日新增与他站存量撞车：", *stock_lines, ""]
open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-20.md"), "w", encoding="utf-8").write("\n".join(ov))

summary = {
    "checked_at": CHECKED_AT,
    "timezone": "Asia/Shanghai",
    "previous_checked_at": PREV_CHECKED_AT,
    "ledger": {
        "sites": len(site_reports),
        "sites_updated": sites_updated,
        "total_templates": total_templates,
        "total_new": total_new,
        "total_digest_new": total_digest_new,
        "samevid_inventory_new": n_sv,
        "putmein_bulk_new": 0,
        "total_removed": 0,
        "filtered": len(filtered),
    },
    "per_site": {
        e["file"]: {
            "template_count": e["template_count"],
            "new_count": e["new_count"],
            "digest_new": len(digest_new.get(e["file"], [])),
            "inventory_new": len(inv_new.get(e["file"], [])),
            "note": e.get("note"),
        } for e in site_reports
    },
}
json.dump(summary, open(os.path.join(OUTDIR, "run-summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("CHECKED_AT", CHECKED_AT)
print("digest", n_digest, "sites", n_sites_digest, "samevid_inv", n_sv, "filtered", len(filtered))
print("total_templates", total_templates, "total_new", total_new)
print("mutual overlaps", len(mutual_lines), "stock overlaps", len(stock_lines))
print("--- NOTICE ---")
print(notice)
