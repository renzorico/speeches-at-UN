import streamlit as st
import matplotlib.pyplot as plt
from words_cloud import display_wordcloud, select_params
from data import get_data_wordcloud


def wordcloud_main():
    st.title("Data Analysis")
    _, stop_words, data_dict = get_data_wordcloud()
    selected_year, selected_country = select_params(data_dict, '2')
    error_message = 'There is no data for your selection. Please choose another selection.'
    wordcloud = display_wordcloud(data_dict, stop_words, selected_year, selected_country)

    if wordcloud != error_message:
        st.subheader("Word Cloud")
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear', cmap='YlOrBr')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.write(error_message)

wordcloud_main()
