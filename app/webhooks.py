# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import agent
from app import handlers
from flask_dialogflow.conversation import V2beta1DialogflowConversation


# define main handlers
@agent.handle(intent="test-intent")
def test_intent_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.test_intent(conv)


@agent.handle(intent="dataset.size")
def dataset_size_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.retrieve_dataset_size(conv)


@agent.handle(intent="dataset.summary")
def dataset_summary_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.construct_dataset_summary(conv)


@agent.handle(intent="dataset.features")
def dataset_features_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.tell(
        "The dataset contains a lot of information about historical figures, such as name, hometown, "
        "birth year and occupation. For example, Aristotle was born in 384 BCE in Greece. He is "
        "a philosopher in the humanities.")
    return conv


@agent.handle(intent="features.historical_popularity_index")
def dataset_hpi_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.tell(
        "The historical popularity index (HPI) is a metric that aggregates information on popularity of the figures "
        "online biography. Parameters such as the number of views and the number of languages the article is available "
        "in, influence this metric.")
    return conv


@agent.handle(intent="location.search")
def address_search_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.location_search(conv)


@agent.handle(intent="domain.search")
def domain_search_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.domain_search(conv)


@agent.handle(intent="birth_year.search")
def birth_year_search_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.birth_year_search(conv)


@agent.handle(intent="person.birth_year")
def person_birthyear_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    # TODO: do we need to handle queries like who was born earliest?
    return handlers.person_birth_year(conv)


@agent.handle(intent="person.sex")
def person_sex_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.person_attribute(conv, "sex")


@agent.handle(intent="person.domain")
def person_sex_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.person_attribute(conv, "domain")


@agent.handle(intent="person.location")
def person_sex_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.person_attribute(conv, "location")


@agent.handle(intent="person.hpi")
def person_hpi_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.person_attribute(conv, "historical_popularity_index")


@agent.handle(intent="dataset.more_info")
def person_sex_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.dataset_more_info(conv)


@agent.handle(intent="dataset.example")
def person_sex_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.dataset_example(conv)
