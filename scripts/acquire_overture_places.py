#!/usr/bin/env python3
"""Download Overture Places for a chosen bounding box; full global data is too large for GitHub Pages."""
from __future__ import annotations
import argparse, pathlib, subprocess

def main():
    p=argparse.ArgumentParser(); p.add_argument("--bbox",required=True,help="west,south,east,north"); p.add_argument("--output",default="data/acquired/raw/overture_places.geojson"); args=p.parse_args()
    out=pathlib.Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    command=["overturemaps","download",f"--bbox={args.bbox}","-f","geojson","--type=place","-o",str(out)]
    print("Running:"," ".join(command)); subprocess.run(command,check=True)
if __name__=="__main__": main()
