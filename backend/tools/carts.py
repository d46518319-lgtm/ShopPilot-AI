from database.db import get_connection


def find_abandoned_carts(days=14):
    """
    Finds cart items added within the given period that were never purchased.
    Groups by product to show which products have the most abandoned carts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT ci.product_id, p.name as product_name,
               COUNT(*) as abandoned_count,
               GROUP_CONCAT(DISTINCT ci.customer_id) as customer_ids
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.added_date >= date('now', '-{days} days')
        GROUP BY ci.product_id
        ORDER BY abandoned_count DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        customer_ids = [int(cid) for cid in row["customer_ids"].split(",")]
        results.append({
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "abandoned_count": row["abandoned_count"],
            "customer_ids": customer_ids,
        })

    return results