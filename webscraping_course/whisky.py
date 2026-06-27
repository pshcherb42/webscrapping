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
