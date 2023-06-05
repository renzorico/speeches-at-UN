import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_vec(text):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(text)
    X_array = X.toarray()
    df = pd.DataFrame(X_array, columns=vectorizer.get_feature_names_out())
    return df
