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

<<<<<<< HEAD
def generate_graph(selected_topic, selected_continent):
    filter_list = ''
=======
def generate_graph(selected_topic):
    if not selected_topic:
        return st.warning('Please select topic first!')
    filterlist = ''
>>>>>>> 04810480ff6a83e388608e152d3ff1afb8a43160
    for each in selected_topic:
        filter_list += f', "{each}"'

<<<<<<< HEAD
    continent_list = ''
    for each in selected_continent:
        continent_list += f', "{each}"'

    query_graph = f'''SELECT year , topic, continent, COUNT(continent) as count FROM {BIG_QUERY}
        WHERE topic IN (''' + filter_list[2:] + ')' + ''' AND continent IN (''' + continent_list[2:] + ''')
        GROUP BY year, topic, continent
        ORDER BY year ASC '''

    query_full = f'''SELECT year , topic, COUNT(continent) as count FROM {BIG_QUERY}
        WHERE topic IN (''' + filter_list[2:] + ')'  + '''
        GROUP BY year, topic
        ORDER BY year ASC '''
=======
    query_full = f'''SELECT year , topic, continent, COUNT(continent) as count FROM {BIG_QUERY}
        WHERE topic IN (''' + filterlist[2:] + ')'  + '''
        GROUP BY year, topic, continent
        ORDER BY year ASC '''

>>>>>>> 04810480ff6a83e388608e152d3ff1afb8a43160

    filtered_df = pd.DataFrame(run_query(query_full))
    # filtered_df = filtered_df.groupby(['year', 'continent']).agg({'count':'sum'}).reset_index()

    fig = px.line(filtered_df, x='year', y='count', color='continent', line_dash='topic')
    st.plotly_chart(fig, use_container_width=True)
