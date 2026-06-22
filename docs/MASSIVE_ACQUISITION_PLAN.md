# Massive Product and Service Acquisition Plan

Millions of records should not be embedded directly in one browser TreeView JSON file. Use a layered design:

1. Human need hierarchy remains compact and meaningful.
2. Product/service groups display counts.
3. Pages or query results load only when expanded.
4. Full bulk datasets remain local as JSONL/Parquet/SQLite/DuckDB.
5. GitHub Pages carries manifests, indexes, samples and small partitions.

The acquisition registry identifies current official sources. Run the scripts locally, normalize into the Comparator schema, then produce need-mapped partitions and tree indexes.
