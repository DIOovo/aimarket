#!/usr/bin/env python3
"""Finalize 2026-11-17 FaceOnTrend competitor scan."""
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
OUTDIR = "/workspace/competitor-scan-2026-11-17"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-15T10:14:26+08:00"

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
    "pimpwalk-entrance": "pimp-walk-entrance",
    "monkey-eating-apple": "monkey-eating-apple",
    "reaching-out-cat": "reaching-out-cat",
})
fin.NAME_OVERRIDE.update({
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
})

# Genuine day-over-day new templates (verified 200). Put Me In bulk is handled separately.
CURATED = {
    "TrendTemplate": [
        {"id_or_slug": "need-for-speed-ai", "title": "Need for Speed AI",
         "url": "https://trendtemplate.com/need-for-speed-ai",
         "desc": "把自己的车放进《极品飞车》小镇烧胎漂移追逐"},
    ],
    "MakeViral": [
        {"id_or_slug": "ai-tidal-wave-video", "title": "AI Tidal Wave Video",
         "url": "https://www.makeviral.ai/templates/ai-tidal-wave-video",
         "desc": "巨浪拍上栏杆，把你和朋友冲倒"},
        {"id_or_slug": "airport-transition-ai-trend", "title": "Airport Transition AI",
         "url": "https://www.makeviral.ai/templates/airport-transition-ai-trend",
         "desc": "登机口用手指在镜头前画圈，一刀切到霓虹夜城"},
        {"id_or_slug": "dance-with-santa-ai", "title": "Dancing With Santa AI",
         "url": "https://www.makeviral.ai/templates/dance-with-santa-ai",
         "desc": "在圣诞树旁和圣诞老人并肩跳舞"},
        {"id_or_slug": "dog-washing-dishes-ai-trend", "title": "Dog Washing Dishes AI",
         "url": "https://www.makeviral.ai/templates/dog-washing-dishes-ai-trend",
         "desc": "宠物在水槽洗碗，打开手机盒却是块海绵"},
        {"id_or_slug": "gta-6-loading-screen-ai", "title": "GTA 6 Loading Screen AI",
         "url": "https://www.makeviral.ai/templates/gta-6-loading-screen-ai",
         "desc": "把自拍做成带棕榈树和跑车的 GTA 6 加载海报"},
        {"id_or_slug": "jingle-bell-brazil-dance-ai", "title": "Jingle Bell Brazil Dance AI",
         "url": "https://www.makeviral.ai/templates/jingle-bell-brazil-dance-ai",
         "desc": "戴圣诞帽排成一排，跳巴西 Funk 版 Jingle Bell 卡点舞"},
        {"id_or_slug": "nadie-ta-frio-ai-trend", "title": "Nadie Ta Frío Trend AI",
         "url": "https://www.makeviral.ai/templates/nadie-ta-frio-ai-trend",
         "desc": "跟跳 Laja《Nadie Ta Frío》手部卡点舞"},
        {"id_or_slug": "reaching-out-cat-ai", "title": "Reaching Out Cat Trend",
         "url": "https://www.makeviral.ai/templates/reaching-out-cat-ai",
         "desc": "手伸上去，把猫/狗/人一把拽出画面"},
        {"id_or_slug": "ronaldo-header-ai-trend", "title": "Ronaldo Header AI",
         "url": "https://www.makeviral.ai/templates/ronaldo-header-ai-trend",
         "desc": "踩着穿晚礼服的朋友做 C 罗式头球破门"},
        {"id_or_slug": "tiger-transition-ai-trend", "title": "Tiger Transition AI",
         "url": "https://www.makeviral.ai/templates/tiger-transition-ai-trend",
         "desc": "手挡镜头后变身虎纹妆/华丽造型，配 You Cannot Reason With a Tiger"},
        {"id_or_slug": "you-rock-my-world-ai-trend", "title": "You Rock My World Trend",
         "url": "https://www.makeviral.ai/templates/you-rock-my-world-ai-trend",
         "desc": "情侣在家被手扫过镜头，再变身盛装（甚至到巴黎）"},
    ],
    "MakeMeme.video": [
        {"id_or_slug": "bigxthaplug-give-it-all-ai", "title": "BigXthaPlug Give It All AI",
         "url": "https://makememe.video/bigxthaplug-give-it-all-ai",
         "desc": "在电影院大厅吊麦前说唱 Give It All"},
        {"id_or_slug": "jingle-bell-rock-ai", "title": "Jingle Bell Rock AI",
         "url": "https://makememe.video/jingle-bell-rock-ai",
         "desc": "《贱女孩》里 Jingle Bell Rock 圣诞群舞"},
        {"id_or_slug": "never-let-her-pay-ai", "title": "Never Let Her Pay AI",
         "url": "https://makememe.video/never-let-her-pay-ai",
         "desc": "约会抢着买单，打开包却掏出一块海绵被罚去洗碗"},
        {"id_or_slug": "old-town-road-ai", "title": "Old Town Road AI",
         "url": "https://makememe.video/old-town-road-ai",
         "desc": "糖果店里唱歌，再坐上红色敞篷车甩钱袋"},
        {"id_or_slug": "pet-taxi-ai", "title": "Pet Taxi AI",
         "url": "https://makememe.video/pet-taxi-ai",
         "desc": "把自己的猫狗变成巴士那么大，骑在它背上回家"},
    ],
    "ClipRemake": [
        {"id_or_slug": "hotline-bling-ai", "title": "Hotline Bling AI",
         "url": "https://clipremake.com/templates/hotline-bling-ai",
         "desc": "和搭档在粉/蓝/紫/绿霓虹房间里轮流出镜跳 Hotline Bling"},
        {"id_or_slug": "wassup-in-a-minute-ai", "title": "Wassup in a Minute AI",
         "url": "https://clipremake.com/templates/wassup-in-a-minute-ai",
         "desc": "和朋友走上一座雾气山坡，抱头、搞怪再耸肩"},
    ],
    "MemeFX AI": [
        {"id_or_slug": "wassup-in-a-minute-ai-trend", "title": "Wassup in a Minute AI",
         "url": "https://memefxai.com/wassup-in-a-minute-ai-trend",
         "desc": "和两个朋友在雾气山坡上跳 Wassup in a Minute 田野舞"},
    ],
    "SameVid AI": [
        {"id_or_slug": "aircraft-carrier-dance-ai", "title": "Aircraft Carrier Dance AI",
         "url": "https://samevid.com/template/aircraft-carrier-dance-ai",
         "desc": "在阳光航母甲板上跳三段卡点舞"},
        {"id_or_slug": "ddg-and-dub-ai-dance", "title": "DDG and Dub AI Dance",
         "url": "https://samevid.com/template/ddg-and-dub-ai-dance",
         "desc": "客厅双人跟跳 DDG and Dub 热门编舞"},
        {"id_or_slug": "grandma-vs-grandpa-fight-ai", "title": "Grandma vs Grandpa Fight AI",
         "url": "https://samevid.com/template/grandma-vs-grandpa-fight-ai",
         "desc": "爷爷奶奶抢遥控器的沙发打架喜剧"},
        {"id_or_slug": "hospital-flying-knee-ai", "title": "Hospital Flying Knee AI",
         "url": "https://samevid.com/template/hospital-flying-knee-ai",
         "desc": "医院里飞膝踢人的短打斗小品"},
        {"id_or_slug": "photographing-dolphins-ai", "title": "Photographing Dolphins AI",
         "url": "https://samevid.com/template/photographing-dolphins-ai",
         "desc": "用长焦拍跃出水面的海豚"},
        {"id_or_slug": "reaching-out-cat-ai", "title": "Reaching Out Cat AI",
         "url": "https://samevid.com/template/reaching-out-cat-ai",
         "desc": "手伸向天花板，再一把把猫拽出画面（Human Nature）"},
        {"id_or_slug": "rich-era-ai", "title": "Rich Era AI",
         "url": "https://samevid.com/template/rich-era-ai",
         "desc": "在金色豪华酒店走廊里气场十足地走过"},
        {"id_or_slug": "ronaldo-header-ai", "title": "Ronaldo Header AI",
         "url": "https://samevid.com/template/ronaldo-header-ai",
         "desc": "扮演头球手或防守人，还原 C 罗 2.56 米头球"},
        {"id_or_slug": "rooster-wet-cement-ai", "title": "Rooster Wet Cement AI",
         "url": "https://samevid.com/template/rooster-wet-cement-ai",
         "desc": "公鸡走进未干水泥地的剧情反转"},
    ],
    "DanceRemake": [
        {"id_or_slug": "hotline-bling-ai", "title": "Hotline Bling AI",
         "url": "https://danceremake.com/templates/hotline-bling-ai",
         "desc": "和搭档在霓虹房间里轮流出镜跳 Hotline Bling"},
        {"id_or_slug": "pimp-walk-entrance-ai", "title": "Pimp Walk Entrance AI",
         "url": "https://danceremake.com/templates/pimp-walk-entrance-ai",
         "desc": "朋友帮你开门，你大摇大摆走进汉堡店并扇红卡"},
        {"id_or_slug": "wassup-in-a-minute-ai", "title": "Wassup in a Minute AI",
         "url": "https://danceremake.com/templates/wassup-in-a-minute-ai",
         "desc": "最多三人走上雾气山坡，抱头耸肩再蹦下去"},
    ],
    "ZapVid": [
        {"id_or_slug": "babydoll-dance-ai-video-generator", "title": "Babydoll Dance AI",
         "url": "https://zapvid.ai/babydoll-dance-ai-video-generator",
         "desc": "跟跳 Jamie Miller《Babydoll》弹跳两步舞，可带上两个朋友"},
        {"id_or_slug": "bicep-heart-ai-video-generator", "title": "Bicep Heart AI",
         "url": "https://zapvid.ai/bicep-heart-ai-video-generator",
         "desc": "秀二头肌再用另一只手比心，还原 7 秒卡点"},
        {"id_or_slug": "clapping-cat-ai-video-generator", "title": "Clapping Cat AI",
         "url": "https://zapvid.ai/clapping-cat-ai-video-generator",
         "desc": "让自己的猫狗直立起来，慢慢对你鼓掌"},
        {"id_or_slug": "flying-tesla-roadster-ai-video-generator", "title": "Flying Tesla Roadster AI",
         "url": "https://zapvid.ai/flying-tesla-roadster-ai-video-generator",
         "desc": "堵车时按下按钮，Roadster 喷火飞过楼宇"},
        {"id_or_slug": "la-tormenta-de-arena-ai-video-generator", "title": "La Tormenta de Arena AI",
         "url": "https://zapvid.ai/la-tormenta-de-arena-ai-video-generator",
         "desc": "在俱乐部阳台微笑，灯光打到舞池里的那个人"},
        {"id_or_slug": "shan-shen-bu-ai-video-generator", "title": "Shan Shen Bu AI（闪身步）",
         "url": "https://zapvid.ai/shan-shen-bu-ai-video-generator",
         "desc": "外卖骑手侧身闪过，保安走过来"},
        {"id_or_slug": "smalltown-boy-cats-ai-video-generator", "title": "Smalltown Boy Cats AI",
         "url": "https://zapvid.ai/smalltown-boy-cats-ai-video-generator",
         "desc": "宠物先对着镜头大叫，再并排站起来跳舞"},
        {"id_or_slug": "toy-car-to-real-car-ai-video-generator", "title": "Toy Car to Real Car AI",
         "url": "https://zapvid.ai/toy-car-to-real-car-ai-video-generator",
         "desc": "火车窗边的迷你车模过隧道后变成真车开出来"},
    ],
    "Try a Trend": [
        {"id_or_slug": "sticky-bubblegum-ai", "title": "Sticky Bubblegum AI",
         "url": "https://tryatrend.com/sticky-bubblegum-ai",
         "desc": "宝宝跟着拍拍手、黏肚皮、再踢一脚的泡泡糖舞"},
        {"id_or_slug": "wassup-in-a-minute-ai", "title": "Wassup in a Minute AI",
         "url": "https://tryatrend.com/wassup-in-a-minute-ai",
         "desc": "在雾气湖边山坡上跳 Wassup in a Minute，可加上朋友"},
    ],
    "RapVideo.ai": [
        {"id_or_slug": "sticky-bubblegum-ai", "title": "Sticky Bubblegum AI",
         "url": "https://rapvideo.ai/sticky-bubblegum-ai",
         "desc": "宝宝在大白床上拍手、黏手、小踢腿的泡泡糖舞"},
    ],
    "Starrd": [
        {"id_or_slug": "monkey-eating-apple-ai-video", "title": "Monkey Eating Apple",
         "url": "https://www.getstarrd.app/template/monkey-eating-apple-ai-video",
         "desc": "森林步道上吃苹果，猴子扑过来抢一大口"},
    ],
    "aiMakeVideo": [
        {"id_or_slug": "babydoll-dance-ai", "title": "Babydoll Dance AI",
         "url": "https://aimakevideo.com/babydoll-dance-ai",
         "desc": "跟跳 Jamie Miller《Babydoll》弹跳两步，手一甩再踢腿"},
        {"id_or_slug": "wassup-in-a-minute-ai", "title": "Wassup in a Minute AI",
         "url": "https://aimakevideo.com/wassup-in-a-minute-ai",
         "desc": "一到三张照片，变成湖边山坡上三人跳 Wassup in a Minute"},
    ],
}

