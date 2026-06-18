# Integration Notes

## Purpose

This package adds an acquisition/reference layer for real product records, specifications, certifications, recalls, ingredients and regulatory evidence.

It does not replace the unified human-facing Comparator taxonomy. The intended relationship is:

```text
Human need / business context
× meaningful Comparator class
× NAPCS official classification
× external product data record
× live seller offer
```

Examples:

- `Shelter → Appliances → Refrigerators` can link NAPCS codes, ENERGY STAR model data, recall records and live retailer offers.
- `Food → Branded Product` can link NAPCS, USDA CNDB/Open Food Facts records, nutrient evidence and a seller listing.
- `Transportation → Passenger Vehicle` can link NAPCS, NHTSA make/model/VIN data, recalls and a live vehicle offer.

## Data roles

- **Classification:** NAPCS, GPC, NAICS where relevant.
- **Reference product record:** USDA, ENERGY STAR, NHTSA, Health Canada.
- **Risk/evidence:** Canada recalls, CPSC recalls, product licence/monograph data.
- **Offer/listing:** future seller/server database; these open sources are not a substitute for current market inventory.

## Recommended application objects

```text
ExternalSource
ExternalProductRecord
OfficialClassificationLink
ProductEvidenceRecord
ProductRecallRecord
CertificationRecord
OfferExternalReference
```
