# Newark Current Online Acquisition Package v0.1

This package is the online/current-data acquisition side of the Newark Comparator work.

## What can be acquired publicly

Public pages identify Newark current-data sources, API documentation, category browsing, procurement tools, and status vocabulary.

## What requires an API key

Bulk current product rows, current price, stock, datasheets, attributes and current availability should be retrieved through the official element14/Newark Product Search API.

The script included here is ready for that once an API key is available.

## Steps

1. Register at the element14 Partner Portal.
2. Get an API key.
3. In PowerShell:

```powershell
$env:E14_API_KEY="your_api_key_here"
python .\Comparator-definitions\data-sources\newark_current_online\scripts\newark_product_search_api_downloader.py
```

4. Results will be written to:

```text
Comparator-definitions/data-sources/newark_current_online/normalized/newark_current_offer_rows.csv
Comparator-definitions/data-sources/newark_current_online/normalized/newark_current_offer_rows.json
```

## Important

This package does not pretend to download Newark's entire live catalogue without permission/API access. It creates a legal, repeatable acquisition path for the current Comparator layer.

The historical Newark 1992 catalog is one layer. The current Newark API is the live offer layer.
