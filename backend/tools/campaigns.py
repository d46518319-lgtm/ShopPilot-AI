from database.db import get_connection
from datetime import datetime


def generate_offer(situation: str, product_name: str = None) -> dict:
    """
    Generates a promotional offer based on the situation type.
    In a real Claude-powered version, this reasoning would be done by the LLM.
    For now, uses simple business rules.
    """
    offers = {
        "abandoned_cart": {
            "discount_percent": 10,
            "message": f"Come back & save! Get 10% off {product_name or 'your cart items'}.",
        },
        "low_conversion": {
            "discount_percent": 15,
            "message": f"Limited time: 15% off {product_name or 'this product'} — don't miss out!",
        },
        "high_value_retention": {
            "discount_percent": 20,
            "message": "As one of our top customers, enjoy an exclusive 20% off your next order.",
        },
        "low_stock_clearance": {
            "discount_percent": 25,
            "message": f"Final stock alert: 25% off {product_name or 'select items'} while supplies last.",
        },
    }

    return offers.get(situation, {
        "discount_percent": 10,
        "message": "Special offer just for you: 10% off your next purchase.",
    })


def create_campaign(name: str, target_description: str, offer_description: str, target_customer_ids: list) -> dict:
    """
    Saves a new campaign to the database.
    Returns the created campaign record.
    """
    conn = get_connection()
    cursor = conn.cursor()

    customer_ids_str = ",".join(str(cid) for cid in target_customer_ids)
    created_date = datetime.now().strftime('%Y-%m-%d')

    cursor.execute("""
        INSERT INTO campaigns (name, target_description, offer_description, target_customer_ids, created_date, status)
        VALUES (?, ?, ?, ?, ?, 'active')
    """, (name, target_description, offer_description, customer_ids_str, created_date))

    campaign_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "campaign_id": campaign_id,
        "name": name,
        "target_description": target_description,
        "offer_description": offer_description,
        "target_customer_count": len(target_customer_ids),
        "created_date": created_date,
        "status": "active",
    }


def list_campaigns() -> list:
    """
    Returns all campaigns, most recent first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM campaigns ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "campaign_id": row["id"],
            "name": row["name"],
            "target_description": row["target_description"],
            "offer_description": row["offer_description"],
            "target_customer_count": len(row["target_customer_ids"].split(",")),
            "created_date": row["created_date"],
            "status": row["status"],
        }
        for row in rows
    ]