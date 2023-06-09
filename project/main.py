from data import load_data, harmonize_data
from preprocessing import basic_cleaning, preproc
from tfidf import tfidf_vec
import pandas as pd
from bert import bertopic_model, bert_topics
from params import DATA_PATH

def data_control():
    data = load_data()
    print("✅ data loaded")
    data = harmonize_data(data)
    print("✅ data harmonized")

    data.loc[:, ['cleaned']] = data['speeches'].apply(basic_cleaning)
    print("✅ data cleaned")
    data[['preprocessed', 'entities']] = data['speeches'].apply(preproc).apply(pd.Series)
    print("✅ data preprocessed")
    data.loc[:, ['preprocessed']] = data['preprocessed'].apply(" ".join)

    return data

data = pd.read_csv(DATA_PATH)

# model --> BERT, embedding, umap, auto
# model --> BERT, embedding, PCA, kmeans
model = bertopic_model(data['preprocessed'].dropna())
print("✅ initialized BERT model")
df_topics, doc_topics = bert_topics(model, data['preprocessed'])
print("✅ created topic dataframes")

# Save data in appropriate csv
