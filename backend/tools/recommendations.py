from database.db import get_connection


def get_customer_purchase_history(customer_id: int) -> list:
    """
    Returns the list of product IDs a customer has purchased.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT oi.product_id
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        WHERE o.customer_id = ?
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()

    return [row["product_id"] for row in rows]


def recommend_products(customer_id: int, limit: int = 3) -> dict:
    """
    Recommends products for a customer based on what similar customers bought.
    'Similar' = customers who bought at least one of the same products.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: What has this customer already bought?
    already_bought = set(get_customer_purchase_history(customer_id))

    if not already_bought:
        conn.close()
        return {
            "customer_id": customer_id,
            "recommendations": [],
            "reason": "No purchase history yet — cannot generate personalized recommendations.",
        }

    # Step 2: Find other customers who bought at least one of the same products
    placeholders = ",".join("?" * len(already_bought))
    cursor.execute(f"""
        SELECT DISTINCT o.customer_id
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        WHERE oi.product_id IN ({placeholders}) AND o.customer_id != ?
    """, (*already_bought, customer_id))
    similar_customer_ids = [row["customer_id"] for row in cursor.fetchall()]

    if not similar_customer_ids:
        conn.close()
        return {
            "customer_id": customer_id,
            "recommendations": [],
            "reason": "No similar customers found yet.",
        }

    # Step 3: What did those similar customers buy that this customer HASN'T?
    similar_placeholders = ",".join("?" * len(similar_customer_ids))
    cursor.execute(f"""
        SELECT p.id, p.name, p.price, COUNT(*) as purchase_count
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.customer_id IN ({similar_placeholders})
        GROUP BY p.id
        ORDER BY purchase_count DESC
    """, similar_customer_ids)
    rows = cursor.fetchall()
    conn.close()

    recommendations = []
    for row in rows:
        if row["id"] not in already_bought:
            recommendations.append({
                "product_id": row["id"],
                "name": row["name"],
                "price": row["price"],
                "popularity_among_similar_customers": row["purchase_count"],
            })
        if len(recommendations) >= limit:
            break

    return {
        "customer_id": customer_id,
        "recommendations": recommendations,
        "reason": f"Based on {len(similar_customer_ids)} customers with similar purchase patterns.",
    }