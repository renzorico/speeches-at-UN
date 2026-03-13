import streamlit as st
st.set_page_config(layout="wide")
from format_search import display_search
from data import get_topic, USE_LOCAL_MODE, format_topic


def main():
    st.title("Speech Search")
    col1, col2 = st.columns(2)
    with col1:
        search_text = st.text_input("Enter the text to search:", value='war')

    topics = [t for t in get_topic() if t != 'bla_bla']
    with col2:
        if topics:
            topic_selection = st.selectbox('Select topic', topics, format_func=format_topic)
        else:
            st.info("No topics found.")
            topic_selection = None

    display_search(search_text, topic_selection)


main()
