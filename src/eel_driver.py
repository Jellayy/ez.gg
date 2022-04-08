import asyncio
import platform
import sys
import threading
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import eel

from champselect import websockets
from utils import ddragon, runes, sum_spells, summoner_info, champ_identifier


# Rune Generator Functions
@eel.expose
def wait_for_champ_select():
    asyncio.run(champ_identifier.wait_for_champ_select())


@eel.expose
def get_champion_pick():
    pick = asyncio.run(champ_identifier.get_champion_pick())
    return pick


@eel.expose
def set_rune_page(champ):
    asyncio.run(runes.set_rune_page(champ))


@eel.expose
def set_sum_spells(champ):
    asyncio.run(sum_spells.set_sum_spells(champ))


@eel.expose
def get_all_champs():
    return ddragon.get_all_champs()


# @eel.expose
# def get_summoner_info():
#     return asyncio.run(summoner_info.get_summoner())


def worker(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websockets.main())


@eel.expose
def run_autopilot():
    pass


# Start Logging
home_folder = str(Path.home())
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(f"{home_folder}/ezgg-logs.txt", maxBytes=5000000, backupCount=1),
        logging.StreamHandler()
    ]
)
logging.getLogger("geventwebsocket.handler").disabled = True
logging.getLogger("asyncio").disabled = True
logging.getLogger("urllib3.connectionpool").disabled = True
logging.info('logging started')

# Start websockets
loop = asyncio.new_event_loop()
websocket = threading.Thread(name='websocket', target=worker, args=(loop,))
websocket.daemon = True
websocket.start()

# eel init
eel.init('utils/ui', allowed_extensions=['.js', '.html'])

try:
    eel.start('main.html', size=(1000, 600))
except EnvironmentError:
    # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
    if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        eel.start('main.html', mode='edge', size=(1000, 600))
    else:
        raise
