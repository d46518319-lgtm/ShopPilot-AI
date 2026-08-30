from agent.orchestrator import run_agent_with_action
import json

result = run_agent_with_action("Find my biggest growth opportunity with abandoned carts")

print("RESPONSE:", result["response"])
print("\nACTION TAKEN:")
print(json.dumps(result["action_taken"], indent=2))