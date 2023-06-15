import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")

from data import load_umap, get_topic
st.title('Distribution of countries on each topic year by year')
df = load_umap()

col1, col2 = st.columns(2)

with col1:
    year = st.slider('Year', min_value=1946, max_value=2021, value=2000)
with col2:
    topic = st.selectbox('Topic', get_topic(),index=13)
df = df.loc[(df.year==year) & (df.topic==topic)]
fig = px.scatter(df, x='umap_1', y='umap_2', hover_name='country', color='continent', title='UMAP Embeddings of Speeches in 2019', size='count')
# update layout to increase height
fig.update_layout(height=600)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

st.plotly_chart(fig, use_container_width=True)
