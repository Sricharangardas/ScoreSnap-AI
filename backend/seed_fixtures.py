import datetime
from database.connection import engine, SessionLocal, Base
from database.models import Match, Standings
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db: Session = SessionLocal()
    
    # Truncate existing standings and matches for clean reseeding
    print("Clearing old matches and standings...")
    db.query(Standings).delete()
    db.query(Match).delete()
    db.commit()

    print("Seeding database with the actual World Cup 2026 fixtures schedule...")

    matches = [
        # Group A
        Match(
            match_id="WC26-M01",
            team_1="Mexico",
            team_2="South Africa",
            score_1=2,
            score_2=0,
            status="completed",
            match_date=datetime.datetime(2026, 6, 12, 20, 0),
            stadium="Estadio Azteca, Mexico City",
            group_name="Group A",
            stats_json={
                "possession_1": 58, "possession_2": 42,
                "shots_1": 15, "shots_2": 8,
                "shots_on_target_1": 7, "shots_on_target_2": 3,
                "corners_1": 6, "corners_2": 2,
                "yellow_cards_1": 1, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 2.1, "expected_goals_2": 0.95,
                "player_of_the_match": "Santiago Gimenez",
                "scorers": [
                    {"team": "Mexico", "player": "Santiago Gimenez", "minute": 14},
                    {"team": "Mexico", "player": "Edson Alvarez", "minute": 78}
                ]
            }
        ),
        Match(
            match_id="WC26-M02",
            team_1="South Korea",
            team_2="Czechia",
            score_1=2,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 12, 23, 0),
            stadium="Chivas Stadium, Guadalajara",
            group_name="Group A",
            stats_json={
                "possession_1": 51, "possession_2": 49,
                "shots_1": 12, "shots_2": 10,
                "shots_on_target_1": 5, "shots_on_target_2": 4,
                "corners_1": 4, "corners_2": 4,
                "yellow_cards_1": 2, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.45, "expected_goals_2": 1.15,
                "player_of_the_match": "Son Heung-min",
                "scorers": [
                    {"team": "Czechia", "player": "Patrik Schick", "minute": 38},
                    {"team": "South Korea", "player": "Son Heung-min", "minute": 62},
                    {"team": "South Korea", "player": "Cho Gue-sung", "minute": 85}
                ]
            }
        ),
        Match(
            match_id="WC26-M25",
            team_1="Czechia",
            team_2="South Africa",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 18, 21, 30),
            stadium="MetLife Stadium, East Rutherford",
            group_name="Group A"
        ),
        Match(
            match_id="WC26-M28",
            team_1="Mexico",
            team_2="South Korea",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 19, 9, 30),
            stadium="Hard Rock Stadium, Miami",
            group_name="Group A"
        ),

        # Group B
        Match(
            match_id="WC26-M03",
            team_1="Canada",
            team_2="Bosnia and Herzegovina",
            score_1=1,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 13, 19, 0),
            stadium="BC Place, Vancouver",
            group_name="Group B",
            stats_json={
                "possession_1": 55, "possession_2": 45,
                "shots_1": 14, "shots_2": 9,
                "shots_on_target_1": 6, "shots_on_target_2": 3,
                "corners_1": 7, "corners_2": 2,
                "yellow_cards_1": 1, "yellow_cards_2": 3,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.6, "expected_goals_2": 1.05,
                "player_of_the_match": "Alphonso Davies",
                "scorers": [
                    {"team": "Bosnia and Herzegovina", "player": "Edin Dzeko", "minute": 24},
                    {"team": "Canada", "player": "Jonathan David", "minute": 57}
                ]
            }
        ),
        Match(
            match_id="WC26-M05",
            team_1="Qatar",
            team_2="Switzerland",
            score_1=1,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 14, 15, 0),
            stadium="Lumen Field, Seattle",
            group_name="Group B",
            stats_json={
                "possession_1": 42, "possession_2": 58,
                "shots_1": 8, "shots_2": 16,
                "shots_on_target_1": 3, "shots_on_target_2": 7,
                "corners_1": 3, "corners_2": 8,
                "yellow_cards_1": 2, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 0.85, "expected_goals_2": 1.9,
                "player_of_the_match": "Akram Afif",
                "scorers": [
                    {"team": "Switzerland", "player": "Breel Embolo", "minute": 18},
                    {"team": "Qatar", "player": "Akram Afif", "minute": 71}
                ]
            }
        ),
        Match(
            match_id="WC26-M26",
            team_1="Switzerland",
            team_2="Bosnia and Herzegovina",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 19, 0, 30),
            stadium="SoFi Stadium, Los Angeles",
            group_name="Group B"
        ),
        Match(
            match_id="WC26-M27",
            team_1="Canada",
            team_2="Qatar",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 19, 3, 30),
            stadium="BC Place, Vancouver",
            group_name="Group B"
        ),

        # Group C
        Match(
            match_id="WC26-M06",
            team_1="Brazil",
            team_2="Morocco",
            score_1=1,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 14, 18, 0),
            stadium="Mercedes-Benz Stadium, Atlanta",
            group_name="Group C",
            stats_json={
                "possession_1": 54, "possession_2": 46,
                "shots_1": 13, "shots_2": 11,
                "shots_on_target_1": 5, "shots_on_target_2": 4,
                "corners_1": 5, "corners_2": 4,
                "yellow_cards_1": 1, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.55, "expected_goals_2": 1.25,
                "player_of_the_match": "Yassine Bounou",
                "scorers": [
                    {"team": "Morocco", "player": "Hakim Ziyech", "minute": 30},
                    {"team": "Brazil", "player": "Vinicius Jr", "minute": 55}
                ]
            }
        ),
        Match(
            match_id="WC26-M07",
            team_1="Haiti",
            team_2="Scotland",
            score_1=0,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 14, 21, 0),
            stadium="NRG Stadium, Houston",
            group_name="Group C",
            stats_json={
                "possession_1": 38, "possession_2": 62,
                "shots_1": 5, "shots_2": 18,
                "shots_on_target_1": 1, "shots_on_target_2": 8,
                "corners_1": 2, "corners_2": 9,
                "yellow_cards_1": 3, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 0.35, "expected_goals_2": 2.15,
                "player_of_the_match": "Andrew Robertson",
                "scorers": [
                    {"team": "Scotland", "player": "John McGinn", "minute": 42}
                ]
            }
        ),

        # Group D
        Match(
            match_id="WC26-M04",
            team_1="USA",
            team_2="Paraguay",
            score_1=4,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 13, 22, 0),
            stadium="SoFi Stadium, Los Angeles",
            group_name="Group D",
            stats_json={
                "possession_1": 60, "possession_2": 40,
                "shots_1": 17, "shots_2": 7,
                "shots_on_target_1": 9, "shots_on_target_2": 2,
                "corners_1": 8, "corners_2": 3,
                "yellow_cards_1": 1, "yellow_cards_2": 3,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 2.65, "expected_goals_2": 0.75,
                "player_of_the_match": "Christian Pulisic",
                "scorers": [
                    {"team": "USA", "player": "Christian Pulisic", "minute": 12},
                    {"team": "Paraguay", "player": "Miguel Almiron", "minute": 33},
                    {"team": "USA", "player": "Folarin Balogun", "minute": 41},
                    {"team": "USA", "player": "Christian Pulisic", "minute": 65},
                    {"team": "USA", "player": "Timothy Weah", "minute": 89}
                ]
            }
        ),
        Match(
            match_id="WC26-M08",
            team_1="Australia",
            team_2="Türkiye",
            score_1=2,
            score_2=0,
            status="completed",
            match_date=datetime.datetime(2026, 6, 14, 23, 30),
            stadium="Gillette Stadium, Boston",
            group_name="Group D",
            stats_json={
                "possession_1": 46, "possession_2": 54,
                "shots_1": 11, "shots_2": 14,
                "shots_on_target_1": 6, "shots_on_target_2": 3,
                "corners_1": 5, "corners_2": 6,
                "yellow_cards_1": 2, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.75, "expected_goals_2": 1.25,
                "player_of_the_match": "Craig Goodwin",
                "scorers": [
                    {"team": "Australia", "player": "Mitchell Duke", "minute": 27},
                    {"team": "Australia", "player": "Craig Goodwin", "minute": 61}
                ]
            }
        ),

        # Group E
        Match(
            match_id="WC26-M09",
            team_1="Germany",
            team_2="Curaçao",
            score_1=7,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 14, 23, 59),
            stadium="Lincoln Financial Field, Philadelphia",
            group_name="Group E",
            stats_json={
                "possession_1": 67, "possession_2": 33,
                "shots_1": 24, "shots_2": 6,
                "shots_on_target_1": 14, "shots_on_target_2": 2,
                "corners_1": 10, "corners_2": 2,
                "yellow_cards_1": 0, "yellow_cards_2": 3,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 4.85, "expected_goals_2": 0.65,
                "player_of_the_match": "Jamal Musiala",
                "scorers": [
                    {"team": "Germany", "player": "Jamal Musiala", "minute": 8},
                    {"team": "Germany", "player": "Kai Havertz", "minute": 19},
                    {"team": "Germany", "player": "Florian Wirtz", "minute": 31},
                    {"team": "Germany", "player": "Jamal Musiala", "minute": 43},
                    {"team": "Curaçao", "player": "Vincent Aboubakar", "minute": 52},
                    {"team": "Germany", "player": "Kai Havertz", "minute": 61},
                    {"team": "Germany", "player": "Niclas Füllkrug", "minute": 74},
                    {"team": "Germany", "player": "Niclas Füllkrug", "minute": 88}
                ]
            }
        ),
        Match(
            match_id="WC26-M11",
            team_1="Ivory Coast",
            team_2="Ecuador",
            score_1=1,
            score_2=0,
            status="completed",
            match_date=datetime.datetime(2026, 6, 15, 18, 0),
            stadium="Hard Rock Stadium, Miami",
            group_name="Group E",
            stats_json={
                "possession_1": 49, "possession_2": 51,
                "shots_1": 10, "shots_2": 12,
                "shots_on_target_1": 4, "shots_on_target_2": 3,
                "corners_1": 4, "corners_2": 6,
                "yellow_cards_1": 2, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.15, "expected_goals_2": 1.05,
                "player_of_the_match": "Franck Kessie",
                "scorers": [
                    {"team": "Ivory Coast", "player": "Sebastian Haller", "minute": 64}
                ]
            }
        ),

        # Group F
        Match(
            match_id="WC26-M10",
            team_1="Netherlands",
            team_2="Japan",
            score_1=2,
            score_2=2,
            status="completed",
            match_date=datetime.datetime(2026, 6, 15, 15, 0),
            stadium="MetLife Stadium, East Rutherford",
            group_name="Group F",
            stats_json={
                "possession_1": 52, "possession_2": 48,
                "shots_1": 15, "shots_2": 16,
                "shots_on_target_1": 7, "shots_on_target_2": 8,
                "corners_1": 6, "corners_2": 5,
                "yellow_cards_1": 1, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 2.25, "expected_goals_2": 2.35,
                "player_of_the_match": "Kaoru Mitoma",
                "scorers": [
                    {"team": "Netherlands", "player": "Memphis Depay", "minute": 11},
                    {"team": "Japan", "player": "Kaoru Mitoma", "minute": 23},
                    {"team": "Netherlands", "player": "Cody Gakpo", "minute": 48},
                    {"team": "Japan", "player": "Ritsu Doan", "minute": 79}
                ]
            }
        ),
        Match(
            match_id="WC26-M12",
            team_1="Sweden",
            team_2="Tunisia",
            score_1=5,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 15, 20, 0),
            stadium="Mercedes-Benz Stadium, Atlanta",
            group_name="Group F",
            stats_json={
                "possession_1": 58, "possession_2": 42,
                "shots_1": 18, "shots_2": 9,
                "shots_on_target_1": 10, "shots_on_target_2": 3,
                "corners_1": 7, "corners_2": 3,
                "yellow_cards_1": 1, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 3.15, "expected_goals_2": 0.85,
                "player_of_the_match": "Alexander Isak",
                "scorers": [
                    {"team": "Sweden", "player": "Alexander Isak", "minute": 14},
                    {"team": "Sweden", "player": "Dejan Kulusevski", "minute": 33},
                    {"team": "Tunisia", "player": "Youssef Msakni", "minute": 45},
                    {"team": "Sweden", "player": "Alexander Isak", "minute": 59},
                    {"team": "Sweden", "player": "Emil Forsberg", "minute": 71},
                    {"team": "Sweden", "player": "Viktor Gyökeres", "minute": 84}
                ]
            }
        ),

        # Group G
        Match(
            match_id="WC26-M14",
            team_1="Belgium",
            team_2="Egypt",
            score_1=1,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 16, 0, 30),
            stadium="NRG Stadium, Houston",
            group_name="Group G",
            stats_json={
                "possession_1": 56, "possession_2": 44,
                "shots_1": 12, "shots_2": 9,
                "shots_on_target_1": 5, "shots_on_target_2": 4,
                "corners_1": 5, "corners_2": 4,
                "yellow_cards_1": 2, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.3, "expected_goals_2": 0.95,
                "player_of_the_match": "Mohamed Salah",
                "scorers": [
                    {"team": "Belgium", "player": "Romelu Lukaku", "minute": 41},
                    {"team": "Egypt", "player": "Mohamed Salah", "minute": 68}
                ]
            }
        ),
        Match(
            match_id="WC26-M16",
            team_1="Iran",
            team_2="New Zealand",
            score_1=2,
            score_2=2,
            status="completed",
            match_date=datetime.datetime(2026, 6, 16, 21, 30),
            stadium="SoFi Stadium, Los Angeles",
            group_name="Group G",
            stats_json={
                "possession_1": 50, "possession_2": 50,
                "shots_1": 11, "shots_2": 10,
                "shots_on_target_1": 5, "shots_on_target_2": 4,
                "corners_1": 4, "corners_2": 4,
                "yellow_cards_1": 1, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.45, "expected_goals_2": 1.35,
                "player_of_the_match": "Sardar Azmoun",
                "scorers": [
                    {"team": "Iran", "player": "Sardar Azmoun", "minute": 19},
                    {"team": "New Zealand", "player": "Chris Wood", "minute": 43},
                    {"team": "Iran", "player": "Mehdi Taremi", "minute": 64},
                    {"team": "New Zealand", "player": "Libby Cacace", "minute": 78}
                ]
            }
        ),

        # Group H
        Match(
            match_id="WC26-M13",
            team_1="Spain",
            team_2="Cape Verde",
            score_1=0,
            score_2=0,
            status="completed",
            match_date=datetime.datetime(2026, 6, 15, 21, 30),
            stadium="Gillette Stadium, Boston",
            group_name="Group H",
            stats_json={
                "possession_1": 65, "possession_2": 35,
                "shots_1": 14, "shots_2": 5,
                "shots_on_target_1": 5, "shots_on_target_2": 1,
                "corners_1": 8, "corners_2": 2,
                "yellow_cards_1": 1, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.6, "expected_goals_2": 0.4,
                "player_of_the_match": "Unai Simon",
                "scorers": []
            }
        ),
        Match(
            match_id="WC26-M15",
            team_1="Saudi Arabia",
            team_2="Uruguay",
            score_1=1,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 16, 3, 30),
            stadium="Lumen Field, Seattle",
            group_name="Group H",
            stats_json={
                "possession_1": 42, "possession_2": 58,
                "shots_1": 7, "shots_2": 15,
                "shots_on_target_1": 3, "shots_on_target_2": 6,
                "corners_1": 3, "corners_2": 6,
                "yellow_cards_1": 2, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 0.8, "expected_goals_2": 1.8,
                "player_of_the_match": "Federico Valverde",
                "scorers": [
                    {"team": "Uruguay", "player": "Darwin Nunez", "minute": 29},
                    {"team": "Saudi Arabia", "player": "Salem Al-Dawsari", "minute": 72}
                ]
            }
        ),

        # Group I
        Match(
            match_id="WC26-M17",
            team_1="France",
            team_2="Senegal",
            score_1=3,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 17, 0, 30),
            stadium="Lincoln Financial Field, Philadelphia",
            group_name="Group I",
            stats_json={
                "possession_1": 61, "possession_2": 39,
                "shots_1": 18, "shots_2": 8,
                "shots_on_target_1": 8, "shots_on_target_2": 3,
                "corners_1": 7, "corners_2": 3,
                "yellow_cards_1": 1, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 2.4, "expected_goals_2": 0.75,
                "player_of_the_match": "Kylian Mbappé",
                "scorers": [
                    {"team": "France", "player": "Kylian Mbappé", "minute": 14},
                    {"team": "Senegal", "player": "Nicolas Jackson", "minute": 41},
                    {"team": "France", "player": "Kylian Mbappé", "minute": 58},
                    {"team": "France", "player": "Antoine Griezmann", "minute": 72}
                ]
            }
        ),
        Match(
            match_id="WC26-M18",
            team_1="Iraq",
            team_2="Norway",
            score_1=1,
            score_2=4,
            status="completed",
            match_date=datetime.datetime(2026, 6, 17, 3, 30),
            stadium="Hard Rock Stadium, Miami",
            group_name="Group I",
            stats_json={
                "possession_1": 43, "possession_2": 57,
                "shots_1": 8, "shots_2": 19,
                "shots_on_target_1": 3, "shots_on_target_2": 9,
                "corners_1": 2, "corners_2": 6,
                "yellow_cards_1": 3, "yellow_cards_2": 1,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 0.85, "expected_goals_2": 2.8,
                "player_of_the_match": "Erling Haaland",
                "scorers": [
                    {"team": "Norway", "player": "Erling Haaland", "minute": 21},
                    {"team": "Iraq", "player": "Aymen Hussein", "minute": 38},
                    {"team": "Norway", "player": "Erling Haaland", "minute": 49},
                    {"team": "Norway", "player": "Martin Ødegaard", "minute": 63},
                    {"team": "Norway", "player": "Alexander Sørloth", "minute": 82}
                ]
            }
        ),

        # Group J
        Match(
            match_id="WC26-M19",
            team_1="Argentina",
            team_2="Algeria",
            score_1=3,
            score_2=0,
            status="completed",
            match_date=datetime.datetime(2026, 6, 17, 9, 30),
            stadium="MetLife Stadium, East Rutherford",
            group_name="Group J",
            stats_json={
                "possession_1": 64, "possession_2": 36,
                "shots_1": 16, "shots_2": 5,
                "shots_on_target_1": 8, "shots_on_target_2": 1,
                "corners_1": 8, "corners_2": 1,
                "yellow_cards_1": 1, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 2.3, "expected_goals_2": 0.45,
                "player_of_the_match": "Lionel Messi",
                "scorers": [
                    {"team": "Argentina", "player": "Lionel Messi", "minute": 28},
                    {"team": "Argentina", "player": "Lautaro Martinez", "minute": 54},
                    {"team": "Argentina", "player": "Julian Alvarez", "minute": 81}
                ]
            }
        ),
        Match(
            match_id="WC26-M20",
            team_1="Austria",
            team_2="Jordan",
            score_1=3,
            score_2=1,
            status="completed",
            match_date=datetime.datetime(2026, 6, 17, 9, 30),
            stadium="Mercedes-Benz Stadium, Atlanta",
            group_name="Group J",
            stats_json={
                "possession_1": 55, "possession_2": 45,
                "shots_1": 14, "shots_2": 9,
                "shots_on_target_1": 7, "shots_on_target_2": 3,
                "corners_1": 5, "corners_2": 4,
                "yellow_cards_1": 2, "yellow_cards_2": 2,
                "red_cards_1": 0, "red_cards_2": 0,
                "expected_goals_1": 1.65, "expected_goals_2": 0.95,
                "player_of_the_match": "Marcel Sabitzer",
                "scorers": [
                    {"team": "Austria", "player": "Marcel Sabitzer", "minute": 33},
                    {"team": "Jordan", "player": "Mousa Al-Tamari", "minute": 45},
                    {"team": "Austria", "player": "Christoph Baumgartner", "minute": 52},
                    {"team": "Austria", "player": "Michael Gregoritsch", "minute": 88}
                ]
            }
        ),

        # Group K
        Match(
            match_id="WC26-M21",
            team_1="Portugal",
            team_2="DR Congo",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 17, 22, 30),
            stadium="NRG Stadium, Houston",
            group_name="Group K"
        ),
        Match(
            match_id="WC26-M24",
            team_1="Uzbekistan",
            team_2="Colombia",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 18, 7, 30),
            stadium="BC Place, Vancouver",
            group_name="Group K"
        ),

        # Group L
        Match(
            match_id="WC26-M22",
            team_1="England",
            team_2="Croatia",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 18, 1, 30),
            stadium="SoFi Stadium, Los Angeles",
            group_name="Group L"
        ),
        Match(
            match_id="WC26-M23",
            team_1="Ghana",
            team_2="Panama",
            score_1=0,
            score_2=0,
            status="scheduled",
            match_date=datetime.datetime(2026, 6, 18, 4, 30),
            stadium="Gillette Stadium, Boston",
            group_name="Group L"
        )
    ]

    for m in matches:
        db.add(m)
    db.commit()
    print("Matches seeded successfully!")

    # Calculate initial standings
    recalculate_standings(db)
    
    db.close()

