# Product Data Provenance

This review build contains exactly 10,000 real processed records, not synthetic product names.

- **9,842** Government of Canada recall/product-safety records selected from the 33,672-row snapshot already present in `Open_Product_Data_Sources_GitHub_Import_v0_1.zip`.
- **158** structured Newark Electronics Catalog 112 (1992) records already present in `Newark_Catalog_112_1992_Comparator_GitHub_Import_v0_1.zip`.

Recall notices are safety/evidence records and do not establish current availability or price. Newark listings are historical and explicitly marked obsolete. The `record_type`, `record_status`, and `availability` fields prevent those records from being presented as current retail offers.
