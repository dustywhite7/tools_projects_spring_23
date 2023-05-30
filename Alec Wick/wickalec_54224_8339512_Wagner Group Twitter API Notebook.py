#!/usr/bin/env python
# coding: utf-8

# # Wagner Group - Twitter API Notebook

# ### Alec Wick

# ## Import Packages

# In[44]:


import tweepy
import webbrowser
import time
import pandas as pd
import plotly.express as px
from tabulate import tabulate
from IPython.display import display
from datetime import date, timedelta


# ## Get Twitter Data

# In[52]:


#put your Bearer Token in the parenthesis below
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAKXlnAEAAAAAZwflF0vkRArcj6daSzVOD2dP%2BNs%3DPGbylowFlykyk2TEREzHSLM45JwfpsT2KZ3tHqGONMlCtXKqWm')

#pull tweets from twitter
query='#wagnergroup -is:retweet lang:en'
#tweets=client.search_recent_tweets(query=query,tweet_fields=['context_annotations','created_at'],max_results=12)


#Users
tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                     user_fields=['location'], expansions='author_id', max_results=10)

# Get users list from the includes object
users = {u["id"]: u for u in tweets.includes['users']}


# ## Create Tweet Table

# In[53]:


#Collect Twitter Messages   
tweetMessages=[]
for tweet in tweets.data:
    tweetMessages.append(tweet.text)
tmTable=pd.DataFrame(tweetMessages,columns=['Tweets'])
pd.set_option('display.max_colwidth', None)
tmTable.replace({ r'\A\s+|\s+\Z': '', '\n' : ' '}, regex=True, inplace=True)

#Collect Usernames
tweetUsers=[]
for tweet in tweets.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        tweetUsers.append(user.name)
uTable=pd.DataFrame(tweetUsers,columns=['Username'])
pd.set_option('display.max_colwidth', None)

#Collect Location
tweetLocation=[]
for tweet in tweets.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        tweetLocation.append(user.location)
LTable=pd.DataFrame(tweetLocation,columns=['Location'])
pd.set_option('display.max_colwidth', None)

#Collect Date
tweetDate=[]
for tweet in tweets.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        tweetDate.append(tweet.created_at)
TTable=pd.DataFrame(tweetDate,columns=['Date'])
pd.set_option('display.max_colwidth', None)
TTable['Date'] = pd.to_datetime(TTable['Date']).dt.strftime('%m-%d-%Y')

#Collect Hour
tweetTime=[]
for tweet in tweets.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        tweetTime.append(tweet.created_at)
ttable=pd.DataFrame(tweetTime,columns=['Time'])
pd.set_option('display.max_colwidth', None)
ttable['Time'] = pd.to_datetime(ttable['Time']).dt.strftime('%H-%M')

#Store data into table
twitterTable=pd.concat([tmTable, uTable,LTable,TTable,ttable], axis=1)
blankIndex=[''] * len(twitterTable)
twitterTable.index=blankIndex
display(twitterTable)


# ## Calculate Frequency Counts

# In[1]:


#Gets count information from twiiter API
counts = client.get_recent_tweets_count(query=query,granularity='day')

#Displays counts
for count in counts.data:
    print(count)

#Displays counts for the past 7 days using the correct formatting
today = date.today()
d1 = today.strftime("%m/%d/%Y")
d2 = today+timedelta(days=-1)
d2 = d2.strftime("%m/%d/%Y")
d3 = today+timedelta(days=-2)
d3 = d3.strftime("%m/%d/%Y")
d4 = today+timedelta(days=-3)
d4 = d4.strftime("%m/%d/%Y")
d5 = today+timedelta(days=-4)
d5 = d5.strftime("%m/%d/%Y")
d6 = today+timedelta(days=-4)
d6 = d6.strftime("%m/%d/%Y")
d7 = today+timedelta(days=-4)
d7 = d7.strftime("%m/%d/%Y")
dates=[d7,d6,d5,d4,d3,d2,d1]
freq=[40,26,36,18,32,238,134]

#Creates frequency table
dtable=pd.DataFrame(dates,columns=['Date'])
ftable=pd.DataFrame(freq,columns=['Freq'])
freqTable=pd.concat([dtable,ftable],axis=1)
print(freqTable)

#Display line chart
line=px.line(freqTable,x="Date",y="Freq",title="Number of Tweets")
line.show()

