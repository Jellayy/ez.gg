import asyncio
import requests
from dependancies import willump

async def get_ranked_names():
    client = await willump.start()
    team_names = await client.request('get', '/chat/v5/participants/champ-select')
    await willump.Willump.close(client)
    data = await team_names.json()
    print(data)
    return data

async def main():
    willup = await willump.start()
    await willup.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
