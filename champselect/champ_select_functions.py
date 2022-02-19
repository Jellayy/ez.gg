import asyncio
from asyncio import sleep
import willump
import champselect.preferences as preferences


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


async def intent_champ(client, actorcellid, championid):
    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}'
    pick = await client.request('PATCH', call, data={
        "championId": championid,
        "type": "pick"
    })
    if pick.status == 200:
        print(pick.status)









async def pick_champ():
    #open willump connection
    client = await willump.start()

    response = await client.request('')


    #close willump connection
    await willump.Willump.close(client)