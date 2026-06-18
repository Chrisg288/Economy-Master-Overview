# Product Identity / Barcode / Classification Source Notes

This package is the broad product-identity layer for the Comparator.

Core distinction:

ProductIdentityRecord = what the item is.
RetailOffer = who sells it, where, when, for how much.
EvidenceRecord = certification, barcode source, image source, classification source.

Best backbone:
- NAPCS Canada for Canadian economic product/service classification.
- GS1 GPC for global retail product grouping.
- UNSPSC for procurement classification.
- GS1/ECCnet for Canadian product identity/content/images where access is possible.
- Open Food Facts family for open barcode records where available.

Do not mix identity and offer:
- A UPC/GTIN can appear in many stores.
- A seller SKU is not the same as the global product identity.
- A retailer listing can disappear while the product identity remains.
