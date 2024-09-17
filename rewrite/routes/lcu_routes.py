from flask import Blueprint, render_template, jsonify, request, Response

from initialize import lcu


lcu_routes = Blueprint('lcu', __name__)


@lcu_routes.route("/lcu/profile")
def profile():
    profile = lcu.get('lol-summoner/v1/current-summoner')
    return render_template(
        'components/profile.html',
        profile=profile.json()
    )


@lcu_routes.route("/lcu/party")
def party():
    in_party = lcu.get('lol-lobby/v2/party-active').json()
    lobby_members = lcu.get('lol-lobby/v2/comms/members').json()

    # Grab icon IDs from separate endpoint
    if in_party:
        for member in lobby_members['players'].values():
            icon_id = lcu.get(f'lol-summoner/v2/summoner-icons?ids=%5B{member['summonerId']}%5D').json()[0]['profileIconId']
            member['icon_id'] = icon_id
    
    return render_template(
        'components/party.html',
        in_party=in_party,
        lobby_members=lobby_members
    )
