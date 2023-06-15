import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from data import run_query, BIG_QUERY, get_topic, get_continent
import pandas as pd
import plotly.express as px


def select_topic():
    topics = get_topic()
    selected_topic = st.multiselect('Topic(s)', topics)
    return selected_topic

def select_continent():
    continents = get_continent()
    selected_continent = st.multiselect('Continent', continents)
    return selected_continent

def generate_graph(selected_topic):
    if not selected_topic:
        return st.warning('Please select topic first!')
    filterlist = ''
    for each in selected_topic:
        filterlist += f', "{each}"'

    query_full = f'''SELECT year , topic, continent, COUNT(continent) as count FROM {BIG_QUERY}
        WHERE topic IN (''' + filterlist[2:] + ')'  + '''
        GROUP BY year, topic, continent
        ORDER BY year ASC '''


    filtered_df = pd.DataFrame(run_query(query_full))
    # filtered_df = filtered_df.groupby(['year', 'continent']).agg({'count':'sum'}).reset_index()

    fig = px.line(filtered_df, x='year', y='count', color='continent', line_dash='topic')
    st.plotly_chart(fig, use_container_width=True)
