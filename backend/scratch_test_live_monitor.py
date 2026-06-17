import os
import datetime
from dotenv import load_dotenv

# MUST load dotenv before importing any app modules
load_dotenv()

from database.connection import SessionLocal
from database.models import Match
from agents.monitor_agent import MonitorAgent

def test_automated_monitoring():
    db = SessionLocal()
    try:
        # 1. Clean up any previous test matches
        db.query(Match).filter(Match.match_id == "TEST-REAL-SYNC").delete()
        db.commit()

        # 2. Insert Argentina vs France with kickoff date set to December 18, 2022
        kickoff_time = datetime.datetime(2022, 12, 18, 18, 0)
        test_match = Match(
            match_id="TEST-REAL-SYNC",
            team_1="Argentina",
            team_2="France",
            score_1=0,
            score_2=0,
            status="live",
            match_date=kickoff_time,
            stadium="Lusail Stadium",
            group_name="Group Stage"
        )
        db.add(test_match)
        db.commit()
        print(f"Inserted test match {test_match.match_id} (Argentina vs France) with status 'live'.")

        # 3. Trigger the MonitorAgent check
        print("\nRunning MonitorAgent.monitor_matches()...")
        MonitorAgent.monitor_matches(db)

        # 4. Query the match state after the monitor run
        db.refresh(test_match)
        print("\n--- Match Verification Results ---")
        print(f"Match ID: {test_match.match_id}")
        print(f"Status: {test_match.status}")
        print(f"Score: {test_match.score_1} - {test_match.score_2}")
        print(f"Stats generated: {test_match.stats_json is not None}")

        if test_match.status == "completed" and test_match.score_1 == 3 and test_match.score_2 == 3:
            print("SUCCESS: Automated score synchronization worked perfectly!")
        else:
            print("FAILED: Match did not complete or score was not synchronized correctly.")

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_automated_monitoring()
