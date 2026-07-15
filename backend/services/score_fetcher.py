import os
import json
import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ScoreFetcher:
    _quota_exhausted = False

    @staticmethod
    def get_real_match_score(team_1: str, team_2: str, match_date: datetime.datetime) -> Optional[Dict[str, Any]]:
        """
        Uses Google Search Grounding via Gemini 2.5 to fetch and parse the real-world score of a match.
        Returns a dict:
        {
            "match_completed": bool,
            "score_1": int or None,
            "score_2": int or None,
            "explanation": str
        }
        or None if parsing failed.
        """
        if ScoreFetcher._quota_exhausted:
            print("[ScoreFetcher] Quota is marked as exhausted. Skipping API call.")
            return None

        if not GEMINI_API_KEY:
            print("[ScoreFetcher] GEMINI_API_KEY not configured. Cannot query Gemini for real-world scores.")
            return None

        # Format match date for query, e.g. "June 14, 2026"
        date_str = match_date.strftime("%B %d, %Y")
        
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
You are a soccer statistics parser. We need to extract the actual score of the FIFA World Cup 2026 match between {team_1} and {team_2} played on/around {date_str}.

Determine if this match is completed in the real world, and if so, what the final score and winner is.
Return a JSON object with these exact keys:
- match_completed (bool): True if the match has finished and a final score is available, False otherwise.
- score_1 (int or null): Goals scored by {team_1} (if completed).
- score_2 (int or null): Goals scored by {team_2} (if completed).
- winner (str or null): The exact team name of the winner who advanced/won the match (if completed). If the match ended in a draw but was decided by a penalty shootout, this must be the team that won the penalty shootout.
- explanation (str): Brief reason for the score extraction.

Respond ONLY with the raw JSON object, no markdown formatting blocks, no ```json tags.
"""
        import time
        import re
        retries = 3
        default_delay = 30
        for attempt in range(retries):
            try:
                print(f"[ScoreFetcher] Querying Gemini with Search Grounding (Attempt {attempt+1}/{retries}): {team_1} vs {team_2} on {date_str}")
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                text = response.text.strip()
                
                # Clean up any potential markdown fences
                if text.startswith("```json"):
                    text = text.split("```json")[1].split("```")[0].strip()
                elif text.startswith("```"):
                    text = text.split("```")[1].split("```")[0].strip()
                    
                data = json.loads(text)
                print(f"[ScoreFetcher] Parsed response from Gemini: {data}")
                return data
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    if "limit: 20" in err_msg or "Quota exceeded" in err_msg:
                        print("[ScoreFetcher] Daily quota exceeded (limit: 20). Setting quota_exhausted = True.")
                        ScoreFetcher._quota_exhausted = True
                        return None
                    if attempt < retries - 1:
                        sleep_time = default_delay
                        try:
                            match = re.search(r"Please retry in (\d+\.?\d*)s", err_msg)
                            if match:
                                sleep_time = float(match.group(1)) + 1.5
                                print(f"[ScoreFetcher] Parsed retry delay from error: {sleep_time:.2f}s")
                        except Exception:
                            pass
                        sleep_time = max(15.0, min(sleep_time, 70.0))
                        print(f"[ScoreFetcher] Rate limit (429) hit. Sleeping for {sleep_time:.2f} seconds before retrying...")
                        time.sleep(sleep_time)
                        continue
                print(f"[ScoreFetcher] Gemini parsing error: {e}")
                return None

