import requests
import geopandas as gpd
import pydeck as pdk
import numpy as np
import streamlit as  st
import plotly.express as px

st.set_page_config(layout="wide")
@st.cache_data(ttl=600)
def load_geo():
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()

    # Convert the GeoJson data to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    return gdf

def create_plot(df, country_column, count_column):
    gdf = load_geo()
    joined_gdf = gdf.set_index('ADMIN').join(df.set_index(country_column), how='left')

    # Create a Plotly choropleth map
    fig = px.choropleth(
        joined_gdf,
        geojson=joined_gdf.geometry,
        locations=joined_gdf.index,
        color=count_column,
        color_continuous_scale='greens',
        range_color=(joined_gdf[count_column].min(), joined_gdf[count_column].max()),
        projection='natural earth',
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig
