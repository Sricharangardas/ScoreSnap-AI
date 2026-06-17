from sqlalchemy.orm import Session
from database.models import Match, Summary
from services.gemini_service import GeminiService
from typing import Dict, Any

class AnalysisAgent:
    @staticmethod
    def analyze_completed_match(db: Session, match_id: str, language: str = "English") -> Summary:
        """
        Agent 3 - Analyzes a completed match, generates summaries using Gemini,
        and saves the summary to the database.
        """
        # Fetch the match with its stats
        match = db.query(Match).filter(Match.match_id == match_id).first()
        if not match:
            raise ValueError(f"Match with ID {match_id} not found.")
        
        if match.status != "completed":
            raise ValueError(f"Cannot analyze match {match_id} because it is not completed yet (status: {match.status}).")

        # Check if summary already exists for this language
        existing_summary = db.query(Summary).filter(
            Summary.match_id == match_id,
            Summary.language == language
        ).first()
        
        if existing_summary:
            print(f"Summary in {language} already exists for match {match_id}. Skipping analysis.")
            return existing_summary

        print(f"Generating AI analysis for match {match_id} in {language}...")
        
        # Structure match data for the prompt
        match_data = {
            "team_1": match.team_1,
            "team_2": match.team_2,
            "score_1": match.score_1,
            "score_2": match.score_2,
            "stadium": match.stadium,
            "group_name": match.group_name,
            "stats_json": match.stats_json
        }
        
        # Call Gemini service
        analysis = GeminiService.generate_match_analysis(match_data, language)
        
        # Save to database
        db_summary = Summary(
            match_id=match_id,
            ai_summary=analysis.get("ai_summary", ""),
            storyline=analysis.get("storyline", ""),
            turning_points=analysis.get("turning_points", ""),
            tactical_analysis=analysis.get("tactical_analysis", ""),
            best_player=analysis.get("best_player", ""),
            tournament_impact=analysis.get("tournament_impact", ""),
            language=language
        )
        
        db.add(db_summary)
        db.commit()
        db.refresh(db_summary)
        print(f"AI summary saved for match {match_id} in {language}.")
        return db_summary
