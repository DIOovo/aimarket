#!/usr/bin/env python3
import json, os, re, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from html import unescape

OUTDIR = "/workspace/competitor-scan-2026-11-22"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
CTX = ssl.create_default_context()

# Curated possible-genuine + keep-alive + a few suspected categories
candidates = [
    # MakeViral
    ("makeviral.json", "bandit-juice-wrld-ai-trend", "https://www.makeviral.ai/templates/bandit-juice-wrld-ai-trend"),
    ("makeviral.json", "black-and-white-wet-look-ai-photo", "https://www.makeviral.ai/templates/black-and-white-wet-look-ai-photo"),
    ("makeviral.json", "eight-legends-ai-trend", "https://www.makeviral.ai/templates/eight-legends-ai-trend"),
    ("makeviral.json", "homesick-for-a-person-ai-trend", "https://www.makeviral.ai/templates/homesick-for-a-person-ai-trend"),
    ("makeviral.json", "keep-going-run-ai-trend", "https://www.makeviral.ai/templates/keep-going-run-ai-trend"),
    ("makeviral.json", "love-handstand-ai-trend", "https://www.makeviral.ai/templates/love-handstand-ai-trend"),
    ("makeviral.json", "low-budget-amanda-ai-trend", "https://www.makeviral.ai/templates/low-budget-amanda-ai-trend"),
    ("makeviral.json", "mecha-ride-ai-trend", "https://www.makeviral.ai/templates/mecha-ride-ai-trend"),
    ("makeviral.json", "vlogmas-intro-ai-cartoon", "https://www.makeviral.ai/templates/vlogmas-intro-ai-cartoon"),
    ("makeviral.json", "waiting-on-my-fries-ai-trend", "https://www.makeviral.ai/templates/waiting-on-my-fries-ai-trend"),
    # MakeMeme
    ("makememe.json", "boom-clap-confetti-ai", "https://makememe.video/boom-clap-confetti-ai"),
    ("makememe.json", "huss-huss-huss-ai", "https://makememe.video/huss-huss-huss-ai"),
    # TrendTemplate
    ("trendtemplate.json", "frozen-viking-warrior-ai", "https://trendtemplate.com/frozen-viking-warrior-ai"),
    ("trendtemplate.json", "vlogmas-intro-ai", "https://trendtemplate.com/vlogmas-intro-ai"),
    # Try a Trend
    ("tryatrend.json", "gta-6-jet-ski-dog-ai", "https://tryatrend.com/gta-6-jet-ski-dog-ai"),
    ("tryatrend.json", "gta-6-loading-screen-ai", "https://tryatrend.com/gta-6-loading-screen-ai"),
    ("tryatrend.json", "huss-huss-huss-ai", "https://tryatrend.com/huss-huss-huss-ai"),
    ("tryatrend.json", "ai-halloween-costume", "https://tryatrend.com/ai-halloween-costume"),  # keep-alive
    # ClipRemake
    ("clipremake.json", "gta-6-jet-ski-dog-ai", "https://clipremake.com/templates/gta-6-jet-ski-dog-ai"),
    ("clipremake.json", "thanksgiving-dance-ai", "https://clipremake.com/templates/thanksgiving-dance-ai"),
    # DanceRemake
    ("danceremake.json", "give-it-all-ai", "https://danceremake.com/templates/give-it-all-ai"),
    ("danceremake.json", "thanksgiving-dance-ai", "https://danceremake.com/templates/thanksgiving-dance-ai"),
    # Put Me In
    ("putmein.json", "58th-floor-ai-trend", "https://putmein.app/templates/58th-floor-ai-trend"),
    ("putmein.json", "window-peeper-ai-trend", "https://putmein.app/templates/window-peeper-ai-trend"),
    # aiMakeVideo
    ("aimakevideo.json", "boom-clap-ai", "https://aimakevideo.com/boom-clap-ai"),
    # Starrd
    ("starrd.json", "ai-christmas-photo", "https://www.getstarrd.app/template/ai-christmas-photo"),
    ("starrd.json", "break-a-leg-crab-ai-video", "https://www.getstarrd.app/template/break-a-leg-crab-ai-video"),
    ("starrd.json", "convertible-drift-ai-video", "https://www.getstarrd.app/template/convertible-drift-ai-video"),
    ("starrd.json", "how-long-you-been-faithful-meme-ai-video", "https://www.getstarrd.app/template/how-long-you-been-faithful-meme-ai-video"),
    ("starrd.json", "stop-humiliating-yourself-rush-hour-ai-video", "https://www.getstarrd.app/template/stop-humiliating-yourself-rush-hour-ai-video"),
    ("starrd.json", "truck-jump-ai-video", "https://www.getstarrd.app/template/truck-jump-ai-video"),
    ("starrd.json", "what-makes-you-beautiful-ai-video", "https://www.getstarrd.app/template/what-makes-you-beautiful-ai-video"),
    ("starrd.json", "who-said-something-about-oil-ai-video", "https://www.getstarrd.app/template/who-said-something-about-oil-ai-video"),
    ("starrd.json", "cars", "https://www.getstarrd.app/template/cars"),  # suspected category
    ("starrd.json", "holidays", "https://www.getstarrd.app/template/holidays"),
    # SameVid
    ("samevid.json", "the-last-dance-ai", "https://samevid.com/template/the-last-dance-ai"),
    ("samevid.json", "last-dance-ai", "https://samevid.com/template/last-dance-ai"),
    ("samevid.json", "ai-legacy-story", "https://samevid.com/template/ai-legacy-story"),
    ("samevid.json", "dance", "https://samevid.com/template/dance"),  # suspected category
    # Memelry borderline
    ("memelry.json", "ai-mermaid-filter", "https://memelry.com/ai-mermaid-filter"),
    ("memelry.json", "saree-pose-ai", "https://memelry.com/saree-pose-ai"),
    ("memelry.json", "wizard-cat-keyboard-ai", "https://memelry.com/wizard-cat-keyboard-ai"),
    ("memelry.json", "la-la-land-couple-ai", "https://memelry.com/la-la-land-couple-ai"),
    ("memelry.json", "im-flying-titanic-meme", "https://memelry.com/im-flying-titanic-meme"),
    # RapVideo borderline
    ("rapvideo.json", "earth-zoom-out", "https://rapvideo.ai/earth-zoom-out"),
    ("rapvideo.json", "ai-hug-deceased-loved-one", "https://rapvideo.ai/ai-hug-deceased-loved-one"),
    # Summrs keep-alive + one tool sample
    ("summrs.json", "bigfoot-vlog", "https://www.summrs.com/bigfoot-vlog"),
    ("summrs.json", "ai-basketball-meme-generator", "https://www.summrs.com/ai-basketball-meme-generator"),
    ("summrs.json", "ai-kissing-generator", "https://www.summrs.com/ai-kissing-generator"),
]

