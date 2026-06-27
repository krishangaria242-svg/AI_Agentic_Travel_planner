import streamlit as st
import os
import urllib.parse
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load Environment Variables
load_dotenv()
weather_api = os.getenv("WEATHER_API_KEY")

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Settings
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

# Sidebar
st.sidebar.title("✈️ AI Travel Planner")
st.sidebar.write("Made by Krish")
st.sidebar.write("---")
st.sidebar.info(
    "Enter your destination, budget and interests to generate a complete AI travel plan."
)

# Main Title
st.title("✈️ AI Travel Planner")
st.write("Plan your trip with Gemini AI")

# Inputs
location = st.text_input("📍 Enter Destination")

days = st.number_input(
    "🗓️ Number of Days",
    min_value=1,
    max_value=30,
    value=3
)

budget = st.selectbox(
    "💰 Select Budget",
    ["Low", "Medium", "High"]
)

interests = st.multiselect(
    "🎯 Select Your Interests",
    [
        "Adventure",
        "Nature",
        "Food",
        "History",
        "Shopping",
        "Photography",
        "Nightlife"
    ]
)

# Button
if st.button("Generate Travel Plan"):

    if location.strip() == "":
        st.warning("Please enter a destination.")

    else:

        prompt = f"""
Create a detailed {days}-day travel itinerary.

Destination: {location}
Budget: {budget}
Interests: {", ".join(interests)}

Include:

1. Day-wise itinerary
2. Famous tourist places
3. Best local food
4. Estimated budget in INR
5. Transportation
6. Hotel recommendations
7. Shopping places
8. Travel tips

Format everything using headings and bullet points.
"""

        with st.spinner("Generating Travel Plan..."):
            response = model.generate_content(prompt)

        st.success("✅ Travel Plan Generated Successfully!")

        st.markdown(response.text)
        st.divider()

st.subheader("🏨 Recommended Hotels")

hotel_prompt = f"""
Suggest 5 best hotels in {location}.

For each hotel provide:
- Hotel Name
- Approximate price per night in INR
- Best for (Family/Couple/Budget/Luxury)
"""

hotel_response = model.generate_content(hotel_prompt)

st.markdown(hotel_response.text)
st.divider()

st.subheader("🍽️ Best Restaurants")

food_prompt = f"""
Suggest 5 famous restaurants in {location}.

Include:
- Restaurant Name
- Famous Dish
- Approximate Cost for Two
"""

food_response = model.generate_content(food_prompt)

st.markdown(food_response.text)
st.divider()

st.subheader("💰 Estimated Trip Budget")

budget_prompt = f"""
Estimate the total budget for a {days}-day trip to {location}.

Budget Type: {budget}

Provide the estimate in INR in a table with:

- Hotel
- Food
- Local Transport
- Sightseeing
- Shopping
- Total Estimated Cost
"""

budget_response = model.generate_content(budget_prompt)

st.markdown(budget_response.text)
st.divider()

st.subheader("🌤️ Live Weather")

url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api}&units=metric"

try:
    weather = requests.get(url).json()

    if weather["cod"] == 200:

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🌡️ Temperature", f"{weather['main']['temp']} °C")
            st.metric("💧 Humidity", f"{weather['main']['humidity']} %")

        with col2:
            st.metric("🌬️ Wind Speed", f"{weather['wind']['speed']} m/s")
            st.metric("☁️ Weather", weather['weather'][0]['description'])

    else:
        st.warning("Weather data not found.")

except Exception:
    st.error("Unable to fetch weather.")

    st.divider()

    st.subheader("📍 Open Destination in Google Maps")

    maps_url = (
        f"https://www.google.com/maps/search/"
        f"{urllib.parse.quote(location)}"
    )

    st.link_button(
        "🗺️ Open in Google Maps",
        maps_url
        )