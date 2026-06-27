import requests
from bs4 import BeautifulSoup

baseurl = "https://www.thewhiskyexchange.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.google.com/",
}

cookies = {
    "cf_clearance": "9hH8DL4VlmwW7wDj_9vptOqzGOUhrNcDCGyS7QX_Ieo-1782585430-1.2.1.1-SuKopPPLbOdK5B7i9AgqYMiRDABdZCzRjSmf7oKOb15w1cn2esiw9CM9YZ83ehP5Fis4cCmB6wlre5EEzC_7EYWAhA7hVFmNRSzgXloW0LOeTNL3C7vWhjkJc5fQ4X5iZTMMxbmFA9ESbHPkrGi0ONNCs9VUL.yHUoiH8LMflfg0tW3fy52zUHeJ3NAoIQBsdqoskF9Bk8zLfFm0zmuoJbF2ixa9L0n7HXd9SxsfYp5w8Gg3yZEigYHC_0G5_fRPQkz6n8XzplT5HHeySbu6dGJxfk5sqZx3Jl7Vzyis_jyFIu_MQKSUuY2MZ0hnuYc1pBPboaqS4c9QCX6ZO4wSBLqJjgjkVkcbX1shGlWKTM0XCXq14RcsHj1leKu8NeWK_BMtMuxnJOLQlsXr4hGSLhXlPzZIwrgAxR864iaR070tKLLaLjfETFHQzjzjOW75",
    "__cf_bm": "iGwHvERs.yAUqbdolt4MStXRMWIHOqVrxUlIO0sNxAA-1782585430.0401814-1.0.1.1-Gfy2Eoc17mRl7FncB0inAmQP4PzVUx1ZVzCcgafmuMlfYlw7qxFtR61cmCAs.GBBtknw2gbP4CgaQKf3ieIG.x1w.9gL.btxQnq.KEzs.z6VL_Arj7c2jkMs_k359UGa",
}

productlinks = []

for x in range(1, 6):
    url = f"https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}"

    response = requests.get(url, headers=headers, cookies=cookies)
    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")
    products = soup.select("li.product-grid__item")
    
    for item in products:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])

print(len(productlinks))

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

