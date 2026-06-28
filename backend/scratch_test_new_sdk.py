import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    print("Sending search grounding request using new SDK...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="What is the final score of the match Spain vs Saudi Arabia played on June 21, 2026?",
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
