from graph_formating import generate_graph, select_topic, select_country
import streamlit as st

st.set_page_config(layout="wide", page_title="Topic Trends | UN Speeches", page_icon="🌍")


def graph_main():
    st.title("Topic Trends Over Time")
    st.caption("How often each topic appears in UN speeches per year, globally or for a specific country.")
    selected_topic = select_topic()
    selected_country = select_country('1')
    if not selected_topic:
        st.write('Please select a topic to plot.')
    else:
        generate_graph(selected_topic, selected_country)


graph_main()