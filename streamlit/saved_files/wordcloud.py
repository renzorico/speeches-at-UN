import streamlit as st
import matplotlib.pyplot as plt
from words_cloud import display_wordcloud
from data import get_data_wordcloud, get_countries, get_years


def wordcloud_main():
    st.title("WordCloud")
    _, stop_words, data_dict = get_data_wordcloud()
    # selected_year, selected_country = select_params(data_dict, '2')
    years = get_years()
    countries = get_countries()

    selected_year = st.selectbox('Select a year', years)
    selected_country = st.selectbox('Select a country', countries)
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
