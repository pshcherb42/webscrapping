
# Project Title

A brief description of what this project does and who it's for

So here is everything that I've done so far




    import cloudscraper
    from bs4 import BeautifulSoup

    baseurl = 'https://www.thewhiskyexchange.com'

    scraper = cloudscraper.create_scraper()

    r = scraper.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky')

    print(r.status_code)
    print(r.url)
    print(r.text[:500])

    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('li', class_='product-grid__item')

    productlinks = []

    for item in productlist:
        for link in item.find_all('a', href=True): then inside it we ar elooking for an a
            print(link['href'])
        


url detects that request is from an authomated script and blocks the connection silently
 las tarjetas de producto no usan la clase genrica div item, sino una clase mas especifica llamada li.product-grid_item
 la pagina usa Cloudflare avanzado. bloque la libreria requests al instante. voy a cambiarla por curl_cffi
 lets check what I actually receive from the server
Cloudflare sigue interceptando el script
voy a usar cloudscrapper. 
 I have two options: Playwright or JSON endpoints
I will try with JSON first as it seems easier to me now.
no JSON

# using Playwright


    from playwright.sync_api import sync_playwright
    from playwright_stealth import Stealth
    from bs4 import BeautifulSoup
    import time

    baseurl = 'https://www.thewhiskyexchange.com'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")  Launch Chrome instead of Chromium

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-GB", because the site is uk based
            viewport={"width": 1280, "height": 720},
            extra_http_headers={
                "Accept-Language": "en-GB,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referrer": "https://www.google.com/",
            }
        )
        page = context.new_page() context instead of browser

        stealth = Stealth()
        stealth.apply_stealth_sync(page)

        page.goto("https://www.thewhiskyexchange.com")
        time.sleep(5)  Wait for a few seconds to mimic human behavior
        response = page.goto(
            "https://www.thewhiskyexchange.com/c/35/japanese-whisky"
            #wait_until="networkidle"
        )
        time.sleep(5)  Wait for a few seconds to mimic human behavior

        print("Status:", response.status)   e.g. 200
        print("URL:", page.url)             
        #page.wait_for_selector("li.product-grid__item", timeout=15000)
        html = page.content()

        soup = BeautifulSoup(html, "lxml")

        products = soup.select("li.product-grid__item")

        for item in products:
            for link in item.find_all('a', href=True):
                print(link['href'])

        browser.close()

timeout error
on the page there are scripts that are sending data nonstop in loop. I am going to eliminate
wait_until='networkidle' so playwright is not going to wait until silence .
browser vanilla exposes javascript navigator.webdriver = true
I am going to install stealth plugin that eliminates these digital prints.
this didnt fully work

# Advansed Approach
Step 1: I am going to try to visit the homepage first, then navigate

Step 2: Launch with a real chrome instead of chromium

Step 3: add delays

Step 4: make the browser look more human 

Nothing helps the site is protected by Cloudflare bot detection.

# Manual enter
I am going to try to enter manually and copy the cookies.

cf_clearance: 

__cf_bm: 

my user_agent: 


    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": " ",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    cookies = {
        "cf_clearance": " ",
        "__cf_bm": " ",
    }

    url = "https://www.thewhiskyexchange.com/c/35/japanese-whisky"

    response = requests.get(url, headers=headers, cookies=cookies)
    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")
    products = soup.select("li.product-grid__item")

    for item in products:
        for link in item.find_all('a', href=True):
            print(link['href'])



this approach worked. I will be satisfied for now. It wont work 
for automated search, just for casual scrapping, but for now and for this project I dont need more. 
note: these credentials expire in minutes.

# Parse each page

Adding loop through 6 pages
Testing to retrieve information from one page only.
name, rating, reviews, price.

# Setting the database to save the results


