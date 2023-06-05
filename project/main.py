from data import load_data
from preprocessing import basic_cleaning, preproc
from tfidf import tfidf_vec

data = load_data()

df = data[:10]
df.loc[:, ['cleaned']] = df['speeches'].apply(basic_cleaning)
df.loc[:, ['preprocessed']] = df['cleaned'].apply(preproc)

results = df['preprocessed'].apply(tfidf_vec)

print(results)
