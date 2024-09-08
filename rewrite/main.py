import webview
import logging
import sys

from flask import Flask

from routes import register_routes
from bristle_instance import lcu


server = Flask(__name__, static_folder='./ui/static', template_folder='./ui/templates')

register_routes(server)


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    logging.info("Logging Started")

    webview.create_window('EZ.GG Experimental', server, frameless=True, height=760, width=500)
    webview.start(user_agent='EZ.GG Experimental', debug=True)
