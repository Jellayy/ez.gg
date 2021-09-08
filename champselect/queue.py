import asyncio
from asyncio import sleep

import willump

from champselect import functions


async def main():
    client = await willump.start()


    await functions.create_lobby(client)
    await functions.select_roles(client)
    await functions.queue_type(client)
    if await functions.can_start(client):
        await functions.start_queue(client)
        while not await functions.queue_pop(client):
            print("queue has not popped yet")
            await sleep(5)
        await functions.accept_queue(client)
        while not await functions.is_champ_select(client):
            print("not quite champ select")
            await sleep(1)
        print('maid it to champ select')
        await sleep(5)
        await functions.lobby(client)
        await functions.pick_champ(client)
        await functions.lock_in(client)

    elif not await functions.can_start(client):
        print("Cannot start queue, exiting program")




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