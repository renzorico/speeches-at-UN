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
    topic = st.selectbox('Topic', umap_topics, format_func=format_topic)
with col2:
    year = st.slider('Year', min_value=1946, max_value=2021, value=2000)

filtered = df.loc[(df['year'] == year) & (df['topic'] == topic)]
fig = px.scatter(
    filtered,
    x='umap_1', y='umap_2',
    hover_name='country',
    color='continent',
    size='count',
    size_max=40,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title=f'{format_topic(topic)} — {year}',
    labels={'umap_1': '', 'umap_2': ''},
)
fig.update_layout(height=580, margin=dict(l=0, r=0, t=40, b=0))
fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
st.plotly_chart(fig, use_container_width=True)

# ── Topic trajectory ──────────────────────────────────────────────────────────
st.header('Topic trajectory over time')
st.caption(
    "The 10 most active countries on this topic, animated from 1946 to 2021. "
    "Countries close together used similar language that year. Press **▶** to animate."
)

topic_df = df[(df['topic'] == topic) & (df['count'] > 0)].copy()

# Fix to top 10 countries by total paragraph count — they appear every year
top10 = (
    topic_df.groupby('country')['count']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index.tolist()
)
traj_df = topic_df[topic_df['country'].isin(top10)].sort_values('year')

x_pad = (traj_df['umap_1'].max() - traj_df['umap_1'].min()) * 0.08
y_pad = (traj_df['umap_2'].max() - traj_df['umap_2'].min()) * 0.08
x_range = [traj_df['umap_1'].min() - x_pad, traj_df['umap_1'].max() + x_pad]
y_range = [traj_df['umap_2'].min() - y_pad, traj_df['umap_2'].max() + y_pad]

fig2 = px.scatter(
    traj_df,
    x='umap_1', y='umap_2',
    animation_frame='year',
    animation_group='country',
    hover_name='country',
    color='country',
    size='count',
    size_max=50,
    range_x=x_range,
    range_y=y_range,
    color_discrete_sequence=px.colors.qualitative.Dark24,
    title=f'{format_topic(topic)} — top 10 countries, 1946–2021',
    labels={'umap_1': '', 'umap_2': ''},
)
fig2.update_layout(height=620, margin=dict(l=0, r=0, t=40, b=0))
fig2.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig2.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 700
fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300

st.plotly_chart(fig2, use_container_width=True)
