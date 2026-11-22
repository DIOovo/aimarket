#!/usr/bin/env python3
"""Apply today's curation on top of finalize_today.py and write store + notice."""
from pathlib import Path
import re

p = Path("/workspace/competitor-scan-2026-11-17/finalize_today.py")
t = p.read_text(encoding="utf-8")

# PREV date
t = t.replace('PREV_CHECKED_AT = "2026-11-15T10:14:26+08:00"',
              'PREV_CHECKED_AT = "2026-11-16T09:51:46+08:00"')

# Replace CURATED assignment with JSON load
m = re.search(r"^# Genuine day-over-day.*\nCURATED = \{.*?^\}\n\nFILTER_REASONS", t, re.M | re.S)
if not m:
    raise SystemExit("CURATED block not found")

replacement = '''# Genuine day-over-day new templates (verified 200). Put Me In bulk is handled separately.
CURATED = json.load(open(os.path.join(OUTDIR, "curated_source.json"), encoding="utf-8"))

FILTER_REASONS'''
t = t[:m.start()] + replacement + t[m.end()-len("FILTER_REASONS"):]

# Expand FILTER_REASONS
old_fr = '''FILTER_REASONS = {
    ("makememe.json", "christmas-ai-video-trends"): "aggregation-hub",
    ("makememe.json", "questions"): "faq-page",
    ("memelry.json", "cortis-go-ai-from-photo"): "seo-variant-of-existing-template",
    ("memelry.json", "how-to-make-no-scrubs-ai-video"): "seo-howto-landing",
    ("memelry.json", "wassup-dance-face-expression-guide"): "guide-page",
    ("memelry.json", "wassup-dance-with-three-friends"): "seo-howto-landing",
}
'''
new_fr = '''FILTER_REASONS = {
    ("makememe.json", "christmas-ai-video-trends"): "aggregation-hub",
    ("makememe.json", "questions"): "faq-page",
    ("memelry.json", "cortis-go-ai-from-photo"): "seo-variant-of-existing-template",
    ("memelry.json", "how-to-make-no-scrubs-ai-video"): "seo-howto-landing",
    ("memelry.json", "wassup-dance-face-expression-guide"): "guide-page",
    ("memelry.json", "wassup-dance-with-three-friends"): "seo-howto-landing",
    ("trendtemplate.json", "tiktok-ai-trends"): "aggregation-hub",
    ("memelry.json", "golf-dance-ai-photo-guide"): "guide-page",
    ("memelry.json", "mourinho-pressure-original-audio"): "seo-variant-of-existing-template",
    ("memelry.json", "gta-6-loading-screen-ai"): "static-image-not-video-template",
}

# Drop slugs that were renamed or now redirect to another existing template.
DROP_SLUGS = {
    "starrd.json": {
        "bro-took-the-whole-bag-ai-video": "old URL now redirects to existing careless-whisper-car-ai-video"
    },
    "putmein.json": {
        "ateez-bad-dance-challenge-ai": "renamed to bad-dance-challenge-ai-trend",
        "bulin-47-dance-ai-trend": "renamed to dame-hombro-dance-ai-trend (redirect)",
        "catel-madatorricelli-ai-dance": "renamed to catel-courtyard-dance-ai-trend (redirect)",
    },
}

# Keep in inventory if missing from sitemap but page still 200.
KEEP_MISSING = {
    "summrs.json": {"bigfoot-vlog"},
    "tryatrend.json": {"ai-halloween-costume"},
}
'''
if old_fr not in t:
    raise SystemExit("FILTER_REASONS block not found")
t = t.replace(old_fr, new_fr, 1)

# Aliases already updated in finalize_today on fin.ALIASES - add more
old_alias = '''fin.ALIASES.update({
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "pimpwalk-entrance": "pimp-walk-entrance",
    "monkey-eating-apple": "monkey-eating-apple",
    "reaching-out-cat": "reaching-out-cat",
})
'''
new_alias = '''fin.ALIASES.update({
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "mean-girls-jingle-bell-rock": "jingle-bell-rock",
    "pimpwalk-entrance": "pimp-walk-entrance",
    "monkey-eating-apple": "monkey-eating-apple",
    "reaching-out-cat": "reaching-out-cat",
    "give-it-all-to-me": "give-it-all",
    "rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "put-the-rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "shoulder-carry-im-the-one": "shoulder-carry-im-the-one",
    "im-the-one": "shoulder-carry-im-the-one",
    "im-the-one-shoulder-carry": "shoulder-carry-im-the-one",
    "feel-the-pressure": "mourinho-pressure",
    "mourinho-pressure": "mourinho-pressure",
    "mourinho-pressure-original-audio": "mourinho-pressure",
    "quiet-on-the-creek-dance": "quiet-on-the-creek",
    "jingle-bell-brazil-dance": "jingle-bell-brazil",
    "la-tormenta-de-arena": "te-he-perdido",
    "te-he-perdido": "te-he-perdido",
    "catch-santa-on-camera": "santa-caught-on-camera",
    "youre-under-arrest": "under-arrest-dance",
    "youre-under-arrest-dance": "under-arrest-dance",
    "under-arrest-dance": "under-arrest-dance",
    "tidal-wave-video": "tidal-wave",
    "su-gibi-git-su-gibi-gel": "tidal-wave",
    "christmas-pajama-dance": "christmas-dance",
    "smalltown-boy-ai-dance": "smalltown-boy-cat",
    "smalltown-boy": "smalltown-boy-cat",
})
'''
if old_alias not in t:
    raise SystemExit("ALIASES block not found")
t = t.replace(old_alias, new_alias, 1)

