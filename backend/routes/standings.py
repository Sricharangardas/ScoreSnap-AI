from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Standings
from agents.standings_agent import StandingsAgent
from routes.auth import get_current_user
from database.models import User
from typing import Dict, List
from pydantic import BaseModel

router = APIRouter(prefix="/standings", tags=["Standings"])

class StandingsResponse(BaseModel):
    id: int
    group_name: str
    team_name: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    points: int

    class Config:
        from_attributes = True

@router.get("/", response_model=Dict[str, List[StandingsResponse]])
def get_grouped_standings(db: Session = Depends(get_db)):
    """
    Returns standings grouped by group_name, sorted by points desc, then goal difference desc, then goals for desc.
    """
    standings = db.query(Standings).all()
    
    # Group in python
    grouped = {}
    for s in standings:
        if s.group_name not in grouped:
            grouped[s.group_name] = []
        grouped[s.group_name].append(s)

    # Sort each group
    for group_name in grouped:
        # Sort key: points DESC, GD DESC, GF DESC
        grouped[group_name] = sorted(
            grouped[group_name],
            key=lambda x: (x.points, (x.goals_for - x.goals_against), x.goals_for),
            reverse=True
        )

    return grouped

@router.post("/recalculate")
def trigger_recalculate_standings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Forces recalculating standings. Requires admin/user authentication.
    """
    try:
        StandingsAgent.update_standings(db)
        return {"status": "success", "message": "Standings successfully recalculated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to recalculate standings: {str(e)}")
