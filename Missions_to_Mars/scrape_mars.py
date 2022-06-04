# Import Dependancies
import pandas as pd
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Set up for browswer to use Chrome
def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


################## NASA Mars News ##################

# Set up browswer to visit NASA Mars News
url = "https://redplanetscience.com/"
browser.visit(url)

# Delay URL from opening for one second
time.sleep(1)

# Scrape page into Soup
html = browser.html
soup = bs(html, "html.parser")

# Locate most recent news title and paragraph
news_title = soup.find_all('div', class_='content_title')[0].text
news_p = soup.find_all('div', class_='article_teaser_body')[0].text


################## JPL Mars Space Images—Featured Image ################## 

# Set up browswer to visit JPL Mars Space Images
mars_space_url = "https://spaceimages-mars.com"
browser.visit(mars_space_url)

# Delays URL from opening for one second
time.sleep(1)

# Scrape page into Soup
html = browser.html
soup = bs(html, 'html.parser')

# Iterate to locate image location
img = [i.get("src") for i in soup.find_all("img", class_="headerimage fade-in")]

# View full featured image url
featured_image_url = url + img

# Save URL to variable
""" featured_image_url = "https://redplanetscience.com/image/featured/mars3.jpg"
 """

################## Mars Facts ################## 

# Visit the following URL
mars_facts_url = "https://galaxyfacts-mars.com"

# Delays URL from opening for one second
time.sleep(1)

# Use read_html to parse the URL
tables=pd.read_html(mars_facts_url)

# Locate mars facts table
mars_facts=tables[1]

# Rename default column names, raise exception and erase index
mars_facts=mars_facts.rename(columns={0:"Mars",1:"Facts"},errors="raise")
mars_facts.set_index("Mars",inplace=True)

# Convert mars facts table to html
facts_table=mars_facts.to_html()

# Replace \n and white space to make html easier to read
facts_table.replace('\n','')

################## Mars Hemispheres ################## 

# Visit the following URL
mars_hem_url = 'https://marshemispheres.com/'
browser.visit(mars_hem_url)

# Delays URL from opening for one second
time.sleep(1)

# Scrape page into Soup
html = browser.html
soup = bs(html, 'html.parser')

# Find hemisphere images by class
div_list = soup.body.find_all("div", class_="description")

# Create list to store html
sites = []

# Loop through div list
for div in div_list:
    
    # Scrape website for href to get location for the full image
    site = div.find("a", class_="product-item")["href"]
    
    # Append sites href to list
    sites.append(site)

# Create list to store as dictionary
hemisphere_image_urls = []

# Loop through each site href
for site in sites:
    try:
        
        # Visit specific html
        url = mars_hem_url + site
        browser.visit(url)
        html = Browser.html
        
        # Convert html to soup
        soup = bs(html, "html.parser")
        
        # Find image with specified class and access source of image
        img_url_ending = soup.body.find("img", class_="wide-image")["src"]
        
        # Add url to the image source to get full url
        img_url = mars_hem_url + img_url_ending
        
        # Obtain title on page - remove "Enhanced" to get title
        title = soup.body.find("h2", class_="title").text.strip()[:-9]
        
        # Append dictionary for title and image url's to list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    except Exception as e:
        print(e)

# Close the browser after scraping
browser.quit()

################## Create dictionary for scraped data ##################

mars_info = {
    "NewsTitle": news_title,
    "NewsParagraph": news_p,
    "FeaturedImage": featured_image_url,
    "MarsFactsTable": mars_facts,
    "HemisphereImages": hemisphere_image_urls
}

# Return results
return mars_info