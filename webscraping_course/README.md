So here is everything that I've done so far

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
'''
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from bs4 import BeautifulSoup
import time

baseurl = 'https://www.thewhiskyexchange.com'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="chrome")  # Launch Chrome instead of Chromium

    # configuramos variables de ususario reales
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="en-GB", # because the site is uk based
        viewport={"width": 1280, "height": 720},
        extra_http_headers={
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referrer": "https://www.google.com/",
        }
    )
    page = context.new_page() # context instead of browser

    # aplicamos el sigilo antes de abrir la pagina web
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

    # Step 1: Visit the homepage first
    page.goto("https://www.thewhiskyexchange.com")
    time.sleep(5)  # Wait for a few seconds to mimic human behavior
    response = page.goto(
        "https://www.thewhiskyexchange.com/c/35/japanese-whisky"
        #wait_until="networkidle"
    )
    time.sleep(5)  # Wait for a few seconds to mimic human behavior

    # check server response
    print("Status:", response.status)   # e.g. 200
    print("URL:", page.url)             
    #page.wait_for_selector("li.product-grid__item", timeout=15000)
    html = page.content()

    soup = BeautifulSoup(html, "lxml")

    products = soup.select("li.product-grid__item")

    for item in products:
        for link in item.find_all('a', href=True):
            print(link['href'])

    browser.close()
'''
# timeout error
# on the page there are scripts that are sending data nonstop in loop. I am going to eliminate
# wait_until='networkidle' so playwright is not going to wait until silence .
# browser vanilla exposes javascript navigator.webdriver = true
# I am going to install stealth plugin that eliminates these digital prints.
# this didnt fully work

# Advansed Approach
# Step 1: I am going to try to visit the homepage first, then navigate
# Step 2: Launch with a real chrome instead of chromium
# Step 3: add delays
# Step 4: make the browser look more human 

# Nothing helps the site is protected by Cloudflare bot detection.

# I am going to try to enter manually and copy the cookies.
# cf_clearance: NjLCTLBAB1wrUDLFyu1c8dSzXPPO3vdBhEoUV94pg54-1782581534-1.2.1.1-pc31VCmvZfEby8klRop_haa2iYZeAa7hV.A9j8NpZe4jLV39a7mXmQ7HSkh6y13bgpbrpgOnAQe2Z8P5s84L5JiafOGNWwg2fi3YPGJQte4wbEFyvJsOYGYHK.wOReJrA.9mlHLGhl3x7zC9yUtg5Xz5S6fd1b2GAZ5JKwpPE9wipSzuKF_0mDBGmC1CdhaK_tr_.EYeYAt_JpwkDx75nttihG0NowSFa1WlIcVGUAuP1FMsKIbVfm5yCk2OsHugZVAMPYz3c0c.Kh9j.V8PFOgM6USRez6U4qlSjkpKMfw129K1062zrzD35Juw1tLa0xQNiBZc1_I6MoHwsdo4B2upTTt9FLBS_SJcfDQeJwDqHX3MMcTzOf1_cMPS4m50dxKzJ6kaa.u4AQTrSMYzCGlke7OBsB6tunO_JSsFFPLR7CABbumS1Qe.ADBtFxi5
#__cf_bm: Byv5Px8EzZpekJRxp.1JY2q9MaPk9QOo9YTatPKDS2I-1782581534.2620761-1.0.1.1-IOY496kPUVgD9ihzsaDdE1JePh0ES8OzLiwJaG.A7sHENvCv6O74wG.tYF.eGm5g_XKTpqxs8OdSSCnxVSGVrgZ929pVwdPC_pjM_3MKujRxxTiacrclwwIzRWg8JExW
# my user_agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.google.com/",
}

cookies = {
    "cf_clearance": "IcGMXkgb4riGLDsqCKCBGe2TiDbN2Fwlb4a3u0_Aij4-1782582387-1.2.1.1-Yk3RHhT6wkB6gVcAI0LnZja4AacMHv8ND4CWO4t1AIIsl_qBBYujysLKU39e66sGcIKOvNAUTLZXmFzYuaP0HlU6hq4dbSmMfLGeT0MO40AtLqXHWwPsvw6VTc8rjUI02Sd_FgI.8z8UiJ5j4hCZcFj1EtT9ZCWO.af0mIXbOIcUHA5fm7dkd0FX9YAu0Obymq_RyK95pTy_qmlipDnKHeXlE7xPBnhEGjfjkrB4XkizAXwhYaZ8pJ.a5Mw.lU4SX9GYZENKBoq01fA32Mpupeg4f1hrNG1nzMWbUaCZVUM127rHzewn14rgXw3OwdDVat2wH.hd2JiqwI6oEucHR2f0FVg9VKiO8Ec5HrZ7D8ije861zgyQ0UTnvhEgVPthwwo6OH7mngR2SRsCz0M6.4_qLisGXHAA0JJvqwiFvQNYOFABoQYRmEFyqqGp9XEW",
    "__cf_bm": "A_QpSpKHg5wHQnr4ILhRSB4uZiTbGJdwKZ53oFeHSbA-1782582387.597306-1.0.1.1-nQTOwgVEjpiu1qSHuAeu_uqquPBFtZNfZZE5e_naZrzOiQusfTpKWXOapR5nMCcQX7qiMm8N703ZuXHFup.aLZ7Jco3rsfOVu_uI45V3jgNOjK2lnDba5GEvBAuBEGc8",
}

url = "https://www.thewhiskyexchange.com/c/35/japanese-whisky"

response = requests.get(url, headers=headers, cookies=cookies)
print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "lxml")
products = soup.select("li.product-grid__item")

for item in products:
    for link in item.find_all('a', href=True):
        print(link['href'])

'''
(myenv) ggg@GiacominoGuardianos-MacBook-Air webscraping_course % python3 whisky.py   
Status: 200
/p/29388/hibiki-harmony
/p/2940/yamazaki-12-year-old
/p/36362/suntory-toki
/p/23771/hakushu-distillers-reserve
/p/70564/chichibu-the-peated-2022
/p/80949/chichibu-red-wine-cask-2023
/p/23772/yamazaki-distillers-reserve
/p/72178/kanosuke-single-malt
/p/23928/nikka-coffey-grain-whisky
/p/44246/suntory-toki-black
/p/81244/kanosuke-hioki-pot-still
/p/73019/fuji-single-blended-whisky
/p/47669/ichiros-malt-double-distilleries-465
/p/63405/the-house-of-suntory-trilogy-pack-3x20cl
/p/82003/akashi-blended-sherry-cask-finish
/p/68390/togouchi-single-malt
/p/71847/yamazaki-12-year-old-100th-anniversary
/p/81705/yamazaki-18-year-old-gift-box
/p/85890/chichibu-distillery-ii
/p/32762/miyagikyo-single-malt
/p/32761/yoichi-single-malt
/p/81835/kanosuke-2020-1st-fill-bourbon-cask-20496-exclusive-to-the-whisky-exchange
/p/72434/fuji-single-malt-whisky
/p/72433/fuji-single-grain-whiskey
'''
# this approach worked. I will be satisfied for now. It wont work for automated search, just for casual scrapping, but for now and for this project I dont need more. 
# note: these credentials expire in minutes.
