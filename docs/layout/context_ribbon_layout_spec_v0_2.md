# Context Ribbon Layout Spec v0.2

## Intent

Bring the current context buttons together into one compact ribbon.

The current layout has separate rows:

```text
Sectors
Scope
Overlays
Tools
```

The new layout should still preserve those four logical dimensions, but visually treat them as one ribbon.

## Recommended ribbon structure

```text
[ Sector: Human / Consumer | Market / Exchange | Business / Commercial | Finance / Capital | Government / Public ]
[ Scope:  International | National | Provincial / State | Municipal | Organizational | Personal ]
[ Overlay: Law / Rights | Security / Defense | Infrastructure | Resources | Information ]
[ Tool: Model | Simulate | Assess | Compare / Transact | Objects / Definitions ]
```

Visually, this can be one rounded rectangle/ribbon container under the title bar, with each row or sub-band aligned tightly.

## Better compact version

For a cleaner IDE-style layout, use group labels and tight button clusters inside a single ribbon:

```text
SECTOR  [Human / Consumer] [Market / Exchange] [Business / Commercial] [Finance / Capital] [Government / Public]
SCOPE   [International] [National] [Provincial / State] [Municipal] [Organizational] [Personal]
LAYER   [Law / Rights] [Security / Defense] [Infrastructure] [Resources] [Information]
TOOL    [Model] [Simulate] [Assess] [Compare / Transact] [Objects / Definitions]
```

The important change is not just visual. It reinforces the mental model:

```text
Sector × Scope × Overlay × Tool × Classification × Object
```

## Behavior

- Sector is single-select.
- Scope is single-select.
- Overlay may be single primary overlay or multi-toggle later.
- Tool is single-select.
- TreeView remains full-depth.
- Context selection changes the center work surface and inspector, not the entire tree identity.
- Selected breadcrumb should remain visible:

```text
Business / Commercial × Personal × Law / Rights × Model × Truck Body Hardware × Gas Spring
```

## Visual values

- One ribbon container under the title bar.
- 4 px corner radius for side panels and ribbon sections.
- 2 px corner radius is acceptable for center panels.
- Active context button uses strong blue fill.
- Inactive buttons use white/pale fill.
- Disabled/unavailable context should be greyed, not hidden.
- Keep font dense and professional.
- Avoid over-rounded “toy” buttons.

## Why this is better

This keeps the Comparator from feeling like separate screens. It becomes a controlled matrix of context:

```text
What sector am I viewing?
At what scope?
Through what overlay/layer?
Using what activity tool?
Against what classification/object?
```

That is the core mental model of the system.
