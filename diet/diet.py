import streamlit as st

st.set_page_config(
    page_title="Nutrition Intelligence",
    layout="wide"
)

st.title("Nutrition Intelligence")

st.write("Personalized diet and BMI analysis")

# User Inputs
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

# ANALYZE BUTTON
if st.button("Analyze"):

    # BMI Calculation
    bmi = weight / (height ** 2)

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

    # SMART RECOMMENDATIONS
    st.markdown("## Personalized Recommendations")

    # UNDERWEIGHT CASE
    if bmi < 18.5:

        st.warning("""
        Your BMI indicates underweight.

        Fat loss is not recommended currently.
        Focus on healthy weight gain and balanced nutrition.
        """)

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

    # OTHER BMI CASES
    else:

        if goal == "Fat Loss":

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