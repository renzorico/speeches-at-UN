# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt


# speeches_df = pd.read_csv('/home/ricorenzo/code/renzorico/speeches-at-UN/raw_data/speeches_with_paragraphs_processed.csv')

# count_topics = speeches_df.groupby(['year', 'topic']).size().reset_index(name='count')
# selection_topic_1 = st.multiselect('Topic', speeches_df['topic'].unique())
# filtered_df = count_topics.loc[count_topics['topic'].isin(selection_topic_1)]


# fig, ax = plt.subplots()
# sns.lineplot(data=filtered_df, x='year', y='count', hue='topic', ax=ax)
# ax.set_title('Count of Topics Over Years')
# st.pyplot(fig)


import streamlit as st
from google.oauth2 import service_account
import pandas as pd
from google.cloud import bigquery
# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows
# Load 10 rows
rows = run_query("SELECT * FROM `lewagon-bootcamp-384011.production_dataset.speeches` LIMIT 10")

unique_topics_query= 'SELECT DISTINCT topic FROM `lewagon-bootcamp-384011.production_dataset.speeches` WHERE topic != "bla_bla"'

unique_topics = run_query(unique_topics_query)
# st.write(unique_topics)
unique_topics = pd.DataFrame(unique_topics).topic.values
# Show first 10 rows of DataFrame
df = pd.DataFrame(rows)
st.dataframe(df)
topic_1 = st.selectbox('Select topic one', unique_topics)
topic_2 = st.selectbox('Select topic two', unique_topics)
topic_3 = st.selectbox('Select topic three', unique_topics)

button = st.button('Plot change of topic over time')
if button:
    topic_results = run_query(f'''SELECT year , topic, COUNT(country) as mentions_count FROM `lewagon-bootcamp-384011.production_dataset.speeches`
                      WHERE topic IN ("{topic_1}", "{topic_2}", "{topic_3}")
                      GROUP BY year, topic
                      ORDER BY year ASC
                      ''')
    topic_df = pd.DataFrame(topic_results)
    compare_df = topic_df.pivot(index='year', columns='topic', values='mentions_count')
    st.line_chart(data=compare_df, width=0, height=0, use_container_width=True)
