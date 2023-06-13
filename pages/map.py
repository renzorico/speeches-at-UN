from plot_map import plot_geo_features, load_geodata
from data import get_topic, run_query, BIG_QUERY
import streamlit as st
def map_main():
    joined_gdf = load_geodata()
    topics = get_topic()
    selected_topic = st.selectbox('Selected topic', topics)
    plot_geo_features()

map_main()
