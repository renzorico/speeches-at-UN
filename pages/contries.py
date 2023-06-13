import streamlit as st
import pandas as pd
from utilities.load_bq import run_query
from utilities.plot_map import create_plot
import plotly.express as px

st.title('What countries were mentioned over time for each topic')

query = """WITH unsetted AS (
SELECT * FROM `lewagon-bootcamp-384011.production_dataset.speeches`,
UNNEST(countries_recoded) as country_mentioned)
SELECT year, topic,country_mentioned, COUNT(country) as country_count from unsetted
GROUP BY year, topic,country_mentioned"""

df = run_query(query)
top_countries = df.groupby('country_mentioned')[['year']].count().sort_values('year', ascending=False).head(50).reset_index().country_mentioned.values

year = st.slider('Year', min_value=1946, max_value=2021)
topic = st.selectbox('Select topic', df.topic.unique())


df = df.loc[(df.topic==topic) & (df.country_mentioned.isin(top_countries))& (df.year ==year) ]
fig = px.bar(df, x='country_mentioned', y='country_count', title=f'Mentioned countries in speeches on topic "{topic}"')


st.plotly_chart(fig)
st.plotly_chart(create_plot(df,'country_mentioned', 'country_count' ), use_container_width=True)
