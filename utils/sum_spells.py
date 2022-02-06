import willump
import asyncio
import utils.opgg as opgg
import utils.ddragon as ddragon


async def set_sum_spells(champion):
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
    client = await willump.start()
    set_sum_spells_result = await client.request('patch', "/lol-champ-select/v1/session/my-selection",
                                                 data={"spell1Id": spell_ids[0], "spell2Id": spell_ids[1]})
    await client.close()
    return set_sum_spells_result


########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    print(await set_sum_spells("darius"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())