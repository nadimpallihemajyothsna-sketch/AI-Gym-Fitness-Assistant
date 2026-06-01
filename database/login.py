import streamlit as st

st.set_page_config(
    page_title="FitAI Login",
    layout="centered"
)

st.title("FitAI Authentication")

menu = ["Login", "Sign Up"]

choice = st.selectbox("Select Option", menu)

# LOGIN
if choice == "Login":

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":
            st.success("Login Successful")

        else:
            st.error("Invalid Username or Password")

# SIGNUP
else:

    st.subheader("Create Account")

    new_user = st.text_input("Create Username")
    new_password = st.text_input(
        "Create Password",
        type="password"
    )

    if st.button("Sign Up"):
        st.success("Account Created Successfully")