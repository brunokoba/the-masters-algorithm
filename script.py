from urllib.request import Request
import requests
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd

# Initializing writer 
csv_file = open('database.csv', 'w', buffering=1, encoding='utf8')
csv_file.write('\ufeff')
writer = csv.writer(csv_file, lineterminator = '\n')

# List of URLs to be scraped
urls = ['https://www.usnews.com/best-graduate-schools/top-engineering-schools/eng-rankings',
        'https://www.usnews.com/best-graduate-schools/top-engineering-schools/eng-rankings/page+2',
        'https://www.usnews.com/best-graduate-schools/top-engineering-schools/eng-rankings/page+3']

# Initializing features to be collected (each list will be a column in the final .csv file, except "univ_pages")
names = []
locations = []
univ_pages = []
inter_deadlines = []
inter_fees = []
ft_teachers = []
ft_enrollments = []
ft_tuitions = []
admissions_links = []
records = []

# Setting agent for scraping authentication
headers = {'User-Agent':'Mozilla/5.0'}

# Loop over the list of URLs
for url in urls:
    
    # Requesting page and saving them as soup objects
    req = requests.get(url, headers=headers)
    data = soup(req.text, "html5lib")
    
    # Appending each found value to the first three features
    for name in data.findAll('a', attrs={'class': 'school-name'}):
        names.append(name.string)
    for location in data.findAll('p', attrs={'class': 'location'}):
        locations.append(location.string)
    for univ_page in data.findAll('a', attrs={'class': 'school-name', 'href': True}):
        univ_pages.append(univ_page['href'])
        
# Extracting information from new URLs, which specific to each university
for univ_page in univ_pages:    
    new_url = 'https://www.usnews.com' + univ_page
    req2 = requests.get(new_url, headers=headers)
    data2 = soup(req2.text, "html5lib")
    
    # Collecting international deadline data
    inter_deadline = data2.find('td', attrs={'class':"column-last", 'data-test-id':"v_international_deadline"})
    try:    
        inter_deadlines.append(inter_deadline.text.strip())
    except:
        inter_deadlines.append(None)
    
    # Collecting international application fee data
    inter_fee = data2.find('td', attrs={'class':"column-last", 'data-test-id':"intl_application_fee"})
    try:
        inter_fees.append(inter_fee.text.strip())
    except:
        inter_fees.append(None)
    
    # Collecting full-time faculty data
    ft_teacher = data2.find('td', attrs={'class':"column-last", 'data-test-id':"ft_teachers"})
    try:
        ft_teachers.append(ft_teacher.text.strip())
    except:
        ft_teachers.append(None)
        
    # Collecting full-time enrollment data
    ft_enrollment = data2.find('td', attrs={'class':"column-last", 'data-test-id':"v_ft_enrolled_dir_pg"})
    try:
        ft_enrollments.append(ft_enrollment.text.strip())
    except:
        ft_enrollments.append(None)
        
    # Collecting full-time tuition data
    ft_tuition = data2.find('tr', attrs={'class':"extra-row v_mas_tuition_ft-extra-row"})
    try:
        ft_tuitions.append(ft_tuition.text.strip())
    except:
        ft_tuitions.append(None)
        
    # Collecting admissions links
    admissions_link = data2.find('a', attrs={'class':"t-strong", 'id': 'moreinfo_link', 'href':True})['href']
    try:
        admissions_links.append(admissions_link)
    except:
        admissions_links.append(None)    

# Add titles
titles = ['Rank', 'School', 'Location', 'Application Deadline', 
          'Application Fee', 'Full-time Faculty', 'Full-time enrollment', 
          'Full-time tuition', 'Grad admissions link']

# Write table titles
writer.writerow(titles)

# Add data to be written in .csv file, row by row
for i in range(len(names)):
    records.extend([i+1,
                    names[i],
                    locations[i],
                    inter_deadlines[i],
                    inter_fees[i],
                    ft_teachers[i],
                    ft_enrollments[i],
                    ft_tuitions[i],
                    admissions_links[i]])
    
    # Writing data into .csv file and reinitilizing storage variable
    writer.writerow(records)
    records = []
    
# Reading as a pandas DataFrame    
df = pd.read_csv('database.csv')
df.head()
