import streamlit as st
from data import run_query, BIG_QUERY, get_topic, select_info
import pandas as pd
import ast

'''
Defines functions to keep track of topics in texts and display them in histplots
(counting texts by topic, zooming in on particular topics)
'''

def display_topics():
    query = f'''
            SELECT year, country, topic
            FROM {BIG_QUERY}
            GROUP BY year, country, topic
            ORDER BY year ASC
            '''
    feature_df = pd.DataFrame(run_query(query))
    year_range, selected_countries = select_info()
    filtered_data = feature_df[(feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])]

    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    topic_counts = filtered_data.groupby('topic').size().reset_index(name='count')
    sorted_data = topic_counts.sort_values(by='count', ascending=False)
    desired_order = sorted_data.topic.values.tolist()
    sorted_data = topic_counts.loc[topic_counts['topic'].isin(desired_order)].copy()
    sorted_data['topic'] = pd.Categorical(sorted_data['topic'], categories=desired_order, ordered=True)
    sorted_data = sorted_data.sort_values('topic')

    st.bar_chart(data=sorted_data, x='topic', y='count')


# Go over this
def select_topic_hist():
    query = f'''SELECT year, country, topic, ber_topic_words
        FROM {BIG_QUERY}
        '''
    data = pd.DataFrame(run_query(query))
    topics = get_topic()
    selected_topic = st.selectbox("Select a topic", topics)

    topic = data[data['topic'] == selected_topic]
    words = topic['ber_topic_words'].tolist()
    word_list = ast.literal_eval(words[0])
    st.write(word_list)
    return word_list
