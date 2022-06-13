# Import Dependancies
import pandas as pd
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def scrape_mars_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)
    browser.is_element_present_by_css("div.list_text", wait_time=4)

    html = browser.html
    soup = bs(html, "html.parser")

    try:
        element = soup.select_one("div.list_text")
        news_title = element.find("div", class_="content_title").get_text()
        news_p = element.find("div", class_="article_teaser_body").get_text()
    except:
        return None, None
    return news_title, news_p

def scrape_mars_space_featured_imgs(browser):
    url = "https://spaceimages-mars.com" 
    browser.visit(url)

    browser.find_by_tag("button")[1].click()

    html = browser.html
    soup = bs(html, "html.parser")

    try:
        img_url_path = soup.find("img", class_="fancybox-image").get("src")
    except:
        return None
    return f"{url}/{img_url_path}"

def scrape_mars_facts():
    url = "https://galaxyfacts-mars.com"
    
    tables=pd.read_html(url)
    mars_facts=tables[1]
    
    mars_facts.columns=["Description", "Values"]

    return mars_facts.to_html()

def scrape_mars_hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    div_list = soup.body.find_all("div", class_="description")

    sites = []

    for div in div_list:
        site = div.find("a", class_="product-item")["href"]   
        sites.append(site)

        hemisphere_image_urls = []

    for site in sites:
        try:
            url = url + site
            browser.visit(url)
            html = browser.html
        
            soup = bs(html, "html.parser")
        
            img_url_ending = soup.find("img", class_="wide-image")["src"]
        
            img_url = mars_hem_url + img_url_ending
        
            title = soup.find("h2", class_="title").text.strip()[:-9]
        
            hemisphere_image_urls.append({"title": title, "img_url" :img_url})
        except:
            return None
    return hemisphere_image_urls

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = scrape_mars_news(browser)
    featured_imgs = scrape_mars_space_featured_imgs(browser)
    hemispheres = scrape_mars_hemispheres(browser)
    mars_facts = scrape_mars_facts()
    browser.quit()
    return {
        "news_title": news_title,
        "news_paragraph": news_p, 
        "featured_images": featured_imgs,
        "hemispheres": hemispheres,
        "facts": mars_facts
    }

if __name__ == "__main__":
    print(scrape())