def fetch(url, timeout=25):
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urlopen(req, context=CTX, timeout=timeout) as resp:
            return getattr(resp, "status", 200), resp.geturl(), resp.read(), None
    except HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        return e.code, url, body, str(e)
    except Exception as e:
        return None, url, b"", f"{type(e).__name__}: {e}"

def m1(text, pat):
    m = re.search(pat, text, re.I | re.S)
    if not m:
        return ""
    s = unescape(re.sub(r"\s+", " ", m.group(1)))
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()

def extract(html):
    title = m1(html, r"<title[^>]*>(.*?)</title>")
    h1 = m1(html, r"<h1[^>]*>(.*?)</h1>")
    og = m1(html, r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']') or m1(html, r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']')
    desc = m1(html, r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']') or m1(html, r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:description["\']')
    if not desc:
        desc = m1(html, r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']')
    low = html.lower()
    looks_404 = any(x in title.lower() for x in ["not found", "404", "page not found", "doesn't exist"]) or "not found" in h1.lower()
    looks_category = bool(re.search(r'(all templates|browse templates|category|filter by|template collection|explore templates)', low))
    return {"title": title, "h1": h1, "og": og, "desc": desc[:400], "len": len(html), "looks_404": looks_404, "looks_category": looks_category}

rows = []
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {}
    for fn, slug, url in candidates:
        futs[ex.submit(fetch, url)] = (fn, slug, url)
    for fut in as_completed(futs):
        fn, slug, url = futs[fut]
        status, final, body, err = fut.result()
        html = body.decode("utf-8", "replace") if body else ""
        meta = extract(html) if html else {"title":"", "h1":"", "og":"", "desc":"", "len":0, "looks_404": True, "looks_category": False}
        row = {"file": fn, "id_or_slug": slug, "url": url, "status": status, "final": final, "error": err, **meta}
        rows.append(row)
        flag = "OK" if status == 200 and not meta["looks_404"] else "BAD"
        print(f"[{flag}] {fn} {slug} status={status} 404={meta['looks_404']} cat={meta['looks_category']}")
        print(f"    h1={meta['h1'][:120]!r}")
        print(f"    og={meta['og'][:120]!r}")
        print(f"    desc={meta['desc'][:240]!r}")

rows.sort(key=lambda r: (r["file"], r["id_or_slug"]))
json.dump(rows, open(os.path.join(OUTDIR, "url_checks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote url_checks.json", len(rows))
