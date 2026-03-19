import streamlit as st
st.set_page_config(layout="wide", page_title="Mentioned Countries | UN Speeches", page_icon="🌍")
import ast
import pandas as pd
import plotly.express as px
from clean_countries import to_drop, clean_country
from data import run_query, BIG_QUERY, load_clean_data, load_mentioned_countries_precomputed, USE_LOCAL_MODE, format_topic

st.title('Countries Mentioned in Speeches')


@st.cache_data
def load_mentioned_countries():
    """Fallback: compute from full CSV if pre-computed file not available."""
    df = load_clean_data()
    if df is None or 'countries_recoded' not in df.columns:
        return None
    df = df[df['topic'] != 'bla_bla'][['year', 'topic', 'country', 'countries_recoded']].copy()
    df['countries_recoded'] = df['countries_recoded'].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) and x != '[]' else []
    )
    exploded = df.explode('countries_recoded').rename(columns={'countries_recoded': 'country_mentioned'})
    exploded = exploded[exploded['country_mentioned'].notna()]
    exploded['country_mentioned'] = exploded['country_mentioned'].apply(clean_country)
    exploded = exploded[~exploded['country_mentioned'].isin(to_drop)]
    result = exploded.groupby(['year', 'topic', 'country_mentioned']).size().reset_index(name='country_count')
    return result


def get_data():
    precomputed = load_mentioned_countries_precomputed()
    if precomputed is not None:
        return precomputed
    df = load_mentioned_countries()
    if df is not None:
        return df
    if not USE_LOCAL_MODE:
        query = f"""WITH unsetted AS (
        SELECT * FROM {BIG_QUERY},
        UNNEST(countries_recoded) as country_mentioned)
        SELECT year, topic, country_mentioned, COUNT(country) as country_count from unsetted
        WHERE topic != "bla_bla"
        GROUP BY year, topic, country_mentioned"""
        df = pd.DataFrame(run_query(query))
        if not df.empty:
            df['country_mentioned'] = df['country_mentioned'].apply(clean_country)
            df = df[~df['country_mentioned'].isin(to_drop)]
        return df
    return None


df = get_data()

if df is None or df.empty:
    st.warning("No data available.")
else:
    _all_topics = sorted(df['topic'].unique())
    _topic_p = st.query_params.get("topic", "peace_war_security")
    _topic_idx = _all_topics.index(_topic_p) if _topic_p in _all_topics else 0
    topic = st.selectbox('Select topic', _all_topics, index=_topic_idx, format_func=format_topic)
    st.query_params["topic"] = topic
    df_topic = df[df['topic'] == topic]

    # ── Line chart: top 5 countries over all years ────────────────────────────
    top_5 = (df_topic.groupby('country_mentioned')['country_count']
             .sum().sort_values(ascending=False)
             .head(5).index.tolist())
    df_plot = df_topic[df_topic['country_mentioned'].isin(top_5)]

    years = sorted(df_topic['year'].unique())

    fig = px.line(
        df_plot, x='year', y='country_count', color='country_mentioned',
        title=f'Top 5 most mentioned countries — {format_topic(topic)}',
        labels={'year': 'Year', 'country_count': 'Mentions', 'country_mentioned': 'Country'},
        markers=True,
        line_shape='spline',
    )
    fig.update_layout(height=400, legend_title_text='')

    event = st.plotly_chart(
        fig, use_container_width=True,
        on_select="rerun", selection_mode=["points"],
        key="country_line",
    )
    st.caption("Click a point on the chart to update the map for that year.")

    # Determine selected year from click or fall back to latest
    selected_year = years[-1]
    if event and event.selection and event.selection.points:
        selected_year = int(event.selection.points[0]['x'])

    # ── Bubble map ────────────────────────────────────────────────────────────
    df_map_year = df_topic[df_topic['year'] == selected_year]
    df_map = (df_map_year.groupby('country_mentioned')['country_count']
              .sum().reset_index()
              .sort_values('country_count', ascending=False))

    st.subheader(f'Most mentioned countries in {selected_year} — {format_topic(topic)}')
    if df_map.empty:
        st.info("No country mentions recorded for this year and topic.")
    else:
        fig_map = px.scatter_geo(
            df_map,
            locations='country_mentioned',
            locationmode='country names',
            size='country_count',
            color='country_count',
            hover_name='country_mentioned',
            color_continuous_scale='Reds',
            size_max=50,
            projection='natural earth',
            labels={'country_count': 'Mentions'},
        )
        fig_map.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=450,
            coloraxis_showscale=False,
            geo=dict(
                showland=True, landcolor='#f0f0f0',
                showocean=True, oceancolor='#d6eaf8',
                showcoastlines=True, coastlinecolor='#aaaaaa',
                showframe=False,
            ),
        )
        st.plotly_chart(fig_map, use_container_width=True)

import streamlit.components.v1 as components
with st.expander("🔗 Share this view"):
    components.html(
        """<div style="display:flex;gap:8px;align-items:center;font-family:sans-serif;">
        <input id="u" readonly style="flex:1;padding:6px 10px;border:1px solid #ccc;border-radius:6px;font-size:13px;background:#f9f9f9;">
        <button onclick="navigator.clipboard.writeText(document.getElementById('u').value);this.textContent='✓ Copied';setTimeout(()=>this.textContent='Copy link',1500)"
          style="padding:6px 14px;background:#009EDB;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;white-space:nowrap;">Copy link</button>
        </div><script>document.getElementById('u').value=window.location.href;</script>""",
        height=50,
    )
