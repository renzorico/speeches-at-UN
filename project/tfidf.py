import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
stop_words = list(stop_words)

def tfidf_vec(text):
    vectorizer = TfidfVectorizer(ngram_range=(2, 3), max_features=2000, stop_words=stop_words)
    X = vectorizer.fit_transform(text)
    X_array = X.toarray()
    df = pd.DataFrame(X_array, columns=vectorizer.get_feature_names_out())

    return df
