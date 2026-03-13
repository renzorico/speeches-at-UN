"""
classify_topics.py
------------------
Classifies each paragraph in speeches_paragraphs.csv by cosine similarity to
the topic anchor paragraphs defined in raw_data/topic_definitions.csv.
Then regenerates UMAP embeddings and pre-computed aggregations used by the app.

No API key required. Runs entirely locally using Sentence Transformers.

Usage:
    cd project
    python classify_topics.py

Outputs:
    - data/speeches_paragraphs.csv         (updated 'topic' and 'topic_similarity' columns)
    - raw_data/topic_labels.csv            (regenerated topic metadata)
    - streamlit/speeches_umap.csv          (regenerated UMAP coordinates)
    - streamlit/mentioned_countries_agg.csv (pre-computed country mentions per year/topic)
"""

import ast
import sys
import numpy as np
import pandas as pd
import umap
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT          = Path(__file__).parent.parent
DATA_PATH             = PROJECT_ROOT / 'data'      / 'speeches_paragraphs.csv'
TOPICS_PATH           = PROJECT_ROOT / 'raw_data'  / 'topic_definitions.csv'
TOPIC_LABELS_OUT      = PROJECT_ROOT / 'raw_data'  / 'topic_labels.csv'
UMAP_OUT              = PROJECT_ROOT / 'streamlit' / 'speeches_umap.csv'
MENTIONED_COUNTRIES_OUT = PROJECT_ROOT / 'streamlit' / 'mentioned_countries_agg.csv'

# Import clean_countries from the streamlit directory
sys.path.insert(0, str(PROJECT_ROOT / 'streamlit'))
from clean_countries import clean_country, to_drop

BATCH_SIZE = 256
MODEL_NAME = 'all-mpnet-base-v2'


def regenerate_topic_labels(df: pd.DataFrame, topics_df: pd.DataFrame,
                             output_path: Path) -> None:
    rows = []
    for _, row in topics_df.iterrows():
        name     = row['Name']
        count    = int((df['topic'] == name).sum())
        keywords = [kw.strip() for kw in str(row['Short_keywords']).split(',')]
        rows.append({
            'topic_id':    int(row['Index']),
            'topic_name':  name,
            'count':       count,
            'top_5_words': str(keywords[:5]),
        })
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"✅ Saved topic_labels.csv ({len(rows)} topics)")


def regenerate_umap(df: pd.DataFrame, paragraph_embeddings: np.ndarray,
                    output_path: Path) -> None:
    reducer     = umap.UMAP(n_components=2, random_state=42)
    umap_coords = reducer.fit_transform(paragraph_embeddings)
    umap_df     = pd.DataFrame(umap_coords, columns=['umap_1', 'umap_2'])
    combined    = pd.concat(
        [df[['iso', 'year', 'country', 'continent', 'topic']].reset_index(drop=True), umap_df],
        axis=1
    )
    speeches_umap = (
        combined
        .groupby(['iso', 'year', 'country', 'continent', 'topic'], dropna=False)
        .agg(umap_1=('umap_1', 'mean'), umap_2=('umap_2', 'mean'), count=('umap_1', 'count'))
        .reset_index()
    )
    speeches_umap[['umap_1', 'umap_2']] = speeches_umap[['umap_1', 'umap_2']].round(4)
    speeches_umap.to_csv(output_path, index=False)
    print(f"✅ Saved speeches_umap.csv ({len(speeches_umap):,} rows)")


def regenerate_mentioned_countries(df: pd.DataFrame, output_path: Path) -> None:
    mc = df[df['topic'] != 'bla_bla'][['year', 'topic', 'country', 'countries_recoded']].copy()
    mc['countries_recoded'] = mc['countries_recoded'].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) and x != '[]' else []
    )
    exploded = mc.explode('countries_recoded').rename(columns={'countries_recoded': 'country_mentioned'})
    exploded = exploded[exploded['country_mentioned'].notna()]
    exploded['country_mentioned'] = exploded['country_mentioned'].apply(clean_country)
    exploded = exploded[~exploded['country_mentioned'].isin(to_drop)]
    result = exploded.groupby(['year', 'topic', 'country_mentioned']).size().reset_index(name='country_count')
    result.to_csv(output_path, index=False)
    print(f"✅ Saved mentioned_countries_agg.csv ({len(result):,} rows)")


def main():
    print("Loading data…")
    df        = pd.read_csv(DATA_PATH)
    topics_df = pd.read_csv(TOPICS_PATH)

    topic_names = topics_df['Name'].str.strip().tolist()
    topic_texts = topics_df['Text'].str.strip().tolist()

    print(f"  {len(df):,} paragraphs")
    print(f"  {len(topic_names)} topics: {topic_names}\n")

    print(f"Loading model ({MODEL_NAME})…")
    model = SentenceTransformer(MODEL_NAME)

    print("Encoding topic anchors…")
    anchor_embeddings = model.encode(topic_texts, show_progress_bar=False)

    print(f"Encoding {len(df):,} paragraphs in batches of {BATCH_SIZE}…")
    paragraphs           = df['speeches'].fillna('').tolist()
    paragraph_embeddings = model.encode(
        paragraphs,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
    )

    print("Computing similarities…")
    similarities = cosine_similarity(paragraph_embeddings, anchor_embeddings)
    best_idx     = similarities.argmax(axis=1)
    best_score   = similarities.max(axis=1)

    df['topic']            = [topic_names[i] for i in best_idx]
    df['topic_similarity'] = best_score.round(4)

    df.to_csv(DATA_PATH, index=False)
    print(f"\n✅ Updated speeches_paragraphs.csv")

    regenerate_topic_labels(df, topics_df, TOPIC_LABELS_OUT)

    print("Running UMAP (this takes a few minutes)…")
    regenerate_umap(df, paragraph_embeddings, UMAP_OUT)

    print("Pre-computing mentioned countries aggregation…")
    regenerate_mentioned_countries(df, MENTIONED_COUNTRIES_OUT)

    print("\nTopic distribution:")
    print(df['topic'].value_counts().to_string())

    low_confidence = (best_score < 0.25).sum()
    print(f"\nLow-confidence rows (similarity < 0.25): "
          f"{low_confidence:,} ({low_confidence / len(df) * 100:.1f}%)")
    print("  → These may be worth reviewing or reassigning to bla_bla")


if __name__ == '__main__':
    main()
