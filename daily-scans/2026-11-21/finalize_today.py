#!/usr/bin/env python3
"""Finalize 2026-11-21 FaceOnTrend competitor scan."""
from __future__ import annotations

import json, os, re, time, html
from collections import defaultdict
from urllib.parse import urlparse
import importlib.util

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-21"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-20T09:39:28+08:00"

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
    "carne-asada-singing-dog": "oh-my-carne-asada",
    "dip-on-em-dance": "dip-on-em",
    "gta-wasted-meme": "gta-wasted",
    "jatayu-indian-mythology": "jatayu",
    "wassup-in-a-minute-dance": "wassup-in-a-minute",
    "wassup-dance": "wassup-in-a-minute",
    "in-a-minute-wassup": "wassup-in-a-minute",
    "wassup-in-a-minute-wassup": "wassup-in-a-minute",
    "ai-fashion-video-edit": "fashion-video-edit",
    "boom-clap-confetti-cannon": "boom-clap-confetti",
    "hanuman-ji": "hanuman",
    "here-we-go-again-gta-meme": "here-we-go-again-gta",
    "im-a-celebrity-jungle-filter": "im-a-celebrity",
    "i-am-a-celebrity": "im-a-celebrity",
    "mr-tumble-filter": "mr-tumble",
    "the-box-podium-meme": "the-box-podium",
    "gta-6-girlfriend-lucia": "gta-6-lucia",
    "hotel-lobby-dance": "hotel-lobby",
    "i-just-wanted-to-take-another-look-at-you": "take-another-look-at-you",
    "london-mews-house": "mews-house-london",
    "water-flyboard": "flyboard",
})

fetch = json.load(open(os.path.join(OUTDIR, "fetch_results.json"), encoding="utf-8"))
diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json"), encoding="utf-8"))
checks = json.load(open(os.path.join(OUTDIR, "url_checks.json"), encoding="utf-8"))
check_map = {(c["file"], c["id_or_slug"].lower()): c for c in checks}

yest_filt = defaultdict(dict)
for x in json.load(open("/workspace/competitor-scan-2026-11-20/filtered_out.json", encoding="utf-8")):
    yest_filt[x["file"]][x["item"]["id_or_slug"].lower()] = x.get("reason") or "parser-drift-or-non-template"

