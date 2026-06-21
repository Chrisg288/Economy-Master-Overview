# Economy Master Overview v1.9.1 — Context Ribbon + Preserved Tree

This repair keeps the unified ribbon but restores the correct tree behavior.

## Main correction

The context buttons now act as **lenses**, not TreeView replacements.

```text
Sector × Scope × Overlay × Tool
```

does **not** delete or replace the tree.

The Context Tree View now uses a single preserved root:

```text
Economy Master Context Tree
```

and includes:

```text
Economy Overview / Whole System Map
Human / Consumer / Household
Market / Exchange
Business / Commercial
Finance / Capital
Government / Public
Cross-Sector Overlays / Layers
Activity Tools / Workspaces
    Comparator
    Simulation
    Credits / Value Assessment
    Objects
```

## Preservation rule

Do not remove TreeView nodes unless explicitly requested.

Future interface changes should patch the current working file rather than rebuilding from an older prototype base.

## Upload

Upload/replace these files at the repo root:

```text
index.html
README.md
```
