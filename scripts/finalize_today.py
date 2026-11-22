#!/usr/bin/env python3
"""Finalize 2026-11-22 FaceOnTrend competitor scan and write store snapshots."""
from __future__ import annotations

import json, os, re, time, html, shutil
from collections import defaultdict
from copy import deepcopy
from urllib.parse import urlparse
import importlib.util

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-22"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-21T09:40:54+08:00"

spec = importlib.util.spec_from_file_location("fin", "/workspace/competitor-scan-2026-11-21/finalize.py")
fin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fin)

fin.ALIASES.update({
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "mean-girls-jingle-bell-rock": "jingle-bell-rock",
    "give-it-all-to-me": "give-it-all",
    "boom-clap": "boom-clap-confetti",
    "boom-clap-confetti": "boom-clap-confetti",
    "vlogmas-intro-ai-cartoon": "vlogmas-intro",
    "vlogmas-intro": "vlogmas-intro",
    "huss-huss-huss": "huss-huss-huss",
    "gta-6-jet-ski-dog": "gta-6-jet-ski-dog",
    "thanksgiving-dance": "thanksgiving-dance",
    "frozen-viking-warrior": "frozen-viking-warrior",
    "gta-6-loading-screen": "gta-6-loading-screen",
    "gta-ai-filter": "gta-6-loading-screen",
    "window-peeper-filter": "window-peeper",
    "window-peeper": "window-peeper",
    "58th-floor": "58th-floor",
    "bandit-juice-wrld": "bandit",
    "bandit": "bandit",
    "eight-legends": "eight-legends",
    "homesick-for-a-person": "homesick-for-a-person",
    "homesick-for-a-person-ill-never-see-again": "homesick-for-a-person",
    "keep-going-run": "keep-going-run",
    "love-handstand": "love-handstand",
    "low-budget-amanda": "low-budget-amanda",
    "mecha-ride": "mecha-ride",
    "motorcycle-mecha-transformation": "mecha-ride",
    "waiting-on-my-fries": "waiting-on-my-fries",
    "break-a-leg-crab": "break-a-leg-crab",
    "convertible-drift": "convertible-drift",
    "convertible-drift-spin": "convertible-drift",
    "how-long-you-been-faithful": "how-long-you-been-faithful",
    "how-long-you-been-faithful-meme": "how-long-you-been-faithful",
    "stop-humiliating-yourself-rush-hour": "stop-humiliating-yourself",
    "stop-humiliating-yourself": "stop-humiliating-yourself",
    "truck-jump": "desert-truck-jump",
    "desert-truck-jump": "desert-truck-jump",
    "what-makes-you-beautiful": "what-makes-you-beautiful",
    "who-said-something-about-oil": "who-said-something-about-oil",
    "wizard-cat-keyboard": "wizard-cat-keyboard",
    "the-last-dance": "the-last-dance",  # keep distinct from last-dance duet
})

fetch = json.load(open(os.path.join(OUTDIR, "fetch_results.json"), encoding="utf-8"))
checks = { (c["file"], c["id_or_slug"].lower()): c for c in json.load(open(os.path.join(OUTDIR, "url_checks.json"), encoding="utf-8")) }

def prev_snap(fn):
    return json.load(open(os.path.join(STORE, fn), encoding="utf-8"))

def url_key(u):
    p = urlparse(u)
    path = p.path.rstrip("/") or "/"
    return (p.netloc.lower().removeprefix("www.") + path).lower()

def item(slug, title, url):
    return {"id_or_slug": slug, "title": title, "url": url}

def title_from_check(fn, slug, fallback):
    c = checks.get((fn, slug.lower()))
    if not c:
        return fallback
    for k in ("h1", "og", "title"):
        v = (c.get(k) or "").split("|")[0].strip()
        v = re.sub(r"\s+", " ", v)
        if v and v.lower() not in {"summrs", "starrd", "memelry"}:
            # shorten after colon if very long? keep first clause reasonably
            return v
    return fallback

