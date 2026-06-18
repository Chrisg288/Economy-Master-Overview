param(
    [string]$Destination = (Join-Path (Split-Path -Parent $PSScriptRoot) "raw"),
    [switch]$IncludeLarge,
    [int]$NaturalHealthPages = 0
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $Destination | Out-Null

$Downloads = @(
    @{ Group="canada_recalls"; Name="canada_recalls.csv"; Url="https://recalls-rappels.canada.ca/sites/default/files/opendata-donneesouvertes/SCRSAMDonneesOuvertes.csv" },
    @{ Group="usda_food"; Name="FoodData_Central_foundation_food_csv_2026-04-30.zip"; Url="https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip" },
    @{ Group="usda_food"; Name="CN.2026.05-CSV.zip"; Url="https://fdc.nal.usda.gov/fdc-datasets/CN.2026.05-CSV.zip" },
    @{ Group="energy_star"; Name="refrigerators.csv"; Url="https://data.energystar.gov/api/views/p5st-her9/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="furnaces.csv"; Url="https://data.energystar.gov/api/views/i97v-e8au/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="smart_thermostats.csv"; Url="https://data.energystar.gov/api/views/7p2p-wkbf/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="televisions.csv"; Url="https://data.energystar.gov/api/views/pd96-rr3d/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="imaging_equipment.csv"; Url="https://data.energystar.gov/api/views/t2v6-g4nf/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="ups.csv"; Url="https://data.energystar.gov/api/views/ifxy-2uty/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="enterprise_servers.csv"; Url="https://data.energystar.gov/api/views/qifb-fcj2/rows.csv?accessType=DOWNLOAD" },
    @{ Group="energy_star"; Name="product_upc_codes.csv"; Url="https://data.energystar.gov/api/views/8edu-y555/rows.csv?accessType=DOWNLOAD" },
    @{ Group="vehicles"; Name="nhtsa_all_makes.csv"; Url="https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=csv" },
    @{ Group="us_cpsc"; Name="cpsc_recalls.json"; Url="https://www.saferproducts.gov/RestWebServices/Recall?format=json" }
)

foreach ($d in $Downloads) {
    $dir = Join-Path $Destination $d.Group
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $out = Join-Path $dir $d.Name
    Write-Host "Downloading $($d.Name)"
    try {
        Invoke-WebRequest -Uri $d.Url -OutFile $out -Headers @{"User-Agent"="Economy-Master-Overview product-data acquisition/0.1"}
        Write-Host "  OK -> $out"
    } catch {
        Write-Warning "  FAILED: $($_.Exception.Message)"
    }
}

if ($NaturalHealthPages -gt 0) {
    $dir = Join-Path $Destination "health_canada_lnhpd"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    for ($page=1; $page -le $NaturalHealthPages; $page++) {
        $url = "https://health-products.canada.ca/api/natural-licences/productlicence/?page=$page&lang=en&type=json"
        $out = Join-Path $dir ("productlicence_page_{0:D4}.json" -f $page)
        Write-Host "Downloading LNHPD page $page"
        try { Invoke-WebRequest -Uri $url -OutFile $out } catch { Write-Warning $_.Exception.Message }
    }
}

if ($IncludeLarge) {
    $dir = Join-Path $Destination "large_optional"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $out = Join-Path $dir "openfoodfacts-products.jsonl.gz"
    Write-Host "Downloading the very large Open Food Facts JSONL archive. This may take a long time."
    Invoke-WebRequest -Uri "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz" -OutFile $out -Headers @{"User-Agent"="Economy-Master-Overview product-data acquisition/0.1"}
}

Write-Host ""
Write-Host "Manual/current resource pages still requiring review:"
Write-Host "- Canadian Nutrient File 2026"
Write-Host "- Health Canada Drug Product Database extract"
Write-Host "- EPA Safer Choice spreadsheet"
Write-Host "See source_catalog.json and docs/ACQUISITION_GUIDE.md."
