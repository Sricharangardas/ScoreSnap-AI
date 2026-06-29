from sqlalchemy.orm import Session
from database.models import Match, Standings

class StandingsAgent:
    @staticmethod
    def update_standings(db: Session) -> None:
        """
        Agent 5 - Updates team standings automatically based on all completed matches.
        """
        print("Recalculating group standings...")
        
        # Fetch all completed matches
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

        # Process stats from completed matches
        for match in completed_matches:
            if "group" not in match.group_name.lower():
                continue
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

        # Also pull in any teams scheduled but who haven't played, to ensure they appear in tables
        all_matches = db.query(Match).all()
        for match in all_matches:
            if "group" not in match.group_name.lower():
                continue
            get_team_stats(match.group_name, match.team_1)
            get_team_stats(match.group_name, match.team_2)

        # Clear existing standings table entries
        db.query(Standings).delete()
        db.commit()

        # Insert new updated standings
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
        print("Group standings updated successfully.")
