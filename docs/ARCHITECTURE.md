# Modular Architecture

## Shell
`index.html` contains only stable regions: header, four-level ribbon, TreeView, center workspace, inspector and bottom dock.

## UI modules
- `ribbon.js`: Sector × Scope × Overlay × Tool
- `treeview.js`: sector-specific hierarchy loaded from JSON
- `workspace.js`: routes the selected Tree node and Tool to the center view
- `datagrid.js`: visible-column selection plus primary/secondary sorting
- `user-profile.js`: profile lens over the selected need
- `inspector.js`: class-aware selected object properties
- `event-bus.js`: summary, VRQ/event and evidence streams

## Data modules
- One JSON file per sector tree
- Source inventory separate from all sector trees
- Need/source crosswalk separate from source inventory
- Comparator columns separate from Comparator records

This prevents interface changes from silently deleting tree nodes or source records.
