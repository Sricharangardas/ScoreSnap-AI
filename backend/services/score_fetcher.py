import os
import json
import datetime
import google.generativeai as genai
from typing import Dict, Any, Optional

from dotenv import load_dotenv

try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        DDGS = None

# Load environment variables
load_dotenv()

# Configure Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class ScoreFetcher:
    @staticmethod
    def get_real_match_score(team_1: str, team_2: str, match_date: datetime.datetime) -> Optional[Dict[str, Any]]:
        """
        Uses DuckDuckGo search + Gemini 3.5 to fetch and parse the real-world score of a match.
        Returns a dict:
        {
            "match_completed": bool,
            "score_1": int or None,
            "score_2": int or None,
            "explanation": str
        }
        or None if parsing failed.
        """
        if not GEMINI_API_KEY:
            print("[ScoreFetcher] GEMINI_API_KEY not configured. Cannot query Gemini for real-world scores.")
            return None

        if DDGS is None:
            print("[ScoreFetcher] duckduckgo-search package is not installed.")
            return None

        # Format match date for query, e.g. "June 14, 2026"
        date_str = match_date.strftime("%B %d, %Y")
        query = f"FIFA World Cup 2026 {team_1} vs {team_2} score {date_str}"
        print(f"[ScoreFetcher] Searching DuckDuckGo: '{query}'")

        snippets = []
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                for r in results:
                    snippets.append(f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
        except Exception as e:
            print(f"[ScoreFetcher] DuckDuckGo search error: {e}")
            return None

        search_text = "\n\n".join(snippets)
        if not search_text:
            print("[ScoreFetcher] No search results returned from DuckDuckGo.")
            return {
                "match_completed": False,
                "score_1": None,
                "score_2": None,
                "explanation": "No search results found to verify completion."
            }

        prompt = f"""
You are a soccer statistics parser. We need to extract the actual score of the FIFA World Cup 2026 match between {team_1} and {team_2} played on/around {date_str}.

Here are the web search results:
{search_text}

Analyze the search results. Determine if this match is completed in the real world, and if so, what the final score is.
Return a JSON object with these exact keys:
- match_completed (bool): True if the match has finished and a final score is available, False otherwise.
- score_1 (int or null): Goals scored by {team_1} (if completed).
- score_2 (int or null): Goals scored by {team_2} (if completed).
- explanation (str): Brief reason for the score extraction.

Respond ONLY with the raw JSON object, no markdown formatting blocks, no ```json tags.
"""
        try:
            # Using gemini-2.5-flash which is active and has quota on your key
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
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
            print(f"[ScoreFetcher] Gemini parsing error: {e}")
            return None
