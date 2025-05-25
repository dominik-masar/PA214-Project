import pandas as pd

def load_datasets(mission_path, astronauts_path):
    missions_df = pd.read_csv(mission_path)
    astronauts_df = pd.read_csv(astronauts_path)

    # TODO some preprocessing?
    missions_df['Country'] = missions_df['Country'].replace('U.S.', 'USA')
    astronauts_df['Profile.Nationality'] = astronauts_df['Profile.Nationality'].replace('U.S.', 'USA')
    missions_df['Company ID'] = missions_df['Company Name'].factorize()[0]

    return missions_df, astronauts_df


def get_country_list(missions_df, astronauts_df):
    countries = astronauts_df['Profile.Nationality'].dropna().unique()
    countries = set(countries).union(set(missions_df['Country'].dropna().unique()))
    countries = sorted(countries)
    return countries
