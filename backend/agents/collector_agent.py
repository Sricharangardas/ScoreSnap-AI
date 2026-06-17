from sqlalchemy.orm import Session
from database.models import Match
from services.gemini_service import GeminiService

class CollectorAgent:
    @staticmethod
    def collect_match_stats(db: Session, match_id: str) -> Match:
        """
        Agent 2 - Gathers/generates match stats.
        If a match does not have stats_json, calls Gemini to build a realistic timeline.
        """
        match = db.query(Match).filter(Match.match_id == match_id).first()
        if not match:
            raise ValueError(f"Match with ID {match_id} not found.")

        # If stats already exist, don't overwrite them
        if match.stats_json and len(match.stats_json.get("scorers", [])) > 0:
            print(f"Stats already exist for match {match_id}. Skipping collection.")
            return match

        print(f"Collecting statistics for match {match_id} ({match.team_1} vs {match.team_2})...")
        
        # Use Gemini to generate realistic stats matching the actual score
        stats = GeminiService.generate_match_stats(
            team_1=match.team_1,
            team_2=match.team_2,
            score_1=match.score_1,
            score_2=match.score_2
        )
        
        # Save to database
        match.stats_json = stats
        db.commit()
        db.refresh(match)
        print(f"Statistics successfully saved for match {match_id}.")
        return match
