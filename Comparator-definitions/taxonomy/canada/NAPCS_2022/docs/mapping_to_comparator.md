# Mapping NAPCS into the Comparator

Recommended relationship model:

```text
ComparatorNode
  has_many OfficialClassificationLinks

OfficialClassificationLink
  source_system = NAPCS Canada 2022
  source_code
  relationship = exact | broader | narrower | related
  confidence
  evidence
```

Examples:

- Human / Consumer → Food → Poultry links to NAPCS poultry/live-animal/product codes.
- Human / Consumer → Shelter → Rent → Apartments links to residential rental/real-estate service codes.
- Business / Commercial → Security → Camera Installation links to security equipment and installation/service codes.

Use NAPCS as a searchable classification layer, inspector reference, and mapping source—not as a replacement for the primary human-facing tree.
