import streamlit as st
import pandas as pd
import seaborn as sns

speeches_df = pd.read_csv('/raw_data/speeches_with_paragraphs_processed.csv')


count_topics = speeches_df.groupby(['country','year','topic'])[['iso']].count()
# ---> selection = st.selectbox('country', ['Spain', 'Portugal'])

options = list(set(speeches_df['topic']))

# ---> st.write(selection)


df_ = count_topics.reset_index().rename({'iso':'count'}, axis=1)
df_['count'] = 1
war_df = df_.loc[df_.topic == options]
war_df =war_df.groupby(['year'])[['topic']].count().reset_index().rename({'topic':'count'}, axis=1)


climate = df_.loc[df_.topic == options]
climate = climate.groupby(['year'])[['topic']].count().reset_index().rename({'topic':'count'}, axis=1)

sns.lineplot(war_df,x='year', y='count')
sns.lineplot(climate,x='year', y='count')
