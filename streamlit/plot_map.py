import plotly.express as px
import streamlit as st

def select_topic(joined_gdf):
    topics = joined_gdf['topic'].unique()
    selected_topic= st.selectbox("Select a topic", topics)
    return selected_topic

# def plot_geo_features(selected_topic, joined_gdf):
#     # Get a threshold for what "small numbers" means, e.g. bottom quartile
#     small_threshold = joined_gdf['counts'].quantile(0.25)
#     # Create a Pydeck layer for the GeoDataFrame
#     layer = dk.Layer(
#     "GeoJsonLayer",
#     data=joined_gdf.loc[joined_gdf['topic'] == selected_topic],
#     opacity=0.8,
#     get_fill_color="[(counts <= {0}) * 255, (counts > {0}) * 255, 0]".format(small_threshold),
#     pickable=True,
#     auto_highlight=True,
#     extruded=True,
#     get_elevation="counts * 1000",
#     get_line_color=[255, 255, 255],
#     )
# # Set the initial view state
#     view_state = pdk.ViewState(
#     latitude=0,
#     longitude=0,
#     zoom=1,
#     )
# # Create a Pydeck map
#     r = pdk.Deck(layers=[layer], initial_view_state=view_state)
#         # Render the map
#     st.pydeck_chart(r)

def plot_geo_features(selected_topic, joined_gdf):
    # Get a threshold for what "small numbers" means, e.g. bottom quartile
    small_threshold = joined_gdf['counts'].quantile(0.25)
    breakpoint()
    # Filter the GeoDataFrame for the selected topic
    filtered_gdf = joined_gdf.loc[joined_gdf['topic'] == selected_topic]
    st.dataframe(filtered_gdf)

    # # Create a choropleth map using Plotly Express
    # fig = px.choropleth(
    #     filtered_gdf,
    #     geojson=filtered_gdf['geometry'],
    #     locations=filtered_gdf.index,
    #     color=filtered_gdf['counts'],
    #     color_continuous_scale='Viridis',
    #     range_color=(0, small_threshold),
    #     hover_name=filtered_gdf['topic'],
    #     labels={'counts': 'Counts'},
    # )

    # # Update the map layout
    # fig.update_layout(
    #     height=600,
    #     margin=dict(r=0, l=0, t=0, b=0),
    #     mapbox_style="carto-positron",
    # )

    # # Render the map using Streamlit
    # st.plotly_chart(fig)
