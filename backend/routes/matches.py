import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Match, Summary
from routes.auth import get_current_user
from database.models import User
from agents.monitor_agent import MonitorAgent
from agents.analysis_agent import AnalysisAgent
from services.gemini_service import GeminiService
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/matches", tags=["Matches"])

# Pydantic schema for response
class MatchResponse(BaseModel):
    match_id: str
    team_1: str
    team_2: str
    score_1: int
    score_2: int
    status: str
    match_date: datetime.datetime
    stadium: str
    group_name: str
    stats_json: Dict[str, Any] | None = None

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    id: int
    match_id: str
    ai_summary: str
    storyline: str | None
    turning_points: str | None
    tactical_analysis: str | None
    best_player: str | None
    tournament_impact: str | None
    language: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[MatchResponse])
def get_matches(
    status: str | None = Query(None, description="Filter matches by status (scheduled, live, completed)"),
    group: str | None = Query(None, description="Filter matches by group (e.g. Group A)"),
    db: Session = Depends(get_db)
):
    query = db.query(Match)
    if status:
        query = query.filter(Match.status == status)
    if group:
        query = query.filter(Match.group_name == group)
    # Order: Completed first (newest), then Live, then Scheduled (soonest)
    matches = query.all()
    
    # Custom ordering: live matches first, then scheduled (ascending), then completed (descending date)
    live = [m for m in matches if m.status == "live"]
    scheduled = sorted([m for m in matches if m.status == "scheduled"], key=lambda x: x.match_date)
    completed = sorted([m for m in matches if m.status == "completed"], key=lambda x: x.match_date, reverse=True)
    
    return live + scheduled + completed

@router.get("/{match_id}", response_model=MatchResponse)
def get_match_detail(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.get("/{match_id}/analysis", response_model=SummaryResponse)
def get_match_analysis(
    match_id: str, 
    lang: str = "English", 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetches the AI summary and analysis for a match. If not available in the requested language,
    triggers the AnalysisAgent to generate it on the fly.
    """
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != "completed":
        raise HTTPException(status_code=400, detail="Match is not completed yet")

    # Attempt to fetch summary in requested language
    summary = db.query(Summary).filter(
        Summary.match_id == match_id,
        Summary.language == lang
    ).first()

    if not summary:
        try:
            # Generate on the fly using the Analysis Agent
            summary = AnalysisAgent.analyze_completed_match(db, match_id, language=lang)
        except Exception as e:
            # Fallback to English summary if language generation fails
            summary = db.query(Summary).filter(
                Summary.match_id == match_id,
                Summary.language == "English"
            ).first()
            if not summary:
                raise HTTPException(status_code=500, detail=f"Failed to generate analysis: {str(e)}")

    return summary

@router.get("/{match_id}/prediction")
def get_match_prediction(
    match_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Advanced Feature - Calls Gemini to generate a match outcome prediction.
    """
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != "scheduled":
        raise HTTPException(status_code=400, detail="Can only predict upcoming scheduled matches")

    prediction = GeminiService.generate_prediction(match.team_1, match.team_2)
    return prediction

# SIMULATION ENDPOINTS
@router.post("/{match_id}/simulate-kickoff", response_model=MatchResponse)
def simulate_kickoff(match_id: str, db: Session = Depends(get_db)):
    """
    Moves a match from scheduled to live.
    """
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != "scheduled":
        raise HTTPException(status_code=400, detail=f"Cannot kickoff match from state: {match.status}")
    
    match.status = "live"
    db.commit()
    db.refresh(match)
    print(f"SIMULATION: Match {match_id} transitioned to LIVE.")
    return match

class FullTimeSimulationInput(BaseModel):
    score_1: int
    score_2: int

@router.post("/{match_id}/simulate-fulltime", response_model=MatchResponse)
def simulate_fulltime(match_id: str, score_input: FullTimeSimulationInput, db: Session = Depends(get_db)):
    """
    Completes a live/scheduled match, sets the scores, and executes the entire
    Agentic AI pipeline (Collector -> Analysis -> Standings -> Dispatch notifications).
    """
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Update match
    match.score_1 = score_input.score_1
    match.score_2 = score_input.score_2
    match.status = "completed"
    db.commit()
    db.refresh(match)

    print(f"SIMULATION: Match {match_id} completed with score {match.score_1}-{match.score_2}.")
    
    # Run pipeline
    MonitorAgent.finalize_completed_match(db, match_id)
    
    db.refresh(match)
    return match
