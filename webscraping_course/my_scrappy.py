import requests
import cloudscraper
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

baseurl="https://www.roastar.com"

scraper = cloudscraper.create_scraper()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

productlinks = []

for x in range(0, 6):   
    r = requests.get(f'https://www.roastar.com/custom-printed-coffee-bags?page={x}')

    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('div', class_='group flex h-full w-full rounded-xl bg-white text-grind shadow-card flex-col')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])

#testlink = 'https://www.roastar.com/get-quote#product=58'
# it's a Nuxt.js app (notice /_nuxt/ in the script tags). The HTML shell has no product data
coffeelist = []
with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pw_page = browser.new_page()
        for link in productlinks:
            try:
                pw_page.goto(link)
                pw_page.wait_for_selector('div.order-last.w-full.flex-none', timeout=10000)

                labels = pw_page.locator('div.py-2.text-sm.uppercase').all()
                values = pw_page.locator('div.order-last.w-full.flex-none').all()
                data = {
                    l.inner_text().strip(): v.inner_text().strip() 
                    for l, v in zip(labels, values)
                }
                coffee = {
                    'category': data.get('PRODUCT CATEGORY', ' '),
                    'quantity': data.get('QUANTITY', ' ')
                }
                coffeelist.append(coffee)
                print('Saving coffee: ', coffee['category'])
            except Exception as e:
                print(f"Error occurred while processing {link}: {e}")
        browser.close()

df = pd.DataFrame(coffeelist)
print(df.head(15))

# I was going to use the same method as before to load more pages but the url doesnt change
# this site is using infinite scroll, I am going to find API for it.
'''
import requests
import json

baseurl="https://www.roastar.com"

url="https://cd4xt0e4m9-dsn.algolia.net/1/indexes/*/queries"
params={
    "x-algolia-agent": "Algolia for JavaScript (5.49.2)",
    "x-algolia-api-key": "5d7599ca23af2dc34b4cde254ac7c8b0",
    "x-algolia-application-id": "CD4XT0E4M9",
}

productlinks = []

for x in range(0, 6):
'''
# it was a wrong approach but I learned something from it

# all works now but the error I gaced is that names of items are not very good differentiated
# i had to labels and pair them with labels
