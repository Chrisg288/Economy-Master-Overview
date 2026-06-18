# Current Newark Data Acquisition Plan

Use the official element14 / Newark Product Search API rather than page scraping.

Workflow:

```text
Historical index term or manufacturer part number
→ Product Search API keyword/manufacturer-part lookup
→ Current Newark product candidates
→ Normalize into BaseComparableOffer
→ Link historical record to current product candidate
→ Mark current lifecycle status and evidence
```

Capture:

```text
newark_order_code
manufacturer
manufacturer_part_number
description
category
datasheet_url
availability
stock
price_breaks
currency
lifecycle/availability label
retrieved_at
```
