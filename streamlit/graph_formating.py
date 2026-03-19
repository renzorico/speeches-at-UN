import streamlit as st
import plotly.express as px
from data import run_query, BIG_QUERY, get_countries, get_topic, load_topics_meta, USE_LOCAL_MODE, format_topic
import pandas as pd


def select_topic():
    topics = get_topic()
    default = ['peace_war_security'] if 'peace_war_security' in topics else (topics[:1] if topics else [])
    selected_topic = st.multiselect('Topic(s)', topics, default=default, format_func=format_topic)
    return selected_topic

def select_country(key):
    countries = get_countries()
    default = ['United States of America'] if 'United States of America' in countries else (
              ['United States'] if 'United States' in countries else [])
    selected_country = st.multiselect('Country(s)', countries, default=default, key=key)
    return selected_country

def generate_graph(selected_topic, selected_country):
    df = load_topics_meta()
    normalize = st.toggle("Show as % of total paragraphs per year")

    if df is not None and 'topic' in df.columns:
        filtered = df[df['topic'].isin(selected_topic)]
        if selected_country:
            filtered = filtered[filtered['country'].isin(selected_country)]
            filtered_df = filtered.groupby(['year', 'topic', 'country']).size().reset_index(name='count')
        else:
            filtered_df = filtered.groupby(['year', 'topic']).size().reset_index(name='count')

        if normalize:
            total_per_year = df[df['topic'] != 'bla_bla'].groupby('year').size().reset_index(name='total_year')
            filtered_df = filtered_df.merge(total_per_year, on='year')
            filtered_df['count'] = (filtered_df['count'] / filtered_df['total_year'] * 100).round(2)

        y_label = '% of yearly paragraphs' if normalize else 'Paragraphs'
        topic_str = ', '.join([format_topic(t) for t in selected_topic])
        if selected_country:
            country_str = ', '.join(selected_country)
            title = f'{topic_str} — {country_str}'
        else:
            title = f'{topic_str} — global'

        hue = 'country' if selected_country else 'topic'
        fig = px.line(
            filtered_df, x='year', y='count', color=hue,
            title=title,
            labels={'year': 'Year', 'count': y_label, 'topic': 'Topic', 'country': 'Country'},
            markers=True,
            line_shape='spline',
        )
        fig.update_layout(height=500, legend_title_text='')
        st.plotly_chart(fig, use_container_width=True)
        return

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

    if selected_country:
        filtered_df = pd.DataFrame(run_query(query_graph))
    else:
        filtered_df = pd.DataFrame(run_query(query_full))

    topic_str = ', '.join([format_topic(t) for t in selected_topic])
    if selected_country:
        country_str = ', '.join(selected_country)
        title = f'{topic_str} — {country_str}'
    else:
        title = f'{topic_str} — global'

    hue = 'country' if selected_country else 'topic'
    fig = px.line(
        filtered_df, x='year', y='count', color=hue,
        title=title,
        labels={'year': 'Year', 'count': 'Paragraphs', 'topic': 'Topic', 'country': 'Country'},
        markers=True,
        line_shape='spline',
    )
    fig.update_layout(height=500, legend_title_text='')
    st.plotly_chart(fig, use_container_width=True)
