import streamlit as st
import pandas as pd

'''
Defines functions to keep track of topics in texts and display them in histplots (counting texts by topic, zooming in on particular topics)
'''

def display_topic_words(topic, df_topics):
    # Find the words for the selected topic
    words = df_topics[df_topics['Topic'] == topic]['Words'].values[0]

    # Create a dataframe to display the words
    df = pd.DataFrame(words, columns=['Words'])
    st.write(df)

def select_topics(years, doc_topics, data):
    # Generate topic counts based on selected year(s) and country(s)
    selected_year = st.selectbox("Select a year", years + ['Select All'])

    min_year = min(years) if selected_year == 'Select All' else int(selected_year)
    max_year = max(years) if selected_year == 'Select All' else int(selected_year)
    year_range = [min_year, max_year]

    selected_countries = countries if selected_country == 'Select All' else [selected_country]

    topic_counts = generate_topic_counts(year_range, selected_countries, doc_topics, data)
