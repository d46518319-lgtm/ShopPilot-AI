from agent.orchestrator import run_agent_with_action
from tools.activity_log import get_activity_log
import json

# Run the agent a few times to generate log entries
run_agent_with_action("Why did my sales decrease?")
run_agent_with_action("Find abandoned carts")
run_agent_with_action("Which products have low conversion?")

print("=== ACTIVITY LOG ===")
log = get_activity_log()
print(json.dumps(log, indent=2))