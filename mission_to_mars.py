# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd


# In[2]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


# Define database and collection
db = client.mission_to_mars
collection = db.items


# In[4]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
response


# In[5]:


soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())


# In[6]:


# Examine the results, then determine element that contains sought info
# results are returned as an iterable list
results = soup.find_all('div', class_='slide')

# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of article
        title = result.find('div', class_='content_title').find('a').text
        description = result.find('div', class_='image_and_description_container').find('a').find('div', class_='rollover_description').find('div', class_='rollover_description_inner').text

        # Run only if title is available
        if (title):
            # Print results
            print('-------------')
            print(title)
            print(description)

            # Dictionary to be inserted as a MongoDB document
            articles = {
                'title': title,
                'description': description
            }


    except Exception as e:
        print(e)


# In[7]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())


# In[8]:


#
import cssutils
div_style = soup.find('article')['style']
style = cssutils.parseStyle(div_style)
url = style['background-image']


url1 = url.strip('url')
url2 = url1.strip('(')
url3 = url2.strip(')')

jpg_link = {
                'jpg': url3
            }


print('https://www.jpl.nasa.gov'+url3)


# In[9]:


executable_path = {'executable_path': 'chromedriver.exe'}
url = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())


# In[10]:


results = soup.find_all('li', class_='js-stream-item stream-item stream-item')
tweets = []

#Identify and return title of article
for result in results:
    
    tweet = result.find('p', class_='tweet-text').text
    tweets.append(tweet)

for content in tweets:
    if content.startswith('InSight sol') == False:
        '0'
    else:
        print(content)
        break
mars_weather = {
                'tweet': content
            }


# In[11]:


executable_path = {'executable_path': 'chromedriver.exe'}
url = 'https://space-facts.com/mars/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())


# In[12]:


results = soup.find('tbody')

labels = []
data = []

#Identify and return title of article
for result in results:
    
    column_1 = result.find('td', class_='column-1').text
    labels.append(column_1)
for result in results:
    
    column_2 = result.find('td', class_='column-2').text
    data.append(column_2)

mars_table = {
                'labels': labels,
                'data': data
            }
    
table_df = pd.DataFrame(list(zip(labels, data)), columns =['Measurement', 'Result']) 
table_df 


# In[13]:


table_df = table_df.to_html()
table_df.replace('\n', '')

table_df


# In[14]:


listings = db.items.find()

for listing in listings:
    print(listing)


# In[ ]:

def scrape():
    listings = {}

    listings["articles", "jpg_link", "mars_weather", "mars_table"]

    return listings



