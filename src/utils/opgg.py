import asyncio
import logging

import bs4
import requests


# Uses BS4 to scrape OP.GG champion pages for recommended rune IDs
async def get_rune_page(champion):
    # Formatting champion name for url insertion
    champion = champion.lower()
    champion = champion.replace("'", "").replace(" ", "")

    # Faking a user agent so that op.gg doesn't give 403 Forbidden on html requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(f'https://na.op.gg/champions/{champion}/', headers=headers)
    r_soup = bs4.BeautifulSoup(r.text, 'html.parser')

    runes = []
    # Keystone
    data = r_soup.find_all("div", {"class": "css-r2m0dx e1o8f101"}, limit=1)
    runes.append(str(data).split("img")[1].split("/")[6].split(".")[0])

    # Primary and Secondary Tree Perks
    data = r_soup.find_all("div", {"class": "css-1rjzcri e1o8f101"}, limit=5)
    for entry in data:
        runes.append(str(entry).split("img")[1].split("/")[6].split(".")[0])

    # Flex Perk Tree
    data = r_soup.find_all("img", {"class": "css-anaetp e1gtrici1"}, limit=9)
    for entry in data:
        if 'grayscale' not in str(entry):
            runes.append(str(entry).split("/")[6].split(".")[0])

    # Keystone and Secondary Tree
    data = r_soup.find_all("div", {"class": "item item_mark"}, limit=2)
    data = str(data).split("img")
    data.pop(0)
    for entry in data:
        runes.append(entry.split("/")[6].split(".")[0])

    # Logging
    logging.debug(f"OP.GG Scraper: {champion} Page: {runes} Generated!")

    return runes


# Uses BS4 to scrape OP.GG champion pages for recommended summoner spell IDs
async def get_sum_spells(champion):
    # Formatting champion name for url insertion
    champion = champion.lower()
    champion = champion.replace("'", "").replace(" ", "")

    # Faking a user agent so that op.gg doesn't give 403 Forbidden on html requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(f'https://na.op.gg/champions/{champion}/', headers=headers)
    r_soup = bs4.BeautifulSoup(r.text, 'html.parser')

    spells = []
    data = r_soup.find_all("ul", {"class": "css-14r5yga esh6m080"}, limit=1)
    data = str(data).split("img")
    data.pop(0)
    for entry in data:
        spells.append(entry.split("/")[6].split(".")[0])

    # Logging
    logging.debug(f"OP.GG Scraper: {champion} Spells: {spells} Generated!")

    return spells


########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    # Should return ELEVEN perks
    # Example: ['8112', '8126', '8138', '8105', '8226', '8233', '5008', '5008', '5003', '8100', '8200']
    print(await get_rune_page("Cho'Gath"))

    # Should return TWO perks
    # Example: ['SummonerFlash', 'SummonerDot']
    print(await get_sum_spells("Cho'Gath"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
