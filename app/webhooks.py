from app import agent
from app import handlers
from flask_dialogflow.conversation import V2beta1DialogflowConversation


@agent.handle(intent="agent.skills")
def agent_skills_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.agent_skills(conv)


"""
-------------
webhooks for general data-set intents
-------------
"""


@agent.handle(intent="dataset.size")
def dataset_size_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.retrieve_dataset_size(conv)


@agent.handle(intent="dataset.summary")
def dataset_summary_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.construct_dataset_info(conv)


@agent.handle(intent="dataset.more_info")
def dataset_more_info_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_more_info(conv)


@agent.handle(intent="dataset.example")
def dataset_example_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_dataset_example(conv)


@agent.handle(intent="dataset.max_min_hpi")
def dataset_most_famous_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_least_most_famous(conv)


@agent.handle(intent="dataset.features")
def dataset_features_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.tell(
        "The dataset contains a lot of information about historical figures, such as name, hometown, "
        "birth year and occupation. For example, Aristotle was born in 384 BCE in Greece. He is "
        "a philosopher in humanities.")
    return conv


@agent.handle(intent="features.historical_popularity_index")
def dataset_hpi_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.tell(
        "The historical popularity index (HPI) is a metric that aggregates information on popularity of the figures "
        "online biography. Parameters such as the number of views and the number of languages the article is available "
        "in, influence this metric.")
    return conv


"""
------------------------------------------------------
webhooks for single observations (historical figures)
------------------------------------------------------
"""


@agent.handle(intent="person.name")
def person_name_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_person_specific_attribute(conv, "name")


@agent.handle(intent="person.birth_year")
def person_birth_year_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_person_specific_attribute(conv, "birth_year")


@agent.handle(intent="person.sex")
def person_gender_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_person_specific_attribute(conv, "sex")


@agent.handle(intent="person.occupation_domain")
def person_domain_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_person_specific_attribute(conv, "occupation_domain")


@agent.handle(intent="person.location")
def person_location_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_person_specific_attribute(conv, "location")


@agent.handle(intent="person.hpi")
def person_hpi_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.get_person_specific_attribute(conv, "hpi")


"""
------------------------------------
webhooks for searching by features
------------------------------------
"""


@agent.handle(intent="location.search")
def address_search_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.location_search(conv)


@agent.handle(intent="occupation.search")
def domain_search_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.occupation_search(conv)


@agent.handle(intent="birth_year.search")
def birth_year_search_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.birth_year_search(conv)


@agent.handle(intent="name.search")
def name_search_hook(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.name_search(conv)
