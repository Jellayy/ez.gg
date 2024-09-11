import requests


def get_latest_version():
    r = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
    return r[0]


def get_all_champs():
    r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/champion.json').json()
    champs = []
    for champion in r['data'].items():
        champs.append(champion[1]['name'])
    return champs
