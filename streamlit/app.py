import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from data import load_data, load_stopwords
from words_cloud import display_wordcloud

def select_params(data_dict):
    years = sorted(list(set([key[0] for key in data_dict.keys()])))
    selected_year = st.selectbox("Select a year", years + ['Select All'])
    countries = sorted(list(set([str(key[1]) for key in data_dict.keys()])))
    selected_country = st.selectbox("Select a country", countries + ['Select All'])
    return selected_year, selected_country

def main():
    st.title("Data Analysis")

    data = load_data()
    stop_words = load_stopwords()
    data_dict = data.set_index(['year', 'country'])['speeches'].to_dict()

    selected_year, selected_country = select_params(data_dict)

    # Display the word cloud using Matplotlib
    wordcloud = display_wordcloud(data_dict, stop_words, selected_year, selected_country)
    st.subheader("Word Cloud")
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear', cmap='YlOrBr')
    plt.axis("off")
    st.pyplot(plt)

main()
