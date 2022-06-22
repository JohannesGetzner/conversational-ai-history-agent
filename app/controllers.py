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


def compute_dataset_size() -> (int, int):
    d = read_dataset()
    return d.shape[0], d.shape[1]


def read_dataset() -> pd.DataFrame:
    d = pd.read_excel(
        f'{os.path.dirname(os.path.abspath(__package__))}/historical_figures_table.xlsx',
        header=0,
        index_col=None
    )
    return d


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
    person = df.head(10)
    person = person.sample()
    return person


def get_id_by_occu(occu):
    df = read_dataset()
    df = df.loc[df['occupation'] == occu]
    person = df.head(10)
    person = person.sample()
    name = person.full_name.item()
    occupation = person.occupation.item()
    person_id = person.person_id.item()
    return name, occupation, person_id
