from data import load_data
from preprocessing import basic_cleaning, preproc
from tfidf import tfidf_vec
from bertopic_vec import bertopic
data = load_data()

df = data[:10]
df.loc[:, ['cleaned']] = df['speeches'].apply(basic_cleaning)
df.loc[:, ['preprocessed']] = df['cleaned'].apply(preproc)
df.loc[:, ['preprocessed']] = df['preprocessed'].apply(" ".join)
breakpoint()
results = df['preprocessed'].apply(tfidf_vec)
model, topics, probs = bertopic(df['preprocessed'])

print(model.get_topic_info())
print(results)
