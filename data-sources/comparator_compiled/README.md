# Comparator Compiled Data Package v0.2

Generated: 2026-06-20

This package compiles the uploaded and discussed source material into first-pass Comparator data structures.

It does **not** fully extract every product row from every catalog yet. Instead it creates the controlled foundation needed to do that safely and repeatably:

- source inventory
- conversion queue
- category tree seed
- field dictionary
- normalized catalog-record schema
- sample normalized records
- context ribbon layout spec

## Main files

```text
data-sources/comparator_compiled/inventory/comparator_source_inventory_v0_2.csv
data-sources/comparator_compiled/inventory/comparator_source_inventory_v0_2.json
data-sources/comparator_compiled/inventory/comparator_conversion_queue_v0_2.csv
data-sources/comparator_compiled/category_tree/comparator_category_tree_seed_v0_2.csv
data-sources/comparator_compiled/category_tree/comparator_category_tree_seed_v0_2.json
data-sources/comparator_compiled/comparator_field_dictionary_v0_2.csv
data-sources/comparator_compiled/samples/comparator_catalog_records_seed_v0_2.csv
data-sources/comparator_compiled/schemas/comparator_catalog_record.schema.json
docs/layout/context_ribbon_layout_spec_v0_2.md
docs/layout/context_ribbon_spec_v0_2.json
```

## Important design rules

1. UID is neutral identity. Do not encode category/type/order into UID.
2. Product category trees must contain meaningful classes, not fake leaves like Budget / Standard / Premium.
3. Budget / Standard / Premium are filter/ranking attributes, not taxonomy nodes.
4. Sensitive sources are reference-only unless explicitly reviewed.
5. Safety-critical catalogs require current standards verification before advice or procurement use.
6. Official classifications such as NAPCS and GS1 GPC are crosswalk layers, not a replacement for human-facing need/value navigation.
7. The Comparator is a mode/tool over the economy model, not the entire system.

## Next extraction runs

Recommended first real product-row conversions:

1. Faucher truck-body hardware set
2. Essentra Components 2014
3. Grote electrical/lighting/fuse catalog set
4. 80/20 modular framing
5. Gregg 2016 by sections
6. Parker hose/fittings
7. GPH/Nexans electrical power connectors and clamps
8. Aluminum Fastener Supply
