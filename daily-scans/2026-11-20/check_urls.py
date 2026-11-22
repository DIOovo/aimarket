#!/usr/bin/env python3
import json, os, re, ssl, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from html import unescape

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-20"
YEST_FILT = "/workspace/competitor-scan-2026-11-19/filtered_out.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
CTX = ssl.create_default_context()

diff = json.load(open(os.path.join(OUTDIR, "diff_raw.json")))
yest = {}
for x in json.load(open(YEST_FILT)):
    yest.setdefault(x["file"], set()).add(x["item"]["id_or_slug"].lower())

FILE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
            ".css", ".js", ".xml", ".txt", ".json", ".webmanifest", ".map")

candidates = []
for fn, d in diff.items():
    for t in d["new"]:
        slug = t["id_or_slug"].lower()
        if slug in yest.get(fn, set()):
            continue
        path = t.get("url") or ""
        if fn == "ricebowl.json":
            continue
        if any(slug.endswith(ext) or path.lower().endswith(ext) for ext in FILE_EXT):
            continue
        candidates.append({
            "site": d["site"], "file": fn,
            "id_or_slug": t["id_or_slug"], "title": t.get("title") or t["id_or_slug"],
            "url": t["url"], "kind": "candidate",
        })

keep_checks = [
    {"site":"Summrs","file":"summrs.json","id_or_slug":"bigfoot-vlog","title":"Bigfoot Vlog",
     "url":"https://www.summrs.com/bigfoot-vlog","kind":"keep_missing"},
    {"site":"Try a Trend","file":"tryatrend.json","id_or_slug":"ai-halloween-costume","title":"AI Halloween Costume",
     "url":"https://tryatrend.com/ai-halloween-costume","kind":"keep_missing"},
]
# Starrd items missing from today's sitemap — check if still 200
import json as _json
_diff=_json.load(open("/workspace/competitor-scan-2026-11-20/diff_raw.json"))
for t in _diff.get("starrd.json",{}).get("missing") or []:
    keep_checks.append({
        "site":"Starrd","file":"starrd.json",
        "id_or_slug": t["id_or_slug"], "title": t.get("title") or t["id_or_slug"],
        "url": t["url"], "kind":"starrd_missing",
    })


print("candidates", len(candidates), "keep", len(keep_checks))
from collections import Counter
print(Counter(c["site"] for c in candidates))

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

def extract_meta(html):
    def m1(pat):
        m = re.search(pat, html, re.I | re.S)
        if not m:
            return ""
        t = unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
        return re.sub(r"\s+", " ", t).strip()
    title = m1(r"<title[^>]*>(.*?)</title>")
    h1 = m1(r"<h1[^>]*>(.*?)</h1>")
    og = (m1(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']')
          or m1(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']'))
    desc = (m1(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']')
            or m1(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:description["\']'))
    if not desc:
        desc = (m1(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']')
                or m1(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']'))
    low = (title + " " + h1).lower()
    looks_404 = any(x in low for x in ("404", "not found", "page not found", "doesn't exist", "does not exist"))
    return {"title_page": title, "h1": h1, "og": og, "desc": desc, "len": len(html), "looks_404": looks_404}

def check_one(item):
    t0 = time.time()
    status, final, raw, err = fetch(item["url"])
    try:
        html = raw.decode("utf-8", errors="replace") if raw else ""
    except Exception:
        html = ""
    meta = extract_meta(html) if html else {"title_page":"","h1":"","og":"","desc":"","len":0,"looks_404":False}
    return {**item, "status": status, "final": final, "error": err,
            "ms": int((time.time()-t0)*1000), **meta}

all_items = candidates + keep_checks
results = []
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(check_one, it) for it in all_items]
    for i, fut in enumerate(as_completed(futs), 1):
        rec = fut.result()
        results.append(rec)
        flag = "OK" if rec["status"]==200 and not rec.get("looks_404") else "BAD"
        print(f"[{i}/{len(all_items)}] {flag} {rec['status']} {rec['site']} {rec['id_or_slug']} | {(rec.get('title_page') or rec.get('h1') or '')[:90]}")

order = {(c["site"], c["id_or_slug"]): i for i,c in enumerate(all_items)}
results.sort(key=lambda r: order.get((r["site"], r["id_or_slug"]), 9999))
json.dump(results, open(os.path.join(OUTDIR,"url_checks.json"),"w"), ensure_ascii=False, indent=2)
print("wrote url_checks.json", len(results))
bad=[r for r in results if r["status"]!=200 or r.get("looks_404")]
print("BAD count", len(bad))
for r in bad:
    print(" BAD", r["status"], r["site"], r["url"], r.get("error"), r.get("title_page"))
