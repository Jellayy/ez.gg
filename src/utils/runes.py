import asyncio
import eel
import utils.opgg as opgg
from dependancies import willump


# Queries the local LCU API for the ID of the currently selected rune page
async def get_current_page_id(client):
    current_page = await client.request('get', '/lol-perks/v1/currentpage')
    page_json = await current_page.json()
    return page_json['id']


# Uses op.gg scraper and local LCU API to update current rune page with recommended for a given champion
async def set_rune_page(client, champion):
    current_page_id = await get_current_page_id(client)
    new_rune_ids = await opgg.get_rune_page(champion)
    selected_perk_ids = [new_rune_ids[0], new_rune_ids[1], new_rune_ids[2], new_rune_ids[3], new_rune_ids[4],
                         new_rune_ids[5], new_rune_ids[6], new_rune_ids[7], new_rune_ids[8]]
    primary_style_id = new_rune_ids[9]
    sub_style_id = new_rune_ids[10]
    set_rune_page_result = await client.request('put', "/lol-perks/v1/pages/" + str(current_page_id),
                                                data={'name': f"EZ.GG: {champion}", 'primaryStyleId': primary_style_id,
                                                      'selectedPerkIds': selected_perk_ids, 'subStyleId': sub_style_id})
    # Error Handling for non-editable default page selected
    if set_rune_page_result.status == 201:
        print(f"Rune Generator: {champion} Runes Set! (Status {set_rune_page_result.status})")
        eel.update_status_text(f"{champion} runes set")()
        eel.update_progressbar(75)()
    elif set_rune_page_result.status == 404:
        print(
            f"ERROR: Rune Generator: Status {set_rune_page_result.status} when setting rune page! (Do you have a non-editable default page selected?)")
        eel.update_status_text("Cannot set rune page, select an editable rune page")()
    else:
        print(f"ERROR: Rune Generator: Rune page application failed with status {set_rune_page_result.status}")
        eel.update_status_text("Rune generation failed, check logs for more info")()


########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    willup = await willump.start()
    result = await set_rune_page(willup, "draven")
    # if result:
    #     print("Rune Page Set")
    # else:
    #     print("Error - Default page selected")
    await willup.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
