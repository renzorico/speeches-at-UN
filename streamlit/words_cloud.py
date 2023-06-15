from wordcloud import WordCloud
import streamlit as st
import numpy as np
from PIL import Image
from os import path
import nltk
nltk.download('stopwords')
# from matplotlib.colors import ListedColormap

'''
Defines functions that are used in Streamlit app to generate WordsClouds
'''



# colors = ['#003366', '#006633', '#660066', '#663300', '#333333', '#800000', '#000080', '#556B2F', '#003333', '#36454F']
# custom_cmap = ListedColormap(colors)
max_words = 200
color_map = 'copper_r'
background = 'white'

# d = path.dirname('/root/code/renzorico/speeches-at-UN/streamlit/raw_data/')
# mask = np.array(Image.open(path.join(d, "trump.png")))


def generate_merged_word_cloud(data, stop_words):
    wordcloud = WordCloud(max_words=max_words, stopwords=stop_words, colormap=color_map,
                          prefer_horizontal=0.9,
                          background_color=background).generate(data)
    return wordcloud

def generate_specific_word_cloud(year, country, data_dict, stop_words):
    wordcloud = WordCloud(max_words=max_words, stopwords=stop_words, colormap=color_map,
                          prefer_horizontal=0.9,
                          background_color=background).generate(data_dict[(year,country)])
    return wordcloud



# Need to change to integrate year_range

def display_wordcloud(data_dict, stop_words, selected_year, selected_country):
    if selected_year == 'Select All' and selected_country == 'Select All':
        # Generate word cloud for all years and countries
        keys_to_merge = [pair for pair in data_dict.keys()]
        merged_values = ' '.join(data_dict[key] for key in keys_to_merge)
        wordcloud = generate_merged_word_cloud(merged_values, stop_words)
        return wordcloud
    elif selected_year == 'Select All':
        # Gnerate word cloud for all years, specific country
        keys_to_merge = set([(pair[0], selected_country) for pair in data_dict.keys()])
        merged_values = ' '.join(data_dict[key] for key in keys_to_merge if key in data_dict.keys())
        stop_words = stop_words + [selected_country]
        wordcloud = generate_merged_word_cloud(merged_values, stop_words)
        return wordcloud
    elif selected_country == 'Select All':
        # Generate word cloud for specific year, all countries
        keys_to_merge = set([(selected_year, pair[1]) for pair in data_dict.keys()])
        merged_values = ' '.join(data_dict[key] for key in keys_to_merge if key in data_dict.keys())
        wordcloud = generate_merged_word_cloud(merged_values, stop_words)
        return wordcloud
    else:
        # Generate word cloud for specific year and country
        stop_words = stop_words + [selected_country]
        error_message = 'There is no data for your selection. Please choose another selection.'
        response = data_dict.get((selected_year, selected_country), error_message)
        if response != error_message:
            wordcloud = generate_specific_word_cloud(selected_year, selected_country, data_dict, stop_words)
            return wordcloud
        else:
            return error_message
