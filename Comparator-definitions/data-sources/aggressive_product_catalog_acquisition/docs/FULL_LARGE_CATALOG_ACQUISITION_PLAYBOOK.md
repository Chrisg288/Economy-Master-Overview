# Full Large-Catalog Acquisition Playbook v0.1

## Acquisition methods

### 1. Direct open download or public API
Use first. Examples include Open Food Facts, NVD CPE, ENERGY STAR, NHTSA vPIC, some government datasets and open product registries.

### 2. Official API, feed, eProcurement or account catalogue
Use when available. Examples include Canadian Tire Developer Program, Best Buy API, Lowe's Product Catalog API, Newark/element14 Product Search API, Staples eProcurement/PunchOut, Ingram Micro and TD SYNNEX feeds.

### 3. PDF or online technical catalogue extraction
Use for manufacturer/distributor catalogues such as Richelieu, Blum, Accuride, Fastenal reference guides and other spec catalogues. Convert tables into structured facts and keep page/source references.

### 4. Public website product/category extraction
Use for public retail pages when no API/feed exists. Extract structured product facts, JSON-LD/Product schema where present, product cards, prices, availability and source URLs. Use rate limits and re-check dates.

### 5. Commercial product-data APIs or scraping APIs
Use when scale and reliability justify cost. These can fill gaps for Home Depot, Grainger, Walmart, Amazon, barcode lookups and other large public catalogues.

## First 10 full-catalog acquisition targets

1. Open Food Facts bulk data.
2. NVD CPE dictionary.
3. ENERGY STAR Product Finder datasets.
4. NAPCS Canada 2022 and GS1 GPC crosswalk.
5. Grainger catalog/index and Grainger 140K reference dataset.
6. Fastenal catalogues and Fastener Reference Guide.
7. Richelieu catalog library and product index.
8. Blum 2024/2025 catalogue and Accuride drawer-slide catalogues.
9. Best Buy Products API.
10. Canadian Tire Developer Program / public category extraction.

## Quality rules

Every row should have:
- source_id;
- source_url;
- vendor/brand/manufacturer;
- retrieved date;
- confidence;
- record type;
- public/private status;
- purchase/source link;
- source page or catalog reference where available.