# Digest descriptions (Chinese one-liners) and titles for the report
DIGEST = {
    ("makeviral.json", "bandit-juice-wrld-ai-trend"): ("Bandit Juice WRLD", "和朋友一起进入 YoungBoy / Juice WRLD《Bandit》MV"),
    ("makeviral.json", "eight-legends-ai-trend"): ("Eight Legends", "你和朋友做成颗粒感黑白「传奇」肖像，配原声"),
    ("makeviral.json", "homesick-for-a-person-ai-trend"): ("Homesick for a Person", "一张想念的人的照片，做成柔和黑白回忆短片"),
    ("makeviral.json", "keep-going-run-ai-trend"): ("Keep Going Run", "你在路上冲刺，一车蒙面粉丝举着 KEEP GOING 牌子跟着加油"),
    ("makeviral.json", "love-handstand-ai-trend"): ("Love Handstand", "倒立用腿拼出 LOVE 里的 V，配原声"),
    ("makeviral.json", "low-budget-amanda-ai-trend"): ("Low Budget Amanda", "对嘴跟跳缪斯小屋 / Low Budget Amanda 那支舞，可双人"),
    ("makeviral.json", "mecha-ride-ai-trend"): ("Mecha Ride", "骑上摩托，车身展开机甲盔甲再开走"),
    ("makeviral.json", "vlogmas-intro-ai-cartoon"): ("Vlogmas Intro", "手绘卡通版的你走进来，镜子写 Welcome to Vlogmas"),
    ("makeviral.json", "waiting-on-my-fries-ai-trend"): ("Waiting On My Fries", "taco 店里慢动作严肃跳舞，朋友把薯条忘了，人宠都行"),
    ("makememe.json", "boom-clap-confetti-ai"): ("Boom Clap Confetti", "对嘴唱《Boom Clap》，每到 boom 礼炮喷银彩带再喷金彩带"),
    ("makememe.json", "huss-huss-huss-ai"): ("Huss Huss Huss", "对嘴唱 “in this town everybody goes out partying except me”"),
    ("trendtemplate.json", "frozen-viking-warrior-ai"): ("Frozen Viking Warrior", "皮草和雪花旋转，你变成雪峰上的维京人"),
    ("trendtemplate.json", "vlogmas-intro-ai"): ("Vlogmas Intro", "手绘卡通走进来挥手，镜子写 Welcome to Vlogmas"),
    ("tryatrend.json", "gta-6-jet-ski-dog-ai"): ("GTA 6 Jet Ski Dog", "宠物戴护目镜骑摩托艇去海里救人"),
    ("tryatrend.json", "gta-6-loading-screen-ai"): ("GTA 6 Loading Screen", "一张照片做成 GTA 6 加载页海报，再转成海报风视频"),
    ("tryatrend.json", "huss-huss-huss-ai"): ("Huss Huss Huss", "对嘴唱 In This Town，再卷哑铃、做 huss，按原片镜头"),
    ("clipremake.json", "gta-6-jet-ski-dog-ai"): ("GTA 6 Jet Ski Dog", "宠物穿救生衣、戴绿护目镜，骑摩托艇去救人"),
    ("clipremake.json", "thanksgiving-dance-ai"): ("Thanksgiving Dance", "客厅里做 “beans, greens, potatoes, tomatoes” 下腰舞"),
    ("danceremake.json", "give-it-all-ai"): ("Give It All", "在大厅吊麦前说唱 “give it all to me”，人宠都行"),
    ("danceremake.json", "thanksgiving-dance-ai"): ("Thanksgiving Dance", "暖光客厅里跳感恩节 “you name it” 下腰舞，人宠都行"),
    ("putmein.json", "58th-floor-ai-trend"): ("58th Floor", "把你和朋友放进 58 层楼那支趋势短片，按原片镜头"),
    ("putmein.json", "window-peeper-ai-trend"): ("Window Peeper", "把你放进窗户偷窥那支趋势短片，按原片镜头"),
    ("aimakevideo.json", "boom-clap-ai"): ("Boom Clap", "对嘴唱《Boom Clap》，礼炮在头上爆两次彩带，三个房间"),
    ("starrd.json", "break-a-leg-crab-ai-video"): ("Break A Leg, Crab", "你变成那支病毒视频里的螃蟹教练"),
    ("starrd.json", "convertible-drift-ai-video"): ("Convertible Drift", "开红色敞篷车原地甩尾画圈"),
    ("starrd.json", "how-long-you-been-faithful-meme-ai-video"): ("How Long You Been Faithful", "播客采访里吹嘘自己有多专一，接那句病毒提问"),
    ("starrd.json", "stop-humiliating-yourself-rush-hour-ai-video"): ("Stop Humiliating Yourself", "Rush Hour 审讯场面翻车，把你放进去"),
    ("starrd.json", "truck-jump-ai-video"): ("Desert Truck Jump", "六轮越野车从你身边腾空飞过，你完全不在意"),
    ("starrd.json", "what-makes-you-beautiful-ai-video"): ("What Makes You Beautiful", "五个朋友坐一辆车，对口型唱完这首歌"),
    ("starrd.json", "who-said-something-about-oil-ai-video"): ("Who Said Something About Oil", "站上新闻发布会讲台，接那句病毒记者会"),
    ("samevid.json", "the-last-dance-ai"): ("The Last Dance", "单人 Invisible-partner 旋转，配 Maretu 原声（和已有双人 Last Dance 不是同一个）"),
    ("memelry.json", "wizard-cat-keyboard-ai"): ("Wizard Cat Keyboard", "把宠物放进电脑桌前的魔法猫咪打字场景"),
}

