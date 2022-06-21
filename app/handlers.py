# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import controllers
from flask import render_template
from flask_dialogflow.conversation import V2beta1DialogflowConversation
from jinja2 import Template
import random


# define sub handlers
def test_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("test_response"))
    conv.google.ask(render_template("test_response"))
    return conv


def retrieve_dataset_size(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    size = controllers.compute_dataset_size()
    conv.tell(render_template("dataset.size", num_rows=size[0], num_columns=size[1]))
    return conv


def construct_dataset_summary(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    data = controllers.read_dataset()
    columns_subset = random.sample(list(data.columns), 3)
    random_sample = data.sample(1)
    example = f"{random_sample.full_name.item()}, a {random_sample.occupation.item()} born year {random_sample.birth_year.item()} in {random_sample.city.item()}"
    summary = render_template("dataset.summary", columns=columns_subset, example=example)
    conv.tell(summary)
    return conv


def location_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    city, country, continent = conv.parameters.get('geo-city').title(), conv.parameters.get(
        'geo-country').title(), conv.parameters.get('continent').title()

    person = controllers.get_person_by_location(city, country, continent)
    if person is not None:
        name = person.full_name.item()
        occupation = person.occupation.item()
        person_id = person.person_id.item()
        conv.contexts.set('person_ctx', lifespan_count=6, person_id=person_id)
        conv.ask(render_template("location_search", name=name, occupation=occupation))
        conv.google.ask(render_template("location_search", name=name, occupation=occupation))
    else:
        conv.tell(f'Sorry! I could not find anyone from there. Please try again.')
    return conv


def domain_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    occu = conv.parameters.get('occu').title()
    name, occupation, person_id = controllers.get_id_by_occu(occu)
    conv.contexts.set('person_ctx', lifespan_count=6, person_id=person_id)
    print(conv)

    conv.ask(render_template("domain_search", name=name, occupation=occupation))
    conv.google.ask(render_template("domain_search", name=name, occupation=occupation))

    return conv


def person_birth_year(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    '''
        Get the birth year of a historical figure.

        1. find the person full name from the given user message
        2. if not found, get person info from current context
        3. if no context set, ask user to provide more information
    '''
    df = controllers.read_dataset()

    # find out whose birth year is asked, get person_id
    # get the person from the given parameters in last question.
    full_name = conv.parameters.get('person_full_name')
    if len(full_name) > 0:
        person_id = df.loc[df['full_name'] == full_name, 'person_id'].tolist()[0]
        conv.contexts.set('person_ctx', lifespan_count=5, person_id=person_id)
    else:  # no recorded full_name is given
        if conv.contexts.has('person_ctx'):
            # check the current contexts to find if the person is fixed
            ctx = conv.contexts.get('person_ctx')
            person_id = ctx.parameters['person_id']
        else:  # fail to get any person info, ask users to get more information
            conv.ask(render_template('ask.person.info'))
            return conv

    # response construction
    sex = df.loc[df['person_id'] == person_id, 'sex'].tolist()[0]
    birth_year = int(df.loc[df['person_id'] == person_id, 'birth_year'].tolist()[0])
    response = 'He ' if sex == 'Male' else 'She '
    response += 'was born in '
    if birth_year < 0:
        response += f'{str(abs(birth_year))} BCE.'
    else:
        response += f'{str(abs(birth_year))} CE.'
    conv.tell(response)

    return conv
