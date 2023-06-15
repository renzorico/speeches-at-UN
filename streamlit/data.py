from nltk.corpus import stopwords
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import os
import pandas as pd
import numpy as np
import requests
import geopandas as gpd


BIG_QUERY = '''`lewagon-bootcamp-384011.production_dataset.speeches`'''

credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

@st.cache_data(ttl=1200)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]  # Convert to list of dicts. Required for st.cache_data to hash the return value.
    return rows

@st.cache_resource()
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
                    'international', 'well', 'like', 'area', 'take', 'end', 'rule', 'great', 'Mr']
    stop_words = stop_words + custom_stopwords
    return stop_words

geo_query = f'''
            SELECT year, country, topic, COUNT(speeches) as counts FROM `lewagon-bootcamp-384011.production_dataset.speeches`
            GROUP BY year, country, topic
            ORDER BY year ASC
            '''

@st.cache_data(ttl=600)
def load_geo():
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()

    # Convert the GeoJson data to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    return gdf


@st.cache_data()
def get_years():
    query = f"SELECT DISTINCT year FROM {BIG_QUERY} ORDER BY year DESC"
    result = pd.DataFrame(run_query(query))
    return result.year.values

@st.cache_data()
def get_countries():
    query = f"SELECT DISTINCT country FROM {BIG_QUERY} ORDER BY country"
    result = pd.DataFrame(run_query(query))
    return result.country.values

@st.cache_resource()
def get_topic():
    query = f"SELECT DISTINCT topic FROM {BIG_QUERY} WHERE topic != 'bla_bla' ORDER BY topic"
    result = pd.DataFrame(run_query(query))
    return result.topic.values

@st.cache_data()
def get_continent():
    query = f"SELECT DISTINCT continent FROM {BIG_QUERY} ORDER BY continent"
    result = pd.DataFrame(run_query(query))
    return result.continent.values







wordcloud_query = f'''
SELECT year, country, STRING_AGG(speeches, ' ') AS merged_speeches
FROM {BIG_QUERY}
GROUP BY year, country
'''

@st.cache_resource()
def get_data_wordcloud():
    data = pd.DataFrame(run_query(wordcloud_query))
    data.drop_duplicates(inplace=True)
    stop_words = load_stopwords()
    data_dict = data.set_index(['year', 'country'])['merged_speeches'].to_dict()
    return data, stop_words, data_dict


@st.cache_resource()
def get_best_words():
    bertopic_query = """WITH unsetted AS (
    SELECT FLOOR(year / 10) * 10 as decade, topic,
    SPLIT(REPLACE(REPLACE(REPLACE(REPLACE(CAST(ber_topic_words AS STRING), '[', ''), ']', ''), ',', ' '), "'", ''), ' ') as ber_topic_words_array,country
    FROM `lewagon-bootcamp-384011.production_dataset.speeches`
    WHERE bert_prob = 1 AND topic != "bla_bla"),
unnested AS (
    SELECT decade, topic, TRIM(word) as word, country
    FROM unsetted, UNNEST(ber_topic_words_array) as word
)
SELECT decade, country, topic, word AS ber_topic_words, COUNT(country) as country_count
FROM unnested
GROUP BY decade, country, topic, word

    """

    data = pd.DataFrame(run_query(bertopic_query))
    data = data.dropna(subset=['ber_topic_words'], axis=0)
    data = data.loc[data.ber_topic_words != '']
    return data




@st.cache_data()
def load_umap():

    df = pd.read_csv('raw_data/umap.csv')
    return df

def select_info():
    years = get_years()
    years = [int(year) for year in years if isinstance(year, np.int64)]
    all_years = [min(years), max(years)]
    start_year, end_year = st.slider("Select a year range", min_value=min(all_years), max_value=max(all_years),
                                     value=(min(years), max(years)))
    year_range = [start_year, end_year]

    countries = get_countries()
    selected_countries = st.multiselect("Select a Country:", countries)
    return year_range, selected_countries
