import datetime
from sqlalchemy.orm import Session
from database.models import Match
from .collector_agent import CollectorAgent
from .analysis_agent import AnalysisAgent
from .standings_agent import StandingsAgent
from .email_agent import EmailAgent

class MonitorAgent:
    @staticmethod
    def monitor_matches(db: Session) -> None:
        """
        Agent 1 - Periodically checks matches, transitions status, and handles completed events.
        """
        now = datetime.datetime.utcnow()
        print(f"[{now.isoformat()}] Match Monitoring Agent executing...")

        # 1. Look for scheduled matches that should be live (kickoff time passed)
        scheduled_matches = db.query(Match).filter(Match.status == "scheduled").all()
        for match in scheduled_matches:
            if match.match_date <= now:
                print(f"Match {match.match_id} ({match.team_1} vs {match.team_2}) kickoff reached! Transitioning to live.")
                match.status = "live"
                db.commit()

        # 2. Look for live matches that should be completed (e.g., 2 hours have passed since kickoff)
        # We query the ScoreFetcher to check if the match has completed in the real world.
        live_matches = db.query(Match).filter(Match.status == "live").all()
        live_match_ids = [m.match_id for m in live_matches]

        for match_id in live_match_ids:
            try:
                db.rollback()  # Ensure connection/transaction is fresh and not stale
                match = db.query(Match).filter(Match.match_id == match_id).first()
                if not match:
                    continue

                match_duration = now - match.match_date
                # 105 minutes total (90 mins play + 15 mins halftime/added time)
                if match_duration >= datetime.timedelta(minutes=105):
                    print(f"Match {match.match_id} ({match.team_1} vs {match.team_2}) full time reached. Checking real-world score...")
                    
                    from services.score_fetcher import ScoreFetcher
                    real_score = ScoreFetcher.get_real_match_score(match.team_1, match.team_2, match.match_date)
                    
                    if real_score and real_score.get("match_completed"):
                        print(f"Match {match.match_id} is completed in the real world! Score: {real_score.get('score_1')} - {real_score.get('score_2')}")
                        match.score_1 = real_score.get("score_1")
                        match.score_2 = real_score.get("score_2")
                        match.status = "completed"
                        db.commit()

                        # Trigger downstream pipeline
                        MonitorAgent.finalize_completed_match(db, match.match_id)
                    else:
                        # Log that we are keeping it live until score is found or match is confirmed completed
                        explanation = real_score.get("explanation") if real_score else "Failed to fetch/parse search results"
                        print(f"Keeping match {match.match_id} live. Reason: {explanation}")
            except Exception as loop_err:
                print(f"Error processing live match {match_id} in monitoring loop: {loop_err}")
                try:
                    db.rollback()
                except Exception:
                    pass

    @staticmethod
    def finalize_completed_match(db: Session, match_id: str) -> None:
        """
        Runs the full pipeline of collector -> analysis -> standings -> email notifications
        for a single finalized match.
        """
        try:
            print(f"--- Finalizing Match Pipeline for {match_id} ---")
            
            # Step 1: Collect Stats
            CollectorAgent.collect_match_stats(db, match_id)
            
            # Step 2: Generate AI Analysis
            AnalysisAgent.analyze_completed_match(db, match_id, language="English")
            
            # Step 3: Recalculate Standings
            StandingsAgent.update_standings(db)
            
            # Step 4: Dispatch Emails and WhatsApp Notifications
            EmailAgent.dispatch_notifications(db, match_id)
            
            print(f"--- Finished Finalizing Match Pipeline for {match_id} ---")
        except Exception as e:
            print(f"Error occurred during finalization pipeline for match {match_id}: {e}")
            db.rollback()
