import streamlit as st
from format_search import load_search_data, display_search


corpus_df = load_search_data()

def main_search():

    st.title("Speech Search")
    search_text = st.text_input("Enter the text to search:")

    display_search(corpus_df, search_text)


main_search()
