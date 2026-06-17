from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.connection import get_db
from agents.monitor_agent import MonitorAgent
from agents.digest_agent import DigestAgent

router = APIRouter(prefix="/cron", tags=["Automation Crons"])

@router.get("/monitor", status_code=status.HTTP_200_OK)
def trigger_monitor(db: Session = Depends(get_db)):
    """
    Called by GitHub Actions / external ping service every 15 minutes.
    Checks kickoff times, updates live scores, completes matches, and sends alerts.
    """
    print("CRON: Triggering Match Monitor Agent...")
    try:
        MonitorAgent.monitor_matches(db)
        return {"status": "success", "message": "Monitor agent executed successfully."}
    except Exception as e:
        print(f"CRON ERROR: Monitor agent failed: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/digest", status_code=status.HTTP_200_OK)
def trigger_digest(db: Session = Depends(get_db)):
    """
    Called by GitHub Actions / external ping service once a day in the morning.
    Aggregates last 24h results and sends morning briefing.
    """
    print("CRON: Triggering Daily Digest Agent...")
    try:
        DigestAgent.generate_and_dispatch_digest(db)
        return {"status": "success", "message": "Daily digest agent executed successfully."}
    except Exception as e:
        print(f"CRON ERROR: Daily digest agent failed: {e}")
        return {"status": "error", "message": str(e)}
