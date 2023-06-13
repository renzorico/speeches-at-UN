import streamlit as st
from topicplot import display_topics


# @st.cache_data
# def load_count_topic_overtime(data):
#     return data.groupby(['year', 'country', 'topic_num'])['topic'].transform('count')

def hist_main():
    display_topics()
    # words_list = select_topic_hist()
    # st.write(words_list)


hist_main()
