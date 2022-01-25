import asyncio
from asyncio import sleep
import utils.runes as runes
from champselect import state_engine



from champselect import functions


async def main():

    # await state_engine.create_lobby()
    # await state_engine.start_queue()
    # await state_engine.auto_queue_accept()
    await state_engine.instalock_champ()



    # client = await willump.start()
    #
    # #create a lobby
    # await functions.create_lobby(client)
    # #select roles
    # await functions.select_roles(client)
    # #get lobby type
    # await functions.queue_type(client)
    # if await functions.can_start(client) and await functions.is_lobby_leader(client):
    #     await functions.start_queue(client)
    # #     while not await functions.queue_pop(client):
    # #         print("queue has not popped yet")
    # #         await sleep(5)
    # #     await functions.accept_queue(client)
    # #     while not await functions.is_champ_select(client):
    # #         print("not quite champ select")
    # #         await sleep(1)
    # #     print('made it to champ select')
    # #     await functions.lobby(client)
    # #     await functions.pick_champ(client, await functions.lobby(client))
    # #     await functions.lock_in(client, await functions.lobby(client))
    # #     await runes.set_rune_page(client, "annie")
    # #
    # elif not await functions.can_start(client):
    #     print("Cannot start queue, exiting program")






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