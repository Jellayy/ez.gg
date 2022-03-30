import asyncio
import random
from asyncio import sleep
import willump
import champselect.preferences as preferences
import eel

import utils.ddragon


async def get_actor_id(client):
    call = '/lol-lobby-team-builder/champ-select/v1/session'
    lobby = await client.request('GET', call)
    if lobby.status == 200:
        data = await lobby.json()
        return data['localPlayerCellId']
    else:
        print(await lobby.json())


async def get_player_id(client):
    call = '/lol-lobby-team-builder/champ-select/v1/session'
    lobby = await client.request('GET', call)
    if lobby.status == 200:
        data = await lobby.json()
        user_id = 0
        for crap in data['actions']:
            for player in crap:
                if player['actorCellId'] == data['localPlayerCellId']:
                    user_id = player['id']
        return user_id
    else:
        print(await lobby.json())


async def get_pickable_champs(client):
    call = '/lol-champ-select/v1/pickable-champion-ids'
    pickable_champs = await client.request('GET', call)
    data = await pickable_champs.json()
    print(data)
    return data


async def get_disabled_champs(client):
    call = '/lol-champ-select/v1/disabled-champion-ids'
    disabled_champs = await client.request('GET', call)
    data = await disabled_champs.json()
    print(data)
    return data


async def get_current_champ(client):
    call = '/lol-champ-select/v1/current-champion'
    current_champ = await client.request('GET', call)
    data = await current_champ
    print(data)
    return data


async def get_champ_grid(client, id):
    call = f'/lol-champ-select/v1/grid-champions/{id}'
    champ_grid = await client.request('GET', call)
    data = await champ_grid.json()
    print(data)
    return data


async def intent_champ(client, actorcellid, championid):

    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}'
    pick = await client.request('PATCH', call, data={
        "championId": championid,
        "type": "pick"
    })
    if pick.status == 200:
        print(await pick.status)
        print("champion hovered")
    else:
        print(await pick.json(), "gays gays gays")


async def lock_in(client, actorcellid):
    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}/complete'
    locked = await client.request('POST', call)
    if locked.status == 200:
        print(await locked.json())
    else:
        print(await locked.json())


async def hover_ban(client, actorcellid, banid):
    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}'
    pick = await client.request('PATCH', call, data={
        "championId": banid,
        "type": "ban"
    })
    print(await pick.json())

# async def report_champ_select(wllp, report_ids):
#     for id in report_ids:
#         call = f'/lol-player-report-sender/v1/champ-select-reports/puuid/{id}/category/1'
#         report = await wllp.request('POST', call, data ={""})
#         print(await report.json())




async def hover_champ():
    try:
        if eel.get_lock_in_preference()():
            client = await willump.start()
            # print("Opened willump")
            player_id = await get_player_id(client)
            await intent_champ(client, player_id, int(preferences.champion))
            await willump.Willump.close(client)
    except:
        print("Something went wrong while hovering champ")
    # print("Closed willump")

async def ban_champ():
    try:
        if eel.get_auto_ban_preference()():
            client = await willump.start()
            print("Opened willump")
            print("Banning champ")
            actor_id = await get_actor_id(client)
            champ_to_ban_list = eel.get_ban_preferences()()
            print(champ_to_ban_list)
            champ_to_ban = utils.ddragon.champ_name_to_id(champ_to_ban_list[0])
            print(champ_to_ban)
            await hover_ban(client, actor_id, champ_to_ban)
            await lock_in(client, actor_id)
            await willump.Willump.close(client)
            print("Closed willump")
    except:
        print("Something went wrong while banning champ")

async def pick_champ():
    try:
        if eel.get_lock_in_preference()():
            client = await willump.start()
            # print("Opened willump")
            player_id = await get_player_id(client)
            pickable_champion_ids = await get_pickable_champs(client)
            preferred_champion = eel.get_pick_preferences()()
            champ_grid = await get_champ_grid(client, preferred_champion)
            champ_banned = champ_grid['selectionStatus']['pickedByOtherOrBanned']
            if champ_banned and preferences.dodge:
                print("champ is banned, not selecting anything")

            else:
                while champ_banned:
                    preferred_champion = int(random.choice(pickable_champion_ids))
                    champ_grid = await get_champ_grid(client, preferred_champion)
                    champ_banned = champ_grid['selectionStatus']['isBanned']

                await intent_champ(client, player_id, preferred_champion)
                await lock_in(client, player_id)
            await willump.Willump.close(client)
    except:
        print("Something went wrong picking champ")

    # print("Closed willump")
