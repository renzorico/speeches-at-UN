from nltk.corpus import stopwords
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import os
import pandas as pd
import numpy as np
import requests
import geopandas as gpd


BIG_QUERY = os.environ.get('PROJECT_BIGQUERY')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

@st.cache_data()
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]  # Convert to list of dicts. Required for st.cache_data to hash the return value.
    return rows

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

@st.cache_data()
def get_topic():
    query = f"SELECT DISTINCT topic FROM {BIG_QUERY} ORDER BY topic"
    result = pd.DataFrame(run_query(query))
    return result.topic.values




wordcloud_query = f'''
SELECT year, country, STRING_AGG(speeches, ' ') AS merged_speeches
FROM {BIG_QUERY}
GROUP BY year, country
'''

@st.cache_data
def get_data_wordcloud():
    data = pd.DataFrame(run_query(wordcloud_query))
    data.drop_duplicates(inplace=True)
    stop_words = load_stopwords()
    data_dict = data.set_index(['year', 'country'])['merged_speeches'].to_dict()
    return data, stop_words, data_dict


def select_info():
    years = get_years()
    years = [int(year) for year in years if isinstance(year, np.int64)]
    all_years = [min(years), max(years)]
    start_year, end_year = st.slider("Select a year range", min_value=min(all_years), max_value=max(all_years),
                                     value=(min(all_years), max(all_years)))
    year_range = [start_year, end_year]

    countries = get_countries()
    selected_countries = st.multiselect("Select country", countries)

    return year_range, selected_countries
