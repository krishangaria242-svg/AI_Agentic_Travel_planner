import streamlit as st
import os
import urllib.parse
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("✈️ AI Travel Planner")
st.sidebar.write("Made by Krish ❤️")
st.sidebar.write("---")
st.sidebar.info(
    "Generate complete AI-powered travel plans with hotels, food, weather and maps."
)

# -------------------------
# Title
# -------------------------
st.title("✈️ AI Travel Planner")
st.write("Plan your dream trip using Gemini AI")

# -------------------------
# Inputs
# -------------------------
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

interest_text = ", ".join(interests) if interests else "General Tourism"

# -------------------------
# Generate Plan
# -------------------------
if st.button("Generate Travel Plan"):

    if location.strip() == "":
        st.warning("Please enter a destination.")

    else:

        prompt = f"""
You are an expert travel planner.

Create a detailed {days}-day travel itinerary.

Destination: {location}

Budget: {budget}

Interests: {interest_text}

Generate the following sections:

# Day-wise Itinerary

Morning
Afternoon
Evening

# Top Tourist Attractions

# Best Hotels
Mention:
- Hotel Name
- Approx Price/Night
- Best For

# Best Restaurants
Mention:
- Restaurant
- Famous Dish
- Cost for Two

# Local Transportation

# Shopping Places

# Estimated Budget in INR
Hotel
Food
Transport
Shopping
Sightseeing
Total

# Travel Tips

Use proper headings and bullet points.
"""

        with st.spinner("Generating AI Travel Plan..."):

            try:

                response = model.generate_content(prompt)

                st.success("✅ Travel Plan Generated Successfully!")

                st.markdown(response.text)

            except Exception:

                st.error(
                    "Gemini API quota exceeded or API key issue."
                )

        st.divider()

        # -------------------------
        # Weather
        # -------------------------

        st.subheader("🌤️ Live Weather")

        try:

            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"q={location}&appid={WEATHER_API_KEY}&units=metric"
            )

            weather = requests.get(url).json()

            if str(weather.get("cod")) == "200":

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "🌡️ Temperature",
                        f"{weather['main']['temp']} °C"
                    )

                    st.metric(
                        "💧 Humidity",
                        f"{weather['main']['humidity']} %"
                    )

                with col2:

                    st.metric(
                        "🌬️ Wind Speed",
                        f"{weather['wind']['speed']} m/s"
                    )

                    st.metric(
                        "☁️ Condition",
                        weather["weather"][0]["description"].title()
                    )

            else:

                st.warning("Weather information not found.")

        except Exception:

            st.error("Unable to fetch weather.")

        st.divider()

        # -------------------------
        # Google Maps
        # -------------------------

        st.subheader("📍 Open in Google Maps")

        maps_url = (
            "https://www.google.com/maps/search/"
            + urllib.parse.quote(location)
        )

        st.link_button(
            "🗺️ Open Google Maps",
            maps_url
        )

        st.divider()
                # -------------------------
        # Best Time to Visit
        # -------------------------

        st.subheader("📅 Best Time to Visit")

        try:

            best_time_prompt = f"""
Tell the best time to visit {location}.

Include:

- Best months
- Weather
- Festivals
- Peak season
- Off season
- Travel advice

Use bullet points.
"""

            best_time = model.generate_content(best_time_prompt)

            st.markdown(best_time.text)

        except Exception:

            st.warning("Unable to generate Best Time to Visit.")

        st.divider()

        # -------------------------
        # Packing Tips
        # -------------------------

        st.subheader("🎒 Packing Checklist")

        try:

            packing_prompt = f"""
Suggest a packing checklist for a {days}-day trip to {location}.

Consider the weather and common travel needs.

Return only bullet points.
"""

            packing = model.generate_content(packing_prompt)

            st.markdown(packing.text)

        except Exception:

            st.warning("Unable to generate packing tips.")

        st.divider()

        # -------------------------
        # Travel Safety Tips
        # -------------------------

        st.subheader("🛡️ Safety Tips")

        try:

            safety_prompt = f"""
Give important travel safety tips for tourists visiting {location}.

Use short bullet points.
"""

            safety = model.generate_content(safety_prompt)

            st.markdown(safety.text)

        except Exception:

            st.warning("Unable to generate safety tips.")

        st.divider()

        # -------------------------
        # Quick Trip Summary
        # -------------------------

        st.subheader("📋 Quick Trip Summary")

        st.info(
            f"""
📍 Destination : {location}

🗓️ Duration : {days} Days

💰 Budget : {budget}

🎯 Interests : {interest_text}
"""
        )

        st.divider()

        # -------------------------
        # Footer
        # -------------------------

        st.markdown(
            """
---
### ❤️ Thanks for using AI Travel Planner

Made with ❤️ by **Krish**

Powered by **Google Gemini AI** + **OpenWeather API** + **Streamlit**
"""
        )