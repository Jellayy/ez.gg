import webview

from flask import Blueprint, render_template, redirect
from bristle import Bristle

from bristle_instance import lcu


base_routes = Blueprint('base', __name__)


@base_routes.route("/")
async def home():
    if lcu.lcu_found:
        profile = lcu.get('lol-summoner/v1/current-summoner')
        print(profile.text)
        return render_template(
            'index.html',
            profile=profile.json()
        )
    else:
        return render_template('no_lcu.html')


@base_routes.route("/re_search_lcu", methods=['POST'])
async def re_search_lcu():
    global lcu
    lcu = Bristle()
    return redirect("/")


@base_routes.route('/exit', methods=['POST'])
def exit():
    print("exit called")
    webview.windows[0].destroy()
    return '', 204


@base_routes.route('/minimize', methods=['POST'])
def minimize():
    print("minimize called")
    webview.windows[0].minimize()
    return '', 204
