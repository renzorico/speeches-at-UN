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
    if not years:
        st.warning("Year data not available.")
        return [1946, 2021], []
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
        from_bq = False
    elif not USE_LOCAL_MODE:
        # Fetch pre-aggregated counts per year/country/topic so Python-side
        # filtering stays fast without re-querying BigQuery on every widget change.
        query = f"""
            SELECT year, country, topic, COUNT(*) AS count
            FROM {BIG_QUERY}
            WHERE topic != 'bla_bla'
            GROUP BY year, country, topic
            ORDER BY year ASC
        """
        rows = run_query(query)
        if not rows:
            st.info("No data available.")
            return
        feature_df = pd.DataFrame(rows)
        from_bq = True
    else:
        st.info("No data available.")
        return

    year_range, selected_countries = select_info()
    filtered_data = feature_df[
        (feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])
    ]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    if from_bq:
        topic_counts = filtered_data.groupby('topic')['count'].sum().reset_index()
    else:
        topic_counts = filtered_data.groupby('topic').size().reset_index(name='count')

    sorted_data = topic_counts.sort_values(by='count', ascending=False)
    sorted_data['topic_label'] = sorted_data['topic'].apply(format_topic)

    fig = px.bar(
        sorted_data, x='count', y='topic_label',
        orientation='h',
        labels={'topic_label': '', 'count': 'Paragraphs'},
        color='count',
        color_continuous_scale='Blues',
    )
    fig.update_layout(height=500, showlegend=False, yaxis={'categoryorder': 'total ascending'})
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
        count_rows = run_query(
            f"SELECT COUNT(*) AS count FROM {BIG_QUERY} WHERE topic = '{selected_topic}'"
        )
        count = count_rows[0]['count'] if count_rows else 0
        return [], count
