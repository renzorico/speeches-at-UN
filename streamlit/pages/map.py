import streamlit as st
from data import load_geodata
from plot_map import select_topic, plot_geo_features

joined_gdf = load_geodata()

query =

@st.cache_data
def load_count_topic_overtime(data):
    return data.groupby(['year', 'country', 'topic_num'])['topic'].transform('count')

def load_geodata():
    # Need to change it, be careful for repeated counts for one speech
    data = load_data()
    data = format_df(data)
    feature_df = load_count_topic_overtime(data)
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()
    # Convert the GeoJson data to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    joined_gdf = gdf.set_index('ADMIN').join(feature_df.set_index('country'), how='left')
    joined_gdf.dropna(subset=['count'], inplace=True)
    return joined_gdf

def map_main():
    selected_topic = select_topic(joined_gdf)
    plot_geo_features(selected_topic, joined_gdf)

map_main()
