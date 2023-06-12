# import streamlit as st
from line_graphtopics import generate_graph, select_topic
from data import load_data

data = load_data()

def graph_main():
    selected_topic = select_topic(data)
    generate_graph(selected_topic, data)


graph_main()