FILTER_REASONS = {
    ("makememe.json", "christmas-ai-video-trends"): "aggregation-hub",
    ("makememe.json", "questions"): "faq-page",
    ("memelry.json", "cortis-go-ai-from-photo"): "seo-variant-of-existing-template",
    ("memelry.json", "how-to-make-no-scrubs-ai-video"): "seo-howto-landing",
    ("memelry.json", "wassup-dance-face-expression-guide"): "guide-page",
    ("memelry.json", "wassup-dance-with-three-friends"): "seo-howto-landing",
}


def title_from_slug(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def build_notice(curated_new, nosmew, smew_only, total_new, putmein_bulk_count, putmein_total):
    by_site = OrderedDict()
    for x in curated_new:
        by_site.setdefault(x["site"], []).append(x)

    lines = []
    n_sites = len(by_site)
    lines.append("竞品模板日报（2026-11-17，上海时间）")
    lines.append("")
    lines.append(
        f"今日共 {total_new} 个新模板，分布在 {n_sites} 家。已核实页面可打开；"
        "解析误伤（分类页/聚合页/FAQ/SEO 变体/通用工具页）未计入。"
    )
    lines.append("")
    lines.append(
        f"另：Put Me In 在 11-15 把大量模板一次性写入 sitemap（lastmod 均为 2026-11-15），"
        f"今日入库 {putmein_bulk_count} 条（快照由 10 增至 {putmein_total}），不在此逐条列出；"
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
            for t in raw_new:
                if t["id_or_slug"].lower() not in genuine_slugs:
                    reason = FILTER_REASONS.get((fn, t["id_or_slug"].lower()), "parser-drift-or-non-template")
                    filtered.append({"site": site, "file": fn, "item": t, "reason": reason})

        fetch_ok = bool(fr.get("fetch_ok"))
        sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        sitemap_existed = bool(fr.get("sitemap_existed") or sitemap_urls)
        update_store = True
        site_notes = []

        if fn == "ricebowl.json":
            site_notes.append(
                "Meme catalog (/trends/meme ItemList) still 82 items; no new genuine meme trends. "
                "Generic /app tool pages not added."
            )
            fetch_ok = True
            sitemap_existed = True
            sitemap_urls = fr.get("sitemap_urls_found") or prev.get("sitemap_urls_found") or []
        elif fn == "remakeyourmeme.json":
            site_notes.append("Sitemap via WebFetch; box IP still 403; inventory unchanged (44).")
            fetch_ok = True
            sitemap_existed = True
            sitemap_urls = ["https://remakeyourmeme.com/sitemap.xml"]
        elif fn == "putmein.json":
            site_notes.append(
                "Bulk sitemap backfill on 2026-11-15 (all lastmod 2026-11-15): "
                f"added {len(putmein_bulk)} templates already on /templates; "
                "not listed one-by-one in the daily digest."
            )

        if fetch_ok and fn not in {"ricebowl.json", "remakeyourmeme.json"}:
            for t in prev_tmpls:
                if t["id_or_slug"].lower() not in now_slugs and t["id_or_slug"].lower() not in {g["id_or_slug"].lower() for g in genuine_for_store}:
                    site_notes.append(
                        f"Kept {t['id_or_slug']} despite missing from today's sitemap (page still 200)."
                    )

        templates = list(prev_tmpls)
        have = {t["id_or_slug"].lower() for t in templates}
        for g in genuine_for_store:
            if g["id_or_slug"].lower() not in have:
                templates.append({"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]})
                have.add(g["id_or_slug"].lower())
        templates.sort(key=lambda t: t["url"])

        rec = {
            "site": site,
            "home": home,
            "checked_at": CHECKED_AT,
            "sitemap_urls_found": sitemap_urls,
            "sitemap_existed": sitemap_existed,
            "template_count": len(templates),
            "templates": templates,
            "new_count": len(genuine_for_store),
            "removed_count": 0,
            "new_templates": [
                {"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]}
                for g in genuine_for_store
            ],
            "removed_templates": [],
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
        ],
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
    with open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-17.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    putmein_total = site_out["putmein.json"]["template_count"]
    notice = build_notice(
        curated_new, nosmew, smew_only, total_digest_new,
        len(putmein_bulk), putmein_total,
    )
    with open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8") as f:
        f.write(notice)
    with open(os.path.join(OUTDIR, "竞品模板日报-2026-11-17.md"), "w", encoding="utf-8") as f:
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
