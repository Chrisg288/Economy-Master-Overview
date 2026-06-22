#!/usr/bin/env python3
"""Acquire English NHTSA vPIC makes/models and write normalized JSONL."""
from __future__ import annotations
import argparse, json, pathlib, time, requests
from tqdm import tqdm
BASE = "https://vpic.nhtsa.dot.gov/api/vehicles"

def get(path: str):
    response = requests.get(BASE + path, timeout=90, headers={"User-Agent": "EconomyMasterAcquisition/0.3"})
    response.raise_for_status(); return response.json().get("Results", [])

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",default="data/acquired/normalized/nhtsa_vpic_models.jsonl"); parser.add_argument("--delay",type=float,default=.15); args=parser.parse_args()
    makes=get("/getallmakes?format=json"); out=pathlib.Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as handle:
        for make in tqdm(makes,desc="Makes"):
            models=get(f"/GetModelsForMakeId/{make['Make_ID']}?format=json")
            for model in models:
                record={"source_uid":"SRC-NHTSA-VPIC","record_kind":"vehicle-product-identity","make_id":make["Make_ID"],"make":make["Make_Name"],"model_id":model.get("Model_ID"),"model":model.get("Model_Name"),"source_language":"English"}
                handle.write(json.dumps(record,ensure_ascii=False)+"\n")
            time.sleep(args.delay)
if __name__=="__main__": main()
