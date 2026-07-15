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

                        # Advance bracket automatically for knockout rounds
                        MonitorAgent.advance_bracket(db, match.match_id, real_score.get("winner"))

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
    def advance_bracket(db: Session, match_id: str, winner: str = None) -> None:
        """
        Advances the winner (and loser for semi-finals) of a knockout match to the next round.
        """
        match = db.query(Match).filter(Match.match_id == match_id).first()
        if not match:
            return

        # Determine winner/loser
        if not winner:
            if match.score_1 > match.score_2:
                winner = match.team_1
            elif match.score_2 > match.score_1:
                winner = match.team_2
            else:
                # Fallback to team_1 if undecidable
                winner = match.team_1

        loser = match.team_2 if winner == match.team_1 else match.team_1

        print(f"[Bracket Progression] Match {match_id} completed. Winner: {winner}, Loser: {loser}")

        # Mapping dictionary: match_id -> (next_match_id, team_position)
        advancement_map = {
            # Round of 32 -> Round of 16
            "WC26-M74": ("WC26-M82", 1),
            "WC26-M68": ("WC26-M82", 2),
            "WC26-M69": ("WC26-M83", 1),
            "WC26-M66": ("WC26-M83", 2),
            "WC26-M75": ("WC26-M84", 1),
            "WC26-M76": ("WC26-M84", 2),
            "WC26-M73": ("WC26-M85", 1),
            "WC26-M72": ("WC26-M85", 2),
            "WC26-M71": ("WC26-M86", 1),
            "WC26-M70": ("WC26-M86", 2),
            "WC26-M81": ("WC26-M87", 1),
            "WC26-M67": ("WC26-M87", 2),
            "WC26-M79": ("WC26-M88", 1),
            "WC26-M78": ("WC26-M88", 2),
            "WC26-M77": ("WC26-M89", 1),
            "WC26-M80": ("WC26-M89", 2),

            # Round of 16 -> Quarter-finals
            "WC26-M82": ("WC26-M90", 1),
            "WC26-M83": ("WC26-M90", 2),
            "WC26-M84": ("WC26-M91", 1),
            "WC26-M85": ("WC26-M91", 2),
            "WC26-M86": ("WC26-M92", 1),
            "WC26-M87": ("WC26-M92", 2),
            "WC26-M88": ("WC26-M93", 1),
            "WC26-M89": ("WC26-M93", 2),

            # Quarter-finals -> Semi-finals
            "WC26-M91": ("WC26-M94", 1),
            "WC26-M90": ("WC26-M94", 2),
            "WC26-M92": ("WC26-M95", 1),
            "WC26-M93": ("WC26-M95", 2),
        }

        if match_id in advancement_map:
            next_match_id, pos = advancement_map[match_id]
            next_match = db.query(Match).filter(Match.match_id == next_match_id).first()
            if next_match:
                if pos == 1:
                    next_match.team_1 = winner
                else:
                    next_match.team_2 = winner
                print(f"[Bracket Progression] Set {next_match_id} team_{pos} to {winner}")
                db.commit()

        # Semi-finals -> Finals/Third-place Special mapping
        elif match_id == "WC26-M94":
            m97 = db.query(Match).filter(Match.match_id == "WC26-M97").first()
            m96 = db.query(Match).filter(Match.match_id == "WC26-M96").first()
            if m97:
                m97.team_1 = winner
                print(f"[Bracket Progression] Set Final (WC26-M97) team_1 to winner: {winner}")
            if m96:
                m96.team_1 = loser
                print(f"[Bracket Progression] Set 3rd Place (WC26-M96) team_1 to loser: {loser}")
            db.commit()

        elif match_id == "WC26-M95":
            m97 = db.query(Match).filter(Match.match_id == "WC26-M97").first()
            m96 = db.query(Match).filter(Match.match_id == "WC26-M96").first()
            if m97:
                m97.team_2 = winner
                print(f"[Bracket Progression] Set Final (WC26-M97) team_2 to winner: {winner}")
            if m96:
                m96.team_2 = loser
                print(f"[Bracket Progression] Set 3rd Place (WC26-M96) team_2 to loser: {loser}")
            db.commit()

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
