
from data import load_data
from preprocessing import basic_cleaing, preproc

data = load_data()

df = data[:50]

df['cleaned'] = df['speeches'].apply(basic_cleaing)
df['preprocessed'] = df['cleaned'].apply(preproc)

df['preprocessed'] = df['preprocessed'].apply(" ".join)
