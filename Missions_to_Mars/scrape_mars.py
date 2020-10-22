from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    browser = init_browser()

    mars_dict = {}

    # This will run the first function
    news_title, news_p = scrape_news()

    # We need to run the others functions

    mars_dict['title'] = news_title
    mars_dict['paragraph'] = news_p
    mars_dict['main_image'] = scrape_image()
    mars_dict['mars_facts'] = scrape_table()
    mars_dict['mars_hemispheres'] = scrape_hemi()


    browser.quit()

    return mars_dict


# Function to scrape Mars title and paragraph
def scrape_news():

    browser = init_browser()
    url ="https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    try:
        side_element = news_soup.select_one("ul.item_list li.slide")
        news_title = side_element.find("div", class_="content_title").get_text()
        news_p = side_element.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    browser.quit()

    return news_title, news_p

# function to scrape the main image from JPL Mars Space 

def scrape_image():

    browser = init_browser()
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(1)
    browser.links.find_by_partial_text('FULL').click()
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.select_one('figure.lede a img').get("src")
    core_url = "https://www.jpl.nasa.gov"
    final_image = core_url + image

    browser.quit()

    return final_image


def scrape_table():

    browser = init_browser()
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    mars_table = pd.read_html(url3)
    mars_table = mars_table[0]
    mars_table.columns=["Description", "Mars"]
    mars_table.set_index("Description", inplace = True)
    table_html = mars_table.to_html()

    browser.quit()

    return table_html

def scrape_hemi():

    browser = init_browser()
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html_hemisphere = browser.html
    soup_hemisphere = bs(html_hemisphere,'html.parser')
    hemispheres = soup_hemisphere.find_all('div', class_='item')

    all_hemis_list = []
    main_url = "https://astrogeology.usgs.gov"
    for x in hemispheres:
    #get title
        title = x.find('h3').text
    
    #Store a link that leads to the full image
        temp_img = x.find('a', class_ = 'itemLink product-item')['href']
    
        browser.visit(main_url + temp_img)
    
        temp_img_html = browser.html
        soup_each_hemis = bs(temp_img_html, "html.parser")
    
    #scrap full image source
        full_img_url = main_url + soup_each_hemis.find('img', class_="wide-image")['src']
    
    #append to the list
        all_hemis_list.append({"title": title, "img_url": full_img_url})

    browser.quit()

    return all_hemis_list
