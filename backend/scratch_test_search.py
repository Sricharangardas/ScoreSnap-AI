import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_search():
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash"
        )
        
        prompt = (
            "What was the final score of the FIFA World Cup 2026 match between Germany and Curaçao "
            "played on June 14, 2026? Respond in JSON format with keys: "
            "match_completed (boolean), score_1 (integer for Germany), score_2 (integer for Curaçao)."
        )
        
        print("Sending prompt to Gemini with Google Search grounding...")
        response = model.generate_content(
            prompt,
            tools=[{"google_search_retrieval": {}}]
        )
        print("Response Text:")
        print(response.text)
        
        # Check if grounding metadata exists
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.web_search_queries:
            print("\nSearch Queries Used:")
            print(metadata.web_search_queries)
            print("\nSearch Results (Sources):")
            for chunk in metadata.grounding_chunks:
                print(chunk.web.uri, chunk.web.title)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
