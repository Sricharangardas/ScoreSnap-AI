import os
import datetime
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Match
from services.gemini_service import GeminiService
from agents.collector_agent import CollectorAgent
from agents.analysis_agent import AnalysisAgent
from agents.standings_agent import StandingsAgent
from agents.monitor_agent import MonitorAgent

def run():
    # Force mock mode to avoid API rate limit sleeps during bulk historical update
    GeminiService._quota_exhausted = True
    db: Session = SessionLocal()
    try:
        print("Starting Database Up-to-Date Sync (Fast Mock Mode)...")

        # 1. First, pre-create all future knockout matches in the database (M82 to M97)
        # so they exist and can receive advanced team names.
        all_knockouts = []
        
        # Round of 16 (M82 to M89)
        r16_configs = {
            "WC26-M82": (datetime.datetime(2026, 7, 4, 17, 0), "Seattle Stadium", "Round of 16"),
            "WC26-M83": (datetime.datetime(2026, 7, 4, 20, 30), "Toronto Stadium", "Round of 16"),
            "WC26-M84": (datetime.datetime(2026, 7, 5, 15, 0), "MetLife Stadium", "Round of 16"),
            "WC26-M85": (datetime.datetime(2026, 7, 5, 18, 0), "SoFi Stadium", "Round of 16"),
            "WC26-M86": (datetime.datetime(2026, 7, 6, 15, 0), "Mercedes-Benz Stadium", "Round of 16"),
            "WC26-M87": (datetime.datetime(2026, 7, 6, 18, 0), "Houston Stadium", "Round of 16"),
            "WC26-M88": (datetime.datetime(2026, 7, 7, 15, 0), "Dallas Stadium", "Round of 16"),
            "WC26-M89": (datetime.datetime(2026, 7, 7, 18, 0), "BC Place", "Round of 16"),
        }
        
        # Quarter-finals (M90 to M93)
        qf_configs = {
            "WC26-M90": (datetime.datetime(2026, 7, 9, 19, 0), "Boston Stadium", "Quarter-finals"),
            "WC26-M91": (datetime.datetime(2026, 7, 10, 19, 0), "Miami Stadium", "Quarter-finals"),
            "WC26-M92": (datetime.datetime(2026, 7, 11, 15, 0), "Dallas Stadium", "Quarter-finals"),
            "WC26-M93": (datetime.datetime(2026, 7, 11, 19, 0), "SoFi Stadium", "Quarter-finals"),
        }
        
        # Semi-finals (M94, M95)
        sf_configs = {
            "WC26-M94": (datetime.datetime(2026, 7, 14, 19, 0), "MetLife Stadium", "Semi-finals"),
            "WC26-M95": (datetime.datetime(2026, 7, 15, 19, 0), "Atlanta Stadium", "Semi-finals"),
        }
        
        # Third-place & Final (M96, M97)
        final_configs = {
            "WC26-M96": (datetime.datetime(2026, 7, 18, 21, 0), "Miami Stadium", "Third-place play-off"),
            "WC26-M97": (datetime.datetime(2026, 7, 19, 19, 0), "New York New Jersey Stadium", "Final"),
        }

        # Insert placeholder matches if they don't exist
        for m_id, (m_date, stadium, stage) in {**r16_configs, **qf_configs, **sf_configs, **final_configs}.items():
            existing = db.query(Match).filter(Match.match_id == m_id).first()
            if not existing:
                m = Match(
                    match_id=m_id,
                    team_1="TBD",
                    team_2="TBD",
                    status="scheduled",
                    match_date=m_date,
                    stadium=stadium,
                    group_name=stage
                )
                db.add(m)
                print(f"Created placeholder match: {m_id} ({stage})")
        db.commit()

        # 2. Process Round of 32 match updates (M66 to M81)
        r32_results = {
            "WC26-M66": (1, 0, "Canada"),
            "WC26-M67": (2, 1, "Brazil"),
            "WC26-M68": (1, 1, "Paraguay"),
            "WC26-M69": (1, 1, "Morocco"),
            "WC26-M70": (2, 0, "Mexico"),
            "WC26-M71": (2, 1, "England"),
            "WC26-M72": (2, 0, "United States"),
            "WC26-M73": (3, 2, "Belgium"),
            "WC26-M74": (3, 0, "France"),
            "WC26-M75": (3, 0, "Spain"),
            "WC26-M76": (2, 1, "Portugal"),
            "WC26-M77": (2, 1, "Switzerland"),
            "WC26-M78": (1, 1, "Egypt"),
            "WC26-M79": (3, 2, "Argentina"),
            "WC26-M80": (1, 0, "Colombia"),
            "WC26-M81": (1, 2, "Norway"),
        }

        print("\n--- Updating Round of 32 matches ---")
        for m_id, (score_1, score_2, winner) in r32_results.items():
            m = db.query(Match).filter(Match.match_id == m_id).first()
            if m:
                m.score_1 = score_1
                m.score_2 = score_2
                m.status = "completed"
                db.commit()
                # Run collector & analysis (no email)
                CollectorAgent.collect_match_stats(db, m_id)
                AnalysisAgent.analyze_completed_match(db, m_id)
                # Advance bracket
                MonitorAgent.advance_bracket(db, m_id, winner)
                print(f"Updated {m_id}: {m.team_1} {score_1} - {score_2} {m.team_2}. Winner: {winner}")

        # 3. Process Round of 16 updates (M82 to M89)
        r16_results = {
            "WC26-M82": (1, 0, "France"),
            "WC26-M83": (3, 0, "Morocco"),
            "WC26-M84": (1, 0, "Spain"),
            "WC26-M85": (4, 1, "Belgium"),
            "WC26-M86": (3, 2, "England"),
            "WC26-M87": (2, 1, "Norway"),
            "WC26-M88": (3, 2, "Argentina"),
            "WC26-M89": (0, 0, "Switzerland"),
        }

        print("\n--- Updating Round of 16 matches ---")
        for m_id, (score_1, score_2, winner) in r16_results.items():
            m = db.query(Match).filter(Match.match_id == m_id).first()
            if m:
                m.score_1 = score_1
                m.score_2 = score_2
                m.status = "completed"
                db.commit()
                CollectorAgent.collect_match_stats(db, m_id)
                AnalysisAgent.analyze_completed_match(db, m_id)
                MonitorAgent.advance_bracket(db, m_id, winner)
                print(f"Updated {m_id}: {m.team_1} {score_1} - {score_2} {m.team_2}. Winner: {winner}")

        # 4. Process Quarter-final updates (M90 to M93)
        qf_results = {
            "WC26-M90": (2, 0, "France"),
            "WC26-M91": (2, 1, "Spain"),
            "WC26-M92": (2, 1, "England"),
            "WC26-M93": (3, 1, "Argentina"),
        }

        print("\n--- Updating Quarter-final matches ---")
        for m_id, (score_1, score_2, winner) in qf_results.items():
            m = db.query(Match).filter(Match.match_id == m_id).first()
            if m:
                m.score_1 = score_1
                m.score_2 = score_2
                m.status = "completed"
                db.commit()
                CollectorAgent.collect_match_stats(db, m_id)
                AnalysisAgent.analyze_completed_match(db, m_id)
                MonitorAgent.advance_bracket(db, m_id, winner)
                print(f"Updated {m_id}: {m.team_1} {score_1} - {score_2} {m.team_2}. Winner: {winner}")

        # 5. Process Semi-final 1 (M94)
        print("\n--- Updating Semi-final 1 match ---")
        m94 = db.query(Match).filter(Match.match_id == "WC26-M94").first()
        if m94:
            m94.score_1 = 2
            m94.score_2 = 0
            m94.status = "completed"
            db.commit()
            CollectorAgent.collect_match_stats(db, "WC26-M94")
            AnalysisAgent.analyze_completed_match(db, "WC26-M94")
            MonitorAgent.advance_bracket(db, "WC26-M94", "Spain")
            print(f"Updated WC26-M94: {m94.team_1} 2 - 0 {m94.team_2}. Winner: Spain")

        # 6. Recalculate Standings
        StandingsAgent.update_standings(db)
        print("\nStandings updated successfully.")

        # 7. Print status of the remaining 3 upcoming matches to verify
        print("\n--- Verifying remaining 3 matches in database ---")
        for m_id in ["WC26-M95", "WC26-M96", "WC26-M97"]:
            m = db.query(Match).filter(Match.match_id == m_id).first()
            if m:
                print(f"Match {m.match_id} ({m.group_name}): {m.team_1} vs {m.team_2} | Status: {m.status} | Date: {m.match_date.isoformat()}")

        print("\nDatabase sync completed successfully!")

    except Exception as e:
        print(f"Error during database sync: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run()