DIGEST_DESCS = {
    ("trendtemplate.json", "boom-clap-confetti-ai"): ("Boom Clap Confetti AI", "对嘴唱 Charli XCX《Boom Clap》，身后爆出彩带，没有礼炮"),
    ("trendtemplate.json", "boom-clap-confetti-cannon-ai"): ("Boom Clap Confetti Cannon AI", "唱到 “boom” 时礼炮朝你喷彩带"),
    ("trendtemplate.json", "no-i-aint-crazy-yb-ai"): ("No I Ain't Crazy YB AI", "欢迎回家拥抱、现金扇脸、小孩入镜，配 YoungBoy《38 Baby》"),
    ("makeviral.json", "boom-clap-confetti-ai-trend"): ("Boom Clap Confetti", "对嘴唱《Boom Clap》，礼炮在 “boom” 时淋下来，宠物也行"),
    ("makeviral.json", "dropped-truck-gta-6-ai-trend"): ("Dropped Truck GTA 6", "一张车照做成 GTA 6 市中心烧胎甩尾"),
    ("makeviral.json", "frozen-viking-warrior-ai"): ("Frozen Viking Warrior", "照片旋转变成雪峰上披毛皮、拿斧头的维京人"),
    ("makeviral.json", "gta-6-car-wash-ai-trend"): ("GTA 6 Car Wash", "GTA 6 风洗车过关，最后弹出金色 Mission Passed"),
    ("makeviral.json", "gta-6-girlfriend-lucia-ai-trend"): ("GTA 6 Girlfriend Lucia", "把 Lucia 加进合照，做成 “11 月 19 日的我们”"),
    ("makeviral.json", "hanuman-ji-ai-video"): ("Hanuman Ji AI Video", "跪地祈福，哈努曼现身赐福，配 Hanuman Chalisa"),
    ("makeviral.json", "here-we-go-again-gta-meme-ai"): ("Here We Go Again GTA Meme", "你或宠物走在 CJ 的阳光巷子里，配原句"),
    ("makeviral.json", "huss-huss-huss-ai-trend"): ("Huss Huss Huss", "对嘴唱 “In this town everybody goes out partying except me”"),
    ("makeviral.json", "im-a-celebrity-jungle-filter-ai"): ("I'm a Celebrity Jungle Filter", "红马甲、丛林帽，走进 I'm a Celeb 雨林定妆照"),
    ("makeviral.json", "mr-tumble-filter-ai"): ("Mr Tumble Filter", "红鼻子主持人造型说唱 Man's Not Hot"),
    ("makeviral.json", "napoleon-dynamite-dance-ai"): ("Napoleon Dynamite Dance", "在学校舞台上跳那支著名独舞，配 Canned Heat"),
    ("makeviral.json", "november-rain-ai-trend"): ("November Rain", "沙漠白色小教堂弹《November Rain》吉他独奏"),
    ("makeviral.json", "the-box-podium-meme-ai"): ("The Box Podium Meme", "车在身后爆炸翻滚，你在记者台说唱 The Box"),
    ("makeviral.json", "water-flyboard-ai-trend"): ("Water Flyboard", "在海上骑水上飞板，可双人从游艇起飞"),
    ("makememe.json", "gta-6-jet-ski-dog-ai"): ("GTA 6 Jet Ski Dog", "宠物戴护目镜骑摩托艇去海里救人"),
    ("makememe.json", "pop-pop-animation-ai"): ("Pop Pop Animation", "两人画成动漫厨师叠煎饼，烤箱起火，配 ILLIT《Pop》"),
    ("makememe.json", "you-are-nice-you-are-pretty-ai"): ("You Are Nice You Are Pretty", "宠物说 “you are nice, you are pretty…”，然后突然走神"),
    ("clipremake.json", "goodbye-gta-5-ai"): ("Goodbye GTA 5 AI", "日落码头三名老友递游戏和车钥匙，你开粉色跑车离开"),
    ("memeclone.json", "gta-ai-filter"): ("GTA AI Filter", "一张照片做成 GTA 6 加载页海报风：描边、Vice City 晚霞"),
    ("zapvid.json", "hotline-bling-ai-video-generator"): ("Hotline Bling", "在粉、红、蓝、紫发光房间里跳 Hotline Bling，可双人"),
    ("summrs.json", "warfare-intro-ai-video-generator"): ("Warfare Intro", "最多 8 张脸贴进 A24《Warfare》开场 Call on Me 海豹突击队那幕"),
    ("aimakevideo.json", "dip-on-em-dance-ai"): ("Dip On Em Dance AI", "孟菲斯舞：轻跳、甩发、抖肩，再下腰"),
    ("tryatrend.json", "dame-hombro-dance-ai"): ("Dame Hombro Dance AI", "转身、手绕圈、抖肩和摆臂，跟跳 TikTok 原片段"),
    ("tryatrend.json", "la-mujer-del-pelotero-ai"): ("La Mujer del Pelotero AI", "双手靠头、小臂滚动、摆胯跟跳"),
    ("starrd.json", "hotel-lobby-dance-ai-video"): ("Hotel Lobby Dance", "红墙前面无表情跳 Hotel Lobby"),
    ("starrd.json", "i-just-wanted-to-take-another-look-at-you-ai-video"): ("I Just Wanted To Take Another Look At You", "《一个明星的诞生》车窗回望那一幕"),
    ("starrd.json", "kiss-cam"): ("Kiss Cam", "大屏幕吻镜头找到你们，观众起哄后接吻"),
    ("starrd.json", "mews-house-london-ai-video"): ("Mews House London", "伦敦贵妇真人秀重聚独白，在缪斯小屋前"),
    ("starrd.json", "thats-my-opinion-ai-video"): ("That's My Opinion", "贵妇重聚梗：“I said, that's my opinion”"),
    ("memelry.json", "dropped-truck-gta-6-ai"): ("Dropped Truck GTA 6 AI", "卡车从直升机下驶过，烧胎滑过镜头"),
    ("memelry.json", "end-of-beginning-ai"): ("End of Beginning AI", "火盆桌前翻唱 Djo《End of Beginning》，最多三人"),
}

DIGEST_SLUGS = {k: set() for k, _ in DIGEST_DESCS}
for (fn, slug) in DIGEST_DESCS:
    DIGEST_SLUGS[fn].add(slug)

# SameVid genuine inventory (URL 200, not 404 page)
SAMEVID_SKIP = set()  # 404s and categories already excluded if not 200
inv_samevid = []
for c in checks:
    if c["file"] != "samevid.json":
        continue
    if c.get("status") == 200 and not c.get("looks_404"):
        inv_samevid.append({
            "id_or_slug": c["id_or_slug"],
            "title": (c.get("h1") or c.get("og") or c.get("title") or c["id_or_slug"]).split("|")[0].strip(),
            "url": c["url"],
        })

