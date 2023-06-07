import streamlit as st
from data import load_geodata
from plot_map import select_topic, plot_geo_features

joined_gdf = load_geodata()

def map_main():
    topic = select_topic(joined_gdf)
    plot_geo_features(topic, joined_gdf)

map_main()
