import willump
import json
import asyncio
from champselect import functions

async def default_message_handler(data):
    # print(data['eventType'] + ' ' + data['uri'])
    pass


async def printing_listener(data):

    print(data['eventType'] + ' ' + data['uri'])
    print(json.dumps(data, indent=4, sort_keys=True))

async def queue_acceptor(data):
    print(data['eventType'] + ' ' + data['uri'])
    print(json.dumps(data, indent=4, sort_keys=True))
    await functions.accept_queue(wllp)




async def main():
    global wllp
    wllp = await willump.start()



    all_events_subscription = await wllp.subscribe('OnJsonApiEvent', default_handler=default_message_handler)

    wllp.subscription_filter_endpoint(all_events_subscription, '/lol-matchmaking/v1/ready-check', handler=queue_acceptor)


    while True:
        await asyncio.sleep(10)


if __name__ == '__main__':
    # uncomment this line if you want to see willump complain (debug log)
    # logging.basicConfig(level=logging.NOTSET)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(wllp.close())
        print()
