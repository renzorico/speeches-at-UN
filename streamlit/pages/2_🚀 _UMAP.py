import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")

from data import load_umap, format_topic

st.title('Speech Similarity Map')

df = load_umap()

NOISE_TOPICS = {'bla_bla', 'data_stats'}
umap_topics = sorted([t for t in df['topic'].unique() if t not in NOISE_TOPICS])

topic = st.selectbox('Topic', umap_topics, format_func=format_topic)
topic_df = df[(df['topic'] == topic) & (df['count'] > 0)].copy()

# ── 3D scatter: semantic space × time ────────────────────────────────────────
st.subheader('Semantic space across years')
st.caption(
    "Each bubble is one country's speeches in a given year. "
    "**X / Y** = semantic similarity (closer = more similar language). "
    "**Z** = year. **Size** = number of paragraphs. Drag to rotate."
)

fig3d = px.scatter_3d(
    topic_df,
    x='umap_1', y='umap_2', z='year',
    color='continent',
    size='count',
    size_max=12,
    hover_name='country',
    hover_data={'umap_1': False, 'umap_2': False, 'year': True, 'count': True, 'continent': False},
    color_discrete_sequence=px.colors.qualitative.Set2,
    title=f'{format_topic(topic)}',
)
fig3d.update_layout(
    height=650,
    scene=dict(
        xaxis=dict(showticklabels=False, title='', showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, title='', showgrid=False, zeroline=False),
        zaxis=dict(title='Year'),
    ),
    margin=dict(l=0, r=0, t=40, b=0),
)
st.plotly_chart(fig3d, use_container_width=True)

# ── Trajectory lines ──────────────────────────────────────────────────────────
st.subheader('Country trajectories over time')
st.caption(
    "How each country's speech-language drifted through semantic space from 1946 to 2021. "
    "Each line traces one country's path — start = earliest year, end = most recent."
)

# Only countries with enough years to show a meaningful path
MIN_YEARS = 20
well_represented = (
    topic_df.groupby('country')['year']
    .count()
    .loc[lambda s: s >= MIN_YEARS]
    .sort_values(ascending=False)
)

top_default = well_represented.head(8).index.tolist()
all_options = well_represented.index.tolist()

selected_countries = st.multiselect(
    'Countries (showing those with ≥ 20 years of data)',
    options=all_options,
    default=top_default,
)

if selected_countries:
    traj_df = topic_df[topic_df['country'].isin(selected_countries)].sort_values('year')

    fig_traj = px.line(
        traj_df,
        x='umap_1', y='umap_2',
        color='country',
        hover_data={'year': True, 'count': True, 'umap_1': False, 'umap_2': False},
        markers=True,
        title=f'{format_topic(topic)} — country trajectories',
        labels={'umap_1': '', 'umap_2': ''},
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    fig_traj.update_layout(height=560, margin=dict(l=0, r=0, t=40, b=0))
    fig_traj.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
    fig_traj.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
    st.plotly_chart(fig_traj, use_container_width=True)
else:
    st.info('Select at least one country above to show trajectories.')
