# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from flask import Flask, render_template
from flask_dialogflow.agent import DialogflowAgent

# create app and agent instances
app = Flask(__name__)
agent = DialogflowAgent(app=app, route="/", templates_file="templates/templates.yaml")

# set up test route
@app.route("/")
def hello_world():
    return render_template('frontend.html')

# import main conversation handlers for webhooks
from app import webhooks