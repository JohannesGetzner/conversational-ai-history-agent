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


