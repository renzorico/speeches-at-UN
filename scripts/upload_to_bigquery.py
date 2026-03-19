#!/usr/bin/env python3
"""
One-time script: upload speeches_paragraphs.csv → BigQuery.

Run from the project root:
    python scripts/upload_to_bigquery.py

The table will be (re-)created using the project / dataset / table names
defined in streamlit/.streamlit/secrets.toml, falling back to the same
defaults that data.py uses.
"""

import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = PROJECT_ROOT / "streamlit" / ".streamlit" / "secrets.toml"
CSV_PATH = PROJECT_ROOT / "data" / "speeches_paragraphs.csv"


def load_secrets():
    if not SECRETS_PATH.exists():
        print(f"ERROR: secrets file not found at {SECRETS_PATH}")
        sys.exit(1)
    with open(SECRETS_PATH, "rb") as f:
        return tomllib.load(f)


def main():
    secrets = load_secrets()

    if "gcp_service_account" not in secrets:
        print("ERROR: [gcp_service_account] section missing from secrets.toml")
        sys.exit(1)

    sa_info = secrets["gcp_service_account"]
    gcp_project = secrets.get("GCP_PROJECT_ID", sa_info.get("project_id", "speeches-at-un"))
    dataset_id = secrets.get("BIGQUERY_DATASET", "un_speeches")
    table_id = secrets.get("BIGQUERY_TABLE", "speeches_paragraphs")
    table_ref = f"{gcp_project}.{dataset_id}.{table_id}"

    if not CSV_PATH.exists():
        print(f"ERROR: CSV not found at {CSV_PATH}")
        sys.exit(1)

    from google.oauth2 import service_account
    from google.cloud import bigquery

    credentials = service_account.Credentials.from_service_account_info(sa_info)
    client = bigquery.Client(project=gcp_project, credentials=credentials)

    # Create dataset if it doesn't exist
    dataset = bigquery.Dataset(f"{gcp_project}.{dataset_id}")
    dataset.location = "US"
    client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset ready: {gcp_project}.{dataset_id}")

    # Read CSV via pandas first — avoids BigQuery's CSV parser choking on
    # columns that contain Python list strings with single quotes (top_5_words,
    # countries_recoded, etc.).  load_table_from_dataframe uses Arrow/Parquet
    # serialisation internally so all string values pass through unchanged.
    import pandas as pd

    file_size_mb = CSV_PATH.stat().st_size / 1_048_576
    print(f"Reading {CSV_PATH.name} ({file_size_mb:.0f} MB) into memory ...")
    df = pd.read_csv(CSV_PATH, low_memory=False)
    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns.")

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    print(f"Uploading → {table_ref} ...")
    print("This may take a few minutes — BigQuery is processing the data.")

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # blocks until done

    table = client.get_table(table_ref)
    print(f"\nDone! {table.num_rows:,} rows, {len(table.schema)} columns → {table_ref}")
    print("\nNext step: paste your secrets.toml contents into Streamlit Cloud:")
    print("  share.streamlit.io → app → ⋮ → Settings → Secrets → Save → Reboot")


if __name__ == "__main__":
    main()
