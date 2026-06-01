import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Page setup
st.set_page_config(
    page_title="FitAI Assistant",
    layout="wide"
)

st.title("FitAI Assistant")

st.write("Your intelligent fitness companion")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
prompt = st.chat_input("Ask a fitness question...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # TRY GEMINI FIRST
    try:

        response = model.generate_content(
            f"""
            You are a professional fitness trainer and nutrition expert.

            Answer this user query:
            {prompt}
            """
        )

        ai_response = response.text

    # IF GEMINI FAILS → USE LOCAL RESPONSES
    except:

        if "fat loss" in prompt.lower():

            ai_response = """
            ## Beginner Fat Loss Diet Plan

            ### Breakfast
            • Oats with banana and almonds
            • 2 boiled eggs
            • Green tea

            ### Mid-Morning Snack
            • Apple or orange
            • Handful of nuts

            ### Lunch
            • Grilled chicken or paneer
            • Brown rice
            • Mixed vegetables
            • Salad

            ### Evening Snack
            • Protein shake or sprouts
            • Black coffee or green tea

            ### Dinner
            • Soup with vegetables
            • Grilled fish/paneer
            • Salad

            ### Before Sleep
            • Warm milk or Greek yogurt

            ## Workout Recommendations
            • 30 min walking or cardio
            • Strength training 4 days/week
            • Drink 3 liters water daily

            ## Important Tips
            • Avoid sugary drinks
            • Reduce junk food
            • Sleep 7-8 hours daily
            • Maintain calorie deficit
            """

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    # Show assistant response
    with st.chat_message("assistant"):
        st.write(ai_response)