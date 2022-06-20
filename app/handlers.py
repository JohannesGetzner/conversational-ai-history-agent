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

def address_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    city = conv.parameters.get('geo-city')
    city = city.title()

    country = conv.parameters.get('geo-country')
    country = country.title()

    continent = conv.parameters.get('continent')
    continent = continent.title()

    name,personIDs,occupation=controllers.get_ID_by_adress(city = city,country = country,continent = continent)

    conv.contexts.set('person_ctx',lifespan_count = 6, name = name)
    print(conv)

    conv.ask(render_template("address_search",name = name,occupation = occupation))
    conv.google.ask(render_template("address_search", name = name, occupation = occupation))
    return conv

def domain_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    occu = conv.parameters.get('occu')
    occu = occu.title()
    name, personIDs, occupation = controllers.get_ID_by_occu(occu)
    conv.contexts.set('person_ctx', lifespan_count=6, name=name)
    print(conv)

    conv.ask(render_template("domain_search", name=name, occupation=occupation))
    conv.google.ask(render_template("domain_search", name=name, occupation=occupation))

    return conv