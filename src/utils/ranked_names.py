import asyncio
import eel
from dependancies import willump

async def get_ranked_names_async():
    client = await willump.start()
    response = await client.request('get', '/chat/v5/participants/champ-select')
    print(f"Response status: {response.status}")
    print(f"Response text: {response.text}")
    data = await response.json()
    print(data)
    await willump.Willump.close(client)
    return data

@eel.expose
def get_ranked_names():
    return asyncio.run(get_ranked_names_async())

async def main():
    await get_ranked_names_async()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
