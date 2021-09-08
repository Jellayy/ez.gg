import requests
import bs4
import asyncio


async def get_rune_page(champion):
    champion = champion.lower()
    r = requests.get(f'https://na.op.gg/champion/{champion}/')
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


async def main():
    print(await get_rune_page("annie"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())