# Conversational AI Workshop: History Agent

This project was created during the Conversational AI Workshop at the Software Engineering for Business Information
Systems (<a href="https://wwwmatthes.in.tum.de/pages/t5ma0jrv6q7k/sebis-Public-Website-Home">sebis</a>) chair at the
Technical University of Munich (TUM).

## Introduction & Motivation

This project aims to showcase how a conversational agent could be used as an interface to explore a dataset. More
information on the dataset can be found <a href="https://www.nature.com/articles/sdata201575#Abs1">here</a>. The agent
was built using Google Dialogflow and a Flask backend. For more details about the setup and technological aspects see
the README file.

## Install the requirements | Python=3.9

### Unix/macOS:

```commandline
python3 -m pip install --user virtualenv
python3 -m venv dialogflow-env
source dialogflow-env/bin/activate
python3 -m pip install -r requirements.txt
```

### Demo

To try out the demo, create a new Google Dialogflow project and import the agent.zip file. Locally start ngrok
with `ngrok http 8000` to forward the Flask port to the Dialog Agent. The link provided by ngrok once started must be
entered in the Dialogflow project under the 'Fulfillment/Webhook/Url' tab.
First run the Flask App and then visit frontend.html file to play around with the demo.