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
