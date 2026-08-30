from agent.orchestrator import run_agent
import json

questions = [
    "Why did my sales decrease?",
    "Find my biggest growth opportunity with abandoned carts",
    "Which customers should I target?",
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"USER: {q}")
    print('='*60)
    result = run_agent(q)
    print(f"TOOL USED: {result['tool_used']}")
    print(f"RESPONSE: {result['response']}")