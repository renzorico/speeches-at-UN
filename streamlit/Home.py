import streamlit as st
from streamlit_player import st_player


def main():
    st.title("Welcome to the United Nations!")

    st.markdown("<h3 style='font-family: Arial; font-size: 20px; text-align: right; line-height: 1.5;'>Sponsored by Kevin Hart...</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: Times New Roman; font-size: 16px; text-align: right; line-height: 0;'>and yours truly Will Smith.</p>", unsafe_allow_html=True)


main()
