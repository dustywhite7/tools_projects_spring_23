##Installs previously not included in class was urllib.parse and selenium

##Because opendorse uses javascript functions to hide teams and players on the site we will need to install
## a web driver to allow python to interact with our preferred browser. If you want to use chrome the driver can be
## found here https://sites.google.com/a/chromium.org/chromedriver/downloads
## I used firefox which required a download from github, that repository can be found here https://github.com/mozilla/geckodriver/releases

import time 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
import requests
import pandas as pd
from bs4 import BeautifulSoup


##This function utilizes our web browser to click through the pages "see more" buttons until all teams are loaded.
## It then will take use beautiful soup to parse through every team icon and pull the url that gets added to opendorse
## so that we have a list of all the links to all of the teams avaialbe on the sight
def load_all_teams(url):
    driver = webdriver.Firefox() #Here is where we implement our webdriver, I could not figure out why my execution path was not working, so I manually opened the driver to have it listen while the code ran
    # This part could be improved

    driver.get(url) #Here we open our web page progamatically and go to our website

    while True: #this while loop will find the button and click until the see more button no longer appears and then will break
        try:
            see_more_button = driver.find_element('css selector','button.sc-ab9b38c8-0:nth-child(2)') #Copying the CSS path from the website we can easily find the see more button
            see_more_button.click() #function is self explanatory, selenium will click on the button
            time.sleep(2) #we have to give the browser time to load the button again or it will break too fast
        except NoSuchElementException: #this a useful part of selenium, if it can't find what we specificifed we break
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser') #saving our pased html to a variable. The driver.page_source is a function that spits out the url of the page the web driver is on, that way we have the expanded list available to pull team links from
    team_links = [urljoin(url, a['href']) for a in soup.select('div.hOQFLF div.eHfFxC a')] #Team_links variable pulls the team url extension and concatenates the opendorse parent url to give us the specific team site for each individual team
    
    driver.quit() #The quit function tells our web browser to close after we pull our information

    return team_links #we return our list of team links to parse through



##Similar to our load_all_teams function, we are going to use the same logic to get every player loaded onto the page
##Since all of the players are stored on one page and hidden behind a javascript button we must go through the same process
def load_all_athletes(team_url):
    driver = webdriver.Firefox() #again we need to load up a web browser

    driver.get(team_url) #We need to go to the site we need

    while True: #We find the see more button and click it until the button stops showing up
        try:
            see_more_button = driver.find_element('css selector','button.sc-ab9b38c8-0:nth-child(2)')
            see_more_button.click()
            time.sleep(2) 
        except NoSuchElementException:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser') #We parse the webpage our driver clicked through
    base_url = 'https://opendorse.com' #we create the base url needed to concatenate our individual player links
    athlete_links = [urljoin(base_url, a['href']) for a in soup.select('div.hOQFLF div.fXWNmg a')]  #We look at each individual tag and concatenate the opendorse parent url with the individual player link
    
    driver.quit() #We quit the driver so when we run our functino we dont open a web page for each individual team (lesson learned)
    
    return athlete_links #We return a list of all player links for that specific team

##This function was required because of an issue I was having when with extraction of player info and loading it into a dictionary
def safe_extract_text(selector, soup): #takes arguements selctor, and the url of each individual player from a team
    element = soup.select_one(selector) #Selects the appropriate text so that we can run an if statement to test of the subsection item for a player comes back with anything or not
    return element.text.strip() if element else None #Returns the element we want to extract or a blank

##This is our function extracts all of the player information from all of the player links that we grabbed earlier. For this function we have one input variable being the player link from the player link list which we will loop through
def extract_player_info(athlete_url): 
    response = requests.get(athlete_url) #Here we use request to get our HTML
    soup = BeautifulSoup(response.text, 'html.parser') #We use beautiful soup to parse

    name = safe_extract_text('.debHsu > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > h1:nth-child(1) > div:nth-child(1)', soup) #We can use the css pass to easily find the name as it will be in the same location on every page
    position = safe_extract_text('.debHsu > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > h1:nth-child(1) > div:nth-child(2) > p:nth-child(1)', soup) #Same with position groupings, this information will be in the same place on every page
    affiliation = safe_extract_text('div[data-qa="affiliations-subsection"] p.bffqNn', soup) #Each subsection div class has the subsection labelled, we cannot use the css path as some subsections are not filled in for every athlete so we must specify
    location = safe_extract_text('div[data-qa="location-subsection"] p.bffqNn', soup)  #The next few sections all have to be specific because of the issues discussed previously
    background = safe_extract_text('div[data-qa="background-subsection"] p.bffqNn', soup)  
    hometown = safe_extract_text('div[data-qa="hometown-subsection"] p.bffqNn', soup)  
    service = safe_extract_text('div.sc-93fb2f96-0:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(1)', soup) #The payment information is in a different part of the page so we can use the css path as we are only scraping the frequently used service
    cost = safe_extract_text('div.sc-93fb2f96-0:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(2)', soup) 
    
    #Here we compile the player info into a dictionary so that we can easily load it into a dataframe
    player_info = {
        'Name': name,
        'Sport/Position': position,
        'Affiliation': affiliation,
        'Location': location,
        'Background': background,
        'Hometown': hometown,
        'Service': service,
        'Cost': cost,
    }

    return player_info #We return the player information dictionary

team_links = load_all_teams('https://opendorse.com/browse/teams') #this is the base url needed to scrube the teams and we pass our load_all_teams function to scrape the team links for every single team on the site
all_players = [] #Here we create our blank list where we can append all of the individual page links for each player

##This is or for loop that will go through each team then each player on that team to scrape the data for that player
for team_link in team_links: #for each team in we are going to load all of the athletes from that team
    athlete_links = load_all_athletes(team_link) #Once we have all of the athletes for that team we are going to loop through those athletes
    
    for athlete_link in athlete_links: #For every athlete link we scraped from our team we are going to extract all information from each individual page
        player_info = extract_player_info(athlete_link)
        all_players.append(player_info) #Then append that information into our all players list

df = pd.DataFrame(all_players) #We then save list of dictionaries into a data frame
df.to_csv('players.csv', index=False) #and save the data as a csv so we can manipulate it further and do analysis