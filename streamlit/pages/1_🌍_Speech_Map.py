import streamlit as st
import numpy as np
import pandas as pd
from data import get_topic, get_years, run_query, BIG_QUERY, load_topics_meta, USE_LOCAL_MODE, format_topic
from plot_map import plot_geo_features


def map_main():
    years = get_years()
    years = [int(y) for y in years]
    start_year, end_year = st.slider(
        "Select a year range",
        min_value=min(years), max_value=max(years),
        value=(2010, 2015)
    )
    topics = [t for t in get_topic() if t != 'bla_bla']
    default_idx = topics.index('peace_war_security') if 'peace_war_security' in topics else 0
    selected_topic = st.selectbox('Select topic', topics, index=default_idx, format_func=format_topic)

    df = load_topics_meta()
    if df is not None and selected_topic:
        filtered = df[
            (df['topic'] == selected_topic) &
            (df['year'] >= start_year) &
            (df['year'] <= end_year)
        ]
        df_map = filtered.groupby(['year', 'country', 'topic']).size().reset_index(name='counts')
    elif not USE_LOCAL_MODE and selected_topic:
        geo_query = f'''
                SELECT year, country, topic, COUNT(speeches) as counts FROM {BIG_QUERY}
                WHERE topic = "{selected_topic}"
                AND year >= {start_year}
                AND year <= {end_year}
                GROUP BY year, country, topic
                ORDER BY year ASC
                '''
        df_map = pd.DataFrame(run_query(geo_query))
    else:
        st.warning("No data available.")
        return

    plot_geo_features(df_map)


map_main()
