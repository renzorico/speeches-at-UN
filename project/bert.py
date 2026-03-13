# import umap
from bertopic import BERTopic
import pandas as pd
import numpy as np
import pycountry
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

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


def bertopic_model(text):
    vectorizer_model = CountVectorizer(stop_words=custom_stopwords, ngram_range=(1, 3), min_df=5, max_features=200)
    vectorized_text = vectorizer_model.fit_transform(text)
    topic_model = BERTopic(top_n_words=10, min_topic_size=5, nr_topics='auto')
    model = topic_model.fit_transform(vectorized_text)
    return model

def bert_topics(model, text):
    topic_words = model.get_topic_freq().apply(lambda row: model.get_topic(row[0]), axis=1)
    df_topics = pd.DataFrame({'Topic': topic_words.index, 'Words': topic_words.values})
    doc_topics = model.get_document_info(text)
    return df_topics, doc_topics
