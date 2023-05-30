#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import plotly.express as px
import requests
import plotly.graph_objects as go
import numpy as np

#All the information needed for the API call, ACLED requires a registered email and key
email = "emilywright@unomaha.edu"
key = "dhlppupy8RQoOfbV*Cwn"
actor1 = "Wagner" #this filters our call to contain events where Wagner Group is an actor
url = "http://api.acleddata.com/acled/read?key=dhlppupy8RQoOfbV*Cwn&email=emilywright@unomaha.edu&actor1=wagner"

#Execution of API call, translating from json, and building a dataframe with results
results = requests.get(url).text
results = json.loads(results)
df = pd.json_normalize(results, 'data')

#adding additional columns to the dataframe for analysis
df['ones'] = 1
df["date"]=pd.to_datetime(df["event_date"])
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year
df["month_year"]=df["date"].dt.strftime('%Y-%m')
df['fatalities_new']=df['fatalities'].astype(float)

#df

#SUBSET of activity in African countries

df_africa = df[(df["country"] == "Mozambique") | (df["country"] == "Libya") | (df["country"] == "Mali") | (df["country"] == "Central African Republic")]

mozambique = df.loc[df['country']=="Mozambique"]
libya = df.loc[df['country']=="Libya"]
mali = df.loc[df['country']=="Mali"]
car = df.loc[df['country']=="Central African Republic"]

#df_africa


# In[2]:


#HISTOGRAMS based on count of events per country per year

#Global
events_per_year_all = px.histogram(df, x = 'year', y = 'ones', color='country',labels={
                                  "year":"Year",
                                  'ones':"Number of Events",
                                  "country":"Country"
                              },
                              title="Wagner Group Events")
#events_per_year_all.show()



#Africa only
events_per_year = px.histogram(df_africa, x = 'year', y = 'ones', color='country',
                               labels={
                                  "year":"Year",
                                  'ones':"Number of Events",
                                  "country":"Country"
                              },
                              title="Wagner Group Events in Africa")
events_per_year.show()


# In[3]:


#MAP of events involving Wagner Group in Africa; events graphed based on latitude and longitude coordinates of observation

events_map = px.scatter_geo(df_africa, lat = "latitude", lon = "longitude", color="country",
                     hover_name="country", scope = 'africa')
events_map.show()


# In[4]:


#HISTOGRAMS and HEATMAPS based on fatalities per country

df_africa['fatalities_new'].sum() #There are 1,242 fatalities tied to Wagner events in Africa

#histogram
fatalities_per_year = px.histogram(df_africa, x = 'year', y = 'fatalities_new', color='country', orientation = "v",
                                   labels={
                                  "year":"Year",
                                  'fatalities_new':"Fatalities",
                                  "country":"Country"
                              },
                              title="Fatalities in Africa due to Wagner Group Operations")
#fatalities_per_year.show()


#heatmap showing fatalities per country per month
country_fatalities_hm = go.Figure(data=go.Heatmap(
                   z=df_africa['fatalities_new'],
                   x=df_africa['month_year'],
                   y=df_africa['country'],
                   hoverongaps = False))
country_fatalities_hm.show()


# In[4]:


#Pie chart showing breakdown of types of events by %
event_pie = px.pie(df_africa, values='ones', names='event_type', title='Wagner Group Event Type')
event_pie.show()


#Histogram showing frequency of each event type in Africa
sub_event_hist = px.histogram(df_africa, x = 'sub_event_type', y = 'ones', color='sub_event_type')
#sub_event_hist.show()


#A new subset that only includes African countries and the top 5 most frequent event types
df_common = df_africa[(df_africa["sub_event_type"] == "Attack") | (df["sub_event_type"] == "Armed clash") | (df["sub_event_type"] == "Looting/property destruction") | (df["sub_event_type"] == "Abduction/forced disappearance")| (df["sub_event_type"] == "Change to group/activity")]
#df_common


#Histogram showing frequency of top 5 event types in Africa
sub_event_hist_common = px.histogram(df_common, x = 'sub_event_type', y = 'ones', color='sub_event_type',labels={
                                  "sub_event_type":"Event Type",
                                  'ones':"Instances",
                              },
                              title="Most Common Wagner Group Event Types")
sub_event_hist_common.show()


# In[5]:


#Histogram showing fatalities for each subevent type in Africa
fatalities_hist = px.histogram(df_africa, x = 'sub_event_type', y = 'fatalities_new', color='sub_event_type')
#fatalities_hist.show()


#A new subset that only includes African countries and the top 5 deadliest event types
df_deadly = df_africa[(df_africa["sub_event_type"] == "Attack") | (df["sub_event_type"] == "Armed clash") | (df["sub_event_type"] == "Remote explosive/landmine/IED") | (df["sub_event_type"] == "Air/drone strike")| (df["sub_event_type"] == "Non-state actor overtakes territory")]
#df_deadly


#Heatmap showing count of fatalities per event type per month
deadly_event_hm = go.Figure(data=go.Heatmap(
                   z=df_deadly['fatalities_new'],
                   x=df_deadly['month_year'],
                   y=df_deadly['sub_event_type'],
                   hoverongaps = False))
deadly_event_hm.show()


# In[6]:


#HEATMAPS based on fatalities by event type in Central African Republic

#Heatmap showing fatalities per event type over time
#within Central African Republic (where the most events and fatalities have been recorded) there was an increase in deaths caused by drone strike, attack, and armed clashes in 2022
CAR_fatalities_hm = go.Figure(data=go.Heatmap(
                   z=car['fatalities_new'],
                   x=car['month_year'],
                   y=car['event_type'],
                   hoverongaps = False))
CAR_fatalities_hm.show()

#Heatmap showing fatalities per sub_event type over time
CAR_fatalities_subtype_hm = go.Figure(data=go.Heatmap(
                   z=car['fatalities_new'],
                   x=car['month_year'],
                   y=car['sub_event_type'],
                   hoverongaps = False))
#CAR_fatalities_subtype_hm.show()


# In[7]:


#HEATMAPS based on fatalities by event type in Mali

#Heatmap showing fatalities per event type over time
#In Mali, the country with the second most fatalities, there have been an increasing number of deaths associated with attack and armed clash in recent months. Violent activity associeted with Warner has only been recorded since 2022
mali_fatalities_type_hm = go.Figure(data=go.Heatmap(
                   z=mali['fatalities_new'],
                   x=mali['month_year'],
                   y=mali['event_type'],
                   hoverongaps = False))
mali_fatalities_type_hm.show()

#Heatmap showing fatalities per sub_event type over time
mali_fatalities_subtype_hm = go.Figure(data=go.Heatmap(
                   z=mali['fatalities_new'],
                   x=mali['month_year'],
                   y=mali['sub_event_type'],
                   hoverongaps = False))
#mali_fatalities_subtype_hm.show()


# In[ ]:




