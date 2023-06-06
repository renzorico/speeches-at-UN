import pandas as pd
from params import DATA_PATH

def load_data():
    return pd.read_csv(DATA_PATH)

def harmonize_data(df):
    df.drop(["Year", "Session","session", "index", "year_iso", "ISO Code", "Unnamed: 6", 'Unnamed: 0'], axis=1, inplace=True)

    #iso_with_blank_country = df[df['Country'].isnull()]['iso']
    # Find ISO codes with multiple countries
    duplicated_iso = df[df.duplicated(subset='iso', keep=False)]['iso']

    # Filter the DataFrame for ISO codes with multiple countries
    df_multiple_countries = df[df['iso'].isin(duplicated_iso)]

    # Group by ISO code and get the unique countries
    duplicated_countries_per_iso = df_multiple_countries.groupby('iso')['Country'].unique()

    # Filter out lines with '.Rapp.history' and '.Rhistory'
    duplicated_countries_per_iso = duplicated_countries_per_iso[~duplicated_countries_per_iso.index.str.startswith('.')]

    # Extract the duplicated countries
    duplicated_countries = duplicated_countries_per_iso.explode().dropna().unique()

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        iso_code = row['iso']
        if iso_code == '.DS':
        # Drop the row if the ISO code is '.DS'
            df = df.drop(index)
        else:
            duplicated_countries = duplicated_countries_per_iso.get(iso_code)
            if duplicated_countries is not None:
            # Check if there are duplicated countries
                if len(duplicated_countries) > 1:
                # Perform specific replacements for certain ISO codes
                    if iso_code == 'BLR':
                        df.loc[index, 'country'] = 'Belarus'
                    elif iso_code == 'COG':
                        df.loc[index, 'country'] = 'Democratic Republic of Congo'
                    elif iso_code == 'CZK' or iso_code == 'CSK':
                        df.loc[index, 'country'] = 'Czechoslovakia'
                    elif iso_code == 'RUS':
                        df.loc[index, 'country'] = 'Russia'
                    elif iso_code == 'UKR':
                        df.loc[index, 'country'] = 'Ukraine'
                    else:
                        df.loc[index, 'country'] = duplicated_countries[0]
                else:
                    df.loc[index, 'country'] = duplicated_countries[0]

    df = df.rename(columns={'Country': 'country_dup'})

    return df
