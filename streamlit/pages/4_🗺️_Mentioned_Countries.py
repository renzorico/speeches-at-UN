import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
from clean_countries import to_drop, clean_country

from data import run_query, get_years
import numpy as np
from plot_map import create_countries_plot
import plotly.express as px

st.title('What countries were mentioned over time for each topic')



def map_countries():
    query = """WITH unsetted AS (
    SELECT * FROM `lewagon-bootcamp-384011.production_dataset.speeches`,
    UNNEST(countries_recoded) as country_mentioned)
    SELECT year, topic,country_mentioned, COUNT(country) as country_count from unsetted
    WHERE topic != "bla_bla"
    GROUP BY year, topic,country_mentioned"""
    df = pd.DataFrame(run_query(query))

    df['country_mentioned'] = df['country_mentioned'].apply(clean_country)

    df = df.loc[~df.country_mentioned.isin(to_drop)]


    top_countries = df.groupby('country_mentioned')[['year']].count().sort_values('year', ascending=False).head(100).reset_index().country_mentioned.values

    years = get_years()
    years = [int(year) for year in years if isinstance(year, np.int64)]
    all_years = [min(years), max(years)]
    start_year, end_year = st.slider("Select a year range", min_value=min(all_years), max_value=max(all_years),
                                     value=(2010, 2012))

    topic = st.selectbox('Select topic', df.topic.unique())


    df = df.loc[(df.topic==topic) & (df.country_mentioned.isin(top_countries))
                & (df.year >= start_year)
                & (df.year <= end_year)]
    # fig = px.bar(df, x='country_mentioned', y='country_count', title=f'Mentioned countries in speeches on topic "{topic}"')
    # st.plotly_chart(fig)
    create_countries_plot(df,'country_mentioned', 'country_count' )

map_countries()
