#!/usr/bin/env python3
"""FaceOnTrend competitor sitemap daily scan — 2026-11-21."""
from __future__ import annotations

import gzip
import json
import os
import re
import ssl
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-21"
RAW = os.path.join(OUTDIR, "raw")
CHECKED_AT = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)
CTX = ssl.create_default_context()

LANG_PREFIXES = {
    "zh", "zh-cn", "zh-tw", "zh-hk", "cn", "tw", "hk",
    "de", "de-de", "es", "es-es", "es-mx", "es-la",
    "ar", "ar-sa", "ar-ae", "fr", "fr-fr", "fr-ca",
    "ja", "ja-jp", "ko", "ko-kr", "pt", "pt-br", "pt-pt",
    "it", "it-it", "ru", "ru-ru", "tr", "tr-tr",
    "vi", "vi-vn", "id", "id-id", "th", "th-th",
    "nl", "nl-nl", "pl", "pl-pl", "uk", "uk-ua",
    "ms", "fil", "hi", "bn", "sv", "da", "no", "fi",
    "cs", "ro", "hu", "el", "he", "fa",
    "en-gb", "en-au", "en-ca", "en-in", "en-us",
}

GENERIC_BLOCK_SLUGS = {
    "pricing", "price", "plans", "plan", "about", "about-us", "aboutus",
    "terms", "terms-of-service", "termsofservice", "tos", "legal",
    "privacy", "privacy-policy", "privacypolicy", "cookie", "cookies",
    "cookie-policy", "dmca", "contact", "contact-us", "contactus",
    "blog", "blogs", "news", "login", "signin", "sign-in", "signup",
    "sign-up", "register", "auth", "api", "admin", "dashboard",
    "account", "settings", "checkout", "cart", "billing", "subscription",
    "affiliate", "partners", "careers", "press", "support", "help",
    "help-center", "faq", "docs", "documentation", "changelog",
    "whats-new", "what's-new", "studio", "refund", "refunds",
    "sitemap", "robots", "favicon", "favicon.svg", "icon", "icon.svg",
    "media", "refs", "gift", "guides", "guide", "result", "results",
    "login-page", "why-us", "features", "enterprise", "partners",
    "affiliate-program", "disclaimer", "impressum", "license",
}

GENERIC_BLOCK_PREFIXES = {
    "blog", "blogs", "news", "auth", "api", "admin", "account",
    "dashboard", "settings", "docs", "help", "legal", "careers",
}

# Site-specific extra blocked slugs (last path segment or exact)
EXTRA_BLOCK = {
    "makememe.json": {"halloween-ai-video-trends"},
    "memefxai.json": {"studio", "whats-new"},
    "trendswap.json": {"help-center"},
    "summrs.json": {"favicon.svg", "icon.svg"},
    "ricebowl.json": {
        "ai-asmr-video-generator", "ai-lip-sync", "animate-illustrations",
        "minecraft-parkour-video-generator", "sketch-to-video-ai",
        "video-to-cartoon-converter",
    },
}

# Non-template tool pages often appearing on these sites
AIMAKE_BLOCK = {
    "pricing", "privacy", "terms", "blog", "text-to-video", "image-to-video",
    "ai-tools", "ai-models", "about", "contact", "login", "signup",
    "templates", "tools",
}
TRYATREND_BLOCK = {
    "about", "pricing", "gift", "guides", "christmas", "result", "results",
    "privacy", "terms", "contact", "login", "signup", "blog",
}
MEMELRY_BLOCK = {
    "cookies", "pricing", "auth", "api", "admin", "media", "refs",
    "templates", "login", "signup", "privacy", "terms", "contact", "blog",
}
RAPVIDEO_BLOCK = {
    "pricing", "privacy", "terms", "contact", "about", "blog", "login", "signup",
}
AITREND_BLOCK = {"custom-video-template", "custom-video", "pricing", "privacy", "terms", "about", "contact"}


