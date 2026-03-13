import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")

from data import load_umap, format_topic

st.title('Speech Similarity Map')
st.caption(
    "Each bubble represents one country's speeches on the selected topic in a given year. "
    "**Proximity** = similar language used. "
    "**Bubble size** = number of paragraphs. **Colour** = continent."
)

df = load_umap()

NOISE_TOPICS = {'bla_bla', 'data_stats'}
umap_topics = sorted([t for t in df['topic'].unique() if t not in NOISE_TOPICS])

col1, col2 = st.columns(2)

with col1:
    year = st.slider('Year', min_value=1946, max_value=2021, value=2000)
with col2:
    topic = st.selectbox('Topic', umap_topics, format_func=format_topic)

filtered = df.loc[(df.year == year) & (df.topic == topic)]
fig = px.scatter(
    filtered,
    x='umap_1', y='umap_2',
    hover_name='country',
    color='continent',
    size='count',
    title=f'{format_topic(topic)} — {year}',
    labels={'umap_1': '', 'umap_2': ''},
)
fig.update_layout(height=600)
fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')

st.plotly_chart(fig, use_container_width=True)

st.header('Topic trajectory over time')
st.caption(
    "How countries cluster and drift in speech-space from 1946 to 2021 on the selected topic. "
    "Press **▶** to animate. Countries close together used similar language that year."
)

topic_df = df.loc[df.topic == topic].copy()
topic_df = topic_df[topic_df['count'] > 0].sort_values('year')

x_pad = (topic_df['umap_1'].max() - topic_df['umap_1'].min()) * 0.05
y_pad = (topic_df['umap_2'].max() - topic_df['umap_2'].min()) * 0.05
x_range = [topic_df['umap_1'].min() - x_pad, topic_df['umap_1'].max() + x_pad]
y_range = [topic_df['umap_2'].min() - y_pad, topic_df['umap_2'].max() + y_pad]

fig2 = px.scatter(
    topic_df,
    x='umap_1', y='umap_2',
    animation_frame='year',
    animation_group='country',
    hover_name='country',
    color='continent',
    size='count',
    size_max=40,
    range_x=x_range,
    range_y=y_range,
    title=f'{format_topic(topic)} — 1946 to 2021',
    labels={'umap_1': '', 'umap_2': ''},
)
fig2.update_layout(height=600)
fig2.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig2.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600
fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300

st.plotly_chart(fig2, use_container_width=True)
