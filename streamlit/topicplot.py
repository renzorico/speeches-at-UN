import streamlit as st
import plotly.express as px
from data import run_query, BIG_QUERY, get_countries, get_years, get_topic, load_topics_meta, load_topic_words, USE_LOCAL_MODE, format_topic
import pandas as pd
import ast

'''
Defines functions to keep track of topics in texts and display them in histplots
(counting texts by topic, zooming in on particular topics)
'''


def select_info():
    years = get_years()
    year_range = st.slider(
        "Select year range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),
    )
    countries = get_countries()
    selected_countries = st.multiselect("Filter by country", countries)
    return list(year_range), selected_countries


def display_topics():
    df = load_topics_meta()
    if df is not None and 'topic' in df.columns:
        feature_df = df[['year', 'country', 'topic']].dropna(subset=['topic'])
        feature_df = feature_df[feature_df['topic'] != 'bla_bla']
    elif not USE_LOCAL_MODE:
        query = f'''
                SELECT year, country, topic
                FROM {BIG_QUERY}
                WHERE topic != 'bla_bla'
                GROUP BY year, country, topic
                ORDER BY year ASC
                '''
        feature_df = pd.DataFrame(run_query(query))
    else:
        st.info("No data available.")
        return

    year_range, selected_countries = select_info()
    filtered_data = feature_df[(feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])]

    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    topic_counts = filtered_data.groupby('topic').size().reset_index(name='count')
    sorted_data = topic_counts.sort_values(by='count', ascending=False).head(7)
    sorted_data['topic_label'] = sorted_data['topic'].apply(format_topic)

    fig = px.bar(
        sorted_data, x='count', y='topic_label',
        orientation='h',
        labels={'topic_label': '', 'count': 'Paragraphs'},
        color='count',
        color_continuous_scale='Blues',
    )
    fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder': 'total ascending'})
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)


def select_topic_hist():
    topics = [t for t in get_topic() if t != 'bla_bla']
    if not topics:
        st.info("No topics available.")
        return []

    selected_topic = st.selectbox("Select a topic", topics, format_func=format_topic)

    tw = load_topic_words()
    if tw is not None:
        row = tw[tw['topic_name'] == selected_topic]
        if not row.empty:
            word_list = ast.literal_eval(row.iloc[0]['top_5_words'])
            return word_list, int(row.iloc[0]['count'])
        return [], 0
    elif not USE_LOCAL_MODE:
        query = f'''SELECT year, country, topic, top_5_words
            FROM {BIG_QUERY}
            '''
        data = pd.DataFrame(run_query(query))
        topic = data[data['topic'] == selected_topic]
        words = topic['top_5_words'].tolist()
        word_list = ast.literal_eval(words[0])
        return word_list, 0
