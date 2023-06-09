import pandas as pd
from nltk.corpus import stopwords
import requests
import geopandas as gpd
import streamlit as st

@st.cache_data
def load_data():
    data = pd.read_csv('~/code/renzorico/speeches-at-UN/raw_data/speeches_with_paragraphs_processed_tt.csv')
    data.dropna(inplace=True)
    df_topics = pd.read_csv('~/code/renzorico/speeches-at-UN/raw_data/df_topics.csv')
    doc_topics = pd.read_csv('~/code/renzorico/speeches-at-UN/raw_data/doc_topics.csv')
    doc_topics.dropna(inplace=True)
    return df_topics, doc_topics, data

@st.cache_data
def load_stopwords():
    stop_words = set(stopwords.words('english'))
    stop_words = list(stop_words)
    custom_stopwords = ['united nations', 'general assembly', 'international law',
                    'international community', 'international criminal', 'international criminal court',
                    'international peace', 'international security', 'international tribunal',
                    'international cooperation', 'united nations general assembly',
                    'united kingdom', 'united nations security', 'united nations general',
                    'sierra leonean', 'sierra leoneans', 'per cent', 'mr president', 'small island',
                    'democratic republic', 'people republic', 'republic congo', 'republic iran', 'republic korea',
                    "united", "nations", "people", "shall", "president", 'delegation',
                    'world', 'herzegovina', 'year', 'argentine', 'today', 'state', 'country', 'also', 'must',
                    'states', 'continue', 'one', 'need', 'region', 'however', 'new', 'many', 'time', 'countries',
                    'international', 'well', 'like', 'area', 'take', 'end', 'rule', 'great']
    stop_words = stop_words + custom_stopwords
    return stop_words

@st.cache_data
def load_count_topic_overtime(doc_topics, data):
    doc_topics = data[['year', 'country']].merge(doc_topics, left_index=True, right_index=True)
    return doc_topics.groupby(['country', 'Name', 'Top_n_words']).agg({'Document': 'count'}).reset_index().rename({'Document': 'count'}, axis=1)

@st.cache_data
def load_geodata():
    _ , doc_topics, data = load_data()
    feature_df = load_count_topic_overtime(doc_topics, data)
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()
    # Convert the GeoJson data to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    joined_gdf = gdf.set_index('ADMIN').join(feature_df.set_index('country'), how='left')
    joined_gdf.dropna(subset=['count'], inplace=True)
    return joined_gdf
