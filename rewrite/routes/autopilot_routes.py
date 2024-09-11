from flask import Blueprint, render_template, jsonify, request, Response

from initialize import lcu, scuttle
from ddragon import get_all_champs


autopilot_routes = Blueprint('autopilot', __name__)


@autopilot_routes.route("/autopilot")
async def autopilot():
    if lcu.lcu_found:
        profile = lcu.get('lol-summoner/v1/current-summoner')
        return render_template(
            'autopilot.html',
            profile=profile.json(),
        )
    else:
        return render_template('no_lcu.html')


@autopilot_routes.route("/autopilot/all_champions_list")
async def all_champions_list():
    champions = get_all_champs()
    return jsonify(champions)


@autopilot_routes.route("/autopilot/update_settings", methods=['POST'])
async def update_settings():
    data = request.data

    scuttle.update_config_from_json('autopilot', data)

    return jsonify({
        'status': 'success'
    })


@autopilot_routes.route("/autopilot/load_settings")
async def load_settings():
    data = scuttle.get_config_as_json('autopilot')
    return jsonify(data)
