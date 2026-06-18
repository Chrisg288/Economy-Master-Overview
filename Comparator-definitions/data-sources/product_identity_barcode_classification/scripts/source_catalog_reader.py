#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT/'normalized'/'product_identity_source_catalog.json').read_text(encoding='utf-8'))['records']
for s in sorted(catalog, key=lambda x: x['priority']):
    print(f"{s['priority']}: {s['source_id']} - {s['name']}")
    print(f"  {s['url']}")
    print(f"  Access: {s['access']}")
