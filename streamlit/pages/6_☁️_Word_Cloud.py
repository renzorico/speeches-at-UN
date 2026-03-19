import streamlit as st
import matplotlib.pyplot as plt
from words_cloud import display_wordcloud, select_params
from data import get_data_wordcloud

st.set_page_config(layout="wide", page_title="Word Cloud | UN Speeches", page_icon="🌍")


def wordcloud_main():
    st.title("Word Cloud")
    _, stop_words, data_dict = get_data_wordcloud()
    if not data_dict:
        st.warning("Speech data is not available. Check your data source configuration.")
        return
    selected_year, selected_country = select_params(data_dict, '2')
    error_message = 'There is no data for your selection. Please choose another selection.'
    wordcloud = display_wordcloud(data_dict, stop_words, selected_year, selected_country)

    if wordcloud != error_message:
        st.subheader("Word Cloud")
        plt.figure(figsize=(70, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.write(error_message)

wordcloud_main()

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