# Inventory-only (real pages, not itemized as 视频模板 in the digest)
INV_ONLY = {
    ("makeviral.json", "black-and-white-wet-look-ai-photo"): item(
        "black-and-white-wet-look-ai-photo",
        "Black and White Wet Face Portrait",
        "https://www.makeviral.ai/templates/black-and-white-wet-look-ai-photo",
    ),
    ("starrd.json", "ai-christmas-photo"): item(
        "ai-christmas-photo",
        "AI Christmas Photo",
        "https://www.getstarrd.app/template/ai-christmas-photo",
    ),
}

DIGEST_FILES_ORDER = [
    "makeviral.json", "makememe.json", "trendtemplate.json", "tryatrend.json",
    "clipremake.json", "danceremake.json", "putmein.json", "aimakevideo.json",
    "starrd.json", "samevid.json", "memelry.json",
]

# Build new-item objects for digest
digest_new = defaultdict(list)
for (fn, slug), (title, desc) in DIGEST.items():
    url = None
    # find url from fetch or checks
    c = checks.get((fn, slug))
    if c:
        url = c["url"]
    else:
        for t in fetch[fn]["templates"]:
            if t["id_or_slug"].lower() == slug:
                url = t["url"]
                break
    digest_new[fn].append({"id_or_slug": slug, "title": title, "url": url, "desc": desc})

# ---- rebuild inventories ----
# Sites whose fetch templates can be used as-is (no junk slipped in, or only digest/inv-only adds)
CLEAN_USE_FETCH = {
    "dothetrend.json", "smew.json", "viralremake.json", "zapvid.json",
    "memeclone.json", "trendify.json", "kubflow.json",
    "clipremake.json", "danceremake.json", "putmein.json", "aimakevideo.json",
}

# Sites where fetch added junk or dropped keep-alive pages: start from previous + curated adds
CURATED_ADDS = defaultdict(list)
for fn, items in digest_new.items():
    for t in items:
        CURATED_ADDS[fn].append(item(t["id_or_slug"], t["title"], t["url"]))
for (fn, slug), t in INV_ONLY.items():
    CURATED_ADDS[fn].append(t)

# MakeViral includes the photo inv-only plus 9 digest — fetch already has all 10 and no junk
CLEAN_USE_FETCH.add("makeviral.json")

KEEP_MISSING = {
    "tryatrend.json": ["ai-halloween-costume"],
    "summrs.json": ["bigfoot-vlog"],
}

# Filter fetch templates for a few mostly-clean sites that only had asset junk
ASSET_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".css", ".js",
             ".xml", ".txt", ".json", ".webmanifest", ".map")
ASSET_SLUGS = {"favicon", "favicon.ico", "apple-icon.png", "apple-touch-icon.png",
               "manifest.webmanifest", "manifest.json", "logo.png", "logo-dark.png",
               "logo-mark.svg", "site.webmanifest", "llms.txt"}

def is_asset(t):
    s = t["id_or_slug"].lower()
    u = (t.get("url") or "").lower()
    return s in ASSET_SLUGS or any(s.endswith(ext) or u.endswith(ext) for ext in ASSET_EXT)

# Sites: use prev + curated, never import sitemap junk
PREV_PLUS_CURATED = {
    "makememe.json", "trendtemplate.json", "tryatrend.json", "starrd.json",
    "samevid.json", "memelry.json", "summrs.json", "memefxai.json",
    "ricebowl.json", "picturetovideo.json", "rapvideo.json", "trendswap.json",
    "genjutsu.json", "bolly.json", "aitrendvideo.json", "remakeyourmeme.json",
}

