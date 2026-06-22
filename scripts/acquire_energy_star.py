#!/usr/bin/env python3
"""Download configured ENERGY STAR Socrata datasets as CSV."""
from __future__ import annotations
import argparse, json, pathlib, requests

def main():
    p=argparse.ArgumentParser(); p.add_argument("--dataset-id",action="append",required=True,help="Socrata dataset identifier; repeat for multiple datasets"); p.add_argument("--output",default="data/acquired/raw/energy_star"); args=p.parse_args()
    out=pathlib.Path(args.output); out.mkdir(parents=True,exist_ok=True)
    for dataset in args.dataset_id:
        url=f"https://data.energystar.gov/resource/{dataset}.csv?$limit=500000"
        response=requests.get(url,timeout=180,headers={"User-Agent":"EconomyMasterAcquisition/0.3"}); response.raise_for_status(); (out/f"{dataset}.csv").write_bytes(response.content)
if __name__=="__main__": main()
