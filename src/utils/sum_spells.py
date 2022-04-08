import asyncio
import logging

import eel
import utils.ddragon as ddragon
import utils.opgg as opgg
from dependancies import willump


async def set_sum_spells(client, champion):
    # Get spell names from opgg
    spell_names = await opgg.get_sum_spells(champion)

    # Flash should always be on F brother
    if spell_names[0] == "SummonerFlash":
        spell_names[0] = spell_names[1]
        spell_names[1] = "SummonerFlash"

    # Convert spell names to IDs
    spell_ids = []
    for spell in spell_names:
        spell_ids.append(ddragon.summoner_name_to_id(spell))

    # Set spell IDs
    set_sum_spells_result = await client.request('patch', "/lol-champ-select/v1/session/my-selection",
                                                 data={"spell1Id": spell_ids[0], "spell2Id": spell_ids[1]})

    if set_sum_spells_result.status == 204:
        logging.debug(f"Spell Generator: {champion} Spells Set! (Status {set_sum_spells_result.status})")
        eel.update_status_text(f"{champion} spells set")()
        eel.update_progressbar(100)()
    else:
        logging.error(f"Spell Generator: Spell application failed with status {set_sum_spells_result.status}")
        eel.update_status_text("Auto spells failed, check logs for more info")()


########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    willup = await willump.start()
    print(await set_sum_spells(willup, "darius"))
    willup.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
