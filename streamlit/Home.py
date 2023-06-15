import streamlit as st
from streamlit_player import st_player


def main():
    st.title("United Nations General Assembly Debate speeches")

    #st_player("https://www.youtube.com/watch?v=eN2jqTilLOM&t=12s")

    st.markdown("<h3 style='font-family: Arial; font-size: 20px; text-align: right; line-height: 1.5;'>Since 1946, in September, all heads of States have been gathering in New York for the General Assembly’s high level Debate week. During this week, they deliver their speeches outlining their priorities in the international arena. These speeches are useful to understand what all States’ priorities are and how they change over time.</h3>", unsafe_allow_html=True)
    #st.markdown("<p style='font-family: Times New Roman; font-size: 16px; text-align: right; line-height: 0;'>and yours truly Will Smith.</p>", unsafe_allow_html=True)


main()
