# Acquisition Run 01 Runbook

## What this run can acquire without keys

- Open Food Facts Canada product sample through public API.
- NVD CPE dictionary sample through public XML feed.
- ENERGY STAR Certified Computers CSV.
- ENERGY STAR Certified Residential Refrigerators CSV.
- NHTSA vPIC All Makes CSV.
- Fastenal Fastener Reference Guide PDF.
- Accuride drawer slide catalogue PDF.

## Local run

```powershell
cd <repo root>
python .\Comparator-definitions\data-sources\acquisition_runs\run_01_open_sources\scripts\download_open_sources_run_01.py
```

## Larger Open Food Facts run

```powershell
python .\Comparator-definitions\data-sources\acquisition_runs\run_01_open_sources\scripts\download_open_sources_run_01.py --include-large
```

The full Open Food Facts JSONL file is large. Do not commit it directly to GitHub.
