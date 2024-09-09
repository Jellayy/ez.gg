import webview
import logging

from flask import Blueprint, render_template, redirect
from bristle import Bristle

from initialize import lcu


base_routes = Blueprint('base', __name__)


@base_routes.route("/")
async def home():
    if lcu.lcu_found:
        profile = lcu.get('lol-summoner/v1/current-summoner')
        in_lobby = lcu.get('lol-lobby/v2/party-active')
        lobby_members = lcu.get('lol-lobby/v2/comms/members')
        logging.info(lobby_members.json())
        return render_template(
            'index.html',
            profile=profile.json(),
            in_lobby = in_lobby.json(),
            lobby_members=lobby_members.json()
        )
    else:
        return render_template('no_lcu.html')


@base_routes.route("/re_search_lcu", methods=['POST'])
async def re_search_lcu():
    logging.info("UI POST called for an LCU re-search")
    global lcu
    lcu = Bristle()
    return redirect("/")


@base_routes.route('/exit', methods=['POST'])
async def exit():
    logging.info("Exited via UI POST call")
    webview.windows[0].destroy()
    return '', 204


@base_routes.route('/minimize', methods=['POST'])
async def minimize():
    logging.info("Minimized via UI POST call")
    webview.windows[0].minimize()
    return '', 204
