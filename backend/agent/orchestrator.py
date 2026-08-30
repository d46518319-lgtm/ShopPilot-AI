from agent.mock_llm import mock_decide_tool, mock_generate_response
from tools.sales import analyze_sales
from tools.products import find_low_conversion_products, check_inventory
from tools.carts import find_abandoned_carts
from tools.customers import find_customer_segments

# Maps tool names to actual Python functions
TOOL_MAP = {
    "analyze_sales": lambda: analyze_sales(),
    "find_abandoned_carts": lambda: find_abandoned_carts(),
    "find_low_conversion_products": lambda: find_low_conversion_products(),
    "check_inventory": lambda: check_inventory(),
    "find_customer_segments": lambda: find_customer_segments(),
}


def run_agent(user_message: str) -> dict:
    """
    The full agent loop:
    1. Decide which tool to call based on the user's message
    2. Execute that tool against the real database
    3. Generate a natural-language response summarizing the result
    """
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