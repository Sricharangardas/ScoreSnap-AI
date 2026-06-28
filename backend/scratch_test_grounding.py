import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_grounding_score(team_1, team_2, date_str):
    prompt = f"""
You are a soccer statistics parser. We need to extract the actual score of the FIFA World Cup 2026 match between {team_1} and {team_2} played on/around {date_str}.

Determine if this match is completed in the real world, and if so, what the final score is.
Return a JSON object with these exact keys:
- match_completed (bool): True if the match has finished and a final score is available, False otherwise.
- score_1 (int or null): Goals scored by {team_1} (if completed).
- score_2 (int or null): Goals scored by {team_2} (if completed).
- explanation (str): Brief reason for the score extraction.

Respond ONLY with the raw JSON object, no markdown formatting blocks, no ```json tags.
"""
    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            tools='google_search_retrieval'
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()
        elif text.startswith("```"):
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    res = test_grounding_score("Spain", "Saudi Arabia", "June 21, 2026")
    print("Result:")
    print(res)
