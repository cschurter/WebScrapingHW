from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


### NASA Mars News
def scrape_news():
    browser = init_browser()
    news = {}

    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all('li',class_='slide')
    item = items[0]
    div = item.find('div',class_='content_title')
    link = div.find('a')
    title = link.text.strip()
    article = item.find('div', class_='article_teaser_body')
    date = item.find('div', class_ ="list_date").get_text()

    news["title"] = title
    news["article"] = article.text.strip()
    news["date"] = date

    # Close the browser after scraping
    browser.quit()

    return news

### Mars Weather
def scrape_weather():
    browser = init_browser()
    mars_weather = {}
    
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    ol = soup.find('ol',id='stream-items-id')
    weather_li = ol.find_all('li')
    latest_weather = weather_li[0]
    latest_weather_p = latest_weather.find('p')

    mars_weather["weather"] = latest_weather_p.text.strip()

    # Close the browser after scraping
    browser.quit()

    return mars_weather

#Mars Facts
def scrape_facts():
    table_data = {}
    mars_facts_url = 'http://space-facts.com/mars/'
    table = pd.read_html(mars_facts_url)

    mars_df = table[0]
    mars_df.columns = ['Mars Fact', 'Value']
    print(mars_df)
    table_html = mars_df.to_html(index=False, header=None, classes='table table-striped')
    table_data["dataframe"] = table_html
    
    return table_data

# JPL Mars Space Images - Featured Image
def scrape_image():
    browser = init_browser()
    mars_image = {}

    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    ul = soup.find('ul',class_='articles')
    images = ul.find_all('li',class_='slide')
    image = images[0]
    featured_image_a = image.find('a',class_='fancybox')
    featured_image_href = featured_image_a.get('data-fancybox-href')
    url_original = 'https://www.jpl.nasa.gov'
    featured_image = url_original + featured_image_href

    mars_image["image"] = featured_image

    # Close the browser after scraping
    browser.quit()

    return mars_image



