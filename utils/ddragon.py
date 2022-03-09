import requests


# Queries latest ddragon patch for all other calls
def get_latest_version():
    r = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
    return r[0]


# Queries ddragon for champion name given an ID
def champ_id_to_name(champ_id):
    r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/champion.json').json()
    for champion in r['data'].items():
        if champion[1]['key'] == champ_id:
            return champion[1]['name']
    return None


# Queries ddragon for champion ID given a name
def champ_name_to_id(champ_name):
    r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/champion.json').json()
    for champion in r['data'].items():
        if champion[1]['name'] == champ_name:
            return champion[1]['key']
    return None


# Queries all champ names from ddragon
def get_all_champs():
    r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/champion.json').json()
    champs = []
    for champion in r['data']:
        champs.append(champion)
    return champs


# Queries ddragon for summoner spell ID given name
def summoner_name_to_id(summoner_name):
    r = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/summoner.json').json()
    for summoner in r['data'].items():
        if summoner[0] == summoner_name:
            return summoner[1]['key']
    return None



