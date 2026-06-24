# v0.3.5 Brick Tree Fix

This patch makes the requested large TreeView correction and leaves the current layout/datagrid work otherwise intact.

## Tree rule

The Human / Consumer TreeView now contains only:

```text
Sector
  → Category / need
    → Class / fulfillment class
      → Brick / product or service class
```

It contains **no individual product or service leaves** and no artificial product-page nodes.

## Record handling

All 19,009 product/service records remain in the existing modular record files. Selecting a category, class, or brick opens/filters the linked datagrid. Selecting a datagrid row opens the flyout inspector without moving the TreeView to an item node.

## Change summary

- Previous Human tree: 19,689 nodes
- New classification-only Human tree: 238 nodes
- Removed product leaves: 13,197
- Removed service leaves: 5,812
- Removed product-page nodes: 291
- Removed service-page nodes: 151
- Retained/converted bricks: 95
- Product/service records deleted: **0**

Extract this ZIP and upload its contents to the repository root, replacing existing files. Then use **Ctrl+Shift+R** once after GitHub Pages redeploys.
