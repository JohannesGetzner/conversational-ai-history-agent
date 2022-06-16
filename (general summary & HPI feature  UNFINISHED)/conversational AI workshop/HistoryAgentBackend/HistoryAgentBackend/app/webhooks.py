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

@agent.handle(intent="Default Welcome Intent")
def welcome_intent_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    print('welcome intent identified')
    return handlers.welcome(conv)

@agent.handle(intent="hpi.intro")
def hpiIntro_intent_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.hpi_intro(conv)


@agent.handle(intent="summary")
def summary_intent_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.summary(conv)

@agent.handle(intent="hpi.person")
def summary_intent_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.hpi_person(conv)