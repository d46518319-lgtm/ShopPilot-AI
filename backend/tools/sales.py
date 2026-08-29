from database.db import get_connection


def analyze_sales(days=7):
    """
    Analyzes revenue trend over the given number of days.
    Returns total revenue, daily breakdown, and whether sales are trending up or down.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT order_date, SUM(total_amount) as revenue, COUNT(*) as order_count
        FROM orders
        WHERE order_date >= date('now', '-{days} days')
        GROUP BY order_date
        ORDER BY order_date
    """)
    rows = cursor.fetchall()
    conn.close()

    daily_data = [
        {"date": row["order_date"], "revenue": round(row["revenue"], 2), "orders": row["order_count"]}
        for row in rows
    ]

    total_revenue = sum(d["revenue"] for d in daily_data)
    total_orders = sum(d["orders"] for d in daily_data)

    # Compare first half vs second half of the period to detect trend
    trend = "insufficient_data"
    if len(daily_data) >= 4:
        midpoint = len(daily_data) // 2
        first_half_avg = sum(d["revenue"] for d in daily_data[:midpoint]) / midpoint
        second_half_avg = sum(d["revenue"] for d in daily_data[midpoint:]) / (len(daily_data) - midpoint)

        if second_half_avg > first_half_avg * 1.1:
            trend = "increasing"
        elif second_half_avg < first_half_avg * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"

    return {
        "period_days": days,
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "daily_breakdown": daily_data,
        "trend": trend,
    }