def recalculate_standings(db: Session):
    # Clear existing standings
    db.query(Standings).delete()
    db.commit()

    print("Calculating standings from all completed matches...")
    completed_matches = db.query(Match).filter(Match.status == "completed").all()

    # Dictionary to accumulate standings
    # Key: (group_name, team_name) -> Dict of stats
    standings_map = {}

    def get_team_stats(group_name, team_name):
        key = (group_name, team_name)
        if key not in standings_map:
            standings_map[key] = {
                "played": 0, "won": 0, "drawn": 0, "lost": 0,
                "goals_for": 0, "goals_against": 0, "points": 0
            }
        return standings_map[key]

    # Process each match
    for match in completed_matches:
        t1_stats = get_team_stats(match.group_name, match.team_1)
        t2_stats = get_team_stats(match.group_name, match.team_2)

        t1_stats["played"] += 1
        t2_stats["played"] += 1

        t1_stats["goals_for"] += match.score_1
        t1_stats["goals_against"] += match.score_2

        t2_stats["goals_for"] += match.score_2
        t2_stats["goals_against"] += match.score_1

        if match.score_1 > match.score_2:
            t1_stats["won"] += 1
            t1_stats["points"] += 3
            t2_stats["lost"] += 1
        elif match.score_2 > match.score_1:
            t2_stats["won"] += 1
            t2_stats["points"] += 3
            t1_stats["lost"] += 1
        else:
            t1_stats["drawn"] += 1
            t1_stats["points"] += 1
            t2_stats["drawn"] += 1
            t2_stats["points"] += 1

    # Include teams that haven't played yet but are in matches list
    all_matches = db.query(Match).all()
    for match in all_matches:
        get_team_stats(match.group_name, match.team_1)
        get_team_stats(match.group_name, match.team_2)

    # Insert into database
    for (group_name, team_name), stats in standings_map.items():
        db_standing = Standings(
            group_name=group_name,
            team_name=team_name,
            played=stats["played"],
            won=stats["won"],
            drawn=stats["drawn"],
            lost=stats["lost"],
            goals_for=stats["goals_for"],
            goals_against=stats["goals_against"],
            points=stats["points"]
        )
        db.add(db_standing)

    db.commit()
    print("Standings seeded successfully!")

if __name__ == "__main__":
    seed_database()
