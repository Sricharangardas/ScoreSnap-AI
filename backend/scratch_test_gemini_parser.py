import os
import json
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_match_score(team_1, team_2, match_date_str):
    query = f"{team_1} vs {team_2} World Cup 2026 score {match_date_str}"
    print(f"Searching web for: {query}")
    
    snippets = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            for r in results:
                snippets.append(f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
    except Exception as e:
        print(f"Search error: {e}")
        return None

    search_text = "\n\n".join(snippets)
    
    prompt = f"""
You are a football statistics parser. We need to extract the actual score of the FIFA World Cup 2026 match between {team_1} and {team_2} played on/around {match_date_str}.

Here are the web search results:
{search_text}

Analyze the search results. Determine if this match is completed, and if so, what the final score is.
Return a JSON object with these keys:
- match_completed (bool): True if the match has finished and a final score is available, False otherwise.
- score_1 (int or null): Goals scored by {team_1} (if completed).
- score_2 (int or null): Goals scored by {team_2} (if completed).
- confidence (str): 'high', 'medium', or 'low'.
- explanation (str): Brief reason for the score extraction.

Respond ONLY with the raw JSON object, no markdown formatting blocks, no ```json tags.
"""
    
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean up any potential markdown fences
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()
        elif text.startswith("```"):
            text = text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Gemini parsing error: {e}")
        return None

if __name__ == "__main__":
    score = get_match_score("Germany", "Curaçao", "June 14, 2026")
    print("\nResult:")
    print(score)
