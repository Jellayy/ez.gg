import webview
import logging

from flask import Blueprint, render_template, redirect, jsonify
from bristle import Bristle

from initialize import lcu


base_routes = Blueprint('base', __name__)


@base_routes.route("/")
async def home():
    return render_template('pages/base.html')


@base_routes.route("/lcu_detect")
async def lcu_detect():
    return jsonify(lcu.lcu_found)


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
