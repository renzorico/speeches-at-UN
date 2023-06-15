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
    # joined_gdf.dropna(subset=['topic'], axis=0, inplace=True)
    # Create a Plotly choropleth map
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


def create_countries_plot(df, country_column, count_column):
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

    st.plotly_chart(fig, use_container_width=True)
