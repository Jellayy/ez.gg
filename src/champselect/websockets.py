import eel

from utils import runes, sum_spells
import asyncio
from dependancies import willump
from champselect import functions, champ_select_functions
import logging

# Used for testing mode (bypasses ui checks)
testing = False


async def default_message_handler(data):
    pass


async def printing_listener(data):
    # print(data['eventType'] + ' ' + data['uri'])
    # print(json.dumps(data, indent=4, sort_keys=True))
    # f = open("champselect/yeet1.txt", "a")
    # f.write(data['eventType'] + ' ' + data['uri'] + "\n" + json.dumps(data, indent=4, sort_keys=True) + "\n")
    pass


# Handler for Queue Pop Websocket Filter
async def queue_acceptor(data):
    try:
        # Check if Queue is not already accepted
        if data['data']['playerResponse'] == 'None':
            print("Queue Acceptor: Queue Pop Detected")
            # Check if Auto Queue Accept is enabled or in testing mode
            if testing or eel.get_queue_preference()():
                print("Queue Acceptor: Auto Accepting Queue...")
                # Send Queue Accept Request
                await functions.accept_queue(client)
            else:
                print("Queue Acceptor: Auto Queue Accept Not Enabled")

    except TypeError:
        # No data given with call
        print("WARNING: Queue Acceptor called without queue popped (This is normal)")


# TODO: Actually implement auto role selecting properly
# async def position_listener(data):
    # try:
    #     if eel.get_lock_in_preference()():
    #     # print(data['eventType'] + ' ' + data['uri'])
    #     # if data['data']['localMember']['firstPositionPreference'] == "UNSELECTED" or data['data']['localMember'][
    #     #     'secondPositionPreference'] == "UNSELECTED":
    #         await functions.select_roles(client)
    #         # await functions.start_queue(client)
    # except:
    #     print("at least it's broken and you know it frikkin gays")


# Handler for champ select events filter
async def champ_select(data):
    try:
        # Persistent value for tracking rune page status
        global runes_set

        # TODO: Implement auto champion picks (currently uses old preferences file)
        # Hover Stage
        if data['data']['isSelf'] and data['data']['isPickIntenting']:
            print("Champ Select: Hovering Stage")
            # Check if Auto Lock In enabled or in testing mode
            if testing or eel.get_lock_in_preference()():
                print("Champ Select: Hovering Champion...")
                await champ_select_functions.hover_champ()
            else:
                print("Champ Select: Not Hovering - Auto Lock-In Not Enabled")

        # Banning Stage
        if data['data']['isSelf'] and data['data']['activeActionType'] == "ban" and data['data']['banIntentSquarePortratPath'] == "":
            print("Champ Select: Banning Stage")
            # Check if Auto Ban enabled or in testing mode
            if testing or eel.get_auto_ban_preference()():
                # Send Champion Ban Request
                print("Champ Select: Auto-Banning Champion...")
                await champ_select_functions.ban_champ(client)
            else:
                print("Champ Select: Auto-Ban Not Enabled")

        # TODO: Implement auto champion picks (currently uses old preferences file)
        # Pick Stage
        if data['data']['isSelf'] and data['data']['activeActionType'] == "pick":
            print("Champ Select: Pick Stage")
            if eel.get_lock_in_preference()():
                await champ_select_functions.pick_champ()
            else:
                print("Champ Select: Not Locking In - Auto Lock-In Not Enabled")

            # Reset rune page tracking
            runes_set = False

        # Rune Generation
        if data['data']['isSelf'] and data['data']['isDonePicking'] and not runes_set:
            if eel.get_runes_preference()():
                # Get champion
                pick = data['data']['championName']
                print("Champ Select: Setting Runes...")
                await runes.set_rune_page(client, pick)
                print("Champ Select: Setting Spells...")
                await sum_spells.set_sum_spells(client, pick)
                runes_set = True

    except TypeError:
        print("ERROR: Champ Select: NO DATA - This should never happen tbh")
    except:
        print("bad things")

# async def report_listener(data):
#     try:
#         reports = []
#         for puids in data['data']['myTeam']:
#             reports.append(puids['summonerId'])
#
#         print(reports)
#         await champ_select_functions.report_champ_select(wllp, reports)
#     except:
#         print("something went wrong with report listener")


async def main():
    print("Autopilot: Autopilot Enabled")

    global runes_set
    runes_set = False

    # Willump Client
    global client
    client = await willump.start()

    # All client events websocket subscription
    all_events_subscription = await client.subscribe('OnJsonApiEvent', default_handler=printing_listener)

    # Lobby Filter
    # client.subscription_filter_endpoint(all_events_subscription, '/lol-lobby/v2/lobby', handler=position_listener)

    # Queue Pop Filter
    client.subscription_filter_endpoint(all_events_subscription, '/lol-matchmaking/v1/ready-check', handler=queue_acceptor)

    # Champ select event filter
    client.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/summoners/', handler=champ_select)

    # client.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/session', handler=report_listener)

    # Keep alive for websocket process
    while True:
        await asyncio.sleep(10)


# Outside of UI Testing Function
if __name__ == '__main__':
    # Disable UI checks
    testing = True

    # uncomment this line if you want to see willump complain (debug log)
    logging.basicConfig(level=logging.NOTSET)

    # Open loop and run until keyboard interrupt
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
        print()
