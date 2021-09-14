import requests


def champ_id_to_name(champ_id):
    r = requests.get('http://ddragon.leagueoflegends.com/cdn/11.17.1/data/en_US/champion.json').json()
    for champion in r['data'].items():
        if champion[1]['key'] == champ_id:
            return champion[1]['name']
    return None
