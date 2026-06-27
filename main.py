import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

print("🌍 AI Travel Planner")
print("-" * 30)

destination = input("Enter destination: ")
days = input("Enter number of days: ")

prompt = f"""
Create a detailed travel plan for {days} days to {destination}.
Include:
1. Places to visit
2. Food recommendations
3. Estimated budget
4. Daily itinerary
"""

response = model.generate_content(prompt)

print("\n✈️ Your Travel Plan:\n")
print(response.text)