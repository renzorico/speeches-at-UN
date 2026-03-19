import plotly.express as px
import streamlit as st
from data import load_geo
def select_topic(joined_gdf):
    topics = joined_gdf['topic'].unique()
    selected_topic= st.selectbox("Select a topic", topics)
    return selected_topic

def plot_geo_features(df):
    gdf = load_geo()
    joined_gdf = gdf.set_index('name').join(df.set_index('country'), how='left')
    fig = px.choropleth(joined_gdf,
        geojson=joined_gdf.geometry,
        locations=joined_gdf.index,
        color='counts',
        color_continuous_scale='YlOrRd',
        projection='natural earth',
    )
    fig.update_traces(marker_line_color='white', marker_line_width=0.5)
    fig.update_geos(
        visible=True,
        showland=True,
        landcolor='#d0d0d0',
        showocean=True,
        oceancolor='#c9e8f5',
        showcoastlines=False,
        fitbounds="locations",
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, width='stretch')


def create_countries_plot(df, country_column, count_column):
    gdf = load_geo()
    joined_gdf = gdf.set_index('name').join(df.set_index(country_column), how='left')
    fig = px.choropleth(
        joined_gdf,
        geojson=joined_gdf.geometry,
        locations=joined_gdf.index,
        color=count_column,
        color_continuous_scale='Blues',
        range_color=(joined_gdf[count_column].min(), joined_gdf[count_column].max()),
        projection='natural earth',
    )
    fig.update_traces(marker_line_color='white', marker_line_width=0.5)
    fig.update_geos(
        visible=True,
        showland=True,
        landcolor='#e8e8e8',
        showocean=True,
        oceancolor='#d6eaf8',
        showcoastlines=False,
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, width='stretch')
