import asyncio
from asyncio import sleep

import willump

import champselect.preferences as preferences


async def create_lobby(client):
    queueType = {"queueId": preferences.queueID}
    call = '/lol-lobby/v2/lobby'
    create_lobby = await client.request('POST', '/lol-lobby/v2/lobby', data=queueType)
    if create_lobby.status == 200:
        print('Successfully created queue ID ', preferences.queueID)
    else:
        print("Failed to create queue type ", preferences.queueID)
        print("Error code:", create_lobby.status)
        error = await create_lobby.json()
        print(error.get('message'))


async def select_roles(client):
    call = '/lol-lobby/v2/lobby/members/localMember/position-preferences'
    positions = {"firstPreference": preferences.primaryRole,
                 "secondPreference": preferences.secondaryRole}
    roles = await client.request('PUT', call, data=positions)
    if roles.status == 201:
        print("Assigned roles, primary:", preferences.primaryRole, " secondary:", preferences.secondaryRole)
    else:
        print("Assigning roles failed, primary:", preferences.primaryRole, " secondary:", preferences.secondaryRole)
        print("Error code:", roles.status)
        error = await roles.json()
        print(error.get("message"))


async def start_queue(client):
    call = '/lol-lobby/v2/lobby/matchmaking/search'
    queue = await client.request('POST', call)
    if queue.status == 204:
        print("Started queue")
    elif not await can_start(client):
        print("Failed to start queue")
        print(queue.status)
        print("Clearing notification")
        print("Waiting for dodge timer to be over in ", await penalty_time(client), " seconds")
        time = await penalty_time(client) + 1
        await sleep(time)
        print("Trying to start queue again")
        await start_queue(client)
    else:
        print(queue.status)


async def queue_type(client):
    call = '/lol-lobby/v1/parties/gamemode'
    queue = await client.request('GET', call)
    data = await queue.json()
    if queue.status == 404:
        print("You are not currently in a lobby")
        return False
    elif queue.status == 200:
        print("You are in lobby type", data['queueId'])
    return data['queueId']


async def queue_pop(client):
    call = '/lol-matchmaking/v1/ready-check'
    lamequeue = await client.request("GET", call)
    response = await lamequeue.json()
    message = response.get("message")
    state = response.get("state")
    if lamequeue.status == 404:
        print("You are not currently in queue")
        print("Error: ", message)
    elif state == "Invalid":
        print("The queue has not popped yet")
        return False
    elif state == "InProgress":
        print("The queue is in progress and ready to be accepted")
        return True
    else:
        print("Yikes, we shouldn't be here")


async def queue(client):
    if not await queue_pop(client):
        print("The queue has not popped yet, waiting 5 seconds before querying again")
        await sleep(5)
        await queue(client)
        return False
    elif await queue_pop(client):
        print("Queue has popped, preparing to accept")
        await accept_queue(client)
        return True


async def accept_queue(client):
    call = '/lol-matchmaking/v1/ready-check/accept'
    accept = await client.request('POST', call)
    response = await accept.json()
    # message = response.get("message")
    if accept.status == 500:
        print("Not only has the ready check not popped, you're not even in queue, and frankly are super lost")
        # print("Error: ", message)
    elif accept.status == 404:
        print("Not in queue")
        # print("Error: ", message)
    else:
        print("Queue has been accepted")


async def is_lobby_leader(client):
    call = '/lol-lobby/v2/lobby'
    lobby = await client.request('GET', call)
    response = await lobby.json()
    localmember = response.get("localMember")
    leader = localmember.get("isLeader")
    print(leader)
    if leader:
        return True
    elif not leader:
        return False


async def is_champ_select(client):
    call = '/lol-champ-select/v1/session'
    champselect = await client.request('GET', call)
    response = await champselect.json()
    if champselect.status == 404:
        return False
    elif champselect.status == 200:
        return True


async def can_start(client):
    call = '/lol-lobby/v2/lobby/matchmaking/search-state/'
    lobby = await client.request('GET', call)
    response = await lobby.json()
    error = response.get('errors')
    print(response)
    print(error)
    if not error:
        print("Can start queue")
        return True
    elif error:
        print("Cannot start queue")
        return False


async def penalty_time(client):
    call = '/lol-lobby/v2/lobby/matchmaking/search-state/'
    lobby = await client.request('GET', call)
    response = await lobby.json()
    error = response.get('errors')
    timeleft = error[0]['penaltyTimeRemaining']
    return timeleft


async def is_in_queue(client):
    call = '/lol-lobby/v2/lobby/matchmaking/search-state'
    lobby = await client.request('GET', call)
    response = await lobby.json()
    state = response.get('searchState')
    print(state)
    if state == "Searching":
        await queue(client)
        return True
    elif state == "Invalid":
        return False


async def is_lobby(client):
    call = '/lol-lobby/v2/lobby'
    lobby = await client.request('GET', call)
    print(lobby.status)
    if lobby.status == 200:
        return True
    elif lobby.status == 404:
        return False


async def is_lobby(client):
    call = '/lol-lobby/v2/lobby'
    lobby = await client.request('GET', call)
    print(lobby.status)
    if lobby.status == 200:
        return True
    elif lobby.status == 404:
        return False


async def lobby(client):
    call = '/lol-lobby-team-builder/champ-select/v1/session'
    lobby = await client.request('GET', call)
    data = await lobby.json()
    print(data)
    print(data['localPlayerCellId'])
    return data['localPlayerCellId']


async def pick_champ(client, actorcellid):
    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}'
    pick = await client.request('PATCH', call, data={
        "actorCellId": actorcellid,
        "championId": 1,
        "type": "pick"
    })
    print(await pick.json())


async def lock_in(client, actorcellid):
    call = f'/lol-lobby-team-builder/champ-select/v1/session/actions/{actorcellid}/complete'
    locked = await client.request('POST', call)
    print(await locked.json())
