import streamlit as st
from format_search import display_search


def main():

    st.title("Speech Search")
    search_text = st.text_input("Enter the text to search:")

    display_search(search_text)


main()
