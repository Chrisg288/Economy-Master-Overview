#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
queue = ROOT / "work_queue" / "catalog_acquisition_work_queue.csv"

with queue.open("r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print(f"Loaded {len(rows)} acquisition jobs")
for method in sorted(set(r["acquisition_method"] for r in rows)):
    subset = [r for r in rows if r["acquisition_method"] == method]
    print(f"\n{method}: {len(subset)}")
    for r in subset[:10]:
        print(f"  {r['priority']} {r['source_id']} - {r['source_name']}")
