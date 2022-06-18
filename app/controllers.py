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
