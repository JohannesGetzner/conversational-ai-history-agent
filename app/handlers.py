# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import controllers
from flask import render_template
from flask_dialogflow.conversation import V2beta1DialogflowConversation
from jinja2 import Template
import random
import time


# define sub handlers
def test_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("test_response"))
    conv.google.ask(render_template("test_response"))
    return conv


def retrieve_dataset_size(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    size = controllers.compute_dataset_size()
    conv.tell(render_template("dataset_size", num_rows=size[0], num_columns=size[1]))
    return conv


def construct_dataset_summary(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    data = controllers.read_dataset()
    columns_subset = random.sample(list(data.columns), 3)
    random_sample = data.head(10).sample(1)
    example = f"{random_sample.full_name.item()}, a {random_sample.occupation.item()} born year {random_sample.birth_year.item()} in {random_sample.city.item()}"
    summary = render_template("dataset_summary", columns=columns_subset, example=example)
    conv.tell(summary)
    conv.google.tell(summary)
    conv.ask("Would you like to find out more?")
    conv.google.ask("Would you like to find out more?")
    return conv


def dataset_more_info(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    yes = conv.parameters.get('yes')
    no = conv.parameters.get('no')
    if len(yes) != 0 or (len(yes) == 0 and len(no) == 0):
        df = controllers.read_dataset()
        conv.tell(
            f"The dataset contains {df.shape[0]} entries and {df.shape[1]} columns. The entries are all ordered "
            f"according to the historical-popularity index (HPI). The important features are name, sex, brith_year, "
            f"city, country, continent, occupation, domain, industry and the hpi")
        conv.google.tell()
        conv.tell("If you want you can always  for an example.")
    elif len(no) != 0:
        conv.tell("Alright! If you want to find out what else I can do, just ask 'What can you do?'")
    else:
        conv.tell("I couldn't quite follow. Please repeat!")
    return conv


def dataset_example(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    df = controllers.read_dataset()
    random_person = df.sample(1)
    conv.tell("Here is a random example:")
    conv.tell(
        render_template(
            "dataset_example",
            full_name=random_person["full_name"].item(),
            occupation=random_person["occupation"].item(),
            birth_year=random_person["birth_year"].item(),
            domain=random_person["domain"].item(),
            city=random_person["city"].item(),
            country=random_person["country"].item(),
            gender=random_person["sex"].item(),
            hpi=random_person["historical_popularity_index"].item()
        ))
    return conv


def location_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    city, country, continent = conv.parameters.get('geo-city').title(), conv.parameters.get(
        'geo-country').title(), conv.parameters.get('continent').title()

    person, count = controllers.get_person_by_location(city, country, continent)
    if person is not None:
        name = person.full_name.item()
        occupation = person.occupation.item()
        person_id = person.person_id.item()
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        conv.ask(render_template("location_search", count=count, name=name, occupation=occupation))
        conv.google.ask(render_template("location_search", count=count, name=name, occupation=occupation))
    else:
        conv.tell(f'Sorry! I could not find anyone from there. Please try again.')
    return conv


def domain_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    occu = conv.parameters.get('occu').title()
    person, count = controllers.get_id_by_occu(occu)
    name = person.full_name.item()
    occupation = person.occupation.item()
    person_id = person.person_id.item()
    location = person.country.item()

    conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
    print(conv)

    conv.ask(render_template("domain_search", count=count, name=name, location=location, occupation=occupation))
    conv.google.ask(render_template("domain_search", count=count, name=name, location=location, occupation=occupation))

    return conv


def birth_year_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    birth_year = int(conv.parameters.get('number'))
    if birth_year < 0:
        birth_year_response = f'{str(abs(birth_year))} BCE'
    else:
        birth_year_response = f'{str(abs(birth_year))} CE'
    person, count = controllers.get_id_by_birth_year(birth_year)

    if person is None:
        conv.tell(f'Sorry! No one that I know was born in {birth_year_response}. Maybe you could  others?')
    else:
        name = person.full_name.item()
        person_id = person.person_id.item()

        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)

        conv.ask(render_template("birth_year_search", count=count, name=name, birth_year_response=birth_year_response))
        conv.google.ask(
            render_template("birth_year_search", count=count, name=name, birth_year_response=birth_year_response))

    return conv


def person_birth_year(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    '''
        Get the birth year of a historical figure.

        1. find the person full name from the given user message
        2. if not found, get person info from current context
        3. if no context set, triger get_person_name_ctx context, ask user to provide more information
    '''
    # find out whose birth year is asked, get person_id
    # get the person from the given parameters in last question.
    full_name = conv.parameters.get('person_full_name')
    if len(full_name) > 0:
        person = controllers.get_person_by_name(full_name)
        if person is not None:
            person_id = person.person_id.item()
            conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        else:  # don't have this person's information in the dataset
            conv.tell(f"I am sorry, but I don't know who is {full_name}. "
                      "Are you interested in others?")
    else:  # no recorded full_name is given
        if conv.contexts.has('person_ctx'):
            # check the current contexts to find if the person is fixed
            ctx = conv.contexts.get('person_ctx')
            person_id = ctx.parameters['person_id']
            person = controllers.get_person_by_id(person_id)
        else:  # fail to get any person info, ask users to get more information
            conv.tell(render_template('ask_person_info'))
            conv.contexts.set('birth_year_person_name_ctx', lifespan_count=1)
            return conv

    # response construction
    response = controllers.construct_person_attribute_response('birth_year', person)
    conv.tell(response)
    return conv


def name_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    '''
        Handle search based on a person's full name.

        In particular, match the dialog context to see 
        if this search is trying to get full_name for birth_year query
        or for general information of some person.
    '''
    # get person name from user response.
    full_name = conv.parameters.get('person_full_name')
    person = controllers.get_person_by_name(full_name)
    if not person.empty:  # person exists in the dataset
        person_id = person.person_id.item()
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        if conv.contexts.has('birth_year_person_name_ctx'):
            # user trying to ask about someone's birth_year
            response = controllers.construct_person_attribute_response('birth_year', person)
            conv.tell(response)
        else:  # only a general query about a person
            response_part = f"Yes, {full_name} is a {person.occupation.item()} from {person.country.item()}. "
            response = response_part + controllers.construct_person_attribute_response('general_query', person)
            conv.ask(response)
    else:  # don't have this person's information in the dataset
        conv.tell(f"I am sorry, but I don't know who {full_name} is. "
                  "Are you interested in others?")
    return conv


def person_attribute(conv: V2beta1DialogflowConversation, attribute) -> V2beta1DialogflowConversation:
    # read dataset and conversation parameters

    df = controllers.read_dataset()
    full_name = conv.parameters.get('person_full_name')
    if len(full_name) == 0:
        if conv.contexts.has('person_ctx'):
            person = df.loc[df['person_id'] == conv.contexts.get('person_ctx').parameters['person_id']]
        else:
            conv.tell("I am sorry, but I am not quite sure who you are referring to. Please try again!")
            return conv
    else:
        person = df.loc[df['full_name'] == full_name]
        if person.empty:
            conv.tell(f"Sorry, but I couldn't find anyone named {full_name} in the data-set.")
            return conv
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person["person_id"].item())

    full_name = person["full_name"].item()
    response_att = controllers.construct_person_attribute_response(attribute, person)
    conv.tell(render_template(f'person_{attribute}', full_name=full_name, attribute=response_att))
    return conv


def agent_skills(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    skills = [
        '- to search for a person by their name \n',
        '- about the birth-year or profession of a person \n',
        '- about the size of the data-set \n',
        '- to list the features \n',
        '- to explain what the HPI is \n',
        '- about the different features in the data-set \n',
        '- about the birth-place or country of a person \n',
        '- about the gender of a person \n',
        '- about how popular a person is \n'
    ]
    random_skills = random.sample(skills, 3)
    conv.tell(render_template('agent_skills', skills=random_skills))
    return conv


def dataset_most_famous(conv) -> V2beta1DialogflowConversation:
    famous = conv.parameters.get('famous')
    unknown = conv.parameters.get('unknown')
    df = controllers.read_dataset()
    location = ''
    if conv.parameters['geo-country'] != '':
        df = df.loc[df['country'] == conv.parameters['geo-country']]
        location = conv.parameters['geo-country']
    elif conv.parameters['continent'] != '':
        df = df.loc[df['continent'] == conv.parameters['continent']]
        location = conv.parameters['continent']
    elif conv.parameters['geo-city'] != '':
        df = df.loc[df['geo-city'] == conv.parameters['geo-city']]
        location = conv.parameters['geo-city']

    df.reset_index(inplace=True, drop=True)
    most_famous = df.iloc[df['historical_popularity_index'].idxmax()]
    least_famous = df.iloc[df['historical_popularity_index'].idxmin()]

    response_beginning = f'The most famous person from {location} is' if location != '' else 'The most famous person is'
    if famous != '' and unknown != '':
        conv.tell(
            f"{response_beginning} {most_famous.full_name} with a HPI of {most_famous.historical_popularity_index} and the least famous person is {least_famous.full_name} with a HPI of {least_famous.historical_popularity_index}")
    elif famous != '':
        conv.tell(
            f"{response_beginning} {most_famous.full_name} with a HPI of {most_famous.historical_popularity_index} ")
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=most_famous.person_id.item())
    elif unknown != '':
        conv.tell(
            f"{response_beginning} {least_famous.full_name} with a HPI of {least_famous.historical_popularity_index} ")
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=least_famous.person_id.item())
    else:
        conv.tell("Sorry I didn't get that. Could you rephrase?")
    return conv


def person_name(conv) -> V2beta1DialogflowConversation:
    if conv.contexts.has('person_ctx'):
        df = controllers.read_dataset()
        person = df.loc[df['person_id'] == conv.contexts.get('person_ctx').parameters['person_id']]
        print(conv.contexts.get('person_ctx'))
        print(person)
        conv.tell(render_template('person_name', name=person.full_name.item()))
    else:
        conv.tell("Sorry, I don't remember talking about anyone specific.")
    return conv
