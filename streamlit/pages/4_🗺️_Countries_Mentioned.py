import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
from clean_countries import to_drop, clean_country
from data import run_query
from plot_map import create_countries_plot
import plotly.graph_objects as go

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
topic = st.selectbox('Select topic', df.topic.unique(), index=2)
# countries = st.multiselect('Select countries', top_countries,)

df = df.loc[(df.topic==topic)]
# fig = px.line(df, x="year", y="country_count", color="country_mentioned", text="country_count")
# fig.update_traces(textposition="bottom right")
# fig.show()
df_agg = df.groupby(['year', 'country_mentioned'])['country_count'].sum().reset_index()

count_mean = df_agg.country_count.mean()
count_std = df_agg.country_count.std()


# top_10 = df.groupby('country_mentioned').agg({'country_count':'sum'}).reset_index().sort_values('country_count', ascending=False).country_mentioned.values[:5]
threshold =count_mean + (count_std*2)
top_10 = list(set(df_agg.loc[df_agg.country_count>(threshold)].country_mentioned.values))
df_agg = df_agg.loc[df_agg.country_mentioned.isin(top_10)]



# List of all countries
all_countries = df_agg['country_mentioned'].unique()

# Countries that should be visible at first
selected_countries = ['Afghanistan', 'Korea', 'Iraq', 'Vietnam']

fig = go.Figure()

for country in all_countries:
    country_data = df_agg[df_agg['country_mentioned']==country]
    max_idx = country_data['country_count'].idxmax()  # get index of the maximum count
    country_text = [country if idx == max_idx else '' for idx in country_data.index]  # put country name at max count

    if country in selected_countries:
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['country_count'],
            mode='lines+text',
            name=country,
            text=country_text,
            textposition='top center',
            line=dict(width=4),
            visible=True
        ))
    else:
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['country_count'],
            mode='lines+text',
            name=country,
            text=country_text,
            textposition='top center',
            line=dict(width=2),
            visible='legendonly'
        ))

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Mentions Count",
)
fig.update_traces(textfont=dict(size=16))




st.plotly_chart(fig, use_container_width=True)

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

# show_map = st.button('Show Map')
# if show_map:
#     map_countries()
