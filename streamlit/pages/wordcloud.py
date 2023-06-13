import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from data import load_data, load_stopwords, format_df
from words_cloud import display_wordcloud, select_params

data = load_data()
data = format_df(data)
stop_words = load_stopwords()
data_dict = data.set_index(['year', 'country'])['speeches'].to_dict()
selected_year, selected_country = select_params()

query =

def wordcloud_main():
    st.title("Data Analysis")
    selected_year, selected_country = select_params(data_dict)
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
