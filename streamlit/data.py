import pandas as pd
from nltk.corpus import stopwords

def load_data():
    data = pd.read_csv('/root/code/renzorico/speeches-at-UN/raw_data/short_preprocessed_text.csv')
    data.dropna(inplace=True)
    df_topics = pd.read_csv('/root/code/renzorico/speeches-at-UN/raw_data/df_topics.csv')
    doc_topics = pd.read_csv('/root/code/renzorico/speeches-at-UN/raw_data/doc_topics.csv')
    doc_topics.dropna(inplace=True)
    return df_topics, doc_topics, data

def load_stopwords():
    stop_words = set(stopwords.words('english'))
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
    stop_words = stop_words + custom_stopwords
    return stop_words
