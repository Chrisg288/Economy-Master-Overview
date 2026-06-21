# Economy Master Interface v2.10.6 — Modular JSON Workspace

This package fixes the problem of only shipping `index.html`.

It keeps the v2.10-style layout and center graphic, keeps the compact ribbon, keeps **User Profile** as a mode, and moves tree/source data into modular JSON files.

## Upload to GitHub root

Upload the contents of this ZIP to the repository root.

It contains:

```text
index.html
README.md
data/app/app_config.json
data/app/context_ribbon.json
data/app/tree_nodes.json
data/app/source_inventory.json
data/app/sample_records.json
data-sources/comparator_compiled/inventory/comparator_source_inventory_modular.json
data-sources/comparator_compiled/samples/comparator_sample_records_modular.json
docs/layout/context_ribbon_modular_spec.json
```

## Key rule

The ribbon is a context lens:

```text
Sector × Scope × Overlay × Tool
```

The TreeView is populated from:

```text
data/app/tree_nodes.json
```

Source/catalog/library records are populated from:

```text
data/app/source_inventory.json
```

Do not remove TreeView nodes unless explicitly requested.
Do not rebuild from old v1.x files.
Patch this v2.10 modular line directly.

## What this does not do yet

This package does not fully extract every product row from every uploaded catalog. It carries the compiled source inventory and modular loading framework so the catalog conversion can proceed in controlled runs.
