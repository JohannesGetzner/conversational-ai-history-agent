# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import controllers
from flask import render_template
from flask_dialogflow.conversation import V2beta1DialogflowConversation


# define sub handlers
def test_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("test_response"))
    conv.google.ask(render_template("test_response"))
    return conv

def welcome(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    print("welcome")
    conv.ask(render_template("welcome"))
    conv.google.ask(render_template("welcome"))
    print('welcome done')
    return conv

def hpi_intro(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("hpi.intro"))
    conv.google.ask(render_template("hpi.intro"))
    return conv

def summary(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("summary"))
    conv.google.ask(render_template('summary'))
    return conv


def hpi_person(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    print(conv)
    firstName = conv.parameters.get("given-name")
    tmp = conv.parameters.get("last-name")
    lastName = tmp if tmp is not None else ''
    name = firstName  + ' ' + lastName
    print(name)
    personIDs =

    conv.contexts.set("find_restaurant_ctx", lifespan_count=6, personIDs=personIDs)

    conv.ask(render_template("hpi.intro"))
    conv.google.ask(render_template("hpi.intro"))
    return conv