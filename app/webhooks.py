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
    # TODO: do we need to remove person context if user now asks about the whole dataset??
    conv.tell(
        "In the dataset, there is much information about historical figures, such as name, hometown, "
        "birth year and occupations, etc. For example, Aristotle was born in 384 BCE in Greece. He is "
        "a philosopher in the humanities.")
    return conv


@agent.handle(intent="features.historical_popularity_index")
def dataset_summary_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.tell(
        "The historical popularity index (HPI) is a metric that aggregates information on popularity of the figures "
        "online biography. Parameters such as the number of views and the number of languages the article is available "
        "in, influence this metric.")
    return conv


@agent.handle(intent="address.search")
def address_search_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:

    return handlers.address_search(conv)


@agent.handle(intent="domain.search")
def domain_search_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.domain_search(conv)


@agent.handle(intent="person.birth_year")
def person_birthyear_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    # TODO: do we need to handle queries like who was born earliest?
    return handlers.person_birth_year(conv)