# NAME_OVERRIDE additions
old_no = '''fin.NAME_OVERRIDE.update({
    "wassup-in-a-minute": "Wassup in a Minute",
'''
new_no = '''fin.NAME_OVERRIDE.update({
    "shoulder-carry-im-the-one": "Shoulder Carry / I'm the One / Rollie On My Wrist",
    "mourinho-pressure": "Mourinho Pressure / Feel The Pressure",
    "te-he-perdido": "Te He Perdido / La Tormenta de Arena",
    "tidal-wave": "Tidal Wave / Su Gibi Git Su Gibi Gel",
    "under-arrest-dance": "You're Under Arrest Dance",
    "quiet-on-the-creek": "Quiet on the Creek",
    "jingle-bell-brazil": "Jingle Bell Brazil Dance",
    "my-moon-my-man": "My Moon My Man",
    "give-it-all": "BigXthaPlug Give It All",
    "dance-with-santa": "Dance With Santa",
    "santa-caught-on-camera": "Catch Santa on Camera",
    "christmas-dance": "Christmas Pajama Dance",
    "reaching-out-cat": "Reaching Out Cat",
    "never-let-her-pay": "Never Let Her Pay",
    "wassup-in-a-minute": "Wassup in a Minute",
'''
if old_no not in t:
    raise SystemExit("NAME_OVERRIDE block not found")
t = t.replace(old_no, new_no, 1)

# Put Me In notice text
old_pmi = '''    lines.append(
        f"另：Put Me In 在 11-15 把大量模板一次性写入 sitemap（lastmod 均为 2026-11-15），"
        f"今日入库 {putmein_bulk_count} 条（快照由 10 增至 {putmein_total}），不在此逐条列出；"
        "与今日他站新增撞车的见文末「多家共有」。"
    )
'''
new_pmi = '''    lines.append(
        f"另：Put Me In 继续把 11-15 的 sitemap 回填写入快照（lastmod 均为 2026-11-15），"
        f"今日再入库 {putmein_bulk_count} 条（快照增至 {putmein_total}；3 条为改名替换，不在此逐条列出）；"
        "与今日他站新增撞车的见文末「多家共有」。"
    )
'''
if old_pmi not in t:
    raise SystemExit("putmein notice block not found")
t = t.replace(old_pmi, new_pmi, 1)

# Store update: drop slugs + keep-missing notes only when kept
# Replace the block that keeps all missing and never removes.
old_keep = '''        if fetch_ok and fn not in {"ricebowl.json", "remakeyourmeme.json"}:
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
'''
new_keep = '''        drop_map = DROP_SLUGS.get(fn, {})
        keep_set = KEEP_MISSING.get(fn, set())
        removed_now = []

        templates = []
        for t0 in prev_tmpls:
            slug = t0["id_or_slug"].lower()
            if slug in drop_map:
                removed_now.append(t0)
                site_notes.append(f"Dropped {t0['id_or_slug']}: {drop_map[slug]}.")
                continue
            if fetch_ok and fn not in {"ricebowl.json", "remakeyourmeme.json"}:
                if slug not in now_slugs and slug not in {g["id_or_slug"].lower() for g in genuine_for_store}:
                    if slug in keep_set:
                        site_notes.append(
                            f"Kept {t0['id_or_slug']} despite missing from today's sitemap (page still 200)."
                        )
                        templates.append(t0)
                        continue
                    # default: keep rather than delete unverified disappearances
                    site_notes.append(
                        f"Kept {t0['id_or_slug']} despite missing from today's sitemap."
                    )
            templates.append(t0)

        have = {t0["id_or_slug"].lower() for t0 in templates}
        for g in genuine_for_store:
            if g["id_or_slug"].lower() not in have:
                templates.append({"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]})
                have.add(g["id_or_slug"].lower())
        templates.sort(key=lambda t0: t0["url"])
'''
if old_keep not in t:
    raise SystemExit("keep/templates block not found")
t = t.replace(old_keep, new_keep, 1)

# also set removed_count on rec
t = t.replace(
'''            "new_count": len(genuine_for_store),
            "removed_count": 0,
            "new_templates": [
                {"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]}
                for g in genuine_for_store
            ],
            "removed_templates": [],
''',
'''            "new_count": len(genuine_for_store),
            "removed_count": len(removed_now),
            "new_templates": [
                {"id_or_slug": g["id_or_slug"], "title": g["title"], "url": g["url"]}
                for g in genuine_for_store
            ],
            "removed_templates": [
                {"id_or_slug": x["id_or_slug"], "title": x.get("title") or x["id_or_slug"], "url": x.get("url")}
                for x in removed_now
            ],
'''
)

# putmein site note text for second wave
old_pmi_note = '''        elif fn == "putmein.json":
            site_notes.append(
                "Bulk sitemap backfill on 2026-11-15 (all lastmod 2026-11-15): "
                f"added {len(putmein_bulk)} templates already on /templates; "
                "not listed one-by-one in the daily digest."
            )
'''
new_pmi_note = '''        elif fn == "putmein.json":
            site_notes.append(
                "Continued 2026-11-15 sitemap backfill (all lastmod 2026-11-15): "
                f"added {len(putmein_bulk)} templates; 3 renamed slugs dropped; "
                "not listed one-by-one in the daily digest."
            )
'''
if old_pmi_note not in t:
    raise SystemExit("putmein site note not found")
t = t.replace(old_pmi_note, new_pmi_note, 1)

out = Path("/workspace/competitor-scan-2026-11-17/finalize_run.py")
out.write_text(t, encoding="utf-8")
print("wrote", out, "bytes", out.stat().st_size)