snapshots = {}
ledger_sites = []
total_new = 0
total_digest = 0
total_inv_only = 0
total_removed = 0

SITE_META = [
    ("DoTheTrend", "dothetrend.json", "https://dothetrend.ai/"),
    ("TrendTemplate", "trendtemplate.json", "https://trendtemplate.com/"),
    ("MemeFX AI", "memefxai.json", "https://memefxai.com/"),
    ("ClipRemake", "clipremake.json", "https://clipremake.com/"),
    ("Remake Your Meme", "remakeyourmeme.json", "https://remakeyourmeme.com/"),
    ("MakeViral", "makeviral.json", "https://www.makeviral.ai/"),
    ("Smew AI", "smew.json", "https://smew.ai/"),
    ("MakeMeme.video", "makememe.json", "https://makememe.video/"),
    ("ViralRemake", "viralremake.json", "https://viralremake.com/"),
    ("MemeClone.ai", "memeclone.json", "https://memeclone.ai/"),
    ("TrendSwap", "trendswap.json", "https://trendswap.app/"),
    ("Put Me In", "putmein.json", "https://putmein.app/"),
    ("SameVid AI", "samevid.json", "https://samevid.com/"),
    ("ZapVid", "zapvid.json", "https://zapvid.ai/"),
    ("Summrs", "summrs.json", "https://www.summrs.com/"),
    ("Trendify Video", "trendify.json", "https://trendify.video/"),
    ("Genjutsu AI", "genjutsu.json", "https://genjutsuai.cc/"),
    ("DanceRemake", "danceremake.json", "https://danceremake.com/"),
    ("Starrd", "starrd.json", "https://www.getstarrd.app/"),
    ("AI Trend Video", "aitrendvideo.json", "https://aitrendvideo.net/"),
    ("Ricebowl AI", "ricebowl.json", "https://ricebowl.ai/"),
    ("Kubflow", "kubflow.json", "https://kubflow.ai/"),
    ("PictureToVideo", "picturetovideo.json", "https://picturetovideo.org/"),
    ("Bolly.AI", "bolly.json", "https://www.bolly.ai/"),
    ("RapVideo.ai", "rapvideo.json", "https://rapvideo.ai/"),
    ("aiMakeVideo", "aimakevideo.json", "https://aimakevideo.com/"),
    ("Try a Trend", "tryatrend.json", "https://tryatrend.com/"),
    ("Memelry", "memelry.json", "https://memelry.com/"),
]

notes_by_file = {}

