import asyncio
import platform
import sys
import threading
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
import requests
import os
import psutil
import base64

import eel

from champselect import websockets
from utils import ddragon, runes, sum_spells, summoner_info, champ_identifier

@eel.expose
def get_ranked_names():
    # Find the LeagueClient.exe process and extract the required information
    for process in psutil.process_iter():
        if process.name() == 'LeagueClient.exe':
            port = process.cmdline()[2].split('=')[1]
            auth_key = process.cmdline()[1].split('=')[1]
            break

    # Create URL and headers for the request
    url = f'https://127.0.0.1:{port}/chat/v5/participants/champ-select'
    headers = {
        'Authorization': f"Basic {base64.b64encode(f'riot:{auth_key}'.encode()).decode()}",
        'Accept': 'application/json'
    }

    # Get the response from the server
    response = requests.get(url=url, headers=headers, verify=r"{}\riotgames.pem".format(os.getcwd()))

    # Parse the JSON response and extract the names
    response_data = json.loads(''.join(chunk.decode() for chunk in response))
    names = [participant['name'] for participant in response_data['participants']]

    return names

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


@eel.expose
def get_version():
    return "Beta v0.1.1"


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
