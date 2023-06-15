import streamlit as st
st.set_page_config(layout="wide")
import seaborn as sns
import pandas as pd
from clean_countries import to_drop, clean_country
import matplotlib.pyplot as plt
from data import run_query
from plot_map import create_countries_plot

st.title('What countries were mentioned over time for each topic')


query = """WITH unsetted AS (
SELECT * FROM `lewagon-bootcamp-384011.production_dataset.speeches`,
UNNEST(countries_recoded) as country_mentioned)
SELECT year, topic,country_mentioned, COUNT(country) as country_count from unsetted
WHERE topic != "bla_bla"
GROUP BY year, topic,country_mentioned"""

df = pd.DataFrame(run_query(query))
df['country_mentioned'] = df['country_mentioned'].apply(clean_country)
df = df.loc[~df.country_mentioned.isin(to_drop)]
top_countries = df.groupby('country_mentioned')[['topic']].count().sort_values('topic', ascending=False).head(100).reset_index().country_mentioned.values
topic = st.selectbox('Select topic', df.topic.unique())
# countries = st.multiselect('Select countries', top_countries,)

df = df.loc[(df.topic==topic)]

top_10 = df.groupby('country_mentioned').agg({'country_count':'sum'}).reset_index().sort_values('country_count', ascending=False).country_mentioned.values[:5]
df = df.loc[df.country_mentioned.isin(top_10)]
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(data=df, x='year', y='country_count', hue='country_mentioned',ax=ax,palette="bright")
st.pyplot(fig)

def map_countries():
    query = """WITH unsetted AS (
    SELECT * FROM `lewagon-bootcamp-384011.production_dataset.speeches`,
    UNNEST(countries_recoded) as country_mentioned)
    SELECT topic,country_mentioned, COUNT(country) as country_count from unsetted
    WHERE topic != "bla_bla"
    GROUP BY topic,country_mentioned"""
    df = pd.DataFrame(run_query(query))

    df['country_mentioned'] = df['country_mentioned'].apply(clean_country)

    df = df.loc[~df.country_mentioned.isin(to_drop)]


    top_countries = df.groupby('country_mentioned')[['topic']].count().sort_values('topic', ascending=False).head(100).reset_index().country_mentioned.values

    df = df.loc[(df.topic==topic) & (df.country_mentioned.isin(top_countries))]

    create_countries_plot(df,'country_mentioned', 'country_count' )

show_map = st.button('Show Map')
if show_map:
    map_countries()
