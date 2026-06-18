# Comparator Vendor-Positive Catalog Data Policy v0.1

## Position

The Comparator uses public and licensed catalogue/product data to help buyers compare, source and purchase products. It should increase seller visibility, not hide it.

## Required attribution fields

Every catalogue-derived row should carry:

```text
vendor_name
brand_name
manufacturer_name
source_id
source_name
source_url
purchase_url or source_link
retrieved_date
last_verified_date
source_access_method
source_record_status
```

## Data posture

Use structured product facts:

```text
SKU / item number
manufacturer part number
GTIN / UPC / EAN
model number
category
dimensions
material
finish
thread / grade / load rating
technical specifications
price
unit of measure
package quantity
availability
vendor/source link
```

Avoid cloning the original catalogue experience:

```text
do not reproduce the vendor page layout as our layout
do not make our page look like their catalogue
avoid full-page image reproduction unless needed for private review or permitted use
avoid copying long marketing prose when factual summaries work
```

## Record separation

```text
ProductIdentityRecord = what the product is
RetailOfferRecord = who sells it, where, when, and for how much
TechnicalSpecRecord = measured/specification evidence
ClassificationRecord = NAPCS / GPC / UNSPSC / brick/category mapping
EvidenceRecord = source proof, certification, compliance, recall, warranty, datasheet
```

## Business logic

The Comparator is buyer-paid comparison and sourcing help. It should preserve source visibility and send qualified traffic to sellers when possible.
