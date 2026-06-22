#!/usr/bin/env python3
"""Download direct official bulk sources. Run locally, not in GitHub Pages."""
from __future__ import annotations
import argparse, pathlib, requests, sys
from tqdm import tqdm

SOURCES = {
    "nvd-cpe": "https://nvd.nist.gov/feeds/json/cpe/2.0/nvdcpe-2.0.zip",
    "cpsc-recalls": "https://www.saferproducts.gov/RestWebServices/Recall?format=Json",
    "health-canada-en": "https://recalls-rappels.canada.ca/sites/default/files/opendata-donneesouvertes/HCRSAMOpenData.csv",
}

def download(url: str, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=180, headers={"User-Agent": "EconomyMasterAcquisition/0.3"}) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with temp.open("wb") as handle, tqdm(total=total, unit="B", unit_scale=True, desc=destination.name) as bar:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    handle.write(chunk); bar.update(len(chunk))
    temp.replace(destination)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", choices=[*SOURCES, "all"])
    parser.add_argument("--output", default="data/acquired/raw")
    args = parser.parse_args()
    out = pathlib.Path(args.output)
    selected = SOURCES if args.source == "all" else {args.source: SOURCES[args.source]}
    extensions = {"nvd-cpe": ".zip", "cpsc-recalls": ".json", "health-canada-en": ".csv"}
    for source_id, url in selected.items():
        download(url, out / f"{source_id}{extensions[source_id]}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
