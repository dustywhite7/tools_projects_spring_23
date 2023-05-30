# ECON 8320 Semester Project - Spring 2023 - Brett Thompson

#Importing Beautiful Soup.
from bs4 import BeautifulSoup
#Importing Numpy.
import numpy as np
#Importing Pandas.
import pandas as pd
#Importing Time to be able to add a time delay when using Selenium.
import time

#Importing Selenium.
from selenium import webdriver
from selenium.webdriver.common.by import By

#Setting the file path to get to the Selenium executable file that will load more pages.
PATH = "/Users/brett/Documents/Miscellaneous/School/ECON 8320/chromedriver.exe"
#Setting the Selenium driver to the path above.
driver = webdriver.Chrome(PATH)

#Telling the driver to open the on# NIL deals page.
driver.get("https://www.on3.com/nil/deals/")

#Finding all of the buttons that have the same name as the 'Load More' button.
click_button = driver.find_elements(by=By.CLASS_NAME, value='MuiButton-label')

#Setting a number of times that the 'Load More' button will get clicked.
for i in range(3):
    #Choosing the last button in the click_button variable because this is the 'Load More' button that we want to click.
    click_button[-1].click()
    #Telling Selenium to wait 5 seconds before it loops again to allow the page to load.
    time.sleep(5)

#Creating a variable with the On3 html after Selenium has loaded more data on the webpage.
on3html = driver.page_source

#Parsing the html with Beautiful Soup
parsednildata = BeautifulSoup(on3html, 'html.parser')

#Creating an empty matrix that all of the data will get added to before getting converted to a dataframe.
nildata = []

#Creating lists for sports which contain their positions. Certain position abbreviations were used across multiple sports so they were left out of the lists. For example 'S' was in Football (Safety), Volleyball (Setter), Swimming (Swimmer), and Track & Field (Sprinter).
football = ['QB','RB','WR','TE','IOL','OT','ATH','DL','EDGE','LB','CB']
basketball = ['PG','SG','CG','SF','PF','C']
golf = ['G']
soccer = ['AT','MF','GK','DF']
volleyball = ['OH','DS','L','MB']
baseball = ['IF','P','OF']
gymnastics = ['ALL','All','UB']
track = ['PV','DR','J']

#Looping through each athlete in the html. The athletes were all in an 'li' container.
for name in parsednildata.find_all('li', {"class":"DealTrackerItem_container__yWF2E"}):
    
    #Creating the empty list that each athletes data will get appended to. After looping through each athlete, row will get appended to the nildata matrix.
    row = []
    
    #Extracting the athlete's name. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("div", {"class": "PlayerDealItem_playerName__K5EXe"}).text)
    except:
        row.append(np.nan)
    
    #Extracting the athlete's On3 NIL Value. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("span", {"class": "PlayerDealItem_nilValueText__3Vv7n"}).text)
    except:
        row.append(np.nan)   
        
    #Extracting the athlete's experience/year. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("h6", {"class": "MuiTypography-root PlayerDealItem_classRank__k7iFc MuiTypography-subtitle1 MuiTypography-colorTextPrimary"}).text)
    except:
        row.append(np.nan)    
    
    #Extracting the athlete's school. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("img", {"class": "PlayerDealItem_committedAssetLogo__4IX6_"}).attrs['title'])
    except:
        row.append(np.nan)  
    
    #Extracting the athlete's position. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("span", {"aria-label": "Position"}).text)
    except:
        row.append(np.nan)  
        
    #Determining the athlete's sport. Appending it to row. The sport is determined by checking to see if the athlete's position abbreviation is in one of the sport lists created above. If nothing is given by On3 or if the sport is not able to be determined by the position abbreviation, nan will be appended to row.
    try:
        if name.find("span", {"aria-label": "Position"}).text in football:
            row.append('Football')
        elif name.find("span", {"aria-label": "Position"}).text in basketball: 
            row.append('Basketball')
        elif name.find("span", {"aria-label": "Position"}).text in golf: 
            row.append('Golf')
        elif name.find("span", {"aria-label": "Position"}).text in soccer: 
            row.append('Soccer')
        elif name.find("span", {"aria-label": "Position"}).text in volleyball: 
            row.append('Volleyball')
        elif name.find("span", {"aria-label": "Position"}).text in baseball: 
            row.append('Baseball')     
        elif name.find("span", {"aria-label": "Position"}).text in gymnastics: 
            row.append('Gymnastics') 
        elif name.find("span", {"aria-label": "Position"}).text in track: 
            row.append('Track')  
        else:
            row.append(np.nan) 
    except:
        row.append(np.nan)    
        
    #Extracting the company/client the athlete is working with. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("h5", {"class": "MuiTypography-root MuiTypography-h5 MuiTypography-colorTextPrimary"}).text)
    except:
        row.append(np.nan)      
        
    #Extracting the collective the athlete is working with. Appending it to row. If nothing is given by On3, nan will be appended to row.
    try:
        row.append(name.find("a", {"class": "MuiTypography-root MuiLink-root MuiLink-underlineNone DealTrackerItem_collectiveLink__DgG6Z MuiTypography-caption MuiTypography-colorPrimary"}).text)
    except:
        row.append(np.nan)    
        
    #Appending the list 'row' with all of the athlete's data to the nildata matrix.    
    nildata.append(row)

#Converting the nildata matrix to a Pandas dataframe.    
nildata = pd.DataFrame(nildata, columns = ['Name', 'NIL Value', 'Year', 'School', 'Position', 'Sport', 'Company/Client', 'Collective'])

#Putting the dataframe into a .csv file named nildata.csv and located locally on my computer.
nildata.to_csv("/Users/brett/Documents/Miscellaneous/School/ECON 8320/nildata.csv")