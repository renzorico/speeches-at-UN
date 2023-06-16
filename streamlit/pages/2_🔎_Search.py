import streamlit as st
st.set_page_config(layout="wide")
import matplotlib.pyplot as plt
from format_search import display_search
from words_cloud import display_wordcloud
from data import get_data_wordcloud, get_countries, get_years, get_topic


def search_main():
    st.title("Speech Search")
    col1, col2 = st.columns(2)
    with col1:
        search_text = st.text_input("Enter the text to search:", value='cartel')
    with col2:
        topic_selection = st.selectbox('Select topic:', get_topic(), index=4)
    display_search(search_text,topic_selection)


    st.title("WordCloud")
    _, stop_words, data_dict = get_data_wordcloud()
    # selected_year, selected_country = select_params(data_dict, '2')
    years = get_years()
    countries = get_countries()

    selected_year = st.selectbox('Select a year:', years,index=9)
    selected_country = st.selectbox('Select a country:', countries, index=36)
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


search_main()