for site, fn, home in SITE_META:
    prev = prev_snap(fn)
    fr = fetch.get(fn, {})
    prev_templates = list(prev.get("templates", []))
    prev_keys = {url_key(t["url"]) for t in prev_templates}
    prev_slugs = {t["id_or_slug"].lower() for t in prev_templates}

    if fn == "remakeyourmeme.json":
        templates = prev_templates
        new_ts, removed_ts = [], []
        sitemap_urls = ["https://remakeyourmeme.com/sitemap.xml"]
        sitemap_existed = True
        notes_by_file[fn] = "Sitemap via WebFetch; box IP still 403; inventory unchanged (44)."
    elif fn in CLEAN_USE_FETCH and fr.get("fetch_ok"):
        templates = [t for t in fr["templates"] if not is_asset(t)]
        sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        sitemap_existed = bool(fr.get("sitemap_existed") or sitemap_urls)
        cur_keys = {url_key(t["url"]) for t in templates}
        cur_slugs = {t["id_or_slug"].lower() for t in templates}
        new_ts = [t for t in templates if url_key(t["url"]) not in prev_keys and t["id_or_slug"].lower() not in prev_slugs]
        removed_ts = [t for t in prev_templates if url_key(t["url"]) not in cur_keys and t["id_or_slug"].lower() not in cur_slugs]
    else:
        # prev + curated adds
        templates = list(prev_templates)
        have = set(prev_keys)
        have_slugs = set(prev_slugs)
        new_ts = []
        for t in CURATED_ADDS.get(fn, []):
            if url_key(t["url"]) in have or t["id_or_slug"].lower() in have_slugs:
                continue
            templates.append(t)
            have.add(url_key(t["url"]))
            have_slugs.add(t["id_or_slug"].lower())
            new_ts.append(t)
        # keep-alive already in prev; nothing to add
        removed_ts = []
        sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        sitemap_existed = bool(fr.get("sitemap_existed") or sitemap_urls)

    # sort
    templates = sorted(templates, key=lambda t: t["id_or_slug"].lower())
    # classify new as digest vs inv-only vs other
    digest_slugs = {s for (f, s) in DIGEST if f == fn}
    inv_slugs = {s for (f, s) in INV_ONLY if f == fn}
    digest_items = [t for t in new_ts if t["id_or_slug"].lower() in digest_slugs]
    inv_items = [t for t in new_ts if t["id_or_slug"].lower() in inv_slugs]
    # MakeViral photo is in new_ts from fetch
    other_new = [t for t in new_ts if t["id_or_slug"].lower() not in digest_slugs and t["id_or_slug"].lower() not in inv_slugs]

    # For clean fetch sites, other_new should be empty except we want only digest+inv in new_templates field
    recorded_new = digest_items + inv_items + [t for t in other_new if fn in CLEAN_USE_FETCH]
    # if somehow clean fetch has unexpected extras, still record them in inventory (already in templates)
    # but only list digest+inv in new_templates for the daily file? Keep all genuine recorded_new.

    note = notes_by_file.get(fn)
    if fn == "tryatrend.json":
        note = "Kept ai-halloween-costume despite missing from today's sitemap (page still 200)."
    elif fn == "summrs.json":
        note = "Kept bigfoot-vlog despite missing from today's sitemap (page still 200). Generic tool/SEO landing pages not added."
    elif fn == "ricebowl.json":
        note = "Meme catalog (/trends/meme ItemList) unchanged vs yesterday (0 genuine new). Generic /app tool pages not added."
    elif fn == "samevid.json":
        note = "Added 1 genuine template (The Last Dance solo). Category listing paths from sitemap not added."
    elif fn == "memelry.json":
        note = "Added 1 genuine template (Wizard Cat Keyboard). SEO satellite / photo-only / helper pages not added."
    elif fn == "starrd.json":
        note = "Added 7 video templates plus 1 photo template (inventory only). Category paths that 404 were not added."
    elif fn == "makememe.json":
        note = "Asset URLs in sitemap ignored."
    elif fn == "trendtemplate.json":
        note = "Asset URLs in sitemap ignored."

    snap = {
        "site": site,
        "home": home,
        "checked_at": CHECKED_AT,
        "sitemap_urls_found": sitemap_urls,
        "sitemap_existed": sitemap_existed,
        "template_count": len(templates),
        "new_count": len(recorded_new),
        "removed_count": len(removed_ts),
        "new_templates": recorded_new,
        "removed_templates": removed_ts,
        "templates": templates,
    }
    if note:
        snap["note"] = note
    snapshots[fn] = snap

    total_new += len(recorded_new)
    total_digest += len(digest_items)
    total_inv_only += len(inv_items)
    total_removed += len(removed_ts)

    ls = {
        "site": site,
        "file": fn,
        "home": home,
        "sitemap_existed": sitemap_existed,
        "sitemap_urls_found": sitemap_urls,
        "template_count": len(templates),
        "new_count": len(recorded_new),
        "removed_count": len(removed_ts),
        "dropped_dead_count": 0,
    }
    if note:
        ls["note"] = note
    ledger_sites.append(ls)

# ---- overlaps ----
# Build current full inventory (all snapshots)
by_key = defaultdict(list)  # core -> list of {site, file, title, url, slug, is_today_new}
today_keys = set()
today_new_index = {}  # (file, slug) 

for fn, items in digest_new.items():
    for t in items:
        today_new_index[(fn, t["id_or_slug"].lower())] = t

for fn, snap in snapshots.items():
    for t in snap["templates"]:
        key = fin.core_key(t["id_or_slug"], t.get("title") or "")
        rec = {
            "site": snap["site"],
            "file": fn,
            "title": t.get("title") or t["id_or_slug"],
            "url": t["url"],
            "slug": t["id_or_slug"],
            "is_today_new": (fn, t["id_or_slug"].lower()) in today_new_index,
        }
        by_key[key].append(rec)
        if rec["is_today_new"]:
            today_keys.add(key)

# collisions involving today's new (across >=2 sites)
collisions = []
for key in sorted(today_keys):
    recs = by_key[key]
    # unique sites
    sites = {}
    for r in recs:
        sites.setdefault(r["site"], r)
    if len(sites) >= 2:
        collisions.append((key, list(sites.values())))

