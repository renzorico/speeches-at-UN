import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")

from data import load_umap, get_topic
st.title('Distribution of countries on each topic year by year')
df = load_umap()

col1, col2 = st.columns(2)

with col1:
    year = st.slider('Year', min_value=1946, max_value=2021, value=1974)
with col2:
    topic = st.selectbox('Topic', get_topic(),index=1)

filtered = df.loc[(df.year==year) & (df.topic==topic)]
fig = px.scatter(filtered, x='umap_1', y='umap_2', hover_name='country', color='continent', title='UMAP Embeddings of Speeches', size='count')
# update layout to increase height
fig.update_layout(height=600)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

st.plotly_chart(fig, use_container_width=True)

# countries = st.multiselect('Select countries', list(set(df.country.values)))
# filtered_country = df.loc[(df.year==year) & (df.topic==topic) & (df.country.isin(countries))]
# fig_country = px.scatter(filtered_country, x='umap_1', y='umap_2', hover_name='country', color='continent', title='UMAP Embeddings of Speeches in 2019', size='count')
# # update layout to increase height
# fig_country.update_layout(height=600)
# fig_country.update_xaxes(showgrid=False)
# fig_country.update_yaxes(showgrid=False)

# st.plotly_chart(fig_country, use_container_width=True)

st.header('Change of topics for each country over time')
filtered_2 = df.loc[df.topic==topic]
fig2= px.scatter_3d(filtered_2, x='year', y='umap_2',z = 'umap_1', hover_name='country', color='continent', size='count')
# update layout to increase height
fig2.update_layout(height=800)

fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(showgrid=False)

st.plotly_chart(fig2, use_container_width=True)
