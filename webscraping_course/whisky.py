import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.thewhiskyexchange.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.google.com/",
}

cookies = {
    "cf_clearance": "zM.opTH1IRkQAVzxPZDN73uTn6vX.dRWF0EToyqBXdA-1782588361-1.2.1.1-BjNIBD_ihhXiGfK05GTG4CLtX4Z5vV4CAhN8MfB.KVrEmu2nKmHKk_ZYYM4.m_0id57XSdaCyVCXkmFzuiQH4pYSec1KA0a0kNnt49t3fEuBYAzzOfqJ2OjOIrKDKxPDnv24VmTtJdWkAf8XNG5QG6y9QAdQUNDrjT9cLBqBt0EFXA_PKofMdAEXGYUViYn8Fq6jJ8VSkV0659kKjN7o1b_e_mDdcx3aQ48mM..r0Lw1L51_cmlFQ6jQX6tIiKUMzjpConuy4BaObCO7H5tlBS_cOT4nTNiA1wdiueUi76rS2X6cnVX0uSp0GuYZ2rSqpyoVRU7UjTtp4Auesr.L5qih6PdWJsGPl7ZBOFncp3uTJ7h8nHD5JdWI5aR0_S8DJhQ9jS3FSbTd8xrYWgSbL8qusDHOoQwfLBqnuj_0Z3Epqda7n7LL9UQ7ybxS5.LP",
    "__cf_bm": ".IFRBwVCGvhUZX75IBJILUQFLaoVmXOD8agQeY_2tbI-1782588361.8566532-1.0.1.1-2iRemig9PO4O06fWrQReHnxAr5wEn10vpqSTnzg08pja65G3KoMxwUmQuzN43w.k.qTmcGjl0R6GxXQlBCaRCnmdojl3OVUgzy2JsiiJ_WLDIVIWvXwyVZ9NloohRQ8F",
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

# testlink = 'https://www.thewhiskyexchange.com/p/62322/matsui-sakura-kurayoshi-distillery'

whiskylist = []
for link in productlinks:
    r = requests.get(link, headers=headers, cookies=cookies)

    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', class_='product-main__name').text.strip()
    price = soup.find('p', class_='product-action__price').text.strip()
    description = soup.find('div', class_='product-main__description').text.strip()
    try:
        stock = soup.find('p', class_='product-action__stock product-action__stock--instock').text.strip()
    except:
        stock = "Stock information not available"

    try:
        rating = soup.find('div', class_='review-overview__rating star-rating star-rating--30').text.strip()
    except:
        rating = "No rating available"

    whisky = {
        'name': name,
        'rating': rating,
        'price': price,
        'stock': stock,
        'description': description
    }

    whiskylist.append(whisky)
    print('Saving whisky: ', whisky['name'])

df = pd.DataFrame(whiskylist)
print(df.head(15))
