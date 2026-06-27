'''
import cloudscraper
from bs4 import BeautifulSoup

baseurl = 'https://www.thewhiskyexchange.com'

# scraper inteligente que hereda comportamientos de un navegador
scraper = cloudscraper.create_scraper()
# pition through the scraper 
r = scraper.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky')

# check server response
print(r.status_code)
print(r.url)
print(r.text[:500])

soup = BeautifulSoup(r.content, 'lxml')

# buscamos productos en las tarjetas actuales de la web
productlist = soup.find_all('li', class_='product-grid__item')

productlinks = []

for item in productlist:
    for link in item.find_all('a', href=True): # then inside it we ar elooking for an a
        print(link['href'])
'''
# url detects that request is from an authomated script and blocks the connection silently
# las tarjetas de producto no usan la clase genrica div item, sino una clase mas especifica llamada li.product-grid_item
# la pagina usa Cloudflare avanzado. bloque la libreria requests al instante. voy a cambiarla por curl_cffi
# lets check what I actually receive from the server
# Cloudflare sigue interceptando el script
# voy a usar cloudscrapper. 
# I have two options: Playwright or JSON endpoints
# I will try with JSON first as it seems easier to me now.
# no JSON
# using Playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.thewhiskyexchange.com/c/35/japanese-whisky",
        wait_until="networkidle"
    )

    html = page.content()

    soup = BeautifulSoup(html, "lxml")

    products = soup.select("li.product-grid__item")

    print(len(products))

    browser.close()