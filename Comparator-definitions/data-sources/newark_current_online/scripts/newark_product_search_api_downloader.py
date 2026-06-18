#!/usr/bin/env python3
"""
Newark / element14 Product Search API downloader for Comparator.

Prerequisites:
  1. Register for an API key at https://partner.element14.com/
  2. Set an environment variable:
       Windows PowerShell:
         $env:E14_API_KEY="your_api_key_here"
       CMD:
         set E14_API_KEY=your_api_key_here
       macOS/Linux:
         export E14_API_KEY="your_api_key_here"

Usage:
  python scripts/newark_product_search_api_downloader.py

The script reads:
  config/api_config.json
  seed/newark_search_terms_seed.csv

It writes:
  raw_api/newark_api_results.jsonl
  normalized/newark_current_offer_rows.csv
  normalized/newark_current_offer_rows.json

Notes:
- The API docs indicate keyword search uses term=any:<term>.
- Manufacturer part number search uses term=manuPartNum:<part>.
- Store IDs include www.newark.com and canada.newark.com.
- API paging is limited; refine search terms rather than trying to download an entire catalog in one search.
"""
from pathlib import Path
import csv, json, os, time, urllib.parse, urllib.request

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config" / "api_config.json").read_text(encoding="utf-8"))
API_KEY = os.getenv("E14_API_KEY") or CONFIG.get("api_key_placeholder")

if not API_KEY or API_KEY == "PUT_YOUR_API_KEY_IN_ENVIRONMENT_VARIABLE":
    raise SystemExit("Missing API key. Set E14_API_KEY first.")

STORE = CONFIG.get("store_info_id", "www.newark.com")
BASE = CONFIG.get("api_url", "https://api.element14.com/catalog/products")
NUMBER = int(CONFIG.get("number_of_results", 10))
RESPONSE_GROUP = CONFIG.get("response_group", "large")

seed_path = ROOT / "seed" / "newark_search_terms_seed.csv"
raw_dir = ROOT / "raw_api"
norm_dir = ROOT / "normalized"
raw_dir.mkdir(parents=True, exist_ok=True)
norm_dir.mkdir(parents=True, exist_ok=True)

def call_api(term, offset=0):
    params = {
        "callInfo.responseDataFormat": "JSON",
        "callInfo.apiKey": API_KEY,
        "storeInfo.id": STORE,
        "term": term,
        "resultsSettings.offset": str(offset),
        "resultsSettings.numberOfResults": str(NUMBER),
        "resultsSettings.responseGroup": RESPONSE_GROUP,
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent":"Comparator-Newark-API/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def first_product_list(payload):
    # API payload nesting has changed across versions; try common shapes.
    if isinstance(payload, dict):
        for key in ("products", "manufacturerPartNumberSearchReturn", "keywordSearchReturn", "productSearchReturn"):
            obj = payload.get(key)
            if isinstance(obj, list):
                return obj
            if isinstance(obj, dict):
                for k2 in ("products", "product"):
                    if isinstance(obj.get(k2), list):
                        return obj[k2]
        # fallback search
        stack = [payload]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in ("product", "products") and isinstance(v, list):
                        return v
                    if isinstance(v, (dict, list)):
                        stack.append(v)
            elif isinstance(x, list):
                stack.extend(x)
    return []

def normalize_product(p, source_term_id, source_search_term):
    def get(*names):
        for n in names:
            if isinstance(p, dict) and n in p:
                return p.get(n)
        return None
    prices = get("prices", "price")
    inventory = get("inventory", "stock", "inv")
    return {
        "source_term_id": source_term_id,
        "source_search_term": source_search_term,
        "source_store": STORE,
        "newark_order_code": get("sku", "id", "orderCode", "displaySku"),
        "manufacturer": get("brandName", "manufacturer", "vendorName"),
        "manufacturer_part_no": get("translatedManufacturerPartNumber", "manufacturerPartNumber", "mpn"),
        "title": get("displayName", "productName", "title"),
        "description": get("description", "productDescription"),
        "rohs_status": get("rohsStatusCode", "rohsStatus"),
        "datasheet_url": get("datasheetUrl", "dataSheetUrl"),
        "image_url": get("imageUrl"),
        "raw_price_object": json.dumps(prices) if prices is not None else "",
        "raw_inventory_object": json.dumps(inventory) if inventory is not None else "",
        "retrieval_status": "api_result",
    }

rows = []
with (raw_dir / "newark_api_results.jsonl").open("w", encoding="utf-8") as rawout:
    with seed_path.open("r", encoding="utf-8-sig", newline="") as f:
        for rec in csv.DictReader(f):
            term_id = rec["term_id"]
            search_term = rec["search_term"].strip()
            mode = rec["search_mode"]
            if mode == "manufacturer_part":
                api_term = "manuPartNum:" + search_term
            elif mode == "manufacturer_or_keyword" and any(ch.isdigit() for ch in search_term):
                api_term = "any:" + search_term
            else:
                api_term = "any:" + search_term
            print("Searching", api_term)
            try:
                payload = call_api(api_term, 0)
                rawout.write(json.dumps({"term_id":term_id,"search_term":search_term,"payload":payload}) + "\n")
                products = first_product_list(payload)
                for p in products:
                    rows.append(normalize_product(p, term_id, search_term))
            except Exception as e:
                rows.append({
                    "source_term_id": term_id,
                    "source_search_term": search_term,
                    "retrieval_status": "failed",
                    "error": str(e),
                })
            time.sleep(float(CONFIG.get("delay_seconds", 0.25)))

# Write normalized files.
fieldnames = sorted({k for r in rows for k in r.keys()})
with (norm_dir / "newark_current_offer_rows.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)
(norm_dir / "newark_current_offer_rows.json").write_text(json.dumps({"records":rows}, indent=2), encoding="utf-8")
print("Wrote", len(rows), "rows.")
