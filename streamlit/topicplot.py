import streamlit as st
# from data import load_count_topic_overtime
from data import run_query, BIT_QUERY
import pandas as pd

'''
Defines functions to keep track of topics in texts and display them in histplots
(counting texts by topic, zooming in on particular topics)
'''

def select_info():
    query_year = f'''SELECT DISTINCT(years) from {BIT_QUERY}'''
    years = pd.DataFrame(run_query(query_year)).year.values
    selected_year_min = st.selectbox("Select a min year", years)
    selected_year_max = st.selectbox("Select a max year", years)
    min_year = int(selected_year_min)
    max_year = int(selected_year_max)
    year_range = [min_year, max_year]

    query_countries = f'''SELECT DISTINCT(country) from {BIT_QUERY}'''
    countries = pd.DataFrame(run_query(query_countries)).country.values
    selected_countries = st.multiselect("Select country", countries + ['Select All'])
    if 'Select All' in selected_countries:
        selected_countries = countries

    return year_range, selected_countries


def display_topics():
    query = '''SELECT year, topic, COUNT(country) AS count # Have to change this
            FROM data
            GROUP BY year, country, topic'''
    feature_df = pd.DataFrame(run_query(query))

    st.write(feature_df)

    year_range, selected_countries = select_info()
    filtered_data = feature_df[(feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])]
    filtered_data = filtered_data.loc[filtered_data['country'].isin(selected_countries)]
    sorted_feature_df = filtered_data.sort_values(by='count', ascending=False)
    st.bar_chart(data=sorted_feature_df, x='Name', y='count')


# def select_topic_hist(doc_topics, data):
#     features_df = load_count_topic_overtime(doc_topics, data)
#     topics = list(sorted(features_df['Name'].unique()))
#     selected_topic = st.selectbox("Select a topic", topics)
#     topic = features_df[features_df['Name'] == selected_topic]
#     words = topic['Top_n_words'].unique()
#     words_list = words[0].split(' - ')
#     return words_list
