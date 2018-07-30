from urllib.request import Request
import requests
from bs4 import BeautifulSoup as soup
import re
import csv
import io
import pandas as pd

# Initializing writer 
csv_file = open('database.csv', 'w', buffering=1, encoding='utf8')
writer = csv.writer(csv_file, lineterminator = '\n')

# List of URLs to be scraped
urls = ['https://www.usnews.com/best-graduate-schools/top-engineering-schools/eng-rankings',\
        'https://www.usnews.com/best-graduate-schools/top-engineering-schools/eng-rankings/page+2']

# Initializing features to be collected (each list will be a column in the final .csv file)
names = []
locations = []
tuitions = []
enrollments = []
univ_pages = []
records = []

# Setting agent for scraping authentication
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
headers = {'User-Agent':'Mozilla/5.0'}

# Loop over the list of URLs
for url in urls:
    
    # Requesting page and saving them as soup objects
    r = requests.get(url, headers=headers)
    data = soup(r.text, "html5lib")
    
    # Appending each found value to the features lists
    for name in data.findAll('a', attrs={'class': 'school-name'}):
        names.append(name.string)
    for location in data.findAll('p', attrs={'class': 'location'}):
        locations.append(location.string)
    for univ_page in data.findAll('a', attrs={'class': 'school-name', 'href': True}):
        univ_pages.append(univ_page['href'])
    for tuition in data.findAll('td', attrs={'span': 'column-odd table-column-odd search_tuition'}):
        tuitions.append(tuition.string)
        print(tuition)
    for enrollment in data.findAll('td', attrs={'class': 'column-even table-column-even  total_enrolled  '}):
        enrollments.append(enrollment.string)
        print(enrollments)
        
# Add data to the .csv file row by row
for i in range(len(names)):
    records.append(i+1)
    records.append(names[i])
    records.append(locations[i])
    records.append(univ_pages[i])
    writer.writerow(records)
    records = []
    
# Reading as a pandas DataFrame    
df = pd.read_csv('database.csv')
print(df)
