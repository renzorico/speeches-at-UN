import pandas as pd
from nltk.corpus import stopwords
import requests
import geopandas as gpd
import streamlit as st

@st.cache_data
def load_data():
    data = pd.read_csv('~/code/renzorico/speeches-at-UN/raw_data/data_st.csv')
    data = data.dropna(subset='speeches')
    return data

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
def load_count_topic_overtime(data):
    return data.groupby(['year', 'country', 'topic_num'])['topic'].transform('count')

@st.cache_data
def load_geodata():
    # Need to change it, be careful for repeated counts for one speech
    data = load_data()
    feature_df = load_count_topic_overtime(data)
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()
    # Convert the GeoJson data to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    joined_gdf = gdf.set_index('ADMIN').join(feature_df.set_index('country'), how='left')
    joined_gdf.dropna(subset=['count'], inplace=True)
    return joined_gdf
