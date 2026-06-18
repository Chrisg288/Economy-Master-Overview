#!/usr/bin/env python3
"""
Comparator Catalog Acquisition Run 01: open/no-key sources.

This script downloads and normalizes public/open sources that do not require private API keys.
Default behavior avoids multi-GB bulk dumps. Use --include-large to download Open Food Facts full JSONL.
"""

from pathlib import Path
import argparse, csv, gzip, io, json, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET, shutil

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
NORM = ROOT / "normalized"
LOGS = ROOT / "logs"
for d in (RAW, NORM, LOGS):
    d.mkdir(parents=True, exist_ok=True)

def urlopen_bytes(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent":"ComparatorCatalogAcquisition/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def download_file(url, dest, timeout=300):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent":"ComparatorCatalogAcquisition/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, dest.open("wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    return dest

def write_csv_json(name, rows):
    if not rows:
        return
    keys = sorted({k for r in rows for k in r.keys()})
    csv_path = NORM / f"{name}.csv"
    json_path = NORM / f"{name}.json"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps({"records": rows}, indent=2), encoding="utf-8")
    print(f"Wrote {csv_path} ({len(rows)} rows)")

def simple_download_csv(name, url):
    data = urlopen_bytes(url)
    text = data.decode("utf-8-sig", errors="replace")
    rows = list(csv.DictReader(io.StringIO(text)))
    for r in rows:
        r.setdefault("source_url", url)
    write_csv_json(name, rows)
    return len(rows)

def download_open_food_facts_sample(pages=2, page_size=100):
    rows = []
    fields = "code,product_name,brands,categories,categories_tags,quantity,stores,countries,labels,packaging,image_front_url,url"
    for page in range(1, pages + 1):
        params = {
            "countries_tags_en": "canada",
            "fields": fields,
            "json": "true",
            "page_size": str(page_size),
            "page": str(page),
        }
        url = "https://world.openfoodfacts.org/api/v2/search?" + urllib.parse.urlencode(params)
        payload = json.loads(urlopen_bytes(url).decode("utf-8"))
        for p in payload.get("products", []):
            rows.append({
                "source_id": "OPEN_FOOD_FACTS",
                "code": p.get("code"),
                "product_name": p.get("product_name"),
                "brands": p.get("brands"),
                "categories": p.get("categories"),
                "quantity": p.get("quantity"),
                "stores": p.get("stores"),
                "countries": p.get("countries"),
                "labels": p.get("labels"),
                "packaging": p.get("packaging"),
                "image_front_url": p.get("image_front_url"),
                "source_url": p.get("url") or ("https://world.openfoodfacts.org/product/" + str(p.get("code")) if p.get("code") else ""),
                "retrieved_mode": "api_sample_canada",
            })
        time.sleep(0.25)
    write_csv_json("open_food_facts_canada_sample", rows)
    return len(rows)

def download_nvd_cpe_sample(limit=5000):
    urls = [
        "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz",
        "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip",
    ]
    data = None
    used_url = None
    for u in urls:
        try:
            data = urlopen_bytes(u, timeout=300)
            used_url = u
            break
        except Exception as e:
            print("Failed", u, e)
    if data is None:
        print("NVD CPE download failed")
        return 0
    raw_path = RAW / ("official-cpe-dictionary_v2.3.xml.gz" if used_url.endswith(".gz") else "official-cpe-dictionary_v2.3.xml.zip")
    raw_path.write_bytes(data)

    if used_url.endswith(".gz"):
        xml_bytes = gzip.decompress(data)
    else:
        import zipfile
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            xml_bytes = z.read(z.namelist()[0])

    rows = []
    cpe_item_tag = "{http://cpe.mitre.org/dictionary/2.0}cpe-item"
    cpe23_tag = "{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item"
    context = ET.iterparse(io.BytesIO(xml_bytes), events=("end",))
    for event, elem in context:
        if elem.tag == cpe_item_tag:
            name = elem.attrib.get("name")
            title = ""
            for child in elem:
                if child.tag.endswith("title"):
                    title = child.text or ""
                    break
            cpe23 = ""
            for child in elem:
                if child.tag == cpe23_tag:
                    cpe23 = child.attrib.get("name", "")
                    break
            rows.append({"source_id":"NVD_CPE_DICTIONARY","cpe22_name":name,"cpe23_name":cpe23,"title":title,"source_url":used_url})
            elem.clear()
            if len(rows) >= limit:
                break
    write_csv_json("nvd_cpe_dictionary_sample", rows)
    return len(rows)

def download_pdfs():
    targets = [
        ("Fastenal_Fastener_Reference_Guide.pdf", "https://www.fastenal.com/content/merch_rules/images/fcom/content-library/Fastener%20Reference%20Guide.pdf"),
        ("Accuride_Drawer_Slide_Wood_Catalog_2018.pdf", "https://www.accuride.com/media/pdf/accuride-drawer-slide-wood-catalog-2018.pdf"),
    ]
    count = 0
    for fname, url in targets:
        try:
            dest = RAW / fname
            download_file(url, dest)
            count += 1
            print("Downloaded", dest)
        except Exception as e:
            print("PDF failed", url, e)
    return count

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--off-pages", type=int, default=2)
    ap.add_argument("--off-page-size", type=int, default=100)
    ap.add_argument("--cpe-limit", type=int, default=5000)
    ap.add_argument("--skip-pdfs", action="store_true")
    ap.add_argument("--include-large", action="store_true")
    args = ap.parse_args()
    summary = {"started": time.strftime("%Y-%m-%dT%H:%M:%S"), "results": {}}

    tasks = [
        ("open_food_facts_canada_sample", lambda: download_open_food_facts_sample(args.off_pages, args.off_page_size)),
        ("nvd_cpe_dictionary_sample", lambda: download_nvd_cpe_sample(args.cpe_limit)),
        ("energy_star_computers", lambda: simple_download_csv("energy_star_computers", "https://data.energystar.gov/resource/rxdj-2c88.csv?$limit=50000")),
        ("energy_star_refrigerators", lambda: simple_download_csv("energy_star_refrigerators", "https://data.energystar.gov/resource/p5st-her9.csv?$limit=50000")),
        ("nhtsa_vpic_all_makes", lambda: simple_download_csv("nhtsa_vpic_all_makes", "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=csv")),
    ]
    for name, fn in tasks:
        try:
            summary["results"][name] = {"status":"ok", "rows_or_files": fn()}
        except Exception as e:
            summary["results"][name] = {"status":"failed", "error": str(e)}
            print("FAILED", name, e)

    if not args.skip_pdfs:
        try:
            summary["results"]["pdf_catalogs"] = {"status":"ok", "files": download_pdfs()}
        except Exception as e:
            summary["results"]["pdf_catalogs"] = {"status":"failed", "error": str(e)}

    if args.include_large:
        try:
            download_file("https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz", RAW / "openfoodfacts-products.jsonl.gz", timeout=3600)
            summary["results"]["open_food_facts_bulk"] = {"status":"ok", "file":"raw/openfoodfacts-products.jsonl.gz"}
        except Exception as e:
            summary["results"]["open_food_facts_bulk"] = {"status":"failed", "error": str(e)}
    else:
        summary["results"]["open_food_facts_bulk"] = {"status":"skipped", "reason":"large file; run with --include-large"}

    summary["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (LOGS / "run_01_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
