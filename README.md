# Conversational AI Workshop History Agent

## Install the requirements
### Unix/macOS:
```commandline
python3 -m pip install --user virtualenv
python3 -m venv dialogflow-env
source dialogflow-env/bin/activate
python3 -m pip install -r requirements.txt
pip install git+https://github.com/ONSEIGmbH/flask-dialogflow.git
```


### windows
```commandline
py -m pip install --user virtualenv
py -m venv dialogflow-env
.\dialogflow-env\Scripts\activate
py -m pip install -r requirements.txt
pip install git+https://github.com/ONSEIGmbH/flask-dialogflow.git
```





## sample codes for pandas use
```python
# load csv
df = pd.read_csv('./historical_figures_table (1).csv',encoding='ISO-8859-1')

# define a filter for matching
filter = df['full_name'] == 'Aristotle'

# get outputs of the filtering
df[filter]


