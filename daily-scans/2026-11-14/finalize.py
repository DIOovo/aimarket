#!/usr/bin/env python3
"""Finalize 2026-11-14 FaceOnTrend competitor scan: curate, update store, overlaps, reports."""
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
OUTDIR = "/workspace/competitor-scan-2026-11-14"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-13T09:18:30+08:00"

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
CURATED = {
    "TrendTemplate": [
        {"id_or_slug": "waist-heart-ai", "title": "Waist Heart AI", "url": "https://trendtemplate.com/waist-heart-ai",
         "desc": "下巴轻点、秀二头肌，再在腰侧用手比心的卡点动作"},
    ],
    "MakeViral": [
        {"id_or_slug": "ai-cat-gym-video", "title": "AI Cat Gym Video", "url": "https://www.makeviral.ai/templates/ai-cat-gym-video",
         "desc": "把宠物放到户外踏步机上，腿乱蹬再滑下去"},
        {"id_or_slug": "aint-you-my-gangsta-ai-trend", "title": "Ain't You My Gangsta B", "url": "https://www.makeviral.ai/templates/aint-you-my-gangsta-ai-trend",
         "desc": "对着镜头问 Ain't you my gangsta，对方喊 Yes 的对口型"},
        {"id_or_slug": "all-i-want-for-christmas-ai-trend", "title": "All I Want for Christmas Dance AI", "url": "https://www.makeviral.ai/templates/all-i-want-for-christmas-ai-trend",
         "desc": "睡衣双人/三人跳《All I Want for Christmas Is You》卡点舞"},
        {"id_or_slug": "bad-aim-edit-ai-trend", "title": "Bad Aim Edit AI Trend", "url": "https://www.makeviral.ai/templates/bad-aim-edit-ai-trend",
         "desc": "射箭屡屡打偏，再切到黑白办公室装酷剪辑"},
        {"id_or_slug": "balmain-couple-yacht-ai-trend", "title": "Balmain Earkid AI Trend", "url": "https://www.makeviral.ai/templates/balmain-couple-yacht-ai-trend",
         "desc": "游艇上自拍，转身看身边睡着的另一半"},
        {"id_or_slug": "cat-shower-ai-trend", "title": "Cat Shower AI", "url": "https://www.makeviral.ai/templates/cat-shower-ai-trend",
         "desc": "倒水洗澡，躲开每一滴再钻进毯子"},
        {"id_or_slug": "chatgpt-sweater-portrait-trend", "title": "ChatGPT Sweater Trend", "url": "https://www.makeviral.ai/templates/chatgpt-sweater-portrait-trend",
         "desc": "黑白肖像里只有厚毛衣是彩色的，袖子捂嘴"},
        {"id_or_slug": "christian-dior-dance-ai-trend", "title": "Christian Dior Dance AI", "url": "https://www.makeviral.ai/templates/christian-dior-dance-ai-trend",
         "desc": "I love Christian Dior 双人卡点舞"},
        {"id_or_slug": "christmas-photobooth-ai-trend", "title": "Christmas Photobooth Trend AI", "url": "https://www.makeviral.ai/templates/christmas-photobooth-ai-trend",
         "desc": "Last Christmas 照相亭拍立得条，一格一个姿势"},
        {"id_or_slug": "demolition-walk-ai-trend", "title": "Jake Gyllenhaal Headphones Walk AI", "url": "https://www.makeviral.ai/templates/demolition-walk-ai-trend",
         "desc": "戴墨镜耳机在人潮里走《拆弹专家》风"},
        {"id_or_slug": "favorite-rumors-about-us-ai-trend", "title": "Favorite Rumors About Us AI", "url": "https://www.makeviral.ai/templates/favorite-rumors-about-us-ai-trend",
         "desc": "情侣谣言字幕加搞怪舞，配 Zany Emote 音效"},
        {"id_or_slug": "fitting-room-outfit-change-ai-trend", "title": "Fitting Room Outfit Change AI", "url": "https://www.makeviral.ai/templates/fitting-room-outfit-change-ai-trend",
         "desc": "镜头滑过五间试衣间，拉开帘就是一套新造型"},
        {"id_or_slug": "flash-couple-silhouette-ai-photo", "title": "Flashlight Trend", "url": "https://www.makeviral.ai/templates/flash-couple-silhouette-ai-photo",
         "desc": "纯黑底暖色轮廓光双人照，头顶一颗小心心"},
        {"id_or_slug": "i-thought-it-was-a-mountain-ai-trend", "title": "I Thought It Was a Mountain AI", "url": "https://www.makeviral.ai/templates/i-thought-it-was-a-mountain-ai-trend",
         "desc": "爬上长满青苔的山，发现是恐龙脑袋并骑着飞走"},
        {"id_or_slug": "jensen-huang-ai-video", "title": "Jensen Huang AI Video", "url": "https://www.makeviral.ai/templates/jensen-huang-ai-video",
         "desc": "坐在车里和英伟达 CEO 黄仁勋并排开车"},
        {"id_or_slug": "mobland-paul-dance-ai", "title": "MobLand Dance AI", "url": "https://www.makeviral.ai/templates/mobland-paul-dance-ai",
         "desc": "MobLand 第二季里 Paul 的搞怪摇摆舞"},
        {"id_or_slug": "nyc-rats-ai-trend", "title": "NYC Rats AI", "url": "https://www.makeviral.ai/templates/nyc-rats-ai-trend",
         "desc": "纽约小巷鼠群直立对峙：Never take the shortcut"},
        {"id_or_slug": "pet-taxi-ai-trend", "title": "Cat Taxi AI", "url": "https://www.makeviral.ai/templates/pet-taxi-ai-trend",
         "desc": "巨型猫狗像巴士一样来接你下班，骑在它背上回家"},
        {"id_or_slug": "pov-outfit-transition-ai-trend", "title": "POV Outfit Transition AI", "url": "https://www.makeviral.ai/templates/pov-outfit-transition-ai-trend",
         "desc": "递出一件单品就跳切成一整套配套造型，一共六套"},
        {"id_or_slug": "talk-to-me-doja-ai-trend", "title": "Talk to Me Doja AI Trend", "url": "https://www.makeviral.ai/templates/talk-to-me-doja-ai-trend",
         "desc": "双手托脸害羞摇摆的动漫女生气，配加速 Like That"},
        {"id_or_slug": "tying-shoes-money-ai-trend", "title": "Tying My Shoes Meme", "url": "https://www.makeviral.ai/templates/tying-shoes-money-ai-trend",
         "desc": "路边放小费杯低头系鞋带，路人往里塞钱"},
    ],
    "MakeMeme.video": [
        {"id_or_slug": "baby-riding-reindeer-ai", "title": "Baby Riding Reindeer AI", "url": "https://makememe.video/baby-riding-reindeer-ai",
         "desc": "宝宝骑驯鹿跑过圣诞街，身后圣诞老人挥手"},
        {"id_or_slug": "christmas-dance-ai", "title": "Christmas Dance AI", "url": "https://makememe.video/christmas-dance-ai",
         "desc": "四套圣诞热门舞蹈可选，和朋友、孩子或宠物一起跳"},
        {"id_or_slug": "grinch-pet-filter", "title": "Grinch Pet Filter", "url": "https://makememe.video/grinch-pet-filter",
         "desc": "把猫狗变成戴圣诞帽的绿毛怪 Grinch"},
    ],
    "MemeClone.ai": [
        {"id_or_slug": "christmas-elf", "title": "Elf Yourself AI", "url": "https://memeclone.ai/templates/christmas-elf",
         "desc": "把自己变成工坊小精灵，跳 Deck the Halls x Blow the Whistle 面瘫舞"},
    ],
    "SameVid AI": [
        {"id_or_slug": "ai-alligator-dance", "title": "AI Alligator Dance", "url": "https://samevid.com/template/ai-alligator-dance",
         "desc": "蓝格子床上的鳄鱼舞"},
        {"id_or_slug": "almost-almost-ai-trend", "title": "Almost Almost AI Trend", "url": "https://samevid.com/template/almost-almost-ai-trend",
         "desc": "快餐赶工狂包汉堡，关键一扔两次都差一寸"},
        {"id_or_slug": "alvin-and-the-chipmunks-ai", "title": "Alvin and the Chipmunks AI", "url": "https://samevid.com/template/alvin-and-the-chipmunks-ai",
         "desc": "花栗鼠三人组跳 You Spin Me Round"},
        {"id_or_slug": "barbie-girl-dance-ai-trend", "title": "Barbie Girl Dance AI Trend", "url": "https://samevid.com/template/barbie-girl-dance-ai-trend",
         "desc": "Come on Barbie let's go party，Aqua《Barbie Girl》双人卡点舞"},
        {"id_or_slug": "beans-greens-potatoes-tomatoes-ai-video", "title": "Beans Greens Potatoes Tomatoes AI Video", "url": "https://samevid.com/template/beans-greens-potatoes-tomatoes-ai-video",
         "desc": "感恩节菜单布道 Remix：beans, greens, potatoes, tomatoes"},
        {"id_or_slug": "davul-zurna-ai-trend", "title": "Davul Zurna AI Trend", "url": "https://samevid.com/template/davul-zurna-ai-trend",
         "desc": "土耳其鼓号 Davul Zurna：在作坊里跟着现场乐边走边唱"},
        {"id_or_slug": "distracted-boyfriend-ai-meme", "title": "Distracted Boyfriend AI Meme", "url": "https://samevid.com/template/distracted-boyfriend-ai-meme",
         "desc": "经典路人分神男友梗，带反转结局"},
        {"id_or_slug": "elsa-ai-video", "title": "Elsa AI Video", "url": "https://samevid.com/template/elsa-ai-video",
         "desc": "冰雪奇缘冰宫里唱 Let It Go，裙子变装"},
        {"id_or_slug": "hit-me-baby-one-more-time-ai-video", "title": "Hit Me Baby One More Time AI Video", "url": "https://samevid.com/template/hit-me-baby-one-more-time-ai-video",
         "desc": "把自己放进 1998 年 Britney 校园走廊 MV"},
        {"id_or_slug": "jurassic-run-ai", "title": "Jurassic Run AI", "url": "https://samevid.com/template/jurassic-run-ai",
         "desc": "被 T-Rex 追着狂奔的侏罗纪逃亡"},
        {"id_or_slug": "old-town-road-ai-video", "title": "Old Town Road AI Video", "url": "https://samevid.com/template/old-town-road-ai-video",
         "desc": "开红敞篷唱《Old Town Road》"},
        {"id_or_slug": "starbucks-sandwich-meme-ai", "title": "Starbucks Sandwich Meme AI", "url": "https://samevid.com/template/starbucks-sandwich-meme-ai",
         "desc": "星巴克三明治馅谜肉的反应梗"},
        {"id_or_slug": "staring-at-me-mad-ai", "title": "She's Staring At Me Mad AI", "url": "https://samevid.com/template/staring-at-me-mad-ai",
         "desc": "巷子里对着烟盒生闷气，朋友跳 Ne-Yo《Mad》瞪你"},
        {"id_or_slug": "yan-diomande-ai", "title": "Yan Diomande AI", "url": "https://samevid.com/template/yan-diomande-ai",
         "desc": "足球运动员 Yan Diomande 式进球庆祝舞"},
    ],
    "Try a Trend": [
        {"id_or_slug": "waist-heart-ai", "title": "Waist Heart AI", "url": "https://tryatrend.com/waist-heart-ai",
         "desc": "侧腰双手比心的卡点姿势"},
    ],
    "Summrs": [
        {"id_or_slug": "cortis-go-ai-video-generator", "title": "CORTIS GO! AI Video", "url": "https://www.summrs.com/cortis-go-ai-video-generator",
         "desc": "K-Pop 组合 CORTIS《GO!》四人对卡点舞"},
        {"id_or_slug": "m-row-bad-day-ai-video-generator", "title": "M Row Bad Day AI Video", "url": "https://www.summrs.com/m-row-bad-day-ai-video-generator",
         "desc": "把自己放进 WhoRunItNYC 的 M Row Bad Day 表演"},
    ],
    "Starrd": [
        {"id_or_slug": "all-i-want-for-christmas-is-you-ai-video", "title": "All I Want for Christmas Is You", "url": "https://www.getstarrd.app/template/all-i-want-for-christmas-is-you-ai-video",
         "desc": "红裙站上圣诞舞台唱现场版《All I Want for Christmas Is You》"},
        {"id_or_slug": "bigxthaplug-give-it-all-ai-video", "title": "Give It All", "url": "https://www.getstarrd.app/template/bigxthaplug-give-it-all-ai-video",
         "desc": "电影厅大堂吊麦，唱 BigXthaPlug《Give It All》"},
        {"id_or_slug": "hotline-bling-pt-2-dance-ai-video", "title": "Hotline Bling Pt 2", "url": "https://www.getstarrd.app/template/hotline-bling-pt-2-dance-ai-video",
         "desc": "Drake《Hotline Bling》MV 第二段，五段光房造型快切"},
    ],
    "aiMakeVideo": [
        {"id_or_slug": "gangstas-paradise-ai", "title": "Gangsta's Paradise AI", "url": "https://aimakevideo.com/gangstas-paradise-ai",
         "desc": "两人分唱《Gangsta's Paradise》主歌/副歌，背后一排黄色防护服合唱"},
        {"id_or_slug": "no-scrubs-ai", "title": "No Scrubs AI", "url": "https://aimakevideo.com/no-scrubs-ai",
         "desc": "银色飞船场景，三人跳 TLC《No Scrubs》"},
    ],
    "Ricebowl AI": [
        {"id_or_slug": "car-chips-prank-ai-trend", "title": "Car Chips Prank AI Trend", "url": "https://ricebowl.ai/app/car-chips-prank-ai-trend",
         "desc": "车里偷薯片、找最后一片的恶作剧（Careless Whisper 那支）"},
        {"id_or_slug": "rubber-band-prank-ai-trend", "title": "Rubber Band Prank AI Trend", "url": "https://ricebowl.ai/app/rubber-band-prank-ai-trend",
         "desc": "皮筋恶作剧，最后反弹打到捣蛋的那只宠物"},
        {"id_or_slug": "i-love-the-smiths-ai-trend", "title": "I Love the Smiths AI Trend", "url": "https://ricebowl.ai/app/i-love-the-smiths-ai-trend",
         "desc": "公园长椅上共用一副耳机，一句 I love the Smiths"},
        {"id_or_slug": "permission-to-cry-sir-ai-trend", "title": "Permission to Cry Sir AI Trend", "url": "https://ricebowl.ai/app/permission-to-cry-sir-ai-trend",
         "desc": "敬礼之后哭出来"},
        {"id_or_slug": "ai-baby-gangster", "title": "AI Baby Gangster", "url": "https://ricebowl.ai/app/ai-baby-gangster",
         "desc": "把自己变成卡通小黑帮，坐在汽车安全座椅里装老大"},
    ],
}

