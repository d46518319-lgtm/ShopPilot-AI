from tools.recommendations import recommend_products
import json

# Test with a few different customer IDs
for customer_id in [1, 5, 10]:
    print(f"\n{'='*50}")
    print(f"Recommendations for Customer #{customer_id}")
    print('='*50)
    result = recommend_products(customer_id)
    print(json.dumps(result, indent=2))