import willump
import asyncio
import utils.opgg as opgg
import json


CLIENT_VERSION = "11.17.1"


async def get_current_page_id(client):
    current_page = await client.request('get', '/lol-perks/v1/currentpage')
    page_json = await current_page.json()
    return page_json['id']


async def set_rune_page(client, champion):
    page_id = await get_current_page_id(client)
    runes = await opgg.get_rune_page(champion)
    print(runes)
    selectedPerkIds = [runes[0], runes[1], runes[2], runes[3], runes[4], runes[5], runes[6], runes[7], runes[8]]
    primaryStyleId = runes[9]
    subStyleId = runes[10]
    setRunePage = await client.request('put', "/lol-perks/v1/pages/" + str(page_id),
                                           data={'autoModifiedSelections': [], 'current': True, 'id': int(page_id),
                                                 'isActive': False, 'isDeletable': True, 'isEditable': True,
                                                 'isValid': True, 'lastModified': 1589016704794, 'name': f"EZ.GG: {champion}",
                                                 'order': 1, 'primaryStyleId': primaryStyleId,
                                                 'selectedPerkIds': selectedPerkIds, 'subStyleId': subStyleId})
    print(setRunePage)


async def main():
    client = await willump.start()
    await set_rune_page(client, "annie")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
