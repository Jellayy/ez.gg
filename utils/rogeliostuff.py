import asyncio
import willump


async def get_summoner():
    wllp = await willump.start()
    response = await wllp.request('get', '/lol-summoner/v1/current-summoner')
    await wllp.close(wllp)
    return await response.json()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_summoner())