DIGEST_FILES_ORDER = [
    "trendtemplate.json", "clipremake.json", "makeviral.json", "makememe.json",
    "memeclone.json", "zapvid.json", "summrs.json", "starrd.json",
    "aimakevideo.json", "tryatrend.json", "memelry.json",
]

# Build digest_new / inv_new / filtered from raw diff
digest_new = defaultdict(list)
inv_new = defaultdict(list)
filtered = []
digest_keys = set()
inv_keys = set()

PHOTO_ONLY = {("starrd.json", "ai-christmas-photo")}

for fn, d in diff.items():
    for t in d.get("new") or []:
        slug = t["id_or_slug"].lower()
        rec = {"id_or_slug": t["id_or_slug"], "title": t.get("title") or t["id_or_slug"], "url": t["url"]}
        if (fn, slug) in DIGEST_DESCS:
            name, _ = DIGEST_DESCS[(fn, slug)]
            rec["title"] = name
            digest_new[fn].append(rec)
            digest_keys.add((fn, slug))
        elif fn == "samevid.json" and any(x["id_or_slug"].lower() == slug for x in inv_samevid):
            # use cleaner title from inv list
            rec["title"] = next(x["title"] for x in inv_samevid if x["id_or_slug"].lower() == slug)
            inv_new[fn].append(rec)
            inv_keys.add((fn, slug))
        else:
            reason = yest_filt.get(fn, {}).get(slug)
            if (fn, slug) in PHOTO_ONLY:
                reason = "photo-template-not-video"
            elif fn == "ricebowl.json":
                reason = "ricebowl-catalog-unchanged-sitemap-junk"
            elif not reason:
                if slug.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".json", ".txt", ".webmanifest", ".xml")):
                    reason = "asset"
                else:
                    reason = "non-template-or-parser-junk"
            filtered.append({
                "site": d.get("site") or (fin.HOMES.get(fn) or ("",))[0],
                "file": fn,
                "item": rec,
                "reason": reason,
            })

# keep-missing
KEEP_MISSING = {
    "summrs.json": {"bigfoot-vlog": "Kept bigfoot-vlog despite missing from today's sitemap (page still 200)."},
    "tryatrend.json": {"ai-halloween-costume": "Kept ai-halloween-costume despite missing from today's sitemap (page still 200)."},
}

n_sv = len(inv_new.get("samevid.json") or [])
NOTES = {
    "remakeyourmeme.json": "Sitemap via WebFetch; box IP still 403; inventory unchanged (44).",
    "ricebowl.json": "Meme catalog (/trends/meme ItemList) unchanged vs yesterday (0 genuine new). Generic /app tool pages and parse junk not added.",
    "samevid.json": f"{n_sv} genuine templates added to inventory as a catalog backfill; not itemized in the digest.",
    "summrs.json": "Kept bigfoot-vlog despite missing from today's sitemap (page still 200).",
    "tryatrend.json": "Kept ai-halloween-costume despite missing from today's sitemap (page still 200).",
}

# Write snapshots
site_reports = []
total_templates = 0
total_new = 0
total_digest_new = 0
sites_updated = 0

