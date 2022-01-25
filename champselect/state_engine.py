import asyncio
from asyncio import sleep
import utils.runes as runes

import willump

from champselect import functions


async def create_lobby():
    client = await willump.start()
    print("Opened willump")
    # create a lobby
    await functions.create_lobby(client)
    # select roles
    await functions.select_roles(client)
    await willump.Willump.close(client)
    print("Closed willump")


# queue accept logic, only works while in queue
async def auto_queue_accept():
    client = await willump.start()
    print("Opened willump")
    # while in queue, attempt to accept queue
    while await functions.is_in_queue(client):
        await functions.queue(client)
    await sleep(10)
    if functions.is_champ_select(client):
        print("I think we made it to champ select, moving on to next step")
    elif functions.is_in_queue(client):
        print("presumably someone did not accept queue, going back to waiting to accept queue")
        await auto_queue_accept()

    await willump.Willump.close(client)
    print("Closed willump")


# start queue
async def start_queue():
    client = await willump.start()
    print("Opened willump")
    await functions.start_queue(client)
    await willump.Willump.close(client)
    print("Closed willump")


# instalock champ, only works in blind pick
async def instalock_champ():
    client = await willump.start()
    print("Opened willump")
    await functions.pick_champ(client, await functions.lobby(client))
    await functions.lock_in(client, await functions.lobby(client))
    await willump.Willump.close(client)
    print("Closed willump")
