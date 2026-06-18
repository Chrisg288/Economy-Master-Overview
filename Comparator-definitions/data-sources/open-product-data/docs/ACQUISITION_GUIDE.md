# Acquisition Guide

## Windows / PowerShell

Open PowerShell in this `open-product-data` folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_selected_product_data.ps1
```

Optional Health Canada LNHPD pages:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_selected_product_data.ps1 -NaturalHealthPages 25
```

Optional very large Open Food Facts dump:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_selected_product_data.ps1 -IncludeLarge
```

Do not commit multi-gigabyte raw archives to normal Git history. Store them locally, through Git LFS, or as GitHub Release assets.

## Python

```text
python scripts/download_selected_product_data.py
```

Add `--include-large` only when you intentionally want the Open Food Facts bulk dump.
