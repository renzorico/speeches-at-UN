import streamlit as st
from data import load_geodata
from plot_map import select_topic, plot_geo_features

joined_gdf = load_geodata()

def map_main():
    selected_topic = select_topic(joined_gdf)
    plot_geo_features(selected_topic, joined_gdf)

map_main()
