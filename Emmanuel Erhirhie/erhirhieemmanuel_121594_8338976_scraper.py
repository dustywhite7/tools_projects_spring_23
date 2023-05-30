import requests
from bs4 import BeautifulSoup
import pandas as pd

# create empty lists to store the data
schools = []
sports = []
sponsorships = []
social_media = []

base_url = 'https://nilcollegeathletes.com'


def table_per_page(url, page_number):
    response = requests.get(url + str(page_number))

    # create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the athlete student_table on the page
    student_table = soup.find('table',{'class': 'min-w-full'} )
    # print('student_table is: ', student_table)

    page_df = pd.DataFrame(columns=['Name', 'Sponsor', 'University', 'Sport'])

    for row in student_table.tbody.find_all('tr'):  
        # Find all data for each column
        columns = row.find_all('td')
        sponsors = []

        athlete_url_suffix = columns[4].find('a')['href']
        athlete_url_path = base_url + athlete_url_suffix
        print(athlete_url_suffix)
        athlete_df = get_athlete_page(athlete_url_path)

        if(columns != []):
            if columns[1].ul:
                for sponsor in columns[1].ul.find_all('li'):
                    sponsors.append(sponsor.text.strip().strip('\n'))                
            name = columns[0].text.strip()
            sponsor = sponsors
            university = columns[2].text.strip()
            sport = columns[3].text.strip()
            if athlete_df.get('Instagram') is not None:
                instagram = athlete_df.get('Instagram')[0].strip('\n').split()[0]
            else:
                instagram = ''
            if athlete_df.get('Twitter') is not None:
                twitter = athlete_df.get('Twitter')[0].strip('\n').split()[0]
            else: 
                twitter = ''
            page_df = page_df._append({'Name': name,  'Sponsor': sponsor, 'University': university, 'Sport': sport, 'Instagram': instagram, 'Twitter': twitter}, ignore_index=True)
    # print(df)
    return(page_df)

def get_all_pages(url):
    all_pages = []
    for page in range(1,430):    #Change the 430 value to the number of pages on the website
    # send a GET request to the website
        df = table_per_page(url, page)
        # print(df)
        all_pages.append(df)

    merged_df = pd.concat(all_pages)

    print(merged_df)

    merged_df.to_csv('data_frame_student.csv')

def get_athlete_url():
    print('test')


def get_athlete_page(athlete_base_url):
    response = requests.get(athlete_base_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # print(soup.encode("utf-8"))

    student_table = soup.find('dl')
    
    # student_df = pd.DataFrame(columns=['University', 'Sport', 'Sponsor', 'Platforms', 'Instagram', 'Twitter'])
    athlete_df = pd.DataFrame()

    student_attribute = []
    for student_head in student_table.find_all('dt'):
        student_attribute.append(student_head.text.strip())
    
    student_attribute_value = []
    for student_value in student_table.find_all('dd'):
        student_attribute_value.append(student_value.text.strip().strip('\n'))
    
    athlete_df['key'] = student_attribute
    athlete_df['value'] = student_attribute_value

    return athlete_df.set_index('key').T  # flips rows into columns and columns into rows

def main():
    athlete_base_url = "https://nilcollegeathletes.com/athletes"
    url = "https://nilcollegeathletes.com/athletes?page="
    get_all_pages(url)


main()