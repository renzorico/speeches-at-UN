import streamlit as st
from data import load_data
from topicplot import display_topics, select_topic_hist

_ , doc_topics, data = load_data()

def hist_main():
    display_topics(doc_topics, data)
    words_list = select_topic_hist(doc_topics, data)
    st.write(words_list)


hist_main()
