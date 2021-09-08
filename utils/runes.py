import willump
import asyncio
import requests


CLIENT_VERSION = "11.17.1"


async def get_current_page_id(client):
    current_page = await client.request('get', '/lol-perks/v1/currentpage')
    page_json = await current_page.json()
    return page_json


async def get_rune_data():
    r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{CLIENT_VERSION}/data/en_US/runesReforged.json')
    print(r.json())


async def main():
    client = await willump.start()
    await get_rune_data()
    print(await get_current_page_id(client))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
