import streamlit as st
# from data import load_count_topic_overtime
from data import run_query, BIG_QUERY, get_countries, get_years
import pandas as pd

'''
Defines functions to keep track of topics in texts and display them in histplots
(counting texts by topic, zooming in on particular topics)
'''



def select_info():
    years = get_years()
    selected_year_min = st.selectbox("Select a min year", years)
    selected_year_max = st.selectbox("Select a max year", years)
    min_year = int(selected_year_min)
    max_year = int(selected_year_max)
    year_range = [min_year, max_year]

    countries = get_countries()
    selected_countries = st.multiselect("Select country", countries)

    return year_range, selected_countries


def display_topics():
    query = f'''
            SELECT year, country, topic
            FROM {BIG_QUERY}
            GROUP BY year, country, topic
            ORDER BY year ASC
            '''
    feature_df = pd.DataFrame(run_query(query))

    st.dataframe(feature_df)

    year_range, selected_countries = select_info()

    st.write(year_range)

    filtered_data = feature_df[(feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])]

    st.dataframe(filtered_data)

    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    topic_counts = filtered_data.groupby('topic').size().reset_index(name='count')
    sorted_data = topic_counts.sort_values(by='count', ascending=False)
    st.bar_chart(data=sorted_data, x='topic', y='count')

    # year_range, selected_countries = select_info()
    # filtered_data = feature_df[(feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])]
    # filtered_data = filtered_data.loc[filtered_data['country'].isin(selected_countries)]
    # sorted_feature_df = filtered_data.sort_values(by='count', ascending=False)
    # st.bar_chart(data=sorted_feature_df, x='topic', y='count')


# def select_topic_hist(doc_topics, data):
#     features_df = load_count_topic_overtime(doc_topics, data)
#     topics = list(sorted(features_df['Name'].unique()))
#     selected_topic = st.selectbox("Select a topic", topics)
#     topic = features_df[features_df['Name'] == selected_topic]
#     words = topic['Top_n_words'].unique()
#     words_list = words[0].split(' - ')
#     return words_list
