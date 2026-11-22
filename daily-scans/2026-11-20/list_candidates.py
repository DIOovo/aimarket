#!/usr/bin/env python3
import json
from collections import defaultdict

checks = json.load(open("/workspace/competitor-scan-2026-11-20/url_checks.json"))
by = defaultdict(list)
for c in checks:
    by[c["site"]].append(c)

for site, items in by.items():
    print("=" * 80)
    print(f"{site} ({len(items)})")
    print("=" * 80)
    for c in items:
        print(f"- {c['kind']:12} {c['id_or_slug']}")
        print(f"  URL: {c['url']}")
        print(f"  page: {(c.get('title_page') or '')[:140]}")
        print(f"  h1: {(c.get('h1') or '')[:140]}")
        print(f"  desc: {(c.get('desc') or '')[:220]}")
        print(f"  final: {c.get('final')}")
        print()
