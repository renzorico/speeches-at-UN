import streamlit as st
st.set_page_config(layout="wide")

from format_search import display_search
from data import get_topic

def main():
    st.title("Speech Search")
    col1, col2 = st.columns(2)
    with col1:
        search_text = st.text_input("Enter the text to search:", value='war')
    with col2:
        topic_selection = st.selectbox('Select topic', get_topic())
    display_search(search_text,topic_selection)

main()
