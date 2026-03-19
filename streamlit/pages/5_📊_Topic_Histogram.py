import streamlit as st
from topicplot import display_topics, select_topic_hist

st.set_page_config(layout="wide", page_title="Topic Histogram | UN Speeches", page_icon="🌍")


def hist_main():
    st.title("Topic Histogram")
    st.caption("Total paragraphs classified under each topic across all years and countries.")
    display_topics()
    result = select_topic_hist()
    if result:
        words_list, count = result
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Paragraphs in topic", f"{count:,}")
        with col2:
            st.markdown("**Top keywords**")
            tags = " ".join([
                f'<span style="background-color:#e8f4ea; padding:4px 12px; border-radius:12px; margin:3px; display:inline-block;">{w}</span>'
                for w in words_list
            ])
            st.markdown(tags, unsafe_allow_html=True)


hist_main()

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
