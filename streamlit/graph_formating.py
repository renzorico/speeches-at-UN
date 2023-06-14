import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from data import run_query, BIG_QUERY, get_countries, get_topic
import pandas as pd



def select_topic():
    topics = get_topic()
    selected_topic = st.multiselect('Topic(s)', topics)
    return selected_topic

def select_country(key):
    countries = get_countries()
    selected_country = st.multiselect('Country(s)', countries, key=key)
    return selected_country

def generate_graph(selected_topic, selected_country):
    filterlist = ''
    for each in selected_topic:
        filterlist += f', "{each}"'

    countrylist = ''
    for each in selected_country:
        countrylist += f', "{each}"'

    query_graph = f'''SELECT year , topic, country, COUNT(country) as count FROM {BIG_QUERY}
        WHERE topic IN (''' + filterlist[2:] + ')' + ''' AND country IN (''' + countrylist[2:] + ''')
        GROUP BY year, topic, country
        ORDER BY year ASC '''

    query_full = f'''SELECT year , topic, COUNT(country) as count FROM {BIG_QUERY}
        WHERE topic IN (''' + filterlist[2:] + ')'  + '''
        GROUP BY year, topic
        ORDER BY year ASC '''

    if len(selected_country) > 1:
        filtered_df = pd.DataFrame(run_query(query_graph))
    else:
        filtered_df = pd.DataFrame(run_query(query_full))

    fig, ax = plt.subplots(figsize=(14, 6))
    if len(selected_country) > 1:
        sns.lineplot(data=filtered_df, x='year', y='count', hue='country', ax=ax, palette="bright")
    else:
        sns.lineplot(data=filtered_df, x='year', y='count', hue='topic', ax=ax, palette="bright")
    ax.set_title('Evolution of Topics Over the Years')
    st.pyplot(fig)
