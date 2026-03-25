import asyncio
from dependancies import willump


async def get_summoner(client):
    response = await client.request('get', '/lol-summoner/v1/current-summoner')
    return await response.json()


if __name__ == '__main__':
    summoner = asyncio.run(get_summoner())
    print(f"Account Name: {summoner['displayName']}\n"
          f"Level: {summoner['summonerLevel']}\n"
          f"Percent to next level: {summoner['percentCompleteForNextLevel']}\n"
          f"Summoner Icon ID: {summoner['profileIconId']}")