@dataclass
class SiteSpec:
    site: str
    file: str
    home: str
    # How to accept a URL path (after host, no query). Return slug or None.
    # Implemented via kind + extras.
    kind: str
    extra_sitemaps: list[str] = field(default_factory=list)
    list_pages: list[str] = field(default_factory=list)


SITES: list[SiteSpec] = [
    SiteSpec("DoTheTrend", "dothetrend.json", "https://dothetrend.ai/", "templates",
             list_pages=["https://dothetrend.ai/templates"]),
    SiteSpec("TrendTemplate", "trendtemplate.json", "https://trendtemplate.com/", "root_ai",
             list_pages=["https://trendtemplate.com/"]),
    SiteSpec("MemeFX AI", "memefxai.json", "https://memefxai.com/", "memefxai",
             list_pages=["https://memefxai.com/", "https://memefxai.com/zh/templates"]),
    SiteSpec("ClipRemake", "clipremake.json", "https://clipremake.com/", "templates",
             list_pages=["https://clipremake.com/templates", "https://clipremake.com/"]),
    SiteSpec("Remake Your Meme", "remakeyourmeme.json", "https://remakeyourmeme.com/", "templates",
             list_pages=["https://remakeyourmeme.com/templates", "https://remakeyourmeme.com/"]),
    SiteSpec("MakeViral", "makeviral.json", "https://www.makeviral.ai/", "templates",
             list_pages=["https://www.makeviral.ai/templates"]),
    SiteSpec("Smew AI", "smew.json", "https://smew.ai/", "templates",
             list_pages=["https://smew.ai/templates"]),
    SiteSpec("MakeMeme.video", "makememe.json", "https://makememe.video/", "makememe",
             extra_sitemaps=["https://makememe.video/sitemap.xml"],
             list_pages=["https://makememe.video/", "https://makememe.video/trends"]),
    SiteSpec("ViralRemake", "viralremake.json", "https://viralremake.com/", "templates",
             list_pages=["https://viralremake.com/templates"]),
    SiteSpec("MemeClone.ai", "memeclone.json", "https://memeclone.ai/", "templates",
             list_pages=["https://memeclone.ai/templates"]),
    SiteSpec("TrendSwap", "trendswap.json", "https://trendswap.app/", "trendswap",
             extra_sitemaps=["https://trendswap.app/video-sitemap.xml", "https://trendswap.app/image-sitemap.xml"],
             list_pages=["https://trendswap.app/templates", "https://trendswap.app/"]),
    SiteSpec("Put Me In", "putmein.json", "https://putmein.app/", "templates",
             extra_sitemaps=["https://putmein.app/sitemap-media.xml"],
             list_pages=["https://putmein.app/templates"]),
    SiteSpec("SameVid AI", "samevid.json", "https://samevid.com/", "samevid",
             list_pages=["https://samevid.com/templates"]),
    SiteSpec("ZapVid", "zapvid.json", "https://zapvid.ai/", "zapvid",
             list_pages=["https://zapvid.ai/"]),
    SiteSpec("Summrs", "summrs.json", "https://www.summrs.com/", "summrs",
             list_pages=["https://www.summrs.com/"]),
    SiteSpec("Trendify Video", "trendify.json", "https://trendify.video/", "trends",
             list_pages=["https://trendify.video/trends"]),
    SiteSpec("Genjutsu AI", "genjutsu.json", "https://genjutsuai.cc/", "genjutsu",
             list_pages=["https://genjutsuai.cc/ai-video-trends", "https://genjutsuai.cc/"]),
    SiteSpec("DanceRemake", "danceremake.json", "https://danceremake.com/", "templates",
             list_pages=["https://danceremake.com/templates"]),
    SiteSpec("Starrd", "starrd.json", "https://www.getstarrd.app/", "starrd",
             list_pages=["https://www.getstarrd.app/templates/viral"]),
    SiteSpec("AI Trend Video", "aitrendvideo.json", "https://aitrendvideo.net/", "aitrendvideo",
             list_pages=["https://aitrendvideo.net/"]),
    SiteSpec("Ricebowl AI", "ricebowl.json", "https://ricebowl.ai/", "ricebowl",
             extra_sitemaps=["https://ricebowl.ai/sitemap-pages.xml", "https://ricebowl.ai/sitemap-models.xml", "https://ricebowl.ai/sitemap-hub.xml"],
             list_pages=["https://ricebowl.ai/trends/meme"]),
    SiteSpec("Kubflow", "kubflow.json", "https://kubflow.ai/", "kubflow",
             list_pages=["https://kubflow.ai/trends"]),
    SiteSpec("PictureToVideo", "picturetovideo.json", "https://picturetovideo.org/", "picturetovideo",
             list_pages=["https://picturetovideo.org/ai-video-effects"]),
    SiteSpec("Bolly.AI", "bolly.json", "https://www.bolly.ai/", "bolly",
             list_pages=["https://www.bolly.ai/templates/dance"]),
    SiteSpec("RapVideo.ai", "rapvideo.json", "https://rapvideo.ai/", "rapvideo",
             list_pages=["https://rapvideo.ai/"]),
    SiteSpec("aiMakeVideo", "aimakevideo.json", "https://aimakevideo.com/", "aimakevideo",
             extra_sitemaps=["https://aimakevideo.com/sitemap.xml"],
             list_pages=["https://aimakevideo.com/templates", "https://aimakevideo.com/"]),
    SiteSpec("Try a Trend", "tryatrend.json", "https://tryatrend.com/", "tryatrend",
             extra_sitemaps=["https://tryatrend.com/sitemap.xml"],
             list_pages=["https://tryatrend.com/"]),
    SiteSpec("Memelry", "memelry.json", "https://memelry.com/", "memelry",
             extra_sitemaps=["https://memelry.com/sitemap.xml"],
             list_pages=["https://memelry.com/templates", "https://memelry.com/"]),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def http_get(url: str, timeout: int = 25, tries: int = 3) -> tuple[int, bytes, str]:
    """Return (status, body, final_url). status 0 on network error."""
    last_err = ""
    for i in range(tries):
        try:
            req = Request(url, headers={
                "User-Agent": UA,
                "Accept": "application/xml,text/xml,text/html,application/xhtml+xml,application/json,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
            })
            with urlopen(req, context=CTX, timeout=timeout) as resp:
                data = resp.read()
                enc = (resp.headers.get("Content-Encoding") or "").lower()
                if enc == "gzip" or url.endswith(".gz") or data[:2] == b"\x1f\x8b":
                    try:
                        data = gzip.decompress(data)
                    except Exception:
                        pass
                final = resp.geturl() or url
                return resp.status, data, final
        except HTTPError as e:
            body = b""
            try:
                body = e.read() or b""
            except Exception:
                pass
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(1.5 * (i + 1))
                continue
            return e.code, body, url
        except Exception as e:
            last_err = str(e)
            if i < tries - 1:
                time.sleep(1.2 * (i + 1))
                continue
            return 0, last_err.encode("utf-8", "replace"), url
    return 0, last_err.encode("utf-8", "replace"), url


def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def parse_sitemap_locs(xml_bytes: bytes) -> tuple[list[str], list[str]]:
    """Return (page_locs, child_sitemap_locs)."""
    pages, children = [], []
    if not xml_bytes or not xml_bytes.strip():
        return pages, children
    text = xml_bytes
    # Some sitemaps have leading BOM or junk
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        # try to extract loc tags with regex
        raw = text.decode("utf-8", "replace")
        locs = re.findall(r"<loc[^>]*>\s*([^<\s]+)\s*</loc>", raw, flags=re.I)
        for loc in locs:
            loc = loc.strip()
            if "sitemap" in loc.lower() and loc.lower().endswith((".xml", ".xml.gz")):
                children.append(loc)
            else:
                pages.append(loc)
        return pages, children
    kind = strip_ns(root.tag).lower()
    for el in root.iter():
        if strip_ns(el.tag).lower() != "loc" or el.text is None:
            continue
        loc = el.text.strip()
        if not loc:
            continue
        parent = strip_ns(el.getparent().tag).lower() if hasattr(el, "getparent") and el.getparent() is not None else ""
        # ElementTree doesn't have getparent unless using lxml. Infer from ancestor by walking...
        # Instead: if this loc is inside a sitemapindex <sitemap>, it's a child.
        # We'll classify after: if current root is sitemapindex, all locs are children.
        if kind == "sitemapindex":
            children.append(loc)
        else:
            pages.append(loc)
    return pages, children


def discover_sitemaps(home: str, extra: list[str]) -> list[str]:
    found: list[str] = []
    seen = set()
    base = home.rstrip("/") + "/"
    candidates = [
        urljoin(base, "sitemap.xml"),
        urljoin(base, "sitemap_index.xml"),
        urljoin(base, "sitemap-index.xml"),
        urljoin(base, "sitemapindex.xml"),
        urljoin(base, "sitemap.xml.gz"),
    ] + list(extra)
    # robots.txt
    robots_url = urljoin(base, "robots.txt")
    status, body, _ = http_get(robots_url, timeout=15, tries=2)
    robots_sitemaps = []
    if status == 200 and body:
        for line in body.decode("utf-8", "replace").splitlines():
            if line.lower().startswith("sitemap:"):
                sm = line.split(":", 1)[1].strip()
                if sm:
                    robots_sitemaps.append(sm)
                    if sm not in candidates:
                        candidates.append(sm)

    def add(u: str) -> None:
        u = u.strip()
        if u and u not in seen:
            seen.add(u)
            found.append(u)

    # probe candidates; follow indexes
    queue = list(candidates)
    probed = set()
    while queue:
        url = queue.pop(0)
        if url in probed:
            continue
        probed.add(url)
        status, body, final = http_get(url, timeout=25, tries=2)
        if status != 200 or not body:
            continue
        # only treat as sitemap if it looks like xml
        head = body.lstrip()[:200].lower()
        if b"<urlset" in head or b"<sitemapindex" in head or b"<?xml" in head or b"<url>" in body[:2000].lower() or b"<loc>" in body[:4000].lower():
            add(final if final.endswith(".xml") or "sitemap" in final.lower() else url)
            pages, children = parse_sitemap_locs(body)
            # save raw
            safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", urlparse(url).netloc + urlparse(url).path)
            try:
                with open(os.path.join(RAW, safe[:180]), "wb") as f:
                    f.write(body)
            except Exception:
                pass
            for c in children:
                if c not in probed:
                    queue.append(c)
        # else ignore HTML homepage accidentally hit
    return found


def normalize_url(u: str) -> str:
    p = urlparse(u.strip())
    # drop query/fragment, keep trailing slash as-is for remakeyourmeme
    path = p.path or "/"
    return urlunparse((p.scheme or "https", p.netloc.lower(), path, "", "", ""))


def path_parts(path: str) -> list[str]:
    return [x for x in path.split("/") if x]


def is_lang_prefix(seg: str) -> bool:
    return seg.lower() in LANG_PREFIXES


def title_from_slug(slug: str) -> str:
    words = slug.replace("_", "-").split("-")
    out = []
    for w in words:
        if not w:
            continue
        low = w.lower()
        if low in {"ai", "uk", "us", "tv", "id", "nr", "ps", "dj", "mc", "rnb"}:
            out.append(low.upper() if low != "rnb" else "RnB")
        elif low == "vs":
            out.append("Vs")
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def slug_of(url: str) -> str:
    parts = path_parts(urlparse(url).path)
    return parts[-1] if parts else ""


# ---------- accept rules ----------

def blocked_generic(parts: list[str], file: str) -> bool:
    if not parts:
        return True
    # language mirror: if first segment is a lang code and there's more, skip (except we may strip and re-check in caller)
    low = [p.lower() for p in parts]
    if any(p in GENERIC_BLOCK_SLUGS for p in low):
        return True
    if low[0] in GENERIC_BLOCK_PREFIXES:
        return True
    extra = EXTRA_BLOCK.get(file, set())
    if low[-1] in extra or any(p in extra for p in low):
        return True
    # *-ai-tools helper pages
    if low[-1].endswith("-ai-tools") or "ai-tools" in low:
        return True
    return False


def maybe_strip_lang(parts: list[str]) -> list[str] | None:
    """If first segment is a language prefix, return remaining parts (to dedupe, we usually DROP mirrors).
    Return None to signal 'this is a language mirror — skip entirely'."""
    if parts and is_lang_prefix(parts[0]):
        return None  # skip mirrors; count main language only
    return parts


def accept(spec: SiteSpec, url: str) -> str | None:
    """Return canonical template URL or None."""
    u = normalize_url(url)
    p = urlparse(u)
    home = urlparse(spec.home)
    # host must match (allow with/without www for same registrable? keep exact home host mostly,
    # but accept www <-> apex if home uses one of them)
    host = p.netloc.lower()
    home_host = home.netloc.lower()
    if host != home_host:
        # allow www variant
        if host.removeprefix("www.") != home_host.removeprefix("www."):
            return None
        # canonicalize to home host
        u = urlunparse((home.scheme, home_host, p.path, "", "", ""))
        p = urlparse(u)
    path = p.path
    parts = path_parts(path)
    parts_or = maybe_strip_lang(parts)
    if parts_or is None:
        return None
    parts = parts_or
    if blocked_generic(parts, spec.file):
        return None
    kind = spec.kind
    low = [x.lower() for x in parts]

    def canon(parts2: list[str], slash: bool = False) -> str:
        path2 = "/" + "/".join(parts2)
        if slash:
            path2 += "/"
        return urlunparse((home.scheme, home.netloc.lower(), path2, "", "", ""))

    if kind == "templates":
        # /templates/{slug}  (remakeyourmeme often has trailing slash)
        if len(parts) == 2 and low[0] == "templates":
            slug = parts[1]
            if slug.lower() in GENERIC_BLOCK_SLUGS:
                return None
            trailing = path.endswith("/")
            return canon(parts, slash=trailing or spec.file == "remakeyourmeme.json")
        return None

    if kind == "trends":
        if len(parts) == 2 and low[0] == "trends":
            if parts[1].lower() in GENERIC_BLOCK_SLUGS:
                return None
            return canon(parts)
        return None

    if kind == "samevid":
        # /template/{slug} (singular). Directory /templates is not a template.
        if len(parts) == 2 and low[0] in {"template", "templates"}:
            if low[0] == "templates":
                # list page or maybe they use plural for items? baseline uses /template/
                # if slug looks like a template, canonicalize to /template/
                pass
            slug = parts[1]
            if slug.lower() in GENERIC_BLOCK_SLUGS:
                return None
            return canon(["template", slug])
        return None

    if kind == "starrd":
        # inventory is /template/{slug}; listing may be /templates/viral
        if len(parts) == 2 and low[0] in {"template", "templates"}:
            if low[1] in {"viral", "dance", "all", "meme", "trending", "new", "popular", "category"}:
                return None
            return canon(["template", parts[1]])
        if len(parts) == 3 and low[0] == "templates":
            # /templates/viral/{slug}? treat as template if not a category-only page
            if low[2] not in GENERIC_BLOCK_SLUGS:
                return canon(["template", parts[2]])
        return None

    if kind == "bolly":
        # /template/{slug}
        if len(parts) == 2 and low[0] in {"template", "templates"}:
            if low[1] in {"dance", "all", "viral", "category"}:
                return None
            return canon(["template", parts[1]])
        return None

    if kind == "kubflow":
        if len(parts) == 2 and low[0] == "trends":
            slug = parts[1]
            if slug.lower() in GENERIC_BLOCK_SLUGS or slug.lower() in {"custom", "custom-trend", "new", "create"}:
                return None
            return canon(parts)
        return None

    if kind == "ricebowl":
        # inventory is /app/{slug}; exclude generic tool pages (already in EXTRA_BLOCK)
        if len(parts) == 2 and low[0] == "app":
            return canon(parts)
        return None

    if kind == "makememe":
        # root /slug (templates), exclude /ar/ already handled; also exclude /trends as a hub? individual maybe /trends/slug?
        # baseline is all root slugs. /trends directory page itself is not a template.
        if len(parts) == 1:
            slug = low[0]
            if slug in {"trends", "pricing", "about", "terms", "privacy", "dmca", "blog", "login"}:
                return None
            return canon(parts)
        return None

    if kind == "memefxai":
        # English root slugs; /zh/templates skipped via lang. Sometimes /templates/{slug}?
        if len(parts) == 1:
            return canon(parts)
        if len(parts) == 2 and low[0] == "templates":
            # canonicalize? baseline uses root slugs. Prefer root form.
            return canon([parts[1]])
        return None

    if kind == "trendswap":
        # baseline: root /{slug}. Directory /templates is a list page.
        if len(parts) == 1:
            if low[0] in {"templates", "blog", "help-center"}:
                return None
            return canon(parts)
        if len(parts) == 2 and low[0] == "templates":
            # if list items live under /templates/{slug}, canonicalize to root to match baseline? 
            # baseline is root. If we find /templates/foo and /foo, dedupe to /foo.
            return canon([parts[1]])
        return None

    if kind == "zapvid":
        if len(parts) == 1 and low[0].endswith("-ai-video-generator"):
            return canon(parts)
        return None

    if kind == "summrs":
        if len(parts) == 1:
            slug = low[0]
            # mostly *-ai-video-generator, some *-ai and others already in baseline
            if slug in {"templates", "blog", "explore", "create"}:
                return None
            # skip obvious SEO assets
            if slug.endswith((".svg", ".png", ".jpg", ".css", ".js", ".ico", ".xml", ".txt")):
                return None
            # accept *-ai-video-generator always; also keep other existing-style meme landing pages
            # but don't ingest random marketing pages. We'll also intersect with existing later if count explodes.
            if slug.endswith("-ai-video-generator") or slug.endswith("-ai") or slug.endswith("-ai-trend"):
                return canon(parts)
            # allow other one-seg only if it looks like a meme landing (contains ai or video or trend or filter)
            if any(tok in slug for tok in ("ai", "video", "trend", "filter", "meme")):
                return canon(parts)
        return None

    if kind == "genjutsu":
        # root slugs; skip aggregation /ai-video-trends
        if len(parts) == 1:
            if low[0] in {"ai-video-trends", "trends", "templates", "blog"}:
                return None
            return canon(parts)
        return None

    if kind == "picturetovideo":
        # root effect pages; skip the hub /ai-video-effects itself
        if len(parts) == 1:
            if low[0] in {"ai-video-effects", "effects", "pricing", "about"}:
                return None
            return canon(parts)
        return None

    if kind == "aitrendvideo":
        if len(parts) == 1:
            if low[0] in AITREND_BLOCK or low[0] in {"templates", "trends", "blog"}:
                return None
            return canon(parts)
        return None

    if kind == "root_ai":
        # TrendTemplate: root /*-ai
        if len(parts) == 1:
            if low[0] in {"templates", "pricing", "about", "blog"}:
                return None
            return canon(parts)
        return None

    if kind == "aimakevideo":
        if len(parts) == 1:
            slug = low[0]
            if slug in AIMAKE_BLOCK:
                return None
            # templates are /*-ai
            if slug.endswith("-ai"):
                return canon(parts)
        return None

    if kind == "tryatrend":
        if len(parts) == 1:
            slug = low[0]
            if slug in TRYATREND_BLOCK:
                return None
            # /*-ai or /*-ai-trend or occasional others already in baseline
            if slug.endswith("-ai") or slug.endswith("-ai-trend") or slug.endswith("-trend"):
                return canon(parts)
            # don't ingest random pages
        return None

    if kind == "memelry":
        if len(parts) == 1:
            slug = low[0]
            if slug in MEMELRY_BLOCK:
                return None
            if slug.endswith("-ai-tools"):
                return None
            # SEO long-form landing pages: typically very long slugs with many words
            # Keep same style as baseline: mostly *-ai, plus a few others already listed.
            # Accept *-ai, *-trend, and ai-* short meme slugs. Reject very long SEO articles.
            tokens = slug.split("-")
            if len(tokens) >= 10:
                return None  # likely SEO article
            if slug.endswith("-ai") or slug.endswith("-trend") or slug.endswith("-ai-dance") or slug.endswith("-ai-video") or slug.endswith("-ai-trend"):
                return canon(parts)
            if slug.startswith("ai-") and len(tokens) <= 6:
                return canon(parts)
            # short distinctive slugs like michael-carrick-window-scene, hotel-lobby
            if len(tokens) <= 5 and slug not in {"index", "home", "explore", "create", "generate", "upload"}:
                # only if looks meme-like or we'll rely on existing set later
                return canon(parts)
        return None

    if kind == "rapvideo":
        if len(parts) == 1:
            slug = low[0]
            if slug in RAPVIDEO_BLOCK:
                return None
            if slug in {"templates", "blog", "tools", "login", "signup"}:
                return None
            return canon(parts)
        # maybe /tools/foo trend landing? instruction says 抓 sitemap 与工具/趋势落地页
        if len(parts) == 2 and low[0] in {"tools", "trends", "templates"}:
            if low[1] not in RAPVIDEO_BLOCK and low[1] not in GENERIC_BLOCK_SLUGS:
                # canonicalize to root if possible? baseline is all root. Keep path as-is only if not already root style.
                # Prefer root to match baseline: /tools/foo -> skip if we also have /foo; if only /tools/foo, keep it
                return canon(parts)
        return None

    return None


HREF_RE = re.compile(r"""(?:href|loc)\s*=\s*["']([^"']+)["']""", re.I)
ABS_RE = re.compile(r"""https?://[^\s"'<>]+""", re.I)


def extract_hrefs(html: bytes, base: str) -> list[str]:
    try:
        text = html.decode("utf-8", "replace")
    except Exception:
        text = html.decode("latin-1", "replace")
    urls = []
    for m in HREF_RE.findall(text):
        urls.append(urljoin(base, m.split("#")[0]))
    # also next-data or json blobs with paths
    for m in re.findall(r"""["'](/[a-zA-Z0-9\-/_]+)["']""", text):
        urls.append(urljoin(base, m))
    return urls


def load_prev(file: str) -> dict:
    path = os.path.join(STORE, file)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def url_key(u: str) -> str:
    p = urlparse(u)
    path = p.path.rstrip("/") or "/"
    return (p.netloc.lower().removeprefix("www.") + path).lower()


def fetch_site(spec: SiteSpec) -> dict:
    notes = []
    sitemap_urls = []
    try:
        sitemap_urls = discover_sitemaps(spec.home, spec.extra_sitemaps)
    except Exception as e:
        notes.append(f"sitemap discover error: {e}")
    loc_urls: list[str] = []
    for sm in sitemap_urls:
        # re-read raw if saved, else fetch
        status, body, _ = http_get(sm, timeout=30, tries=2)
        if status != 200 or not body:
            notes.append(f"sitemap fetch fail {sm} status={status}")
            continue
        pages, children = parse_sitemap_locs(body)
        loc_urls.extend(pages)
        # children should already have been pulled into sitemap_urls, but parse their pages if missed
        for c in children:
            if c not in sitemap_urls:
                st, bd, _ = http_get(c, timeout=30, tries=2)
                if st == 200 and bd:
                    sitemap_urls.append(c)
                    p2, _ = parse_sitemap_locs(bd)
                    loc_urls.extend(p2)

    # list pages as supplement (and title source)
    list_htmls: dict[str, bytes] = {}
    for lp in spec.list_pages:
        st, bd, _ = http_get(lp, timeout=25, tries=2)
        if st == 200 and bd:
            list_htmls[lp] = bd
            loc_urls.extend(extract_hrefs(bd, lp))
        else:
            notes.append(f"list page {lp} status={st}")

    accepted: dict[str, str] = {}  # url_key -> canonical url
    for u in loc_urls:
        try:
            cu = accept(spec, u)
        except Exception:
            cu = None
        if cu:
            accepted[url_key(cu)] = cu

    prev = load_prev(spec.file)
    prev_by_key = {url_key(t["url"]): t for t in prev.get("templates", [])}
    prev_by_slug = {}
    for t in prev.get("templates", []):
        prev_by_slug.setdefault(t.get("id_or_slug", "").lower(), t)

    templates = []
    for key, cu in sorted(accepted.items(), key=lambda kv: kv[1]):
        slug = slug_of(cu)
        # keep previous title if same url or same slug
        title = None
        if key in prev_by_key:
            title = prev_by_key[key].get("title")
        elif slug.lower() in prev_by_slug:
            title = prev_by_slug[slug.lower()].get("title")
        if not title:
            title = title_from_slug(slug)
        templates.append({"id_or_slug": slug, "title": title, "url": cu})

    # Safety: if inventory collapsed, don't treat as mass removal — keep prev and flag
    prev_count = len(prev.get("templates", []))
    new_count_est = len(templates)
    fetch_ok = True
    if prev_count >= 8 and new_count_est < max(3, int(prev_count * 0.5)):
        fetch_ok = False
        notes.append(f"INCOMPLETE FETCH: got {new_count_est} vs previous {prev_count}; snapshot not replaced")

    return {
        "spec": spec,
        "sitemap_urls_found": sitemap_urls,
        "sitemap_existed": bool(sitemap_urls),
        "templates": templates,
        "fetch_ok": fetch_ok,
        "notes": notes,
        "prev": prev,
        "list_htmls_ok": list(list_htmls.keys()),
    }


def main_fetch():
    results = {}
    # parallel but not too aggressive
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_site, spec): spec for spec in SITES}
        for fut in as_completed(futs):
            spec = futs[fut]
            try:
                res = fut.result()
            except Exception as e:
                log(f"FAIL {spec.site}: {e}\n{traceback.format_exc()}")
                res = {
                    "spec": spec,
                    "sitemap_urls_found": [],
                    "sitemap_existed": False,
                    "templates": [],
                    "fetch_ok": False,
                    "notes": [f"exception: {e}"],
                    "prev": load_prev(spec.file),
                    "list_htmls_ok": [],
                }
            results[spec.file] = res
            n = len(res["templates"])
            prev_n = len(res["prev"].get("templates", []))
            flag = "OK" if res["fetch_ok"] else "WARN"
            log(f"[{flag}] {spec.site}: {n} templates (prev {prev_n}) sitemaps={len(res['sitemap_urls_found'])} notes={res['notes']}")
    with open(os.path.join(OUTDIR, "fetch_results.json"), "w", encoding="utf-8") as f:
        dump = {}
        for k, v in results.items():
            dump[k] = {
                "site": v["spec"].site,
                "sitemap_urls_found": v["sitemap_urls_found"],
                "sitemap_existed": v["sitemap_existed"],
                "template_count": len(v["templates"]),
                "fetch_ok": v["fetch_ok"],
                "notes": v["notes"],
                "list_htmls_ok": v["list_htmls_ok"],
                "templates": v["templates"],
            }
        json.dump(dump, f, ensure_ascii=False, indent=2)
    log("Wrote fetch_results.json")
    return results


if __name__ == "__main__":
    main_fetch()
