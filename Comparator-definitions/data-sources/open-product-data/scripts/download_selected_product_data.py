#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
import argparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

DOWNLOADS = [
    ("canada_recalls", "canada_recalls.csv", "https://recalls-rappels.canada.ca/sites/default/files/opendata-donneesouvertes/SCRSAMDonneesOuvertes.csv"),
    ("usda_food", "FoodData_Central_foundation_food_csv_2026-04-30.zip", "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip"),
    ("usda_food", "CN.2026.05-CSV.zip", "https://fdc.nal.usda.gov/fdc-datasets/CN.2026.05-CSV.zip"),
    ("energy_star", "refrigerators.csv", "https://data.energystar.gov/api/views/p5st-her9/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "furnaces.csv", "https://data.energystar.gov/api/views/i97v-e8au/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "smart_thermostats.csv", "https://data.energystar.gov/api/views/7p2p-wkbf/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "televisions.csv", "https://data.energystar.gov/api/views/pd96-rr3d/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "imaging_equipment.csv", "https://data.energystar.gov/api/views/t2v6-g4nf/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "ups.csv", "https://data.energystar.gov/api/views/ifxy-2uty/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "enterprise_servers.csv", "https://data.energystar.gov/api/views/qifb-fcj2/rows.csv?accessType=DOWNLOAD"),
    ("energy_star", "product_upc_codes.csv", "https://data.energystar.gov/api/views/8edu-y555/rows.csv?accessType=DOWNLOAD"),
    ("vehicles", "nhtsa_all_makes.csv", "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=csv"),
    ("us_cpsc", "cpsc_recalls.json", "https://www.saferproducts.gov/RestWebServices/Recall?format=json"),
]

def download(url, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent":"Economy-Master-Overview product-data acquisition/0.1"})
    with urlopen(req, timeout=180) as response:
        destination.write_bytes(response.read())

parser = argparse.ArgumentParser()
parser.add_argument("--destination", default=str(ROOT / "raw"))
parser.add_argument("--include-large", action="store_true")
parser.add_argument("--natural-health-pages", type=int, default=0)
args = parser.parse_args()
outroot = Path(args.destination)

for group, name, url in DOWNLOADS:
    dest = outroot / group / name
    print(f"Downloading {name}")
    try:
        download(url, dest)
        print(f"  OK -> {dest}")
    except Exception as exc:
        print(f"  FAILED: {exc}")

for page in range(1, args.natural_health_pages + 1):
    url = f"https://health-products.canada.ca/api/natural-licences/productlicence/?page={page}&lang=en&type=json"
    dest = outroot / "health_canada_lnhpd" / f"productlicence_page_{page:04d}.json"
    print(f"Downloading LNHPD page {page}")
    try: download(url, dest)
    except Exception as exc: print(f"  FAILED: {exc}")

if args.include_large:
    download("https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz", outroot / "large_optional" / "openfoodfacts-products.jsonl.gz")
