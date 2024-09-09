import webview

from flask import Flask

from routes import register_routes
from initialize import lcu


server = Flask(__name__, static_folder='./ui/static', template_folder='./ui/templates')

register_routes(server)


if __name__ == '__main__':
    webview.create_window('EZ.GG Experimental', server, frameless=True, height=760, width=500)
    webview.start(user_agent='EZ.GG Experimental', debug=True)
