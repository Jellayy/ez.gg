import asyncio

import willump

from champselect import functions


async def main():
    client = await willump.start()


    await functions.create_lobby(client)
    await functions.select_roles(client)




    # while True:
    #     champ_select = await client.request('get', '/lol-champ-select/v1/session')
    #     champ_select_json = await champ_select.json()
    #     if list(champ_select_json.keys())[0] != 'errorCode':
    #         champion = await client.request('get', '/lol-champ-select/v1/current-champion')
    #         print(id_to_name(str(await champion.json())))
    #     else:
    #         print("Not in champ select")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())