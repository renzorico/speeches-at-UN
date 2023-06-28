import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from data import run_query, BIG_QUERY, get_topic, get_continent
import pandas as pd



def select_topic():
    topics = get_topic()
    selected_topic = st.multiselect('Topic(s)', topics)
    return selected_topic

def select_continent():
    continents = get_continent()
    selected_continent = st.multiselect('Continent', continents)
    return selected_continent

def generate_graph(selected_topic, selected_continent):
    filter_list = ''
    for each in selected_topic:
        filter_list += f', "{each}"'

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

    if len(selected_continent) > 1:
        filtered_df = pd.DataFrame(run_query(query_graph))
    else:
        filtered_df = pd.DataFrame(run_query(query_full))

    fig, ax = plt.subplots(figsize=(14, 6))
    if len(selected_continent) > 1:
        sns.lineplot(data=filtered_df, x='year', y='count', hue='continent', ax=ax, palette="bright")
    else:
        sns.lineplot(data=filtered_df, x='year', y='count', hue='topic', ax=ax, palette="bright")

    ax.set_title('Evolution of Topics Over the Years')
    st.pyplot(fig)
