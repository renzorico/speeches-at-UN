import umap
from bertopic import BERTopic

umap_model = umap.UMAP(n_neighbors=15, n_components=10, metric='cosine', low_memory=False)

def bertopic_model(text):
    topic_model = BERTopic(
        top_n_words = 10,
        n_gram_range = (1, 3),
        embedding_model = None,
        vectorizer_model = None,
        min_topic_size = 30,
        nbr_topics = 'HDBSCAN',
        umap_model=umap_model
        )
    topics, probs = topic_model.fit_transform(text)
    return topic_model, topics, probs
