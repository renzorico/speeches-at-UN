import streamlit as st
from data import load_data
from topicplot import display_topics, select_topic_hist

data = load_data()

def hist_main():
    display_topics(data)
    words_list = select_topic_hist(data)
    st.write(words_list)


hist_main()
