from selenium import webdriver
from selenium.webdriver.support.ui import Select
import bs4
from time import sleep
import re
import operator
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

def save_to_file(content, out_path='./scrape.html'):
    with open(out_path, 'w') as f:
        f.write(content)

def get_page_source(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    browser.implicitly_wait(1)

    # below code is hardcoded to search for "vinterjakke", change send_keys("...") for
    # to change search
    search_field = browser.find_element_by_id('searchField')
    search_field.send_keys('vinterjakke')
    search_field.submit()

    # hardcoded to do a specific search
    # find "oprettet" and click "Seneste 24 timer" and select "København og omegn"
    created = "Oprettet"
    hours_24 = "Seneste 24 timer"
    copenhagen_area = "København og omegn"

    click_on_Newest = browser.find_element_by_xpath("//*[contains(text(), '" +  created + "')]")
    click_on_Newest.click()

    select_24_hours = browser.find_element_by_xpath("//*[contains(text(), '" + hours_24 + "')]")
    select_24_hours.click()

    select_copenhagen_area = browser.find_element_by_xpath("//*[contains(text(), '"+ copenhagen_area +"')]")
    select_copenhagen_area.click()

    browser.close()

    return browser.page_source


# USE THESE FIRST TIME RUNNING CODE, MIGHT THROW INVALID SESSION ID EXCEPTION
# IF YOU GET THAT EXCEPTION GG HAVE FUN NO FIX

# page_source = get_page_source('https://www.dba.dk')
# save_to_file(page_source)


with open('scrape.html') as file:
    soup = bs4.BeautifulSoup(file, 'html.parser')


product_cells = soup.find_all('tr', {'class': 'dbaListing'})

entries = []
for listing in product_cells:
    listingLinks = listing.find_all('a', {'class': 'listingLink'})
    description = listingLinks[1].text
    price = int(re.findall('\d+',listingLinks[2].text.replace(".", ""))[0])

    
    imagelinks = listing.find_all('div', {'class': 'thumbnail image-placeholder lazy'})
    imagelink = imagelinks[0]['data-original']

    detailslinks = listing.find_all('a', {'class': 'link-to-listing'})
    detaillink = detailslinks[0]['href']

    mytuple = (description,price,imagelink,detaillink)
    entries.append(mytuple)

entries.sort(key = operator.itemgetter(1))
print("List items sorted by price:\n")

for entry in entries:
    print(entry[1])
    print(entry[0])
    print(entry[2])
    print(entry[3])
    print("\n")