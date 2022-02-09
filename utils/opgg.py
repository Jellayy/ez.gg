import requests
import bs4
import asyncio


# Uses BS4 to scrape OP.GG champion pages for recommended rune IDs
async def get_rune_page(champion):
    champion = champion.lower()
    # Faking a user agent so that op.gg doesn't give 403 Forbidden on html requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(f'https://na.op.gg/champions/{champion}/', headers=headers)
    r_soup = bs4.BeautifulSoup(r.text, 'html.parser')

    runes = []
    # Keystone
    data = r_soup.find_all("div", {"class": "css-1w13bvn e495vw30"}, limit=1)
    runes.append(str(data).split("img")[1].split("/")[6].split(".")[0])

    # Primary and Secondary Tree Perks
    data = r_soup.find_all("div", {"class": "css-l5ga7x e495vw30"}, limit=5)
    for entry in data:
        runes.append(str(entry).split("img")[1].split("/")[6].split(".")[0])

    # Flex Perk Tree
    data = r_soup.find_all("img", {"class": "css-atqrr"}, limit=3)
    for entry in data:
        runes.append(str(entry).split("/")[6].split(".")[0])

    # Keystone and Secondary Tree
    data = r_soup.find_all("div", {"class": "item item_mark"}, limit=2)
    data = str(data).split("img")
    data.pop(0)
    for entry in data:
        runes.append(entry.split("/")[6].split(".")[0])

    return runes


# Uses BS4 to scrape OP.GG champion pages for recommended summoner spell IDs
async def get_sum_spells(champion):
    champion = champion.lower()
    # Faking a user agent so that op.gg doesn't give 403 Forbidden on html requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(f'https://na.op.gg/champions/{champion}/', headers=headers)
    r_soup = bs4.BeautifulSoup(r.text, 'html.parser')

    spells = []
    data = r_soup.find_all("ul", {"class": "css-wc914 e1jyy41s0"}, limit=1)
    data = str(data).split("img")
    data.pop(0)
    for entry in data:
        spells.append(entry.split("/")[6].split(".")[0])

    return spells

########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    print(await get_rune_page("annie"))
    print(await get_sum_spells("annie"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
