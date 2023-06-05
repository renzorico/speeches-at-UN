
from project.data import load_data
from project.preprocessing import basic_cleaning, preproc
from project.tfidf import tfidf_vec

data = load_data()

df = data[:50]
df.loc[:, 'cleaned'] = df['speeches'].apply(basic_cleaning)
df.loc[:, 'preprocessed'] = df['cleaned'].apply(preproc)

results = tfidf_vec(df['preprocessed'])
results.head()
