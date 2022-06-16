# -*- coding: utf-8 -*-
"""

@author: sebis
"""
import pandas as pd
import random


# define functions for conversation controllers
def get_random_element(number: int) -> list:
    """Return a list with a specified number of randomly selected elements from a hardcoded list."""
    element_list = ["A", "B", "C"]
    random_selection = random.sample(element_list, number)
    return random_selection

def get_ID_by_name(name: str)  -> list:
    df = pd.read_csv('./historical_figures_table (1).csv',encoding='ISO-8859-1')
    print(df)
    return

if __name__ == '__main__':

    get_ID_by_name('hello')