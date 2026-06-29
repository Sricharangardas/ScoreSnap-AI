import datetime
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Match

def seed():
    db: Session = SessionLocal()
    try:
        # 1. Update WC26-M66 (which already exists but was seeded with placeholders)
        m66 = db.query(Match).filter(Match.match_id == "WC26-M66").first()
        if m66:
            print("Updating WC26-M66 to Canada vs South Africa...")
            m66.team_1 = "Canada"
            m66.team_2 = "South Africa"
            m66.group_name = "Round of 32"
            m66.status = "live" # Set it to live so the monitor agent will check it
            db.commit()

        # 2. Add other Round of 32 matches (M67 to M81)
        fixtures = [
            Match(
                match_id="WC26-M67",
                team_1="Brazil",
                team_2="Japan",
                status="scheduled",
                match_date=datetime.datetime(2026, 6, 29, 17, 0),
                stadium="Houston Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M68",
                team_1="Germany",
                team_2="Paraguay",
                status="scheduled",
                match_date=datetime.datetime(2026, 6, 29, 20, 30),
                stadium="Boston Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M69",
                team_1="Netherlands",
                team_2="Morocco",
                status="scheduled",
                match_date=datetime.datetime(2026, 6, 30, 23, 59),
                stadium="Monterrey Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M70",
                team_1="Mexico",
                team_2="Ecuador",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 1, 17, 0),
                stadium="Mexico City Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M71",
                team_1="England",
                team_2="DR Congo",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 1, 20, 0),
                stadium="Atlanta Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M72",
                team_1="United States",
                team_2="Bosnia and Herzegovina",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 2, 15, 0),
                stadium="SoFi Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M73",
                team_1="Belgium",
                team_2="Senegal",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 2, 17, 0),
                stadium="Dallas Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M74",
                team_1="France",
                team_2="Sweden",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 2, 19, 0),
                stadium="Kansas City Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M75",
                team_1="Spain",
                team_2="Austria",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 2, 21, 0),
                stadium="Miami Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M76",
                team_1="Portugal",
                team_2="Croatia",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 3, 15, 0),
                stadium="New York New Jersey Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M77",
                team_1="Switzerland",
                team_2="Algeria",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 3, 17, 0),
                stadium="BC Place Vancouver",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M78",
                team_1="Australia",
                team_2="Egypt",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 3, 19, 0),
                stadium="Seattle Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M79",
                team_1="Argentina",
                team_2="Cape Verde",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 3, 21, 0),
                stadium="Estadio Monterrey",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M80",
                team_1="Colombia",
                team_2="Ghana",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 3, 22, 30),
                stadium="Philadelphia Stadium",
                group_name="Round of 32"
            ),
            Match(
                match_id="WC26-M81",
                team_1="Ivory Coast",
                team_2="Norway",
                status="scheduled",
                match_date=datetime.datetime(2026, 7, 3, 23, 59),
                stadium="Toronto Stadium",
                group_name="Round of 32"
            ),
        ]

        print("Seeding Round of 32 fixtures...")
        for fixture in fixtures:
            existing = db.query(Match).filter(Match.match_id == fixture.match_id).first()
            if existing:
                print(f"Match {fixture.match_id} already exists. Skipping.")
                continue
            db.add(fixture)
            print(f"Added match {fixture.match_id}: {fixture.team_1} vs {fixture.team_2}")

        db.commit()
        print("Seeding complete!")
    except Exception as e:
        print(f"Error seeding Round of 32 matches: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
