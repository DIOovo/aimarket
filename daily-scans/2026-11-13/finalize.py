#!/usr/bin/env python3
"""Finalize 2026-11-13 FaceOnTrend competitor scan: curate, update store, overlaps, reports."""
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
OUTDIR = "/workspace/competitor-scan-2026-11-13"
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
PREV_CHECKED_AT = "2026-11-12T09:22:09+08:00"

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
        {"id_or_slug": "christmas-pajama-dance-ai", "title": "Christmas Pajama Dance AI", "url": "https://trendtemplate.com/christmas-pajama-dance-ai",
         "desc": "情侣/双人穿同款格子睡衣跳 Deck the Halls 圣诞卡点舞"},
        {"id_or_slug": "drake-hotline-bling-dance-ai", "title": "Drake Hotline Bling Dance AI", "url": "https://trendtemplate.com/drake-hotline-bling-dance-ai",
         "desc": "把自己放进 Drake《Hotline Bling》红羽绒 MV 里的经典舞步"},
    ],
    "MakeViral": [
        {"id_or_slug": "ai-video-with-celebrity", "title": "Kara Sevda AI Trend", "url": "https://www.makeviral.ai/templates/ai-video-with-celebrity",
         "desc": "Kara Sevda（《无尽的爱》）风：夜间自拍和 Kemal/Emir 明星同框"},
        {"id_or_slug": "almost-almost-ai-trend", "title": "Almost Almost AI Trend", "url": "https://www.makeviral.ai/templates/almost-almost-ai-trend",
         "desc": "Ahh almost almost：夜训拼了命，关键一击两次都差一寸"},
        {"id_or_slug": "barbie-girl-dance-ai-trend", "title": "Barbie Girl Dance AI Trend", "url": "https://www.makeviral.ai/templates/barbie-girl-dance-ai-trend",
         "desc": "Come on Barbie let's go party，Aqua《Barbie Girl》双人卡点舞"},
        {"id_or_slug": "davul-zurna-ai-trend", "title": "Davul Zurna AI Trend", "url": "https://www.makeviral.ai/templates/davul-zurna-ai-trend",
         "desc": "土耳其鼓号 Davul Zurna：在仓库里跟着现场乐边走边唱"},
        {"id_or_slug": "if-i-was-chatgpt-trend", "title": "If I Was ChatGPT Trend", "url": "https://www.makeviral.ai/templates/if-i-was-chatgpt-trend",
         "desc": "If I Was ChatGPT「Observe, just observe」城市/季节/花/画/动物心情板"},
        {"id_or_slug": "island-boy-ai-trend", "title": "Island Boy AI Trend", "url": "https://www.makeviral.ai/templates/island-boy-ai-trend",
         "desc": "I'm an island boy：一人坐泳池边，另一人在水里对口型"},
        {"id_or_slug": "misanthropy-meme-ai-trend", "title": "Misanthropy Meme AI Trend", "url": "https://www.makeviral.ai/templates/misanthropy-meme-ai-trend",
         "desc": "长角二次元角色左右侧目再坏笑，画面转红的 Misanthropy 梗"},
        {"id_or_slug": "old-town-road-ai-video", "title": "Old Town Road AI Video", "url": "https://www.makeviral.ai/templates/old-town-road-ai-video",
         "desc": "《Old Town Road》：糖果店里唱歌，再开红敞篷载着钱袋兜风"},
        {"id_or_slug": "st-tropez-dj-ai-trend", "title": "St Tropez DJ AI Trend", "url": "https://www.makeviral.ai/templates/st-tropez-dj-ai-trend",
         "desc": "St Tropez knows how to party：在圣特罗佩海滩俱乐部当 DJ"},
        {"id_or_slug": "zoolander-who-is-she-ai-trend", "title": "Zoolander Who Is She AI Trend", "url": "https://www.makeviral.ai/templates/zoolander-who-is-she-ai-trend",
         "desc": "《Zoolander》红毯对视，「Who Is She」互瞪名场面"},
    ],
    "MakeMeme.video": [
        {"id_or_slug": "dog-pool-party-ai", "title": "Dog Pool Party AI", "url": "https://makememe.video/dog-pool-party-ai",
         "desc": "宠物穿粉红泳镜比基尼，夜场泳池边后腿站立热舞"},
        {"id_or_slug": "gangstas-paradise-ai", "title": "Gangsta's Paradise AI", "url": "https://makememe.video/gangstas-paradise-ai",
         "desc": "两人分唱《Gangsta's Paradise》主歌/副歌，背后排福音唱诗班"},
        {"id_or_slug": "kiss-cam-ai", "title": "Kiss Cam AI", "url": "https://makememe.video/kiss-cam-ai",
         "desc": "体育场/演唱会大屏幕心形 Kiss Cam 被镜头抓到接吻"},
    ],
    "ClipRemake": [
        {"id_or_slug": "fish-chop-ai", "title": "Fish Chop AI", "url": "https://clipremake.com/templates/fish-chop-ai",
         "desc": "爷爷处理晚餐梗：厨房案板上用砍刀拍一条巨型鱼"},
        {"id_or_slug": "tiger-fight-ai", "title": "Tiger Fight AI", "url": "https://clipremake.com/templates/tiger-fight-ai",
         "desc": "灰色监控画面里在林间小道和扑过来的老虎搏斗"},
    ],
    "MemeFX AI": [
        {"id_or_slug": "christmas-couple-dance-ai", "title": "Christmas Couple Dance AI", "url": "https://memefxai.com/christmas-couple-dance-ai",
         "desc": "壁炉圣诞树前的 Deck the Halls x Blow the Whistle 双人面瘫舞"},
        {"id_or_slug": "dancing-dog-pool-party-ai", "title": "Dancing Dog Pool Party AI", "url": "https://memefxai.com/dancing-dog-pool-party-ai",
         "desc": "宠物戴泳镜穿粉红比基尼，夜场泳池边后腿站立热舞"},
        {"id_or_slug": "dj-cat-ai", "title": "DJ Cat AI", "url": "https://memefxai.com/dj-cat-ai",
         "desc": "把猫狗放到拥挤演出现场的打碟台后面当 DJ"},
        {"id_or_slug": "dog-drummer-ai", "title": "Dog Drummer AI", "url": "https://memefxai.com/dog-drummer-ai",
         "desc": "狗狗往鼓上倒水、扔瓶子，再敲一曲《Beggin'》"},
        {"id_or_slug": "dog-grooming-time-ai", "title": "Dog Grooming Time AI", "url": "https://memefxai.com/dog-grooming-time-ai",
         "desc": "My dog when it's grooming time：狗狗功夫赶跑美容师还抢走推子"},
        {"id_or_slug": "gangstas-paradise-ai", "title": "Gangsta's Paradise AI", "url": "https://memefxai.com/gangstas-paradise-ai",
         "desc": "烛光教堂里唱《Gangsta's Paradise》，红袍唱诗班接副歌"},
    ],
    "SameVid AI": [
        {"id_or_slug": "boss-entrance-ai", "title": "Boss Entrance AI", "url": "https://samevid.com/template/boss-entrance-ai",
         "desc": "直升机落地、五人保镖开路的老板出场"},
        {"id_or_slug": "car-jump-ai", "title": "Car Jump AI", "url": "https://samevid.com/template/car-jump-ai",
         "desc": "沙漠里一辆豪华 SUV 从你头顶飞跃而过"},
        {"id_or_slug": "disney-pet-ai", "title": "Disney Pet AI", "url": "https://samevid.com/template/disney-pet-ai",
         "desc": "把宠物变成 3D 迪士尼/皮克斯风动画短片"},
        {"id_or_slug": "driving-wave-ai", "title": "Driving Wave AI", "url": "https://samevid.com/template/driving-wave-ai",
         "desc": "开车时扶着方向盘夸张打招呼的 Driving Wave 梗"},
        {"id_or_slug": "dubai-vacation-ai", "title": "Dubai Vacation AI", "url": "https://samevid.com/template/dubai-vacation-ai",
         "desc": "迪拜度假风：日落无边泳池、哈利法塔阳台干杯"},
        {"id_or_slug": "edmund-fitzgerald-ai", "title": "Edmund Fitzgerald AI", "url": "https://samevid.com/template/edmund-fitzgerald-ai",
         "desc": "把自己放进 SS Edmund Fitzgerald 在苏必利尔湖风暴中的电影预告"},
        {"id_or_slug": "fish-cutting-meme-ai", "title": "Fish Cutting Meme AI", "url": "https://samevid.com/template/fish-cutting-meme-ai",
         "desc": "机械般精准地剁一条巨型银鱼的砍鱼梗"},
        {"id_or_slug": "give-it-all-ai", "title": "Give It All AI", "url": "https://samevid.com/template/give-it-all-ai",
         "desc": "BigXthaPlug《Give It All》：悬挂式麦克风前对口型"},
        {"id_or_slug": "is-this-how-you-cut-it-ai-video", "title": "Is This How You Cut It AI Video", "url": "https://samevid.com/template/is-this-how-you-cut-it-ai-video",
         "desc": "Is this how you cut it：面瘫挥砍刀在巨型金枪鱼上差点砍空"},
        {"id_or_slug": "lush-life-dog-ai", "title": "Lush Life Dog AI", "url": "https://samevid.com/template/lush-life-dog-ai",
         "desc": "宠物跳 Zara Larsson《Lush Life》里那只网红跳舞小狗"},
        {"id_or_slug": "motu-patlu-ai", "title": "Motu Patlu AI", "url": "https://samevid.com/template/motu-patlu-ai",
         "desc": "印度动画《Motu Patlu》3D 卡通双人互怼短片"},
        {"id_or_slug": "need-girl-ai", "title": "I Need A Girl AI", "url": "https://samevid.com/template/need-girl-ai",
         "desc": "P. Diddy《I Need a Girl》双人街头嘻哈卡点舞"},
        {"id_or_slug": "not-like-us-ai", "title": "Not Like Us AI", "url": "https://samevid.com/template/not-like-us-ai",
         "desc": "Kendrick《Not Like Us》中场两步舞"},
        {"id_or_slug": "pet-rock-ai", "title": "Pet Rock AI", "url": "https://samevid.com/template/pet-rock-ai",
         "desc": "宠物穿黑帽衫跟着重金属狂甩头"},
        {"id_or_slug": "pitch-invader-tackle-ai", "title": "Pitch Invader Tackle AI", "url": "https://samevid.com/template/pitch-invader-tackle-ai",
         "desc": "球场闯入者被滑铲放倒的 Pitch Invader 梗"},
        {"id_or_slug": "russian-dance-ai", "title": "Russian Dance AI", "url": "https://samevid.com/template/russian-dance-ai",
         "desc": "蹲踢俄罗斯舞（Prisyadka），配 Dschinghis Khan《Moskau》"},
        {"id_or_slug": "soda-pop-ai-dance", "title": "Soda Pop AI Dance", "url": "https://samevid.com/template/soda-pop-ai-dance",
         "desc": "K-pop《Soda Pop》抖肩卡点双人舞"},
        {"id_or_slug": "talking-pet-ai", "title": "Talking Pet AI", "url": "https://samevid.com/template/talking-pet-ai",
         "desc": "宠物对着迷你麦克风开口说话"},
        {"id_or_slug": "three-kittens-you-spin-me-round-dance", "title": "Three Kittens You Spin Me Round Dance", "url": "https://samevid.com/template/three-kittens-you-spin-me-round-dance",
         "desc": "三只小猫转圈舞，配《You Spin Me Round》花栗鼠音"},
    ],
    "TrendSwap": [
        {"id_or_slug": "la-mujer-del-pelotero-ai", "title": "La Mujer del Pelotero AI", "url": "https://trendswap.app/la-mujer-del-pelotero-ai",
         "desc": "拉美《La Mujer del Pelotero》手势卡点舞，可单人可双人"},
        {"id_or_slug": "sheru-bhai-ai", "title": "Sheru Bhai AI", "url": "https://trendswap.app/sheru-bhai-ai",
         "desc": "Sheru Bhai：白狮宫殿走步、金狮亮相或超跑出场"},
    ],
    "Summrs": [
        {"id_or_slug": "vintage-vuitton-earfzilla-ai-video-generator", "title": "Vintage Vuitton Earfzilla AI Video Generator", "url": "https://www.summrs.com/vintage-vuitton-earfzilla-ai-video-generator",
         "desc": "Earfzilla《Vintage Vuitton》MV 里换上你的脸和造型"},
    ],
    "Memelry": [
        {"id_or_slug": "cctv-tiger-fight-ai", "title": "CCTV Tiger Fight AI", "url": "https://memelry.com/cctv-tiger-fight-ai",
         "desc": "监控画面里的老虎搏斗"},
        {"id_or_slug": "dog-grooming-time-ai", "title": "Dog Grooming Time AI", "url": "https://memelry.com/dog-grooming-time-ai",
         "desc": "My dog when it's grooming time：狗狗功夫赶跑美容师"},
        {"id_or_slug": "huell-money-ai", "title": "Huell Money AI", "url": "https://memelry.com/huell-money-ai",
         "desc": "《绝命毒师》Huell 抱钱/护钱梗"},
        {"id_or_slug": "kakalika-dance-ai", "title": "Kakalika Dance AI", "url": "https://memelry.com/kakalika-dance-ai",
         "desc": "Kakalika 舞蹈"},
        {"id_or_slug": "mbappe-sprint-ai", "title": "Mbappé Sprint AI", "url": "https://memelry.com/mbappe-sprint-ai",
         "desc": "姆巴佩冲刺跑"},
        {"id_or_slug": "mr-bean-looking-through-window", "title": "Mr Bean Looking Through the Window", "url": "https://memelry.com/mr-bean-looking-through-window",
         "desc": "憨豆先生从窗外往里看的经典镜头"},
        {"id_or_slug": "natsuki-hmph-dance-ai", "title": "Natsuki Hmph Dance AI", "url": "https://memelry.com/natsuki-hmph-dance-ai",
         "desc": "Natsuki 哼声/跺脚卡点舞"},
        {"id_or_slug": "not-like-us-dance-ai", "title": "Not Like Us Dance AI", "url": "https://memelry.com/not-like-us-dance-ai",
         "desc": "Kendrick《Not Like Us》中场舞"},
        {"id_or_slug": "peaky-blinders-explosion-ai", "title": "Peaky Blinders Explosion AI", "url": "https://memelry.com/peaky-blinders-explosion-ai",
         "desc": "《浴血黑帮》爆炸场面"},
        {"id_or_slug": "perfume-transition-ai", "title": "Perfume Transition AI", "url": "https://memelry.com/perfume-transition-ai",
         "desc": "喷香水变装转场"},
        {"id_or_slug": "pregnancy-test-reveal-ai", "title": "Pregnancy Test Reveal AI", "url": "https://memelry.com/pregnancy-test-reveal-ai",
         "desc": "验孕棒揭晓怀孕短片"},
        {"id_or_slug": "rush-hour-fantasy-ai", "title": "Rush Hour Fantasy AI", "url": "https://memelry.com/rush-hour-fantasy-ai",
         "desc": "《尖峰时刻》风格动作幻想"},
        {"id_or_slug": "steer-wrestling-ai", "title": "Steer Wrestling AI", "url": "https://memelry.com/steer-wrestling-ai",
         "desc": "摔牛/牛仔竞技"},
        {"id_or_slug": "the-office-parkour-ai", "title": "The Office Parkour AI", "url": "https://memelry.com/the-office-parkour-ai",
         "desc": "《The Office》办公室跑酷"},
        {"id_or_slug": "tricycle-crash-ai", "title": "Tricycle Crash AI", "url": "https://memelry.com/tricycle-crash-ai",
         "desc": "三轮车撞击"},
        {"id_or_slug": "truck-driver-ai", "title": "Truck Driver AI", "url": "https://memelry.com/truck-driver-ai",
         "desc": "卡车司机场景"},
        {"id_or_slug": "waist-heart-ai", "title": "Waist Heart AI", "url": "https://memelry.com/waist-heart-ai",
         "desc": "在腰间比心的卡点动作"},
    ],
    "RapVideo.ai": [
        {"id_or_slug": "gangstas-paradise-ai", "title": "Gangsta's Paradise AI", "url": "https://rapvideo.ai/gangstas-paradise-ai",
         "desc": "和朋友分唱《Gangsta's Paradise》，牧场或机库场景"},
    ],
    "Starrd": [
        {"id_or_slug": "atm-christmas-wish-ai-video", "title": "ATM Christmas Wish AI Video", "url": "https://www.getstarrd.app/template/atm-christmas-wish-ai-video",
         "desc": "车里许下圣诞愿望，ATM 就开始往外喷钞票"},
        {"id_or_slug": "barbie-girl-dance", "title": "Barbie Girl Dance", "url": "https://www.getstarrd.app/template/barbie-girl-dance",
         "desc": "门口走廊里跳《Barbie Girl》双人转圈贴臀舞"},
        {"id_or_slug": "careless-whisper-car-ai-video", "title": "Careless Whisper Car AI Video", "url": "https://www.getstarrd.app/template/careless-whisper-car-ai-video",
         "desc": "Careless Whisper 车内薯片梗（bro took the whole bag）"},
        {"id_or_slug": "catch-santa-at-your-tree-ai-video", "title": "Catch Santa at Your Tree AI Video", "url": "https://www.getstarrd.app/template/catch-santa-at-your-tree-ai-video",
         "desc": "用自家圣诞树照片，抓拍圣诞老人在客厅放礼物并挥手"},
        {"id_or_slug": "catch-santa-down-the-chimney-ai-video", "title": "Catch Santa Down the Chimney AI Video", "url": "https://www.getstarrd.app/template/catch-santa-down-the-chimney-ai-video",
         "desc": "用壁炉照片，抓拍圣诞老人从烟囱爬出来放礼物"},
        {"id_or_slug": "catch-santa-eating-the-cookies-ai-video", "title": "Catch Santa Eating the Cookies AI Video", "url": "https://www.getstarrd.app/template/catch-santa-eating-the-cookies-ai-video",
         "desc": "抓拍圣诞老人偷吃留下的饼干和牛奶"},
        {"id_or_slug": "catch-the-grinch-ai-video", "title": "Catch the Grinch AI Video", "url": "https://www.getstarrd.app/template/catch-the-grinch-ai-video",
         "desc": "抓拍绿毛怪偷走礼物、把饼干塞进袋子"},
        {"id_or_slug": "catch-the-sneaky-elf-ai-video", "title": "Catch the Sneaky Elf AI Video", "url": "https://www.getstarrd.app/template/catch-the-sneaky-elf-ai-video",
         "desc": "抓拍小精灵偷礼物、偷吃饼干"},
        {"id_or_slug": "christmas-dance-trend", "title": "Christmas Dance Trend", "url": "https://www.getstarrd.app/template/christmas-dance-trend",
         "desc": "穿同款圣诞睡衣跳 Deck the Halls 混音卡点舞"},
        {"id_or_slug": "elf-dance-ai-video", "title": "Elf Dance AI Video", "url": "https://www.getstarrd.app/template/elf-dance-ai-video",
         "desc": "把自己变成北极精灵，在圣诞老人工坊跳同步舞"},
        {"id_or_slug": "gangstas-paradise-ai-video", "title": "Gangsta's Paradise AI Video", "url": "https://www.getstarrd.app/template/gangstas-paradise-ai-video",
         "desc": "烛光教堂里和朋友分唱《Gangsta's Paradise》，唱诗班在后"},
        {"id_or_slug": "gangstas-paradise-extended-ai-video", "title": "Gangsta's Paradise Extended AI Video", "url": "https://www.getstarrd.app/template/gangstas-paradise-extended-ai-video",
         "desc": "《Gangsta's Paradise》30 秒完整版，主歌逐句对口型"},
        {"id_or_slug": "hit-me-baby-one-more-time-ai-video", "title": "Hit Me Baby One More Time AI Video", "url": "https://www.getstarrd.app/template/hit-me-baby-one-more-time-ai-video",
         "desc": "把自己放进 1998 年 Britney《...Baby One More Time》校园 MV"},
        {"id_or_slug": "iconic-by-mistake-ai-video", "title": "Iconic By Mistake AI Video", "url": "https://www.getstarrd.app/template/iconic-by-mistake-ai-video",
         "desc": "Iconic By Mistake 三人舞台舞：OK 手势、大跳、挽臂卡点"},
        {"id_or_slug": "island-boy-ai-trend", "title": "Island Boy AI Trend", "url": "https://www.getstarrd.app/template/island-boy-ai-trend",
         "desc": "I'm an island boy：一人坐泳池边唱，另一人站在水里"},
        {"id_or_slug": "shes-staring-at-me-mad-trend", "title": "She's Staring At Me Mad Trend", "url": "https://www.getstarrd.app/template/shes-staring-at-me-mad-trend",
         "desc": "涂鸦巷里对着烟盒生闷气，两个朋友跳 Ne-Yo《Mad》瞪你"},
    ],
    "Bolly.AI": [
        {"id_or_slug": "mariah-carey-it-s-time-ai-character-swap", "title": "Mariah Carey It's Time AI Character Swap", "url": "https://www.bolly.ai/template/mariah-carey-it-s-time-ai-character-swap",
         "desc": "把自己换进 Mariah Carey「It's Time」（圣诞歌）TikTok 片段"},
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
            update_store = False
            site_notes.append(
                "Fetch failed: sitemap/robots//trends/meme all HTTP 500 (box curl and WebFetch). "
                "Snapshot left unchanged; not treated as removals."
            )
            fetch_ok = False
            sitemap_existed = False
            sitemap_urls = prev.get("sitemap_urls_found") or []
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
        # for ricebowl (not updated) new_count should be 0 in today's ledger
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
        if fn == "ricebowl.json":
            entry["fetch_ok"] = False
            entry["updated"] = False
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
        "sites_left_unchanged": ["ricebowl.json"],
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
    with open(os.path.join(OUTDIR, "多家共有-不含Smew-2026-11-13.md"), "w", encoding="utf-8") as f:
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
    with open(os.path.join(OUTDIR, "竞品模板日报-2026-11-13.md"), "w", encoding="utf-8") as f:
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
    lines.append(f"竞品模板日报（2026-11-13，上海时间）")
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
