import streamlit as st
import numpy as np
import pandas as pd
from data import get_topic, get_years, run_query, BIG_QUERY, load_topics_meta, USE_LOCAL_MODE, format_topic
from plot_map import plot_geo_features

st.set_page_config(layout="wide", page_title="Speech Map | UN Speeches", page_icon="🌍")


def map_main():
    st.title("Speech Map")
    st.caption("Which countries focused on which topics, year by year. Colour intensity shows the number of paragraphs classified under the selected topic.")

    with st.spinner("Loading geographic data, this may take a few seconds…"):
        years = get_years()
        years = [int(y) for y in years]

    _p = st.query_params
    _y0, _y1 = min(years), max(years)
    _start = max(_y0, min(_y1, int(_p.get("year_start", 2015))))
    _end   = max(_y0, min(_y1, int(_p.get("year_end",   2021))))

    start_year, end_year = st.slider(
        "Select a year range",
        min_value=_y0, max_value=_y1,
        value=(_start, _end)
    )
    topics = [t for t in get_topic() if t != 'bla_bla']
    _topic_p = _p.get("topic", "peace_war_security")
    default_idx = topics.index(_topic_p) if _topic_p in topics else (
        topics.index('peace_war_security') if 'peace_war_security' in topics else 0
    )
    selected_topic = st.selectbox('Select topic', topics, index=default_idx, format_func=format_topic)
    st.query_params["year_start"] = start_year
    st.query_params["year_end"]   = end_year
    st.query_params["topic"]      = selected_topic

    with st.spinner("Building map…"):
        df = load_topics_meta()
        if df is not None and selected_topic:
            filtered = df[
                (df['topic'] == selected_topic) &
                (df['year'] >= start_year) &
                (df['year'] <= end_year)
            ]
            df_map = filtered.groupby(['year', 'country', 'topic']).size().reset_index(name='counts')
        elif not USE_LOCAL_MODE and selected_topic:
            geo_query = f'''
                    SELECT year, country, topic, COUNT(speeches) as counts FROM {BIG_QUERY}
                    WHERE topic = "{selected_topic}"
                    AND year >= {start_year}
                    AND year <= {end_year}
                    GROUP BY year, country, topic
                    ORDER BY year ASC
                    '''
            df_map = pd.DataFrame(run_query(geo_query))
        else:
            st.warning("No data available.")
            return

    st.subheader(f"Countries focused on {format_topic(selected_topic)} — {start_year}–{end_year}")
    st.caption("Colour intensity shows the number of paragraphs classified under this topic. Hover over a country to see the count.")
    plot_geo_features(df_map)

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


map_main()
