from database.db import get_connection


def find_customer_segments():
    """
    Groups customers into segments based on total spend:
    - high_value: top spenders
    - medium_value: moderate spenders
    - low_value: minimal spenders
    - no_purchases: signed up but never bought anything
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id, c.name, c.email,
               COALESCE(SUM(o.total_amount), 0) as total_spent,
               COUNT(o.id) as order_count
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id
    """)
    rows = cursor.fetchall()
    conn.close()

    segments = {"high_value": [], "medium_value": [], "low_value": [], "no_purchases": []}

    for row in rows:
        customer = {
            "customer_id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "total_spent": round(row["total_spent"], 2),
            "order_count": row["order_count"],
        }

        if row["total_spent"] == 0:
            segments["no_purchases"].append(customer)
        elif row["total_spent"] >= 10000:
            segments["high_value"].append(customer)
        elif row["total_spent"] >= 3000:
            segments["medium_value"].append(customer)
        else:
            segments["low_value"].append(customer)

    return {
        "high_value": {"count": len(segments["high_value"]), "customers": segments["high_value"]},
        "medium_value": {"count": len(segments["medium_value"]), "customers": segments["medium_value"]},
        "low_value": {"count": len(segments["low_value"]), "customers": segments["low_value"]},
        "no_purchases": {"count": len(segments["no_purchases"]), "customers": segments["no_purchases"]},
    }