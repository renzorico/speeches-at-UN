import streamlit as st
from line_graphtopics import generate_graph
from data import load_data

topics_df, doc_topics, data = load_data()

def graph_main():
    generate_graph(data)


graph_main()
