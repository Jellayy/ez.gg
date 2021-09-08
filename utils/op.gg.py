import requests
import bs4

aatrox = requests.get('https://na.op.gg/champion/aatrox/')
aatrox_soup = bs4.BeautifulSoup(aatrox.text, 'html.parser')

div = aatrox_soup.find_all("div", {"class": "perk-page__item--active"})

for thing in div:
    print(thing)
