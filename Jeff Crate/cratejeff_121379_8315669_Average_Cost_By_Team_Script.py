##This script will create a graph based on average cost of a players most frequently purchased service and group them
## by team. We will be using plotly express and io to open in browser

import pandas as pd
import plotly.express as px
import plotly.io as pio


##First we need to read the updated players csv
df = pd.read_csv('players_updated.csv')

##These two particular athletes skew the numbers because their most frequently purchased cost on the site is 10M
##This is obviously an error on their site
df = df[(df['Name'] != 'Amanda Bradford') & (df['Name'] != 'Weston Miser')]

##Because a person can be apart of multiple teams, I decided to attribute that persons cost to each team they are apart of
df['Team'] = df['Team'].apply(lambda x: x.split(', ') if isinstance(x, str) else []) #First we split the column based on the comma delimiter
df = df.explode('Team') #Then use the explode functions to replicate each row with each of the items that were split

##In order to get our desired result we have to group each athlete into each team
grouped_df = df.groupby('Team', as_index=False).agg({'Cost_in_$': 'mean'}).sort_values('Cost_in_$', ascending=False) #I wanted the bar graphs to be descending so we use the sort values method and group by the column name team
fig = px.bar(grouped_df, x='Team', y='Cost_in_$', title='Average NIL Sponsorship Cost by Team', labels={'Team': 'Team', 'Cost_in_$': 'Average Cost in $'}, text='Cost_in_$') #Here we use the plottly express to do all the hard work (tried to do GGplot and Matplotlib and it gave me a headache, this is so much easier)

##My ide does not display plots for some reason so we use the plotly io to show it in my browser
pio.renderers.default = 'browser' #we set our renderings to show in browser
fig.show() #shows us our plot