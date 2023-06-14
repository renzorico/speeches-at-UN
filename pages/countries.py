import streamlit as st
import pandas as pd
from utilities.load_bq import run_query
from utilities.plot_map import create_plot
from utilities.country_clean import clen_country_v2
import plotly.express as px

st.title('What countries were mentioned over time for each topic')

query = """WITH unsetted AS (
SELECT * FROM `lewagon-bootcamp-384011.production_dataset.speeches`,
UNNEST(countries_recoded) as country_mentioned)
SELECT year_range, topic,country_mentioned, COUNT(country) as country_count from unsetted
GROUP BY year_range, topic,country_mentioned"""

df = run_query(query)
df["country_mentioned"] = df["country_mentioned"].apply(clen_country_v2)
st.dataframe(df)
st.write(len(df.country_mentioned.unique()))
#top_countries = df.groupby('country_mentioned')[['year_range']].count().sort_values('year_range', ascending=False).head(50).reset_index().country_mentioned.values

year = st.selectbox('Year', df.year_range.unique())
topic = st.selectbox('Select topic', df.topic.unique())


df = df.loc[(df.topic==topic) & (df.year_range ==year) ]
fig = px.bar(df, x='country_mentioned', y='country_count', title=f'Mentioned countries in speeches on topic "{topic}"')


st.plotly_chart(fig)
st.plotly_chart(create_plot(df,'country_mentioned', 'country_count' ), use_container_width=True)
