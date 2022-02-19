import asyncio
from asyncio import sleep
import utils.runes as runes
from champselect import state_engine
import willump


from champselect import functions


async def main():

    # await state_engine.create_lobby()
    # await state_engine.start_queue()
    # await state_engine.auto_queue_accept()
    # await state_engine.instalock_champ()

    # await state_engine.pick_champ()
    # await state_engine.ban_champ()
    # # await state_engine.get_gameflow()
    # await runes.set_rune_page("udyr")

    async def get_player_id(client):
        call = '/lol-lobby-team-builder/champ-select/v1/session'
        lobby = await client.request('GET', call)
        if lobby.status == 200:
            data = await lobby.json()
            # print(data)
            # print(data['localPlayerCellId'])
            user_id = 0
            for crap in data['actions']:
                # print(crap)
                for player in crap:
                    # print(player)
                    if player['actorCellId'] == data['localPlayerCellId']:
                        # print(player['id'])
                        user_id = player['id']
            # print(user_id)
            return user_id
        else:
            print(await lobby.json())

    client = await willump.start()
    await get_player_id(client)
    await willump.Willump.close(client)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())