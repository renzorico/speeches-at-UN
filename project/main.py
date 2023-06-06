from data import load_data, harmonize_data
from preprocessing import basic_cleaning, preproc
from tfidf import tfidf_vec
<<<<<<< HEAD
#from bert import bertopic_model
import pandas as pd

=======
from bertopic_vec import bertopic
>>>>>>> 359abae63046464d5cfee8ce038a88a9454ff127
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
<<<<<<< HEAD

df.to_csv('/root/code/renzorico/speeches-at-UN/raw_data/short_preprocessed_text.csv')

# model, topics, results = bertopic_model(list(df['preprocessed']))

# print(model.get_topic_info())
# print(results)
=======
breakpoint()
results = df['preprocessed'].apply(tfidf_vec)
model, topics, probs = bertopic(df['preprocessed'])

print(model.get_topic_info())
print(results)
>>>>>>> 359abae63046464d5cfee8ce038a88a9454ff127
