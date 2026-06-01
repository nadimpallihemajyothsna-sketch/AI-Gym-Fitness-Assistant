import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

from groq import Groq

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Gym & Fitness Assistant",
    page_icon="🏋",
    layout="wide",
    initial_sidebar_state="expanded"
)

client = Groq(
    api_key="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"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
}

[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown("""
<h1 style='text-align:center; color:#4CAF50;'>
🏋️ AI Gym & Fitness Assistant
</h1>
<h4 style='text-align:center;'>
Personalized Workout & Fitness Guidance Using AI
</h4>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏋 FitAI")
st.sidebar.caption("AI-powered Fitness Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Login",
        "AI Chatbot",
        "Nutrition",
        "Workout Logger",
        "Workout History",
        "Fitness Habit Tracker",
        "AI Gym Planner",
        "Performance Score",
        "Analytics",
        "BMI History"
    ]
)

# =========================
# USER SESSION
# =========================
if "logged_in" in st.session_state:

    st.sidebar.success(
        f"Logged in as: {st.session_state['username']}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()

# =========================
# HOME PAGE
# =========================
if page == "Home":

    st.markdown("""
       ## Train Smarter. Perform Better.

       An AI-powered fitness ecosystem designed to help users improve health, track performance, and achieve fitness goals.

       ### 🚀 Key Features

       ✅ AI Fitness Chatbot

       ✅ Nutrition Intelligence & BMI Analysis

       ✅ Workout Logger & History

       ✅ Fitness Habit Tracker

       ✅ AI Gym Planner

       ✅ Analytics Dashboard

       ✅ User Authentication

       ✅ Progress Tracking
    """)
    col1, col2, col3 = st.columns(3)

    with col1:
       st.metric("Workouts Available", "50+")
    
    with col2:
       st.metric("Fitness Categories", "10+")

    with col3:
      st.metric("AI Assistance", "24/7")

    st.markdown("---")

    feature1, feature2 = st.columns(2)

    with feature1:
        st.info("🤖 AI Fitness Chatbot")
        st.info("🥗 Nutrition Intelligence")

    with feature2:
        st.info("🏋 Workout Tracking")
        st.info("📈 Analytics Dashboard")

# =========================
# LOGIN PAGE
# =========================
elif page == "Login":

    st.title("FitAI Authentication")

    conn = sqlite3.connect("fitness.db")
    c = conn.cursor()

    menu = ["Login", "Sign Up"]

    choice = st.selectbox(
        "Select Option",
        menu
    )

    # LOGIN
    if choice == "Login":

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )

            data = c.fetchone()

            if data:

                st.session_state["logged_in"] = True
                st.session_state["username"] = username

                st.success(f"Welcome {username}")

            else:
                st.error("Invalid Username or Password")

    # SIGNUP
    else:

        new_user = st.text_input("Create Username")

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Create Account"):

            c.execute(
                "INSERT INTO users(username, password) VALUES(?, ?)",
                (new_user, new_password)
            )

            conn.commit()

            st.success("Account Created Successfully")

    conn.close()

# =========================
# AI CHATBOT PAGE
# =========================
elif page == "AI Chatbot":

    st.title("FitAI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask a fitness question...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

                # AI RESPONSE
        try:

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional fitness trainer and nutrition expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )

            ai_response = completion.choices[0].message.content

        except Exception as e:

            ai_response = f"Error: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })

        with st.chat_message("assistant"):
            st.write(ai_response)

# =========================
# NUTRITION PAGE
# =========================
elif page == "Nutrition":

    st.title("Nutrition Intelligence")

    weight = st.number_input(
        "Enter Weight (kg)",
        min_value=20.0
    )

    height_cm = st.number_input(
        "Enter Height (cm)",
        min_value=50.0
    )

    height = height_cm / 100

    age = st.number_input(
        "Enter Age",
        min_value=10
    )

    goal = st.selectbox(
        "Select Fitness Goal",
        ["Fat Loss", "Muscle Gain", "Maintain Fitness"]
    )

    if st.button("Analyze"):

        bmi = weight / (height ** 2)

        # SAVE BMI HISTORY
        if "username" in st.session_state:

            conn = sqlite3.connect("fitness.db")
            c = conn.cursor()

            c.execute(
                "INSERT INTO bmi_history(username, bmi, goal) VALUES(?, ?, ?)",
                (
                    st.session_state["username"],
                    bmi,
                    goal
                )
            )

            conn.commit()
            conn.close()

        st.metric("BMI Score", f"{bmi:.2f}")

        # BMI CATEGORY
        if bmi < 18.5:
            st.error("Underweight")

        elif bmi < 25:
            st.success("Healthy Weight Range")

        elif bmi < 30:
            st.warning("Above Healthy Weight Range")

        else:
            st.error("Obese")

        # RECOMMENDATIONS
        st.markdown("## Personalized Recommendations")

        # UNDERWEIGHT
        if bmi < 18.5:

            st.markdown("""
            ### Healthy Weight Gain Plan

            • Increase calorie intake
            • Eat protein-rich foods
            • Strength training
            • Sleep 7-8 hours

            #### Recommended Foods
            - Milk
            - Banana
            - Rice
            - Peanut butter
            - Eggs
            - Paneer
            """)

        # FAT LOSS
        elif goal == "Fat Loss":

            st.markdown("""
            ### Fat Loss Plan

            • High protein diet
            • Calorie deficit
            • Avoid sugary foods
            • Cardio 4-5 days/week
            • Drink 3L water daily

            #### Recommended Foods
            - Eggs
            - Chicken breast
            - Oats
            - Fruits
            - Vegetables
            """)

        # MUSCLE GAIN
        elif goal == "Muscle Gain":

            st.markdown("""
            ### Muscle Gain Plan

            • Increase protein intake
            • Strength training
            • Calorie surplus
            • Proper sleep and recovery

            #### Recommended Foods
            - Rice
            - Chicken
            - Fish
            - Peanut butter
            - Milk
            """)

        # MAINTENANCE
        else:

            st.markdown("""
            ### Maintenance Plan

            • Balanced nutrition
            • Moderate exercise
            • Hydration
            • Proper sleep

            #### Recommended Foods
            - Fruits
            - Vegetables
            - Whole grains
            - Lean protein
            """)

# =========================
# WORKOUT LOGGER
# =========================
elif page == "Workout Logger":

    st.title("🏋 Workout Logger")

    exercise = st.text_input("Exercise Name")

    sets = st.number_input(
        "Sets",
        min_value=1,
        value=3
    )

    reps = st.number_input(
        "Reps",
        min_value=1,
        value=10
    )

    duration = st.number_input(
        "Duration (minutes)",
        min_value=1,
        value=30
    )

    if st.button("Save Workout"):

        if "username" in st.session_state:

            conn = sqlite3.connect("fitness.db")
            c = conn.cursor()

            c.execute(
                """
                INSERT INTO workouts
                VALUES(?,?,?,?,?)
                """,
                (
                    st.session_state["username"],
                    exercise,
                    sets,
                    reps,
                    duration
                )
            )

            conn.commit()
            conn.close()

            st.success("Workout Saved Successfully")

        else:

            st.error("Please login first.")

# =========================
# WORKOUT HISTORY
# =========================
elif page == "Workout History":

    st.title("📈 Workout History")

    if "username" in st.session_state:

        conn = sqlite3.connect("fitness.db")
        c = conn.cursor()

        c.execute(
            """
            SELECT exercise, sets, reps, duration
            FROM workouts
            WHERE username=?
            """,
            (st.session_state["username"],)
        )

        records = c.fetchall()

        conn.close()

        if records:

            workout_df = pd.DataFrame(
                records,
                columns=[
                    "Exercise",
                    "Sets",
                    "Reps",
                    "Duration"
                ]
            )

            st.dataframe(
                workout_df,
                use_container_width=True
            )

            st.subheader("Workout Duration Progress")

            st.bar_chart(
                workout_df["Duration"]
            )

        else:

            st.warning(
                "No workout history found."
            )

    else:

        st.error(
            "Please login first."
        )

# =========================
# FITNESS HABIT TRACKER
# =========================
elif page == "Fitness Habit Tracker":

    st.title("🔥 Fitness Habit Tracker")

    workout_days = st.slider(
        "How many days did you workout this week?",
        0,
        7,
        3
    )

    st.metric(
        "Workout Days",
        f"{workout_days}/7"
    )

    if workout_days >= 6:

        st.success(
            "Excellent consistency! Keep it up."
        )

    elif workout_days >= 4:

        st.info(
            "Good progress. Stay consistent."
        )

    elif workout_days >= 2:

        st.warning(
            "You missed several workouts this week."
        )

    else:

        st.error(
            "Low activity detected. Let's get moving!"
        )

    # AI Motivation
    if workout_days < 4:

        st.markdown(
            """
            ### AI Motivation

            Consistency beats intensity.

            Try scheduling shorter workouts
            and focus on building a habit.
            """
        )

    else:

        st.markdown(
            """
            ### AI Motivation

            Great job staying active.

            Continue progressing and
            challenge yourself gradually.
            """
        )

# =========================
# AI GYM PLANNER
# =========================
elif page == "AI Gym Planner":

    st.title("🏋 AI Gym Planner")

    goal = st.selectbox(
        "Select Your Goal",
        [
            "Fat Loss",
            "Muscle Gain",
            "General Fitness"
        ]
    )

    if st.button("Generate Plan"):

        if goal == "Fat Loss":

            st.markdown("""
            ## Weekly Fat Loss Plan

            Monday - Cardio + Abs

            Tuesday - Chest + Triceps

            Wednesday - HIIT Workout

            Thursday - Back + Biceps

            Friday - Legs

            Saturday - Full Body Circuit

            Sunday - Active Recovery
            """)

        elif goal == "Muscle Gain":

            st.markdown("""
            ## Weekly Muscle Gain Plan

            Monday - Chest

            Tuesday - Back

            Wednesday - Legs

            Thursday - Shoulders

            Friday - Arms

            Saturday - Full Body

            Sunday - Rest
            """)

        else:

            st.markdown("""
            ## General Fitness Plan

            Monday - Walking + Stretching

            Tuesday - Upper Body

            Wednesday - Cardio

            Thursday - Lower Body

            Friday - Core Workout

            Saturday - Outdoor Activity

            Sunday - Recovery
            """)

# =========================
# PERFORMANCE SCORE
# =========================
elif page == "Performance Score":

    st.title("🏆 Performance Score Analyzer")

    workout_days = st.slider(
        "Workout Days per Week",
        0,
        7,
        3
    )

    bmi_status = st.selectbox(
        "BMI Status",
        [
            "Underweight",
            "Normal",
            "Overweight",
            "Obese"
        ]
    )

    duration = st.number_input(
        "Weekly Workout Duration (minutes)",
        min_value=0,
        value=150
    )

    if st.button("Calculate Score"):

        score = 0

        # Workout Days
        score += workout_days * 10

        # Duration
        score += min(duration // 10, 20)

        # BMI
        if bmi_status == "Normal":
            score += 20

        elif bmi_status == "Overweight":
            score += 10

        elif bmi_status == "Underweight":
            score += 10

        score = min(score, 100)

        st.metric(
            "Performance Score",
            f"{score}/100"
        )

        if score >= 80:

            st.success(
                "Excellent Fitness Performance"
            )

        elif score >= 60:

            st.info(
                "Good Progress. Keep Going!"
            )

        elif score >= 40:

            st.warning(
                "Average Performance. Improve Consistency."
            )

        else:

            st.error(
                "Low Performance Score. Increase Activity."
            )

# =========================
# ANALYTICS PAGE
# =========================
elif page == "Analytics":

    st.title("Fitness Analytics Dashboard")

    data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Calories Burned": [250, 320, 280, 400, 360, 500, 450],
        "Workout Hours": [1, 1.5, 1, 2, 1.5, 2, 2]
    }

    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Calories Burned",
            f"{df['Calories Burned'].sum()} kcal"
        )

    with col2:
        st.metric(
            "Workout Hours",
            f"{df['Workout Hours'].sum()} hrs"
        )

    fig1 = px.line(
        df,
        x="Day",
        y="Calories Burned",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        df,
        x="Day",
        y="Workout Hours"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# BMI HISTORY PAGE
# =========================
elif page == "BMI History":

    st.title("BMI Progress History")

    if "username" in st.session_state:

        conn = sqlite3.connect("fitness.db")
        c = conn.cursor()

        c.execute(
            "SELECT bmi, goal FROM bmi_history WHERE username=?",
            (st.session_state["username"],)
        )

        records = c.fetchall()

        conn.close()

        if records:

            history_df = pd.DataFrame(
                records,
                columns=["BMI", "Goal"]
            )

            history_df.index = [
                f"Record {i+1}"
                for i in range(len(history_df))
            ]

            st.dataframe(
                history_df,
                use_container_width=True
            )

            st.line_chart(history_df["BMI"])

        else:

            st.warning("No BMI history found.")

    else:

        st.error("Please login first.")