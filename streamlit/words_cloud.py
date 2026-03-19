from wordcloud import WordCloud
import streamlit as st


max_words = 50
color_map = 'Blues'

def select_params(data_dict, key):
    years = sorted(list(set([k[0] for k in data_dict.keys()])))
    default_year_idx = years.index(2016) if 2016 in years else len(years) - 1
    selected_year = st.selectbox("Select a year", years + ['Select All'], index=default_year_idx)

    countries = sorted(list(set([str(k[1]) for k in data_dict.keys()])))
    default_country = 'United Kingdom'
    default_country_idx = countries.index(default_country) if default_country in countries else 0
    selected_country = st.selectbox("Select a country", countries + ['Select All'], key=key, index=default_country_idx)
    return selected_year, selected_country

def generate_merged_word_cloud(data, stop_words):
    wordcloud = WordCloud(max_words=max_words, stopwords=stop_words, colormap=color_map,
                          prefer_horizontal=0.9,
                          background_color='white').generate(data)
    return wordcloud

def generate_specific_word_cloud(year, country, data_dict, stop_words):
    wordcloud = WordCloud(max_words=max_words, stopwords=stop_words, colormap=color_map,
                          prefer_horizontal=0.9,
                          background_color='white').generate(data_dict[(year,country)])
    return wordcloud

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
