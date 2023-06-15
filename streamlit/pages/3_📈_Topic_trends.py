from graph_formating import generate_graph, select_topic, select_country
import streamlit as st


def graph_main():
    selected_topic = select_topic()
    selected_country = select_country('1')
    if not selected_topic:
        st.write('Please select a topic to plot.')
    else:
        generate_graph(selected_topic, selected_country)


graph_main()
