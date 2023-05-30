#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Dr. White,

Each cell below represents its fully-encompassing code for that specific objective. For example, all code
(both inside and outside of the main functions) is within that one code cell. The first code cell is everything
that I used to scrape, clean, and analyze the NIL College Athlete website. Following that, the next 3 cells each 
have everything I used to scrape, clean, and analyze the On3 Top 100, Football Top 100, and Basketball Top 100,
respectively. To run just parts of the code to get a certain output, please notice where the large breaks using
hashtags are. This is to help separate my code into readable portions. Also, for the On3 data, if you run my analysis with
newly scraped data, my values will most likely be off from what you find as the On3 website updates extremely quickly.

-James Hamlette
'''


# In[27]:


############ALL NIL College Athlete Website Scraping, Cleaning, and Analyzing Code#################

#Load relevant libraries
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
from urllib.parse import urljoin

#Define function that takes a url link and creates columns of data as follows
def collectNames(startURL):
    myPage = requests.get(startURL)
    parsed = BeautifulSoup(myPage.text)
    
    #Start with the names of the athletes via tag "a"
    a = parsed.find_all('td', class_="px-2 md:px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900")
    n=[i.a.text.strip() for i in a]
    
    #Append names to "ndata"
    ndata=[]
    for x in n:
        ndata.append(x)
    ndata=pd.DataFrame(ndata, columns=['Name'])
    
    #Append Sponsor to "t3"
    t=[]
    for i in a:
        try:
            d=i.find_next_sibling()
            t.append(d.text)
        except:
            t.append("not listed")
    t2=list(t)
    t2new= [item.strip().replace('\n','') for item in t2]
    t3=pd.DataFrame(t2new, columns=['Sponsors'])
    
    
    #Append University and Sport to "datab"
    b= parsed.find_all('span', class_="truncate")
    blist= []
    for i in b:
        blist.append(i.text)
    blist2=list(blist)
    
    #Values are in succeeding positions, so create lists for every other to split
    left = []
    right = []
    for i, j in enumerate(blist2):
        if i%2==0:
            left.append(j.strip())
        else:
            right.append(j.strip())
    
    #zip the two lists of Universities and Sports Together
    b3 = list(zip(left, right))
    b4=[list(i) for i in b3]
    datab= pd.DataFrame(b4, columns=['University', 'Sport'])
    
    
    
    #################Collect Twitter handles-DO NOT UN-COMMENT AS THIS DOESN'T WORK#########
    
    #root= "https://nilcollegeathletes.com"
    #ww = parsed.find_all('a',class_='flex text-blue-600 hover:text-blue-900', href=True)

    #wwlinks= [link['href'] for link in ww]
    #ind=[root + i for i in wwlinks]
    
   # tw=[]
    #for i in ind:
       # try:
           # mypage2= requests.get(i)
           # parse2= BeautifulSoup(mypage2.text)
           # q=parse2.find('span', class_='pr-2')
          #  tw.append(q.text)
       # except:
         #   tw.append("none")
    #tw=pd.DataFrame(tw, columns=['Twitter'])
    
    #######################################################################################
    
    
    #Inner join of ndata and datab
    all_data= ndata.join([datab,t3])
    
    #Parse through all remaining pages if there is one, then concatenate using recursive function
    try:
        nextPage= urljoin( 'https://nilcollegeathletes.com', parsed.find('div', class_="-mt-px flex w-0 flex-1 justify-end").a['href'])
    except:
        nextPage=None
    if nextPage:
        return pd.concat([all_data,collectNames(nextPage)], axis=0)
    else:
        return all_data
###############################################END OF FUNCTION###########################################################



#############BEGIN EXTRACTION################

main_data=collectNames('https://nilcollegeathletes.com/athletes')
main_data
main_data.to_csv("main_data.csv")

####ANALYSIS#####

#NIL Deals By Sport Horizontal Histogram
import plotly.express as px
import plotly.graph_objs as go
plot1=px.histogram(main_data, y="Sport", color_discrete_sequence=['red'],opacity=0.9, title="Sport Distribution among NIL Deals",orientation='h')
plo1
#NIL Deals By Sponsor Table (in percents) for the top 10
table0=main_data['Sponsors'].value_counts
table0=table2.nlargest(10)
table0


# In[37]:


##################### ON3 TOP 100 OF ALL ATHLETES SCRAPING, CLEANING, ANALYSIS#######################

#import relevant libraries
import numpy as np
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

#Define a scraping function to take a url link value
def onThree(scrapeurl):
    myPage_ = requests.get("https://www.on3.com/nil/rankings/player/nil-100/")
    soup = BeautifulSoup(myPage_.text)

    #Scrape Names and append to dataframe
    oo= soup.find_all('a', class_="MuiTypography-root MuiLink-root MuiLink-underlineNone NilPlayerRankingItem_name__nzSp9 MuiTypography-h5 MuiTypography-colorPrimary")
    oo=list(oo)

    ood=[]
    for o in oo:
        oo2=o.text
        ood.append(oo2)
    ood=pd.DataFrame(ood, columns=['Name'])
    
    
    #Scrape the text/string number of followers
    for o in oo:
        uu= soup.find_all('p', class_="MuiTypography-root NilPlayerRankingItem_followersNumber__ifWQr MuiTypography-body1 MuiTypography-colorTextPrimary")
        uu=list(uu)

    uud=[]
    for u in uu:
        try:
            uu2=u.text
            uud.append(uu2)
        except:
            uud.append("blank")
    uud=pd.DataFrame(uud, columns=['Followers'])
    
    #Scape the String of NIL Valuation
    vv= soup.find_all('p', class_="MuiTypography-root NilPlayerRankingItem_valuationCurrency__oSkvo MuiTypography-body1 MuiTypography-colorTextPrimary")

    vvd=[]
    for v in vv:
        vvs=v.text
        vvd.append(vvs)
    vvd=pd.DataFrame(vvd, columns=['Valuation'])
    
    #Join the datasets
    full_data=ood.join([uud,vvd])
    
    #No further pages so just return
    return full_data
###############################################################################################

##Begin Extraction using defined function
tophundred=onThree("https://www.on3.com/nil/rankings/player/nil-100/")
tophundred.to_csv("on3top100.csv")

############################################CLEANING BELOW###################################################################

#Valuation has "$", so remove to allow for quantitative analysis
tophundred['Valuation']=tophundred['Valuation'].str.replace('$','')

###Values for thousands, millions etc are as "5K"; write function to convert to numeric values "5,000"
def value_change(num):
    if num[-1:]=='K':
        return float(num[:-1]) * 10**3
    elif num[-1:]=='M':
        return float(num[:-1]) * 10**6
    elif num[-1:]=='B':
        return float(num[:-1]) * 10**9
    else:
        num=float(num)

#Use value_change function to apply it to both followers and valuation columns without replacing original data
tophundred['Followers_total']=tophundred['Followers'].apply(value_change)
tophundred['Valuation_total']=tophundred['Valuation'].apply(value_change)

#Generate Rank variable based on the index
tophundred['Rank']=tophundred.index +1
###############################################################

########################ANALYSIS######################

#Top 100 Athletes Scatter plot Valuation by Rank
plot2=px.scatter(tophundred,x="Valuation_total",y="Rank",title="Top 100 Athletes NIL Valuation by Rank")
plot2
#Top 100 Athletes Summary with commas as thousands
pd.options.display.float_format='{:,.0f}'.format
summary=tophundred.describe()
print(summary)
#Scatter plot showing Rank by how many social media followers they have; define title
plot3=px.scatter(tophundred, x='Followers_total', y='Rank', title="Top 100 Athletes Social Media Followers by Rank")
plot3
#####################################################


# In[38]:


summary


# In[39]:


################ ALL ON3 FOOTBALL SCRAPING, CLEANING, ANALYSIS#######################


#import relevant libraries
import numpy as np
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

###############Define function to scrape on3 football top 100######################

def onThreeFootball(scrapeurl):
    myPage_ = requests.get("https://www.on3.com/nil/rankings/player/college/football/")
    soup = BeautifulSoup(myPage_.text)

    #Scrape Names and append to dataframe
    oo= soup.find_all('a', class_="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-h5 MuiTypography-colorPrimary")
    oo=list(oo)

    ood=[]
    for o in oo:
        oo2=o.text
        ood.append(oo2)
    ood=pd.DataFrame(ood, columns=['Name'])
    
    
    #Scrape the text/string number of followers and append to dataframe
    for o in oo:
        uu= soup.find_all('p', class_="MuiTypography-root NilPlayerRankingItem_followersNumber__ifWQr MuiTypography-body1 MuiTypography-colorTextPrimary")
        uu=list(uu)

    uud=[]
    for u in uu:
        try:
            uu2=u.text
            uud.append(uu2)
        except:
            uud.append("blank")
    uud=pd.DataFrame(uud, columns=['Followers'])
    
    #Scape the String of NIL Valuation and append to dataframe
    vv= soup.find_all('p', class_="MuiTypography-root NilPlayerRankingItem_valuationCurrency__oSkvo MuiTypography-body1 MuiTypography-colorTextPrimary")

    vvd=[]
    for v in vv:
        vvs=v.text
        vvd.append(vvs)
    vvd=pd.DataFrame(vvd, columns=['Valuation'])
    
    #Scrape the String of position and append to dataframe
    jj= soup.find_all('span', class_="MuiTypography-root NilPlayerRankingItem_position__vZ3bv MuiTypography-body1 MuiTypography-colorTextPrimary")

    jjd=[]
    for j in jj:
        jjs=j.text
        jjd.append(jjs)
    jjd=pd.DataFrame(jjd, columns=['Position'])
    
    #Join completed dataframes into one dataframe
    full_data2=ood.join([uud,vvd,jjd])
    
    return full_data2
#################################################END OF FUNCTION###########################################################
#Run the function and create csv file
on3top100_football=onThreeFootball("https://www.on3.com/nil/rankings/player/college/football/")
on3top100_football.to_csv("on3top100_football.csv")
on3top100_football

###Values for thousands, millions etc are as "5K"; write function to convert to numeric values "5,000"
def value_change(num):
    if num[-1:]=='K':
        return float(num[:-1]) * 10**3
    elif num[-1:]=='M':
        return float(num[:-1]) * 10**6
    elif num[-1:]=='B':
        return float(num[:-1]) * 10**9
    else:
        num=float(num)


#Get rid of dollar signs within valuation string
on3top100_football['Valuation']=on3top100_football['Valuation'].str.replace('$','')

#Create rank variable that is based on pre-defined index
on3top100_football['Rank']=on3top100_football.index +1

#Apply the value_change function to create a new column of values that are floats instead of strings
on3top100_football['Followers_total']=on3top100_football['Followers'].apply(value_change)
on3top100_football['Valuation_total']=on3top100_football['Valuation'].apply(value_change)

################################Analysis###########################################################################

#Make bar chart of NIL valuation for top 100 football players, grouped by position
plot4=px.bar(on3top100_football, x="Position",y="Valuation_total", title="NIL Valuation by Football Position")
plot4
#Make table of percent in each position out of top 100
table1=on3top100_football['Position'].value_counts()
table1


# In[41]:


plot4


# In[42]:


################ ALL ON3 BASKETBALL SCRAPING, CLEANING, ANALYSIS#######################


#Import relevant libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup


###############Define function to scrape on3 football top 100######################
def onThreeBasketball(scrapeurl):
    myPage_ = requests.get("https://www.on3.com/nil/rankings/player/college/basketball/")
    soup = BeautifulSoup(myPage_.text)

    #Scrape Names and append to dataframe
    oo= soup.find_all('a', class_="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-h5 MuiTypography-colorPrimary")
    oo=list(oo)

    ood=[]
    for o in oo:
        oo2=o.text
        ood.append(oo2)
    ood=pd.DataFrame(ood, columns=['Name'])
    
    
    #Scrape the text/string number of followers and append to dataframe
    for o in oo:
        uu= soup.find_all('p', class_="MuiTypography-root NilPlayerRankingItem_followersNumber__ifWQr MuiTypography-body1 MuiTypography-colorTextPrimary")
        uu=list(uu)
    
    uud=[]
    for u in uu:
        try:
            uu2=u.text
            uud.append(uu2)
        except:
            uud.append("blank")
    uud=pd.DataFrame(uud, columns=['Followers'])
    
    #Scape the String of NIL Valuation and append to dataframe
    vv= soup.find_all('p', class_="MuiTypography-root NilPlayerRankingItem_valuationCurrency__oSkvo MuiTypography-body1 MuiTypography-colorTextPrimary")

    vvd=[]
    for v in vv:
        vvs=v.text
        vvd.append(vvs)
    vvd=pd.DataFrame(vvd, columns=['Valuation'])
    
    #Scrape the String of position and append to dataframe
    jj= soup.find_all('span', class_="MuiTypography-root NilPlayerRankingItem_position__vZ3bv MuiTypography-body1 MuiTypography-colorTextPrimary")

    jjd=[]
    for j in jj:
        jjs=j.text
        jjd.append(jjs)
    jjd=pd.DataFrame(jjd, columns=['Position'])
    
    
    #Join all dataframes into one and return it
    full_data2=ood.join([uud,vvd,jjd])
    
    return full_data2
###################################################END OF FUNCTION#####################################################

###Begin Extraction and create csv
on3top100_Basketball=onThreeBasketball("https://www.on3.com/nil/rankings/player/college/basketball/")
on3top100_Basketball.to_csv("on3top100_Basketball.csv")
on3top100_Basketball
###Values for thousands, millions etc are as "5K"; write function to convert to numeric values "5,000"
def value_change(num):
    if num[-1:]=='K':
        return float(num[:-1]) * 10**3
    elif num[-1:]=='M':
        return float(num[:-1]) * 10**6
    elif num[-1:]=='B':
        return float(num[:-1]) * 10**9
    else:
        num=float(num)


        
#Get rid of dollar signs within valuation string
on3top100_Basketball['Valuation']=on3top100_Basketball['Valuation'].str.replace('$','')

#Create rank variable that is based on pre-defined index
on3top100_Basketball['Rank']=on3top100_Basketball.index +1

#Apply the value_change function to create a new column of values that are floats instead of strings
on3top100_Basketball['Followers_total']=on3top100_Basketball['Followers'].apply(value_change)
on3top100_Basketball['Valuation_total']=on3top100_Basketball['Valuation'].apply(value_change)

################################Begin Graphing###########################################################################

import plotly.express as px
#Make bar chart of NIL valuation for top 100 basketball players, grouped by position
plot5=px.bar(on3top100_Basketball, x="Position",y="Valuation_total", title="NIL Valuation by Basketball Position")
plot5
#Make table of percent in each position out of top 100
table2=on3top100_Basketball['Position'].value_counts()
table2


# In[44]:


plot5

