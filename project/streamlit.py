import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('/root/code/renzorico/speeches-at-UN/raw_data/short_preprocessed_text.csv')

custom_stopwords = #needs to be defined

@st.cache
def generate_word_cloud(year, country):
    # In this function, you can extract the important words for the given year and country
    # Replace this code with your actual word extraction logic

    data_dict = data.set_index(['year', 'country'])['cleaned'].to_dict()

    document = data_dict.get((year, country), "")
    wordcloud = WordCloud(max_words=100, stopwords=custom_stopwords).generate(document)
    return wordcloud

@st.cache
def generate_topic_counts(year_range, countries):
    # In this function, you can use your BERT model to generate topics for your corpus and count the number of documents for each topic
    # Replace this code with your actual topic generation and counting logic
    df = pd.DataFrame(topics_data)
    filtered_df = df[df['Year'].between(year_range[0], year_range[1]) & df['Country'].isin(countries)]
    topic_counts = filtered_df['Topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Document Count']
    return topic_counts

def display_topic_words(topic):
    # Find the words for the selected topic
    words = topics_data[topics_data['Topic'] == topic]['Words'].values[0]

    # Create a dataframe to display the words
    df = pd.DataFrame(words, columns=['Words'])
    st.write(df)

def main():
    st.title("Data Analysis")

    # Select the year from a dropdown menu
    years = sorted(list(set([key[0] for key in document_data.keys()])))
    selected_year = st.selectbox("Select a year", years + ['Select All'])

    # Select the country from a dropdown menu
    countries = sorted(list(set([key[1] for key in document_data.keys()])))
    selected_country = st.selectbox("Select a country", countries + ['Select All'])

    # Generate word cloud for the selected year and country
    if selected_year == 'Select All' and selected_country == 'Select All':
        # Generate word cloud for all years and countries
        wordcloud = generate_word_cloud(years, countries)
    elif selected_year == 'Select All':
        # Generate word cloud for all years, specific country
        wordcloud = generate_word_cloud(years, selected_country)
    elif selected_country == 'Select All':
        # Generate word cloud for specific year, all countries
        wordcloud = generate_word_cloud(selected_year, countries)
    else:
        # Generate word cloud for specific year and country
        wordcloud = generate_word_cloud(selected_year, selected_country)

    # Display the word cloud using Matplotlib
    st.subheader("Word Cloud")
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

    # Generate topic counts based on selected year(s) and country(s)
    min_year = min(years) if selected_year == 'Select All' else int(selected_year)
    max_year = max(years) if selected_year == 'Select All' else int(selected_year)
    year_range = [min_year, max_year]

    selected_countries = countries if selected_country == 'Select All' else [selected_country]

    topic_counts = generate_topic_counts(year_range, selected_countries)

    # Display the topic counts as a bar plot
    st.subheader("Topic Document Counts")
    fig = px.bar(topic_counts, x='Topic', y='Document Count',
                 labels={'Topic': 'Topic', 'Document Count': 'Document Count'},
                 title="Topic Document Counts")

    fig.update_layout(width=800, height=500)

    # Add click event to the bar plot
    fig.update_traces(marker=dict(color='rgb(158,202,225)', opacity=0.6),
                      selected_marker=dict(color='black'),
                      unselected_marker=dict(color='rgb(158,202,225)', opacity=0.6),
                      selected=dict(marker=dict(opacity=1)))
    fig.update_layout(clickmode='event+select')

    selected_topic = None

    # Check if a bar is clicked
    if st.plotly_chart(fig, use_container_width=True):
        selected_data = px.get_click_data()
        if selected_data and selected_data['points']:
            selected_topic = selected_data['points'][0]['x']

    if selected_topic:
        st.subheader(f"Words for the topic: {selected_topic}")
        display_topic_words(selected_topic)
