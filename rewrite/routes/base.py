import webview

from flask import Blueprint, render_template

from bristle_instance import lcu


base_routes = Blueprint('base', __name__)


@base_routes.route("/")
async def hello_world():
    r = lcu.get('lol-summoner/v1/current-summoner')
    print(r.status_code)
    print(r.text)
    return render_template('index.html')


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
