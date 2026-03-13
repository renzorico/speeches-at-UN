import os
from pathlib import Path

# Get paths from environment or use defaults relative to project root
PROJECT_ROOT = Path(__file__).parent.parent

# Source data: the original all_speeches.csv in /data folder
SOURCE_DATA_PATH = str(PROJECT_ROOT / 'data' / 'all_speeches.csv')

# Processed data paths
DATA_PATH = os.getenv('DATA_PATH', str(PROJECT_ROOT / 'raw_data' / 'speeches_with_paragraphs_processed.csv'))
CORPUS_PATH = os.getenv('CORPUS_PATH', str(PROJECT_ROOT / 'raw_data' / 'all_speeches.csv'))
CLEAN_DATA_PATH = str(PROJECT_ROOT / 'raw_data' / 'clean_data.csv')