for fn, (site, home) in fin.HOMES.items():
    prev = json.load(open(os.path.join(STORE, fn), encoding="utf-8"))
    fr = fetch.get(fn, {})
    prev_tmpls = list(prev.get("templates") or [])
    prev_slugs = {t["id_or_slug"].lower(): t for t in prev_tmpls}

    added = list(digest_new.get(fn, [])) + list(inv_new.get(fn, []))
    new_tmpls = list(prev_tmpls)
    have = set(prev_slugs)
    for t in added:
        if t["id_or_slug"].lower() not in have:
            new_tmpls.append({"id_or_slug": t["id_or_slug"], "title": t["title"], "url": t["url"]})
            have.add(t["id_or_slug"].lower())

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
    "samevid_inventory_new": n_sv,
    "total_removed": 0,
    "sites_count": len(site_reports),
    "sites_updated": sites_updated,
    "sites_left_unchanged": 0,
    "sites": site_reports,
}
json.dump(ledger, open(os.path.join(STORE, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(ledger, open(os.path.join(OUTDIR, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

curated_source = {fn: list(items) for fn, items in digest_new.items()}
json.dump(curated_source, open(os.path.join(OUTDIR, "curated_source.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump({fn: items for fn, items in digest_new.items()}, open(os.path.join(OUTDIR, "curated_new.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump({fn: items for fn, items in inv_new.items()}, open(os.path.join(OUTDIR, "inventory_only.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(filtered, open(os.path.join(OUTDIR, "filtered_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump([], open(os.path.join(OUTDIR, "putmein_bulk.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def core_of(item):
    slug = (item.get("id_or_slug") or "").lower()
    if slug in {"gta-ai-filter", "gta-filter"}:
        return "gta-6-loading-screen"
    return fin.core_key(slug, item.get("title") or "")

clusters = defaultdict(list)
for fn, (site, home) in fin.HOMES.items():
    snap = json.load(open(os.path.join(STORE, fn), encoding="utf-8"))
    for t in snap.get("templates") or []:
        slug = t["id_or_slug"].lower()
        k = core_of(t)
        clusters[k].append({
            "core": k, "site": site, "file": fn, "item": t,
            "digest_new": (fn, slug) in digest_keys,
            "inv_new": (fn, slug) in inv_keys,
        })

PRETTY = {
    "oh-my-carne-asada": "Oh My Carne Asada",
    "dip-on-em": "Dip On Em Dance",
    "gta-farewell": "GTA 5 Goodbye / Farewell",
    "boom-clap-confetti": "Boom Clap Confetti",
    "dropped-truck-gta-6": "Dropped Truck GTA 6",
    "hanuman": "Hanuman Ji",
    "here-we-go-again-gta": "Here We Go Again GTA",
    "im-a-celebrity": "I'm a Celebrity Jungle Filter",
    "mr-tumble": "Mr Tumble",
    "november-rain": "November Rain",
    "the-box-podium": "The Box Podium Meme",
    "gta-6-lucia": "GTA 6 Lucia",
    "gta-6-jet-ski-dog": "GTA 6 Jet Ski Dog",
    "pop-pop-animation": "Pop Pop Animation",
    "hotel-lobby": "Hotel Lobby",
    "take-another-look-at-you": "Take Another Look At You",
    "mews-house-london": "Mews House London",
    "thats-my-opinion": "That's My Opinion",
    "hotline-bling": "Hotline Bling",
    "gta-6-loading-screen": "GTA 6 Loading Screen",
    "kiss-cam": "Kiss Cam",
    "flyboard": "Water Flyboard",
    "end-of-beginning": "End of Beginning",
}

def one_per_site(rows):
    by_site = defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r)
    out = []
    for site, rs in by_site.items():
        rs_sorted = sorted(rs, key=lambda r: (0 if (r["digest_new"] or r["inv_new"]) else 1, len(r["item"]["id_or_slug"])))
        out.append(rs_sorted[0])
    order = {site: i for i, (site, _) in enumerate(fin.HOMES.values())}
    out.sort(key=lambda r: order.get(r["site"], 999))
    return out

overlap_hits = []
for k, rows in clusters.items():
    picked = one_per_site(rows)
    smew = [r for r in picked if r["site"] == "Smew AI"]
    main = [r for r in picked if r["site"] != "Smew AI"]
    sites_main = {r["site"] for r in main}
    if len(sites_main) < 2:
        continue
    # Only show clusters that involve at least one digest-new template
    # (SameVid backfills vs stock only stay out of the report)
    n_digest = sum(1 for r in main if r["digest_new"])
    if n_digest == 0:
        continue
    n_today = sum(1 for r in main if r["digest_new"] or r["inv_new"])
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
    return f"[{r['site']}]({r['item']['url']})（{tag}）"

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

n_sites_digest = sum(1 for fn in DIGEST_FILES_ORDER if digest_new.get(fn))
n_digest = sum(len(digest_new[fn]) for fn in DIGEST_FILES_ORDER)

lines = []
lines.append("竞品模板日报（2026-11-21，上海时间）")
lines.append("")
lines.append(f"今日共 {n_digest} 个新模板，分布在 {n_sites_digest} 家。已核实页面可打开；解析误伤（分类页/聚合页/FAQ/SEO 变体/通用工具页）未计入。")
if n_sv:
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
elif not mutual_lines:
    lines.append("今日无多家共有")

notice = "\n".join(lines).rstrip() + "\n"
open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8").write(notice)
open(os.path.join(OUTDIR, "竞品模板日报-2026-11-21.md"), "w", encoding="utf-8").write(notice)
ov = ["# 多家共有（2026-11-21）", "", "今日新增互相撞车：", *mutual_lines, "", "今日新增与他站存量撞车：", *stock_lines, ""]
open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-21.md"), "w", encoding="utf-8").write("\n".join(ov))

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
print("per digest:")
for fn in DIGEST_FILES_ORDER:
    print(" ", fn, len(digest_new.get(fn) or []))
print("--- NOTICE ---")
print(notice)
