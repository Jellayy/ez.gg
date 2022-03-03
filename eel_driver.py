import eel
import asyncio
import champ_identifier
from utils import runes, sum_spells
from configparser import ConfigParser


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
def autopilot_settings(setting, value):
    config = ConfigParser()
    config.read('utils\\autopilot.ini')
    if setting == 'primary_role':
        config.set('AUTOPILOT', 'primaryrole', value)
    elif setting == 'secondary_role':
        config.set('AUTOPILOT', 'secondaryrole', value)
    elif setting == 'queueaccept':
        config.set('AUTOPILOT', 'queueaccept', str(value))
    elif setting == 'lockin':
        config.set('AUTOPILOT', 'lockin', str(value))
    with open('utils\\autopilot.ini', 'w') as f:
        config.write(f)


# eel init
eel.init('utils/ui', allowed_extensions=['.js', '.html'])
eel.start('main.html', size=(1000, 600))