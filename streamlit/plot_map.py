import pydeck as pdk
import streamlit as st

def select_topic(joined_gdf):
    topics = joined_gdf['Name'].unique()
    selected_topic= st.selectbox("Select a topic", topics)
    return selected_topic

def plot_geo_features(topic, joined_gdf):
    # Create a Pydeck layer for the GeoDataFrame
    layer = pdk.Layer(
        "GeoJsonLayer",
        data=joined_gdf.loc[joined_gdf.Name == topic],
        opacity=0.8,
        get_fill_color="[count * 50, 0, 255 - count * 50]",
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
    r
