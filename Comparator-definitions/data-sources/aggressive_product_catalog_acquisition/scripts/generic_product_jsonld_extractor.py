#!/usr/bin/env python3
'''
Offline helper for saved HTML product pages.

Usage:
  python generic_product_jsonld_extractor.py saved_page.html

It extracts JSON-LD Product blocks where present. This is not a crawler.
'''
from pathlib import Path
import json, re, sys

if len(sys.argv) < 2:
    raise SystemExit("Usage: python generic_product_jsonld_extractor.py saved_page.html")

text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, flags=re.I|re.S)
out = []
for b in blocks:
    try:
        data = json.loads(b.strip())
        stack = data if isinstance(data, list) else [data]
        for item in stack:
            if isinstance(item, dict):
                typ = item.get("@type")
                if typ == "Product" or (isinstance(typ, list) and "Product" in typ):
                    out.append(item)
    except Exception:
        pass

print(json.dumps({"products": out}, indent=2))
