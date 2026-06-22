#!/usr/bin/env python3
"""FDA NDC download helper. Download links can change; this records the official manual page."""
from __future__ import annotations
import argparse, pathlib, requests
URL="https://open.fda.gov/apis/drug/ndc/download/"
def main():
    p=argparse.ArgumentParser(); p.add_argument("--save-page",default="data/acquired/raw/fda_ndc_download_page.html"); args=p.parse_args(); out=pathlib.Path(args.save_page); out.parent.mkdir(parents=True,exist_ok=True)
    response=requests.get(URL,timeout=90,headers={"User-Agent":"EconomyMasterAcquisition/0.3"}); response.raise_for_status(); out.write_bytes(response.content); print(f"Saved official download page to {out}. Follow its current zipped JSON links.")
if __name__=="__main__": main()
