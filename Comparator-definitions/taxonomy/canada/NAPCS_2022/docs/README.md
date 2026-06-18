# NAPCS Canada 2022 — Comparator Import Package

Official Statistics Canada **North American Product Classification System (NAPCS) Canada 2022 Version 1.0** for the Comparator definition layer.

## Included official files

- English classification structure
- English elements/examples/inclusions/exclusions
- Agricultural goods variant
- Farm Product Price Index variant
- Industrial Product Price Index variant
- Manufacturing and Logging Update 1 variant
- Merchandise import/export accounts variant
- Raw Materials Price Index variant

## Classification statistics

- **5,199 classification nodes**
- **158 groups**
- **515 classes**
- **1,477 subclasses**
- **3,049 detail nodes**
- **3,049 leaf nodes**
- **65,778 element/example records**

## Comparator use

Treat NAPCS as an official product/service classification dimension that links to the unified human-value/business tree. Do not use it to erase the human-facing taxonomy.

```text
Human need/domain path
× official NAPCS product/service code
× sector/viewpoint
× scope
```

NAPCS supplies classifications, definitions, examples, inclusions and exclusions. Live offers/listings still come from sample JSON or a server-side database.

## Main normalized files

- `napcs_canada_2022_tree.json`
- `napcs_canada_2022_nodes_flat.json`
- `napcs_canada_2022_comparator_search_index.json`
- `napcs_canada_2022_elements_by_code.json`
- `napcs_canada_2022_leaf_nodes.csv`
- `BaseComparableOffer.template.json`

## GitHub installation

Unzip and merge the contained `Comparator-definitions` folder into the root of `Economy-Master-Overview`.
