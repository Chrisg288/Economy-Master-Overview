# UI Review v0.3.3

This patch preserves the adjustable TreeView and parent record counts.

## Changes

- Comparator rows are one physical line only.
- Long values are truncated visually and available in a hover tooltip.
- The datagrid/table expands horizontally and provides a horizontal scrollbar.
- The center workspace no longer reserves permanent width for the inspector.
- The inspector is a right-side flyout. It opens for a product/service or other inspectable entity, closes with × or Escape, and closes when ribbon context changes.
- Low-information and duplicate product leaf labels use their extracted description where available. Original labels remain in hover text and inspector identity fields.
- No product records or tree nodes are deleted by this patch.

## Upload

Extract the patch ZIP and upload its contents to the repository root. Commit it as one small UI patch.
