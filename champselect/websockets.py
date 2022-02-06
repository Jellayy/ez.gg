import willump
import json
import asyncio
from champselect import functions
import logging
import preferences


async def default_message_handler(data):
    # print(data['eventType'] + ' ' + data['uri'])
    pass


async def printing_listener(data):
    print(data['eventType'] + ' ' + data['uri'])
    print(json.dumps(data, indent=4, sort_keys=True))


async def queue_acceptor(data):
    try:

        print(data['eventType'] + ' ' + data['data']['playerResponse'])
        print(json.dumps(data, indent=4, sort_keys=True))
        if data['data']['playerResponse'] == 'None':
            print("Accepting queue")
            await functions.accept_queue(wllp)
    except:
        print("lmao idk wtf went wrong, not my problem tbh")


async def position_listener(data):
    try:
        print("am here")
        print(data['eventType'] + ' ' + data['uri'])
        if  data['data']['localMember']['firstPositionPreference'] == "UNSELECTED" or data['data']['localMember'][
            'secondPositionPreference'] == "UNSELECTED":
            await functions.select_roles(wllp)
    except:
        print("at least it's broken and you know it frikkin gays")


async def main():
    global wllp
    wllp = await willump.start()

    all_events_subscription = await wllp.subscribe('OnJsonApiEvent', default_handler=default_message_handler)

    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-matchmaking/v1/ready-check',
                                      handler=queue_acceptor)
    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/session',
                                      handler=printing_listener)
    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-lobby/v2/lobby', handler=position_listener)

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