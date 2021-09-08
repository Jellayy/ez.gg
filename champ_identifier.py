import asyncio
import willump
import requests
import utils.runes


def id_to_name(champ_id):
    r = requests.get('http://ddragon.leagueoflegends.com/cdn/11.17.1/data/en_US/champion.json').json()
    for champion in r['data'].items():
        if champion[1]['key'] == champ_id:
            return champion[1]['name']
    return "No Champion Selected"


async def main():
    client = await willump.start()
    while True:
        champ_select = await client.request('get', '/lol-champ-select/v1/session')
        champ_select_json = await champ_select.json()
        if list(champ_select_json.keys())[0] != 'errorCode':
            champion = await client.request('get', '/lol-champ-select/v1/current-champion')
            champion = await champion.json()
            print(champion)
            if str(champion) != "0":
                champion = id_to_name(str(champion))
                print(champion)
                await utils.runes.set_rune_page(client, champion)
                break
        else:
            print("Not in champ select")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
