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
    return locked.status


async def hover_ban(client, actorcellid, banid):
    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}'
    pick = await client.request('PATCH', call, data={
        "championId": banid,
        "type": "ban"
    })
    return pick.status

# async def report_champ_select(wllp, report_ids):
#     for id in report_ids:
#         call = f'/lol-player-report-sender/v1/champ-select-reports/puuid/{id}/category/1'
#         report = await wllp.request('POST', call, data ={""})
#         print(await report.json())




async def hover_champ():
    try:
        client = await willump.start()
        # print("Opened willump")
        player_id = await get_player_id(client)
        await intent_champ(client, player_id, int(preferences.champion))
        await willump.Willump.close(client)
    except:
        print("Champ Select: Something went wrong while hovering champ")
    # print("Closed willump")


async def ban_champ(client):
    try:
        # Get champ select actor ID
        actor_id = await get_actor_id(client)

        # Obtain Ban Preferences from UI
        ban_preferences = eel.get_ban_preferences()()
        ban_list = []
        for champ in ban_preferences:
            if champ != '':
                ban_list.append({'name': champ,
                                 'id': int(utils.ddragon.champ_name_to_id(champ))})

        # Add none ban in case all bans are hovered
        ban_list.append({'name': 'None', 'id': -1})
        print(f"Champ Select: Ban List: {ban_list}")

        # Get Team Picks
        team_picks = []
        result = await client.request('GET', '/lol-champ-select/v1/session/')
        result_json = await result.json()
        for player in result_json['myTeam']:
            team_picks.append(player['championPickIntent'])
        print(f"Champ Select: Team Hovers: {team_picks}")

        # Check if you're banning a teammate pick
        confirmed_ban_list = []
        for ban in ban_list:
            if ban['id'] in team_picks:
                print(f"Champ Select: {ban['name']} hovered by teammate, skipping")
            else:
                confirmed_ban_list.append(ban)
        print(f"Champ Select: Confirmed Ban List: {confirmed_ban_list}")

        # Hover Ban
        result = await hover_ban(client, actor_id, confirmed_ban_list[0]['id'])
        if result == 204:
            print(f"Champ Select: Ban hovered (Status {result})")
        elif result == 500:
            print(f"Champ Select: Ban already hovered (Status {result})")
        else:
            print(f"ERROR: Champ Select: Ban hover failed with status {result}")

        # Lock In Ban
        result = await lock_in(client, actor_id)
        if result == 204:
            print(f"Champ Select: {confirmed_ban_list[0]['name']} Banned! (Status {result})")
        elif result == 500:
            print(f"Champ Select: Already banned (Status {result})")
        else:
            print(f"ERROR: Champ Select: Ban lock in failed with status {result}")
    except Exception as e:
        print(f"ERROR: Champ Select: Got error {e} while banning champion")

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
