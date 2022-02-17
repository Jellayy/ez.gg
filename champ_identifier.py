import asyncio
import willump
import requests
import utils.runes as runes
import utils.ddragon as ddragon


# TODO: Rate limiting champ select check and champion pulling to 1sec reeeealy helped cpu usage a lot(0% pretty much), could probably go even further with a passive mode that only checks for champ select every 30sec-1min or so that can permanently run in the background without worry
async def wait_for_champ_select():
    client = await willump.start()
    while True:
        check_for_champ_select = await (await client.request('get', '/lol-champ-select/v1/session')).json()
        if list(check_for_champ_select.keys())[0] != 'errorCode':
            await willump.Willump.close(client)
            return True
        await asyncio.sleep(1)


async def get_champion_pick():
    print('1')
    client = await willump.start()
    print('2')
    while True:
        champion_check = await (await client.request('get', '/lol-champ-select/v1/current-champion')).json()
        if str(champion_check) != "0":
            champion = ddragon.champ_id_to_name(str(champion_check))
            await willump.Willump.close(client)
            return champion
        await asyncio.sleep(1)


async def main():

    await wait_for_champ_select()
    print("ENTERED CHAMP SELECT")
    pick = await get_champion_pick()
    print(f"PICKED {pick.upper()}")
    client = await willump.start()
    await runes.set_rune_page(pick)
    await willump.Willump.close(client)
    print("RUNE PAGE SET")
    return f'{pick} runes complete!'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
