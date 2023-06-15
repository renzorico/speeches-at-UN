import streamlit as st
import plotly.express as px
from data import run_query, BIG_QUERY, get_topic, select_info, get_countries,get_best_words
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
            WHERE topic != "bla_bla"
            GROUP BY year, country, topic
            ORDER BY year ASC
            '''
    feature_df = pd.DataFrame(run_query(query))
    feature_df['decade'] = pd.cut(feature_df['year'], bins=range(1900, 2101, 10), labels=range(1900, 2100, 10))


    col1,col2 = st.columns(2)
    with col1:
        decade = st.slider('Select decade', min_value=feature_df['decade'].min(),
                           max_value=feature_df['decade'].max(),step=10, value=2010)
    with col2:
        countries = get_countries()
        selected_countries = st.multiselect("Select a Country:", countries,default=['Spain', 'France', 'Italy'])




    filtered_data = feature_df[feature_df['decade'] == decade]

    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
        # filtered_data = filtered_data.groupby('topic')

    topic_counts = filtered_data.groupby(['topic', 'country']).size().reset_index(name='count')
    sorted_data = topic_counts.sort_values(by='count', ascending=False)
    desired_order = sorted_data.topic.drop_duplicates().values.tolist()
    sorted_data['topic'] = pd.Categorical(sorted_data['topic'], categories=desired_order, ordered=True)
    sorted_data = sorted_data.sort_values('topic')

    fig = px.bar(sorted_data, x='topic', y='count',barmode='group', color='country', color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(
    xaxis_tickangle=-45,
    xaxis=dict(
        tickfont=dict(size=18),
        title=dict(font=dict(size=18))
    ),
    yaxis=dict(
        title=dict(font=dict(size=14))
    )
)
    st.plotly_chart(fig, use_container_width=True)


# Go over this
def select_topic_hist():
    df = get_best_words()
    df['decade'] = df.decade.astype(int)
    col1,col2, col3= st.columns(3)
    with col1:
        decade = st.slider('Select decade', min_value=int(df['decade'].min()),
                           max_value=int(df['decade'].max()),step=10, value=2010, key='new')
    with col2:
        countries = get_countries()
        selected_countries = st.multiselect("Select a Country:", countries,default=['Spain', 'France', 'Italy'], key='countries_words')
    with col3:
        topic = st.selectbox("Select topic", get_topic())


    df = df.loc[(df.decade==decade)& (df.country.isin(selected_countries)) & (df.topic==topic)]
    fig_topic = px.bar(df, x='ber_topic_words', y='country_count',barmode='group', color='country', color_discrete_sequence=px.colors.qualitative.Safe)
    fig_topic.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig_topic, use_container_width=True)

    # query = f'''SELECT year, country, topic, ber_topic_words
    #     FROM {BIG_QUERY}
    #     '''
    # data = pd.DataFrame(run_query(query))
    # topics = get_topic()
    # selected_topic = st.selectbox("Select a topic", topics)

    # topic = data[data['topic'] == selected_topic]
    # words = topic['ber_topic_words'].tolist()
    # word_list = ast.literal_eval(words[0])
    # return word_list
