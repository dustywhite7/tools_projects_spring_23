##after finally getting the webscraping script to complete as anticipated I realized I needed to change the columns a bit
## because the website holds specific columns differently, such as affiliation can have current teams, past teams,
## professional experience, etc. Also I wanted to break out sport and position, but some athletes can play multiple sports
## and that will be reflected in this section. We will be using pandas for this

import pandas as pd


df = pd.read_csv('players.csv') #Here we load our CSV


df['Affiliation'] = df['Affiliation'].str.replace('•', '/') #We change the delimiter Opendorse uses from the bullet to the / because it breaks when we open it in excel
df['Background'] = df['Background'].str.replace('•', '/') #Ditto
df['Sport/Position'] = df['Sport/Position'].str.replace('•', '/') #Ditto

##I wanted to do analysis by sport and luckily the sport was always in the first part of the column so we can use our
## delimiter we created to split the column on that delimitter and take the first item and put it in sport, and the rest
## we can put in position
df['Sport'] = df['Sport/Position'].apply(lambda x: str(x).split('/')[0].strip() if x else None) #We split the column and put the first item into sport
df['Position'] = df['Sport/Position'].apply(lambda x: '/'.join(str(x).split('/')[1:]).strip() if x else None) #we take everything after the split and put it in to position

##I dropped this column because I kep confusing msyelf, not a necessary line 
df.drop('Sport/Position', axis=1, inplace=True)

##I wanted to do analysis by team and conference, unfortunately the affiliation subsection was not super standardized after team, because players can have multiple teams and affilitations. Luckily the team names were all clustered, so we could see each team that person was apart of
df['Team'] = df['Affiliation'].apply(lambda x: str(x).split('/')[0].strip() if x else None) #Here is where we split based on the delimiter we gave earlier
df['Conference/Affiliation'] = df['Affiliation'].apply(lambda x: '/'.join(str(x).split('/')[1:]).strip() if x else None) #In most cases conference goes second, but that is not always the case so we put other affiliations to designate

##Again not a necessary column, but helpful when I kept making issues calling this column instead of the conference/affiliation column
df.drop('Affiliation', axis=1, inplace=True)

##To do analysis i needed to be able to convert the dollar cost into a numeric type so I needed to drop the + and $
df['Cost'] = df['Cost'].str.replace('[$+,]', '', regex=True).astype(float)
df = df.rename(columns={'Cost': 'Cost_in_$'})

##Here we save our updated dataset for analysis
df.to_csv('players_updated.csv', index=False)