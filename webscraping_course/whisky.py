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
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
import time

baseurl = 'https://www.thewhiskyexchange.com'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # configuramos variables de ususario reales
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="es-ES",
        viewport={"width": 1280, "heght": 720}
    )
    page = context.new_page() # context instead of browser

    # aplicamos el sigilo antes de abrir la pagina web
    stealth_sync(page)

    page.goto(
        "https://www.thewhiskyexchange.com/c/35/japanese-whisky"
        #wait_until="networkidle"
    )

    #page.wait_for_selector("li.product-grid__item", timeout=15000)
    html = page.content()

    soup = BeautifulSoup(html, "lxml")

    products = soup.select("li.product-grid__item")

    for item in products:
        for link in item.find_all('a', href=True):
            print(link['href'])

    browser.close()

# timeout error
# on the page there are scripts that are sending data nonstop in loop. I am going to eliminate
# wait_until='networkidle' so playwright is not going to wait until silence .
# browser vanilla exposes javascript navigator.webdriver = true
# I am going to install stealth plugin that eliminates these digital prints.
