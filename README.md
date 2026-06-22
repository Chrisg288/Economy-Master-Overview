# Economy Master Interface — Modular Rebuild v0.2

Review build based on the v2.10.1 layout with the compact four-level ribbon.

## What changed

- The Human / Consumer TreeView now contains **10,000 product-linked leaves**.
- Products are organized under: **survival-priority need → fulfillment class → source category → 50-product page → product**.
- Tree nodes show linked product counts.
- The Comparator datagrid is linked at every tree level.
- Clicking a tree node filters the datagrid.
- Clicking a datagrid row selects and expands the exact product in the tree.
- The datagrid now has search, selectable columns, multi-column sorting, pagination, and page-size control.
- Existing source inventory, processed-asset registry, need/source mappings, and all sector trees remain included.

## Product data

Exactly 10,000 real processed records are included:

- 9,842 Government of Canada product recall/safety records.
- 158 Newark Electronics Catalog 112 (1992) historical records.

These are deliberately labelled by status. Recall evidence is not treated as a current market offer, and Newark listings are marked obsolete.

## Review

Run `serve_local.bat`, then verify:

1. Human / Consumer shows `10,000 products`.
2. Expand a need and fulfillment class to reach product categories and 50-product pages.
3. Select a need/category/page/product, click **Open Linked Datagrid**, and verify the record count.
4. Click a datagrid row and confirm the tree returns to the matching product node.
5. Click headers to sort; Shift-click adds secondary sorting.
