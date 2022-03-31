import eel
import willump
import json
from utils import runes, sum_spells, ddragon
import asyncio
from champselect import functions
import champ_identifier
import logging
from champselect import champ_select_functions


async def default_message_handler(data):
    pass


async def printing_listener(data):
    # print(data['eventType'] + ' ' + data['uri'])
    # print(json.dumps(data, indent=4, sort_keys=True))
    f = open("champselect/yeet1.txt", "a")
    f.write(data['eventType'] + ' ' + data['uri'] + "\n" + json.dumps(data, indent=4, sort_keys=True) + "\n")


async def queue_acceptor(data):


        try:
            if data['data']['playerResponse'] == 'None':
                if eel.get_queue_preference()():
                    print("Accepting queue")
                    await functions.accept_queue(wllp)
        except:
            print("lmao idk wtf went wrong, not my problem tbh")


async def position_listener(data):
    try:
        if eel.get_lock_in_preference()():
        # print(data['eventType'] + ' ' + data['uri'])
        # if data['data']['localMember']['firstPositionPreference'] == "UNSELECTED" or data['data']['localMember'][
        #     'secondPositionPreference'] == "UNSELECTED":
            await functions.select_roles(wllp)
            # await functions.start_queue(wllp)
    except:
        print("at least it's broken and you know it frikkin gays")



async def summoner_listener(data):

    # print('are here')
    try:
        # print(data['data'])
        # print(data['eventType'] + ' ' + data['uri'])
        if data['data']['isSelf'] and data['data']['isPickIntenting']:
            print("Pick Intenting Champion")
            await champ_select_functions.hover_champ()

        if data['data']['isSelf'] and data['data']['activeActionType'] == "ban":
            print("Banning Champion")
            await champ_select_functions.ban_champ()

        if data['data']['isSelf'] and data['data']['activeActionType'] == "pick":
            print("Picking Champion")
            await champ_select_functions.pick_champ()
        if data['data']['isSelf'] and data['data']['areSummonerActionsComplete']:
            print("Generating Runes")
            pick = await champ_identifier.get_champion_pick()
            await runes.set_rune_page(pick)
            await sum_spells.set_sum_spells(pick)
    except:
        print("something went wrong in summoner listener with data")

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
    global wllp
    wllp = await willump.start()

    all_events_subscription = await wllp.subscribe('OnJsonApiEvent', default_handler=printing_listener)

    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-lobby/v2/lobby', handler=position_listener)

    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-matchmaking/v1/ready-check',
                                      handler=queue_acceptor)

    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/summoners/',
                                      handler=summoner_listener)
    # wllp.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/session',
    #                                   handler=report_listener)


    while True:
        await asyncio.sleep(10)


if __name__ == '__main__':
    # uncomment this line if you want to see willump complain (debug log)
    logging.basicConfig(level=logging.NOTSET)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(wllp.close())
        print()
