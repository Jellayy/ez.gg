import asyncio
from asyncio import sleep
import utils.runes as runes
from champselect import state_engine



from champselect import functions


async def main():

    # await state_engine.create_lobby()
    # await state_engine.start_queue()
    # await state_engine.auto_queue_accept()
    # await state_engine.instalock_champ()

    await state_engine.pick_champ()
    # await state_engine.ban_champ()
    await state_engine.get_gameflow()
    # await runes.set_rune_page("kalista")





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())