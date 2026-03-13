import pydeck as pdk
import streamlit as st
import requests
import pandas as pd
import geopandas as gpd
from data import get_topic, run_query, BIG_QUERY

def select_topic():
    topics = get_topic()
    selected_topic = st.selectbox('Selected topic', topics)
    return selected_topic

query = f'''SELECT year , topic, COUNT(country) as count FROM {BIG_QUERY}
    GROUP BY year, topic
    ORDER BY year ASC '''

@st.cache_data
def load_count_topic_overtime(data):
    return data.groupby(['year', 'country', 'topic_num'])['topic'].transform('count')

def load_geodata():
    # Need to change it, be careful for repeated counts for one speech
    data = pd.DataFrame(run_query(query))
    feature_df = load_count_topic_overtime(data)
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()
    # Convert the GeoJson data to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    joined_gdf = gdf.set_index('ADMIN')found
➜  speeches-at-UN git:(renzo-streamlit) ✗ direnv reload            [🐍 speeches-UN]
direnv: loading ~/code/renzorico/speeches-at-UN/.envrc
direnv: export +PROJECT_BIGQUERY
➜  speeches-at-UN git:(renzo-streamlit) ✗ streamlit run app.py     [🐍 speeches-UN]

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8503
  Network URL: http://10.0.2.38:850.join(feature_df.set_index('country'), how='left')
    joined_gdf.dropna(subset=['count'], inplace=True)
    return joined_gdf

def plot_geo_features(selected_topic, joined_gdf):
    # Get a threshold for what "small numbers" means, e.g. bottom quartile
    small_threshold = joined_gdf['count'].quantile(0.25)
    # Create a Pydeck layer for the GeoDataFrame
    layer = pdk.Layer(
    "GeoJsonLayer",
    data=joined_gdf.loc[joined_gdf['Name'] == selected_topic],
    opacity=0.8,
    get_fill_color="[(count <= {0}) * 255, (count > {0}) * 255, 0]".format(small_threshold),
    pickable=True,
    auto_highlight=True,
    extruded=True,
    get_elevation="count * 1000",
    get_line_color=[255, 255, 255],
    )
# Set the initial view state
    view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1,
    )
# Create a Pydeck map
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
        # Render the map
    st.pydeck_chart(r)
