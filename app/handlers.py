from app import controllers
from flask import render_template
from flask_dialogflow.conversation import V2beta1DialogflowConversation
from app.controllers import read_dataset
import random


def conversation_tell(conv: V2beta1DialogflowConversation, msg) -> None:
    """
    triggers the dialogflow tell commend
    @param conv: the conversation object
    @param msg: the message to tell
    """
    conv.tell(msg)
    conv.google.tell(msg)


def conversation_ask(conv: V2beta1DialogflowConversation, msg) -> None:
    """
    triggers the dialogflow ask commend
    @param conv: the conversation object
    @param msg: the questionto ask
    """
    conv.ask(msg)
    conv.google.ask(msg)


def agent_skills(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    randomly selects three skills and then constructs the answer
    """
    skills = [
        '- to search for a historical figure by any property \n',
        '- about an attribute of a historical figure (e.g. gender, profession) \n',
        '- about an attribute of a historical figure (e.g. popularity, origin) \n',
        '- about the size of the data-set \n',
        '- to list the data set features \n',
        '- to explain what the HPI is \n',
        '- about the different features in the data set \n',
        '- about the birth-place or country of a historical figure \n',
    ]
    random_skills = random.sample(skills, 3)
    conversation_tell(conv, render_template('agent_skills', skills=random_skills))
    return conv


"""
------------------------------------------------------
handlers for general data-set intents
------------------------------------------------------
"""


def retrieve_dataset_size(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    retrieves the size of the dataset renders the template response
    """
    df = read_dataset()
    size = df.shape[0], df.shape[1]
    conversation_tell(conv, render_template("dataset_size", num_rows=size[0], num_columns=size[1]))
    return conv


def construct_dataset_info(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    constructs a small summary of the data set by sampling three random features and an example historical figures
    """
    data = controllers.read_dataset()
    # get 3 random features
    columns_subset = random.sample(list(data.columns), 3)
    # get a random example figure
    random_sample = data.sample()
    example = f"{random_sample.full_name.item()}, a {random_sample.occupation.item()} born year {random_sample.birth_year.item()} in {random_sample.city.item()}"
    summary = render_template("dataset_summary", columns=columns_subset, example=example)
    conversation_tell(conv, summary)
    conversation_ask(conv, "Would you like to find out more?")
    return conv


def get_more_info(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    callback to the initial dataset_info handler; returns a template with more exhaustive information on the data set
    """
    # get response from the
    yes = conv.parameters.get('yes')
    no = conv.parameters.get('no')
    if len(yes) != 0 or (len(yes) == 0 and len(no) == 0):
        df = controllers.read_dataset()
        conversation_tell(conv,
                          f"The dataset contains {df.shape[0]} entries and {df.shape[1]} columns. The entries are all ordered according to the HPI. The most important features are name, sex, brith_year, city, country, continent, occupation, domain, industry and the hpi. If you want you can always ask for an example.")
    elif len(no) != 0:
        conversation_tell(conv, "Ok! If you are not sure about what I can do, just ask 'What can you do?'")
    else:
        conversation_tell(conv, "I couldn't quite follow. Please repeat!")
    return conv


def get_dataset_example(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """gets a random example historical figure and constructs an answer describing its feature"""
    df = controllers.read_dataset()
    random_person = df.sample()
    conversation_tell(conv, render_template(
        "dataset_example",
        full_name=random_person["full_name"].item(),
        occupation=random_person["occupation"].item().lower(),
        birth_year=random_person["birth_year"].item(),
        domain=random_person["domain"].item(),
        city=random_person["city"].item(),
        country=random_person["country"].item(),
        pronouns=('He', 'he', 'him') if random_person.sex.item() == 'Male' else ('She', 'she', 'her'),
        hpi=round(random_person["historical_popularity_index"].item(), 2)
    ))
    return conv


def get_least_most_famous(conv) -> V2beta1DialogflowConversation:
    """
    gets the parameters from dialogflow and finds the most and least famous person according to the filter and then
    constructs an answer
    """
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

    response_beginning_famous = f'The most famous person from {location} is' if location != '' else 'The most famous person is'
    response_beginning_infamous = f'The least famous person from {location} is' if location != '' else 'The least famous person is'
    if famous != '' and unknown != '':
        msg = f"{response_beginning_famous} {most_famous.full_name} with a HPI of {round(most_famous.historical_popularity_index, 2)} and the least famous person is {least_famous.full_name} with a HPI of {round(least_famous.historical_popularity_index, 2)}."
    elif famous != '':
        msg = f"{response_beginning_famous} {most_famous.full_name} with a HPI of {round(most_famous.historical_popularity_index, 2)}."
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=most_famous.person_id.item())
    elif unknown != '':
        msg = f"{response_beginning_infamous} {least_famous.full_name} with a HPI of {round(least_famous.historical_popularity_index, 2)}."
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=least_famous.person_id.item())
    else:
        msg = "Sorry I didn't get that. Could you rephrase?"
    conversation_tell(conv, msg)
    return conv


"""
------------------------------------------------------
webhook for single observations (historical figures)
------------------------------------------------------
"""


def get_person_specific_attribute(conv: V2beta1DialogflowConversation, attribute):
    """
    extracts the attribute and full name from the user input and constructs an answer containing the full name and the
    attribute value. List of attributes is not exhaustive.
    """
    df = controllers.read_dataset()
    full_name = conv.parameters.get('person_full_name')

    # check if observation identifier is present
    if not full_name:
        # check context
        if conv.contexts.has('person_ctx'):
            person = df.loc[df['person_id'] == conv.contexts.get('person_ctx').parameters['person_id']]
        # respond with not found
        else:
            conv.tell("I am sorry, but I am not quite sure who you are referring to. Please try again!")
            return conv
    else:
        person = df.loc[df['full_name'] == full_name]
        # respond with not found if specified name is unknown
        if person.empty:
            conv.tell(f"Sorry, but I couldn't find anyone named {full_name} in the data-set.")
            return conv
    # refresh context
    conv.contexts.set('person_ctx', lifespan_count=4, person_id=person["person_id"].item())
    attribute_value = None
    if attribute == 'occupation_domain':
        attribute_value = f"{person.occupation.item()} in {person.domain.item()}"
    elif attribute == 'sex':
        attribute_value = person.sex.item()
    elif attribute == 'location':
        attribute_value = f"{person.city.item()}, {person.country.item()}"
    elif attribute == 'birth_year':
        birth_year = int(person.birth_year.item())
        if birth_year < 0:
            attribute_value = f'{str(abs(birth_year))} BCE'
        else:
            attribute_value = f'{str(abs(birth_year))} CE'
    elif attribute == 'hpi':
        attribute_value = round(person.historical_popularity_index.item(), 2)
    elif attribute == 'name':
        attribute_value = person.full_name.item()
    template = render_template(f'person_{attribute}', full_name=person.full_name.item(), attribute=attribute_value)
    conversation_tell(conv, template)
    return conv


"""
------------------------------------
webhooks for searching by features
------------------------------------
"""


def location_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    extracts the location parameters from the user input, filters the data and constructs an answer based on the
    count and an example from the filtered dataset
    """
    city, country, continent = conv.parameters.get('geo-city').title(), conv.parameters.get(
        'geo-country').title(), conv.parameters.get('continent').title()

    person, count = controllers.get_person_by_location(city, country, continent)
    if person is not None:
        name = person.full_name.item()
        occupation = person.occupation.item()
        person_id = person.person_id.item()
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        msg = render_template("location_search", count=count, name=name, occupation=occupation)
    else:
        msg = f'Sorry! I could not find anyone this location. Please try again.'
    conversation_tell(conv, msg)
    return conv


def occupation_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    extracts the occupation parameter from the user input, filters the data and constructs an answer based on the number
    of people that pursue this occupation and an example from the filtered dataset.
    """
    occupation = conv.parameters.get('occupation').title()
    person, count = controllers.get_person_by_occupation(occupation)
    if person is not None:
        person_id = person.person_id.item()
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        name = person.full_name.item()
        occupation = person.occupation.item()
        location = person.country.item()
        msg = render_template("domain_search", count=count, name=name, location=location, occupation=occupation)
    else:
        msg = f'Sorry! I could not find anyone with that occupation.'
    conversation_tell(conv, msg)
    return conv


def birth_year_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    extracts the birth_year parameter from the user input, filters the data and constructs an answer based on the
    number of people that were born in that year and an example from the filtered dataset.
    """
    birth_year = int(conv.parameters.get('number'))
    if birth_year < 0:
        birth_year_response = f'{str(abs(birth_year))} BCE'
    else:
        birth_year_response = f'{str(abs(birth_year))} CE'
    person, count = controllers.get_id_by_birth_year(birth_year)

    if person is None:
        msg = f'Sorry! No one that I know was born in {birth_year_response}.'
    else:
        name = person.full_name.item()
        person_id = person.person_id.item()

        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        msg = render_template("birth_year_search", count=count, name=name, birth_year_response=birth_year_response)
    conversation_tell(conv, msg)
    return conv


def name_search(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    """
    Handle search based on a person's full name.
    In particular, match the dialog context to see
    if this search is trying to get full_name for birth_year query
    or for general information of some person.
    """
    # get person name from user response.
    full_name = conv.parameters.get('person_full_name')
    df = read_dataset()
    person = df[df['full_name'] == full_name]

    if not person.empty:  # person exists in the dataset
        person_id = person.person_id.item()
        conv.contexts.set('person_ctx', lifespan_count=4, person_id=person_id)
        msg = f"Yes, {full_name} is a {person.occupation.item()} from {person.country.item()}. "
        sex = person.sex.item()
        pronoun = 'him' if sex == 'Male' else 'her'
        msg2 = f"What else would you like to know about {pronoun}?"
        conversation_tell(conv, msg)
        conversation_ask(conv, msg2)
    else:
        conversation_tell(conv, f"I am sorry, but I don't know who that is.")
    return conv
