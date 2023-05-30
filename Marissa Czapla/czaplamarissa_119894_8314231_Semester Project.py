#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

#collect information for each althete on page
def collectAthletes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='min-w-full divide-y divide-gray-200')
    data = []

#collect the name, sponsor, university and sport of each athlete    
    for athlete in table.find_all('tbody'):
        rows = athlete.find_all('tr')
        for row in rows:
            athlete = row.find('td', class_='px-2 md:px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900').text.strip()
            sponsors = [i.strip() for i in row.find('td', class_='px-2 md:px-6 py-4 whitespace-nowrap').text.strip().split('\n') if len(i.strip())> 0]
            university = row.find('span', class_="truncate").text.strip()
            sport = row.find('span', class_="text-sm text-gray-900 truncate").text.strip()
            
#create an individual row for each sponsor that an athlete has and add to a data frame            
            for sponsor in sponsors:
                data.append([athlete, sponsor, university, sport])
    data = pd.DataFrame(data, columns=['athlete', 'sponsor', 'university', 'sport'])


#go to the next page and append athlete information to the original data frame    
    try: 
        next_button = soup.find('a', class_="inline-flex items-center border-b-2 border-transparent py-2 pl-1 text-sm font-medium text-gray-500 hover:border-blue-700 hover:text-gray-700")['href']
    except:
        next_button = None
        
    if next_button:
        return pd.concat([data, collectAthletes('https://nilcollegeathletes.com' + next_button)],axis=0)
    else:
        return data

url= 'https://nilcollegeathletes.com/athletes'        

data = collectAthletes(url)

#create a bar chart that looks at the top sponsors     
top_sponsors = data['sponsor'].value_counts().nlargest(20)
fig = px.bar(x=top_sponsors.index, y=top_sponsors.values)
fig.update_layout(title='Top 20 Sponsors', xaxis_title='Sponsor', yaxis_title='Count')
fig.show()


#create a bar chart that looks at top sponsors excluding barstool sports
top_sponsors = data['sponsor'].value_counts().nlargest(20)
#exclude Barstool Sports
top_sponsors = top_sponsors[top_sponsors.index != "Barstool Sports"]
fig1 = px.bar(x=top_sponsors.index, y=top_sponsors.values)
fig1.update_layout(title='Top 20 Sponsors w/Barstool', xaxis_title='Sponsor', yaxis_title='Count')
fig1.show()

top_athlete = data['athlete'].value_counts().nlargest(10)
fig2 = px.bar(x=top_athlete.index, y=top_athlete.values)
fig2.update_layout(title='Top Athletes',xaxis_title='Athlete',yaxis_title='Count')
fig2.show()

top_sport = data['sport'].value_counts().nlargest(10)
fig4 = px.bar(x=top_sport.index, y=top_sport.values)
fig4.update_layout(title='Top Sport',xaxis_title='Sport',yaxis_title='Count')
fig4.show()

top_univ = data['university'].value_counts().nlargest(10)
fig5 = px.bar(x=top_univ.index, y=top_univ.values)
fig5.update_layout(title='Top College',xaxis_title='College',yaxis_title='Count')
fig5.show()

collectAthletes(url)

