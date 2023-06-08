import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


speeches_df = pd.read_csv('/home/ricorenzo/code/renzorico/speeches-at-UN/raw_data/speeches_with_paragraphs_processed.csv')

count_topics = speeches_df.groupby(['year', 'topic']).size().reset_index(name='count')
selection_topic_1 = st.multiselect('Topic', speeches_df['topic'].unique())
filtered_df = count_topics.loc[count_topics['topic'].isin(selection_topic_1)]


fig, ax = plt.subplots()
sns.lineplot(data=filtered_df, x='year', y='count', hue='topic', ax=ax)
ax.set_title('Count of Topics Over Years')
st.pyplot(fig)
