#!/usr/bin/env python3
import os
targets = [
    ("BEST_BUY_PRODUCTS_API", "BESTBUY_API_KEY"),
    ("CANADIAN_TIRE_DEVELOPER", "CANADIAN_TIRE_API_KEY"),
    ("NEWARK_PRODUCT_SEARCH_API", "E14_API_KEY"),
    ("LOWES_PRODUCT_CATALOG_API", "LOWES_API_KEY"),
    ("GS1_CANADA_ECCNET", "GS1_CANADA_ACCESS"),
    ("INGRAM_MICRO_FEEDS", "INGRAM_RESELLER_ACCESS"),
    ("TD_SYNNEX_APIS", "TD_SYNNEX_ACCESS"),
]
for source, envvar in targets:
    print(f"{source}: {'READY' if os.getenv(envvar) else 'missing ' + envvar}")
