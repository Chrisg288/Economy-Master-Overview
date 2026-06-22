# Economy Master Interface — Modular Rebuild v0.1

**Layout baseline:** v2.10.1  
**Review goal:** preserve the familiar v2.10.1 three-panel workspace while rebuilding the interface as separate modules.

## What is included

```text
index.html                         Shell only
assets/css/                        Separate layout, ribbon and component styles
assets/js/                         Separate state, loader, ribbon, tree, workspace, datagrid, profile and inspector modules
data/config/                       App and four-level ribbon configuration
data/trees/                        One JSON tree per sector
data/comparator/                   Sortable Comparator columns and sample records
data/sources/                      66 compiled source records plus processed-asset registry
data/mappings/                     Need-to-source support mappings
docs/                              Architecture, principles and review checklist
```

## Non-negotiable principles

1. **Human / Consumer TreeView:** user wants and needs are ordered from most important survival need to least important want.
2. **Comparator Datagrid:** the user chooses visible columns and sorts relative items to determine greatest value and fulfillment.
3. **Source library:** catalogs, official datasets and reference books support the needs tree but never replace it.
4. **Ribbon:** Sector × Scope × Overlay × Tool is a context lens only.

## Compact four-level ribbon

The ribbon uses 17-pixel rows and reduced button padding:

```css
padding: 2px 7px;
font-size: 9.5px;
line-height: 1;
gap: 4px;
```

Each row scrolls horizontally on narrower screens instead of overlapping the workspace.

## Run locally

Double-click:

```text
serve_local.bat
```

or run:

```powershell
.\serve_local.ps1
```

Then open `http://localhost:8000/`.

GitHub Pages will load the JSON and JavaScript modules normally.
