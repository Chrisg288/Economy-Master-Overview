#!/usr/bin/env python3
"""Maintenance entry point for rebuilding normalized NAPCS indexes from raw CSVs."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
print("Raw:",root/"raw")
print("Normalized:",root/"normalized")
print("Use the package-generation logic documented in docs/README.md for full rebuild.")
