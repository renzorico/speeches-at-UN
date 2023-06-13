import pandas as pd
from utilities.params import DATA_PATH

def load_data():
    print("✅ data loaded")
    return pd.read_csv(DATA_PATH)
