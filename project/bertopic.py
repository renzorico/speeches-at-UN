from bertopic import BERTopic

topic_model = BERTopic()
topics, probs = topic_model.fit_transform(df)

topic_model.get_topic_info(docs)

def bertopic(text):
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(text)

    return topics, probs
