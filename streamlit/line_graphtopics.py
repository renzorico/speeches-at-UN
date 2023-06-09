import streamlit as st
# import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def select_topic(data):
    selected_topic = st.multiselect('Topic', data['topic'].unique())
    # selected_country = st.multiselect('Country', data['country'].unique())

    return selected_topic


def generate_graph(selected_topic, data):
    count_topics = data.groupby(['year', 'topic']).size().reset_index(name='count')
    filtered_df = count_topics.loc[count_topics['topic'].isin(selected_topic)]


    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_df, x='year', y='count', hue='topic', ax=ax)
    ax.set_title('Count of Topics Over Years')
    st.pyplot(fig)
