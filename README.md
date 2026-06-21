# Economy Master Interface v2.10.8 — Human Needs Priority Tree

This version restores the core Comparator design principle:

```text
LIST USER WANTS / NEEDS
MOST IMPORTANT
↓
HIERARCHICAL TREEVIEW
↓
LEAST IMPORTANT
```

## Fundamental rule

For **Human / Consumer**, the TreeView is the fastest way for a user to identify wants and needs.

It is ordered by priority from immediate survival needs to lower-priority wants.

## Second fundamental rule

The Comparator uses sortable datagrids so the user can compare relative items and determine greatest value/fulfillment.

## Modular files

```text
index.html
README.md
data/app/app_config.json
data/app/context_ribbon.json
data/app/tree_nodes.json
data/app/source_inventory.json
data/app/sample_records.json
data/app/datagrid_columns.json
data/app/need_priority_model.json
data/app/tree_nodes.csv
data/app/sample_records.csv
data-sources/comparator_compiled/inventory/comparator_source_inventory_modular.json
data-sources/comparator_compiled/inventory/comparator_source_inventory_modular.csv
data-sources/comparator_compiled/samples/comparator_sample_records_modular.json
docs/layout/context_ribbon_modular_spec.json
docs/principles/human_consumer_needs_tree_principle.md
```

## Preservation rule

Do not remove or replace this priority-tree principle unless explicitly instructed. Product catalog trees support the need tree; they do not replace the need tree.
