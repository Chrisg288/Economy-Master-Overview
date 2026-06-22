# Economy Master Interface — English Massive Corpus v0.3.1 (GitHub Web Upload Safe)

This review build keeps the v2.10.1 modular layout and four-level ribbon, makes the TreeView **30% wider by default**, and adds a draggable TreeView/Workspace separator.

## Included now

- **13,197 actual English product records** extracted from uploaded catalogs.
- **5,812 actual English historical education-service records** extracted from the uploaded Independent Study Catalog.
- **19,009 linked product/service records in total**.
- **5,199 English NAPCS Canada 2022 classification nodes** under Market → Product Identity.
- **4,447 lower-confidence catalog candidates** retained separately for QA rather than silently discarded.
- Complete prior source inventory, processed-asset registry, modular trees, sortable Comparator datagrid, and tree↔datagrid linking.

## Tree width

The TreeView begins at **367 px**, approximately 30% wider than the earlier 282 px column. Drag the vertical separator beside the TreeView to resize it. The width is saved in browser local storage. Double-click the separator or press Home while it is focused to reset it.

## Language

The default corpus in this build is English. The record schema includes `source_language` and `translations` fields, and `data/config/languages.json` defines the future language-switch contract. A genuine cross-language switch still needs translated values or a configured translation service; this build does not pretend that fallback text is a translation.

## Massive acquisition

`data/acquisition/source_registry.json` and `scripts/` define the next acquisition layer for Overture Places, NVD CPE, ENERGY STAR, USDA FoodData Central, FDA NDC, NHTSA vPIC, CPSC recalls, and Health Canada’s English recall export. These sources are intentionally acquired and partitioned locally rather than loading millions of records into one GitHub Pages file.

## Run locally

```powershell
.\serve_local.bat
```

Then open the local address shown by Python.


## GitHub web-upload repair

The former file:

```text
data/products/product_service_records_19009.csv
```

was 25,690,014 bytes and caused the browser commit to fail. It has been replaced by four smaller CSV files:

```text
data/products/product_service_records_19009_part_001.csv
data/products/product_service_records_19009_part_002.csv
data/products/product_service_records_19009_part_003.csv
data/products/product_service_records_19009_part_004.csv
```

The app does not depend on the former combined CSV at runtime. The linked need-level JSON files remain unchanged.

For browser uploading, use the four batch ZIPs supplied with this release. Extract each ZIP and upload its contents to the repository root in numerical order. Do not upload the ZIP files themselves.
