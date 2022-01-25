import requests
import bs4
import asyncio


# Uses BS4 to scrape OP.GG champion pages for recommended rune IDs
async def get_rune_page(champion):
    champion = champion.lower()
    # Faking a user agent so that op.gg doesn't give 403 Forbidden on html requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(f'https://na.op.gg/champion/{champion}/', headers=headers)
    r_soup = bs4.BeautifulSoup(r.text, 'html.parser')

    runes = []
    data = r_soup.find_all("div", {"class": "perk-page__item--active"}, limit=6)
    for element in data:
        str_element = str(element)
        lines = str_element.splitlines()
        for line in lines:
            if line.__contains__("img"):
                line_split = line.split("/")[6]
                line_split = line_split.split(".")[0]
                runes.append(int(line_split))

    data = r_soup.find_all("img", {"class": "active"}, limit=3)
    for img in data:
        str_img = str(img)
        str_split = str_img.split("/")[6]
        str_split = str_split.split(".")[0]
        runes.append(int(str_split))

    data = r_soup.find_all("img", {"class": "perk-page__image"}, limit=2)
    for img in data:
        str_img = str(img)
        str_split = str_img.split("/")[6]
        str_split = str_split.split(".")[0]
        runes.append(int(str_split))

    return runes


########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    print(await get_rune_page("akshan"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
