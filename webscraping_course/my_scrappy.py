import cloudscraper
from bs4 import BeautifulSoup

baseurl="https://www.roastar.com"

scraper = cloudscraper.create_scraper()

r = scraper.get('https://www.roastar.com/custom-printed-coffee-bags')

print(r.status_code)
print(r.url)
print(r.text[:500])

soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('div', class_='group flex h-full w-full rounded-xl bg-white text-grind shadow-card flex-col')

productlinks = []

for x in range(1, 6):
    url = f"https://www.roastar.com/custom-printed-coffee-bags?page={x}"

    response = scraper.get(url)
    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")
    products = soup.find_all('div', class_='group flex h-full w-full rounded-xl bg-white text-grind shadow-card flex-col')
    
    for item in products:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])

# I was going to use the same method as before to load more pages but the url doesnt change
# this site is using infinite scroll, I am going to find API for it.