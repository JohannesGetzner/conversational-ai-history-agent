# -*- coding: utf-8 -*-
"""

@author: sebis
"""

import random
import pandas as pd
import os


# define functions for conversation controllers
def get_random_element(number: int) -> list:
    """Return a list with a specified number of randomly selected elements from a hardcoded list."""
    element_list = ["A", "B", "C"]
    random_selection = random.sample(element_list, number)
    return random_selection


def compute_dataset_size() -> tuple:
    d = read_dataset()
    return d.shape[0], d.shape[1]


def read_dataset() -> pd.DataFrame:
    d = pd.read_excel(
        f'{os.path.dirname(os.path.abspath(__package__))}/historical_figures_table.xlsx',
        header=0,
        index_col=None
    )
    return d


def get_person_by_name(full_name):
    df = read_dataset()
    match = df['full_name']== full_name
    person = df[match]

    if df.empty:
        return None

    return person


def get_person_by_id(person_id):
    df = read_dataset()
    match = df['person_id']== person_id
    person = df[match]

    if df.empty:
        return None

    return person


def get_person_by_location(city, country, continent):
    if city != '':
        geo_feature = 'city'
    elif country != '':
        geo_feature = 'country'
    elif continent != '':
        geo_feature = 'continent'
    else:
        return None

    df = read_dataset()
    match = df[geo_feature] == eval(geo_feature)
    df = df[match]

    if df.empty:
        return None

    count = df.shape[0]
    if df.shape[0] < 10:
        person = df.sample()
    else:
        person = df.head(10)
        person = person.sample()
    return person, count


def get_id_by_occu(occu):
    df = read_dataset()
    df = df.loc[df['occupation'] == occu]

    count = df.shape[0]

    if df.shape[0] < 10:
        person = df.sample()
    else:
        person = df.head(10)
        person = person.sample()

    return person, count


def get_id_by_birth_year(birth_year):
    df = read_dataset()
    df = df.loc[df['birth_year'] == str(birth_year)]
    # check how many people was born in this year
    count = df.shape[0]

    if df.shape[0] == 0:  # no person matched
        person = None
    else:  # sample one from min(10, count) persons
        person = df.head(min(10, count))
        person = person.sample()

    return person, count


def construct_person_attribute_response(attribute, person):
    if attribute == 'domain':
        part = f"{person['occupation'].item()} in {person['domain'].item()}"
    elif attribute == 'location':
        part = f"{person['city'].item()} in {person['country'].item()}"
    elif attribute == 'birth_year':
        sex = person.sex.item()
        birth_year = int(person.birth_year.item())
        part = 'He ' if sex == 'Male' else 'She '
        part += 'was born in '
        if birth_year < 0:
            part += f'{str(abs(birth_year))} BCE.'
        else:
            part += f'{str(abs(birth_year))} CE.'
    else:
        part = person[attribute].item()
    return part

def get_age_data() -> pd.DataFrame:
    df = read_dataset()
    ind = df['birth_year'] != 'Unknown'
    df = df[ind]
    df.birth_year = df.birth_year.astype(int)
    df = df.sort_values(by=['birth_year'])
    return df