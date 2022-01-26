import willump
import asyncio
import utils.opgg as opgg


# Queries the local LCU API for the ID of the currently selected rune page
async def get_current_page_id(client):
    current_page = await client.request('get', '/lol-perks/v1/currentpage')
    page_json = await current_page.json()
    return page_json['id']


# Uses op.gg scraper and local LCU API to update current rune page with recommended for a given champion
async def set_rune_page(champion):
    client = await willump.start()
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
    set_rune_page_result = await set_rune_page_result.json()
    await willump.Willump.close(client)
    if set_rune_page_result is None:
        return True
    else:
        return False


########################################################################################################################
# TESTING
########################################################################################################################
async def main():
    result = await set_rune_page("draven")
    if result:
        print("Rune Page Set")
    else:
        print("Error - Default page selected")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
