from data import load_count_topic_overtime, load_data

_ , doc_topics, data = load_data()
count_topics_df = load_count_topic_overtime(doc_topics, data)

def hist_main():
