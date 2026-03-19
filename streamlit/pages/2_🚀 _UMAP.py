import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide", page_title="Speech Similarity Map | UN Speeches", page_icon="🌍")

from data import load_umap, format_topic

st.title('Speech Similarity Map')
st.caption(
    "Each bubble is one country's speeches on the selected topic in a given year. "
    "**The axes have no fixed meaning** — positions are computed by UMAP, which groups countries "
    "by how similar their language is. **Distance is what matters**: countries close together "
    "spoke about the topic in a very similar way. Bubbles are labelled for the 8 most active speakers."
)

df = load_umap()

NOISE_TOPICS = {'bla_bla', 'data_stats'}
umap_topics = sorted([t for t in df['topic'].unique() if t not in NOISE_TOPICS])

if 'umap_year' not in st.session_state:
    st.session_state['umap_year'] = int(st.query_params.get("year", 2000))

def _prev_year():
    st.session_state['umap_year'] = max(1946, st.session_state['umap_year'] - 1)

def _next_year():
    st.session_state['umap_year'] = min(2021, st.session_state['umap_year'] + 1)

col_topic, col_prev, col_slider, col_next = st.columns([4, 1, 6, 1])
with col_topic:
    _topic_p = st.query_params.get("topic", umap_topics[0] if umap_topics else "")
    _topic_idx = umap_topics.index(_topic_p) if _topic_p in umap_topics else 0
    topic = st.selectbox('Topic', umap_topics, index=_topic_idx, format_func=format_topic)
with col_prev:
    st.write('')
    st.button('◀', on_click=_prev_year, help='Previous year')
with col_slider:
    year = st.slider('Year', min_value=1946, max_value=2021, key='umap_year')
with col_next:
    st.write('')
    st.button('▶', on_click=_next_year, help='Next year')

st.query_params["topic"] = topic
st.query_params["year"]  = year

filtered = df.loc[(df['year'] == year) & (df['topic'] == topic)].copy()

if len(filtered) < 5:
    st.info(f"Only {len(filtered)} {'country' if len(filtered) == 1 else 'countries'} discussed this topic in {year}. This is expected for niche topics or early years — try a different year or topic to see more activity.")

# Label the 8 most active countries so positions are self-explanatory
top8 = filtered.nlargest(8, 'count')['country']
filtered['label'] = filtered['country'].where(filtered['country'].isin(top8), '')

fig = px.scatter(
    filtered,
    x='umap_1', y='umap_2',
    text='label',
    hover_name='country',
    color='continent',
    size='count',
    size_max=40,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title=f'{format_topic(topic)} — {year}',
    labels={'umap_1': '', 'umap_2': ''},
)
fig.update_traces(textposition='top center', textfont_size=10)
fig.update_layout(height=580, margin=dict(l=0, r=0, t=40, b=0))
fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
st.plotly_chart(fig, width='stretch')

# ── Topic trajectory ──────────────────────────────────────────────────────────
st.header('Topic trajectory over time')
st.caption(
    "The 10 countries with the most speeches on this topic across all years, animated from 1946 to 2021. "
    "**Bubble size** = paragraphs that year (small = few speeches that year). "
    "Countries close together used similar language. Press **▶** to animate."
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
traj_base = topic_df[topic_df['country'].isin(top10)]
all_years = sorted(topic_df['year'].unique())

# Interpolate missing years so every country has a bubble in every frame
filled = []
for country in top10:
    cdf = traj_base[traj_base['country'] == country].set_index('year')
    continent = cdf['continent'].iloc[0]
    cdf = cdf.reindex(all_years)
    cdf[['umap_1', 'umap_2']] = cdf[['umap_1', 'umap_2']].interpolate(
        method='linear', limit_direction='both'
    )
    # Missing years get count=1 so bubbles stay visible but small
    cdf['count'] = cdf['count'].fillna(1)
    cdf['country'] = country
    cdf['continent'] = continent
    filled.append(cdf.reset_index().rename(columns={'index': 'year'}))

traj_df = pd.concat(filled).sort_values('year')

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
    text='country',
    color='country',
    size='count',
    size_max=50,
    range_x=x_range,
    range_y=y_range,
    color_discrete_sequence=px.colors.qualitative.Dark24,
    title=f'{format_topic(topic)} — top 10 countries, 1946–2021',
    labels={'umap_1': '', 'umap_2': ''},
)
fig2.update_traces(textposition='middle center', textfont=dict(size=9, color='white'))
# Apply text styling to every animation frame
for frame in fig2.frames:
    for trace in frame.data:
        trace.update(textposition='middle center', textfont=dict(size=9, color='white'))
fig2.update_layout(height=620, margin=dict(l=0, r=0, t=40, b=0))
fig2.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig2.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, title='')
fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 700
fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300

st.plotly_chart(fig2, width='stretch')
