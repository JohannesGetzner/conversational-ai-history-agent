# Conversational AI Workshop

## sample codes for pandas use
```python
# load csv
df = pd.read_csv('./historical_figures_table (1).csv',encoding='ISO-8859-1')

# define a filter for matching
filter = df['full_name'] == 'Aristotle'

# get outputs of the filtering
df[filter]