# Also "今日新增之间撞车" vs "今日新增与他站存量撞车"
def collision_kind(recs):
    new_sites = [r for r in recs if r["is_today_new"]]
    if len({r["site"] for r in new_sites}) >= 2:
        return "今日新增互撞"
    return "与他站存量撞车"

# pretty names
PRETTY = {
    "boom-clap-confetti": "Boom Clap Confetti",
    "vlogmas-intro": "Vlogmas Intro",
    "huss-huss-huss": "Huss Huss Huss",
    "gta-6-jet-ski-dog": "GTA 6 Jet Ski Dog",
    "thanksgiving-dance": "Thanksgiving Dance",
    "frozen-viking-warrior": "Frozen Viking Warrior",
    "gta-6-loading-screen": "GTA 6 Loading Screen",
    "give-it-all": "Give It All",
    "58th-floor": "58th Floor",
    "window-peeper": "Window Peeper",
    "bandit": "Bandit (Juice WRLD)",
    "eight-legends": "Eight Legends",
    "homesick-for-a-person": "Homesick for a Person",
    "keep-going-run": "Keep Going Run",
    "love-handstand": "Love Handstand",
    "low-budget-amanda": "Low Budget Amanda",
    "mecha-ride": "Mecha Ride",
    "waiting-on-my-fries": "Waiting On My Fries",
    "break-a-leg-crab": "Break A Leg, Crab",
    "convertible-drift": "Convertible Drift",
    "how-long-you-been-faithful": "How Long You Been Faithful",
    "stop-humiliating-yourself": "Stop Humiliating Yourself",
    "desert-truck-jump": "Desert Truck Jump",
    "what-makes-you-beautiful": "What Makes You Beautiful",
    "who-said-something-about-oil": "Who Said Something About Oil",
    "wizard-cat-keyboard": "Wizard Cat Keyboard",
    "the-last-dance": "The Last Dance",
}

overlap_out = []
for key, recs in collisions:
    # unique by site, prefer today-new url if both
    by_site = {}
    for r in recs:
        if r["site"] not in by_site or (r["is_today_new"] and not by_site[r["site"]]["is_today_new"]):
            by_site[r["site"]] = r
    uniq = list(by_site.values())
    overlap_out.append({
        "key": key,
        "name": PRETTY.get(key) or fin.pretty_name(key, [r["title"] for r in uniq]),
        "kind": collision_kind(uniq),
        "n_sites": len(uniq),
        "sites": uniq,
    })

# sort: mutual new first, then by n_sites desc, then name
overlap_out.sort(key=lambda x: (0 if x["kind"] == "今日新增互撞" else 1, -x["n_sites"], x["name"].lower()))

