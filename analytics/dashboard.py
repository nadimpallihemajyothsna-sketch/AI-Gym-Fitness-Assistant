import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fitness Analytics",
    layout="wide"
)

# TITLE
st.title("Fitness Analytics Dashboard")

st.write("Monitor workout performance and calorie tracking")

# SAMPLE DATA
data = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Calories Burned": [250, 320, 280, 400, 360, 500, 450],
    "Workout Hours": [1, 1.5, 1, 2, 1.5, 2, 2]
}

df = pd.DataFrame(data)

# METRICS
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

# CALORIES GRAPH
st.subheader("Weekly Calories Burned")

fig1 = px.line(
    df,
    x="Day",
    y="Calories Burned",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# WORKOUT GRAPH
st.subheader("Workout Duration")

fig2 = px.bar(
    df,
    x="Day",
    y="Workout Hours"
)

st.plotly_chart(fig2, use_container_width=True)

# DATA TABLE
st.subheader("Fitness Data")

st.dataframe(
    df,
    use_container_width=True
)