"""
Temporary mock of the LLM's decision-making.
Once a real Anthropic API key is available, this will be replaced
with actual Claude tool-calling logic in orchestrator.py.

For now, this uses simple keyword matching to simulate the agent
'deciding' which tool to call based on the user's question.
"""

def mock_decide_tool(user_message: str) -> str:
    """
    Given a user's question, guess which tool the AI would call.
    Returns the tool name as a string.
    """
    message = user_message.lower()

    if "sale" in message or "revenue" in message or "decrease" in message:
        return "analyze_sales"
    elif "abandon" in message or "cart" in message:
        return "find_abandoned_carts"
    elif "convert" in message or "promote" in message:
        return "find_low_conversion_products"
    elif "stock" in message or "inventory" in message:
        return "check_inventory"
    elif "customer" in message or "segment" in message or "target" in message:
        return "find_customer_segments"
    else:
        return "analyze_sales"  # default fallback


def mock_generate_response(tool_name: str, tool_result: dict) -> str:
    """
    Given a tool's result, generate a fake 'AI-written' summary.
    This mimics what Claude would say after analyzing the data.
    """
    if tool_name == "analyze_sales":
        trend = tool_result.get("trend", "unknown")
        revenue = tool_result.get("total_revenue", 0)
        return f"Based on my analysis, your revenue over this period was ₹{revenue:,.2f}, and the trend appears to be {trend}. [This is a placeholder response — real AI reasoning will replace this once Claude is connected.]"

    elif tool_name == "find_abandoned_carts":
        if not tool_result:
            return "Good news — no abandoned carts found in this period."
        top = tool_result[0]
        return f"I found {top['abandoned_count']} customers who abandoned '{top['product_name']}' in their cart. This looks like your biggest recovery opportunity. [Placeholder response.]"

    elif tool_name == "find_low_conversion_products":
        if not tool_result:
            return "All your products are converting well!"
        top = tool_result[0]
        return f"'{top['name']}' has {top['views']:,} views but only a {top['conversion_rate']}% conversion rate. This might need a pricing or listing review. [Placeholder response.]"

    elif tool_name == "check_inventory":
        if not tool_result:
            return "All products are well-stocked."
        return f"{len(tool_result)} products are running low on stock. [Placeholder response.]"

    elif tool_name == "find_customer_segments":
        high_value = tool_result.get("high_value", {}).get("count", 0)
        return f"You have {high_value} high-value customers. Consider a loyalty campaign to retain them. [Placeholder response.]"

    return "I analyzed the data but I'm not sure how to summarize it yet. [Placeholder response.]"