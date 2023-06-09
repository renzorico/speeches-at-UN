import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def select_topic(data):
    selected_topic = st.multiselect('Topic', data['Name'].unique())
    selected_country = st.multiselect('Topic', data['country'].unique())
    return selected_topic, selected_country


def generate_graph(data):
    count_topics = data.groupby(['year', 'Name']).size().rest_index(name='count')
    selected_topics, selected_country = select_topic(data)
    filtered_df = count_topics.loc[count_topics['topic'].isin(selected_topics)]
    filtered_df = filtered_df.loc[filtered_df['topic'].isin(selected_country)]

    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_df, x='year', y='count', hue='topic', ax=ax)
    ax.set_title('Evolution of Topics Over the Years')
    st.pyplot(fig)
