from agent.mock_llm import mock_decide_tool, mock_generate_response
from tools.sales import analyze_sales
from tools.products import find_low_conversion_products, check_inventory
from tools.carts import find_abandoned_carts
from tools.customers import find_customer_segments
from tools.campaigns import generate_offer, create_campaign

TOOL_MAP = {
    "analyze_sales": lambda: analyze_sales(),
    "find_abandoned_carts": lambda: find_abandoned_carts(),
    "find_low_conversion_products": lambda: find_low_conversion_products(),
    "check_inventory": lambda: check_inventory(),
    "find_customer_segments": lambda: find_customer_segments(),
}


def run_agent(user_message: str) -> dict:
    tool_name = mock_decide_tool(user_message)
    tool_function = TOOL_MAP[tool_name]
    tool_result = tool_function()
    response_text = mock_generate_response(tool_name, tool_result)

    return {
        "user_message": user_message,
        "tool_used": tool_name,
        "tool_result": tool_result,
        "response": response_text,
    }


def run_agent_with_action(user_message: str) -> dict:
    """
    Extended agent flow: analyze, then automatically take action
    if the situation calls for it (e.g., abandoned carts -> create campaign).
    """
    base_result = run_agent(user_message)
    tool_name = base_result["tool_used"]
    tool_result = base_result["tool_result"]

    action_taken = None

    if tool_name == "find_abandoned_carts" and tool_result:
        top = tool_result[0]
        offer = generate_offer("abandoned_cart", top["product_name"])
        campaign = create_campaign(
            name=f"Come Back & Save - {top['product_name']}",
            target_description=f"Customers who abandoned {top['product_name']} in their cart",
            offer_description=offer["message"],
            target_customer_ids=top["customer_ids"],
        )
        action_taken = campaign

    elif tool_name == "find_low_conversion_products" and tool_result:
        top = tool_result[0]
        offer = generate_offer("low_conversion", top["name"])
        campaign = create_campaign(
            name=f"Boost Sales - {top['name']}",
            target_description=f"Customers who viewed {top['name']} but didn't purchase",
            offer_description=offer["message"],
            target_customer_ids=[],
        )
        action_taken = campaign

    base_result["action_taken"] = action_taken
    return base_result