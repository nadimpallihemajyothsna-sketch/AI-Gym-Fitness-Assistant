import streamlit as st

st.set_page_config(
    page_title="Workout Tracking",
    layout="wide"
)

st.title("AI Workout Tracking")

picture = st.camera_input("Open Camera")

if picture:
    st.image(picture)