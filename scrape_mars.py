import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ### Mars News 

    # Set Mars News url for scraping
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    # scrape page into soup
    html=browser.html
    news_soup = bs(html, 'html.parser')

    # print the news
    news_article = news_soup.find('div', class_= 'list_text')
    news_title = news_article.find('div', class_ = "content_title").text
    news_p = news_article.find('div', class_ = "article_teaser_body").text





    ### JPL Mars Space Images

    url_jpl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg'

    browser.visit(url_jpl)
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Parse HTML with Beautiful Soup
    # html = browser.html
    # image_soup = bs(html, 'html.parser')

    # Scrape the URL
    # feat_img_url = image_soup.find('img', class_='fancybox-image').src
    # featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    # print(featured_image_url)



    ### Mars Facts

    url_mars_facts = "https://space-facts.com/mars/"

    # create Mars tables
    mars_tables = pd.read_html(url_mars_facts)
    # mars_tables

    # Pull the first table
    mars_df = mars_tables[0]
    # mars_df.head()

    # Move first row into header
    mars_df.columns = ["Descriptor", "Value"]
    # mars_df.head()


    # reset the index
    mars_df = mars_df.reset_index(drop=True)
    # mars_df.head()

    # bring table into html and clean
    mars_facts_html = mars_df.to_html()
    # mars_facts_html
    mars_facts_html.replace('\n', '')




    ### Mars Hemispheres

    # open browser with the hemispheres link
    url_usgs = "https://astrogeology.usgs.gov"
    url_hemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemis)

    # bring url into bs
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')

    # locate the hemispheres images in the html
    all_hemi = hemi_soup.find_all('div', class_='collapsible results')
    single_hemi = hemi_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    # loop through the html

    for hemi in single_hemi:
        # thread title
        hemisphere = hemi.find('div', class_="description")
        title = hemisphere.h3.text
        
        # image
        hemisphere_link = hemisphere.a["href"]
        browser.visit(url_usgs + hemisphere_link)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        
        # dictionary for title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)


    ### Store the Mars Data

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # close browser after scraping
    browser.quit()

    # return results
    return mars_data





if __name__ == '__main__':
    scrape()