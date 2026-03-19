from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/introspection", tags=["v190"])

@router.get("/decision-logs")
async def get_decision_logs():
    db_path = "agentic_core/data/interactions.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50")
    logs = c.fetchall()
    conn.close()
    return [{"timestamp": l[0], "agent": l[1], "query": l[2], "response": l[3], "feedback": l[4]} for l in logs]
