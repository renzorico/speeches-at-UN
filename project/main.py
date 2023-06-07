from data import load_data, harmonize_data
from preprocessing import basic_cleaning, preproc
from tfidf import tfidf_vec
import pandas as pd
from bert import bertopic_model, bert_topics

data = load_data()
print("✅ data loaded")
data = harmonize_data(data)
print("✅ data harmonized")

df = data[:1000]

df.loc[:, ['cleaned']] = df['speeches'].apply(basic_cleaning)
print("✅ data cleaned")
df[['preprocessed', 'entities']] = df['speeches'].apply(preproc).apply(pd.Series)
print("✅ data preprocessed")
df.loc[:, ['preprocessed']] = df['preprocessed'].apply(" ".join)

model = bertopic_model(df['preprocessed'].dropna())
print("✅ initialized BERT model")
df_topics, doc_topics = bert_topics(model, df['preprocessed'])
print("✅ created topic dataframes")
