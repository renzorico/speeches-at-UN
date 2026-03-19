import streamlit as st
st.set_page_config(layout="wide", page_title="Speech Search | UN Speeches", page_icon="🌍")
from format_search import display_search
from data import get_topic, USE_LOCAL_MODE, format_topic


def main():
    st.title("Speech Search")
    st.caption("Search across all 117,000+ paragraphs. Use the topic filter to narrow results.")

    _p = st.query_params
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        search_text = st.text_input("Enter the text to search:", value=_p.get("q", "war"))

    topics = [t for t in get_topic() if t != 'bla_bla']
    with col2:
        _topic_p = _p.get("topic", None)
        _topic_list = [None] + topics
        _topic_idx = _topic_list.index(_topic_p) if _topic_p in _topic_list else 0
        topic_selection = st.selectbox(
            'Topic',
            _topic_list,
            index=_topic_idx,
            format_func=lambda t: 'All Topics' if t is None else format_topic(t),
        )
    with col3:
        sort_order = st.selectbox('Sort by', ['Most recent', 'Oldest first'])

    st.query_params["q"] = search_text
    if topic_selection:
        st.query_params["topic"] = topic_selection
    elif "topic" in st.query_params:
        del st.query_params["topic"]

    display_search(search_text, topic_selection, sort_order)

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


main()