json.dump(overlap_out, open(os.path.join(OUTDIR, "overlaps-today.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- notice ----
site_names = {fn: site for site, fn, _ in SITE_META}
n_digest = sum(len(v) for v in digest_new.values())
n_sites = len([fn for fn in DIGEST_FILES_ORDER if digest_new[fn]])
lines = []
lines.append(f"竞品模板日报（2026-11-22，上海时间）")
lines.append("")
lines.append(f"今日共 {n_digest} 个新模板，分布在 {n_sites} 家。已核实页面可打开；解析误伤（分类页/聚合页/FAQ/SEO 变体/通用工具页/静态资源）未计入。")
lines.append("另：MakeViral 的 Black and White Wet Look、Starrd 的 AI Christmas Photo 为照片模板，已记入库存，不在正文列出。")
lines.append("")

for fn in DIGEST_FILES_ORDER:
    items = digest_new[fn]
    if not items:
        continue
    lines.append(f"【{site_names[fn]}】{len(items)} 个")
    for t in items:
        lines.append(f"- {t['title']}：{t['desc']}")
        lines.append(f"  {t['url']}")
    lines.append("")

lines.append("【多家共有】")
if not overlap_out:
    lines.append("今日无多家共有")
else:
    mutual = [x for x in overlap_out if x["kind"] == "今日新增互撞"]
    stock = [x for x in overlap_out if x["kind"] != "今日新增互撞"]
    if mutual:
        lines.append("今日新增里已经撞车：")
        for x in mutual:
            bits = []
            for r in x["sites"]:
                mark = "（今日新增）" if r["is_today_new"] else ""
                bits.append(f"{r['site']}{mark} {r['url']}")
            lines.append(f"- {x['name']}（{x['n_sites']} 家）：")
            for b in bits:
                lines.append(f"  · {b}")
        lines.append("")
    if stock:
        lines.append("今日新增与他站存量撞车：")
        for x in stock:
            bits = []
            for r in x["sites"]:
                mark = "（今日新增）" if r["is_today_new"] else ""
                bits.append(f"{r['site']}{mark} {r['url']}")
            lines.append(f"- {x['name']}（{x['n_sites']} 家）：")
            for b in bits:
                lines.append(f"  · {b}")

notice = "\n".join(lines).rstrip() + "\n"
open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8").write(notice)
open(os.path.join(OUTDIR, "竞品模板日报-2026-11-22.md"), "w", encoding="utf-8").write(notice)

# ---- write store (after backup) ----
backup = os.path.join(OUTDIR, "store-backup-pre")
if not os.path.exists(backup):
    shutil.copytree(STORE, backup)

for fn, snap in snapshots.items():
    path = os.path.join(STORE, fn)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
        f.write("\n")

# update excluded list with newly confirmed junk stems
exc_path = os.path.join(STORE, "excluded-non-templates.json")
exc = json.load(open(exc_path, encoding="utf-8"))
extra = {
    "starrd.json": ["birthday", "effects", "famous", "cars", "drama", "gaming", "holidays", "music", "pets", "song", "sports"],
    "samevid.json": ["anime", "baby-kids", "christmas", "couple", "dance", "effects", "family", "festival", "friends", "funny", "halloween", "movie-tv", "music", "new", "pets", "sports", "templates", "transformation"],
    "trendswap.json": ["help-center", "content-policy", "refund-policy", "dance", "duo", "meme", "new", "pet", "prompts", "videos"],
    "bolly.json": ["anime", "brainrot", "edits", "football", "kpop", "meme", "multi-person"],
    "aitrendvideo.json": ["create", "history", "refund-policy", "custom-video-template"],
    "memefxai.json": ["studio", "whats-new", "alternatives", "refund-policy", "report", "templates", "videos"],
    "genjutsu.json": ["history"],
}
for fn, slugs in extra.items():
    cur = list(exc.get("by_file", {}).get(fn, []))
    for s in slugs:
        if s not in cur:
            cur.append(s)
    exc.setdefault("by_file", {})[fn] = cur
json.dump(exc, open(exc_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(exc_path, "a").write("\n")

ledger = {
    "checked_at": CHECKED_AT,
    "timezone": "Asia/Shanghai",
    "baseline": False,
    "previous_checked_at": PREV_CHECKED_AT,
    "total_templates": sum(s["template_count"] for s in ledger_sites),
    "total_new": total_new,
    "total_digest_new": n_digest,
    "total_inventory_only_new": total_inv_only,
    "total_removed": total_removed,
    "sites_count": 28,
    "sites_updated": 28,
    "sites_left_unchanged": 0,
    "sites": ledger_sites,
}
json.dump(ledger, open(os.path.join(STORE, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(os.path.join(STORE, "ledger.json"), "a").write("\n")
json.dump(ledger, open(os.path.join(OUTDIR, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

summary = {
    "checked_at": CHECKED_AT,
    "total_templates": ledger["total_templates"],
    "total_new": total_new,
    "total_digest_new": n_digest,
    "total_inventory_only_new": total_inv_only,
    "total_removed": total_removed,
    "overlap_count": len(overlap_out),
    "mutual": [x["name"] for x in overlap_out if x["kind"] == "今日新增互撞"],
    "stock": [x["name"] for x in overlap_out if x["kind"] != "今日新增互撞"],
    "per_site": {fn: [t["id_or_slug"] for t in digest_new[fn]] for fn in DIGEST_FILES_ORDER if digest_new[fn]},
}
json.dump(summary, open(os.path.join(OUTDIR, "run-summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("CHECKED_AT", CHECKED_AT)
print("templates", ledger["total_templates"], "recorded_new", total_new, "digest", n_digest, "inv_only", total_inv_only, "removed", total_removed)
print("overlaps", len(overlap_out), "mutual", summary["mutual"], "stock", summary["stock"])
print("---- notice ----")
print(notice)
for s in ledger_sites:
    if s["new_count"] or s["removed_count"] or s.get("note"):
        print(f"  {s['site']}: count={s['template_count']} new={s['new_count']} rm={s['removed_count']} {s.get('note','')}")
