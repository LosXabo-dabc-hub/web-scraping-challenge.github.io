from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
import numpy as np

def init_browser():
    # @NOTE: Path to my chromedriver
    executable_path = {"executable_path": "c:\\Users\\mwals\\Desktop\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    ###NASA MARS NEWS
    # Visit the following URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get latest NASA Mars news title and teaser
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_="article_teaser_body").text


    ###JPL Mars Space Images - FEATURED IMAGE
    # Visit the following URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl = "https://www.jpl.nasa.gov"
    browser.visit(url)
    time.sleep(3)

    # xpath for image
    xpath = '//*[@id="full_image"]'

    # Use splinter to Click the image to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(3)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    img_desc = soup.find('div', class_="fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open")
    image = img_desc.find('img')
    image['src']
    featured_image_url = jpl + image['src']

    #### MARS WEATHER
    # Visit the following URL
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(3)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    tweet = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    z=0
    for x in tweet:
        if tweet[z].text.split(' ', 1)[0] == 'InSight':
            mars_weather = tweet[z].text #_Mars weather
            break
        else:
            z+=1
    # Scrapes for Mars weather

    ### MARS FACTS
    # Visit the following URL
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Fact', 'Value']
    html_table = df.to_html()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table":html_table
    }

    time.sleep(7)
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
