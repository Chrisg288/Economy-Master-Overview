# GitHub Web Upload Instructions

The previous commit failed because one CSV file was too large for the browser uploader.

## Upload sequence

Download and extract each batch ZIP. Upload the **extracted contents** to the repository root in this order:

1. `BATCH_01_CORE_APP_DOCS`
2. `BATCH_02_TREES_CLASSIFICATIONS`
3. `BATCH_03_PRODUCT_DATA_A`
4. `BATCH_04_PRODUCT_DATA_B_SERVICES_SOURCES`

Commit each batch before starting the next one.

## Important

Do not upload the batch ZIP files themselves. GitHub Pages does not unpack ZIP files.

The split product/service CSV files are archival/review tables. The interface itself loads the need-level JSON files, so no runtime behavior was removed.

## Reconstructing the combined CSV locally

The parts are listed in:

```text
data/products/product_service_records_19009_parts_index.json
```

PowerShell example:

```powershell
$parts = Get-ChildItem ".\data\products\product_service_records_19009_part_*.csv" | Sort-Object Name
Get-Content $parts[0] | Set-Content ".\data\products\product_service_records_19009_combined.csv"
$parts | Select-Object -Skip 1 | ForEach-Object {
    Get-Content $_ | Select-Object -Skip 1 | Add-Content ".\data\products\product_service_records_19009_combined.csv"
}
```
