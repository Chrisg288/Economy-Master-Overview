#!/usr/bin/env python3
"""Download FoodData Central through the API. Keep the API key outside the repository."""
from __future__ import annotations
import argparse, json, os, pathlib, requests

def main():
    p=argparse.ArgumentParser(); p.add_argument("--query",default="*"); p.add_argument("--pages",type=int,default=5); p.add_argument("--page-size",type=int,default=200); p.add_argument("--output",default="data/acquired/normalized/fooddata_search.jsonl"); args=p.parse_args()
    key=os.environ.get("FDC_API_KEY");
    if not key: raise SystemExit("Set FDC_API_KEY in your environment. Do not commit it.")
    out=pathlib.Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as handle:
        for page in range(1,args.pages+1):
            response=requests.post("https://api.nal.usda.gov/fdc/v1/foods/search",params={"api_key":key},json={"query":args.query,"pageSize":args.page_size,"pageNumber":page},timeout=120); response.raise_for_status()
            for food in response.json().get("foods",[]): handle.write(json.dumps(food,ensure_ascii=False)+"\n")
if __name__=="__main__": main()
