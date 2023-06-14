import streamlit as st
from plot_map import select_topic, plot_geo_features
from data import BIG_QUERY, run_query, load_geodata
import geopandas as gpd
import requests
import pandas as pd

joined_gdf = load_geodata()


def map_main():
    selected_topic = select_topic(joined_gdf)
    plot_geo_features(selected_topic, joined_gdf)

map_main()
