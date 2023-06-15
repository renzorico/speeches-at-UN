from graph_formating import generate_graph, select_topic
from topicplot import display_topics, select_topic_hist
import streamlit as st
st.set_page_config(layout="wide")

def topics_main():
    st.header('How did the agenda change over time for continents')

    with st.form('form'):

        selected_topic = select_topic()
        st.session_state.selected_topic = selected_topic



        graph_buttom = st.form_submit_button('Plot the graph')
    if graph_buttom:
         generate_graph(st.session_state.selected_topic)

    st.empty()
    st.empty()
    st.empty()
    st.empty()


    st.header('What were the main topics for each country in each decade')

    display_topics()

    st.header('How did the underline vocabulary change over time')

    words_list = select_topic_hist()
    st.write(words_list)

topics_main()
