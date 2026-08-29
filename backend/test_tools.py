from tools.sales import analyze_sales
from tools.products import find_low_conversion_products, check_inventory
from tools.carts import find_abandoned_carts
from tools.customers import find_customer_segments
import json

print("=== SALES ANALYSIS ===")
print(json.dumps(analyze_sales(), indent=2))

print("\n=== LOW CONVERSION PRODUCTS ===")
print(json.dumps(find_low_conversion_products(), indent=2))

print("\n=== LOW STOCK ===")
print(json.dumps(check_inventory(), indent=2))

print("\n=== ABANDONED CARTS ===")
print(json.dumps(find_abandoned_carts(), indent=2))

print("\n=== CUSTOMER SEGMENTS ===")
segments = find_customer_segments()
for key in segments:
    print(f"{key}: {segments[key]['count']} customers")