# import umap
from bertopic import BERTopic
import pandas as pd
import numpy as np
import pycountry
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords', quiet=True)

# umap_model = umap.UMAP(n_neighbors=15, n_components=10, metric='cosine', low_memory=False)

countries = list(pycountry.countries)
country_names = [country.name.lower() for country in countries]

stop_words = set(stopwords.words('english'))
# stop_words.add('country')
# stop_words.update(country_names)
stop_words = list(stop_words)

custom_stopwords = ['united nations','united states', 'international community', 'human rights',
                    'security council', 'general assembly', 'middle east','international law',
                    'international community', 'international criminal', 'international criminal court',
                    'international peace', 'international security', 'international tribunal',
                    'international cooperation', 'south africa', 'european union', 'african union',
                    'united kingdom', 'united nations security', 'united nations general', 'united nations general assembly',
                    'soviet union', 'latin america', 'north america', 'south america', 'viet nam','central america',
                    'east asia', 'south asia', 'south east asia', 'eastern europe', 'western europe', 'el salvador',
                    'indian ocean', 'pacific ocean', 'atlantic ocean', 'arab league', 'european','siere leone', 'sierra leone',
                    'sierra leonean', 'sierra leoneans', 'costa rica', 'per cent', 'mr president', 'small island',
                    'democratic republic', 'people republic', 'republic congo', 'republic iran', 'republic korea',
                    'european community', "united", "nations", "people", "shall", "president", 'delegation',
                    'world', 'herzegovina']


def bertopic_model(text_list):
    """
    Fit BERTopic model on text list.

    Args:
        text_list: List of text strings (raw text, not vectorized)

    Returns:
        topic_model: Fitted BERTopic model
    """
    vectorizer_model = CountVectorizer(stop_words=custom_stopwords, ngram_range=(1, 3), min_df=5, max_features=200)
    topic_model = BERTopic(vectorizer_model=vectorizer_model, language="english", min_topic_size=5, top_n_words=10)

    # BERTopic expects raw text list, not vectorized
    topics, probs = topic_model.fit_transform(text_list)
    return topic_model, topics, probs


def bert_topics(topic_model, topics):
    """
    Extract topics and document assignments from fitted BERTopic model.

    Args:
        topic_model: Fitted BERTopic model
        topics: Topic assignments for documents

    Returns:
        df_topics: DataFrame with topic info
        doc_topics: DataFrame with document-topic assignments
    """
    topic_freq = topic_model.get_topic_freq()
    df_topics = pd.DataFrame({
        'Topic_ID': topic_freq['Topic'].values,
        'Frequency': topic_freq['Frequency'].values
    })

    # Create document-topic dataframe
    doc_topics = pd.DataFrame({'Topic': topics})

    return df_topics, doc_topics
