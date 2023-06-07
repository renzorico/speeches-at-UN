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

    df_topics, doc_topics, data = load_data()
    stop_words = load_stopwords()
    data_dict = data.set_index(['year', 'country'])['cleaned'].to_dict()

    selected_year, selected_country = select_params(data_dict)

    # Display the word cloud using Matplotlib
    wordcloud = display_wordcloud(data_dict, stop_words, selected_year, selected_country)
    st.subheader("Word Cloud")
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear', cmap='YlOrBr')
    plt.axis("off")
    st.pyplot(plt)

    # # Display the topic counts as a bar plot
    # st.subheader("Topic Document Counts")
    # fig = px.bar(topic_counts, x='Topic', y='Document Count',
    #              labels={'Topic': 'Topic', 'Document Count': 'Document Count'},
    #              title="Topic Document Counts")

    # fig.update_layout(width=800, height=500)

    # # Add click event to the bar plot
    # fig.update_traces(marker=dict(color='rgb(158,202,225)', opacity=0.6),
    #                   selected_marker=dict(color='black'),
    #                   unselected_marker=dict(color='rgb(158,202,225)', opacity=0.6),
    #                   selected=dict(marker=dict(opacity=1)))
    # fig.update_layout(clickmode='event+select')

    # selected_topic = None

    # # Check if a bar is clicked
    # if st.plotly_chart(fig, use_container_width=True):
    #     selected_data = st.plotly_chart(fig).to_dict().get('clickData')
    #     if selected_data and selected_data['points']:
    #         selected_topic = selected_data['points'][0]['x']

    # if selected_topic:
    #     st.subheader(f"Words for the topic: {selected_topic}")
    #     display_topic_words(selected_topic, df_topics)

main()
