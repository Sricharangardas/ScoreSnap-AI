import os
import json
import google.generativeai as genai
from typing import Dict, List, Any

# Configure Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY environment variable is not set. Gemini features will run in mock mode.")

class GeminiService:
    _quota_exhausted = False

    @staticmethod
    def get_model():
        return genai.GenerativeModel("gemini-2.5-flash")

    @classmethod
    def _call_gemini_with_retry(cls, prompt: str, generation_config: Dict[str, Any] = None) -> str:
        if cls._quota_exhausted:
            print("[GeminiService] Quota is marked as exhausted. Skipping API call.")
            raise Exception("429 RESOURCE_EXHAUSTED (cached)")

        import time
        import re
        retries = 3
        default_delay = 30
        for attempt in range(retries):
            try:
                model = cls.get_model()
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                return response.text
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    if "limit: 20" in err_msg or "Quota exceeded" in err_msg:
                        print("[GeminiService] Daily quota exceeded (limit: 20). Setting quota_exhausted = True.")
                        cls._quota_exhausted = True
                        raise e
                    if attempt < retries - 1:
                        sleep_time = default_delay
                        try:
                            match = re.search(r"Please retry in (\d+\.?\d*)s", err_msg)
                            if match:
                                sleep_time = float(match.group(1)) + 1.5
                                print(f"[GeminiService] Parsed retry delay from error: {sleep_time:.2f}s")
                        except Exception:
                            pass
                        sleep_time = max(15.0, min(sleep_time, 70.0))
                        print(f"[GeminiService] Rate limit (429) hit. Sleeping for {sleep_time:.2f} seconds before retrying...")
                        time.sleep(sleep_time)
                        continue
                raise e

    @classmethod
    def generate_match_stats(cls, team_1: str, team_2: str, score_1: int, score_2: int) -> Dict[str, Any]:
        """
        Agent 2 - Generates realistic stats and event timeline matching the final score.
        Uses structured JSON response format.
        """
        if not GEMINI_API_KEY:
            # Mock fallback if no API key
            return cls._get_mock_stats(team_1, team_2, score_1, score_2)

        prompt = f"""
        Search for and retrieve the actual details for this real FIFA World Cup 2026 match:
        {team_1} ({score_1}) vs {team_2} ({score_2}).
        
        Retrieve the ACTUAL player names who scored the goals, their scoring minutes, the actual player of the match, and realistic match statistics.
        
        The result must strictly have {team_1} scoring {score_1} goal(s) and {team_2} scoring {score_2} goal(s).
        Return the response in JSON format matching this schema:
        {{
            "possession_1": int (possession percentage for team 1, e.g. 55),
            "possession_2": int (possession percentage for team 2, e.g. 45, must sum to 100),
            "shots_1": int,
            "shots_2": int,
            "shots_on_target_1": int (must be <= shots_1),
            "shots_on_target_2": int (must be <= shots_2),
            "corners_1": int,
            "corners_2": int,
            "yellow_cards_1": int,
            "yellow_cards_2": int,
            "red_cards_1": int,
            "red_cards_2": int,
            "expected_goals_1": float (e.g. 1.45),
            "expected_goals_2": float (e.g. 0.95),
            "player_of_the_match": "string (name of the standout player)",
            "scorers": [
                {{"team": "string", "player": "string", "minute": int}}
            ],
            "assists": [
                {{"team": "string", "player": "string", "minute": int}}
            ]
        }}
        """
        try:
            response_text = cls._call_gemini_with_retry(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response_text)
        except Exception as e:
            print(f"Error calling Gemini for match stats: {e}")
            return cls._get_mock_stats(team_1, team_2, score_1, score_2)

    @classmethod
    def generate_match_analysis(cls, match_data: Dict[str, Any], language: str = "English") -> Dict[str, Any]:
        """
        Agent 3 - Generates the AI-powered summary, storylines, turning points,
        tactical analysis, and tournament impact in the requested language.
        """
        if not GEMINI_API_KEY:
            return cls._get_mock_analysis(match_data, language)

        prompt = f"""
        You are a world-class football analyst. Analyze the following completed World Cup 2026 match:
        Match Details: {match_data['team_1']} ({match_data['score_1']}) vs {match_data['team_2']} ({match_data['score_2']})
        Stadium: {match_data.get('stadium', 'World Cup Stadium')}
        Group: {match_data.get('group_name', 'Group Stage')}
        Stats: {json.dumps(match_data.get('stats_json', {}))}

        Please write the analysis in {language}.
        The summary must be engaging, fan-friendly, and professional.
        Return the analysis in JSON format with these exact keys:
        {{
            "ai_summary": "150 to 250 words describing the flow of the match, key moments, and final outcome",
            "storyline": "A short narrative title/hook summarizing the match theme",
            "turning_points": "The single most critical event/minute that changed the outcome",
            "tactical_analysis": "2-3 sentences analyzing how both managers setup and key tactical patterns",
            "best_player": "Detailed breakdown of the player of the match's performance",
            "tournament_impact": "How this result reshapes group standings or knockout qualifications"
        }}
        """
        try:
            response_text = cls._call_gemini_with_retry(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response_text)
        except Exception as e:
            print(f"Error calling Gemini for match analysis: {e}")
            return cls._get_mock_analysis(match_data, language)

    @classmethod
    def generate_daily_digest(cls, completed_matches: List[Dict[str, Any]], standings_summary: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Agent 6 - Generates a comprehensive morning digest report.
        """
        if not GEMINI_API_KEY:
            return cls._get_mock_digest(completed_matches)

        prompt = f"""
        You are a football digest editor. Create the morning digest briefing for the World Cup 2026.
        Matches completed in last 24h: {json.dumps(completed_matches)}
        Current Standings state: {json.dumps(standings_summary)}

        Generate a premium morning report. Return in JSON format with these exact keys:
        {{
            "overnight_summary": "2-3 sentences summarizing the action overnight",
            "biggest_upset": "Which match was the biggest upset and why",
            "match_of_the_day": "The most thrilling match of the day with high stakes",
            "highest_scoring_match": "The match with the most goals",
            "top_scorers_digest": "Brief update on the Golden Boot race",
            "standings_insight": "How the groups are shaking up",
            "digest_title": "An eye-catching, creative title for today's briefing"
        }}
        """
        try:
            response_text = cls._call_gemini_with_retry(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response_text)
        except Exception as e:
            print(f"Error calling Gemini for daily digest: {e}")
            return cls._get_mock_digest(completed_matches)

    @classmethod
    def generate_prediction(cls, team_1: str, team_2: str, head_to_head: str = "") -> Dict[str, Any]:
        """
        Advanced Feature - Predicts the score and tactical overview of an upcoming match.
        """
        if not GEMINI_API_KEY:
            return {
                "predicted_score": f"{team_1} 2 - 1 {team_2}",
                "confidence": "72%",
                "key_battle": "Midfield control and transition speed.",
                "analysis": f"A tight tactical match is expected. {team_1} has an edge in squad depth, but {team_2} is highly organized defensively."
            }

        prompt = f"""
        Provide an AI-powered prediction for the upcoming World Cup 2026 fixture:
        {team_1} vs {team_2}.
        {f"Head-to-head history: {head_to_head}" if head_to_head else ""}

        Return your output in JSON format with these exact keys:
        {{
            "predicted_score": "string (e.g. France 2 - 1 Italy)",
            "confidence": "string (e.g. 65%)",
            "key_battle": "string (describing the key match-up on the pitch)",
            "analysis": "2-3 sentences analyzing team form, tactics, and why you predicted this outcome"
        }}
        """
        try:
            response_text = cls._call_gemini_with_retry(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response_text)
        except Exception as e:
            print(f"Error calling Gemini for prediction: {e}")
            return {
                "predicted_score": f"{team_1} 1 - 1 {team_2}",
                "confidence": "50%",
                "key_battle": "Attacking efficiency.",
                "analysis": "Both teams are evenly matched. A draw is the most statistical outcome."
            }

    @staticmethod
    def _get_mock_stats(team_1: str, team_2: str, score_1: int, score_2: int) -> Dict[str, Any]:
        scorers = []
        for i in range(score_1):
            scorers.append({"team": team_1, "player": f"Star Player {i+1}", "minute": 15 + i * 25})
        for i in range(score_2):
            scorers.append({"team": team_2, "player": f"Forward {i+1}", "minute": 20 + i * 30})
        
        return {
            "possession_1": 53,
            "possession_2": 47,
            "shots_1": 12 + score_1,
            "shots_2": 9 + score_2,
            "shots_on_target_1": 5 + score_1,
            "shots_on_target_2": 3 + score_2,
            "corners_1": 6,
            "corners_2": 4,
            "yellow_cards_1": 1,
            "yellow_cards_2": 2,
            "red_cards_1": 0,
            "red_cards_2": 0,
            "expected_goals_1": round(score_1 + 0.35, 2),
            "expected_goals_2": round(score_2 + 0.12, 2),
            "player_of_the_match": scorers[0]["player"] if scorers else "No Scorers",
            "scorers": scorers,
            "assists": [{"team": s["team"], "player": f"Midfielder {idx+1}", "minute": s["minute"]} for idx, s in enumerate(scorers)]
        }

    @staticmethod
    def _get_mock_analysis(match_data: Dict[str, Any], language: str = "English") -> Dict[str, Any]:
        t1, t2 = match_data['team_1'], match_data['team_2']
        s1, s2 = match_data['score_1'], match_data['score_2']
        winner = t1 if s1 > s2 else (t2 if s2 > s1 else "Draw")
        
        summary_en = f"An absolute thriller at the World Cup! {t1} battled {t2} in an intense affair that concluded {s1}-{s2}. Both sides demonstrated high pressing and tactical prowess. {winner if winner != 'Draw' else 'The share of points'} was well-deserved, reflecting the incredible effort on display. Fans witnessed a tactical masterclass with spectacular goals."
        
        # Simple translation simulation for demo
        summary = summary_en
        if language.lower() == "hindi":
            summary = f"विश्व कप में एक रोमांचक मुकाबला! {t1} और {t2} के बीच जोरदार टक्कर हुई जिसका अंत {s1}-{s2} के स्कोर पर हुआ। दोनों टीमों ने शानदार खेल दिखाया और यह मैच प्रशंसकों के लिए यादगार रहेगा।"
        elif language.lower() == "spanish":
            summary = f"¡Un absoluto partidazo en la Copa del Mundo! {t1} se enfrentó a {t2} en un duelo intenso que terminó {s1}-{s2}. Ambos equipos demostraron un gran nivel táctico."

        return {
            "ai_summary": summary,
            "storyline": f"Clash of Giants: {t1} vs {t2}",
            "turning_points": "Late tactical substitution at 75th minute that shored up midfield defenses.",
            "tactical_analysis": f"{t1} utilized a heavy 4-3-3 counter-pressing style, while {t2} sat back in a compact 4-4-2 low block.",
            "best_player": f"Standout display of distribution, tactical awareness, and clinical execution.",
            "tournament_impact": f"This crucial result shifts points in the group, setting up a final matchday showdown."
        }

    @staticmethod
    def _get_mock_digest(completed_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        match_count = len(completed_matches)
        return {
            "overnight_summary": f"A busy night of World Cup action saw {match_count} match(es) completed with dramatic scores and critical shifts in the groups.",
            "biggest_upset": "No massive upsets recorded, but teams showed resilient tactical performances across the board.",
            "match_of_the_day": "The matches featured end-to-end action, keeping fans glued to their screens late into the night.",
            "highest_scoring_match": "The matches generated excitement, showcasing top attacking talent.",
            "top_scorers_digest": "Strikers are hitting form early, establishing solid goals tallies in the Golden Boot race.",
            "standings_insight": "The standings are tightening, leaving group qualification wide open for the final round.",
            "digest_title": "ScoreSnap World Cup Morning Wrap-Up"
        }
