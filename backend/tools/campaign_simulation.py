import random
from database.db import get_connection


def simulate_campaign_performance(campaign_id: int) -> dict:
    """
    Generates simulated (fake, clearly labeled) performance metrics for a campaign.
    In a real product, this would come from actual campaign tracking data
    (email opens, click-throughs, purchases) over time.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    campaign = cursor.fetchone()
    conn.close()

    if not campaign:
        return {"error": "Campaign not found"}

    target_count = len(campaign["target_customer_ids"].split(","))

    # Simulate realistic-looking funnel: not everyone converts
    open_rate = random.uniform(0.55, 0.85)
    click_rate = random.uniform(0.25, 0.50)
    conversion_rate = random.uniform(0.10, 0.30)

    opened = round(target_count * open_rate)
    clicked = round(opened * click_rate)
    converted = round(clicked * conversion_rate)

    avg_order_value = random.uniform(800, 3000)
    revenue_generated = round(converted * avg_order_value, 2)

    # Assume a small cost per targeted customer (e.g. discount cost, email cost)
    estimated_cost = round(target_count * random.uniform(15, 40), 2)
    roi_percent = round(((revenue_generated - estimated_cost) / estimated_cost) * 100, 1) if estimated_cost > 0 else 0

    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign["name"],
        "is_simulated": True,
        "simulation_note": "These are SIMULATED/DEMO results, not real campaign data.",
        "customers_targeted": target_count,
        "opened": opened,
        "clicked": clicked,
        "converted": converted,
        "conversion_rate_percent": round((converted / target_count) * 100, 1) if target_count > 0 else 0,
        "revenue_generated": revenue_generated,
        "estimated_cost": estimated_cost,
        "roi_percent": roi_percent,
    }