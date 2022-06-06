from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import pandas as pd



options = webdriver.ChromeOptions()
options.headless = True # opens chrome in the background

# Launches the chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
url = 'https://trends.google.com/trends/trendingsearches/daily?geo=US'

driver.get(url) # opens url
time.sleep(5) # waits for 5 seconds to allow the page to open


html =driver.page_source # gets the html from the page source
soup = BeautifulSoup(html, 'html.parser') # Parses the html in the page using BEautifulSoup

search_trends = [] # initializes a list for all search trends
no_of_searches = [] # initializes a list for the number of each search trend


trending_results = soup.find_all("md-list") # finds all the search trends in the last 24 hours

for result in trending_results[1:]:
    # print(repr(result.text))
    result = result.text.strip().split()
    trend = ' '.join(result)

    def parser(pattern):
        '''
        This function parses information about each search trend and gets only what is relevant
        based on the regex pattern passed
        
        '''
        
        result = re.search(pattern, trend)
        result = result.group(1)
        return result

    trend_name = parser(r"\d\s(.*)share") # parses each search trend to extract the name of the search trend
    search_trends.append(trend_name) # adds the search trend to the list of popular searches

    searches = parser(r"searches\s(.*)\searches") # parses each search trend to extract the number of times it has been searched

    # Google trend provides the number of searches in a shortened form
    # This section converts the shortened number of searches into actual integers
    if 'K+' in searches:
        searches = searches.strip('K+')
        searches = int(searches) * 1000
    elif 'M+' in searches:
        searches = searches.strip('M+')
        searches = int(searches) * 1000000

    no_of_searches.append(searches) # adds the number of searches to the list

# initializes a dictionary with the Keys as the column names and values as the entry into each column
dictionary = {
  'Search Trend': search_trends,
  'Number of Searches (+)': no_of_searches
  } 

df=pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dictionary.items()]))
print(df)

# writes the data into sample.data csv
df.to_csv(''+'sample_data'+'.csv',encoding='utf-8-sig')

print('---------------------')
print('Operation Closed')
    


