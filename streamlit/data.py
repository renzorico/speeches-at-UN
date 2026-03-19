from nltk.corpus import stopwords
import nltk
nltk.download('stopwords', quiet=True)
import streamlit as st
import os
import pandas as pd
import requests
import geopandas as gpd
from pathlib import Path

# ============================================================
# Configuration
# ============================================================
PROJECT_ROOT = Path(__file__).parent.parent
CLEAN_DATA_PATH = PROJECT_ROOT / 'data' / 'speeches_paragraphs.csv'
MENTIONED_COUNTRIES_PATH = Path(__file__).parent / 'mentioned_countries_agg.csv'

gcp_project = os.getenv('GCP_PROJECT_ID') or st.secrets.get('GCP_PROJECT_ID', 'speeches-at-un')
dataset = os.getenv('BIGQUERY_DATASET') or st.secrets.get('BIGQUERY_DATASET', 'un_speeches')
table = os.getenv('BIGQUERY_TABLE') or st.secrets.get('BIGQUERY_TABLE', 'speeches_paragraphs')
BIG_QUERY = os.getenv('BIGQUERY_TABLE_FULL') or st.secrets.get('BIGQUERY_TABLE_FULL', f'`{gcp_project}.{dataset}.{table}`')

# ============================================================
# BigQuery vs Local Mode Detection
# ============================================================
USE_LOCAL_MODE = True
client = None

try:
    # Only try BigQuery if credentials are actually configured
    if "gcp_service_account" in st.secrets and st.secrets["gcp_service_account"]:
        from google.oauth2 import service_account
        from google.cloud import bigquery

        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = bigquery.Client(credentials=credentials)
        USE_LOCAL_MODE = False
except Exception as e:
    USE_LOCAL_MODE = True
    client = None

# ============================================================
# Query Function
# ============================================================
@st.cache_data()
def run_query(query):
    """Run a query - BigQuery or local"""
    if not USE_LOCAL_MODE and client is not None:
        try:
            query_job = client.query(query)
            rows_raw = query_job.result()
            rows = [dict(row) for row in rows_raw]
            return rows
        except Exception as e:
            return []
    return []


# ============================================================
# Stopwords
# ============================================================
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


# ============================================================
# Local Data Functions
# ============================================================
@st.cache_data
def load_clean_data():
    """Load cleaned speeches from CSV"""
    if CLEAN_DATA_PATH.exists():
        return pd.read_csv(CLEAN_DATA_PATH)
    return None

@st.cache_data
def load_topics_meta():
    """Load only the columns needed for topic-based pages (map, trends, histogram).
    Much lighter than load_clean_data() — skips all speech text columns."""
    if CLEAN_DATA_PATH.exists():
        return pd.read_csv(CLEAN_DATA_PATH, usecols=['year', 'country', 'iso', 'continent', 'topic'])
    return None

@st.cache_data()
def get_years():
    """Get unique years"""
    df = load_topics_meta()
    if df is not None:
        return sorted(df['year'].unique())
    if not USE_LOCAL_MODE:
        result = pd.DataFrame(run_query(f"SELECT DISTINCT year FROM {BIG_QUERY} ORDER BY year"))
        return result['year'].tolist() if not result.empty else []
    return []

@st.cache_data()
def get_countries():
    """Get unique countries"""
    df = load_topics_meta()
    if df is not None:
        return sorted(df['country'].dropna().unique())
    if not USE_LOCAL_MODE:
        result = pd.DataFrame(run_query(f"SELECT DISTINCT country FROM {BIG_QUERY} WHERE country IS NOT NULL ORDER BY country"))
        return result['country'].tolist() if not result.empty else []
    return []

TOPIC_WORDS_PATH = PROJECT_ROOT / 'raw_data' / 'topic_labels.csv'

@st.cache_data()
def load_topic_words():
    """Load topic metadata (id, name, top_5_words) from CSV"""
    if TOPIC_WORDS_PATH.exists():
        return pd.read_csv(TOPIC_WORDS_PATH)
    return None

_ACRONYMS = {'ai', 'un', 'ussr', 'usa', 'eu', 'nato', 'aids', 'hiv'}

def format_topic(name: str) -> str:
    """Format a raw topic name for display: 'technology_ai_cyber' → 'Technology AI Cyber'"""
    words = name.replace('_', ' ').split()
    return ' '.join(w.upper() if w in _ACRONYMS else w.capitalize() for w in words)


@st.cache_data()
def get_topic():
    """Get list of topic name strings - prefers local CSV over BigQuery"""
    tw = load_topic_words()
    if tw is not None:
        return tw['topic_name'].tolist()
    if not USE_LOCAL_MODE:
        query = f"SELECT DISTINCT topic FROM {BIG_QUERY} WHERE topic != 'bla_bla' ORDER BY topic"
        result = pd.DataFrame(run_query(query))
        return result['topic'].tolist() if not result.empty else []
    return []


# ============================================================
# Geo Data
# ============================================================
@st.cache_data(ttl=600)
def load_geo():
    geojson_url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    geojson_data = requests.get(geojson_url).json()
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    return gdf


# ============================================================
# Word Cloud Data
# ============================================================
@st.cache_data
def get_data_wordcloud():
    """Get data for word cloud generation"""
    stop_words = load_stopwords()
    df = load_clean_data()
    if df is not None:
        wordcloud_data = df.groupby(['year', 'country'])['speeches'].apply(' '.join).reset_index()
        wordcloud_data.columns = ['year', 'country', 'merged_speeches']
        data_dict = wordcloud_data.set_index(['year', 'country'])['merged_speeches'].to_dict()
        return wordcloud_data, stop_words, data_dict
    if not USE_LOCAL_MODE:
        query = f"""
            SELECT year, country, STRING_AGG(speeches, ' ') AS merged_speeches
            FROM {BIG_QUERY}
            WHERE topic != 'bla_bla' AND speeches IS NOT NULL
            GROUP BY year, country
            ORDER BY year, country
        """
        rows = run_query(query)
        if rows:
            wordcloud_data = pd.DataFrame(rows)
            data_dict = wordcloud_data.set_index(['year', 'country'])['merged_speeches'].to_dict()
            return wordcloud_data, stop_words, data_dict
    return None, stop_words, {}


@st.cache_data()
def load_umap():
    """Load pre-computed UMAP embeddings"""
    umap_path = Path(__file__).parent / 'speeches_umap.csv'
    if umap_path.exists():
        return pd.read_csv(umap_path)
    return None

@st.cache_data()
def load_mentioned_countries_precomputed():
    """Load pre-computed mentioned countries aggregation.
    Generated by classify_topics.py — avoids runtime explosion of 117k rows."""
    if MENTIONED_COUNTRIES_PATH.exists():
        return pd.read_csv(MENTIONED_COUNTRIES_PATH)
    return None
