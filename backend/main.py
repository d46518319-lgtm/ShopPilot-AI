from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import get_connection
from pydantic import BaseModel
from agent.orchestrator import run_agent_with_action
from tools.campaigns import list_campaigns
from tools.campaign_simulation import simulate_campaign_performance
from tools.activity_log import get_activity_log
import os
app = FastAPI(title="ShopPilot AI Backend")
@app.on_event("startup")
def seed_database_if_needed():
    from database.db import DB_PATH
    if not os.path.exists(DB_PATH):
        from database.seed_data import create_database
        create_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ShopPilot AI backend is running"}


@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as order_count, COALESCE(SUM(total_amount), 0) as revenue
        FROM orders
        WHERE order_date >= date('now', '-7 days')
    """)
    row = cursor.fetchone()
    order_count = row["order_count"]
    revenue = row["revenue"]

    cursor.execute("SELECT COUNT(*) as count FROM customers")
    customer_count = cursor.fetchone()["count"]

    cursor.execute("SELECT SUM(views) as total_views FROM products")
    total_views = cursor.fetchone()["total_views"] or 1
    conversion_rate = round((order_count / total_views) * 100, 2)

    conn.close()

    return {
        "revenue": round(revenue, 2),
        "orders": order_count,
        "customers": customer_count,
        "conversion_rate": conversion_rate,
    }


@app.get("/api/dashboard/revenue-chart")
def get_revenue_chart():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_date, SUM(total_amount) as revenue
        FROM orders
        WHERE order_date >= date('now', '-7 days')
        GROUP BY order_date
        ORDER BY order_date
    """)
    rows = cursor.fetchall()
    conn.close()

    return [{"day": row["order_date"], "revenue": round(row["revenue"], 2)} for row in rows]


@app.get("/api/dashboard/top-products")
def get_top_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name,
               p.views,
               COALESCE(SUM(oi.quantity), 0) as purchases
        FROM products p
        LEFT JOIN order_items oi ON p.id = oi.product_id
        GROUP BY p.id
        ORDER BY p.views DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        conversion = round((row["purchases"] / row["views"]) * 100, 1) if row["views"] > 0 else 0
        result.append({
            "name": row["name"],
            "views": row["views"],
            "purchases": row["purchases"],
            "conversion": f"{conversion}%"
        })

    return result
class ChatMessage(BaseModel):
    message: str


@app.post("/api/agent/chat")
def agent_chat(payload: ChatMessage):
    result = run_agent_with_action(payload.message)
    return result


@app.get("/api/campaigns")
def get_campaigns():
    campaigns = list_campaigns()
    for c in campaigns:
        c["performance"] = simulate_campaign_performance(c["campaign_id"])
    return campaigns


@app.get("/api/agent/activity-log")
def agent_activity_log():
    return get_activity_log()