
import json, os, re, ssl, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
from html import unescape

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-20"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)
CTX = ssl.create_default_context()

def fetch(url, timeout=25):
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urlopen(req, context=CTX, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
            final = resp.geturl()
            ctype = resp.headers.get("Content-Type", "")
        return {"ok": True, "status": status, "final": final, "ctype": ctype, "body": raw, "error": None}
    except HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        return {"ok": False, "status": e.code, "final": url, "ctype": "", "body": body, "error": str(e)}
    except Exception as e:
        return {"ok": False, "status": None, "final": url, "ctype": "", "body": b"", "error": f"{type(e).__name__}: {e}"}

def decode(raw):
    if not raw:
        return ""
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc, errors="replace")
        except Exception:
            pass
    return raw.decode("utf-8", errors="replace")

def extract_meta(html):
    text = html
    def m1(pat):
        m = re.search(pat, text, re.I | re.S)
        return unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""
    title = m1(r"<title[^>]*>(.*?)</title>")
    h1 = m1(r"<h1[^>]*>(.*?)</h1>")
    h1 = re.sub(r"<[^>]+>", "", h1)
    og = m1(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']') or m1(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']')
    desc = m1(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']') or m1(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:description["\']')
    if not desc:
        desc = m1(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']') or m1(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']')
    return {"title": title, "h1": h1, "og": og, "desc": desc, "len": len(html)}

# ---- ricebowl catalog ----
print("Fetching ricebowl catalog...")
rb = fetch("https://ricebowl.ai/trends/meme")
rb_html = decode(rb["body"])
print("ricebowl status", rb["status"], "final", rb["final"], "len", len(rb_html), "err", rb["error"])
open(os.path.join(OUTDIR, "raw/ricebowl_trends_meme.html"), "w").write(rb_html)

# parse ItemList JSON-LD and /app/ links
items = []
for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)<\/script>', rb_html, re.I|re.S):
    raw = m.group(1).strip()
    try:
        data = json.loads(raw)
    except Exception:
        continue
    blob = json.dumps(data)
    if "ItemList" in blob or "itemListElement" in blob:
        def walk(o):
            if isinstance(o, dict):
                typ = o.get("@type") or o.get("type")
                if typ == "ItemList" or "itemListElement" in o:
                    for el in o.get("itemListElement") or []:
                        if isinstance(el, dict):
                            item = el.get("item") or el
                            url = ""
                            name = ""
                            if isinstance(item, dict):
                                url = item.get("url") or item.get("@id") or ""
                                name = item.get("name") or item.get("title") or ""
                            elif isinstance(item, str):
                                url = item
                            slug = url.rstrip("/").split("/")[-1] if url else ""
                            if slug:
                                items.append({"id_or_slug": slug, "title": name, "url": url})
                else:
                    for v in o.values():
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)

# also collect unique /app/ links from page
app_links = []
for m in re.finditer(r'https?://ricebowl\.ai/app/([a-z0-9\-]+)', rb_html, re.I):
    slug = m.group(1)
    app_links.append(slug)
for m in re.finditer(r'href=["\'](/app/([a-z0-9\-]+))["\']', rb_html, re.I):
    app_links.append(m.group(2))

print("jsonld items", len(items), "app link mentions", len(set(app_links)))
if items:
    print("jsonld sample", items[:3])
print("unique app slugs from html", len(set(app_links)))
# numberOfItems
m = re.search(r'"numberOfItems"\s*:\s*(\d+)', rb_html)
print("numberOfItems", m.group(1) if m else None)

# prefer jsonld if reasonably sized, else app links
catalog = items
if not catalog:
    # unique preserve order
    seen=set(); catalog=[]
    for slug in app_links:
        if slug not in seen:
            seen.add(slug)
            catalog.append({"id_or_slug": slug, "title": slug, "url": f"https://ricebowl.ai/app/{slug}"})

# dedupe catalog
seen=set(); dedup=[]
for t in catalog:
    s=t["id_or_slug"].lower()
    if s in seen: continue
    seen.add(s)
    # normalize url to /app/
    url=t["url"]
    if "/app/" not in url and t["id_or_slug"]:
        url=f"https://ricebowl.ai/app/{t['id_or_slug']}"
    dedup.append({"id_or_slug": t["id_or_slug"], "title": t["title"] or t["id_or_slug"], "url": url})
catalog=dedup
print("catalog size", len(catalog))

prev_cat=json.load(open("/workspace/competitor-scan-2026-11-19/ricebowl_catalog.json"))
prev_slugs={t["id_or_slug"].lower() for t in prev_cat["catalog"]}
store=json.load(open(os.path.join(STORE,"ricebowl.json")))
store_slugs={t["id_or_slug"].lower() for t in store["templates"]}
new_vs_cat=[t for t in catalog if t["id_or_slug"].lower() not in prev_slugs]
new_vs_store=[t for t in catalog if t["id_or_slug"].lower() not in store_slugs]
gone=[t for t in prev_cat["catalog"] if t["id_or_slug"].lower() not in {x["id_or_slug"].lower() for x in catalog}]
print("new vs yest catalog", len(new_vs_cat))
for t in new_vs_cat:
    print("  CATNEW", t)
print("new vs store", len(new_vs_store))
for t in new_vs_store:
    in_yest_cat = t["id_or_slug"].lower() in prev_slugs
    print("  STORENEW", ("(already in yest catalog, was filtered tool?)" if in_yest_cat else "(brand new)"), t)
print("gone from catalog", len(gone))
for t in gone[:20]:
    print("  GONE", t["id_or_slug"])

out={"catalog": catalog, "new_vs_yest_catalog": new_vs_cat, "new_vs_store": new_vs_store, "gone": gone,
     "numberOfItems_claimed": int(m.group(1)) if m else None, "status": rb["status"], "html_len": len(rb_html)}
json.dump(out, open(os.path.join(OUTDIR,"ricebowl_catalog.json"),"w"), ensure_ascii=False, indent=2)
print("wrote ricebowl_catalog.json")
