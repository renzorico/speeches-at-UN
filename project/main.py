from data import load_data, harmonize_data
from preprocessing import basic_cleaning, preproc
from tfidf import tfidf_vec
#from bert import bertopic_model
import pandas as pd

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

df.to_csv('/root/code/renzorico/speeches-at-UN/raw_data/short_preprocessed_text.csv')

# model, topics, results = bertopic_model(list(df['preprocessed']))

# print(model.get_topic_info())
# print(results)
