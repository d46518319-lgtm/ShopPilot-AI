from database.db import get_connection


def find_low_conversion_products(threshold_percent=3.0):
    """
    Finds products with high views but low purchase conversion rate.
    A product 'converts' when views are high but purchases are proportionally low.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.name, p.views,
               COALESCE(SUM(oi.quantity), 0) as purchases
        FROM products p
        LEFT JOIN order_items oi ON p.id = oi.product_id
        GROUP BY p.id
    """)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        if row["views"] == 0:
            continue
        conversion_rate = (row["purchases"] / row["views"]) * 100
        if conversion_rate < threshold_percent:
            results.append({
                "product_id": row["id"],
                "name": row["name"],
                "views": row["views"],
                "purchases": row["purchases"],
                "conversion_rate": round(conversion_rate, 2),
            })

    # Sort by highest views first (biggest missed opportunity)
    results.sort(key=lambda x: x["views"], reverse=True)
    return results


def check_inventory(low_stock_threshold=20):
    """
    Finds products running low on stock.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, stock, views
        FROM products
        WHERE stock <= ?
        ORDER BY stock ASC
    """, (low_stock_threshold,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {"product_id": row["id"], "name": row["name"], "stock": row["stock"], "views": row["views"]}
        for row in rows
    ]