import streamlit as st

st.set_page_config(
    page_title="My First Streamlit App",
    page_icon="📊",
    layout="wide"
)

st.title("👋 Welcome Reema!")

st.write("Congratulations! You have successfully installed Streamlit.")

st.success("Your Streamlit environment is working correctly!")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}! Welcome to Streamlit 🚀")