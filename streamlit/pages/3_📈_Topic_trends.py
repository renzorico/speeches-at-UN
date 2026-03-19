from graph_formating import generate_graph, select_topic, select_country
import streamlit as st

st.set_page_config(layout="wide", page_title="Topic Trends | UN Speeches", page_icon="🌍")


def graph_main():
    st.title("Topic Trends Over Time")
    st.caption("How often each topic appears in UN speeches per year, globally or for a specific country.")
    selected_topic = select_topic()
    selected_country = select_country('1')
    if not selected_topic:
        st.write('Please select a topic to plot.')
    else:
        generate_graph(selected_topic, selected_country)


graph_main()

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