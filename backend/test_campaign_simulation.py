from tools.campaign_simulation import simulate_campaign_performance
import json

result = simulate_campaign_performance(1)
print(json.dumps(result, indent=2))