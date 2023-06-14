import plotly.express as px
import streamlit as st
from data import load_geo

def select_topic(joined_gdf):
    topics = joined_gdf['topic'].unique()
    selected_topic= st.selectbox("Select a topic", topics)
    return selected_topic

def plot_geo_features(df):
    gdf = load_geo()
    joined_gdf = gdf.set_index('ADMIN').join(df.set_index('country'), how='left')

    fig = px.choropleth(joined_gdf,
        geojson=joined_gdf.geometry,
        locations=joined_gdf.index,
        color='counts',
        color_continuous_scale='greens',
        projection='natural earth',
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Render the map using Streamlit
    st.plotly_chart(fig)
