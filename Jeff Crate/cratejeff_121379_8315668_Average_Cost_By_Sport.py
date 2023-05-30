##Here I wanted to show the average cost by sport by grouping the athletes by their sport and averaging the collective cost
import pandas as pd
import plotly.express as px

##Again we need to load the updated player name
df = pd.read_csv('players_updated.csv')

##Have to take out the two outliers that apparently cost 10 million for a shout out
df = df[(df['Name'] != 'Amanda Bradford') & (df['Name'] != 'Weston Miser')]

##Similar to the Avg Cost By Team, some players play multiple sports and we want to attribute that cost to to each sport not just one
## we have to split the column and explode the dataset
df['Sport'] = df['Sport'].apply(lambda x: x.split(', ') if isinstance(x, str) else []) #Here is where we split the column with an if statement to create a blank so it wont fail for one sport athletes
exploded_df = df.explode('Sport') #Use the explode method to attribute each person to each sport

##Here we are going to group by sport and mean the cost
average_cost_by_sport = exploded_df.groupby('Sport')['Cost_in_$'].mean().reset_index()
sport_average_costs = average_cost_by_sport.sort_values('Cost_in_$', ascending=False) #Here we sort the column so our bar chart doesn't look so spikey

##utilize the ease of life from plotly express
fig = px.bar(sport_average_costs, x='Sport', y='Cost_in_$', title='Average Cost by Sport')

##Show the figure
fig.show()


## May need the following two lines if you want to view in browser
## pio.renderers.default = 'browser' #
#fig.show() #shows us our plot