# Manual core aliases after suffix stripping
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
                "Sitemap is reachable again, but inventory stays meme-catalog only "
                "(/trends/meme ItemList, not all /app pages). Added 5 genuine meme trends; "
                "generic tools on the catalog were excluded."
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
        kept_missing = []
        if fetch_ok and fn not in {"ricebowl.json", "remakeyourmeme.json"}:
            for t in prev_tmpls:
                if t["id_or_slug"].lower() not in now_slugs and t["id_or_slug"].lower() not in genuine_slugs:
                    # page still live (we checked the three known cases); keep
                    kept_missing.append(t)
                    site_notes.append(
                        f"Kept {t['id_or_slug']} despite missing from today's sitemap (page still 200)."
                    )

        templates = list(prev_tmpls)
        # append genuine new
        have = {t["id_or_slug"].lower() for t in templates}
        for g in genuine:
            if g["id_or_slug"].lower() not in have:
                templates.append(g)
                have.add(g["id_or_slug"].lower())
        templates.sort(key=lambda t: t["url"])

        rec = {
            "site": site,
            "home": home,
            "checked_at": CHECKED_AT if update_store else prev.get("checked_at"),
            "sitemap_urls_found": sitemap_urls,
            "sitemap_existed": sitemap_existed,
            "template_count": len(templates),
            "templates": templates,
            "new_count": len(genuine) if update_store else 0,
            "removed_count": 0,
            "new_templates": genuine if update_store else prev.get("new_templates", []),
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
    with open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-14.md"), "w", encoding="utf-8") as f:
        f.write(md_nosmew)

    # User-facing Chinese notice
    notice = build_notice(curated_new, involving_new, nosmew, smew_only, total_new)
    with open(os.path.join(OUTDIR, "notice-zh.txt"), "w", encoding="utf-8") as f:
        f.write(notice)
    # report-zh
    report = build_report(
        CHECKED_AT, notes_by_file, site_out, fetch, curated_new, filtered,
        involving_new, nosmew, smew_only, total_new, total_templates, notice,
    )
    with open(os.path.join(OUTDIR, "report-zh.md"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(OUTDIR, "竞品模板日报-2026-11-14.md"), "w", encoding="utf-8") as f:
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


def build_notice(curated_new, involving_new, nosmew, smew_only, total_new):
    from collections import OrderedDict
    by_site = OrderedDict()
    for x in curated_new:
        by_site.setdefault(x["site"], []).append(x)

    lines = []
    n_sites = len(by_site)
    lines.append(f"竞品模板日报（2026-11-14，上海时间）")
    lines.append("")
    lines.append(f"今日共 {total_new} 个新模板，分布在 {n_sites} 家。已核实页面可打开；解析误伤（图标/政策页/分类页/SEO 变体/通用工具页）未计入。")
    lines.append("")
    for site, items in by_site.items():
        lines.append(f"【{site}】{len(items)} 个")
        for x in items:
            it = x["item"]
            lines.append(f"- {it['title']}：{x['desc']}")
            lines.append(f"  {it['url']}")
        lines.append("")

    # 多家共有 section for the user notice
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
                lines.append(f"· {o['name']}（{o['site_count']} 家，今日新增 {len(o['new_sites'])} 家）：" + " ｜ ".join(bits) + smew_note)
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


def build_report(checked_at, notes_by_file, site_out, fetch, curated_new, filtered,
                 involving_new, nosmew, smew_only, total_new, total_templates, notice):
    # The user-facing digest is the main body, plus a health appendix? Yesterday report-zh WAS the notice itself (long smew list).
    # I'll use the notice as the main report, and also we have notice-zh.txt.
    return notice


if __name__ == "__main__":
    main()
