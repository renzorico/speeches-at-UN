from pathlib import Path
import nltk
nltk.download('stopwords', quiet=True)

import pandas as pd
from data import load_data, harmonize_data
from preprocessing import basic_cleaning
from bert import bertopic_model, bert_topics

def data_control():
    data = load_data()
    print("✅ data loaded")
    data = harmonize_data(data)
    print("✅ data harmonized")
    data.loc[:, ['cleaned']] = data['speeches'].apply(basic_cleaning)
    print("✅ data cleaned")
    return data

output_path = Path(__file__).parent.parent / 'raw_data' / 'clean_data.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)

clean_data = data_control()

# Run BERTopic on cleaned text
valid_mask = clean_data['cleaned'].notna() & (clean_data['cleaned'] != '')
text_list = clean_data.loc[valid_mask, 'cleaned'].tolist()
valid_indices = clean_data.loc[valid_mask].index

print(f"Running BERTopic on {len(text_list)} speeches...")
topic_model, topics, probs = bertopic_model(text_list)
print("✅ BERTopic model fitted")

# Assign topic IDs back to the dataframe
clean_data.loc[valid_indices, 'topic_id'] = topics
clean_data['topic_id'] = clean_data['topic_id'].fillna(-1).astype(int)

# Build topic label lookup: topic_id -> human-readable name (top words joined)
topic_info = topic_model.get_topic_info()
label_map = {}
top_words_map = {}
for _, row in topic_info.iterrows():
    tid = int(row['Topic'])
    label_map[tid] = row['Name']
    words = topic_model.get_topic(tid)
    top_words_map[tid] = str([w for w, _ in words[:5]])

clean_data['topic'] = clean_data['topic_id'].map(label_map)
clean_data.to_csv(output_path, index=False)
print("✅ saved clean_data.csv with topic columns")

# Save topic metadata (for streamlit get_topic() and top words)
rows = []
for _, row in topic_info.iterrows():
    tid = int(row['Topic'])
    if tid == -1:
        continue
    rows.append({
        'topic_id': tid,
        'topic_name': row['Name'],
        'count': int(row['Count']),
        'top_5_words': top_words_map[tid],
    })

topic_words_path = output_path.parent / 'topic_words.csv'
pd.DataFrame(rows).to_csv(topic_words_path, index=False)
print(f"✅ saved {len(rows)} topics to topic_words.csv")
