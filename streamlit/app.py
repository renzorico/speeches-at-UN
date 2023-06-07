import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from data import load_data, load_stopwords
from words_cloud import display_wordcloud


# @st.cache_data
# def generate_topic_counts(year_range, countries, doc_topics, data):
#     # In this function, you can use your BERT model to generate topics for your corpus and count the number of documents for each topic
#     # Replace this code with your actual topic generation and counting logic

#     # df is created with get topics from BERT
#     df_topics = pd.DataFrame(doc_topics.drop(columns=['Representative_Docs', 'Probability', 'Representative_document']))

#     # needs to merge on index with original dataframe with only year, speech, and country
#     df_topics = df_topics.merge(data[['year', 'country']], left_index=True, right_index=True)

#     filtered_df = df_topics[df_topics['year'].between(year_range[0], year_range[1]) & df_topics['country'].isin(countries)]
#     topic_counts = filtered_df['Topic'].value_counts().reset_index()
#     topic_counts.columns = ['Topic', 'Document Count']
#     return topic_counts

# def display_topic_words(topic, df_topics):
#     # Find the words for the selected topic
#     words = df_topics[df_topics['Topic'] == topic]['Words'].values[0]

#     # Create a dataframe to display the words
#     df = pd.DataFrame(words, columns=['Words'])
#     st.write(df)

def main():
    st.title("Data Analysis")

    df_topics, doc_topics, data = load_data()
    stop_words = load_stopwords()
    data_dict = data.set_index(['year', 'country'])['cleaned'].to_dict()

    # Display the word cloud using Matplotlib
    wordcloud = display_wordcloud(data_dict, stop_words)
    st.subheader("Word Cloud")
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear', cmap='YlOrBr')
    plt.axis("off")
    st.pyplot(plt)

    # Generate topic counts based on selected year(s) and country(s)
    min_year = min(years) if selected_year == 'Select All' else int(selected_year)
    max_year = max(years) if selected_year == 'Select All' else int(selected_year)
    year_range = [min_year, max_year]

    selected_countries = countries if selected_country == 'Select All' else [selected_country]

    topic_counts = generate_topic_counts(year_range, selected_countries, doc_topics, data)

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
        selected_data = st.plotly_chart(fig).to_dict().get('clickData')
        if selected_data and selected_data['points']:
            selected_topic = selected_data['points'][0]['x']

    if selected_topic:
        st.subheader(f"Words for the topic: {selected_topic}")
        display_topic_words(selected_topic, df_topics)

main()
