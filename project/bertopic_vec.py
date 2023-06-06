from bertopic import BERTopic


def bertopic(texts):
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(texts)

    return topic_model, topics, probs
