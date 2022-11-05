import pandas as pd
import os


def read_dataset() -> pd.DataFrame:
    """
    reads the data from the csv file and returns dataset
    """
    d = pd.read_excel(
        f'{os.path.dirname(os.path.abspath(__package__))}/data.xlsx',
        header=0,
        index_col=None
    )
    return d


def get_person_by_location(city, country, continent):
    """
    searches for a person in the dataset by city, country or continent
    @param city: the city to search by
    @param country: the country to search by
    @param continent: the continent to search by
    @return: one of the top 10 most famous people that fulfill the criteria and the count of matches
    """
    if city:
        geo_feature = 'city'
    elif country:
        geo_feature = 'country'
    elif continent:
        geo_feature = 'continent'
    else:
        return None, None
    df = read_dataset()
    match = df[geo_feature] == eval(geo_feature)
    df = df[match]
    if df.empty:
        return None, None
    count = df.shape[0]
    person = df.head(10).sample()
    return person, count


def get_person_by_occupation(occupation):
    """
    searches for a historic person by the occupation parameter
    @param occupation: the specified occupation
    @return: one of the top 10 most famous people that fulfill the occupation criteria and the count of matches
    """
    df = read_dataset()
    df = df.loc[df['occupation'] == occupation]
    if df.empty:
        return None, None
    count = df.shape[0]
    person = df.head(10).sample()
    return person, count


def get_id_by_birth_year(birth_year):
    """
    searches for a historic person by the birth_year
    @param birth_year: the birth_year to search by
    @return: one of the top 10 most famous people that fulfill the birth_yer criteria and the count of matches
    """
    df = read_dataset()
    df = df.loc[df['birth_year'] == str(birth_year)]
    count = df.shape[0]
    if count == 0:
        return None, None
    else:
        person = df.head(10).sample()
    return person, count
