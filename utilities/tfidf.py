import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_vec(text):
    vectorizer = TfidfVectorizer(ngram_range=(2, 3), max_features=2000, stop_words=stop_words)
    X = vectorizer.fit_transform(text)
    X_array = X.toarray()

    print("✅ data vectorized")

    return X_array


#  df = pd.DataFrame(results, columns=vectorizer.get_feature_names_out())
