import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data import load_count_topic_overtime, load_data

'''
Defines functions to keep track of topics in texts and display them in histplots (counting texts by topic, zooming in on particular topics)
'''

def select_info(data):
    years = list(sorted(data['year'].unique()))
    selected_year_min = st.selectbox("Select a min year", years)
    selected_year_max = st.selectbox("Select a max year", years)
    min_year = int(selected_year_min)
    max_year = int(selected_year_max)
    year_range = [min_year, max_year]

    countries = list(data['country'].unique())
    selected_countries = st.multiselect("Select country", countries + ['Select All'])
    if 'Select All' in selected_countries:
        selected_countries = countries

    return year_range, selected_countries


def display_topics(data):
    feature_df = data.groupby(['year','country','topic']).agg({'Document': 'count'}).reset_index().rename({'Document': 'count'}, axis=1)
    year_range, selected_countries = select_info(data)
    filtered_data = feature_df[(feature_df['year'] >= year_range[0]) & (feature_df['year'] <= year_range[1])]
    filtered_data = filtered_data.loc[filtered_data['country'].isin(selected_countries)]
    sorted_feature_df = filtered_data.sort_values(by='count', ascending=False)
    st.bar_chart(data=sorted_feature_df, x='Name', y='count')


def select_topic_hist(doc_topics, data):
    features_df = load_count_topic_overtime(doc_topics, data)
    topics = list(sorted(features_df['Name'].unique()))
    selected_topic = st.selectbox("Select a topic", topics)
    topic = features_df[features_df['Name'] == selected_topic]
    words = topic['Top_n_words'].unique()
    words_list = words[0].split(' - ')
    return words_list
