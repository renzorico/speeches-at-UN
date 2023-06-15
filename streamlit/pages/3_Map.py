import streamlit as st
from data import get_topic, run_query, get_years
from plot_map import plot_geo_features
import pandas as pd
import numpy as np


def map_main():
    years = get_years()
    years = [int(year) for year in years if isinstance(year, np.int64)]
    all_years = [min(years), max(years)]
    start_year, end_year = st.slider("Select a year range", min_value=min(all_years), max_value=max(all_years),
                                     value=(min(years), max(years)))

    selected_topic = st.selectbox('Select topic', get_topic())
    geo_query = f'''
            SELECT year, country, topic, COUNT(speeches) as counts FROM `lewagon-bootcamp-384011.production_dataset.speeches`
            WHERE topic = "{selected_topic}"
            AND year >= {start_year}
            AND year <= {end_year}
            GROUP BY year, country, topic
            ORDER BY year ASC
            '''
    df = pd.DataFrame(run_query(geo_query))


    plot_geo_features(df)

map_main()
