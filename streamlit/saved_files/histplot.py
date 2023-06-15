import streamlit as st
from topicplot import display_topics, select_topic_hist


def hist_main():
    display_topics()
    words_list = select_topic_hist()
    st.write(words_list)


hist_main()
