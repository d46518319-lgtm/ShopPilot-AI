from database.db import get_connection
from datetime import datetime


def log_activity(user_message: str, tool_used: str, finding_summary: str, action_taken: str = None) -> dict:
    """
    Records one agent action to the activity log.
    """
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO activity_log (user_message, tool_used, finding_summary, action_taken, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_message, tool_used, finding_summary, action_taken, timestamp))

    log_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "log_id": log_id,
        "user_message": user_message,
        "tool_used": tool_used,
        "finding_summary": finding_summary,
        "action_taken": action_taken,
        "timestamp": timestamp,
    }


def get_activity_log(limit: int = 20) -> list:
    """
    Returns the most recent agent activities, newest first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM activity_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "log_id": row["id"],
            "user_message": row["user_message"],
            "tool_used": row["tool_used"],
            "finding_summary": row["finding_summary"],
            "action_taken": row["action_taken"],
            "timestamp": row["timestamp"],
        }
        for row in rows
    ]