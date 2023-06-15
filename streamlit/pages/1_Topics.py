from graph_formating import generate_graph, select_topic, select_continent
from topicplot import display_topics, select_topic_hist
import streamlit as st


def topics_main():
    st.header('Topics over Time')
    selected_topic = select_topic()
    selected_continent = select_continent()
    if not selected_topic:
        st.write('Please select a topic to plot.')
    else:
        generate_graph(selected_topic, selected_continent)

    st.empty()
    st.empty()
    st.empty()
    st.empty()


    st.header('Topics by Country over Time')

    display_topics()
    words_list = select_topic_hist()
    st.write(words_list)

topics_main()
